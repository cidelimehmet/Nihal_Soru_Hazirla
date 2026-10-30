"""
Zenginleştirilmiş Sınıf, Ünite ve Kazanım Bazlı Soru Havuzu & Dinamik Varyasyon Motoru
MEB 2026 Türkiye Yüzyılı Maarif Modeli & Özel Eğitim (BEP) Uyumlu
Her ders (DKAB, Kur'an-ı Kerim, Siyer) ve her sınıf (5, 6, 7, 8) için çoklu soru varyasyonları üretir.
"""

import re
import random


# ==============================================================================
# 1. SINIF VE ÜNİTE BAZLI ÖZGÜN SORU HAVUZU (5, 6, 7 ve 8. SINIFLAR)
# ==============================================================================

GRADE_SPECIFIC_POOLS = {
    "dkab": {
        5: [
            {
                "unit_no": 1,
                "learning_outcome": "[DKAB.5.1.1] Evrendeki mükemmel düzen ile Allah'ın varlığı ve birliği arasında ilişki kurar.",
                "cognitive_level": "Analiz",
                "difficulty": "Kolay",
                "source_page": "Sayfa 14-20",
                "source_context": "Güneş'in, Ay'ın ve Dünya'nın yörüngeleri, mevsimlerin ardışıklığı ve canlıların uyum içinde yaşaması Allah'ın varlığının ve birliğinin (Tevhid) delilleridir.",
                "arabic_text": "قُلْ هُوَ اللَّهُ أَحَدٌ",
                "question_text": "Fen bilimleri dersinde Dünya'nın Güneş'e olan uzaklığının çok hassas bir ölçüde olduğunu, biraz yaklaşsa aşırı sıcaktan, biraz uzaklaşsa aşırı soğuktan yaşamın sona ereceğini öğrenen 5. sınıf öğrencisi Elif, bu durumu Din Kültürü dersindeki 'Evrendeki Düzen ve Tevhid İnancı' konusuyla nasıl ilişkilendirmelidir? Açıklayınız.",
                "options": [
                    "A) Evrendeki bu kusursuz ölçü ve düzenin tesadüfen olamayacağını, her şeyi bilen ve gücü yeten tek bir Yaratıcının (Allah'ın) varlığını kanıtladığını gösterir.",
                    "B) Doğa olaylarının kendi kendine gerçekleştiğini gösterir.",
                    "C) Evrende birden fazla yaratıcı olduğunu gösterir.",
                    "D) Düzenin sadece Dünya ile sınırlı olduğunu ifade eder."
                ],
                "answer_text": "Elif, evrendeki bu hassas dengenin kendiliğinden veya tesadüfen oluşamayacağını; gökleri, yeri ve canlıları kusursuz bir ölçüyle yaratan ve yöneten tek bir Yaratıcının (Allah'ın) varlığına ve birliğine (Tevhid) delil olduğunu ifade etmelidir.",
                "rubric": [
                    {"criterion": "Evrendeki hassas dengenin tesadüfen oluşamayacağının belirtilmesi", "points": 5},
                    {"criterion": "Bu düzenin Allah'ın varlığına ve birliğine (Tevhid) delil olduğunun açıklanması", "points": 5}
                ]
            },
            {
                "unit_no": 1,
                "learning_outcome": "[DKAB.5.1.2] Allah'ın (c.c.) isim ve sıfatlarının (Esmaü'l-Hüsna) anlamlarını açıklar.",
                "cognitive_level": "Yorumlama",
                "difficulty": "Orta",
                "source_page": "Sayfa 22-30",
                "source_context": "Esmaü'l-Hüsna'dan Rahman, Rahim, Alim, Semi, Basir ve Kadir isimlerinin anlamları ve insan davranışlarına etkisi.",
                "arabic_text": "وَلِلَّهِ الْأَسْمَاءُ الْحُسْنَىٰ فَادْعُوهُ بِهَا",
                "question_text": "Yüce Allah'ın her şeyi görmesi (Basîr), her şeyi işitmesi (Semî) ve gizli-açık her şeyi bilmesi (Alîm) sıfatlarına içtenlikle inanan bir insanın, yalnız kaldığında veya toplum içinde davranışlarına nasıl dikkat etmesi beklenir? Örnek vererek açıklayınız.",
                "options": [
                    "A) Hiç kimsenin görmediği yerde bile Allah'ın kendisini gördüğünü ve bildiğini düşünerek kötülükten, yalandan ve hileden uzak durur.",
                    "B) Yalnızca insanların yanında güzel davranır.",
                    "C) Yalnız kaldığında kurallara uymayabilir.",
                    "D) Sadece ibadet ederken dikkatli olur."
                ],
                "answer_text": "Allah'ın Semî, Basîr ve Alîm olduğuna inanan bir kişi, yanında kimse olmasa bile Allah'ın kendisini gördüğünü ve duyduğunu bilir. Bu bilinç ona özdenetim kazandırır; gizlice hile yapmaz, yalan söylemez ve her yerde dürüst davranır.",
                "rubric": [
                    {"criterion": "Semî, Basîr ve Alîm isimlerinin anlamlarının doğru ifade edilmesi", "points": 5},
                    {"criterion": "İnsana kazandırdığı özdenetim ve dürüstlük bilincinin örneklendirilmesi", "points": 5}
                ]
            },
            {
                "unit_no": 1,
                "learning_outcome": "[DKAB.5.1.4] Dua ile ilgili ayet ve hadislerden hareketle duanın anlamını ve önemini yorumlar.",
                "cognitive_level": "Değerlendirme",
                "difficulty": "Kolay",
                "source_page": "Sayfa 34-40",
                "source_context": "Dua kulun Rabbine yönelmesi, şükretmesi ve yalnız olmadığını hissetmesidir. Dua adabı ve Rabbena duaları.",
                "arabic_text": "ادْعُونِي أَسْتَجِبْ لَكُمْ",
                "question_text": "'Bana dua edin, duanıza karşılık vereyim.' (Mü'min, 60) ayetini dikkate alarak; duanın insan ile Yüce Allah arasındaki iletişime katkısını ve dua ederken nelere dikkat edilmesi gerektiğini (dua adabını) yazınız.",
                "options": [
                    "A) Dua kulu Allah'a yakınlaştırır, insana güven ve ümit verir; samimiyetle, sadece Allah'tan isteyerek ve iyi şeyler dileyerek yapılmalıdır.",
                    "B) Dua sadece sıkıntılı anlarda yapılmalıdır.",
                    "C) Çalışmadan sadece dua etmek yeterlidir.",
                    "D) Dua yalnızca belirli dillerde yapılabilir."
                ],
                "answer_text": "Dua, insanın sevincini ve sıkıntısını Rabbiyle paylaşarak yalnız olmadığını hissetmesini sağlar. Dua ederken içten ve samimi olunmalı, önce üzerimize düşen gayret gösterilmeli, kendimiz, ailemiz ve tüm inananlar için hayırlı şeyler istenmelidir.",
                "rubric": [
                    {"criterion": "Duanın kul ile Allah arasındaki bağı güçlendirdiğinin ve huzur verdiğinin açıklanması", "points": 5},
                    {"criterion": "Dua adabından (samimiyet, gayret gösterme, hayır isteme) en az iki maddenin yazılması", "points": 5}
                ]
            },
            {
                "unit_no": 1,
                "learning_outcome": "[DKAB.5.1.6] İhlas suresini anlamıyla birlikte analiz eder.",
                "cognitive_level": "Analiz",
                "difficulty": "Orta",
                "source_page": "Sayfa 42-47",
                "source_context": "İhlas Suresi Tevhid inancının özüdür; Allah'ın Ehad (bir) ve Samed (hiçbir şeye muhtaç olmayan) olduğunu bildirir.",
                "arabic_text": "قُلْ هُوَ اللَّهُ أَحَدٌ ۝ اللَّهُ الصَّمَدُ ۝ لَمْ يَلِدْ وَلَمْ يُولَدْ ۝ وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ",
                "question_text": "İhlas Suresi'nde Yüce Allah'ın tanıtıldığı dört temel özelliği (sure mealinden hareketle) maddeler halinde yazarak 'Samed' isminin ne anlama geldiğini açıklayınız.",
                "options": [
                    "A) Allah'ın bir olduğu (Ehad), hiçbir şeye muhtaç olmadığı (Samed), doğurmadığı ve doğurulmadığı, hiçbir denginin bulunmadığı bildirilir.",
                    "B) Yalnızca namaz ibadetinin kuralları anlatılır.",
                    "C) Geçmiş kavimlerin kıssaları anlatılır.",
                    "D) Sadece meleklerin görevleri sıralanır."
                ],
                "answer_text": "1) Allah birdir (Ehad). 2) Allah Samed'dir (Her şey O'na muhtaçtır, O hiçbir şeye muhtaç değildir). 3) O doğurmamış ve doğurulmamıştır. 4) Hiçbir şey O'na denk ve benzer değildir.",
                "rubric": [
                    {"criterion": "İhlas Suresi'ndeki tevhid ilkelerinin doğru sıralanması", "points": 5},
                    {"criterion": "Samed kavramının (her şeyin O'na muhtaç olması, O'nun hiçbir şeye muhtaç olmaması) açıklanması", "points": 5}
                ]
            },
            {
                "unit_no": 2,
                "learning_outcome": "[DKAB.5.2.1] Ramazan ayı ve orucun bireysel/toplumsal önemini açıklar.",
                "cognitive_level": "Yorumlama",
                "difficulty": "Orta",
                "source_page": "Sayfa 50-64",
                "source_context": "Ramazan ayı Kur'an ayıdır; sahur, iftar, teravih, mukabele ve fitre kavramlarıyla yardımlaşma ve sabır bilinci gelişir.",
                "arabic_text": "شَهْرُ رَمَضَانَ الَّذِي أُنزِلَ فِيهِ الْقُرْآنُ",
                "question_text": "Ramazan ayında tutulan orucun insana 'sabır' ve 'nimetlerin kıymetini bilme' yönünden ne gibi faydalar sağladığını; ayrıca 'fitre (fıtır sadakası)' ile 'mukabele' kavramlarının anlamlarını açıklayınız.",
                "options": [
                    "A) Oruç iradeyi güçlendirip yoksulların halini anlamayı sağlar; fitre Ramazan'da verilen yardımdır, mukabele ise Kur'an'ın karşılıklı okunup takip edilmesidir.",
                    "B) Oruç sadece aç kalmaktır; mukabele ise bayramlaşmaktır.",
                    "C) Fitre sadece Kurban Bayramı'nda verilir.",
                    "D) Mukabele orucu açma vaktine denir."
                ],
                "answer_text": "Oruç, insanın iradesine hâkim olmasını (sabır) ve aç-susuz kalarak yoksullarla empati kurup nimetlere şükretmesini sağlar. Fitre: Ramazan ayında bayramdan önce ihtiyaç sahiplerine verilen sadakadır. Mukabele: Ramazan'da Kur'an-ı Kerim'in bir kişi tarafından okunup diğerlerinin takip etmesidir.",
                "rubric": [
                    {"criterion": "Orucun sabır, şükür ve empati kazandırma yönünün açıklanması", "points": 5},
                    {"criterion": "Fitre ve mukabele kavramlarının doğru tanımlanması", "points": 5}
                ]
            },
            {
                "unit_no": 3,
                "learning_outcome": "[DKAB.5.3.1] Toplumsal hayatta nezaket, selamlaşma ve iletişim adabına uymanın önemini değerlendirir.",
                "cognitive_level": "Uygulama",
                "difficulty": "Kolay",
                "source_page": "Sayfa 92-118",
                "source_context": "Selamlaşma, konuşma, dinleme ve sofra adabı insanların birbirine sevgi ve saygı duymasını sağlar.",
                "arabic_text": "السَّلَامُ عَلَيْكُمْ",
                "question_text": "Peygamber Efendimiz (s.a.v.) 'Size yaptığınız takdirde birbirinizi seveceğiniz bir iş göstereyim mi? Aranızda selamı yayınız!' buyurmuştur. Selamlaşmanın, konuşma ve sofra adabına uymanın arkadaşlık ilişkilerimize katkısını 3 maddeyle açıklayınız.",
                "options": [
                    "A) İnsanlar arasında güven ve sevgi bağı kurar, kırgınlıkları önler, nezaketli ve huzurlu bir ortam oluşturur.",
                    "B) İletişimi zorlaştırır.",
                    "C) Sadece resmi ortamlarda geçerlidir.",
                    "D) Sofra adabı sadece tek başına yemek yemektir."
                ],
                "answer_text": "1) Selamlaşmak insanlara 'benden sana zarar gelmez' güveni verir ve sevgiyi artırır. 2) Konuşurken söz kesmemek ve güler yüzlü olmak saygıyı güçlendirir. 3) Sofra adabına (Besmele çekmek, israf etmemek, şükretmek) uymak bereket ve görgü kazandırır.",
                "rubric": [
                    {"criterion": "Selamlaşmanın güven ve sevgi oluşturma etkisinin açıklanması", "points": 5},
                    {"criterion": "Konuşma veya sofra adabına dair en az iki kuralın doğru yazılması", "points": 5}
                ]
            }
        ],
        6: [
            {
                "unit_no": 1,
                "learning_outcome": "[DKAB.6.1.2] Peygamberlerin sıfatlarını (Sıdk, Emanet, Fetanet, İsmet, Tebliğ) ve görevlerini örneklerle açıklar.",
                "cognitive_level": "Analiz",
                "difficulty": "Orta",
                "source_page": "Sayfa 16-26",
                "source_context": "Yüce Allah'ın insanlara rehber olarak gönderdiği peygamberlerin ortak nitelikleri: Sıdk, Emanet, Fetanet, İsmet ve Tebliğ.",
                "arabic_text": "",
                "question_text": "Bir peygamberin Allah'tan aldığı vahiyleri hiçbir ekleme veya çıkarma yapmadan insanlara eksiksiz iletmesi hangi sıfatıyla ilgilidir? Peygamberlerin 'Sıdk', 'Emanet', 'Fetanet' ve 'İsmet' sıfatlarının anlamlarını da kısaca yazınız.",
                "options": [
                    "A) Vahyi iletmesi Tebliğ'dir. Sıdk: Doğruluk, Emanet: Güvenilirlik, Fetanet: Akıllı ve zeki olma, İsmet: Günah işlemekten korunmuş olmadır.",
                    "B) Vahyi iletmesi Fetanet'tir.",
                    "C) İsmet sıfatı sadece zengin olmak demektir.",
                    "D) Peygamberlerin sıfatları sadece son peygambere aittir."
                ],
                "answer_text": "Allah'tan aldığı mesajları eksiksiz iletmesi TEBLİĞ sıfatıdır. Sıdk: Doğru ve dürüst olmak; Emanet: Güvenilir olmak; Fetanet: Akıllı, zeki ve ileri görüşlü olmak; İsmet: Günah işlemekten korunmuş olmaktır.",
                "rubric": [
                    {"criterion": "Tebliğ sıfatının doğru tespit edilmesi", "points": 4},
                    {"criterion": "Sıdk, Emanet, Fetanet ve İsmet sıfatlarının anlamlarının doğru yazılması", "points": 6}
                ]
            },
            {
                "unit_no": 1,
                "learning_outcome": "[DKAB.6.1.3] İlahi kitapları ve gönderildikleri peygamberleri eşleştirerek vahyin gönderiliş amacını açıklar.",
                "cognitive_level": "Kavrama",
                "difficulty": "Kolay",
                "source_page": "Sayfa 27-35",
                "source_context": "Dört büyük ilahi kitap (Tevrat, Zebur, İncil, Kur'an-ı Kerim) ve Suhuf (sahifeler) ile vahyin insanlığa rehberliği.",
                "arabic_text": "",
                "question_text": "Yüce Allah'ın tarih boyunca insanlara gönderdiği dört büyük ilahi kitabın isimlerini ve hangi peygamberlere indirildiğini eşleştirerek; ilahi kitapların gönderiliş amacını açıklayınız.",
                "options": [
                    "A) Tevrat -> Hz. Musa, Zebur -> Hz. Davud, İncil -> Hz. İsa, Kur'an-ı Kerim -> Hz. Muhammed (s.a.v.). Amacı insanlara doğru yolu ve Tevhid inancını göstermektir.",
                    "B) Tevrat -> Hz. İsa, Zebur -> Hz. Musa, İncil -> Hz. Davud.",
                    "C) İlahi kitaplar sadece tarih bilgisi vermek için gönderilmiştir.",
                    "D) Suhuf dört büyük kitaptan biridir."
                ],
                "answer_text": "1) Tevrat -> Hz. Musa (a.s.), 2) Zebur -> Hz. Davud (a.s.), 3) İncil -> Hz. İsa (a.s.), 4) Kur'an-ı Kerim -> Hz. Muhammed (s.a.v.). Gönderiliş amacı: İnsanlara Tevhid inancını öğretmek, iyi ve güzeli gösterip dünya-ahiret mutluluğuna ulaştırmaktır.",
                "rubric": [
                    {"criterion": "Dört büyük kitabın peygamberleriyle doğru eşleştirilmesi", "points": 6},
                    {"criterion": "İlahi kitapların gönderiliş amacının (rehberlik, tevhid, mutluluk) açıklanması", "points": 4}
                ]
            },
            {
                "unit_no": 2,
                "learning_outcome": "[DKAB.6.2.2] Namazın içindeki ve dışındaki farzlarını (şartlarını ve rükünlerini) ayırt eder.",
                "cognitive_level": "Uygulama",
                "difficulty": "Orta",
                "source_page": "Sayfa 52-68",
                "source_context": "Namaza hazırlık şartları (dışındaki farzlar) ve namazın rükünleri (içindeki farzlar) ile abdest, gusül ve teyemmüm.",
                "arabic_text": "",
                "question_text": "Namaz ibadetinin geçerli olması için namaza başlamadan önce yerine getirilmesi gereken 'Namazın Dışındaki Farzlar (Hazırlık Şartları)' ile namaz esnasında yapılan 'Namazın İçindeki Farzlar (Rükünler)' nelerdir? Maddeler halinde yazınız.",
                "options": [
                    "A) Dışındakiler: Hadesten taharet, Necasetten taharet, Setr-i avret, İstikbal-i kıble, Vakit, Niyet. İçindekiler: İftitah tekbiri, Kıyam, Kıraat, Rükû, Secde, Ka'de-i ahîre.",
                    "B) Sadece niyet etmek ve selam vermek yeterlidir.",
                    "C) Ezan okumak namazın içindeki farzlardandır.",
                    "D) Rükû ve secde namazın dışındaki şartlardandır."
                ],
                "answer_text": "Dışındaki Farzlar (6): Hadesten taharet (abdest), Necasetten taharet (beden/elbise/yer temizliği), Setr-i avret (örtünme), İstikbal-i kıble (Kâbe'ye yönelme), Vakit, Niyet. İçindekiler (6): İftitah tekbiri, Kıyam (ayakta durmak), Kıraat (Kur'an okumak), Rükû, Secde, Ka'de-i ahîre (son oturuş).",
                "rubric": [
                    {"criterion": "Namazın dışındaki 6 şartın doğru yazılması", "points": 5},
                    {"criterion": "Namazın içindeki 6 rüknün doğru yazılması", "points": 5}
                ]
            },
            {
                "unit_no": 2,
                "learning_outcome": "[DKAB.6.2.3] Abdest, boy abdesti (gusül) ve teyemmümün hangi durumlarda ve nasıl alındığını açıklar.",
                "cognitive_level": "Uygulama",
                "difficulty": "Orta",
                "source_page": "Sayfa 54-60",
                "source_context": "Maddi ve manevi temizlik kapsamında abdestin farzları, guslün farzları ve su bulunmadığında teyemmüm uygulaması.",
                "arabic_text": "",
                "question_text": "Doğa yürüyüşüne çıkan Ömer ve arkadaşları namaz vakti girdiğinde yanlarında abdest alacak su kalmadığını ve yakınlarda su kaynağı bulunmadığını fark etmişlerdir. Bu durumda İslam'ın kolaylık ilkesi gereği hangi temizlik uygulamasını, ne ile ve nasıl yapmalıdırlar?",
                "options": [
                    "A) Temiz toprak veya toprak cinsinden bir yüzeyle Teyemmüm almalıdırlar (Niyet edip elleri toprağa vurarak yüzü ve kolları meshetmek).",
                    "B) Namazı tamamen terk etmelidirler.",
                    "C) Abdestsiz namaz kılmalıdırlar.",
                    "D) Yağmur yağana kadar günlerce beklemelidirler."
                ],
                "answer_text": "Su bulunmadığında veya suyu kullanma imkânı olmadığında TEYEMMÜM yapılır. Niyet edilir, eller temiz toprağa (veya toprak cinsinden bir yüzeye) sürülüp silkelendikten sonra yüz meshedilir; ikinci kez vurulup sağ ve sol kollar dirseklerle birlikte meshedilir.",
                "rubric": [
                    {"criterion": "Teyemmüm kavramının ve su bulunmadığında yapıldığının belirtilmesi", "points": 5},
                    {"criterion": "Teyemmümün farzlarının (niyet + yüzü ve kolları temiz toprakla meshetmek) açıklanması", "points": 5}
                ]
            },
            {
                "unit_no": 3,
                "learning_outcome": "[DKAB.6.3.1] Zararlı alışkanlıklardan korunma yollarını ve kul hakkı bilincini değerlendirir.",
                "cognitive_level": "Değerlendirme",
                "difficulty": "Kolay",
                "source_page": "Sayfa 88-110",
                "source_context": "Alkol, kumar, sigara ve teknoloji bağımlılığı gibi zararlı alışkanlıkların bireye ve topluma zararları ile korunma yolları.",
                "arabic_text": "",
                "question_text": "İslam dininde alkol, uyuşturucu, sigara ve kumar gibi zararlı alışkanlıkların yasaklanmasının temel sebepleri nelerdir? Gençlerin bu tür zararlı alışkanlıklardan ve bağımlılıklardan korunması için 3 öneri yazınız.",
                "options": [
                    "A) Aklı, sağlığı, aile huzurunu ve malı koruduğu için yasaklanmıştır; iyi arkadaş seçimi, spor/sanat faaliyetleri ve 'hayır' diyebilme becerisiyle korunulur.",
                    "B) Sadece maddi masraf olduğu için yasaklanmıştır.",
                    "C) Merak edip bir kez denemekte sakınca yoktur.",
                    "D) Zararlı alışkanlıklar sadece kişinin kendisini ilgilendirir."
                ],
                "answer_text": "Bu alışkanlıklar insanın aklını, beden sağlığını, malını ve aile huzurunu yok ettiği için yasaklanmıştır. Korunmak için: 1) Doğru ve dürüst arkadaşlar seçilmeli, 2) Yanlış tekliflere kararlılıkla 'Hayır!' denilmeli, 3) Spor, okuma ve faydalı sosyal etkinliklere yönelinmelidir.",
                "rubric": [
                    {"criterion": "Akıl, can/sağlık ve malı koruma gerekçesinin açıklanması", "points": 5},
                    {"criterion": "Zararlı alışkanlıklardan korunma yollarından en az üçünün yazılması", "points": 5}
                ]
            }
        ],
        7: [
            {
                "unit_no": 1,
                "learning_outcome": "[DKAB.7.1.1] Varlıklar âlemini sınıflandırarak meleklerin özelliklerini ve dört büyük meleğin görevlerini açıklar.",
                "cognitive_level": "Analiz",
                "difficulty": "Kolay",
                "source_page": "Sayfa 12-25",
                "source_context": "Görülen (şehadet) ve görülmeyen (gayb) varlıklar; melek, cin ve şeytanın farkları ile Cebrail, Mikail, İsrafil ve Azrail'in görevleri.",
                "arabic_text": "",
                "question_text": "Dört büyük melek olan Cebrail, Mikail, İsrafil ve Azrail'in (a.s.) görevlerini sırasıyla yazarak; insanın sağında ve solunda bulunup iyilik ve kötülüklerini kaydeden meleklere ne ad verildiğini belirtiniz.",
                "options": [
                    "A) Cebrail: Vahiy, Mikail: Doğa olayları/rızık, İsrafil: Sûr'a üfleme, Azrail: Can alma meleğidir. Yazıcı meleklere Kirâmen Kâtibîn denir.",
                    "B) Cebrail: Doğa olayları, Mikail: Vahiy meleğidir. Yazıcı meleklere Münker-Nekir denir.",
                    "C) İsrafil: Rızık meleğidir.",
                    "D) Melekler geleceği tek başlarına bilirler."
                ],
                "answer_text": "1) Cebrail: Peygamberlere vahiy getiren melektir. 2) Mikail: Rızık ve doğa olaylarını (yağmur, rüzgâr vb.) yöneten melektir. 3) İsrafil: Kıyamet günü Sûr'a üfleyecek melektir. 4) Azrail: Eceli gelenlerin canını alan melektir. İnsanın amellerini yazan meleklere 'Kirâmen Kâtibîn' denir.",
                "rubric": [
                    {"criterion": "Dört büyük meleğin görevlerinin doğru eşleştirilmesi", "points": 6},
                    {"criterion": "Kirâmen Kâtibîn (yazıcı melekler) kavramının doğru belirtilmesi", "points": 4}
                ]
            },
            {
                "unit_no": 1,
                "learning_outcome": "[DKAB.7.1.3] Ahiret hayatının aşamalarını (Kıyamet, Ba's, Haşr, Mahşer, Mizan) ve davranışlara etkisini yorumlar.",
                "cognitive_level": "Yorumlama",
                "difficulty": "Orta",
                "source_page": "Sayfa 26-40",
                "source_context": "Dünya hayatı ahiretin tarlasıdır. Berzah, Kıyamet, Ba's, Haşr, Mahşer ve Mizan kavramları ile hesap bilinci.",
                "arabic_text": "فَمَن يَعْمَلْ مِثْقَالَ ذَرَّةٍ خَيْرًا يَرَهُ",
                "question_text": "'Kim zerre miktarı hayır yapmışsa onu görür; kim de zerre miktarı şer (kötülük) işlemişse onu görür.' (Zilzâl, 7-8) ayetinden hareketle; ahiret hayatının aşamalarından 'Ba's', 'Haşr/Mahşer' ve 'Mizan' kavramlarının anlamlarını açıklayınız.",
                "options": [
                    "A) Ba's: Kıyametten sonra yeniden diriliş, Haşr/Mahşer: Hesap için toplanma ve toplanılan meydan, Mizan: Amellerin tartıldığı ilahi adalet terazisidir.",
                    "B) Ba's: Dünya hayatı, Mizan: Kabir hayatıdır.",
                    "C) Haşr: Sûr'a ilk üfleyiştir.",
                    "D) Mizan sadece ibadet vakitlerini gösterir."
                ],
                "answer_text": "Ba's: Kıyamet koptuktan sonra insanların yeniden diriltilmesidir. Haşr / Mahşer: Diriltilen tüm insanların hesap vermek üzere toplanması (Haşr) ve toplandıkları büyük meydandır (Mahşer). Mizan: İnsanların iyilik ve kötülüklerinin tartıldığı ilahi adalet terazisidir.",
                "rubric": [
                    {"criterion": "Ba's ve Haşr/Mahşer kavramlarının doğru tanımlanması", "points": 5},
                    {"criterion": "Mizan kavramının ve ayetteki ilahi adalet mesajının açıklanması", "points": 5}
                ]
            },
            {
                "unit_no": 2,
                "learning_outcome": "[DKAB.7.2.2] Hac ve umre ile ilgili temel kavramları (İhram, Tavaf, Sa'y, Vakfe, Mikat) ayırt eder.",
                "cognitive_level": "Uygulama",
                "difficulty": "Orta",
                "source_page": "Sayfa 50-76",
                "source_context": "Haccın farzları (İhrama girmek, Arafat'ta vakfe yapmak, Kâbe'yi ziyaret tavafı yapmak) ve hac-umre farkları.",
                "arabic_text": "",
                "question_text": "Hac ibadetinin üç farzını yazarak; hac ile umre ibadeti arasındaki temel farkları (zaman, hükmü ve uygulanış farkı açısından) karşılaştırınız.",
                "options": [
                    "A) Haccın farzları: İhram, Arafat vakfesi ve Ziyaret tavafıdır. Hac farzdır ve yılda bir kez belirli günlerde (Arafat/Kurban ile) yapılır; Umre ise sünnettir ve yılın her vaktinde yapılabilir.",
                    "B) Hac ve umre tamamen aynıdır.",
                    "C) Umrede de Arafat vakfesi ve kurban kesimi vardır.",
                    "D) Tavaf sadece Safa ile Merve arasında yürümektir."
                ],
                "answer_text": "Haccın Farzları (3): 1) İhrama girmek, 2) Arafat'ta vakfe yapmak, 3) Kâbe'yi ziyaret tavafı yapmak. Hac ile Umre Farkı: Hac zenginlere farzdır ve yılda bir kez Zilhicce ayında (Arafat vakfesi, Müzdelife, şeytan taşlama ve kurban ile) yapılır. Umre ise sünnettir, vakfe ve şeytan taşlama olmadan yılın diğer zamanlarında ihram + tavaf + sa'y ile yapılır.",
                "rubric": [
                    {"criterion": "Haccın üç farzının (İhram, Arafat vakfesi, Ziyaret tavafı) doğru yazılması", "points": 5},
                    {"criterion": "Hac ve umre arasındaki hüküm, vakit ve uygulama farkının açıklanması", "points": 5}
                ]
            },
            {
                "unit_no": 3,
                "learning_outcome": "[DKAB.7.3.1] Güzel ahlaki tutum ve davranışları (Adalet, Dürüstlük, Özdenetim, Dostluk, Sabır) örneklerle açıklar.",
                "cognitive_level": "Değerlendirme",
                "difficulty": "Orta",
                "source_page": "Sayfa 92-120",
                "source_context": "İslam ahlakında adalet, dürüstlük, özdenetim (irade kontrolü), yardımseverlik ve vatanseverlik değerleri.",
                "arabic_text": "",
                "question_text": "Bir öğrencinin sınavda gözetmen öğretmen sınıfta olmasa bile kopya çekmemesi ve ödevlerini zamanında kendi emeğiyle yapması hangi iki ahlaki erdemin (değerin) göstergesidir? Bu erdemlerin bireye ve topluma kazandırdıklarını açıklayınız.",
                "options": [
                    "A) Özdenetim (otokontrol) ve Dürüstlük (doğruluk) erdemlerini gösterir; bireye güvenilirlik, topluma ise adalet ve huzur kazandırır.",
                    "B) Sadece korku ve çekingenlik göstergesidir.",
                    "C) Yalnızca yüksek not alma isteğidir.",
                    "D) Arkadaşlarıyla yardımlaşmadığını gösterir."
                ],
                "answer_text": "Bu davranış kişinin kendi kendini denetlemesi olan ÖZDENETİM ve hakikatten ayrılmaması olan DÜRÜSTLÜK (ve kul hakkına saygı) erdemlerini gösterir. Özdenetimli ve dürüst bireyler toplumda güveni, adaleti ve hakkaniyeti tesis eder.",
                "rubric": [
                    {"criterion": "Özdenetim ve dürüstlük kavramlarının doğru tespit edilmesi", "points": 5},
                    {"criterion": "Güven ve kul hakkı açısından toplumsal öneminin açıklanması", "points": 5}
                ]
            }
        ],
        8: [
            {
                "unit_no": 1,
                "learning_outcome": "[DKAB.8.1.2] İnsanın cüz'i iradesi, külli irade ve sorumluluk arasındaki ilişkiyi analiz eder.",
                "cognitive_level": "Analiz",
                "difficulty": "Orta",
                "source_page": "Sayfa 18-26",
                "source_context": "Külli irade Allah'ın sınırsız iradesidir; cüz'i irade ise insana verilen seçme özgürlüğüdür ve sorumluluğun temelidir.",
                "arabic_text": "إِنَّا هَدَيْنَاهُ السَّبِيلَ إِمَّا شَاكِرًا وَإِمَّا كَفُورًا",
                "question_text": "'Şüphesiz biz ona (insana) doğru yolu gösterdik; ister şükredici olsun ister nankör.' (İnsan, 3) ayetini 'Külli İrade', 'Cüz'i İrade' ve 'İnsanın Sorumluluğu' kavramları çerçevesinde analiz ediniz.",
                "options": [
                    "A) Allah külli iradesiyle insana akıl ve seçme özgürlüğü (cüz'i irade) vermiş, peygamberlerle doğru yolu göstermiştir; insan kendi seçimiyle yaptığı davranışlardan sorumludur.",
                    "B) İnsan hiçbir seçim yapamaz, her davranış zorunludur.",
                    "C) Külli irade insana, cüz'i irade Allah'a aittir.",
                    "D) İnsan yaptığı kötülüklerden sorumlu tutulmaz."
                ],
                "answer_text": "Yüce Allah Külli İradesi (sınırsız iradesi) ile insana iyi ve kötüyü ayırt edebileceği akıl ve Cüz'i İrade (seçme özgürlüğü) vermiş, kitap ve peygamberlerle doğru yolu göstermiştir. İnsan özgür iradesiyle yaptığı tercihlerden dolayı dünyada ve ahirette sorumludur.",
                "rubric": [
                    {"criterion": "Külli irade ve cüz'i irade kavramlarının doğru tanımlanması", "points": 5},
                    {"criterion": "Seçme özgürlüğü ile sorumluluk arasındaki ilişkinin ayetle açıklanması", "points": 5}
                ]
            },
            {
                "unit_no": 1,
                "learning_outcome": "[DKAB.8.1.6] Ayet el-Kürsi'yi okur ve içerdiği tevhid/kudret mesajlarını yorumlar.",
                "cognitive_level": "Yorumlama",
                "difficulty": "Orta",
                "source_page": "Sayfa 35-39",
                "source_context": "Bakara Suresi 255. ayet (Ayet el-Kürsi) Allah'ın Hayy, Kayyum, Aliyy ve Azim sıfatlarını ve eşsiz kudretini anlatır.",
                "arabic_text": "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ",
                "question_text": "Bakara Suresi 255. ayet olan Ayet el-Kürsi'de geçen 'el-Hayy' ve 'el-Kayyûm' isimlerinin anlamlarını yazarak, ayette Yüce Allah'ın ilmi ve kudreti hakkında verilen mesajlardan 3 tanesini belirtiniz.",
                "options": [
                    "A) el-Hayy: Daima diri ve hayat sahibi; el-Kayyûm: Her şeyi ayakta tutan ve yönetendir. O'nu uyuklama ve uyku tutmaz, göklerde ve yerde ne varsa O'nundur, ilmi her şeyi kuşatmıştır.",
                    "B) Ayet el-Kürsi sadece oruç ibadetini anlatır.",
                    "C) el-Hayy rızık veren, el-Kayyûm affeden demektir.",
                    "D) Ayet el-Kürsi İhlas Suresi'nin bir ayetidir."
                ],
                "answer_text": "el-Hayy: Daima diri olan, hayatın kaynağı olan; el-Kayyûm: Evreni kendi kudretiyle ayakta tutan ve yönetendir. Mesajları: 1) Allah'tan başka ilah yoktur (Tevhid), 2) O'nu ne uyuklama ne de uyku tutar, 3) Göklerde ve yerde olan her şey O'nundur ve izni olmadan kimse şefaat edemez.",
                "rubric": [
                    {"criterion": "el-Hayy ve el-Kayyûm sıfatlarının doğru açıklanması", "points": 5},
                    {"criterion": "Ayet el-Kürsi'deki tevhid, ilim ve kudret mesajlarından en az üçünün yazılması", "points": 5}
                ]
            },
            {
                "unit_no": 2,
                "learning_outcome": "[DKAB.8.2.2] Zekâtın nisap miktarını, verileceği malları/oranları ve kimlere verileceğini (Tevbe 60) açıklar.",
                "cognitive_level": "Uygulama",
                "difficulty": "Zor",
                "source_page": "Sayfa 46-58",
                "source_context": "Nisap miktarı (85 gr altın vb.), zekât oranları (1/40, 1/10, 1/20, 1/30) ve Tevbe Suresi 60. ayetteki 8 sınıf.",
                "arabic_text": "",
                "question_text": "Zekât ibadetinde 'Nisap Miktarı' ne demektir? Altın, nakit para ve ticaret mallarında zekât oranı kaçtır ve İslam'a göre bir kimse yakın akrabalarından hangilerine zekât VEREMEZ? Açıklayınız.",
                "options": [
                    "A) Nisap, temel ihtiyaçlar dışında dinen zenginlik ölçüsüdür (85 gr altın). Altın/para/ticaret malında oran 1/40 (%2,5)'tir. Anne, baba, dede, nine, eş, çocuklar ve torunlara zekât verilmez.",
                    "B) Altında zekât oranı 1/10'dur ve anne-babaya zekât verilebilir.",
                    "C) Nisap miktarı 10 gram altındır.",
                    "D) Sadece tarım ürünlerinden zekât verilir."
                ],
                "answer_text": "Nisap: Temel ihtiyaçlar ve borçlar dışında dinen belirlenen asgari zenginlik ölçüsüdür (altında 85 gram). Altın, gümüş, nakit para ve ticaret mallarında zekât oranı 1/40 (%2,5) kadardır. Kişi bakmakla yükümlü olduğu usul (anne, baba, dede, nine), füru (çocuklar, torunlar) ve eşine zekât veremez.",
                "rubric": [
                    {"criterion": "Nisap kavramının ve altın/para zekât oranının (1/40 veya %2,5) doğru yazılması", "points": 5},
                    {"criterion": "Zekât verilemeyecek yakın akrabaların (anne-baba, dede-nine, çocuklar, torunlar, eş) belirtilmesi", "points": 5}
                ]
            }
        ]
    },
    "kuran": {
        5: [
            {
                "unit_no": 1,
                "learning_outcome": "[KURAN.5.1.1] Vahiy kavramını, Kur'an-ı Kerim'in indiriliş sürecini ve temel özelliklerini açıklar.",
                "cognitive_level": "Kavrama",
                "difficulty": "Kolay",
                "source_page": "Sayfa 12-24",
                "source_context": "610 yılı Ramazan ayı Kadir Gecesi'nde Hira Mağarası'nda Alak Suresi ilk 5 ayetle başlayan 23 yıllık vahiy süreci.",
                "arabic_text": "اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ",
                "question_text": "Kur'an-ı Kerim hangi yılda, hangi gecede, nerede ve hangi surenin ilk ayetleriyle indirilmeye başlanmıştır? Kur'an-ı Kerim'in parça parça (23 yılda) indirilmesinin hikmetini açıklayınız.",
                "options": [
                    "A) 610 yılı Ramazan ayı Kadir Gecesi'nde, Hira Mağarası'nda Alak Suresi'nin ilk 5 ayetiyle başlamıştır; kolay ezberlenmesi ve hükümlerin hayata aşama aşama uygulanması için 23 yılda indirilmiştir.",
                    "B) Medine'de Bakara Suresi ile bir defada indirilmiştir.",
                    "C) 571 yılında Kâbe'de indirilmiştir.",
                    "D) Sadece 1 yılda tamamlanmıştır."
                ],
                "answer_text": "Kur'an-ı Kerim 610 yılı Ramazan ayının Kadir Gecesi'nde, Mekke'deki Nur Dağı Hira Mağarası'nda Alak Suresi'nin ilk 5 ayeti ('Oku!') ile indirilmeye başlanmıştır. İnsanların ayetleri kolayca öğrenip ezberlemesi ve İslam hükümlerini hayatlarına sindirerek uygulaması için 23 yılda aşama aşama indirilmiştir.",
                "rubric": [
                    {"criterion": "610 yılı, Kadir Gecesi, Hira Mağarası ve Alak Suresi bilgilerinin doğru yazılması", "points": 6},
                    {"criterion": "23 yılda parça parça indirilmesinin hikmetinin (kolay ezberleme ve uygulama) açıklanması", "points": 4}
                ]
            },
            {
                "unit_no": 1,
                "learning_outcome": "[KURAN.5.1.2] Ayet, sure, cüz ve mushaf kavramlarını tanımlayarak özelliklerini yazar.",
                "cognitive_level": "Analiz",
                "difficulty": "Kolay",
                "source_page": "Sayfa 25-36",
                "source_context": "Kur'an'ın iç düzeni: 6666 (6236) ayet, 114 sure, 30 cüz; ilk sure Fatiha, son sure Nas, en uzun Bakara, en kısa Kevser.",
                "arabic_text": "",
                "question_text": "Kur'an-ı Kerim'in iç düzeniyle ilgili 'Ayet', 'Sure' ve 'Cüz' kavramlarını tanımlayınız. Kur'an'da kaç sure ve kaç cüz bulunduğunu, en uzun ve en kısa surelerin isimlerini yazınız.",
                "options": [
                    "A) Ayet: Duraklarla ayrılan cümleler; Sure: Ayetlerden oluşan bölümler (114 sure); Cüz: 20 sayfalık bölümlerdir (30 cüz). En uzun sure Bakara, en kısa sure Kevser'dir.",
                    "B) Kur'an'da 30 sure ve 114 cüz vardır.",
                    "C) En kısa sure Fatiha, en uzun sure İhlas'tır.",
                    "D) Cüz 100 sayfadan oluşur."
                ],
                "answer_text": "Ayet: Kur'an'ın durak işaretleriyle ayrılan her bir cümlesidir. Sure: Ayetlerden oluşan bağımsız bölümlerdir (Toplam 114 sure vardır). Cüz: Her biri 20 sayfadan oluşan bölümlerdir (Toplam 30 cüz vardır). En uzun sure Bakara (286 ayet), en kısa sure Kevser (3 ayet) suresidir.",
                "rubric": [
                    {"criterion": "Ayet, sure ve cüz kavramlarının doğru tanımlanması", "points": 5},
                    {"criterion": "114 sure, 30 cüz ile Bakara ve Kevser surelerinin doğru belirtilmesi", "points": 5}
                ]
            },
            {
                "unit_no": 2,
                "learning_outcome": "[KURAN.5.2.3] Harekeleri, cezm (sükun), şedde ve tenvin işaretlerini işlevleriyle ayırt eder.",
                "cognitive_level": "Uygulama",
                "difficulty": "Orta",
                "source_page": "Sayfa 50-85",
                "source_context": "Harfleri seslendiren harekeler (üstün, esre, ötre), tenvin (iki üstün -en/-an, iki esre -in/-ın, iki ötre -ün/-un), cezm ve şedde.",
                "arabic_text": "رَبٍّ  —  مِنْ  —  كِتَابًا",
                "question_text": "Kur'an-ı Kerim okurken kullanılan 'Cezm (Sükûn)', 'Şedde' ve 'Tenvin' işaretlerinin harfleri nasıl okuttuğunu yukarıdaki Arapça örneklerle ilişkilendirerek açıklayınız.",
                "options": [
                    "A) Cezm (مِنْ) harfi harekesiz/sakin okutur; Şedde (رَبٍّ) harfi iki kez vurgulu okutur; Tenvin (كِتَابًا) kelime sonuna '-en/-an, -in/-ın, -ün/-un' şeklinde sakin nun sesi katar.",
                    "B) Cezm harfi uzatır, şedde harfi okutmaz.",
                    "C) Tenvin sadece kelime başında bulunur.",
                    "D) Şedde harfi ince okutur."
                ],
                "answer_text": "1) Cezm (مِنْ): Üzerinde bulunduğu harfi harekesiz (sesli harf olmadan) kendinden önceki harfe bağlayarak okutur. 2) Şedde (رَبٍّ): Üzerinde bulunduğu harfi önce cezimli, sonra harekeli olmak üzere iki kere (vurgulu) okutur. 3) Tenvin (كِتَابًا): İki üstün, iki esre ve iki ötre olup kelime sonuna '-an/-en, -ın/-in, -un/-ün' sesi verir.",
                "rubric": [
                    {"criterion": "Cezm ve Şedde işaretlerinin okunuş işlevinin doğru açıklanması", "points": 5},
                    {"criterion": "Tenvin işaretinin çeşitleri ve verdiği sesin açıklanması", "points": 5}
                ]
            }
        ],
        6: [
            {
                "unit_no": 2,
                "learning_outcome": "[KURAN.6.1.2] Harf-i medleri (Elif, Vav, Ya) ve Medd-i Tabiî kuralını örneklerle açıklar.",
                "cognitive_level": "Uygulama",
                "difficulty": "Kolay",
                "source_page": "Sayfa 46-60",
                "source_context": "Uzatma (Med) harfleri olan Elif (ا), Vav (و) ve Ya (ي) harflerinin harekesiz gelip kendinden önceki harfi bir elif miktarı uzatması.",
                "arabic_text": "قَالَ  —  يَقُولُ  —  قِيلَ",
                "question_text": "Kur'an-ı Kerim tecvidinde uzatma (harf-i med) harfleri hangileridir? Verilen 'قَالَ — يَقُولُ — قِيلَ' kelimelerinde Medd-i Tabiî kuralının nasıl oluştuğunu ve kaç elif miktarı uzatıldığını açıklayınız.",
                "options": [
                    "A) Med harfleri Elif (ا), Vav (و) ve Ya (ي)'dır. Sebeb-i med (hemze veya sükun) bulunmadığı için her üç kelimede de Medd-i Tabiî vardır ve 1 elif miktarı uzatılır.",
                    "B) Med harfleri Be, Te ve Se'dir; 4 elif miktarı uzatılır.",
                    "C) Bu kelimelerde uzatma yapılmaz.",
                    "D) Hepsinde İklab kuralı vardır."
                ],
                "answer_text": "Med harfleri 3 tanedir: Elif (ا), Vav (و) ve Ya (ي). 'قَالَ' kelimesinde üstünden sonra harekesiz Elif; 'يَقُولُ' kelimesinde ötreden sonra sakin Vav; 'قِيلَ' kelimesinde esreden sonra sakin Ya gelmiştir. Sonrasında hemze veya sükun olmadığı için Medd-i Tabiî olur ve 1 elif miktarı uzatılır.",
                "rubric": [
                    {"criterion": "Üç med harfinin (Elif, Vav, Ya) ve hareke şartlarının doğru yazılması", "points": 5},
                    {"criterion": "Medd-i Tabiî kuralının ve 1 elif miktarı uzatıldığının belirtilmesi", "points": 5}
                ]
            },
            {
                "unit_no": 4,
                "learning_outcome": "[KURAN.6.4.1] Hz. İbrahim, Hz. Zekeriya ve Hz. Yahya kıssalarından tevhid ve dua dersleri çıkarır.",
                "cognitive_level": "Yorumlama",
                "difficulty": "Orta",
                "source_page": "Sayfa 145-168",
                "source_context": "Kur'an kıssalarında peygamberlerin tevhid mücadelesi, ümitsizliğe kapılmadan Allah'a dua etmeleri ve güzel ahlakları.",
                "arabic_text": "",
                "question_text": "Kur'an-ı Kerim'de anlatılan Hz. İbrahim'in (a.s.) yıldızlara, Ay'a ve Güneş'e bakarak kavmine Tevhid dersini vermesi ile Hz. Zekeriya'nın (a.s.) ilerlemiş yaşına rağmen ümidini kaybetmeyip Allah'a dua etmesi bize hangi mesajları vermektedir?",
                "options": [
                    "A) Aklımızı kullanarak geçici varlıkların ilah olamayacağını (Tevhid'i) kavramamız ve her şartta ümidimizi koruyarak yalnızca Allah'a dua etmemiz gerektiğini öğretir.",
                    "B) Gökyüzü cisimlerinin kutsal olduğunu gösterir.",
                    "C) Yaşlılıkta dua edilmemesi gerektiğini ifade eder.",
                    "D) Kıssaların sadece geçmiş zamana ait hikayeler olduğunu gösterir."
                ],
                "answer_text": "Hz. İbrahim kıssası, insanın aklını ve tefekkürünü kullanarak batıp giden varlıkların yaratıcı olamayacağını, yalnız Allah'a ibadet edilmesi gerektiğini öğretir. Hz. Zekeriya kıssası ise şartlar ne kadar zor olursa olsun Allah'ın rahmetinden ümit kesmeden samimiyetle dua etmemiz gerektiğini gösterir.",
                "rubric": [
                    {"criterion": "Hz. İbrahim kıssasındaki akıl yürütme ve Tevhid mesajının açıklanması", "points": 5},
                    {"criterion": "Hz. Zekeriya kıssasındaki ümitvar olma ve samimi dua bilincinin yazılması", "points": 5}
                ]
            }
        ],
        7: [
            {
                "unit_no": 2,
                "learning_outcome": "[KURAN.7.1.2] İhfa ve İzhar kurallarını harfleriyle ayırt ederek metin üzerinde gösterir.",
                "cognitive_level": "Uygulama",
                "difficulty": "Orta",
                "source_page": "Sayfa 52-74",
                "source_context": "Sakin nun veya tenvinden sonra 6 boğaz harfi (أ ه ع ح غ خ) gelirse İzhar; 15 ihfa harfi gelirse genizden gunneli İhfa yapılır.",
                "arabic_text": "مِنْ خَوْفٍ  —  أَنْفُسَهُمْ  —  عَلِيمٌ حَكِيمٌ",
                "question_text": "Verilen 'مِنْ خَوْفٍ — أَنْفُسَهُمْ — عَلِيمٌ حَكِيمٌ' örneklerinde sakin nun ve tenvinden sonra gelen harflere göre hangi tecvid kurallarının (İzhar / İhfa) oluştuğunu gerekçeleriyle açıklayınız.",
                "options": [
                    "A) مِنْ خَوْفٍ (خ harfi) ve عَلِيمٌ حَكِيمٌ (ح harfi): Boğaz harfleri geldiği için İZHAR; أَنْفُسَهُمْ (ف harfi): İhfa harfi geldiği için İHFA olur.",
                    "B) Hepsinde İhfa kuralı vardır.",
                    "C) مِنْ خَوْفٍ: İhfa, أَنْفُسَهُمْ: İzhar'dır.",
                    "D) Hepsinde İdgam vardır."
                ],
                "answer_text": "1) 'مِنْ خَوْفٍ' (خ) ve 'عَلِيمٌ حَكِيمٌ' (ح) ifadelerinde sakin nun ve tenvinden sonra 6 boğaz harfinden (أ ه ع ح غ خ) biri geldiği için İZHAR olur, ses tutulmadan açık okunur. 2) 'أَنْفُسَهُمْ' kelimesinde ise sakin nundan sonra ف (ihfa harfi) geldiği için İHFA olur, ses genizden gunneli olarak gizlenir.",
                "rubric": [
                    {"criterion": "İzhar örneklerinin ve boğaz harfleri gerekçesinin doğru yazılması", "points": 5},
                    {"criterion": "أَنْفُسَهُمْ örneğinde İhfa kuralının ve okunuşunun doğru açıklanması", "points": 5}
                ]
            },
            {
                "unit_no": 4,
                "learning_outcome": "[KURAN.7.4.1] Ashab-ı Kehf kıssasından ve Rabbena dualarından inanç/ahlak dersleri çıkarır.",
                "cognitive_level": "Değerlendirme",
                "difficulty": "Orta",
                "source_page": "Sayfa 148-172",
                "source_context": "Kehf Suresi'nde anlatılan gençlerin (Ashab-ı Kehf) tevhid inancını koruma kararlılığı ve Rabbena dualarının anlamı.",
                "arabic_text": "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً",
                "question_text": "Kur'an-ı Kerim'de Kehf Suresi'nde anlatılan 'Ashab-ı Kehf' (Mağara Arkadaşları) kıssasındaki gençlerin inançlarını korumak için gösterdiği fedakârlığı ve Bakara Suresi 201. ayetteki 'Rabbena Âtinâ' duasının anlamını açıklayınız.",
                "options": [
                    "A) Ashab-ı Kehf putperest baskısına karşı Tevhid inancından taviz vermeyen imanlı gençlerin sembolüdür; Rabbena Âtinâ duasıyla hem dünyada hem ahirette iyilik ve güzellik istenir.",
                    "B) Ashab-ı Kehf ticaret için yolculuk yapan kervandır.",
                    "C) Rabbena duası sadece dünya zenginliği istemektir.",
                    "D) Kıssada sadece coğrafi bilgiler anlatılır."
                ],
                "answer_text": "Ashab-ı Kehf, yaşadıkları toplumun putperestlik baskısına boyun eğmeyip Tevhid inançlarını korumak için mağaraya sığınan ve Allah'ın mucizesiyle korunan imanlı gençlerdir. 'Rabbena Âtinâ' duasında ise: 'Rabbimiz! Bize dünyada da iyilik ve güzellik ver, ahirette de iyilik ver ve bizi ateş azabından koru' diye dua edilir.",
                "rubric": [
                    {"criterion": "Ashab-ı Kehf kıssasının Tevhid ve inançta kararlılık mesajının açıklanması", "points": 5},
                    {"criterion": "Rabbena Âtinâ duasının dünya-ahiret dengesi ve anlamının yazılması", "points": 5}
                ]
            }
        ],
        8: [
            {
                "unit_no": 3,
                "learning_outcome": "[KURAN.8.3.2] Ra (ر) harfinin kalın (tefhim) ve ince (terkik) okunduğu durumları ayırt eder.",
                "cognitive_level": "Analiz",
                "difficulty": "Zor",
                "source_page": "Sayfa 55-68",
                "source_context": "Hükmü'r-Ra: Ra harfinin harekesine veya sakin olduğunda kendinden önceki harfin harekesine göre kalın veya ince okunması.",
                "arabic_text": "رَبَّنَا  —  رِزْقًا  —  فِرْعَوْنَ  —  مَرْيَمَ",
                "question_text": "Tecvid ilminde Ra (ر) harfinin okunuşuyla ilgili (Hükmü'r-Ra); yukarıda verilen dört kelimenin hangilerinde Ra harfi KALIN, hangilerinde İNCE okunur? Sebepleriyle açıklayınız.",
                "options": [
                    "A) رَبَّنَا (üstünlü) ve مَرْيَمَ (sakin, öncesi üstünlü) kelimelerinde KALIN; رِزْقًا (esreli) ve فِرْعَوْنَ (sakin, öncesi esreli) kelimelerinde İNCE okunur.",
                    "B) Dördünde de Ra harfi kalın okunur.",
                    "C) رَبَّنَا ve مَرْيَمَ ince, diğerleri kalın okunur.",
                    "D) Ra harfi her zaman ince okunur."
                ],
                "answer_text": "Ra harfi üstün veya ötreli olduğunda (veya sakin olup önceki harf üstün/ötreli olduğunda) KALIN; esreli olduğunda (veya sakin olup önceki harf asli esreli olduğunda) İNCE okunur. Buna göre 'رَبَّنَا' ve 'مَرْيَمَ' kelimelerinde KALIN; 'رِزْقًا' ve 'فِرْعَوْنَ' kelimelerinde İNCE okunur.",
                "rubric": [
                    {"criterion": "Hükmü'r-Ra (kalın ve ince okunma) kuralının doğru açıklanması", "points": 5},
                    {"criterion": "Dört örnek kelimenin doğru gruplandırılması", "points": 5}
                ]
            },
            {
                "unit_no": 4,
                "learning_outcome": "[KURAN.8.4.1] Hucurat suresindeki ahlaki ilkeleri (suizan, tecessüs, gıybet, alay etmeme) analiz eder.",
                "cognitive_level": "Değerlendirme",
                "difficulty": "Orta",
                "source_page": "Sayfa 88-108",
                "source_context": "Hucurat Suresi 10-12. ayetlerde müminlerin kardeş olduğu bildirilir ve toplumsal barışı bozan suizan, tecessüs ve gıybet yasaklanır.",
                "arabic_text": "يَا أَيُّهَا الَّذِينَ آمَنُوا اجْتَنِبُوا كَثِيرًا مِّنَ الظَّنِّ",
                "question_text": "Hucurât Suresi 11 ve 12. ayetlerde müminler arasındaki kardeşliği korumak için kesin olarak yasaklanan 'Suizan', 'Tecessüs' ve 'Gıybet' kavramlarının anlamlarını açıklayarak, bu yasakların toplumsal huzura katkısını değerlendiriniz.",
                "options": [
                    "A) Suizan: Kötü zan ve önyargı; Tecessüs: İnsanların gizli kusurlarını araştırmak; Gıybet: Birinin arkasından hoşlanmayacağı şekilde konuşmaktır. Bunlardan kaçınmak güven ve kardeşliği korur.",
                    "B) Bu kavramlar ticaret kurallarıyla ilgilidir.",
                    "C) Suizan güzel düşünmek, gıybet yüzüne karşı övmektir.",
                    "D) Tecessüs yardımlaşmak demektir."
                ],
                "answer_text": "1) Suizan: Bir kimse hakkında kesin bilgi olmadan kötü düşünmek ve önyargılı olmaktır. 2) Tecessüs: İnsanların özel hayatını ve gizli kusurlarını araştırmaktır. 3) Gıybet: Bir insanın arkasından duyduğunda üzüleceği kusurlarını konuşmaktır (dedikodu). Bu üç davranıştan uzak durmak toplumda güven, saygı ve kardeşliği korur.",
                "rubric": [
                    {"criterion": "Suizan, tecessüs ve gıybet kavramlarının doğru tanımlanması", "points": 6},
                    {"criterion": "Toplumsal güven ve kardeşliği koruma boyutunun değerlendirilmesi", "points": 4}
                ]
            }
        ]
    },
    "siyer": {
        5: [
            {
                "unit_no": 1,
                "learning_outcome": "[SIYER.5.1.1] İslam öncesi Arap Yarımadası'nın (Cahiliye Dönemi) dini ve sosyal durumunu açıklar.",
                "cognitive_level": "Analiz",
                "difficulty": "Kolay",
                "source_page": "Sayfa 12-22",
                "source_context": "İslam öncesi Mekke'de putperestlik, kabile savaşları, güçlülerin zayıfları ezmesi (Cahiliye) ve Hz. İbrahim'den kalan Haniflik inancı.",
                "arabic_text": "",
                "question_text": "Peygamber Efendimizin (s.a.v.) dünyaya geldiği dönemdeki Arap toplumuna neden 'Cahiliye Dönemi' denilmiştir? O dönemde Hz. İbrahim'in tevhid inancını sürdüren kimselere ne ad verildiğini belirterek açıklayınız.",
                "options": [
                    "A) Putperestlik, kan davaları, kadınlara ve zayıflara yapılan haksızlıklar sebebiyle Cahiliye denmiştir; Hz. İbrahim'in tevhid inancını koruyanlara ise 'Hanif' denir.",
                    "B) Okuma-yazma hiç bilinmediği için Cahiliye denmiştir.",
                    "C) O dönemde herkes barış ve adalet içinde yaşıyordu.",
                    "D) Tevhid inancını sürdürenlere Müşrik denir."
                ],
                "answer_text": "İslam öncesi dönemde insanlar Allah'ı bırakıp putlara taptıkları, kabile savaşları (kan davaları) güttükleri, kadınlara, kölelere ve zayıflara zulmettikleri için bu döneme ahlaki bilgisizlik anlamında 'Cahiliye Dönemi' denmiştir. Putlara tapmayıp Hz. İbrahim'in (a.s.) getirdiği Tevhid dinine bağlı kalanlara ise 'Hanif' denilmiştir.",
                "rubric": [
                    {"criterion": "Cahiliye kavramının dini ve toplumsal haksızlıklarla açıklanması", "points": 6},
                    {"criterion": "Hanif kavramının (Hz. İbrahim'in tevhid inancını sürdürenler) doğru belirtilmesi", "points": 4}
                ]
            },
            {
                "unit_no": 1,
                "learning_outcome": "[SIYER.5.1.2] Peygamberimizin ailesini, sütanneye veriliş sürecini ve çocukluk yıllarını açıklar.",
                "cognitive_level": "Kavrama",
                "difficulty": "Kolay",
                "source_page": "Sayfa 23-42",
                "source_context": "Hz. Muhammed'in (s.a.v.) annesi Hz. Âmine, babası Abdullah, sütannesi Halime, dedesi Abdülmuttalib ve amcası Ebu Talib.",
                "arabic_text": "",
                "question_text": "Peygamber Efendimizin (s.a.v.) bebekliğinde sütanne Hz. Halime'nin yanına (Beni Sa'd yurduna) verilmesinin sebepleri nelerdir? Annesi ve dedesinin vefatından sonra O'na hangi aile büyüğü sevgiyle sahip çıkmıştır?",
                "options": [
                    "A) Mekke'nin sıcak havasından korunup sağlam bir bünyeyle büyümesi ve fasih (düzgün) Arapçayı öğrenmesi için verilmiştir; dedesinden sonra amcası Ebu Talib himaye etmiştir.",
                    "B) Ticaret öğrenmesi için Şam'a gönderilmiştir.",
                    "C) Dedesinden sonra Ebu Leheb himaye etmiştir.",
                    "D) Sadece seyahat amacıyla gönderilmiştir."
                ],
                "answer_text": "Mekke'nin havası çok sıcak ve salgın hastalıklara açık olduğu için bebeklerin temiz yayla havasında sağlıklı büyümesi ve fasih (duru/güzel) Arapçayı öğrenmesi amacıyla sütanneye verilmiştir. 6 yaşında annesi Hz. Âmine, 8 yaşında dedesi Abdülmuttalib vefat edince O'nu amcası Ebu Talib kendi evladı gibi koruyup büyütmüştür.",
                "rubric": [
                    {"criterion": "Sütanneye verilme sebeplerinin (sağlıklı büyüme ve fasih Arapça öğrenme) yazılması", "points": 5},
                    {"criterion": "Hz. Âmine, Abdülmuttalib ve amcası Ebu Talib'in himaye sürecinin doğru belirtilmesi", "points": 5}
                ]
            }
        ],
        6: [
            {
                "unit_no": 1,
                "learning_outcome": "[SIYER.6.1.2] Hira Mağarası'ndaki ilk vahiy sürecini ve ilk Müslümanların fedakârlıklarını özetler.",
                "cognitive_level": "Analiz",
                "difficulty": "Kolay",
                "source_page": "Sayfa 18-38",
                "source_context": "Hira'da ilk vahiy sonrası Hz. Hatice'nin tesellisi, Varaka b. Nevfel ve ilk Müslümanlar (Hz. Hatice, Hz. Ali, Hz. Zeyd, Hz. Ebu Bekir).",
                "arabic_text": "",
                "question_text": "Hira Mağarası'nda ilk vahyi aldıktan sonra heyecanla evine dönen Peygamber Efendimizi eşi Hz. Hatice hangi sözlerle teselli etmiştir? İslam davetini ilk kabul eden 4 öncü sahabenin (İlk Müslümanların) isimlerini yazınız.",
                "options": [
                    "A) 'Allah seni asla utandırmaz; çünkü sen akrabayı gözetir, doğru konuşur, misafiri ağırlar ve mazlumlara yardım edersin' diyerek teselli etmiştir. İlk Müslümanlar: Hz. Hatice, Hz. Ali, Hz. Zeyd b. Harise ve Hz. Ebu Bekir'dir.",
                    "B) İlk Müslümanlar Medineli Ensar'dır.",
                    "C) İlk vahiy Medine'de gelmiştir.",
                    "D) Hz. Hatice bu durumu kimseye anlatmamasını söylemiştir."
                ],
                "answer_text": "Hz. Hatice validemiz: 'Korkma! Allah seni asla mahcup etmez. Çünkü sen akrabanı gözetirsin, doğru söylersin, güçsüzlerin yükünü taşırsın ve misafire ikram edersin' diyerek Efendimize en büyük desteği vermiştir. İlk Müslümanlar: 1) Hz. Hatice, 2) Hz. Ali, 3) Hz. Zeyd b. Harise, 4) Hz. Ebu Bekir'dir.",
                "rubric": [
                    {"criterion": "Hz. Hatice'nin teselli sözlerindeki ahlaki vurguların yazılması", "points": 5},
                    {"criterion": "İlk dört Müslümanın (Hz. Hatice, Hz. Ali, Hz. Zeyd, Hz. Ebu Bekir) eksiksiz belirtilmesi", "points": 5}
                ]
            },
            {
                "unit_no": 3,
                "learning_outcome": "[SIYER.6.3.1] Akabe Biatlarını ve Medine'ye Hicret yolculuğunun İslam tarihi açısından önemini değerlendirir.",
                "cognitive_level": "Değerlendirme",
                "difficulty": "Orta",
                "source_page": "Sayfa 88-120",
                "source_context": "1. ve 2. Akabe Biatları, Hz. Ebu Bekir ile Sevr Mağarası, Kuba Mescidi ve Hicret'in sonuçları.",
                "arabic_text": "لَا تَحْزَنْ إِنَّ اللَّهَ مَعَنَا",
                "question_text": "Medine'ye hicret yolculuğu sırasında Sevr Mağarası'nda Hz. Ebu Bekir endişelendiğinde Peygamber Efendimizin söylediği 'Üzülme! Şüphesiz Allah bizimledir' (Tevbe, 40) sözü hangi inancı gösterir? Hicret'in İslam tarihi açısından 2 önemli sonucunu yazınız.",
                "options": [
                    "A) Tam bir tevekkül ve Allah'a güven bilincini gösterir; Hicret ile Müslümanlar baskıdan kurtulup Medine'de İslam devletinin temellerini atmış ve Hicri takvimin başlangıcı olmuştur.",
                    "B) Hicret sadece ticari bir yolculuktur.",
                    "C) Hicret sonrasında İslam'ın yayılışı durmuştur.",
                    "D) Sevr Mağarası Şam yolundadır."
                ],
                "answer_text": "Bu söz, tüm tedbirleri aldıktan sonra Allah'a tam bir teslimiyet ve tevekkül bilincini gösterir. Hicret'in sonuçları: 1) Müslümanlar Mekke'deki baskıdan kurtulup dinlerini özgürce yaşayacakları bir yurda kavuştular. 2) Medine'de Mescid-i Nebevî, kardeşlik hukuku ve İslam şehir devletinin temelleri atıldı.",
                "rubric": [
                    {"criterion": "Sevr Mağarası'ndaki tedbir ve tevekkül bilincinin açıklanması", "points": 5},
                    {"criterion": "Hicret'in İslam tarihi açısından en az iki sonucunun yazılması", "points": 5}
                ]
            }
        ],
        7: [
            {
                "unit_no": 1,
                "learning_outcome": "[SIYER.7.1.2] Uhud Savaşı'nda Okçular Tepesi olayından çıkarılması gereken dersleri analiz eder.",
                "cognitive_level": "Analiz",
                "difficulty": "Orta",
                "source_page": "Sayfa 24-38",
                "source_context": "Uhud Savaşı öncesi istişare ve Ayneyn (Okçular) Tepesi'ne yerleştirilen okçuların Peygamberimizin emrine itaatinin önemi.",
                "arabic_text": "",
                "question_text": "Uhud Savaşı'nda başlangıçta İslam ordusu üstünlük sağlamışken, Ayneyn (Okçular) Tepesi'ndeki okçuların büyük kısmının yerlerini terk etmesi savaşın seyrini nasıl değiştirmiştir? Bu olaydan günümüz Müslümanlarının çıkarması gereken 2 temel dersi yazınız.",
                "options": [
                    "A) İslam ordusu arkadan kuşatılarak ağır kayıplar vermiştir; bu olay Hz. Peygamber'in emirlerine itaatin, görev bilincinin ve dünyevi çıkarlara (ganimete) kapılmamanın önemini öğretir.",
                    "B) Okçuların yerini terk etmesi zaferi hızlandırmıştır.",
                    "C) Savaşta kurallara uymanın önemli olmadığını gösterir.",
                    "D) İstişareden vazgeçilmesi gerektiğini gösterir."
                ],
                "answer_text": "Okçuların Peygamber Efendimizin 'Biz kazansak da kaybetsek de benden haber gelmedikçe yerinizi terk etmeyin!' uyarısını unutup ganimet toplamak için tepeden ayrılması, müşrik süvarilerinin ordumuzu arkadan kuşatmasına ve ağır kayıplara yol açmıştır. Dersler: 1) Peygamberimizin sünnetine ve emirlerine sıkı sıkıya bağlı kalmak, 2) Verilen görevi sonuna kadar sorumluluk bilinciyle korumak.",
                "rubric": [
                    {"criterion": "Okçular Tepesi'nin terk edilmesinin savaşın seyrine etkisinin doğru açıklanması", "points": 5},
                    {"criterion": "Görev bilinci, sabır ve Peygamberimize itaat derslerinin çıkarılması", "points": 5}
                ]
            },
            {
                "unit_no": 2,
                "learning_outcome": "[SIYER.7.2.1] Hudeybiye Barış Antlaşması'nın neden Kur'an'da 'Feth-i Mübîn (Apaçık Zafer)' olarak nitelendirildiğini yorumlar.",
                "cognitive_level": "Yorumlama",
                "difficulty": "Zor",
                "source_page": "Sayfa 54-70",
                "source_context": "628 yılında imzalanan Hudeybiye Barış Antlaşması'nın barış ortamı sağlaması, İslam'ın hızla yayılması ve Mekke'nin fethine zemin hazırlaması.",
                "arabic_text": "إِنَّا فَتَحْنَا لَكَ فَتْحًا مُّبِينًا",
                "question_text": "628 yılında imzalanan Hudeybiye Barış Antlaşması'nın bazı maddeleri ilk bakışta Müslümanların aleyhine gibi görünmesine rağmen, Fetih Suresi 1. ayette bu antlaşma 'Apaçık bir fetih (zafer)' olarak müjdelenmiştir. Hudeybiye Barışı'nın İslam'ın yayılmasına sağladığı katkıları açıklayınız.",
                "options": [
                    "A) Mekkeliler Müslümanları resmen muhatap kabul etmiş, oluşan barış ve güven ortamında insanlar İslam'ı yakından tanıyarak kitleler halinde Müslüman olmuştur.",
                    "B) Antlaşma sadece ticari vergileri düzenlemiştir.",
                    "C) Barış ortamı tebliğ çalışmalarını durdurmuştur.",
                    "D) Hudeybiye Antlaşması hiç uygulanmamıştır."
                ],
                "answer_text": "1) Mekke müşrikleri Medine İslam Devleti'ni resmen tanımış oldu. 2) Savaşların durmasıyla oluşan barış ortamında kabileler Müslümanlarla özgürce iletişim kurdu ve İslam ahlakını yakından tanıdı; iki yıl içinde önceki 18 yıldan daha fazla insan Müslüman oldu ve Mekke'nin fethine zemin hazırlandı.",
                "rubric": [
                    {"criterion": "Müslümanların siyasi bir güç olarak resmen tanınmasının belirtilmesi", "points": 5},
                    {"criterion": "Barış ortamında İslam tebliğinin hızla yayılması ve Mekke'nin fethine zemin hazırlamasının açıklanması", "points": 5}
                ]
            }
        ],
        8: [
            {
                "unit_no": 1,
                "learning_outcome": "[SIYER.8.1.1] Hacerü'l-Esved hakemliği üzerinden Peygamberimizin güvenilirliğini ve kriz çözme/uzlaştırma bilgeliğini analiz eder.",
                "cognitive_level": "Analiz",
                "difficulty": "Orta",
                "source_page": "Sayfa 14-26",
                "source_context": "Kâbe tamiri sırasında Hacerü'l-Esved taşını yerine koyma anlaşmazlığında Hz. Muhammed'in (s.a.v.) tüm kabileleri kuşatan adil çözümü.",
                "arabic_text": "",
                "question_text": "Kâbe'nin tamiri sırasında 'Hacerü'l-Esved' taşını yerine hangi kabilenin koyacağı konusunda neredeyse savaş çıkacakken, Kâbe kapısından giren Hz. Muhammed'i (s.a.v.) gören herkes 'İşte el-Emîn (Güvenilir insan) geldi, onun hakemliğine razıyız!' demiştir. Efendimiz bu krizi nasıl çözmüştür ve bu çözüm hangi liderlik özelliğini gösterir?",
                "options": [
                    "A) Hırkasını yere serip taşı üzerine koymuş, her kabile temsilcisinin bir ucundan tutarak taşı birlikte taşımasını sağlamıştır; bu durum O'nun birleştirici, adil ve kimseyi dışlamayan liderliğini gösterir.",
                    "B) Taşı sadece kendi kabilesine taşıtmıştır.",
                    "C) Kura çekerek tek bir kabile seçmiştir.",
                    "D) Taşın yerine konulmasını ertelemiştir."
                ],
                "answer_text": "Efendimiz hırkasını yere serip Hacerü'l-Esved'i üzerine koymuş ve her kabilenin temsilcisinin hırkanın birer ucundan tutarak taşı birlikte kaldırmasını sağlamış, son aşamada da mübarek elleriyle yerine yerleştirmiştir. Böylece hiçbir kabileyi dışlamadan kan dökülmesini önlemiş; adil, uzlaştırıcı ve birleştirici şahsiyetini göstermiştir.",
                "rubric": [
                    {"criterion": "Hırka/yaygı yöntemiyle tüm kabileleri sürece dahil etme çözümünün doğru anlatılması", "points": 5},
                    {"criterion": "Güvenilirlik (el-Emîn), adalet ve toplumsal uzlaşı/kriz çözme ilkelerinin açıklanması", "points": 5}
                ]
            },
            {
                "unit_no": 4,
                "learning_outcome": "[SIYER.8.4.1] Kavli, fiili ve takriri sünnet kavramlarını örneklerle açıklayarak sünnetin dinin anlaşılmasındaki yerini değerlendirir.",
                "cognitive_level": "Değerlendirme",
                "difficulty": "Orta",
                "source_page": "Sayfa 108-125",
                "source_context": "Sünnetin kısımları: Kavli (sözlü hadisler), Fiili (uygulamalar) ve Takriri (onaylamalar) sünnet ile Kur'an-Sünnet bütünlüğü.",
                "arabic_text": "وَأَنزَلْنَا إِلَيْكَ الذِّكْرَ لِتُبَيِّنَ لِلنَّاسِ",
                "question_text": "İslam dininin Kur'an-ı Kerim'den sonraki ikinci temel kaynağı olan 'Sünnet'in üç çeşidini (Kavlî, Fiilî ve Takrirî Sünnet) birer örnekle açıklayınız. Namazın kılınış şeklini ve rekât sayılarını nereden öğreniriz?",
                "options": [
                    "A) Kavlî: Sözleri, Fiilî: Davranış ve uygulamaları, Takrirî: Sahabenin yaptığı güzel işleri onaylamasıdır. Namazın kılınışını ve rekâtlarını Peygamberimizin fiilî sünnetinden ('Beni nasıl namaz kılarken görüyorsanız öyle kılın') öğreniriz.",
                    "B) Sünnet sadece sözlü tavsiyelerden ibarettir.",
                    "C) Namazın rekât sayıları sünnette yer almaz.",
                    "D) Takrirî sünnet yasaklanan davranışlardır."
                ],
                "answer_text": "1) Kavlî Sünnet: Peygamberimizin mübarek sözleridir (Hadisleri). 2) Fiilî Sünnet: Peygamberimizin bizzat yaptığı uygulama ve davranışlardır. 3) Takrirî Sünnet: Sahabelerin yaptığı doğru davranışları görüp sessiz kalarak veya överek onaylamasıdır. Kur'an'da emredilen namaz, hac ve zekât gibi ibadetlerin nasıl uygulanacağını ve rekât sayılarını Peygamberimizin sünnetinden öğreniriz.",
                "rubric": [
                    {"criterion": "Kavlî, Fiilî ve Takrirî sünnet kavramlarının doğru tanımlanması", "points": 6},
                    {"criterion": "Kur'an'daki ibadet emirlerinin (namazın kılınışı vb.) sünnetle açıklandığının belirtilmesi", "points": 4}
                ]
            }
        ]
    }
}


