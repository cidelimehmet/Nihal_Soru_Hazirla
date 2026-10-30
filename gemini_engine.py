"""
Google Gemini Entegrasyonu ve MEB 2026 OYSS Soru Üretim Motoru - Genişletilmiş Sürüm
Yazılı Sınav, Etüt / Çalışma Kağıdı ve Yaprak Test (Çoktan Seçmeli) formatlarını destekler.
Sorularla birlikte kitap kaynağı, sayfa bilgisi, bilişsel düzey ve zorluk derecesini üretir.
"""

import os
import json
import re
import random
from config import get_config
from pdf_engine import extract_text_for_units
from curriculum_data import load_curriculum_dict, get_units, get_scenarios_for
from question_pools import (
    GRADE_SPECIFIC_POOLS,
    EXTRA_BEP_POOLS,
    synthesize_dynamic_questions_for_units,
    synthesize_dynamic_bep_questions_for_units
)

# Oturum boyunca sunulan soruların imzalarını tutarak art arda sınav hazırlamada aynı soruların gelmesini önler
_RECENT_SERVED_SIGNATURES: dict[str, list[str]] = {}


def _normalize_sig(text: str) -> str:
    """Soru metnini karşılaştırma için normalize eder."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text).strip().lower())


SYSTEM_INSTRUCTION = """
Sen, Millî Eğitim Bakanlığı (MEB) Ölçme, Değerlendirme ve Sınav Hizmetleri Genel Müdürlüğü ile Din Öğretimi Genel Müdürlüğü standartlarında uzmanlaşmış kıdemli bir İmam Hatip Ortaokulu Zümre Başkanısın.

GÖREVİN:
Verilen ders, sınıf, ünite ve sınav türüne göre MEB 2026 Türkiye Yüzyılı Maarif Modeli standartlarında sorular hazırlamaktır.

SINAV TÜRLERİ:
1. "yazili_sinav": 2026 MEB OYSS Açık Uçlu ve Kısa Cevaplı Sınavı. (Şans başarısı sıfır, analiz ve çıkarım odaklı, analitik rubrikli).
2. "etut_calisma": Öğrenci Etüt ve Çalışma Kağıdı. Açık uçlu sorular, kavram eşleştirme/yorumlama ve düşündürücü etkinlikler.
3. "yaprak_test": Çoktan seçmeli 4 seçenekli (A, B, C, D) yeni nesil bağlam temelli kazanım değerlendirme testi.
4. "bep_sinav": MEB Özel Eğitim Hizmetleri Yönetmeliği ve Ölçme Değerlendirme Yönergesi uyarınca BEP (Bireyselleştirilmiş Eğitim Programı) Kapsamındaki Öğrenci Sınavı.

BEP SINAVI ("bep_sinav") ÖZEL PEDAGOJİK VE TEKNİK KURALLARI:
- BEP'li öğrenciler genel sınıf senaryolarındaki karmaşık açık uçlu analiz sorularından muaftır.
- Soru köklerinde ASLA devrik, olumsuz ("Hangisi söylenemez?", "Hangisi çıkarılamaz?", "Hangisi değildir?"), çok bileşenli veya soyut ifadeler kullanılmaz! Yönergeler net, kısa ve olumlu olmalıdır ("Doğru olanı işaretleyiniz.", "Aşağıdaki kavramları anlamlarıyla eşleştiriniz.", "Kutucuktaki kelimelerden uygun olanı boşluğa yazınız.", "Cümlelerin başına Doğru ise (D), Yanlış ise (Y) yazınız.").
- Soru tipleri çeşitlendirilmelidir:
  a) Eşleştirme ("bep_eslestirme")
  b) Doğru-Yanlış ("bep_dogru_yanlis")
  c) Kelime Havuzlu Boşluk Doldurma ("bep_bosluk_doldurma" - kelimeler mutlaka üstte [Kelime Havuzu: ...] kutucuğu içinde verilmelidir)
  d) 3 Seçenekli Çoktan Seçmeli ("bep_coktan_secmeli_3" - sadece A, B, C seçenekleri olmalıdır, D seçeneği olmamalıdır!)