# ==============================================================================
# 2. DİNAMİK MÜFREDAT & DERS KİTABI VARYASYON SENTEZLEYİCİ
# Seçilen sınıf, ünite, kazanım ve PDF kitap metinlerinden her çağrıda farklı
# bağlam, karakter ve pedagojik açı (Vaka Analizi, Kavram Karşılaştırma,
# Ayet/Hadis Yorumu, Günlük Hayat Uygulaması) ile özgün sorular üretir.
# ==============================================================================

PEDAGOGICAL_ANGLES = [
    {
        "angle_id": "vaka_analizi",
        "cognitive_level": "Analiz",
        "difficulty": "Orta",
        "protagonists": [
            ("Zeynep ve ailesi", "akşam sohbetinde"),
            ("Ahmet Öğretmen ve öğrencileri", "ders içi etkinlikte"),
            ("Dedeleriyle sohbet eden Kerem ile Sude", "hafta sonu ziyaretinde"),
            ("Okul kütüphanesinde araştırma yapan Emre", "proje ödevini hazırlarken"),
            ("Cami imamıyla sohbet eden Yusuf ve arkadaşları", "kandil programı öncesinde"),
            ("Sosyal yardımlaşma kulübü öğrencisi Meryem", "okul panosunu hazırlarken")
        ]
    },
    {
        "angle_id": "kavram_ve_ilke",
        "cognitive_level": "Yorumlama",
        "difficulty": "Kolay",
        "protagonists": [
            ("Bir İmam Hatip Ortaokulu öğrencisi", "günlük hayatında"),
            ("Din Kültürü zümresinin hazırladığı çalışma yaprağında", "kavram haritası etkinliğinde"),
            ("Sınıf içi münazarada söz alan Selim", "konunun temel ilkelerini açıklarken"),
            ("Kitaptaki okuma metnini inceleyen Büşra", "ünite değerlendirme sorusunda")
        ]
    },
    {
        "angle_id": "degerlendirme_sentz",
        "cognitive_level": "Değerlendirme",
        "difficulty": "Zor",
        "protagonists": [
            ("Toplumsal dayanışma ve ahlak konulu bir seminerde", "birey-toplum ilişkisi ele alınırken"),
            ("Günümüzde karşılaşılan değer erozyonu karşısında", "bilinçli bir müminin duruşu tartışılırken"),
            ("İslam'ın evrensel mesajlarını araştıran Furkan", "neden-sonuç tablosu oluştururken"),
            ("Kazanım değerlendirme atölyesinde", "iki farklı tutum karşılaştırılırken")
        ]
    },
    {
        "angle_id": "uygulama_orneklem",
        "cognitive_level": "Uygulama",
        "difficulty": "Orta",
        "protagonists": [
            ("Öğrendiği bilgileri hayatına yansıtmak isteyen Betül", "arkadaşlık ve aile ilişkilerinde"),
            ("Ders kitabındaki örnek olayı okuyan Kaan", "kendi çevresinden örnekler verirken"),
            ("Kardeşine konuyu anlatan 8. sınıf öğrencisi Taha", "somut örnekler kullanırken"),
            ("Okul gazetesine yazı hazırlayan Elif", "konunun pratik yansımalarını sıralarken")
        ]
    }
]


def synthesize_dynamic_questions_for_units(
    subject_id: str,
    subject_name: str,
    grade: int,
    active_units: list[dict],
    scenario_items: list[dict] | None,
    book_context: str,
    is_test: bool = False
) -> list[dict]:
    """
    Seçili ünitelerin alt konularından (topics), MEB senaryo kazanımlarından ve
    PDF ders kitabından çekilen gerçek metin parçalarından çok sayıda farklı soru
    varyasyonu üretir. Böylece havuz asla tükenmez ve her sınavda farklı sorular gelir.
    """
    book_name = f"{grade}. Sınıf {subject_name} MEB Ders Kitabı"
    q_type = "coktan_secmeli" if is_test else "acik_uclu"
    synthesized = []

    # Kitap metninden anlamlı cümle/paragraf parçaları ayıkla
    book_sentences = []
    if book_context:
        for line in book_context.split("\n"):
            line_clean = line.strip()
            if line_clean.startswith("[Sayfa"):
                book_sentences.append(line_clean[:320])

    # 1) Önce Senaryo Kazanımlarından (varsa) her kazanım için 3 farklı açıdan soru sentezle
    if scenario_items:
        for sc_idx, sc in enumerate(scenario_items):
            u_no = int(sc.get("unit_no", 1))
            u_title = sc.get("unit_title", f"{u_no}. Ünite")
            o_code = sc.get("outcome_code", f"{subject_id.upper()}.{grade}.{u_no}.{sc_idx+1}")
            o_desc = sc.get("outcome_description", "").strip()

            unit_obj = None
            for u in active_units:
                if f"{u_no}. Ünite" in u.get("name", "") or u.get("id", "").endswith(f"u{u_no}"):
                    unit_obj = u
                    break
            if not unit_obj and active_units:
                unit_obj = active_units[sc_idx % len(active_units)]

            topics = unit_obj.get("topics", [u_title]) if unit_obj else [u_title]
            pr = unit_obj.get("page_range", [15, 45]) if unit_obj else [15, 45]
            page_str = f"Sayfa {pr[0]}-{pr[1]} ({unit_obj.get('name', u_title) if unit_obj else u_title})"
            ctx_snippet = (
                book_sentences[sc_idx % len(book_sentences)]
                if book_sentences
                else f"{grade}. Sınıf {subject_name} ders kitabının '{u_title}' ünitesinde {', '.join(topics[:3])} konuları ve '{o_desc}' kazanımı işlenmektedir."
            )

            # Her senaryo maddesi için 3 tamamen farklı soru kökü şablonu oluştur
            for var_idx in range(3):
                angle = PEDAGOGICAL_ANGLES[(sc_idx + var_idx) % len(PEDAGOGICAL_ANGLES)]
                actor, setting = angle["protagonists"][(sc_idx * 2 + var_idx) % len(angle["protagonists"])]
                focus_topic = topics[(sc_idx + var_idx) % len(topics)]
                paired_topic = topics[(sc_idx + var_idx + 1) % len(topics)]
                template_variant = (sc_idx * 3 + var_idx) % 9

                if template_variant == 0:
                    q_txt = (
                        f"{actor}, {setting} '{focus_topic}' konusunu ele almıştır. "
                        f"'{o_desc}' kazanımı doğrultusunda '{focus_topic}' kavramının temel anlamını ve "
                        f"insan hayatına kazandırdığı olumlu yönleri iki madde halinde açıklayınız."
                    )
                elif template_variant == 1:
                    q_txt = (
                        f"'{o_desc}' kazanımı kapsamında; '{focus_topic}' ile '{paired_topic}' konuları arasındaki "
                        f"ilişkiyi günlük hayattan somut bir örnek vererek yorumlayınız."
                    )
                elif template_variant == 2:
                    q_txt = (
                        f"'{u_title}' ünitesinde vurgulanan '{focus_topic}' ilkesine uygun hareket eden bir müminin; "
                        f"bireysel ahlakına ve toplumsal huzura sağlayacağı katkıları değerlendiriniz."
                    )
                elif template_variant == 3:
                    q_txt = (
                        f"Bir öğrencinin '{focus_topic}' konusunu öğrendikten sonra davranışlarında hangi olumlu "
                        f"değişimlerin görülmesi beklenir? '{o_desc}' ilkesini dikkate alarak 3 örnek yazınız."
                    )
                elif template_variant == 4:
                    q_txt = (
                        f"Ders kitabımızın '{u_title}' ünitesinde geçen '{focus_topic}' kavramını tanımlayarak; "
                        f"bu kavramın İslam'ın inanç ve ibadet bütünlüğü içindeki yerini açıklayınız."
                    )
                elif template_variant == 5:
                    q_txt = (
                        f"{actor} {setting} arkadaşlarına şu soruyu yöneltmiştir: "
                        f"\"'{focus_topic}' ilkesini hayatımıza nasıl yansıtabiliriz?\" "
                        f"'{o_desc}' kazanımına göre bu soruya verilebilecek en doğru cevabı gerekçesiyle yazınız."
                    )
                elif template_variant == 6:
                    q_txt = (
                        f"'{u_title}' ünitesindeki '{focus_topic}' ve '{paired_topic}' başlıklarının "
                        f"verdiği ortak mesaj nedir? '{o_desc}' çerçevesinde analiz ediniz."
                    )
                elif template_variant == 7:
                    q_txt = (
                        f"Günümüzde '{focus_topic}' bilincinin yaşatılması neden önemlidir? "
                        f"Bu bilincin zayıflaması durumunda ortaya çıkabilecek sorunları ve çözüm yollarını açıklayınız."
                    )
                else:
                    q_txt = (
                        f"İslam ahlakı ve '{u_title}' ünitesi açısından '{focus_topic}' kavramının önemi nedir? "
                        f"'{o_desc}' kazanımına uygun olarak neden-sonuç ilişkisiyle açıklayınız."
                    )

                opts = [
                    f"A) '{focus_topic}' ilkesini doğru kavrayarak inanç, ibadet ve güzel ahlak bütünlüğü içinde hayata yansıtır.",
                    f"B) Konunun yalnızca teorik tanımıyla yetinip günlük davranışlarla ilişkilendirmez.",
                    f"C) '{focus_topic}' ilkesinin sadece geçmiş dönemlerle sınırlı olduğunu düşünür.",
                    f"D) Toplumsal sorumlulukları göz ardı ederek yalnızca bireysel çıkarları öne alır."
                ]
                ans_txt = (
                    f"'{focus_topic}' konusu ({o_code}: {o_desc}), bireyin dini ve ahlaki bilincini güçlendirir. "
                    f"1) Kişiye sorumluluk, özdenetim ve doğru inanç/uygulama bilinci kazandırır. "
                    f"2) Günlük yaşamda sevgi, saygı, doğruluk ve dayanışmayı artırarak toplumsal huzura katkı sağlar."
                )

                synthesized.append({
                    "unit_no": u_no,
                    "unit_name": unit_obj.get("name", u_title) if unit_obj else u_title,
                    "learning_outcome": f"[{o_code}] {o_desc}",
                    "question_type": q_type,
                    "cognitive_level": angle["cognitive_level"],
                    "difficulty": angle["difficulty"],
                    "source_book": book_name,
                    "source_page": page_str,
                    "source_context": ctx_snippet,
                    "arabic_text": "",
                    "question_text": q_txt,
                    "options": opts if is_test else [],
                    "answer_text": ans_txt,
                    "rubric": [
                        {"criterion": f"'{focus_topic}' kavramının ve kazanım ilkesinin doğru açıklanması", "points": 5},
                        {"criterion": "Günlük hayat veya toplumsal yansımasının uygun örneklerle yazılması", "points": 5}
                    ]
                })

    # 2) Ayrıca seçili her ünitenin her alt başlığı (topic) için özgün ünite soruları üret
    for u_idx, u in enumerate(active_units):
        u_name = u.get("name", f"{u_idx + 1}. Ünite")
        pr = u.get("page_range", [12, 48])
        page_str = f"Sayfa {pr[0]}-{pr[1]} ({u_name})"
        topics = u.get("topics", [])

        # Ünite numarasını çıkar
        m = re.search(r"(\d+)", u.get("id", "") or u_name)
        u_no = int(m.group(1)) if m else (u_idx + 1)

        for t_idx, topic in enumerate(topics):
            angle = PEDAGOGICAL_ANGLES[(u_idx + t_idx) % len(PEDAGOGICAL_ANGLES)]
            actor, setting = angle["protagonists"][(u_idx + t_idx) % len(angle["protagonists"])]
            paired_topic = topics[(t_idx + 1) % len(topics)] if len(topics) > 1 else topic

            outcome_code = f"{subject_id.upper()}.{grade}.{u_no}.{t_idx + 1}"
            outcome_str = f"[{outcome_code}] {u_name} kapsamında '{topic}' konusunu analiz eder ve yorumlar."

            topic_variant = (u_idx * 3 + t_idx) % 5
            if topic_variant == 0:
                q_txt = (
                    f"'{topic}' konusunun temel mesajını açıklayarak; "
                    f"{actor} örneğinde olduğu gibi {setting} bu konunun günlük hayatımıza nasıl rehberlik ettiğini yazınız."
                )
            elif topic_variant == 1:
                q_txt = (
                    f"'{topic}' ile '{paired_topic}' kavramlarını karşılaştırarak; "
                    f"her iki kavramın İslam düşüncesi ve ahlakı açısından önemini ikişer cümleyle açıklayınız."
                )
            elif topic_variant == 2:
                q_txt = (
                    f"{u_name} ünitesinde yer alan '{topic}' başlığında vurgulanan temel ilkeler nelerdir? "
                    f"Maddeler halinde yazarak bir örnekle açıklayınız."
                )
            elif topic_variant == 3:
                q_txt = (
                    f"Bir Müslümanın '{topic}' konusundaki duyarlılığı, onun ibadetlerine ve insanlarla olan "
                    f"iletişimine nasıl yansır? '{u_name}' ünitesi kapsamında değerlendiriniz."
                )
            else:
                q_txt = (
                    f"Ders kitabımızda '{u_name}' ünitesinde işlenen '{topic}' konusunun birey ve toplum "
                    f"açısından önemini neden-sonuç ilişkisi kurarak yorumlayınız."
                )

            opts = [
                f"A) '{topic}' konusu, doğru bilgi ve güzel ahlak ilkeleriyle bireyin hayatına yön verir.",
                f"B) '{topic}' yalnızca tarihsel bir kavram olup günümüzle ilişkisi yoktur.",
                f"C) '{paired_topic}' ile '{topic}' birbirine tamamen zıt kavramlardır.",
                f"D) Bu ilkeler sadece belirli kişiler için geçerlidir."
            ]

            synthesized.append({
                "unit_no": u_no,
                "unit_name": u_name,
                "learning_outcome": outcome_str,
                "question_type": q_type,
                "cognitive_level": angle["cognitive_level"],
                "difficulty": angle["difficulty"],
                "source_book": book_name,
                "source_page": page_str,
                "source_context": f"{book_name} {page_str} aralığında '{topic}' ve '{paired_topic}' konuları örneklerle ele alınmaktadır.",
                "arabic_text": "",
                "question_text": q_txt,
                "options": opts if is_test else [],
                "answer_text": (
                    f"'{topic}' konusu, {u_name} ünitesinin temel kazanımlarından biridir. "
                    f"Bireyin konuyu doğru anlaması, hem ibadet/ahlak bilincini geliştirir hem de '{paired_topic}' ilkesiyle bütünleşerek örnek bir yaşam sürmesini sağlar."
                ),
                "rubric": [
                    {"criterion": f"'{topic}' kavramının/konusunun doğru tanımlanıp açıklanması", "points": 5},
                    {"criterion": "Örnek olay veya günlük yaşam bağlantısının doğru kurulması", "points": 5}
                ]
            })

    return synthesized