- Ders Bazında BEP Uyarlama:
  * DKAB: Soyut kader/fıkıh hesaplamaları yerine somut, günlük yaşamla bağdaşan kavramlar, Esmaül Hüsna eşleştirmeleri, temel ibadetler ve ahlaki davranışlar sorulur.
  * Peygamberimizin Hayatı (Siyer): Karmaşık savaş/siyasi antlaşma maddeleri yerine Peygamberimizin aile fertleri, temel ahlaki vasıfları (Muhammedü'l-Emin, doğruluk, merhamet, yetimleri koruma) ve temel olaylar (Mekke-Medine hicreti vb.) D/Y, kelime havuzlu boşluk doldurma veya 3 şıklı testle sorulur.
  * Kur'an-ı Kerim: Ağır tecvid tahlilleri yerine temel harf tanıma, harekeler (üstün, esre, ötre), bilinen surelerin (Fatiha, Kevser, İhlas vb.) isimleri/anlamları ve eksik kelime tamamlama sorulur.
- BEP Puanlama ve Rubrik: Yazım hataları ve el yazısı bozukluğundan puan kırılmaz; öğrencinin sorunun özünü kavradığını gösteren her doğru işaretlemeye tam puan verilir.

PEDAGOJİK STANDARTLAR:
- Din Kültürü (DKAB): Ezber tanım yerine hayatla bağ kurma, meal analizi, 8. sınıfta evren yasaları.
- Kur'an-ı Kerim: Tecvid kurallarının ayet üzerinde tespiti, Arapça metinlerin tam harekeli yazılması.
- Peygamberimizin Hayatı (Siyer): Hadis ve olayların günümüz ahlakıyla modellenmesi.
- Her soru için kitap sayfa aralığı, bilişsel düzey (Analiz / Yorumlama / Değerlendirme / Uygulama) ve zorluk (Kolay / Orta / Zor) belirtilmelidir.

ÇIKTI FORMATI (JSON):
Kesinlikle sadece aşağıdaki JSON şemasına uygun yanıt ver:
{
  "questions": [
    {
      "q_order": 1,
      "points": 10,
      "learning_outcome": "Kazanım açıklaması",
      "question_type": "acik_uclu",
      "cognitive_level": "Analiz",
      "difficulty": "Orta",
      "source_book": "Ders Kitabı Adı",
      "source_page": "Sayfa 45-48",
      "source_context": "Kitaptaki ilgili konunun pedagojik bağlamı ve alıntısı...",
      "arabic_text": "Varsa Arapça metin",
      "question_text": "Soru metni ve net yönerge...",
      "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "answer_text": "Beklenen örnek cevap veya doğru seçenek...",
      "rubric": [
        {"criterion": "Kriter 1", "points": 5},
        {"criterion": "Kriter 2", "points": 5}
      ]
    }
  ]
}
"""

def generate_questions_with_gemini(
    subject_id: str,
    grade: int,
    term: str,
    exam_no: str,
    scenario: str,
    question_count: int,
    selected_unit_ids: list[str],
    difficulty: str = "Dengeli",
    exam_type: str = "yazili_sinav",
    scenario_items: list[dict] | None = None,
    bep_options: dict | None = None,
    exclude_questions: list[str] | None = None
) -> dict:
    """Gemini API veya akıllı yerel motor ile zenginleştirilmiş ve tekrarsız soruları üretir."""
    cfg = get_config()
    api_key = cfg.get("gemini_api_key", "").strip()
    curr = load_curriculum_dict()
    bep_opts = bep_options or {}
    is_bep = (exam_type == "bep_sinav")
    exclude_list = [str(x).strip() for x in (exclude_questions or []) if str(x).strip()]

    # Eğer Özel/BEP senaryo değilse ve scenario_items boş gönderildiyse sistemdeki MEB senaryosundan otomatik çöz
    resolved_scenario_items = list(scenario_items) if scenario_items else []
    if not is_bep and not resolved_scenario_items and scenario and not str(scenario).startswith("Özel"):
        available_scenarios = get_scenarios_for(subject_id, grade, term)
        for sc in available_scenarios:
            sc_name = sc.get("name", "")
            sc_id_label = f"Senaryo {sc.get('scenario_id', 1)}"
            if sc_name == scenario or scenario.startswith(sc_id_label) or sc_name.startswith(scenario):
                resolved_scenario_items = sc.get("items", [])
                break
        if not resolved_scenario_items and available_scenarios:
            resolved_scenario_items = available_scenarios[0].get("items", [])

    all_units = get_units(subject_id, grade)

    # Eğer senaryo maddeleri varsa, üniteleri senaryodaki unit_no'lara göre de eşleştir
    if resolved_scenario_items and not selected_unit_ids:
        scen_unit_nos = {int(it.get("unit_no", 1)) for it in resolved_scenario_items}
        selected_unit_ids = [
            all_units[u_no - 1]["id"]
            for u_no in scen_unit_nos
            if 1 <= u_no <= len(all_units)
        ]

    book_context = extract_text_for_units(subject_id, grade, selected_unit_ids, max_chars=8000)
    subject_name = curr.get(subject_id, {}).get("name", subject_id)

    selected_units_objs = [u for u in all_units if u["id"] in selected_unit_ids] or all_units[:2]
    unit_names = [u["name"] for u in selected_units_objs]

    history_key = f"{subject_id}_{grade}_{exam_type}"
    recent_sigs = _RECENT_SERVED_SIGNATURES.get(history_key, [])

    scenario_prompt_block = ""
    if is_bep:
        bep_style = bep_opts.get("question_style", "karma")
        bep_custom_outcomes = (bep_opts.get("custom_outcomes") or "").strip()
        style_desc = {
            "karma": "Karma BEP Yapısı: 1 adet Eşleştirme, 1 adet Doğru-Yanlış (D/Y), 1 adet Kelime Havuzlu Boşluk Doldurma ve 1-2 adet 3 Seçenekli (A, B, C) Çoktan Seçmeli soru.",
            "coktan_secmeli_3": "Tamamı 3 Seçenekli (A, B, C) Çoktan Seçmeli BEP soruları (kesinlikle 3 şık: A, B, C).",
            "eslestirme_dy_bosluk": "Eşleştirme, Doğru-Yanlış (D/Y) ve Kelime Havuzlu Boşluk Doldurma soruları."
        }.get(bep_style, "Karma BEP soru tipleri")

        scenario_prompt_block = f"""
BU SINAV MEB ÖZEL EĞİTİM HİZMETLERİ YÖNETMELİĞİ KAPSAMINDA "BEP (BİREYSELLEŞTİRİLMİŞ EĞİTİM PROGRAMI)" ÖĞRENCİSİ İÇİN HAZIRLANMAKTADIR:
- MEB genel sınıf senaryolarındaki karmaşık açık uçlu analiz sorularından muaftır.
- İstenen Soru Tipi Dağılımı: {style_desc}
- Yönergeler çok sade, olumlu ve net olmalıdır ("Hangisi söylenemez/çıkarılamaz?" gibi olumsuz soru kökleri KESİNLİKLE YASAKTIR).
- Boşluk doldurma sorularında üstte mutlaka "📦 Kelime Havuzu: [ ... | ... ]" verilmelidir.
- Çoktan seçmeli sorularda "options" dizisinde SADECE 3 seçenek (A, B, C) yer almalıdır.
- Eşleştirme, Doğru-Yanlış ve Boşluk doldurma sorularında "options" dizisi boş `[]` bırakılmalı, maddeler `question_text` içinde net ve alt alta yazılmalıdır.
{f'- Öğrencinin Bireysel BEP Kazanım Hedefleri: {bep_custom_outcomes}' if bep_custom_outcomes else '- Seçili ünitelerdeki en temel, somut ve günlük yaşamla ilişkili BEP kazanımları esas alınmalıdır.'}
"""
    elif resolved_scenario_items:
        lines = []
        for idx, it in enumerate(resolved_scenario_items, 1):
            u_no = it.get("unit_no", 1)
            u_title = it.get("unit_title", "")
            o_code = it.get("outcome_code", "")
            o_desc = it.get("outcome_description", "")
            q_cnt = it.get("question_count", 1)
            lines.append(f"  {idx}. [{o_code}] ({u_no}. Ünite: {u_title}) -> {o_desc} [SORU ADEDİ: {q_cnt}]")
        scenario_prompt_block = (
            "\nMEB SENARYO KAZANIM VE SORU DAĞILIMI TABLOSU (KESİNLİKLE BU DAĞILIMA UYULACAKTIR):\n"
            + "\n".join(lines)
            + "\nHer sorunun 'learning_outcome' alanına ilgili kazanım kodunu ve açıklamasını (Örn: '[DKAB.5.1.1] ...') yaz.\n"
        )

    exam_type_label = (
        "BEP Kapsamındaki Öğrenci Sınavı (Özel Eğitim Uyarlamalı)" if is_bep
        else "MEB Ortak Yazılı Sınavı" if exam_type == "yazili_sinav"
        else "Çalışma / Etüt Kağıdı" if exam_type == "etut_calisma"
        else "Çoktan Seçmeli Yaprak Test"
    )

    exclusion_prompt_block = ""
    combined_exclude = list(dict.fromkeys(exclude_list + recent_sigs[-12:]))
    if combined_exclude:
        sample_excl = "\n".join(f"  - {q[:140]}..." for q in combined_exclude[:12])
        exclusion_prompt_block = (
            "\nSORU ÇEŞİTLİLİĞİ VE TEKRAR ÖNLEME KURALI:\n"
            "Daha önce sorulan aşağıdaki soruları, örnek olayları veya cümleleri KESİNLİKLE TEKRAR ETME! "
            "Tamamen farklı örnek olaylar, farklı isimler, farklı ayet/hadis örnekleri ve özgün bakış açıları kullan:\n"
            f"{sample_excl}\n"
        )

    variation_seed = random.randint(1000, 9999)
    user_prompt = f"""
Lütfen aşağıdaki parametrelere göre {question_count} adet ÖZGÜN ve FARKLI soru hazırla (Varyasyon Kodu: #{variation_seed}):

DERS: {subject_name}
SINIF: {grade}. Sınıf
SINAV TÜRÜ: {exam_type} ({exam_type_label})
DÖNEM / SINAV: {term} - {exam_no}
SENARYO: {'BEP Bireysel Kazanım Planı' if is_bep else scenario}
SORU SAYISI: {question_count}
ZORLUK SEVİYESİ: {'Kolay (BEP Somut / Temel Düzey)' if is_bep else difficulty}
KAPSAMDAKİ ÜNİTELER: {', '.join(unit_names)}
{scenario_prompt_block}
{exclusion_prompt_block}
DERS KİTABINDAN ÇIKARILAN BÖLÜMLER:
{book_context if book_context else 'Kitap konuları ve 2026 MEB Maarif Modeli kazanımları esas alınacaktır.'}

Her soru için kitap kaynağı, sayfa aralığı, bilişsel düzeyi, çözümü ve kısmi puanlama rubriğini eksiksiz doldur.
"""

    if api_key and api_key.startswith("AIza"):
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=api_key)
            preferred_model = cfg.get("gemini_model", "gemini-2.5-flash")
            candidate_models = [preferred_model]
            for fallback_m in ["gemini-2.5-flash", "gemini-2.0-flash"]:
                if fallback_m not in candidate_models:
                    candidate_models.append(fallback_m)
                    
            for model_name in candidate_models:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION,
                            response_mime_type="application/json",
                            temperature=0.75
                        )
                    )
                    text_resp = response.text.strip()
                    data = json.loads(text_resp)
                    if "questions" in data and len(data["questions"]) > 0:
                        if is_bep:
                            q_style_cfg = bep_opts.get("question_style", "karma")
                            for bq in data["questions"]:
                                bq_txt = str(bq.get("question_text") or "")
                                while "\n\n" in bq_txt:
                                    bq_txt = bq_txt.replace("\n\n", "\n")
                                bq["question_text"] = bq_txt.strip()
                                bq_type = str(bq.get("question_type") or "")
                                if q_style_cfg != "coktan_secmeli_3" and (
                                    bq_type in ("bep_eslestirme", "bep_dogru_yanlis", "bep_bosluk_doldurma")
                                    or "KELİME HAVUZU" in bq_txt
                                    or "( ..... )" in bq_txt
                                    or "(...)" in bq_txt
                                ):
                                    bq["options"] = []
                        _normalize_points(data["questions"])
                        for q in data["questions"]:
                            sig = _normalize_sig(q.get("question_text", ""))
                            if sig:
                                _RECENT_SERVED_SIGNATURES.setdefault(history_key, []).append(sig)
                        return data
                except Exception as inner_e:
                    print(f"Gemini model {model_name} attempt failed: {inner_e}")
                    continue
        except Exception as e:
            print(f"Gemini API error, falling back to smart local generator: {e}")

    if is_bep:
        return _generate_bep_fallback_questions(
            subject_id, grade, term, exam_no, question_count, selected_unit_ids, bep_opts, exclude_list
        )
            
    # Yerel zengin, sınıf/ünite duyarlı ve tekrarı önleyen MEB 2026 soru motoru
    return _generate_fallback_questions(
        subject_id, grade, term, exam_no, scenario, question_count, selected_unit_ids, exam_type, difficulty, resolved_scenario_items, book_context, exclude_list
    )

def _normalize_points(questions: list):
    if not questions:
        return
    count = len(questions)
    base_point = 100 // count
    remainder = 100 % count
    for i, q in enumerate(questions):
        p = base_point + (1 if i < remainder else 0)
        q["points"] = p
        q["q_order"] = i + 1

def _generate_fallback_questions(
    subject_id: str,
    grade: int,
    term: str,
    exam_no: str,
    scenario: str,
    question_count: int,
    selected_unit_ids: list[str],
    exam_type: str = "yazili_sinav",
    difficulty: str = "Dengeli",
    scenario_items: list[dict] | None = None,
    book_context: str = "",
    exclude_questions: list[str] | None = None
) -> dict:
    curr = load_curriculum_dict()
    subject_name = curr.get(subject_id, {}).get("name", "Din Kültürü ve Ahlak Bilgisi")
    book_name = f"{grade}. Sınıf {subject_name} MEB Ders Kitabı"
    is_test = (exam_type == "yaprak_test")
    q_type = "coktan_secmeli" if is_test else "acik_uclu"

    all_units = get_units(subject_id, grade)
    active_units = [u for u in all_units if u["id"] in selected_unit_ids] or all_units

    # 1. DİN KÜLTÜRÜ VE AHLAK BİLGİSİ (DKAB) ÖZEL HAVUZU (10 Özgün Soru)
    dkab_pool = [
        {
            "learning_outcome": "Kader ve evrenin yasaları ile tevekkül arasındaki ilişkiyi analiz eder.",
            "cognitive_level": "Analiz",
            "difficulty": "Orta",
            "source_page": "Sayfa 16-22",
            "source_context": "Evrendeki fiziksel, biyolojik ve toplumsal yasalar ile insanın cüz'i iradesi ve tevekkül bilinci karşılaştırmalı olarak ele alınmaktadır.",
            "arabic_text": "وَخَلَقَ كُلَّ شَيْءٍ فَقَدَّرَهُ تَقْدِيرًا",
            "question_text": "Ahmet Bey, tarlasına buğday ektikten sonra kuraklık yaşanmaması için damla sulama sistemi kurmuş ve gerekli gübrelemeyi yapmıştır. Komşusu Mehmet Bey ise 'Nasibimizde ne varsa o olur' diyerek hiçbir tedbir almamıştır. Bu durumu İslam'ın 'kader, irade ve tevekkül' anlayışı açısından karşılaştırarak açıklayınız.",
            "options": [
                "A) Her ikisi de doğru tevekkül anlayışı sergilemiştir.",
                "B) Ahmet Bey sebeplere sarılarak doğru tevekkül etmiş, Mehmet Bey ise sorumluluğunu ihmal etmiştir.",
                "C) Mehmet Bey'in davranışı kadere tam teslimiyeti gösterir.",
                "D) Tarımda tevekkülün yeri yoktur, yalnızca çalışmak yeterlidir."
            ],
            "answer_text": "Doğru tevekkül Ahmet Bey'in yaptığı gibi üzerine düşen tüm önlemleri aldıktan sonra sonucu Allah'a bırakmaktır. Mehmet Bey ise cüz'i iradesini kullanmayarak kaderi yanlış yorumlamıştır.",
            "rubric": [
                {"criterion": "Tevekkül kavramının tedbir + Allah'a güven olarak doğru tanımlanması", "points": 5},
                {"criterion": "Ahmet ve Mehmet Bey'in tutumlarının irade ve sorumluluk açısından karşılaştırılması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Evrenin yasalarını (fiziksel, biyolojik, toplumsal) örneklerle ayırt eder.",
            "cognitive_level": "Yorumlama",
            "difficulty": "Kolay",
            "source_page": "Sayfa 24-29",
            "source_context": "Yüce Allah'ın evrene koyduğu ölçü ve düzen (sünnetullah) fiziksel, biyolojik ve toplumsal yasalar başlıklarında incelenir.",
            "arabic_text": "",
            "question_text": "1) Suyun deniz seviyesinde 100 derecede kaynaması\n2) Balıkların suda solungaçlarıyla solunum yapması\n3) Adaletin ve güvenin sarsıldığı toplumlarda huzurun bozulması\nYukarıdaki öncüllerin sırasıyla hangi evrensel yasalara (fiziksel, biyolojik, toplumsal) örnek olduğunu gerekçeleriyle yazınız.",
            "options": [
                "A) 1: Fiziksel - 2: Biyolojik - 3: Toplumsal",
                "B) 1: Biyolojik - 2: Fiziksel - 3: Toplumsal",
                "C) 1: Toplumsal - 2: Biyolojik - 3: Fiziksel",
                "D) 1: Fiziksel - 2: Toplumsal - 3: Biyolojik"
            ],
            "answer_text": "1. öncül madde ve enerjinin yapısıyla ilgili olduğu için Fiziksel Yasa; 2. öncül canlıların yapısıyla ilgili olduğu için Biyolojik Yasa; 3. öncül insan ilişkileriyle ilgili olduğu için Toplumsal Yasadır.",
            "rubric": [
                {"criterion": "Fiziksel ve biyolojik yasaların doğru eşleştirilip açıklanması", "points": 5},
                {"criterion": "Toplumsal yasanın neden-sonuç ilişkisiyle açıklanması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Zekât ve sadakanın bireysel ve toplumsal dayanışmadaki önemini değerlendirir.",
            "cognitive_level": "Değerlendirme",
            "difficulty": "Orta",
            "source_page": "Sayfa 42-50",
            "source_context": "İslam'da paylaşma ve yardımlaşma ibadetleri (zekât, infak, sadaka ve sadaka-i cariye) ile toplumsal barış ilişkisi vurgulanmaktadır.",
            "arabic_text": "",
            "question_text": "İslam dininde zenginlerle yoksullar arasında bir gönül köprüsü kuran zekât ve sadaka ibadetlerinin; bireyin ahlaki gelişimine ve toplumsal huzura sağladığı katkılardan iki tanesini açıklayınız.",
            "options": [
                "A) Yalnızca maddi serveti azaltır.",
                "B) Bireyi cimrilikten korur, toplumda gelir dağılımını dengeleyerek sevgi ve kardeşliği güçlendirir.",
                "C) Sadece yakın akrabalar arasındaki iletişimi artırır.",
                "D) Yardımlaşmayı yalnızca Ramazan ayıyla sınırlandırır."
            ],
            "answer_text": "1) Bireyi cimrilik ve bencillik hastalığından arındırıp şükür bilinci kazandırır. 2) Zengin ile yoksul arasındaki uçurumu azaltarak kıskançlık yerine sevgi ve toplumsal barışı tesis eder.",
            "rubric": [
                {"criterion": "Bireysel faydasının (cimrilikten korunma, şükür bilinci) açıklanması", "points": 5},
                {"criterion": "Toplumsal faydasının (gelir dengesi, kardeşlik ve huzur) açıklanması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Maun suresinin mealinden hareketle ibadet ve ahlak bütünlüğünü analiz eder.",
            "cognitive_level": "Analiz",
            "difficulty": "Zor",
            "source_page": "Sayfa 60-66",
            "source_context": "Maun Suresi'nde yetim ve yoksul hakkını gözetmeyen, ibadetlerinde gösteriş (riya) yapan kimselerin tutumu eleştirilmektedir.",
            "arabic_text": "أَرَأَيْتَ الَّذِي يُكَذِّبُ بِالدِّينِ ۝ فَذَٰلِكَ الَّذِي يَدُعُّ الْيَتِيمَ",
            "question_text": "Maun Suresi'nde kınanan ve İslam ahlakıyla bağdaşmayan insan tutum ve davranışları nelerdir? Surenin mesajını dikkate alarak 3 temel davranışı maddeler halinde yazınız.",
            "options": [
                "A) Ticaret yapmak, yolculuğa çıkmak ve dinlenmek",
                "B) Yetimi itip kakmak, yoksulu doyurmaya teşvik etmemek ve namazlarında gösteriş (riya) yapıp yardıma engel olmak",
                "C) Nafile ibadetleri az yapmak ve sessiz dua etmek",
                "D) Yalnızca kendi ailesine harcama yapmak"
            ],
            "answer_text": "1) Yetimi itip kakmak ve hakkını yemektir. 2) Yoksulu doyurmaya önayak olmamaktır. 3) Namazlarını ciddiyetten uzak ve gösteriş (riya) için kılıp en küçük yardımı (maun) dahi esirgemektir.",
            "rubric": [
                {"criterion": "Yetim ve yoksul hakkına dair eleştirilerin doğru yazılması", "points": 5},
                {"criterion": "İbadette riyakarlık (gösteriş) ve yardıma engel olma davranışının belirtilmesi", "points": 5}
            ]
        },
        {
            "learning_outcome": "Dinin temel gayelerini (Zarûrât-ı Diniyye) günlük hayattan örneklerle açıklar.",
            "cognitive_level": "Uygulama",
            "difficulty": "Orta",
            "source_page": "Sayfa 76-84",
            "source_context": "İslam dininin emir ve yasaklarının temel amacı; Canın, Aklın, Dinin, Malın ve Neslin korunması (Zarûrât-ı Hamse) ilkelerine dayanır.",
            "arabic_text": "",
            "question_text": "İslam dininin beş temel gayesinden (Zarûrât-ı Diniyye) 'Aklın Korunması' ve 'Malın Korunması' ilkelerinin hangi emir ve yasaklarla güvence altına alındığını birer örnekle açıklayınız.",
            "options": [
                "A) Aklın korunması için alkol ve uyuşturucu; malın korunması için hırsızlık, rüşvet ve israf yasaklanmıştır.",
                "B) Aklın korunması için ticaret; malın korunması için seyahat emredilmiştir.",
                "C) Yalnızca ibadet esasları düzenlenmiştir.",
                "D) Malın korunması için zekât yasaklanmıştır."
            ],
            "answer_text": "Aklın korunması için iradeyi devre dışı bırakan alkol ve uyuşturucu maddeler haram kılınmıştır. Malın korunması için ise hırsızlık, kumar, faiz, rüşvet ve israf yasaklanmış; helal kazanç emredilmiştir.",
            "rubric": [
                {"criterion": "Aklın korunması ilkesinin doğru örneklerle açıklanması", "points": 5},
                {"criterion": "Malın korunması ilkesinin helal kazanç ve yasaklarla açıklanması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Allah'ın varlığı ve birliği (Tevhid) ile evrendeki eşsiz düzen arasında bağ kurar.",
            "cognitive_level": "Analiz",
            "difficulty": "Kolay",
            "source_page": "Sayfa 14-21",
            "source_context": "İhlas Suresi ve Enbiya Suresi 22. ayet bağlamında Tevhid inancı ve evrendeki kusursuz düzen işlenmektedir.",
            "arabic_text": "قُلْ هُوَ اللَّهُ أَحَدٌ ۝ اللَّهُ الصَّمَدُ",
            "question_text": "'Eğer yerde ve gökte Allah'tan başka ilahlar olsaydı kesinlikle ikisinin de düzeni bozulurdu.' (Enbiyâ, 22) ayeti ile İhlas Suresi'nde vurgulanan 'Tevhid' ve 'Samed' kavramlarını evrendeki düzen açısından açıklayınız.",
            "options": [
                "A) Evrendeki kusursuz düzen, tek ve hiçbir şeye muhtaç olmayan (Samed) Yaratıcının varlığının ve birliğinin (Tevhid) en açık delilidir.",
                "B) Evrendeki olaylar tesadüfen gerçekleşmektedir.",
                "C) Samed kavramı yalnızca meleklerin özelliğidir.",
                "D) Tevhid yalnızca ibadetlerin şekliyle ilgilidir."
            ],
            "answer_text": "Tevhid, Allah'ın tek ve eşsiz olmasıdır; Samed ise her şeyin O'na muhtaç olması, O'nun hiçbir şeye muhtaç olmamasıdır. Evrendeki bozulmayan uyum, tek bir Yaratıcının hükümranlığını kanıtlar.",
            "rubric": [
                {"criterion": "Tevhid ve Samed kavramlarının doğru açıklanması", "points": 5},
                {"criterion": "Evrendeki düzen ile Allah'ın birliği arasındaki ilişkinin kurulması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Namaz ve oruç ibadetlerinin insan davranışları üzerindeki olumlu etkilerini yorumlar.",
            "cognitive_level": "Yorumlama",
            "difficulty": "Orta",
            "source_page": "Sayfa 52-60",
            "source_context": "Ankebut Suresi 45. ayet ('Şüphesiz namaz insanı hayasızlıktan ve kötülükten alıkoyar') ve orucun sabır/empati boyutu ele alınmaktadır.",
            "arabic_text": "إِنَّ الصَّلَاةَ تَنْهَىٰ عَنِ الْفَحْشَاءِ وَالْمُنكَرِ",
            "question_text": "Kur'an-ı Kerim'de namazın insanı kötülüklerden alıkoyduğu, orucun ise kötülüklere karşı bir kalkan olduğu bildirilir. İbadetlerin sadece şekilsel hareketler olmayıp ahlakı güzelleştirmesi gerektiğini nasıl açıklarsınız?",
            "options": [
                "A) Bilinç ve samimiyetle yapılan ibadetler insana özdenetim, sabır, empati ve kötülükten sakınma bilinci kazandırır.",
                "B) İbadetlerin günlük davranışlarla hiçbir ilişkisi yoktur.",
                "C) Oruç yalnızca aç kalmaktan ibarettir.",
                "D) Namaz sadece zamanı değerlendirmek için kılınır."
            ],
            "answer_text": "Günde beş kez Allah'ın huzuruna çıkan ve oruçla nefsini terbiye eden bir mümin; yalandan, kul hakkından ve kötü sözden uzak durarak ibadetin ruhunu ahlakına yansıtır.",
            "rubric": [
                {"criterion": "Namazın özdenetim ve kötülükten sakındırma etkisinin açıklanması", "points": 5},
                {"criterion": "Orucun sabır, irade eğitimi ve empati boyutunun vurgulanması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Asr suresinde kurtuluşa eren insanların temel özelliklerini analiz eder.",
            "cognitive_level": "Analiz",
            "difficulty": "Orta",
            "source_page": "Sayfa 92-98",
            "source_context": "Asr Suresi'nde zamanın kıymeti ve insanın ziyandan kurtulmasının dört temel şartı açıklanmaktadır.",
            "arabic_text": "وَالْعَصْرِ ۝ إِنَّ الْإِنسَانَ لَفِي خُسْرٍ",
            "question_text": "Asr Suresi'ne göre insanlığın büyük bir kayıp (hüsran) içinde olduğu, ancak dört temel özelliğe sahip olanların kurtuluşa ereceği bildirilmektedir. Bu dört temel özelliği maddeler halinde yazınız.",
            "options": [
                "A) İman etmek, salih amel işlemek, birbirine hakkı tavsiye etmek ve birbirine sabrı tavsiye etmek",
                "B) Çok uyumak, çok konuşmak, mal biriktirmek ve yalnız yaşamak",
                "C) Yalnızca bireysel ibadet yapmak ve toplumdan uzaklaşmak",
                "D) Sadece zor zamanlarda dua etmek"
            ],
            "answer_text": "1) İman etmek, 2) Salih (iyi, güzel ve faydalı) ameller işlemek, 3) Birbirine hakkı ve doğruluğu tavsiye etmek, 4) Birbirine sabrı tavsiye etmektir.",
            "rubric": [
                {"criterion": "İman ve salih amel şartlarının yazılması", "points": 5},
                {"criterion": "Hakkı ve sabrı tavsiye etme şartlarının yazılması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Kul hakkı kavramını ve toplumsal adalet açısından önemini değerlendirir.",
            "cognitive_level": "Değerlendirme",
            "difficulty": "Zor",
            "source_page": "Sayfa 104-110",
            "source_context": "İslam ahlakında kamu malı, dürüstlük, dedikodudan sakınma ve kul hakkıyla Allah'ın huzuruna çıkmama ilkeleri işlenmektedir.",
            "arabic_text": "",
            "question_text": "Günlük hayatta sadece hırsızlık yapmak değil; sırada bekleyenlerin önüne geçmek, okul eşyalarına zarar vermek ve birinin arkasından konuşmak (gıybet) da kul hakkı sayılmaktadır. Nedenini ve kul hakkının nasıl affedilebileceğini açıklayınız.",
            "options": [
                "A) Başkasının emeğine, zamanına veya onuruna zarar veren her davranış kul hakkıdır; affı için hak sahibiyle helalleşmek şarttır.",
                "B) Küçük davranışlar kul hakkına girmez.",
                "C) Kul hakkı yalnızca maddi borçları kapsar.",
                "D) Kamu malına zarar vermek kul hakkı sayılmaz."
            ],
            "answer_text": "Çünkü bu davranışlar diğer insanların zamanını, onurunu veya ortak kullanım hakkını gasp etmektedir. Allah kendi hakkını tövbeyle affeder ancak kul hakkının affı için mağdurun zararı giderilmeli ve helallik alınmalıdır.",
            "rubric": [
                {"criterion": "Manevi ve kamusal hakların da kul hakkı olduğunun gerekçelendirilmesi", "points": 5},
                {"criterion": "Hak sahibiyle helalleşme şartının belirtilmesi", "points": 5}
            ]
        },
        {
            "learning_outcome": "Kültürümüzde, mimarimizde ve örf-adetlerimizde dinin izlerini yorumlar.",
            "cognitive_level": "Yorumlama",
            "difficulty": "Kolay",
            "source_page": "Sayfa 168-180",
            "source_context": "Cami merkezli şehir mimarisi, şifahaneler, sadaka taşları, kuş evleri ve bayramlaşma geleneğimizde İslam ahlakının yansımaları.",
            "arabic_text": "",
            "question_text": "Ecdadımızın cami ve konakların dış cephelerine 'Kuş Evleri' yapması ile cami avlularına 'Sadaka Taşları' yerleştirmesi, kültürümüzdeki hangi dini ve ahlaki duyarlılıkların göstergesidir? Açıklayınız.",
            "options": [
                "A) Kuş evleri yaradılanı Yaradan'dan ötürü sevme merhametini; sadaka taşları ise yoksulu incitmeden gizlice yardımlaşma nezaketini gösterir.",
                "B) Sadece mimari süsleme amacıyla yapılmıştır.",
                "C) Yalnızca zenginliği göstermek için inşa edilmiştir.",
                "D) Ticari amaçlarla kullanılmıştır."
            ],
            "answer_text": "Kuş evleri İslam'ın tüm canlılara şefkat ve merhamet ilkesini; sadaka taşları ise 'sağ elin verdiğini sol elin görmemesi' hadisine uygun olarak yoksulun onurunu incitmeden yardımlaşma ahlakını gösterir.",
            "rubric": [
                {"criterion": "Kuş evlerinin canlılara merhamet ve şefkat boyutuyla açıklanması", "points": 5},
                {"criterion": "Sadaka taşlarının gizli infak ve insan onurunu koruma boyutuyla açıklanması", "points": 5}
            ]
        }
    ]

    # 2. KUR'AN-I KERİM DERSİ ÖZEL HAVUZU (10 Özgün Tecvid, Mahreç, Vakıf ve Sure Analizi Sorusu)
    kuran_pool = [
        {
            "learning_outcome": "Sakin nun ve tenvin kurallarını (İzhar, İhfa, İklab, İdgam) örnekler üzerinde tespit eder.",
            "cognitive_level": "Uygulama",
            "difficulty": "Orta",
            "source_page": "Sayfa 98-115",
            "source_context": "Tecvid ilminde tenvin veya sakin nundan sonra gelen harflere göre uygulanan İzhar, İklab ve İhfa kuralları örneklerle işlenmektedir.",
            "arabic_text": "مِنْ بَعْدِ  —  أَنْعَمْتَ  —  مَنْ آمَنَ",
            "question_text": "Yukarıda verilen Kur'an-ı Kerim lafızlarında sakin nun (نْ) harfinden sonra gelen harflere göre hangi tecvid kurallarının meydana geldiğini ve bu kelimelerin nasıl okunması gerektiğini sırasıyla açıklayınız.",
            "options": [
                "A) مِنْ بَعْدِ: İklab (mim'e çevrilir) — أَنْعَمْتَ ve مَنْ آمَنَ: İzhar (boğaz harfleri geldiği için açık okunur)",
                "B) Hepsinde İdgam-ı Meal Gunne vardır.",
                "C) مِنْ بَعْدِ: İzhar — أَنْعَمْتَ: İklab — مَنْ آمَنَ: İhfa",
                "D) Hiçbirinde tecvid kuralı uygulanmaz."
            ],
            "answer_text": "1) مِنْ بَعْدِ lafzında sakin nundan sonra ب harfi geldiği için İKLAB olur (nun sesi mim'e çevrilerek gunneli okunur). 2) أَنْعَمْتَ ve مَنْ آمَنَ lafızlarında sakin nundan sonra boğaz harfleri (ع ve أ) geldiği için İZHAR olur (tutulmadan açık ve net okunur).",
            "rubric": [
                {"criterion": "مِنْ بَعْدِ örneğinde İklab kuralının ve uygulanışının doğru yazılması", "points": 5},
                {"criterion": "أَنْعَمْتَ ve مَنْ آمَنَ örneklerinde İzhar kuralının ve sebebinin doğru yazılması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Uzatma (Med) kurallarından Medd-i Tabiî, Medd-i Muttasıl ve Medd-i Munfasıl'ı ayırt eder.",
            "cognitive_level": "Analiz",
            "difficulty": "Orta",
            "source_page": "Sayfa 46-72",
            "source_context": "Harf-i medden (Elif, Vav, Ya) sonra sebeb-i med olan hemzenin aynı kelimede veya ayrı kelimede gelmesi durumu karşılaştırılmaktadır.",
            "arabic_text": "جَاءَ — إِذَا أَرَادَ — قَالَ",
            "question_text": "Verilen üç Arapça kelimedeki med (uzatma) kurallarını bularak; Medd-i Muttasıl ile Medd-i Munfasıl arasındaki temel farkı bu örnekler üzerinden açıklayınız.",
            "options": [
                "A) جَاءَ: Medd-i Muttasıl (aynı kelimede) — إِذَا أَرَادَ: Medd-i Munfasıl (ayrı kelimelerde) — قَالَ: Medd-i Tabiî",
                "B) جَاءَ: Medd-i Tabiî — إِذَا أَرَادَ: Medd-i Lâzım — قَالَ: Medd-i Muttasıl",
                "C) Üçü de Medd-i Ârız örneğidir.",
                "D) جَاءَ: Medd-i Munfasıl — إِذَا أَرَادَ: Medd-i Muttasıl"
            ],
            "answer_text": "جَاءَ kelimesinde med harfi Elif ile kırık hemze aynı kelimede bulunduğu için Medd-i Muttasıl (vacip); إِذَا أَرَادَ ifadesinde med harfi ile uzun hemze ayrı kelimelerde olduğu için Medd-i Munfasıl (caiz); قَالَ kelimesinde ise sebeb-i med olmadığı için Medd-i Tabiî vardır.",
            "rubric": [
                {"criterion": "Üç örneğin med çeşitlerinin doğru tespit edilmesi", "points": 5},
                {"criterion": "Bitişik (Muttasıl) ve ayrık (Munfasıl) hemze farkının açıklanması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Kalkale harflerini (Kutbu Cedin) ve ayet sonlarında uygulanışını açıklar.",
            "cognitive_level": "Uygulama",
            "difficulty": "Kolay",
            "source_page": "Sayfa 48-58",
            "source_context": "İhlas ve Tebbet sureleri üzerinden Kalkale (ق ط ب ج د) harflerinin cezimli okunuşundaki yankılanma/vurgu kuralı işlenmektedir.",
            "arabic_text": "قُلْ هُوَ اللَّهُ أَحَدٌ ۝ اللَّهُ الصَّمَدُ ۝ لَمْ يَلِدْ وَلَمْ يُولَدْ",
            "question_text": "İhlas Suresi'nin verilen ayetlerinde durak yapıldığında (vakıf halinde) hangi harfte ve hangi tecvid kuralının oluştuğunu; bu kurala ait 5 harfin neler olduğunu yazınız.",
            "options": [
                "A) Dal (د) harfinde Kalkale kuralı oluşur; harfleri ق ط ب ج د (Kutbu Cedin) harfleridir.",
                "B) Lam (ل) harfinde İdgam kuralı oluşur.",
                "C) Mim (م) harfinde İklab kuralı oluşur.",
                "D) He (ه) harfinde Medd-i Lâzım oluşur."
            ],
            "answer_text": "Ayet sonlarındaki 'أَحَدٌ - الصَّمَدُ - يَلِدْ - يُولَدْ' kelimelerinde durulduğunda Dal (د) harfi sakinleştiği için KALKALE kuralı oluşur. Kalkale harfleri 'Kutbu Cedin' (ق، ط، ب، ج، د) olarak kodlanan 5 harftir.",
            "rubric": [
                {"criterion": "Kalkale kuralının ve Dal (د) harfinin tespit edilmesi", "points": 5},
                {"criterion": "Beş kalkale harfinin (ق ط ب ج د / Kutbu Cedin) eksiksiz yazılması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Lafzatullah (Allah lafzı) ve Ra (ر) harfinin kalın/ince okunuş kurallarını analiz eder.",
            "cognitive_level": "Analiz",
            "difficulty": "Zor",
            "source_page": "Sayfa 62-75",
            "source_context": "Allah lafzından önceki harfin harekesine göre Lam harfinin kalın veya ince okunması kuralı örneklerle açıklanmaktadır.",
            "arabic_text": "بِسْمِ اللَّهِ  —  هُوَ اللَّهُ  —  رَسُولُ اللَّهِ",
            "question_text": "Yukarıdaki üç lafızda geçen 'Allah' (اللَّه) lafzının Lam harfinin hangilerinde İNCE, hangilerinde KALIN okunduğunu kuralın gerekçesiyle birlikte açıklayınız.",
            "options": [
                "A) بِسْمِ اللَّهِ lafzında önceki harf esreli olduğu için İNCE; هُوَ اللَّهُ ve رَسُولُ اللَّهِ lafızlarında önceki harf üstün/ötreli olduğu için KALIN okunur.",
                "B) Üçünde de kalın okunur.",
                "C) بِسْمِ اللَّهِ lafzında kalın, diğerlerinde ince okunur.",
                "D) Yalnızca cümle başında kalın okunur."
            ],
            "answer_text": "Lafzatullah'tan önceki harfin harekesi esre ise ince, üstün veya ötre ise kalın okunur. Bu sebeple 'بِسْمِ اللَّهِ' lafzında Mim esreli olduğu için İNCE; 'هُوَ اللَّهُ' (üstün) ve 'رَسُولُ اللَّهِ' (ötre) lafızlarında ise KALIN okunur.",
            "rubric": [
                {"criterion": "Lafzatullah'ın kalın ve ince okunma kuralının doğru açıklanması", "points": 5},
                {"criterion": "Verilen üç örneğin doğru sınıflandırılması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Secavend (Vakıf / Durak) işaretlerinin anlamlarını ve tilavetteki önemini açıklar.",
            "cognitive_level": "Yorumlama",
            "difficulty": "Orta",
            "source_page": "Sayfa 40-54",
            "source_context": "Kur'an-ı Kerim okurken anlam bozulmasını önleyen durak (vakıf) işaretleri (م، ط، ج، لا، ص) ve duruş kuralları işlenmektedir.",
            "arabic_text": "(م)   —   (لا)   —   (ط)",
            "question_text": "Kur'an-ı Kerim sayfalarında ayet içinde gördüğümüz (م), (لا) ve (ط) durak (secavend) işaretlerinin okuyucuya verdiği mesaj nedir? Neden durak işaretlerine dikkat etmeliyiz?",
            "options": [
                "A) (م): Kesinlikle durulmalı (Vakf-ı Lâzım) — (لا): Durulmamalı — (ط): Durmak daha uygundur (Vakf-ı Mutlak)",
                "B) (م): Durulmaz — (لا): Kesinlikle durulur — (ط): Hızlı geçilir",
                "C) Bu işaretler sadece sayfa numarasını gösterir.",
                "D) Sadece ses tonunu yükseltmek için kullanılır."
            ],
            "answer_text": "(م) Vakf-ı Lâzım: Anlam bozulacağı için kesinlikle durulmalıdır. (لا): Anlam devam ettiği için durulmamalı, geçilmelidir. (ط) Vakf-ı Mutlak: Cümle tamamlandığı için durulması uygundur. Duraklara uymak ayetlerin manasını doğru korumayı sağlar.",
            "rubric": [
                {"criterion": "Mim (م), Lâ (لا) ve Tı (ط) durak işaretlerinin anlamlarının doğru yazılması", "points": 6},
                {"criterion": "Anlam bütünlüğünü koruma gerekçesinin belirtilmesi", "points": 4}
            ]
        },
        {
            "learning_outcome": "İdgam-ı Meal Gunne ve İdgam-ı Bila Gunne kurallarını harfleriyle ayırt eder.",
            "cognitive_level": "Uygulama",
            "difficulty": "Zor",
            "source_page": "Sayfa 116-128",
            "source_context": "Sakin nun veya tenvinden sonra ي ن م و (Yemnu) veya ل ر harflerinin gelmesiyle oluşan idgam çeşitleri.",
            "arabic_text": "مَنْ يَقُولُ  —  مِنْ رَبِّهِمْ  —  هُدًى لِلْمُتَّقِينَ",
            "question_text": "Verilen üç Kur'an ifadesinde sakin nun ve tenvinden sonra gelen harflere dikkat ederek; hangisinde 'İdgam-ı Meal Gunne', hangilerinde 'İdgam-ı Bila Gunne' olduğunu açıklayınız.",
            "options": [
                "A) مَنْ يَقُولُ: İdgam-ı Meal Gunne (ي harfi) — مِنْ رَبِّهِمْ ve هُدًى لِلْمُتَّقِينَ: İdgam-ı Bila Gunne (ر ve ل harfleri)",
                "B) Üçü de İdgam-ı Meal Gunne örneğidir.",
                "C) مَنْ يَقُولُ: İzhar — diğerleri İhfa'dır.",
                "D) مَنْ يَقُولُ: İdgam-ı Bila Gunne — diğerleri Meal Gunne'dir."
            ],
            "answer_text": "'مَنْ يَقُولُ' ifadesinde sakin nundan sonra 'Yemnu' (ي ن م و) harflerinden ي geldiği için gunneli katma (İdgam-ı Meal Gunne) olur. 'مِنْ رَبِّهِمْ' (ر) ve 'هُدًى لِلْمُتَّقِينَ' (ل) ifadelerinde ise ل ve ر harfleri geldiği için gunnesiz katma (İdgam-ı Bila Gunne) olur.",
            "rubric": [
                {"criterion": "İdgam-ı Meal Gunne örneğinin ve harflerinin (ي ن م و) belirtilmesi", "points": 5},
                {"criterion": "İdgam-ı Bila Gunne örneklerinin ve harflerinin (ل، ر) belirtilmesi", "points": 5}
            ]
        },
        {
            "learning_outcome": "Sakin Mim (مْ) hallerini (İhfa-i Şefevi, İdgam-ı Misleyn, İzhar-ı Şefevi) analiz eder.",
            "cognitive_level": "Analiz",
            "difficulty": "Orta",
            "source_page": "Sayfa 130-140",
            "source_context": "Dudak harfi olan cezimli Mim (مْ) harfinden sonra Be (ب), Mim (م) veya diğer harflerin gelmesiyle oluşan üç tecvid durumu.",
            "arabic_text": "تَرْمِيهِمْ بِحِجَارَةٍ  —  لَهُمْ مَا يَشَاءُونَ  —  أَلَمْ نَشْرَحْ",
            "question_text": "Yukarıdaki ayet örneklerinde cezimli Mim (مْ) harfinden sonra gelen harflere göre oluşan üç farklı tecvid kuralını sırasıyla yazınız.",
            "options": [
                "A) 1: İhfa-i Şefevi (ب geldiği için) — 2: İdgam-ı Misleyn Meal Gunne (م geldiği için) — 3: İzhar-ı Şefevi (ن geldiği için)",
                "B) 1: İzhar — 2: İklab — 3: Kalkale",
                "C) Hepsi Dudak İhfasıdır.",
                "D) 1: İdgam — 2: İzhar — 3: İhfa"
            ],
            "answer_text": "1) تَرْمِيهِمْ بِحِجَارَةٍ: Sakin mim'den sonra ب geldiği için Dudak İhfası (İhfa-i Şefevi). 2) لَهُمْ مَا: Sakin mim'den sonra م geldiği için İdgam-ı Misleyn Meal Gunne. 3) أَلَمْ نَشْرَحْ: Sakin mim'den sonra ب ve م dışında bir harf (ن) geldiği için İzhar-ı Şefevi.",
            "rubric": [
                {"criterion": "Dudak ihfası ve İdgam-ı Misleyn örneklerinin doğru tespiti", "points": 5},
                {"criterion": "İzhar-ı Şefevi örneğinin ve kuralının doğru açıklanması", "points": 5}
            ]
        },
        {
            "learning_outcome": "İnşirah ve Kadir surelerinin ana mesajlarını ve hayatımıza yansımalarını yorumlar.",
            "cognitive_level": "Yorumlama",
            "difficulty": "Kolay",
            "source_page": "Sayfa 70-88",
            "source_context": "İnşirah Suresi'ndeki 'Şüphesiz güçlükle beraber bir kolaylık vardır' müjdesi ve çalışma disiplini incelenmektedir.",
            "arabic_text": "فَإِنَّ مَعَ الْعُسْرِ يُسْرًا ۝ إِنَّ مَعَ الْعُسْرِ يُسْرًا ۝ فَإِذَا فَرَغْتَ فَانصَبْ",
            "question_text": "İnşirah Suresi'nin verilen ayetlerinde zorluklarla karşılaşan bir mümine verilen ümit mesajı ile bir işi bitirdikten sonra nasıl davranması gerektiğine dair ilkeyi açıklayınız.",
            "options": [
                "A) Her zorluğun yanında bir kolaylık olduğu bilinciyle ümitsizliğe kapılmamalı; bir işi bitirince tembellik etmeyip hemen yeni bir hayırlı işe koyulmalıdır.",
                "B) Zorluk karşısında çalışmayı bırakıp beklemelidir.",
                "C) Bir iş bitince uzun süre hiçbir şey yapmamalıdır.",
                "D) Yalnızca dünyevi işlerle meşgul olmalıdır."
            ],
            "answer_text": "Ayetler, her güçlükle beraber mutlaka bir kolaylık olduğunu iki kez vurgulayarak müslümana ümit ve sabır aşılar. Ayrıca 'Bir işi bitirince hemen başka bir işe koyul ve yalnız Rabbine yönel' buyrularak sürekli üretkenlik ve ibadet bilinci öğütlenir.",
            "rubric": [
                {"criterion": "Zorlukla beraber kolaylık (ümit ve sabır) mesajının açıklanması", "points": 5},
                {"criterion": "Sürekli çalışma, üretkenlik ve Rabbine yönelme ilkesinin yazılması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Kur'an-ı Kerim okuma adabını (Tertil, İstiaze, Besmele, Huşu) açıklar.",
            "cognitive_level": "Değerlendirme",
            "difficulty": "Kolay",
            "source_page": "Sayfa 12-30",
            "source_context": "Müzzemmil Suresi 4. ayet ('Kur'an'ı tertil üzere oku') ve Nahl Suresi 98. ayet bağlamında tilavet adabı.",
            "arabic_text": "وَرَتِّلِ الْقُرْآنَ تَرْتِيلًا",
            "question_text": "Yüce Allah Müzzemmil Suresi 4. ayette 'Kur'an'ı tertil üzere oku!' buyurmaktadır. 'Tertil üzere okumak' ne demektir ve Kur'an okumaya başlarken uyulması gereken maddi/manevi adap kurallarından 3 tanesini yazınız.",
            "options": [
                "A) Tertil; Kur'an'ı acele etmeden, harflerin mahreç ve tecvid hakkını vererek, anlamını düşünerek tane tane okumaktır.",
                "B) Tertil; Kur'an'ı mümkün olduğunca hızlı okumaktır.",
                "C) Sadece sessizce gözle takip etmektir.",
                "D) Tecvid kurallarına dikkat etmeden okumaktır."
            ],
            "answer_text": "Tertil; Kur'an'ı acele etmeden, harfleri mahreçlerinden çıkarıp tecvid kurallarına uyarak ve manasını tefekkür ederek tane tane okumaktır. Adapları: 1) Abdestli ve temiz olmak, 2) Eûzü-Besmele çekmek, 3) Huşu ve saygı ile dinlemek/okumaktır.",
            "rubric": [
                {"criterion": "Tertil kavramının doğru tanımlanması", "points": 5},
                {"criterion": "En az 3 Kur'an okuma adabının (abdest, istiaze/besmele, huşu vb.) yazılması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Kevser ve Fil surelerinin indiriliş bağlamını ve verdiği tevhid mesajını analiz eder.",
            "cognitive_level": "Analiz",
            "difficulty": "Orta",
            "source_page": "Sayfa 140-162",
            "source_context": "Kevser Suresi'nde Rabbe şükür, namaz ve kurban bilinci; Fil Suresi'nde Kâbe'nin korunması ve Allah'ın kudreti işlenmektedir.",
            "arabic_text": "إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ ۝ فَصَلِّ لِرَبِّكَ وَانْحَرْ",
            "question_text": "Kevser Suresi'nde Yüce Allah'ın Peygamberimize (ve müminlere) bol nimet (Kevser) lütfettiği bildirildikten sonra bu nimete şükür olarak hangi iki temel ibadeti yapması emredilmiştir? Açıklayınız.",
            "options": [
                "A) Yalnızca Rabbin için namaz kıl (فَصَلِّ) ve kurban kes (وَانْحَرْ).",
                "B) Ticaret yap ve seyahat et.",
                "C) Oruç tut ve hicret et.",
                "D) Yalnızca tefekkür et."
            ],
            "answer_text": "Verilen bol nimete (Kevser'e) şükür olarak; 1) 'Yalnızca Rabbin için namaz kıl' (فَصَلِّ لِرَبِّكَ) ve 2) 'Kurban kes' (وَانْحَرْ) ibadetleri emredilmiştir. Ayrıca asıl soyu kesik (ebter) olanların kin besleyen inkârcılar olduğu bildirilmiştir.",
            "rubric": [
                {"criterion": "Kevser kavramının (bol nimet/hayır) açıklanması", "points": 4},
                {"criterion": "Namaz kılma ve kurban kesme emirlerinin doğru belirtilmesi", "points": 6}
            ]
        }
    ]

    # 3. PEYGAMBERİMİZİN HAYATI (SİYER) ÖZEL HAVUZU (10 Özgün Nebevî Örneklik Sorusu)
    siyer_pool = [
        {
            "learning_outcome": "Peygamberimizin gençlik yıllarındaki güvenilirliğini (Muhammedü'l-Emîn) ve Hilfü'l-Fudûl'e katılımını analiz eder.",
            "cognitive_level": "Analiz",
            "difficulty": "Orta",
            "source_page": "Sayfa 46-62",
            "source_context": "Hz. Muhammed'in (s.a.v.) peygamberlik öncesinde Mekke'de haksızlıklara karşı kurulan Erdemliler Topluluğu'na (Hilfü'l-Fudûl) katılması ve emanet bilinci.",
            "arabic_text": "",
            "question_text": "Peygamber Efendimiz (s.a.v.) gençlik yıllarında Mekke'de mazlumların hakkını korumak için kurulan 'Hilfü'l-Fudûl' (Erdemliler Topluluğu) cemiyetine katılmış ve yıllar sonra 'İslam'da da böyle bir antlaşmaya çağrılsam yine icabet ederim' buyurmuştur. Bu durum Efendimizin adalet ve insan hakları anlayışı hakkında bize hangi mesajı verir?",
            "options": [
                "A) Mazlumun kimliğine bakılmaksızın adaleti savunmanın ve haksızlığa karşı ortak tavır almanın her Müslümanın görevi olduğunu gösterir.",
                "B) Yalnızca kendi kabilemizin haklarını savunmamız gerektiğini gösterir.",
                "C) Toplumsal sorunlara karışmamak gerektiğini ifade eder.",
                "D) Adalet arayışının sadece belirli bir dönemle sınırlı olduğunu gösterir."
            ],
            "answer_text": "Hz. Peygamber (s.a.v.), kimden gelirse gelsin zulme karşı durmuş ve mazlumun yanında yer almıştır. Müslümanlar da toplumda adaletin tesisi ve insan haklarının korunması için her zaman erdemli girişimlere destek vermelidir.",
            "rubric": [
                {"criterion": "Hilfü'l-Fudûl'ün kuruluş amacının (mazlumları koruma ve adalet) açıklanması", "points": 5},
                {"criterion": "Günümüz dünyasında haksızlıklara karşı erdemli duruş mesajının çıkarılması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Medine'de kurulan Ensar-Muhacir kardeşliğini (Muâhât) ve Medine Sözleşmesi'ni değerlendirir.",
            "cognitive_level": "Değerlendirme",
            "difficulty": "Orta",
            "source_page": "Sayfa 118-136",
            "source_context": "Hicret sonrasında Medine'de tesis edilen Muâhât (kardeşleştirme), Mescid-i Nebevî'nin inşası ve birlikte yaşama hukuku.",
            "arabic_text": "إِنَّمَا الْمُؤْمِنُونَ إِخْوَةٌ",
            "question_text": "Hicret sonrasında Peygamber Efendimizin Medine'de attığı üç temel adım olan; 'Mescid-i Nebevî ve Suffe'nin inşası', 'Muâhât (Ensar-Muhacir kardeşliği)' ve 'Medine Sözleşmesi'nin toplumsal açıdan hangi ihtiyaçları karşıladığını açıklayınız.",
            "options": [
                "A) Mescid eğitim ve ibadet merkezi olmuş; Muâhât sosyal yardımlaşmayı sağlamış; Medine Sözleşmesi ise farklı inançlarla barış içinde yaşama hukukunu kurmuştur.",
                "B) Sadece askeri savunma amacı taşımıştır.",
                "C) Yalnızca ticari gelir elde etmek için yapılmıştır.",
                "D) Muhacirlerin Mekke'ye geri dönmesini sağlamıştır."
            ],
            "answer_text": "1) Mescid-i Nebevî ve Suffe: İbadet, eğitim ve yönetim merkezi ihtiyacını karşılamıştır. 2) Muâhât: Evlerini bırakıp gelen Muhacirler ile Ensar arasında eşsiz bir dayanışma ve kardeşlik kurmuştur. 3) Medine Sözleşmesi: Farklı din ve kabilelerin barış ve hukuk içinde bir arada yaşamasını sağlamıştır.",
            "rubric": [
                {"criterion": "Mescid-i Nebevî/Suffe ve Muâhât'ın eğitim ve dayanışma işlevinin açıklanması", "points": 5},
                {"criterion": "Medine Sözleşmesi'nin birlikte yaşama ve toplumsal barış boyutunun yazılması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Bedir, Uhud ve Hendek savaşlarında Peygamberimizin istişare, eğitim ve merhamet ilkelerini analiz eder.",
            "cognitive_level": "Analiz",
            "difficulty": "Zor",
            "source_page": "Sayfa 14-48",
            "source_context": "Bedir esirlerinin 10 Müslümana okuma-yazma öğretme karşılığında serbest bırakılması ve Uhud/Hendek'te istişare uygulaması.",
            "arabic_text": "وَشَاوِرْهُمْ فِي الْأَمْرِ",
            "question_text": "Peygamber Efendimizin (s.a.v.) Bedir Savaşı sonrasında esirleri '10 Müslümana okuma-yazma öğretmeleri' karşılığında serbest bırakması ile Hendek Savaşı'nda Selman-ı Farisî'nin hendek kazma fikrini kabul etmesi hangi iki Nebevî ilkeyi ortaya koymaktadır?",
            "options": [
                "A) İlim/eğitime verilen üstün değer ile karar alma süreçlerinde istişareye (ortak akla) verilen önem.",
                "B) Savaş ganimetlerini artırma ve tek başına karar alma.",
                "C) Yalnızca askeri taktik geliştirme.",
                "D) Esirleri cezalandırma politikası."
            ],
            "answer_text": "Bedir uygulaması İslam'ın ilme, okuma-yazmaya ve esirlere insani muameleye verdiği eşsiz değeri; Hendek uygulaması ise Efendimizin ortak akla ve istişareye (şûra) verdiği önemi açıkça göstermektedir.",
            "rubric": [
                {"criterion": "Bedir uygulamasının ilim ve eğitime verilen önem açısından açıklanması", "points": 5},
                {"criterion": "Hendek uygulamasının istişare ve ortak akıl açısından açıklanması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Mekke'nin Fethi ve Peygamberimizin genel af ilanındaki affedicilik ahlakını yorumlar.",
            "cognitive_level": "Yorumlama",
            "difficulty": "Kolay",
            "source_page": "Sayfa 68-86",
            "source_context": "Hudeybiye Barışı sonrasında gerçekleşen Mekke'nin Fethi ve Hz. Peygamber'in 'Bugün size kınama yoktur, hepiniz serbestsiniz' (Genel Af) beyanı.",
            "arabic_text": "لَا تَثْرِيبَ عَلَيْكُمُ الْيَوْمَ",
            "question_text": "Yıllarca Müslümanlara eziyet eden ve onları yurtlarından çıkaran Mekkelilere karşı, Mekke'nin Fethi günü güçlü konumda olmasına rağmen Peygamber Efendimiz 'Bugün size kınama yoktur, hepiniz serbestsiniz!' buyurmuştur. Bu tavrın insanların kalbini kazanmadaki etkisini yorumlayınız.",
            "options": [
                "A) İntikam yerine merhamet ve affediciliği seçmesi, kalplerdeki düşmanlığı eriterek insanların gönüllü olarak İslam'a girmesini sağlamıştır.",
                "B) Mekkelilerin şehirden tamamen göç etmesine neden olmuştur.",
                "C) Kabile savaşlarının yeniden başlamasına yol açmıştır.",
                "D) Yalnızca siyasi bir anlaşma olarak kalmıştır."
            ],
            "answer_text": "Gücü elinde bulundurduğu anda intikam almak yerine affetmeyi seçmesi, gerçek fethin kalpleri kazanmak olduğunu göstermiştir. Bu yüce merhamet karşısında en azılı düşmanlar dahi İslam'la şereflenmiştir.",
            "rubric": [
                {"criterion": "Güçlüyken affetmenin ve intikamdan uzak durmanın erdeminin vurgulanması", "points": 5},
                {"criterion": "Kalplerin kazanılması ve toplumsal barışa etkisinin açıklanması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Veda Hutbesi'nde yer alan evrensel insan hakları ve adalet ilkelerini analiz eder.",
            "cognitive_level": "Analiz",
            "difficulty": "Orta",
            "source_page": "Sayfa 96-114",
            "source_context": "632 yılında Veda Haccı'nda irad edilen Veda Hutbesi'ndeki can/mal güvenliği, kadın hakları, ırkçılık ve kan davalarının kaldırılması ilkeleri.",
            "arabic_text": "",
            "question_text": "Peygamber Efendimizin (s.a.v.) yüz binden fazla sahabeye hitap ettiği Veda Hutbesi'nde tüm insanlığa ilan ettiği evrensel insan hakları ilkelerinden 4 tanesini maddeler halinde yazınız.",
            "options": [
                "A) Can ve mal dokunulmazlığı, ırkçılığın reddi (takva üstünlüğü), kadın haklarının korunması, faiz ve kan davalarının kaldırılması",
                "B) Arapların diğer milletlerden üstün olduğu ve ticaretin sınırlandırılması",
                "C) Sadece Mekkelilere yönelik yerel kurallar",
                "D) Yalnızca hac ibadetinin şekilsel kuralları"
            ],
            "answer_text": "1) Can, mal ve onur dokunulmazlığı, 2) Arap'ın Arap olmayana üstünlüğü olmadığı (ırkçılığın reddi, üstünlüğün ancak takvada olduğu), 3) Kadınların haklarının korunması ve Allah'ın emaneti görülmesi, 4) Kan davalarının ve faizin kesin olarak kaldırılması.",
            "rubric": [
                {"criterion": "Can/mal güvenliği ve ırkçılığın reddi ilkelerinin yazılması", "points": 5},
                {"criterion": "Kadın hakları, emanet bilinci ve kan davası/faiz yasağının yazılması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Peygamberimizin aile içi iletişimini, nezaketini ve çocuklara şefkatini modeller.",
            "cognitive_level": "Uygulama",
            "difficulty": "Kolay",
            "source_page": "Sayfa 82-110",
            "source_context": "Hz. Peygamber'in ev işlerine yardım etmesi, eşlerine ve çocuklarına tebessüm ve nezaketle yaklaşması, torunları Hz. Hasan ve Hüseyin'e sevgisi.",
            "arabic_text": "خَيْرُكُمْ خَيْرُكُمْ لِأَهْلِهِ",
            "question_text": "'Sizin en hayırlınız, ailesine karşı en hayırlı (en iyi ve nazik) olanınızdır.' buyuran Peygamber Efendimizin (s.a.v.) kendi ev hayatındaki örnek davranışlarından 3 tanesini yazarak günümüz aile iletişimi açısından önemini açıklayınız.",
            "options": [
                "A) Ev işlerinde ailesine yardım etmesi, asla kırıcı konuşmaması, çocuklara ve yaşlılara sevgi/şefkatle vakit ayırması",
                "B) Ev işlerini tamamen başkalarına bırakması ve sert bir disiplin uygulaması",
                "C) Aile bireyleriyle istişare etmemesi",
                "D) Çocukların oyun oynamasına izin vermemesi"
            ],
            "answer_text": "1) Ev işlerinde eşlerine bizzat yardım ederdi. 2) Aile bireyleriyle istişare eder, kimseyi azarlamazdı. 3) Çocuklara selam verir, onlarla şakalaşır ve sevgisini açıkça gösterirdi. Bu tutum ailede huzur ve güvenin temelidir.",
            "rubric": [
                {"criterion": "Peygamberimizin aile içi örnek davranışlarından en az üçünün yazılması", "points": 5},
                {"criterion": "Günümüz aile huzuru ve iletişimiyle bağlantısının kurulması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Peygamberimizin hukuk önünde eşitlik ve adalet anlayışını (Fatıma Hadisi) değerlendirir.",
            "cognitive_level": "Değerlendirme",
            "difficulty": "Zor",
            "source_page": "Sayfa 50-66",
            "source_context": "Mahzumoğulları kabilesinden hırsızlık yapan soylu bir kadının affedilmesi için aracı gönderildiğinde Hz. Peygamber'in verdiği tarihi adalet dersi.",
            "arabic_text": "",
            "question_text": "Soylu bir aileden suç işleyen bir kişinin cezalandırılmaması için Peygamberimize aracı gönderildiğinde Efendimiz: 'Sizden önceki toplumlar, aralarından güçlü biri suç işlediğinde onu bırakıp zayıf biri suç işlediğinde cezalandırdıkları için helak oldular. Allah'a yemin ederim ki suç işleyen kızım Fatıma bile olsa cezasını verirdim!' buyurmuştur. Bu hadisi 'hukukun üstünlüğü' ilkesi açısından değerlendiriniz.",
            "options": [
                "A) Adaletin kişilerin makamına, zenginliğine veya yakınlığına göre değişemeyeceğini; kanun önünde herkesin eşit olduğunu gösterir.",
                "B) Soylu ailelere ayrıcalık tanınabileceğini gösterir.",
                "C) Cezaların sadece fakirlere uygulanacağını ifade eder.",
                "D) Akrabaların her durumda kayırılması gerektiğini savunur."
            ],
            "answer_text": "Bu hadis, İslam'da hiçbir kimseye makam, soy veya yakınlık sebebiyle imtiyaz (ayrıcalık) tanınamayacağını; hukukun üstünlüğü ve kanun önünde eşitliğin toplumların ayakta kalması için vazgeçilmez şart olduğunu ortaya koyar.",
            "rubric": [
                {"criterion": "Hukuk önünde eşitlik ve ayrıcalıksız adalet ilkesinin vurgulanması", "points": 5},
                {"criterion": "Adaletsizliğin toplumların çöküş sebebi olduğunun açıklanması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Habeşistan Hicreti, Taif Yolculuğu ve Hüzün Yılı'nda Peygamberimizin sabır ve kararlılığını analiz eder.",
            "cognitive_level": "Analiz",
            "difficulty": "Orta",
            "source_page": "Sayfa 49-78",
            "source_context": "Mekke dönemindeki boykot yılları, Hz. Hatice ve Ebu Talib'in vefatı (Hüzün Yılı) ve Taif'te taşlanmasına rağmen beddua etmeyip hidayet dilemesi.",
            "arabic_text": "",
            "question_text": "Peygamber Efendimiz (s.a.v.) Taif'te tebliğ yaparken ağır hakaretlere uğrayıp taşlandığı halde, onların helak olmasını değil; 'Rabbim! Kavmimi bağışla, çünkü onlar bilmiyorlar. Belki nesillerinden yalnız Sana ibadet edecek kimseler çıkar.' diyerek dua etmiştir. Bu olay Efendimizin hangi iki üstün ahlaki vasfını gösterir?",
            "options": [
                "A) Engin şefkat/merhametini (Rahmet Peygamberi oluşunu) ve zorluklar karşısında asla ümitsizliğe kapılmayan sabrını gösterir.",
                "B) Tebliğ görevinden vazgeçtiğini gösterir.",
                "C) Taif halkına beddua ettiğini gösterir.",
                "D) Sadece Mekke'de kalmaya karar verdiğini gösterir."
            ],
            "answer_text": "1) Âlemlere rahmet olarak gönderildiğini (intikam ve beddua yerine hidayet ve af dileyen merhametini), 2) En zor şartlarda bile davasından vazgeçmeyen sabır, azim ve ümidini gösterir.",
            "rubric": [
                {"criterion": "Merhamet ve hidayet dileme (beddua etmeme) yönünün açıklanması", "points": 5},
                {"criterion": "Sabır, kararlılık ve ümitvar olma yönünün açıklanması", "points": 5}
            ]
        },
        {
            "learning_outcome": "Peygamberimizin çevre bilinci, israf karşıtlığı ve hayvanlara merhametini günlük hayata uyarlar.",
            "cognitive_level": "Uygulama",
            "difficulty": "Kolay",
            "source_page": "Sayfa 116-138",
            "source_context": "Akan nehir kenarında bile abdest alırken suyu israf etmeme uyarısı, ağaç dikme teşviki ve hayvan haklarına dair nebevî sünnet.",
            "arabic_text": "",
            "question_text": "Peygamber Efendimizin (s.a.v.) 'Kıyametin kopacağını bilseniz bile elinizdeki fidanı dikiniz' ve 'Akan bir nehrin kenarında abdest alıyor olsanız dahi suyu israf etmeyiniz' hadis-i şeriflerini günümüzde yaşanan kuraklık ve çevre sorunları açısından nasıl değerlendirirsiniz?",
            "options": [
                "A) Sünnet-i seniyye, doğal kaynakların sınırsız olsa bile israf edilmemesini ve doğanın son ana kadar korunup yeşertilmesini emreder.",
                "B) Su kaynakları bol olduğunda israf yapılabilir.",
                "C) Çevre temizliği dini bir sorumluluk değildir.",
                "D) Ağaç dikmek sadece çiftçilerin görevidir."
            ],
            "answer_text": "Hz. Peygamber 1400 yıl öncesinden sürdürülebilir çevre bilincinin temelini atmıştır. Doğal kaynakları korumak, su israfından kaçınmak ve doğayı ağaçlandırmak her Müslüman için dini ve ahlaki bir görevdir.",
            "rubric": [
                {"criterion": "Kaynakların ve suyun israf edilmemesi ilkesinin açıklanması", "points": 5},
                {"criterion": "Ağaçlandırma ve doğayı koruma bilincinin günümüzle ilişkilendirilmesi", "points": 5}
            ]
        },
        {
            "learning_outcome": "Genç sahabelerin (Mus'ab b. Umeyr, Muaz b. Cebel, Usame b. Zeyd, Hz. Ali) İslam tarihindeki rollerini yorumlar.",
            "cognitive_level": "Yorumlama",
            "difficulty": "Orta",
            "source_page": "Sayfa 127-150",
            "source_context": "İlk öğretmen Mus'ab b. Umeyr, Yemen valisi/kadısı Muaz b. Cebel ve genç komutan Usame b. Zeyd'e verilen sorumluluklar.",
            "arabic_text": "",
            "question_text": "Peygamber Efendimiz (s.a.v.) Medine'ye ilk öğretmen olarak genç sahabe Mus'ab b. Umeyr'i, Yemen'e elçi ve öğretmen olarak Muaz b. Cebel'i göndermiştir. Efendimizin gençlere böylesine önemli görevler vermesi gençliğe bakışı hakkında ne ifade eder?",
            "options": [
                "A) Gençlerin enerjisine, ilmine ve liyakatine güvendiğini; onlara sorumluluk vererek toplumu geleceğe hazırladığını gösterir.",
                "B) Yaşlı sahabelerin görev almak istemediğini gösterir.",
                "C) Gençlere sadece kolay işler verildiğini gösterir.",
                "D) Eğitim işlerinin önemsiz görüldüğünü gösterir."
            ],
            "answer_text": "Hz. Peygamber gençleri sadece geleceğin değil, bugünün de kurucu öznesi olarak görmüş; liyakat, bilgi ve ahlak sahibi gençlere öğretmenlik, elçilik ve komutanlık gibi en üst düzey sorumlulukları güvenle tevdi etmiştir.",
            "rubric": [
                {"criterion": "Peygamberimizin gençlere duyduğu güven ve liyakat ilkesinin açıklanması", "points": 5},
                {"criterion": "Mus'ab b. Umeyr veya Muaz b. Cebel örneği üzerinden eğitimin öneminin vurgulanması", "points": 5}
            ]
        }
    ]

    if subject_id == "kuran":
        general_pool = kuran_pool
    elif subject_id == "siyer":
        general_pool = siyer_pool
    else:
        general_pool = dkab_pool

    grade_int = int(grade)
    grade_curated = GRADE_SPECIFIC_POOLS.get(subject_id, {}).get(grade_int, [])
    dynamic_unit_pool = synthesize_dynamic_questions_for_units(
        subject_id=subject_id,
        subject_name=subject_name,
        grade=grade_int,
        active_units=active_units,
        scenario_items=scenario_items,
        book_context=book_context,
        is_test=is_test
    )

    # Soru bankasında öğretmen tarafından eklenen/düzenlenen aynı sınıf ve ders sorularını da havuza dahil et
    bank_candidates = []
    try:
        import database
        db_items = database.get_question_bank_items(subject=subject_id, grade=grade_int)
        for db_q in db_items:
            if str(db_q.get("question_type", "")).startswith("bep_"):
                continue
            if db_q.get("origin_type") == "teacher_edited":
                bank_candidates.append(db_q)
    except Exception:
        pass

    # Tüm aday havuzunu birleştir ve tekilleştir
    candidate_pool = []
    seen_sigs = set()

    def _add_candidates(items_list, tier_name):
        for it in items_list:
            sig = _normalize_sig(it.get("question_text", ""))
            if not sig or sig in seen_sigs:
                continue
            seen_sigs.add(sig)
            cloned = dict(it)
            cloned["_sig"] = sig
            cloned["_tier"] = tier_name
            candidate_pool.append(cloned)

    _add_candidates(grade_curated, "grade_curated")
    _add_candidates(bank_candidates, "bank")
    _add_candidates(dynamic_unit_pool, "dynamic_unit")
    _add_candidates(general_pool, "general")

    # Hariç tutulacak (ekranda mevcut olan veya son sınavlarda gösterilen) soru imzaları
    exclude_sigs = {_normalize_sig(t) for t in (exclude_questions or []) if _normalize_sig(t)}
    history_key = f"{subject_id}_{grade_int}_{exam_type}"
    recent_list = _RECENT_SERVED_SIGNATURES.setdefault(history_key, [])
    recent_sigs = set(recent_list)

    # Eğer taze (hiç gösterilmemiş) soru sayısı istenen soru adedinden azsa rotasyon geçmişini sıfırla
    fresh_available = [
        c for c in candidate_pool
        if c["_sig"] not in exclude_sigs and c["_sig"] not in recent_sigs
    ]
    if len(fresh_available) < question_count:
        recent_list.clear()
        recent_sigs.clear()

    # Havuzu her çağrıda rastgele karıştır (Deterministik tekrarı tamamen engeller)
    random.shuffle(candidate_pool)

    # Senaryo kazanım dağılımı varsa her soru yuvasını (slot) ilgili kazanıma eşleştir
    expanded_slots = []
    if scenario_items:
        for sc_it in scenario_items:
            cnt = max(1, int(sc_it.get("question_count", 1)))
            for _ in range(cnt):
                expanded_slots.append(sc_it)

    active_unit_nos = set()
    for u_idx, u in enumerate(all_units, 1):
        if u["id"] in selected_unit_ids:
            active_unit_nos.add(u_idx)

    used_pool_indices = set()
    selected = []
    for i in range(question_count):
        slot = expanded_slots[i] if i < len(expanded_slots) else None

        keywords = []
        target_code = ""
        target_unit_no = None
        if slot:
            target_code = str(slot.get("outcome_code", "")).strip().lower()
            if slot.get("unit_no"):
                target_unit_no = int(slot.get("unit_no", 1))
            keywords = [
                w.lower()
                for w in re.findall(r"\w+", f"{slot.get('unit_title', '')} {slot.get('outcome_description', '')}")
                if len(w) > 3
            ]

        best_idx = 0
        best_score = -999999.0

        for p_idx, cand in enumerate(candidate_pool):
            if p_idx in used_pool_indices and len(used_pool_indices) < len(candidate_pool):
                continue

            sig = cand["_sig"]
            score = 0.0

            # 1) Ekranda olan veya yakın zamanda gösterilen soruları güçlü biçimde geri plana at
            if sig in exclude_sigs:
                score -= 10000.0
            if sig in recent_sigs:
                score -= 2500.0

            # Aynı sınav kağıdı içinde aynı cümle kalıbıyla başlayan iki soru olmasını engelle
            cand_prefix = sig[:28]
            if any(_normalize_sig(sel_q.get("question_text", ""))[:28] == cand_prefix for sel_q in selected):
                score -= 500.0

            # 2) Sınıf ve ünite uyumu puanı
            tier = cand.get("_tier", "general")
            if tier == "grade_curated":
                score += 24.0
            elif tier == "bank":
                score += 22.0
            elif tier == "dynamic_unit":
                score += 20.0
            else:
                score += 10.0

            # 3) Zorluk uyumu
            if difficulty in ("Kolay", "Orta", "Zor") and cand.get("difficulty") == difficulty:
                score += 12.0

            # 4) Senaryo kazanımı veya seçili ünite uyumu
            cand_outcome = str(cand.get("learning_outcome", "")).lower()
            cand_unit_no = cand.get("unit_no")
            if slot:
                if target_code and target_code in cand_outcome:
                    score += 35.0
                if target_unit_no and cand_unit_no == target_unit_no:
                    score += 20.0
                if keywords:
                    haystack = f"{cand_outcome} {cand.get('question_text', '')} {cand.get('source_context', '')}".lower()
                    kw_hits = sum(1 for kw in keywords if kw in haystack)
                    score += min(kw_hits * 4.5, 25.0)
            else:
                if cand_unit_no and active_unit_nos and cand_unit_no in active_unit_nos:
                    score += 18.0

            # 5) Çeşitlilik jitter'ı: Aynı kazanımdaki alternatif soruların her tıklamada dönüşümlü gelmesini sağlar
            score += random.uniform(0.0, 14.0)

            if score > best_score:
                best_score = score
                best_idx = p_idx

        used_pool_indices.add(best_idx)
        raw = candidate_pool[best_idx]
        recent_list.append(raw["_sig"])

        # Ünite ve sayfa aralığını belirle
        unit_obj = None
        if slot and slot.get("unit_no"):
            u_no = int(slot.get("unit_no", 1))
            if 1 <= u_no <= len(all_units):
                unit_obj = all_units[u_no - 1]
        elif raw.get("unit_no") and 1 <= int(raw["unit_no"]) <= len(all_units):
            unit_obj = all_units[int(raw["unit_no"]) - 1]
        if not unit_obj:
            unit_obj = active_units[i % len(active_units)] if active_units else None

        unit_page_str = raw.get("source_page", "İlgili Ünite")
        unit_name_str = slot.get("unit_title", "") if slot else raw.get("unit_name", "")
        if unit_obj:
            unit_name_str = unit_obj.get("name", unit_name_str)
            pr = unit_obj.get("page_range")
            if pr and len(pr) == 2:
                unit_page_str = f"Sayfa {pr[0]}-{pr[1]} ({unit_name_str})"

        outcome_str = raw.get("learning_outcome", "")
        if slot and (slot.get("outcome_code") or slot.get("outcome_description")):
            code = slot.get("outcome_code", "").strip()
            desc = slot.get("outcome_description", "").strip()
            outcome_str = f"[{code}] {desc}" if code else desc

        opts = list(raw.get("options", []))
        if is_test and not opts:
            opts = [
                "A) Doğru bilgi ve güzel ahlak ilkelerine uygun hareket etmek",
                "B) Sorumlulukları ertelemek",
                "C) Yalnızca bireysel çıkarları gözetmek",
                "D) Toplumsal kuralları dikkate almamak"
            ]

        item = {
            "q_order": i + 1,
            "points": 10,
            "unit_name": unit_name_str,
            "learning_outcome": outcome_str,
            "question_type": q_type,
            "cognitive_level": raw.get("cognitive_level", "Analiz"),
            "difficulty": difficulty if difficulty in ("Kolay", "Orta", "Zor") else raw.get("difficulty", "Orta"),
            "source_book": book_name,
            "source_page": unit_page_str,
            "source_context": raw.get("source_context", ""),
            "arabic_text": raw.get("arabic_text", ""),
            "question_text": raw.get("question_text", ""),
            "options": opts if is_test else [],
            "answer_text": raw.get("answer_text", ""),
            "rubric": raw.get("rubric", [{"criterion": "Doğru ve gerekçeli açıklama", "points": 10}])
        }
        selected.append(item)

    # Geçmiş listesini aşırı büyümemesi için son 45 soruyla sınırla
    if len(recent_list) > 45:
        del recent_list[:-45]

    _normalize_points(selected)
    return {"questions": selected}


def _generate_bep_fallback_questions(
    subject_id: str,
    grade: int,
    term: str,
    exam_no: str,
    question_count: int,
    selected_unit_ids: list[str],
    bep_opts: dict | None = None,
    exclude_questions: list[str] | None = None
) -> dict:
    """
    MEB Özel Eğitim Hizmetleri Yönetmeliği ve Ölçme Değerlendirme Yönergesi'ne tam uyumlu
    BEP (Bireyselleştirilmiş Eğitim Programı) yerel soru kütüphanesi.
    Eşleştirme, Doğru-Yanlış, Kelime Havuzlu Boşluk Doldurma ve 3 Seçenekli (A, B, C) Çoktan Seçmeli sorular üretir.
    """
    curr = load_curriculum_dict()
    subject_name = curr.get(subject_id, {}).get("name", "Din Kültürü ve Ahlak Bilgisi")
    book_name = f"{grade}. Sınıf {subject_name} MEB Ders Kitabı (BEP Uyarlamalı)"
    bep_opts = bep_opts or {}
    q_style = bep_opts.get("question_style", "karma")
    custom_outcomes_text = (bep_opts.get("custom_outcomes") or "").strip()
    custom_outcomes_list = [line.strip() for line in custom_outcomes_text.split("\n") if line.strip()] if custom_outcomes_text else []

    all_units = get_units(subject_id, grade)
    active_units = [u for u in all_units if u["id"] in selected_unit_ids] or all_units

    # A. DİN KÜLTÜRÜ VE AHLAK BİLGİSİ (DKAB) BEP ÖZEL HAVUZU (5-8. Sınıf Somut & Sadeleştirilmiş)
    dkab_bep_pool = [
        {
            "learning_outcome": "[BEP.DKAB.1] Allah'ın güzel isimlerini (Esmaü'l-Hüsna) temel anlamlarıyla eşleştirir.",
            "question_type": "bep_eslestirme",
            "cognitive_level": "Hatırlama / Kavrama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 16-22 (BEP Temel Kazanım)",
            "source_context": "BEP Kavram Sadeleştirme: Yüce Allah'ın güzel isimleri (Semi, Basir, Rahman, Alim) somut anlamlarıyla eşleştirilir.",
            "arabic_text": "",
            "question_text": (
                "Aşağıda verilen Yüce Allah'ın güzel isimlerini (Esmaü'l-Hüsna) karşısındaki doğru anlamlarıyla ok çizerek eşleştiriniz:\n"
                "1) Semî  .....................  ( a ) Her şeyi gören\n"
                "2) Basîr .....................  ( b ) Her şeyi işiten\n"
                "3) Rahmân ....................  ( c ) Bütün canlılara merhamet eden\n"
                "4) Alîm  .....................  ( d ) Her şeyi çok iyi bilen"
            ),
            "options": [
                "A) 1-b, 2-a, 3-c, 4-d",
                "B) 1-a, 2-b, 3-d, 4-c",
                "C) 1-c, 2-d, 3-a, 4-b"
            ],
            "answer_text": "1) Semî -> (b) Her şeyi işiten | 2) Basîr -> (a) Her şeyi gören | 3) Rahmân -> (c) Bütün canlılara merhamet eden | 4) Alîm -> (d) Her şeyi çok iyi bilen",
            "rubric": [
                {"criterion": "Her doğru eşleştirme için eşit puan verilir (Yazım veya çizgi hatasından puan kırılmaz)", "points": 20}
            ]
        },
        {
            "learning_outcome": "[BEP.DKAB.2] İslam'da paylaşma ve yardımlaşma ibadetlerini (Zekât ve Sadaka) tanır.",
            "question_type": "bep_coktan_secmeli_3",
            "cognitive_level": "Kavrama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 42-48 (BEP Temel Kazanım)",
            "source_context": "BEP 3 Seçenekli Çoktan Seçmeli: Fıkhi hesaplamalar yerine zekât ibadetinin temel ve somut tanımı sorulur.",
            "arabic_text": "",
            "question_text": "Aç ve yoksul insanlara yardım etmek amacıyla zengin Müslümanların yılda bir kez verdiği zorunlu yardıma ne ad verilir? Doğru olanı işaretleyiniz.",
            "options": [
                "A) Zekât",
                "B) Oruç",
                "C) Namaz"
            ],
            "answer_text": "Doğru Seçenek: A) Zekât",
            "rubric": [
                {"criterion": "A seçeneğinin (Zekât) doğru işaretlenmesi veya belirtilmesi", "points": 20}
            ]
        },
        {
            "learning_outcome": "[BEP.DKAB.3] Temel inanç ve ibadet kavramlarını kelime havuzundan seçerek tamamlar.",
            "question_type": "bep_bosluk_doldurma",
            "cognitive_level": "Uygulama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 24-35 (BEP Temel Kazanım)",
            "source_context": "BEP Kelime Havuzu Desteği: Öğrencinin kavramları sıfırdan hatırlaması yerine kutucuktaki kelimelerden seçip yerleştirmesi sağlanır.",
            "arabic_text": "",
            "question_text": (
                "📦 KELİME HAVUZU:  [  Tevhid   |   Tevekkül   |   Ramazan   |   Kâbe  ]\n"
                "Yukarıdaki kutucukta verilen kelimelerden uygun olanları aşağıdaki boşluklara yazınız:\n"
                "1) Allah'ın bir ve tek olmasına .................................... inancı denir.\n"
                "2) Bir işi yaparken bütün önlemleri alıp çalıştıktan sonra Allah'a güvenmeye .................................... denir.\n"
                "3) Müslümanların oruç tuttuğu mübarek ayın adı .................................... ayıdır.\n"
                "4) Namaz kılarken yöneldiğimiz kutsal mekân ....................................'dir."
            ),
            "options": [
                "A) 1: Tevhid - 2: Tevekkül - 3: Ramazan - 4: Kâbe",
                "B) 1: Ramazan - 2: Kâbe - 3: Tevhid - 4: Tevekkül",
                "C) 1: Kâbe - 2: Tevekkül - 3: Tevhid - 4: Ramazan"
            ],
            "answer_text": "1) Tevhid  —  2) Tevekkül  —  3) Ramazan  —  4) Kâbe",
            "rubric": [
                {"criterion": "Kelime havuzundaki her bir kavramın doğru boşluğa yazılması (Yazım hatalarından puan kırılmaz)", "points": 20}
            ]
        },
        {
            "learning_outcome": "[BEP.DKAB.4] Doğru ve yanlış dini/ahlaki bilgileri ayırt eder.",
            "question_type": "bep_dogru_yanlis",
            "cognitive_level": "Kavrama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 50-60 (BEP Temel Kazanım)",
            "source_context": "BEP Doğru/Yanlış Desteği: Günlük yaşamla bağdaşan somut dini ve ahlaki ilkeler D/Y formatında yoklanır.",
            "arabic_text": "",
            "question_text": (
                "Aşağıdaki cümlelerin başına bilgi doğru ise ( D ), yanlış ise ( Y ) yazınız:\n"
                "( ..... ) İslam dini temizliğe, doğruluğa ve yardımlaşmaya büyük önem verir.\n"
                "( ..... ) Günde beş vakit kılınan farz ibadetimiz namazdır.\n"
                "( ..... ) Başkalarının eşyasını izinsiz almak doğru bir davranıştır.\n"
                "( ..... ) Evrendeki her şey Yüce Allah tarafından bir ölçü ve düzen içinde yaratılmıştır."
            ),
            "options": [
                "A) D - D - Y - D",
                "B) D - Y - D - Y",
                "C) Y - D - Y - D"
            ],
            "answer_text": "1) ( D ) Doğru  |  2) ( D ) Doğru  |  3) ( Y ) Yanlış  |  4) ( D ) Doğru",
            "rubric": [
                {"criterion": "Her doğru (D/Y) işaretlemesi için tam puan verilir", "points": 20}
            ]
        },
        {
            "learning_outcome": "[BEP.DKAB.5] İslam'ın ve İmanın temel şartlarını ayırt eder.",
            "question_type": "bep_coktan_secmeli_3",
            "cognitive_level": "Hatırlama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 62-70 (BEP Temel Kazanım)",
            "source_context": "BEP 3 Seçenekli Çoktan Seçmeli: Peygamberlere ve kutsal kitaplara iman kavramı sade bir soru köküyle sorulur.",
            "arabic_text": "",
            "question_text": "Yüce Allah'ın insanlara doğru yolu göstermek için Hz. Muhammed'e (s.a.v.) indirdiği son kutsal kitabın adı nedir? Doğru olanı işaretleyiniz.",
            "options": [
                "A) Kur'an-ı Kerim",
                "B) İncil",
                "C) Tevrat"
            ],
            "answer_text": "Doğru Seçenek: A) Kur'an-ı Kerim",
            "rubric": [
                {"criterion": "A seçeneğinin (Kur'an-ı Kerim) doğru işaretlenmesi", "points": 20}
            ]
        },
        {
            "learning_outcome": "[BEP.DKAB.6] Evrendeki fiziksel ve biyolojik düzeni günlük hayattan somut örneklerle eşleştirir.",
            "question_type": "bep_coktan_secmeli_3",
            "cognitive_level": "Kavrama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 24-28 (BEP Temel Kazanım)",
            "source_context": "BEP Kavram Sadeleştirme: Gece-gündüz oluşumu ve canlıların yaşamı somut örneklerle sorulur.",
            "arabic_text": "",
            "question_text": "Bir insanın hastalanmamak için dengeli beslenmesi, ellerini yıkaması ve doktora gitmesi sonrasında Allah'a dua etmesi hangi doğru davranışı gösterir? İşaretleyiniz.",
            "options": [
                "A) Doğru tevekkül (Tedbir alıp Allah'a güvenmek)",
                "B) Tembellik etmek",
                "C) Hiçbir önlem almamak"
            ],
            "answer_text": "Doğru Seçenek: A) Doğru tevekkül (Tedbir alıp Allah'a güvenmek)",
            "rubric": [
                {"criterion": "A seçeneğinin doğru işaretlenmesi", "points": 20}
            ]
        }
    ]

    # B. PEYGAMBERİMİZİN HAYATI (SİYER) BEP ÖZEL HAVUZU (5-8. Sınıf Kronolojik & Ahlaki Sadeleştirme)
    siyer_bep_pool = [
        {
            "learning_outcome": "[BEP.SİYER.1] Peygamberimizin temel ahlaki vasıflarını ve aile fertlerini Doğru-Yanlış cümleleriyle tanır.",
            "question_type": "bep_dogru_yanlis",
            "cognitive_level": "Hatırlama / Kavrama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 18-32 (BEP Temel Kazanım)",
            "source_context": "BEP Siyer Stratejisi: Peygamberimizin güvenilirliği (Muhammedü'l-Emin), aile fertleri ve merhameti D/Y cümleleriyle yoklanır.",
            "arabic_text": "",
            "question_text": (
                "Aşağıdaki cümlelerin başına bilgi Doğru ise ( D ), Yanlış ise ( Y ) yazınız:\n"
                "( ..... ) Peygamberimiz çok dürüst ve güvenilir olduğu için ona 'Muhammedü'l-Emin' (Güvenilir Muhammed) denmiştir.\n"
                "( ..... ) Peygamberimizin annesinin adı Hz. Âmine, babasının adı Abdullah'tır.\n"
                "( ..... ) Peygamberimiz çocuklara ve yetimlere karşı her zaman çok merhametli davranmıştır.\n"
                "( ..... ) Peygamberimiz insanların kalbini kırmayı ve yalan söylemeyi hoş görürdü."
            ),
            "options": [
                "A) D - D - D - Y",
                "B) D - Y - D - D",
                "C) Y - D - Y - D"
            ],
            "answer_text": "1) ( D ) Doğru  |  2) ( D ) Doğru  |  3) ( D ) Doğru  |  4) ( Y ) Yanlış",
            "rubric": [
                {"criterion": "Her doğru (D/Y) işaretlemesi için eşit puan verilir", "points": 20}
            ]
        },
        {
            "learning_outcome": "[BEP.SİYER.2] Peygamberimizin hayatındaki temel olayları ve şehirleri kelime havuzundan seçerek tamamlar.",
            "question_type": "bep_bosluk_doldurma",
            "cognitive_level": "Uygulama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 46-68 (BEP Temel Kazanım)",
            "source_context": "BEP Kelime Havuzlu Boşluk Doldurma: Mekke, Medine, Ensar ve Hira kavramları kutucuk içinde verilerek cümlede tamamlatılır.",
            "arabic_text": "",
            "question_text": (
                "📦 KELİME HAVUZU:  [  Medine   |   Mekke   |   Hira   |   Ensar  ]\n"
                "Yukarıdaki kutucukta verilen kelimelerden uygun olanları aşağıdaki boşluklara yazınız:\n"
                "1) Peygamberimiz Hz. Muhammed (s.a.v.) 571 yılında .................................... şehrinde doğmuştur.\n"
                "2) Peygamberimize ilk vahiy Nur Dağı'ndaki .................................... Mağarası'nda gelmiştir.\n"
                "3) Peygamberimiz ve Müslümanlar baskılar nedeniyle Mekke'den .................................... şehrine göç etmişlerdir (Hicret).\n"
                "4) Medine'ye göç eden Müslümanlara evlerini açıp yardım eden Medineli Müslümanlara .................................... denir."
            ),
            "options": [
                "A) 1: Mekke - 2: Hira - 3: Medine - 4: Ensar",
                "B) 1: Medine - 2: Mekke - 3: Ensar - 4: Hira",
                "C) 1: Hira - 2: Medine - 3: Mekke - 4: Ensar"
            ],
            "answer_text": "1) Mekke  —  2) Hira  —  3) Medine  —  4) Ensar",
            "rubric": [
                {"criterion": "Kelime havuzundaki her kelimenin doğru boşluğa yerleştirilmesi (Yazım hatalarından puan kırılmaz)", "points": 20}
            ]
        },
        {
            "learning_outcome": "[BEP.SİYER.3] Peygamberimizin yakın aile büyüklerini ve görevlerini eşleştirir.",
            "question_type": "bep_eslestirme",
            "cognitive_level": "Hatırlama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 20-36 (BEP Temel Kazanım)",
            "source_context": "BEP Eşleştirme: Peygamberimizin ailesi ve yakın çevresi basit ve net ifadelerle eşleştirilir.",
            "arabic_text": "",
            "question_text": (
                "Peygamber Efendimizin hayatındaki önemli kişileri karşısındaki açıklamalarla ok çizerek eşleştiriniz:\n"
                "1) Hz. Âmine ........................  ( a ) Peygamberimizin dedesidir.\n"
                "2) Abdülmuttalib ....................  ( b ) Peygamberimizin annesidir.\n"
                "3) Hz. Hatice .......................  ( c ) Peygamberimizin amcasıdır.\n"
                "4) Ebu Talib ........................  ( d ) Peygamberimizin ilk eşi ve ona ilk inanan kişidir."
            ),
            "options": [
                "A) 1-b, 2-a, 3-d, 4-c",
                "B) 1-a, 2-b, 3-c, 4-d",
                "C) 1-d, 2-c, 3-b, 4-a"
            ],
            "answer_text": "1) Hz. Âmine -> (b) Annesidir | 2) Abdülmuttalib -> (a) Dedesidir | 3) Hz. Hatice -> (d) İlk eşidir | 4) Ebu Talib -> (c) Amcasıdır",
            "rubric": [
                {"criterion": "Her doğru eşleştirme için eşit puan verilir", "points": 20}
            ]
        },
        {
            "learning_outcome": "[BEP.SİYER.4] Peygamberimizin doğruluk ve güvenilirlik vasfını tanır.",
            "question_type": "bep_coktan_secmeli_3",
            "cognitive_level": "Kavrama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 38-45 (BEP Temel Kazanım)",
            "source_context": "BEP 3 Seçenekli Çoktan Seçmeli: Muhammedü'l-Emin sıfatının anlamı 3 şıklı sade soruyla ölçülür.",
            "arabic_text": "",
            "question_text": "Peygamber Efendimiz (s.a.v.) hayatı boyunca hiç yalan söylemediği ve emanetleri koruduğu için Mekke halkı ona hangi ismi vermiştir? Doğru olanı işaretleyiniz.",
            "options": [
                "A) Muhammedü'l-Emin (Güvenilir Muhammed)",
                "B) Yolcu",
                "C) Şair"
            ],
            "answer_text": "Doğru Seçenek: A) Muhammedü'l-Emin (Güvenilir Muhammed)",
            "rubric": [
                {"criterion": "A seçeneğinin doğru işaretlenmesi", "points": 20}
            ]
        },
        {
            "learning_outcome": "[BEP.SİYER.5] Peygamberimizin çevreye, hayvanlara ve çocuklara olan şefkatini örnek alır.",
            "question_type": "bep_coktan_secmeli_3",
            "cognitive_level": "Uygulama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 82-96 (BEP Temel Kazanım)",
            "source_context": "BEP 3 Seçenekli Çoktan Seçmeli: Peygamberimizin örnek ahlakı günlük yaşam davranışlarıyla ilişkilendirilir.",
            "arabic_text": "",
            "question_text": "Peygamber Efendimiz (s.a.v.) çocuklara selam verir, yaşlılara yardım eder ve hayvanlara zarar verilmesini yasaklardı. Bu durum Peygamberimizin hangi güzel özelliğini gösterir? İşaretleyiniz.",
            "options": [
                "A) Çok şefkatli ve merhametli olduğunu",
                "B) Sadece ticaretle uğraştığını",
                "C) İnsanlardan uzak durduğunu"
            ],
            "answer_text": "Doğru Seçenek: A) Çok şefkatli ve merhametli olduğunu",
            "rubric": [
                {"criterion": "A seçeneğinin doğru işaretlenmesi", "points": 20}
            ]
        },
        {
            "learning_outcome": "[BEP.SİYER.6] Medine'de inşa edilen Mescid-i Nebevî'nin önemini bilir.",
            "question_type": "bep_coktan_secmeli_3",
            "cognitive_level": "Hatırlama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 118-124 (BEP Temel Kazanım)",
            "source_context": "BEP 3 Seçenekli Çoktan Seçmeli: Hicret sonrası Medine'de yapılan peygamber mescidi sorulur.",
            "arabic_text": "",
            "question_text": "Peygamber Efendimizin (s.a.v.) Medine'ye hicret ettikten sonra arkadaşlarıyla birlikte inşa ettiği mescidin (caminin) adı nedir? Doğru olanı işaretleyiniz.",
            "options": [
                "A) Mescid-i Nebevî (Peygamber Mescidi)",
                "B) Sultanahmet Camii",
                "C) Selimiye Camii"
            ],
            "answer_text": "Doğru Seçenek: A) Mescid-i Nebevî (Peygamber Mescidi)",
            "rubric": [
                {"criterion": "A seçeneğinin doğru işaretlenmesi", "points": 20}
            ]
        }
    ]

    # C. KUR'AN-I KERİM DERSİ BEP ÖZEL HAVUZU (5-8. Sınıf Harf, Hareke ve Temel Sure Tanıma)
    kuran_bep_pool = [
        {
            "learning_outcome": "[BEP.KURAN.1] Kur'an-ı Kerim'in en kısa suresini ve temel surelerin isimlerini tanır.",
            "question_type": "bep_coktan_secmeli_3",
            "cognitive_level": "Hatırlama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 140-148 (BEP Temel Kazanım)",
            "source_context": "BEP Kur'an Stratejisi: Ağır tecvid teorisi yerine bilinen temel surelerin (Kevser, Fatiha, İhlas) isimleri ve özellikleri 3 şıklı olarak sorulur.",
            "arabic_text": "إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ",
            "question_text": "Kur'an-ı Kerim'in en kısa (3 ayetli) suresi aşağıdakilerden hangisidir? Doğru olanı işaretleyiniz.",
            "options": [
                "A) Kevser Suresi",
                "B) Bakara Suresi",
                "C) Yasin Suresi"
            ],
            "answer_text": "Doğru Seçenek: A) Kevser Suresi",
            "rubric": [
                {"criterion": "A seçeneğinin (Kevser Suresi) doğru işaretlenmesi", "points": 20}
            ]
        },
        {
            "learning_outcome": "[BEP.KURAN.2] Kur'an-ı Kerim harflerini okutucu işaretleri (Harekeler: Üstün, Esre, Ötre) görevleriyle eşleştirir.",
            "question_type": "bep_eslestirme",
            "cognitive_level": "Kavrama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 18-30 (BEP Temel Kazanım)",
            "source_context": "BEP Görsel ve Kavramsal Eşleştirme: Temel harekeler (üstün, esre, ötre, cezim) sade açıklamalarıyla eşleştirilir.",
            "arabic_text": "بَ   —   بِ   —   بُ   —   بْ",
            "question_text": (
                "Kur'an-ı Kerim okurken harfleri seslendirmeye yarayan aşağıdaki işaretleri (harekeleri) doğru açıklamalarıyla ok çizerek eşleştiriniz:\n"
                "1) Üstün ( بَ ) ....................  ( a ) Harfin altında bulunur, ince harfleri 'i', kalın harfleri 'ı' sesiyle okutur.\n"
                "2) Esre  ( بِ ) ....................  ( b ) Harfin üstünde bulunur, ince harfleri 'e', kalın harfleri 'a' sesiyle okutur.\n"
                "3) Ötre  ( بُ ) ....................  ( c ) Harfi harekesiz (sesli harf olmadan) sakin okutur.\n"
                "4) Cezim ( بْ ) ....................  ( d ) Harfin üstünde bulunur, harfleri 'u / ü' sesiyle okutur."
            ),
            "options": [
                "A) 1-b, 2-a, 3-d, 4-c",
                "B) 1-a, 2-b, 3-c, 4-d",
                "C) 1-d, 2-c, 3-b, 4-a"
            ],
            "answer_text": "1) Üstün -> (b) 'e / a' okutur | 2) Esre -> (a) 'i / ı' okutur | 3) Ötre -> (d) 'u / ü' okutur | 4) Cezim -> (c) Sakin okutur",
            "rubric": [
                {"criterion": "Her doğru eşleştirme için eşit puan verilir", "points": 20}
            ]
        },
        {
            "learning_outcome": "[BEP.KURAN.3] Temel surelerin isimlerini ve Kur'an kavramlarını kelime havuzundan seçerek tamamlar.",
            "question_type": "bep_bosluk_doldurma",
            "cognitive_level": "Uygulama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 32-55 (BEP Temel Kazanım)",
            "source_context": "BEP Kelime Havuzlu Boşluk Doldurma: Sureleri sıfırdan yazdırmak yerine kutucuktaki kelimelerle tamamlama yaptırılır.",
            "arabic_text": "",
            "question_text": (
                "📦 KELİME HAVUZU:  [  Fâtiha   |   İhlâs   |   Besmele   |   Elif  ]\n"
                "Yukarıdaki kutucukta verilen kelimelerden uygun olanları aşağıdaki boşluklara yazınız:\n"
                "1) Namazların her rekâtında okunan ve Kur'an-ı Kerim'in ilk suresi olan sure .................................... suresidir.\n"
                "2) Allah'ın bir ve tek olduğunu (Ehad ve Samed olduğunu) anlatan sure .................................... suresidir.\n"
                "3) Kur'an okumaya ve her hayırlı işe başlarken 'Bismillâhirrahmânirrahîm' demeye .................................... çekmek denir.\n"
                "4) Kur'an-ı Kerim alfabesinin (Elif-Bâ'nın) ilk harfi .................................... ( ا ) harfidir."
            ),
            "options": [
                "A) 1: Fâtiha - 2: İhlâs - 3: Besmele - 4: Elif",
                "B) 1: İhlâs - 2: Fâtiha - 3: Elif - 4: Besmele",
                "C) 1: Elif - 2: Besmele - 3: Fâtiha - 4: İhlâs"
            ],
            "answer_text": "1) Fâtiha  —  2) İhlâs  —  3) Besmele  —  4) Elif",
            "rubric": [
                {"criterion": "Kelime havuzundaki her kelimenin doğru boşluğa yazılması", "points": 20}
            ]
        },
        {
            "learning_outcome": "[BEP.KURAN.4] Kur'an-ı Kerim okuma adabını ve temel bilgileri Doğru-Yanlış cümleleriyle ayırt eder.",
            "question_type": "bep_dogru_yanlis",
            "cognitive_level": "Kavrama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 12-24 (BEP Temel Kazanım)",
            "source_context": "BEP Doğru/Yanlış Desteği: Kur'an okuma adabı ve temel bilgiler açık ve olumlu cümlelerle yoklanır.",
            "arabic_text": "",
            "question_text": (
                "Aşağıdaki cümlelerin başına bilgi Doğru ise ( D ), Yanlış ise ( Y ) yazınız:\n"
                "( ..... ) Kur'an-ı Kerim okumaya başlarken abdest almak ve Eûzü-Besmele çekmek gerekir.\n"
                "( ..... ) Kur'an-ı Kerim sağdan sola doğru okunur.\n"
                "( ..... ) Şedde ( ّ ) işareti, üzerinde bulunduğu harfi iki kere (vurguyla) okutur.\n"
                "( ..... ) Kur'an-ı Kerim okunurken gürültü yapmak doğru bir davranıştır."
            ),
            "options": [
                "A) D - D - D - Y",
                "B) D - Y - D - D",
                "C) Y - D - Y - D"
            ],
            "answer_text": "1) ( D ) Doğru  |  2) ( D ) Doğru  |  3) ( D ) Doğru  |  4) ( Y ) Yanlış",
            "rubric": [
                {"criterion": "Her doğru (D/Y) işaretlemesi için eşit puan verilir", "points": 20}
            ]
        },
        {
            "learning_outcome": "[BEP.KURAN.5] Kur'an-ı Kerim harflerini Türkçe okunuşlarıyla eşleştirir ve tanır.",
            "question_type": "bep_coktan_secmeli_3",
            "cognitive_level": "Hatırlama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 14-20 (BEP Temel Kazanım)",
            "source_context": "BEP Harf Tanıma: Büyük puntolu Arapça harflerin isimleri 3 seçenekli olarak sorulur.",
            "arabic_text": "م   —   ن   —   ك",
            "question_text": "Yukarıda büyük harflerle verilen üç Kur'an-ı Kerim harfinin sırasıyla isimleri aşağıdakilerden hangisidir? Doğru olanı işaretleyiniz.",
            "options": [
                "A) Mim — Nun — Kef",
                "B) Be — Te — Se",
                "C) Cim — Ha — Hı"
            ],
            "answer_text": "Doğru Seçenek: A) Mim (م) — Nun (ن) — Kef (ك)",
            "rubric": [
                {"criterion": "A seçeneğinin doğru işaretlenmesi", "points": 20}
            ]
        },
        {
            "learning_outcome": "[BEP.KURAN.6] İhlas suresindeki eksik kelimeyi ayet metninden tamamlar.",
            "question_type": "bep_coktan_secmeli_3",
            "cognitive_level": "Hatırlama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 58-64 (BEP Temel Kazanım)",
            "source_context": "BEP Sure Takibi: Sureyi sıfırdan yazdırmak yerine ayetteki eksik kelime 3 seçenek arasından seçtirilir.",
            "arabic_text": "قُلْ هُوَ اللَّهُ أَحَدٌ ۝ اللَّهُ الصَّمَدُ",
            "question_text": "'Kul hüvallâhü ehad. Allâhü's-..................' (İhlâs Suresi 1-2. ayetler) okunuşunda boş bırakılan yere hangi kelime gelmelidir? İşaretleyiniz.",
            "options": [
                "A) Samed",
                "B) Kevser",
                "C) Felak"
            ],
            "answer_text": "Doğru Seçenek: A) Samed (Allâhü's-Samed)",
            "rubric": [
                {"criterion": "A seçeneğinin (Samed) doğru işaretlenmesi", "points": 20}
            ]
        }
    ]

    if subject_id == "kuran":
        base_pool = list(kuran_bep_pool)
    elif subject_id == "siyer":
        base_pool = list(siyer_bep_pool)
    else:
        base_pool = list(dkab_bep_pool)

    extra_pool = EXTRA_BEP_POOLS.get(subject_id, [])
    dynamic_bep_pool = synthesize_dynamic_bep_questions_for_units(
        subject_id=subject_id,
        subject_name=subject_name,
        grade=int(grade),
        active_units=active_units
    )

    combined_bep_candidates = []
    seen_sigs = set()
    for q_cand in (base_pool + extra_pool + dynamic_bep_pool):
        sig = _normalize_sig(q_cand.get("question_text", ""))
        if not sig or sig in seen_sigs:
            continue
        seen_sigs.add(sig)
        c_copy = dict(q_cand)
        c_copy["_sig"] = sig
        combined_bep_candidates.append(c_copy)

    exclude_sigs = {_normalize_sig(t) for t in (exclude_questions or []) if _normalize_sig(t)}
    history_key = f"{subject_id}_{int(grade)}_bep_sinav"
    recent_list = _RECENT_SERVED_SIGNATURES.setdefault(history_key, [])
    recent_sigs = set(recent_list)

    fresh_bep = [
        c for c in combined_bep_candidates
        if c["_sig"] not in exclude_sigs and c["_sig"] not in recent_sigs
    ]
    if len(fresh_bep) < question_count:
        recent_list.clear()
        recent_sigs.clear()

    random.shuffle(combined_bep_candidates)

    # Karma modda her soru tipinden (eşleştirme, D/Y, boşluk doldurma, 3 şıklı) dengeli gelmesi için hedef sıra
    karma_type_cycle = ["bep_eslestirme", "bep_dogru_yanlis", "bep_bosluk_doldurma", "bep_coktan_secmeli_3"]
    used_indices = set()
    selected = []

    for i in range(question_count):
        preferred_type = karma_type_cycle[i % len(karma_type_cycle)] if q_style == "karma" else None
        best_idx = 0
        best_score = -999999.0

        for idx, cand in enumerate(combined_bep_candidates):
            if idx in used_indices and len(used_indices) < len(combined_bep_candidates):
                continue
            sig = cand["_sig"]
            score = 0.0
            if sig in exclude_sigs:
                score -= 10000.0
            if sig in recent_sigs:
                score -= 2500.0

            c_type = cand.get("question_type", "")
            if q_style == "coktan_secmeli_3" and c_type == "bep_coktan_secmeli_3":
                score += 25.0
            elif q_style == "eslestirme_dy_bosluk" and c_type in ("bep_eslestirme", "bep_dogru_yanlis", "bep_bosluk_doldurma"):
                score += 25.0
            elif preferred_type and c_type == preferred_type:
                score += 30.0

            score += random.uniform(0.0, 12.0)
            if score > best_score:
                best_score = score
                best_idx = idx

        used_indices.add(best_idx)
        raw = combined_bep_candidates[best_idx]
        recent_list.append(raw["_sig"])

        unit_obj = active_units[i % len(active_units)] if active_units else None
        unit_name_str = unit_obj.get("name", "Temel BEP Ünitesi") if unit_obj else "Temel BEP Ünitesi"
        unit_page_str = raw["source_page"]
        if unit_obj and unit_obj.get("page_range") and len(unit_obj["page_range"]) == 2:
            pr = unit_obj["page_range"]
            unit_page_str = f"Sayfa {pr[0]}-{pr[1]} ({unit_name_str} - BEP Uyarlaması)"

        outcome_str = custom_outcomes_list[i % len(custom_outcomes_list)] if custom_outcomes_list else raw["learning_outcome"]

        q_type = raw["question_type"]
        opts = list(raw.get("options", []))

        if q_style == "coktan_secmeli_3":
            q_type = "bep_coktan_secmeli_3"
            opts = opts[:3] if opts else ["A) Doğru Seçenek", "B) İkinci Seçenek", "C) Üçüncü Seçenek"]
        elif q_style == "eslestirme_dy_bosluk":
            if q_type == "bep_coktan_secmeli_3":
                q_type = "bep_kisa_cevap"
            opts = []
        else:
            if q_type != "bep_coktan_secmeli_3":
                opts = []

        item = {
            "q_order": i + 1,
            "points": 20,
            "unit_name": unit_name_str,
            "learning_outcome": outcome_str,
            "question_type": q_type,
            "cognitive_level": raw["cognitive_level"],
            "difficulty": "Kolay",
            "source_book": book_name,
            "source_page": unit_page_str,
            "source_context": raw["source_context"],
            "arabic_text": raw["arabic_text"],
            "question_text": raw["question_text"],
            "options": opts,
            "answer_text": raw["answer_text"],
            "rubric": [dict(r) for r in raw.get("rubric", [{"criterion": "Doğru işaretleme / cevap", "points": 20}])]
        }
        selected.append(item)

    if len(recent_list) > 40:
        del recent_list[:-40]

    _normalize_points(selected)
    # Rubrik puanlarını da soru puanına eşitle (BEP net puanlama ilkesi: örn. 4x25p veya 5x20p)
    for q in selected:
        if q.get("rubric") and len(q["rubric"]) > 0:
            q["rubric"][0]["points"] = q["points"]

    return {"questions": selected}