# ==============================================================================
# 3. GENİŞLETİLMİŞ BEP SORU HAVUZU ÜRETİCİSİ (TEKRARI ÖNLEYEN ÇOKLU SETLER)
# ==============================================================================

EXTRA_BEP_POOLS = {
    "dkab": [
        {
            "learning_outcome": "[BEP.DKAB.7] İslam'ın şartlarını ve temel ibadetleri doğru açıklamalarıyla eşleştirir.",
            "question_type": "bep_eslestirme",
            "cognitive_level": "Hatırlama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 48-56 (BEP Temel Kazanım)",
            "source_context": "BEP Kavram Eşleştirme: Namaz, Oruç, Zekât ve Hac ibadetleri en yalın tanımlarıyla eşleştirilir.",
            "arabic_text": "",
            "question_text": (
                "Aşağıdaki İslam'ın şartlarından olan temel ibadetleri karşısındaki açıklamalarla ok çizerek eşleştiriniz:\n"
                "1) Namaz ......................  ( a ) Ramazan ayında yeme ve içmeden uzak durarak yapılır.\n"
                "2) Oruç .......................  ( b ) Günde beş vakit abdest alınarak kılınır.\n"
                "3) Zekât ......................  ( c ) Kâbe'yi ve kutsal mekânları ziyaret ederek yapılır.\n"
                "4) Hac ........................  ( d ) Zenginlerin yoksullara yılda bir kez verdiği yardımdır."
            ),
            "options": [
                "A) 1-b, 2-a, 3-d, 4-c",
                "B) 1-a, 2-b, 3-c, 4-d",
                "C) 1-d, 2-c, 3-b, 4-a"
            ],
            "answer_text": "1) Namaz -> (b) Günde beş vakit kılınır | 2) Oruç -> (a) Ramazan ayında tutulur | 3) Zekât -> (d) Yoksullara verilen yardımdır | 4) Hac -> (c) Kâbe'yi ziyarettir",
            "rubric": [{"criterion": "Her doğru eşleştirme için eşit puan verilir", "points": 20}]
        },
        {
            "learning_outcome": "[BEP.DKAB.8] Dört büyük meleği ve görevlerini eşleştirir.",
            "question_type": "bep_eslestirme",
            "cognitive_level": "Hatırlama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 18-24 (BEP Temel Kazanım)",
            "source_context": "BEP Melek İnancı: Dört büyük melek ve temel görevleri sade ifadelerle eşleştirilir.",
            "arabic_text": "",
            "question_text": (
                "Dört büyük meleği karşısındaki görevleriyle ok çizerek eşleştiriniz:\n"
                "1) Cebrail .....................  ( a ) Doğa olaylarını (yağmur, rüzgâr) yöneten melektir.\n"
                "2) Mikail ......................  ( b ) Peygamberlere vahiy (mesaj) getiren melektir.\n"
                "3) İsrafil .....................  ( c ) Ömrü bitenlerin canını alan melektir.\n"
                "4) Azrail ......................  ( d ) Kıyamet günü Sûr'a üfleyecek olan melektir."
            ),
            "options": [
                "A) 1-b, 2-a, 3-d, 4-c",
                "B) 1-a, 2-b, 3-c, 4-d",
                "C) 1-c, 2-d, 3-a, 4-b"
            ],
            "answer_text": "1) Cebrail -> (b) Vahiy meleği | 2) Mikail -> (a) Doğa olayları meleği | 3) İsrafil -> (d) Sûr meleği | 4) Azrail -> (c) Can alma meleği",
            "rubric": [{"criterion": "Her doğru eşleştirme için eşit puan verilir", "points": 20}]
        },
        {
            "learning_outcome": "[BEP.DKAB.9] Güzel ahlaki davranışları kelime havuzundan seçerek tamamlar.",
            "question_type": "bep_bosluk_doldurma",
            "cognitive_level": "Uygulama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 92-104 (BEP Temel Kazanım)",
            "source_context": "BEP Kelime Havuzlu Boşluk Doldurma: Selam, Besmele, Şükür ve Doğruluk kavramları.",
            "arabic_text": "",
            "question_text": (
                "📦 KELİME HAVUZU:  [  Bismillah   |   Selam   |   Elhamdülillah   |   Dürüst  ]\n"
                "Yukarıdaki kutucukta verilen kelimelerden uygun olanları aşağıdaki boşluklara yazınız:\n"
                "1) Yemek yemeye ve her güzel işe başlarken .................................... deriz.\n"
                "2) Yemeği bitirdikten sonra Allah'a teşekkür etmek için .................................... deriz.\n"
                "3) Arkadaşlarımızla karşılaştığımızda 'Selamün Aleyküm' diyerek .................................... veririz.\n"
                "4) Asla yalan söylemeyen ve sözünde duran insana .................................... insan denir."
            ),
            "options": [
                "A) 1: Bismillah - 2: Elhamdülillah - 3: Selam - 4: Dürüst",
                "B) 1: Selam - 2: Bismillah - 3: Dürüst - 4: Elhamdülillah",
                "C) 1: Dürüst - 2: Selam - 3: Bismillah - 4: Elhamdülillah"
            ],
            "answer_text": "1) Bismillah  —  2) Elhamdülillah  —  3) Selam  —  4) Dürüst",
            "rubric": [{"criterion": "Kelime havuzundaki her kelimenin doğru boşluğa yazılması", "points": 20}]
        },
        {
            "learning_outcome": "[BEP.DKAB.10] Temizlik ve ibadet kurallarını Doğru-Yanlış cümleleriyle ayırt eder.",
            "question_type": "bep_dogru_yanlis",
            "cognitive_level": "Kavrama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 52-64 (BEP Temel Kazanım)",
            "source_context": "BEP Doğru-Yanlış Etkinliği: Abdest, namaz, Kâbe ve anne-baba saygısı.",
            "arabic_text": "",
            "question_text": (
                "Aşağıdaki cümlelerin başına bilgi Doğru ise ( D ), Yanlış ise ( Y ) yazınız:\n"
                "( ..... ) Namaz kılmadan önce el, yüz, kol, baş ve ayakları yıkayarak abdest alırız.\n"
                "( ..... ) Anne ve babamıza karşı her zaman saygılı ve güler yüzlü olmalıyız.\n"
                "( ..... ) Suyu ve ekmeği gereksiz yere çöpe atıp israf etmek güzel bir davranıştır.\n"
                "( ..... ) Müslümanların dinî bayramları Ramazan Bayramı ve Kurban Bayramı'dır."
            ),
            "options": [
                "A) D - D - Y - D",
                "B) D - Y - D - Y",
                "C) Y - D - Y - D"
            ],
            "answer_text": "1) ( D ) Doğru  |  2) ( D ) Doğru  |  3) ( Y ) Yanlış  |  4) ( D ) Doğru",
            "rubric": [{"criterion": "Her doğru (D/Y) işaretlemesi için eşit puan verilir", "points": 20}]
        },
        {
            "learning_outcome": "[BEP.DKAB.11] Cuma ve bayram namazlarının toplumsal birlikteliğe katkısını tanır.",
            "question_type": "bep_coktan_secmeli_3",
            "cognitive_level": "Hatırlama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 68-74 (BEP Temel Kazanım)",
            "source_context": "BEP 3 Seçenekli Çoktan Seçmeli: Müslümanların haftada bir gün camide toplanarak cemaatle kıldığı namaz.",
            "arabic_text": "",
            "question_text": "Müslümanların her hafta Cuma günü öğle vaktinde camide bir araya gelerek cemaatle kıldıkları farz namaz hangisidir? Doğru olanı işaretleyiniz.",
            "options": [
                "A) Cuma Namazı",
                "B) Teravih Namazı",
                "C) Cenaze Namazı"
            ],
            "answer_text": "Doğru Seçenek: A) Cuma Namazı",
            "rubric": [{"criterion": "A seçeneğinin (Cuma Namazı) doğru işaretlenmesi", "points": 20}]
        },
        {
            "learning_outcome": "[BEP.DKAB.12] İslam'da selamlaşma ve dua ifadelerini tanır.",
            "question_type": "bep_coktan_secmeli_3",
            "cognitive_level": "Kavrama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 95-102 (BEP Temel Kazanım)",
            "source_context": "BEP 3 Seçenekli Çoktan Seçmeli: Hasta ziyaretinde veya iyilik gördüğümüzde söylediğimiz güzel sözler.",
            "arabic_text": "",
            "question_text": "Hasta olan bir arkadaşımızı ziyaret ettiğimizde ona iyi dileklerimizi bildirmek için ne söyleriz? Doğru olanı işaretleyiniz.",
            "options": [
                "A) Geçmiş olsun, Allah şifa versin.",
                "B) Güle güle oturunuz.",
                "C) Yolunuz açık olsun."
            ],
            "answer_text": "Doğru Seçenek: A) Geçmiş olsun, Allah şifa versin.",
            "rubric": [{"criterion": "A seçeneğinin doğru işaretlenmesi", "points": 20}]
        }
    ],
    "siyer": [
        {
            "learning_outcome": "[BEP.SİYER.7] Peygamberimizin çocuklarını, torunlarını ve yakın arkadaşlarını kelime havuzundan seçerek tamamlar.",
            "question_type": "bep_bosluk_doldurma",
            "cognitive_level": "Hatırlama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 75-92 (BEP Temel Kazanım)",
            "source_context": "BEP Kelime Havuzlu Boşluk Doldurma: Peygamberimizin ailesi ve sevgili torunları.",
            "arabic_text": "",
            "question_text": (
                "📦 KELİME HAVUZU:  [  Hz. Fâtıma   |   Hz. Ebu Bekir   |   571   |   Muhacir  ]\n"
                "Yukarıdaki kutucukta verilen kelimelerden uygun olanları aşağıdaki boşluklara yazınız:\n"
                "1) Peygamber Efendimiz (s.a.v.) miladi .................................... yılında dünyaya gelmiştir.\n"
                "2) Peygamberimizin çok sevdiği, Hz. Hasan ve Hz. Hüseyin'in annesi olan kızı ....................................'dır.\n"
                "3) Hicret yolculuğunda Peygamberimize yol arkadaşlığı yapan en yakın dostu ....................................'dir.\n"
                "4) İnançları için Mekke'deki evlerini bırakıp Medine'ye göç eden Müslümanlara .................................... denir."
            ),
            "options": [
                "A) 1: 571 - 2: Hz. Fâtıma - 3: Hz. Ebu Bekir - 4: Muhacir",
                "B) 1: Muhacir - 2: 571 - 3: Hz. Fâtıma - 4: Hz. Ebu Bekir",
                "C) 1: Hz. Ebu Bekir - 2: Muhacir - 3: 571 - 4: Hz. Fâtıma"
            ],
            "answer_text": "1) 571  —  2) Hz. Fâtıma  —  3) Hz. Ebu Bekir  —  4) Muhacir",
            "rubric": [{"criterion": "Kelime havuzundaki her kelimenin doğru boşluğa yazılması", "points": 20}]
        },
        {
            "learning_outcome": "[BEP.SİYER.8] Peygamberimizin hayatındaki kutsal mekânları açıklamalarıyla eşleştirir.",
            "question_type": "bep_eslestirme",
            "cognitive_level": "Kavrama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 48-115 (BEP Temel Kazanım)",
            "source_context": "BEP Mekân Eşleştirmesi: Kâbe, Hira Mağarası, Mescid-i Nebevî ve Suffe.",
            "arabic_text": "",
            "question_text": (
                "Peygamberimizin hayatındaki önemli mekânları karşısındaki açıklamalarla ok çizerek eşleştiriniz:\n"
                "1) Kâbe ........................  ( a ) Peygamberimize ilk vahyin geldiği mağaradır.\n"
                "2) Hira Mağarası ...............  ( b ) Mekke'de bulunan ve namazda yöneldiğimiz kutsal mabettir.\n"
                "3) Mescid-i Nebevî .............  ( c ) Medine'de öğrencilerin ilim öğrendiği okul bölümüdür.\n"
                "4) Suffe .......................  ( d ) Peygamberimizin Medine'de inşa ettiği mescittir."
            ),
            "options": [
                "A) 1-b, 2-a, 3-d, 4-c",
                "B) 1-a, 2-b, 3-c, 4-d",
                "C) 1-d, 2-c, 3-b, 4-a"
            ],
            "answer_text": "1) Kâbe -> (b) | 2) Hira Mağarası -> (a) | 3) Mescid-i Nebevî -> (d) | 4) Suffe -> (c)",
            "rubric": [{"criterion": "Her doğru eşleştirme için eşit puan verilir", "points": 20}]
        },
        {
            "learning_outcome": "[BEP.SİYER.9] Peygamberimizin örnek davranışlarını Doğru-Yanlış cümleleriyle ayırt eder.",
            "question_type": "bep_dogru_yanlis",
            "cognitive_level": "Kavrama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 80-110 (BEP Temel Kazanım)",
            "source_context": "BEP Doğru-Yanlış: Aile yardımı, misafirperverlik, affedicilik ve israftan kaçınma.",
            "arabic_text": "",
            "question_text": (
                "Aşağıdaki cümlelerin başına bilgi Doğru ise ( D ), Yanlış ise ( Y ) yazınız:\n"
                "( ..... ) Peygamberimiz ev işlerinde ailesine yardım eder ve herkese güler yüz gösterirdi.\n"
                "( ..... ) Peygamberimiz Mekke fethedildiğinde kendisine kötülük yapanları bile affetmiştir.\n"
                "( ..... ) Peygamberimiz suyu ve yiyecekleri israf etmemizi yasaklamıştır.\n"
                "( ..... ) Peygamberimiz hasta olan komşularını hiç ziyaret etmezdi."
            ),
            "options": [
                "A) D - D - D - Y",
                "B) D - Y - D - D",
                "C) Y - D - Y - D"
            ],
            "answer_text": "1) ( D ) Doğru  |  2) ( D ) Doğru  |  3) ( D ) Doğru  |  4) ( Y ) Yanlış",
            "rubric": [{"criterion": "Her doğru (D/Y) işaretlemesi için eşit puan verilir", "points": 20}]
        },
        {
            "learning_outcome": "[BEP.SİYER.10] Peygamberimize ilk vahyi getiren meleği ve ilk emri tanır.",
            "question_type": "bep_coktan_secmeli_3",
            "cognitive_level": "Hatırlama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 16-24 (BEP Temel Kazanım)",
            "source_context": "BEP 3 Seçenekli Çoktan Seçmeli: İlk vahiy ve Oku (İkra) emri.",
            "arabic_text": "اقْرَأْ",
            "question_text": "Hira Mağarası'nda vahiy meleği Cebrail'in (a.s.) Peygamber Efendimize getirdiği ilk ayetin ilk emri aşağıdakilerden hangisidir? İşaretleyiniz.",
            "options": [
                "A) Oku! (Yaratan Rabbinin adıyla oku)",
                "B) Yolculuk yap!",
                "C) Ticaret yap!"
            ],
            "answer_text": "Doğru Seçenek: A) Oku! (Yaratan Rabbinin adıyla oku)",
            "rubric": [{"criterion": "A seçeneğinin (Oku!) doğru işaretlenmesi", "points": 20}]
        }
    ],
    "kuran": [
        {
            "learning_outcome": "[BEP.KURAN.7] Kur'an-ı Kerim ile ilgili temel kavramları açıklamalarıyla eşleştirir.",
            "question_type": "bep_eslestirme",
            "cognitive_level": "Hatırlama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 14-28 (BEP Temel Kazanım)",
            "source_context": "BEP Kavram Eşleştirme: Ayet, Sure, Cüz ve Hafız kavramları.",
            "arabic_text": "",
            "question_text": (
                "Kur'an-ı Kerim ile ilgili aşağıdaki temel kavramları karşısındaki doğru anlamlarıyla ok çizerek eşleştiriniz:\n"
                "1) Ayet ........................  ( a ) Kur'an-ı Kerim'in 20 sayfalık her bir bölümüdür.\n"
                "2) Sure ........................  ( b ) Kur'an-ı Kerim'in her bir cümlesidir.\n"
                "3) Cüz .........................  ( c ) Kur'an-ı Kerim'i baştan sona ezberleyen kişidir.\n"
                "4) Hâfız .......................  ( d ) Ayetlerden oluşan bölümlerdir (114 tanedir)."
            ),
            "options": [
                "A) 1-b, 2-d, 3-a, 4-c",
                "B) 1-a, 2-b, 3-c, 4-d",
                "C) 1-c, 2-a, 3-d, 4-b"
            ],
            "answer_text": "1) Ayet -> (b) Cümledir | 2) Sure -> (d) 114 bölümdür | 3) Cüz -> (a) 20 sayfalık bölümdür | 4) Hâfız -> (c) Kur'an'ı ezberleyen kişidir",
            "rubric": [{"criterion": "Her doğru eşleştirme için eşit puan verilir", "points": 20}]
        },
        {
            "learning_outcome": "[BEP.KURAN.8] Kur'an-ı Kerim'in temel bilgilerini kelime havuzundan seçerek tamamlar.",
            "question_type": "bep_bosluk_doldurma",
            "cognitive_level": "Uygulama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 20-45 (BEP Temel Kazanım)",
            "source_context": "BEP Kelime Havuzlu Boşluk Doldurma: 30 Cüz, 114 Sure, Kadir Gecesi ve Kevser Suresi.",
            "arabic_text": "",
            "question_text": (
                "📦 KELİME HAVUZU:  [  30   |   114   |   Kadir   |   Bakara  ]\n"
                "Yukarıdaki kutucukta verilen kelimelerden uygun olanları aşağıdaki boşluklara yazınız:\n"
                "1) Kur'an-ı Kerim Ramazan ayının .................................... Gecesi'nde indirilmeye başlanmıştır.\n"
                "2) Kur'an-ı Kerim'de toplam .................................... adet cüz vardır.\n"
                "3) Kur'an-ı Kerim'de toplam .................................... adet sure vardır.\n"
                "4) Kur'an-ı Kerim'in en uzun suresi .................................... suresidir."
            ),
            "options": [
                "A) 1: Kadir - 2: 30 - 3: 114 - 4: Bakara",
                "B) 1: Bakara - 2: 114 - 3: 30 - 4: Kadir",
                "C) 1: 30 - 2: Kadir - 3: Bakara - 4: 114"
            ],
            "answer_text": "1) Kadir  —  2) 30  —  3) 114  —  4) Bakara",
            "rubric": [{"criterion": "Kelime havuzundaki her kelimenin doğru boşluğa yazılması", "points": 20}]
        },
        {
            "learning_outcome": "[BEP.KURAN.9] Uzatma (Med) harflerini ve Kur'an bilgilerini Doğru-Yanlış cümleleriyle ayırt eder.",
            "question_type": "bep_dogru_yanlis",
            "cognitive_level": "Kavrama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 46-68 (BEP Temel Kazanım)",
            "source_context": "BEP Doğru-Yanlış: Elif-Vav-Ya uzatma harfleri ve sure bilgileri.",
            "arabic_text": "ا   —   و   —   ي",
            "question_text": (
                "Aşağıdaki cümlelerin başına bilgi Doğru ise ( D ), Yanlış ise ( Y ) yazınız:\n"
                "( ..... ) Kur'an-ı Kerim'de uzatma (med) harfleri Elif ( ا ), Vav ( و ) ve Ya ( ي ) olmak üzere 3 tanedir.\n"
                "( ..... ) Kur'an-ı Kerim'in ilk suresi Fâtiha Suresi, son suresi ise Nâs Suresi'dir.\n"
                "( ..... ) İki üstün, iki esre ve iki ötre işaretlerine 'Tenvin' denir.\n"
                "( ..... ) Kur'an-ı Kerim soldan sağa doğru okunur."
            ),
            "options": [
                "A) D - D - D - Y",
                "B) D - Y - D - D",
                "C) Y - D - Y - D"
            ],
            "answer_text": "1) ( D ) Doğru  |  2) ( D ) Doğru  |  3) ( D ) Doğru  |  4) ( Y ) Yanlış",
            "rubric": [{"criterion": "Her doğru (D/Y) işaretlemesi için eşit puan verilir", "points": 20}]
        },
        {
            "learning_outcome": "[BEP.KURAN.10] Kur'an-ı Kerim harflerini tanır ve okunuşunu işaretler.",
            "question_type": "bep_coktan_secmeli_3",
            "cognitive_level": "Hatırlama (BEP)",
            "difficulty": "Kolay",
            "source_page": "Sayfa 16-25 (BEP Temel Kazanım)",
            "source_context": "BEP Harf Tanıma: Elif, Be, Cim, Dal, Ra, Sin, Şın harfleri.",
            "arabic_text": "ر   —   س   —   ش",
            "question_text": "Yukarıda verilen üç Kur'an-ı Kerim harfinin sırasıyla isimleri aşağıdakilerden hangisidir? Doğru olanı işaretleyiniz.",
            "options": [
                "A) Ra — Sin — Şın",
                "B) Dal — Zel — Vav",
                "C) Sad — Dad — Tı"
            ],
            "answer_text": "Doğru Seçenek: A) Ra (ر) — Sin (س) — Şın (ش)",
            "rubric": [{"criterion": "A seçeneğinin (Ra - Sin - Şın) doğru işaretlenmesi", "points": 20}]
        }
    ]
}


def synthesize_dynamic_bep_questions_for_units(
    subject_id: str,
    subject_name: str,
    grade: int,
    active_units: list[dict]
) -> list[dict]:
    """
    Seçili sınıf ve ünitelerin alt konularından (topics) BEP'e uygun
    (Eşleştirme, Doğru/Yanlış, Kelime Havuzlu Boşluk Doldurma ve 3 Şıklı Test)
    dinamik sorular üretir. Böylece BEP sınavlarında da her tıklamada yeni sorular gelir.
    """
    dynamic_bep = []
    for u_idx, u in enumerate(active_units):
        u_name = u.get("name", f"{u_idx + 1}. Ünite")
        topics = u.get("topics", [])
        pr = u.get("page_range", [12, 48])
        page_str = f"Sayfa {pr[0]}-{pr[1]} ({u_name} - BEP Uyarlaması)"

        if len(topics) >= 3:
            t1, t2, t3 = topics[0], topics[1], topics[2]
            t4 = topics[3] if len(topics) >= 4 else "Güzel Ahlak ve Doğruluk"

            # 1) Üniteye özel Kelime Havuzlu Boşluk Doldurma
            dynamic_bep.append({
                "learning_outcome": f"[BEP.{subject_id.upper()}.{grade}.U{u_idx+1}.A] '{u_name}' ünitesindeki temel kavramları kelime havuzundan seçerek tamamlar.",
                "question_type": "bep_bosluk_doldurma",
                "cognitive_level": "Hatırlama / Uygulama (BEP)",
                "difficulty": "Kolay",
                "source_page": page_str,
                "source_context": f"{grade}. Sınıf {subject_name} dersi '{u_name}' ünitesi BEP kelime havuzlu etkinlik uyarlaması.",
                "arabic_text": "",
                "question_text": (
                    f"📦 KELİME HAVUZU:  [  {t1}   |   {t2}   |   {t3}   |   {t4}  ]\n"
                    f"Yukarıdaki kutucukta verilen '{u_name}' ünitesi kavramlarını uygun boşluklara yazınız:\n"
                    f"1) Bu ünitede öğrendiğimiz ilk temel konu .................................... konusudur.\n"
                    f"2) Ders kitabımızda üzerinde durulan ikinci önemli başlık .................................... ilkesidir.\n"
                    f"3) Günlük hayatımıza rehberlik eden bir diğer konu .................................... bilincidir.\n"
                    f"4) Ünitemizi tamamlayan örnek davranış ve değer ise .................................... konusudur."
                ),
                "options": [
                    f"A) 1: {t1} - 2: {t2} - 3: {t3} - 4: {t4}",
                    f"B) 1: {t3} - 2: {t1} - 3: {t4} - 4: {t2}",
                    f"C) 1: {t4} - 2: {t3} - 3: {t2} - 4: {t1}"
                ],
                "answer_text": f"1) {t1}  —  2) {t2}  —  3) {t3}  —  4) {t4}",
                "rubric": [{"criterion": "Kelime havuzundaki her ifadenin doğru boşluğa yazılması", "points": 20}]
            })

            # 2) Üniteye özel Doğru / Yanlış
            dynamic_bep.append({
                "learning_outcome": f"[BEP.{subject_id.upper()}.{grade}.U{u_idx+1}.B] '{u_name}' ünitesindeki doğru ve yanlış ifadeleri ayırt eder.",
                "question_type": "bep_dogru_yanlis",
                "cognitive_level": "Kavrama (BEP)",
                "difficulty": "Kolay",
                "source_page": page_str,
                "source_context": f"{grade}. Sınıf {subject_name} dersi '{u_name}' ünitesi BEP Doğru-Yanlış uyarlaması.",
                "arabic_text": "",
                "question_text": (
                    f"Aşağıdaki '{u_name}' ünitesi cümlelerinin başına Doğru ise ( D ), Yanlış ise ( Y ) yazınız:\n"
                    f"( ..... ) '{t1}' konusu bize doğru inanç ve güzel davranış ilkelerini öğretir.\n"
                    f"( ..... ) '{t2}' konusunda öğrendiğimiz bilgileri günlük hayatımızda uygulamalıyız.\n"
                    f"( ..... ) İslam dini insanlara zarar vermeyi, yalan söylemeyi ve israfı yasaklamıştır.\n"
                    f"( ..... ) '{t3}' konusunun günlük hayatımızla ve ahlakımızla hiçbir ilgisi yoktur."
                ),
                "options": [
                    "A) D - D - D - Y",
                    "B) D - Y - D - D",
                    "C) Y - D - Y - D"
                ],
                "answer_text": "1) ( D ) Doğru  |  2) ( D ) Doğru  |  3) ( D ) Doğru  |  4) ( Y ) Yanlış",
                "rubric": [{"criterion": "Her doğru (D/Y) işaretlemesi için eşit puan verilir", "points": 20}]
            })

            # 3) Üniteye özel 3 Seçenekli Çoktan Seçmeli
            dynamic_bep.append({
                "learning_outcome": f"[BEP.{subject_id.upper()}.{grade}.U{u_idx+1}.C] '{u_name}' ünitesinin temel mesajını 3 seçenek arasından işaretler.",
                "question_type": "bep_coktan_secmeli_3",
                "cognitive_level": "Hatırlama / Kavrama (BEP)",
                "difficulty": "Kolay",
                "source_page": page_str,
                "source_context": f"{grade}. Sınıf {subject_name} dersi '{u_name}' ünitesi 3 seçenekli BEP sorusu.",
                "arabic_text": "",
                "question_text": f"{grade}. Sınıf {subject_name} dersimizin '{u_name}' ünitesinde işlenen '{t1}' ve '{t2}' konuları bize aşağıdakilerden hangisini kazandırır? Doğru olanı işaretleyiniz.",
                "options": [
                    "A) Doğru bilgi sahibi olmayı, güzel ahlaklı ve duyarlı bir insan olmayı",
                    "B) Arkadaşlarımızla tartışmayı ve kurallara uymamayı",
                    "C) Sorumluluklarımızı ihmal etmeyi"
                ],
                "answer_text": "Doğru Seçenek: A) Doğru bilgi sahibi olmayı, güzel ahlaklı ve duyarlı bir insan olmayı",
                "rubric": [{"criterion": "A seçeneğinin doğru işaretlenmesi", "points": 20}]
            })

    return dynamic_bep

