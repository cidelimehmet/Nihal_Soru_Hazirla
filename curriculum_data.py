"""
Müfredat, Kazanımlar ve Kitap Sayfa Haritası Modülü - Dinamik & Özelleştirilebilir Sürüm
data/custom_curriculum.json dosyasından okur ve öğretmenin düzenlemelerine izin verir.
"""

import json
from pathlib import Path
from config import DATA_DIR

CUSTOM_CURRICULUM_PATH = DATA_DIR / "custom_curriculum.json"

DEFAULT_CURRICULUM = {
    "dkab": {
        "name": "Din Kültürü ve Ahlak Bilgisi",
        "grades": {
            5: {
                "pdf_pattern": "din-kulturu-ve-ahlak-bilgisi-5sinif",
                "units": [
                    {
                        "id": "dkab5_u1",
                        "name": "1. Ünite: Allah İnancı",
                        "topics": ["Allah Vardır ve Birdir", "Allah Yaradandır", "Allah Rahman ve Rahimdir", "Allah Görür ve İşitir", "İhlas Suresi ve Anlamı"],
                        "page_range": [11, 48]
                    },
                    {
                        "id": "dkab5_u2",
                        "name": "2. Ünite: Ramazan ve Oruç / Namaz İbadeti",
                        "topics": ["Ramazan Orucu ve Önemi", "Namaz İbadeti ve Önemi", "Namaz Çeşitleri", "Namazın Şartları", "Rabbena Duaları"],
                        "page_range": [49, 90]
                    },
                    {
                        "id": "dkab5_u3",
                        "name": "3. Ünite: Adap ve Nezaket",
                        "topics": ["Nezaket Kuralları", "Selamlaşma Adabı", "İletişim ve Konuşma Adabı", "Sofra Adabı", "Tahiyyat Duası"],
                        "page_range": [91, 130]
                    },
                    {
                        "id": "dkab5_u4",
                        "name": "4. Ünite: Hz. Muhammed ve Aile Hayatı",
                        "topics": ["Hz. Muhammed'in Evliliği ve Çocukları", "Peygamberimizin Aile İçi İletişimi", "Akrabalık İlişkileri", "Kevser Suresi"],
                        "page_range": [131, 165]
                    },
                    {
                        "id": "dkab5_u5",
                        "name": "5. Ünite: Çevremizde Dinin İzleri",
                        "topics": ["Mimarimizde Dinin İzleri", "Musikimizde Dinin İzleri", "Edebiyatımızda Dinin İzleri", "Örf ve Adetlerimizde Dinin İzleri"],
                        "page_range": [166, 198]
                    }
                ]
            },
            6: {
                "pdf_pattern": "din-kulturu-ve-ahlak-bilgisi-6sinif",
                "units": [
                    {
                        "id": "dkab6_u1",
                        "name": "1. Ünite: Peygamber ve İlahi Kitap İnancı",
                        "topics": ["İnsanlara Rehber: Peygamber", "Peygamberlerin Nitelikleri", "Vahiy ve İlahi Kitaplar", "Hz. Âdem (a.s.)", "Kunut Duaları"],
                        "page_range": [11, 46]
                    },
                    {
                        "id": "dkab6_u2",
                        "name": "2. Ünite: Namaz",
                        "topics": ["Namazın Anlamı ve Önemi", "Namazın Kılınış Şartları", "Beş Vakit Namaz ve Cemaatle Namaz", "Cuma ve Bayram Namazları", "Fil Suresi"],
                        "page_range": [47, 86]
                    },
                    {
                        "id": "dkab6_u3",
                        "name": "3. Ünite: Zararlı Alışkanlıklar",
                        "topics": ["Zararlı Alışkanlıklardan Korunma Yolları", "Alkol, Kumar ve Bağımlılıklar", "Kul Hakkı", "Tebbet Suresi"],
                        "page_range": [87, 122]
                    },
                    {
                        "id": "dkab6_u4",
                        "name": "4. Ünite: Hz. Muhammed'in Hayatı (Tebliğ ve Davet)",
                        "topics": ["İlk Vahiy ve Gizli Davet", "Açık Davet ve Karşılaşılan Baskılar", "Medine'ye Hicret", "Nasr Suresi"],
                        "page_range": [123, 158]
                    },
                    {
                        "id": "dkab6_u5",
                        "name": "5. Ünite: Temel Değerlerimiz",
                        "topics": ["Vatan ve Millet Sevgisi", "Şehitlik ve Gazilik", "Dini ve Milli Bayramlarımız", "Fatiha Suresi"],
                        "page_range": [159, 189]
                    }
                ]
            },
            7: {
                "pdf_pattern": "din-kulturu-ve-ahlak-bilgisi-7sinif",
                "units": [
                    {
                        "id": "dkab7_u1",
                        "name": "1. Ünite: Melek ve Ahiret İnancı",
                        "topics": ["Varlıklar Âlemi ve Melekler", "Meleklerin Özellikleri ve Görevleri", "Dünya ve Ahiret Hayatı", "Kıyamet ve Yeniden Dirilme", "Nas Suresi"],
                        "page_range": [11, 48]
                    },
                    {
                        "id": "dkab7_u2",
                        "name": "2. Ünite: Hac ve Kurban",
                        "topics": ["Hac İbadeti ve Önemi", "Haccın Yapılışı ve Mekanlar (Kabe, Arafat, Müzdelife)", "Umre İbadeti", "Kurban İbadeti"],
                        "page_range": [49, 90]
                    },
                    {
                        "id": "dkab7_u3",
                        "name": "3. Ünite: Ahlaki Davranışlar",
                        "topics": ["Güzel Ahlaki Tutum ve Davranışlar (Adalet, Dürüstlük, Özdenetim, Sabır, Vatanseverlik)", "Felak Suresi"],
                        "page_range": [91, 132]
                    },
                    {
                        "id": "dkab7_u4",
                        "name": "4. Ünite: İslam Düşüncesinde Yorumlar",
                        "topics": ["Dinin Anlaşılmasında Farklı Yorumlar", "İtikadi ve Fıkhi Yorumlar (Hanefilik, Şafiilik, Malikilik, Hanbelilik)", "Tasavvufi Yorumlar"],
                        "page_range": [133, 172]
                    },
                    {
                        "id": "dkab7_u5",
                        "name": "5. Ünite: Din, Kültür ve Sanat",
                        "topics": ["Kültürümüzde Dinin İzleri", "Mimarimiz ve Hat Sanatı", "Kafirun Suresi"],
                        "page_range": [173, 204]
                    }
                ]
            },
            8: {
                "pdf_pattern": "din-kulturu-ve-ahlak-bilgisi-8sinif",
                "units": [
                    {
                        "id": "dkab8_u1",
                        "name": "1. Ünite: Kader İnancı (LGS Odaklı)",
                        "topics": ["Kader ve Kaza Kavramları", "Evrenin Yasaları (Fiziksel, Biyolojik ve Toplumsal Yasalar)", "İnsanın İradesi ve Kader", "Ömür, Ecel, Tevekkül, Rızık, Sağlık ve Başarı", "Ayet el-Kürsi"],
                        "page_range": [11, 40]
                    },
                    {
                        "id": "dkab8_u2",
                        "name": "2. Ünite: Zekât ve Sadaka (LGS Odaklı)",
                        "topics": ["İslam'ın Paylaşma ve Yardımlaşmaya Verdiği Önem", "Zekât ve Sadaka İbadeti (Nisap, Kimlere Verilir, Hangi Oranlarda Verilir)", "Zekâtın Toplumsal Faydaları", "Maun Suresi"],
                        "page_range": [41, 72]
                    },
                    {
                        "id": "dkab8_u3",
                        "name": "3. Ünite: Din ve Hayat (Zarûrât-ı Diniyye)",
                        "topics": ["Din, Birey ve Toplum", "Dinin Temel Gayesi (Canın, Neslin, Aklın, Malın ve Dinin Korunması)", "Asr Suresi"],
                        "page_range": [73, 100]
                    },
                    {
                        "id": "dkab8_u4",
                        "name": "4. Ünite: Hz. Muhammed'in Örnekliği",
                        "topics": ["Hz. Muhammed'in Doğruluğu ve Güvenilirliği (Muhammedü'l-Emîn)", "Merhameti, Affediciliği ve Hoşgörüsü", "İstişareye Verdiği Önem", "Kureyş Suresi"],
                        "page_range": [101, 126]
                    },
                    {
                        "id": "dkab8_u5",
                        "name": "5. Ünite: Kur'an-ı Kerim ve Özellikleri",
                        "topics": ["İslam Dininin Temel Kaynakları", "Kur'an-ı Kerim'in Ana Konuları (İnanç, İbadet, Ahlak, Kıssalar)", "Kur'an'ın Yol Göstericiliği"],
                        "page_range": [127, 146]
                    }
                ]
            }
        }
    },
    "kuran": {
        "name": "Kur'an-ı Kerim",
        "grades": {
            5: {
                "pdf_pattern": "kuran-i-kerim-5sinif",
                "units": [
                    {
                        "id": "kuran5_u1",
                        "name": "1. Ünite: Kur'an-ı Kerim'i Tanıyorum",
                        "topics": ["Kur'an-ı Kerim'in Özellikleri", "Arap Alfabesi ve Harfler", "Harflerin Mahreçleri (Çıkış Yerleri)", "Kalın ve İnce Harfler"],
                        "page_range": [11, 48]
                    },
                    {
                        "id": "kuran5_u2",
                        "name": "2. Ünite: Harflerin Okunuşu ve Harekeler",
                        "topics": ["Üstün, Esre, Ötre Harekeleri", "Cezm (Sükun) ve Şedde", "Tenvin (İki Üstün, İki Esre, İki Ötre)", "Kelimeleri Birleştirerek Okuma"],
                        "page_range": [49, 94]
                    },
                    {
                        "id": "kuran5_u3",
                        "name": "3. Ünite: Uzatma (Med) Harfleri",
                        "topics": ["Elif, Vav, Ya Harfleriyle Uzatma", "Medd-i Tabiî Kavramı ve Uygulanışı", "Fatiha Suresi Ezberi ve Meali"],
                        "page_range": [95, 138]
                    },
                    {
                        "id": "kuran5_u4",
                        "name": "4. Ünite: Sureler ve Dualar",
                        "topics": ["İhlas Suresi ve Meali", "Felak ve Nas Sureleri", "Sübhaneke ve Salavat Duaları"],
                        "page_range": [139, 173]
                    }
                ]
            },
            6: {
                "pdf_pattern": "kuran-i-kerim-6sinif",
                "units": [
                    {
                        "id": "kuran6_u1",
                        "name": "1. Ünite: Kur'an-ı Kerim'in İndiriliş Süreci",
                        "topics": ["Vahyin Başlangıcı", "Ayet ve Sure Kavramları", "Mushaf Haline Getirilmesi ve Çoğaltılması"],
                        "page_range": [11, 44]
                    },
                    {
                        "id": "kuran6_u2",
                        "name": "2. Ünite: Tecvid Kuralları I (Medler)",
                        "topics": ["Med Sebepleri (Hemze ve Sükun)", "Medd-i Muttasıl (Bitişik Uzatma)", "Medd-i Munfasıl (Ayrık Uzatma)", "Medd-i Lâzım ve Medd-i Ârız"],
                        "page_range": [45, 96]
                    },
                    {
                        "id": "kuran6_u3",
                        "name": "3. Ünite: Tecvid Kuralları II (Nun-ı Sakin ve Tenvin)",
                        "topics": ["İhfa Kuralı ve Harfleri", "İzhar Kuralı ve Harfleri", "İklab Kuralı (M harfine dönüşüm)", "İdgam-ı Meal Gunne ve Bila Gunne"],
                        "page_range": [97, 138]
                    },
                    {
                        "id": "kuran6_u4",
                        "name": "4. Ünite: Sure Mealleri ve Kıssalar",
                        "topics": ["Kevser Suresi Okunuşu, Tecvidi ve Meali", "Kafirun Suresi", "Nasr Suresi", "Hz. İbrahim'in Kıssası"],
                        "page_range": [139, 173]
                    }
                ]
            },
            7: {
                "pdf_pattern": "kuran-i-kerim-7sinif",
                "units": [
                    {
                        "id": "kuran7_u1",
                        "name": "1. Ünite: Kur'an Okuma Adabı ve Fazileti",
                        "topics": ["Tertil Üzere Okumak", "Huşu ve Anlayarak Okuma", "Kur'an'a Karşı Görevlerimiz"],
                        "page_range": [11, 46]
                    },
                    {
                        "id": "kuran7_u2",
                        "name": "2. Ünite: İleri Tecvid Kuralları",
                        "topics": ["Kalkale (Kaf, Tı, Be, Cim, Dal harfleri)", "Ra Harfinin Kalın ve İnce Okunduğu Yerler", "Lafzatullah (Allah lafzındaki Lam'ın hükmü)", "Zamir ve Hükm-ü Ra"],
                        "page_range": [47, 98]
                    },
                    {
                        "id": "kuran7_u3",
                        "name": "3. Ünite: İdgam Çeşitleri",
                        "topics": ["İdgam-ı Misleyn", "İdgam-ı Mütecaniseyn", "İdgam-ı Mütekaribeyn", "Mim-i Sakin Halleri (İhfa, İdgam, İzhar)"],
                        "page_range": [99, 142]
                    },
                    {
                        "id": "kuran7_u4",
                        "name": "4. Ünite: Sure Analizleri",
                        "topics": ["Maun Suresi ve Toplumsal Mesajı", "Fil ve Kureyş Sureleri", "Tebbet Suresi"],
                        "page_range": [143, 177]
                    }
                ]
            },
            8: {
                "pdf_pattern": "kuran-i-kerim-8sinif",
                "units": [
                    {
                        "id": "kuran8_u1",
                        "name": "1. Ünite: Kur'an-ı Kerim'in Ana Mesajları",
                        "topics": ["Tevhid İnancı", "Ahlak ve İbadet Bütünlüğü", "Adalet ve İhsan İlkeleri"],
                        "page_range": [11, 38]
                    },
                    {
                        "id": "kuran8_u2",
                        "name": "2. Ünite: Vakıf (Durak) İşaretleri ve Usulleri",
                        "topics": ["Secavend (Vakıf) İşaretleri (Mim, Tı, Cim, Ze, Sad, Lâ)", "Vakıf Yapma Kuralları (Sükun ile, İki Üstün ile, Te-i Merbuta ile)", "Vasl (Geçiş) Kuralları"],
                        "page_range": [39, 68]
                    },
                    {
                        "id": "kuran8_u3",
                        "name": "3. Ünite: Sure Mealleri ve Kavramsal Çıkarımlar",
                        "topics": ["İnşirah Suresi ve Zorlukla Beraber Kolaylık İlkesi", "Tin Suresi ve İnsanın Yaratılışı", "Kadir Suresi ve Vahyin Kıymeti", "Zilzal Suresi ve Hesap Şuuru"],
                        "page_range": [69, 96]
                    },
                    {
                        "id": "kuran8_u4",
                        "name": "4. Ünite: Kur'an'dan Dualar ve Hayatımıza Yansımaları",
                        "topics": ["Peygamberlerin Kur'an'daki Duaları", "Bağışlanma ve Şükür Bilinci", "Kur'an Ahlakı"],
                        "page_range": [97, 116]
                    }
                ]
            }
        }
    },
    "siyer": {
        "name": "Peygamberimizin Hayatı",
        "grades": {
            5: {
                "pdf_pattern": "peygamberimizin-hayati-5sinif",
                "units": [
                    {
                        "id": "siyer5_u1",
                        "name": "1. Ünite: Peygamberimizin Doğumu ve Çocukluğu",
                        "topics": ["Doğduğu Çevre ve Dönem", "Ailesi ve Sütanne Yılları", "Dedesi ve Amcası Himayesinde Geçen Yıllar", "Şam Ticaret Kervanı"],
                        "page_range": [11, 45]
                    },
                    {
                        "id": "siyer5_u2",
                        "name": "2. Ünite: Gençlik Yılları ve Erdemlilik",
                        "topics": ["Hilfü'l-Fudûl (Erdemliler Topluluğu) ve Adalet Arayışı", "Muhammedü'l-Emîn Sıfatı", "Hz. Hatice ile Evliliği ve Aile Hayatı"],
                        "page_range": [46, 80]
                    },
                    {
                        "id": "siyer5_u3",
                        "name": "3. Ünite: Peygamberimizin Aile İçi Ahlakı",
                        "topics": ["Eş Olarak Peygamberimiz", "Baba ve Dede Olarak Peygamberimiz", "Akraba ve Komşu Haklarına Verdiği Önem"],
                        "page_range": [81, 114]
                    },
                    {
                        "id": "siyer5_u4",
                        "name": "4. Ünite: Peygamberimizin Nezaket ve Merhameti",
                        "topics": ["Çocuklara Karşı Şefkati", "Yetimleri ve Kimsesizleri Koruması", "Hayvanlara ve Doğaya Sevgisi"],
                        "page_range": [115, 143]
                    }
                ]
            },
            6: {
                "pdf_pattern": "peygamberimizin-hayati-6sinif",
                "units": [
                    {
                        "id": "siyer6_u1",
                        "name": "1. Ünite: Mekke Dönemi ve Vahiy",
                        "topics": ["Hira Mağarası ve İlk Vahiy", "Yakın Çevreye Gizli Davet (İlk Müslümanlar)", "Açık Davet ve Safa Tepesi Çağrısı", "Müşriklerin Baskı ve Boykot Dönemi"],
                        "page_range": [11, 48]
                    },
                    {
                        "id": "siyer6_u2",
                        "name": "2. Ünite: Habeşistan Hicreti ve Hüzün Yılı",
                        "topics": ["Habeşistan'a Hicret ve Necaşi ile Diyalog", "Hüzün Yılı (Hz. Hatice ve Ebu Talib'in Vefatı)", "Taif Seferi ve Peygamberimizin Duası", "İsra ve Miraç Mucizesi"],
                        "page_range": [49, 86]
                    },
                    {
                        "id": "siyer6_u3",
                        "name": "3. Ünite: Akabe Biatları ve Hicret",
                        "topics": ["1. ve 2. Akabe Biatları", "Medine'ye Hicret Yolculuğu ve Sevr Mağarası", "Kuba Mescidi ve Mescid-i Nebevî'nin İnşası"],
                        "page_range": [87, 122]
                    },
                    {
                        "id": "siyer6_u4",
                        "name": "4. Ünite: Medine'de Toplumsal Kardeşlik",
                        "topics": ["Muâhât (Ensar-Muhacir Kardeşliği)", "Medine Sözleşmesi ve Birlikte Yaşama Kültürü", "Ezanın Meşru Kılınması"],
                        "page_range": [123, 154]
                    }
                ]
            },
            7: {
                "pdf_pattern": "peygamberimizin-hayati-7sinif",
                "units": [
                    {
                        "id": "siyer7_u1",
                        "name": "1. Ünite: Medine Dönemi ve Mücadeleler",
                        "topics": ["Bedir Savaşı ve Esirlere Muamele (Eğitim Karşılığı Özgürlük)", "Uhud Savaşı ve İstişarenin Önemi / Okçular Tepesi Dersi", "Hendek Savaşı ve Selman-ı Farisi'nin İstişare Önerisi"],
                        "page_range": [11, 52]
                    },
                    {
                        "id": "siyer7_u2",
                        "name": "2. Ünite: Hudeybiye Barışı ve Mekke'nin Fethi",
                        "topics": ["Hudeybiye Antlaşması ve Zafer Boyutu", "Mekke'nin Kansız Fethi", "Peygamberimizin Genel Af İlanı ve Merhameti", "Kabe'nin Putlardan Temizlenmesi"],
                        "page_range": [53, 94]
                    },
                    {
                        "id": "siyer7_u3",
                        "name": "3. Ünite: Veda Haccı ve Veda Hutbesi",
                        "topics": ["Veda Haccı", "Veda Hutbesi'ndeki Evrensel İnsan Hakları İlkeleri (Can, Mal, Kadın Hakları, Irkçılığın Reddi)", "Peygamberimizin Vefatı"],
                        "page_range": [95, 126]
                    },
                    {
                        "id": "siyer7_u4",
                        "name": "4. Ünite: Örnek Sahabeler",
                        "topics": ["Hz. Ebu Bekir, Hz. Ömer, Hz. Osman, Hz. Ali'nin Hayatları ve Erdemleri", "Genç Sahabeler (Mus'ab b. Umeyr, Usame b. Zeyd, Muaz b. Cebel)"],
                        "page_range": [127, 153]
                    }
                ]
            },
            8: {
                "pdf_pattern": "peygamberimizin-hayati-8sinif",
                "units": [
                    {
                        "id": "siyer8_u1",
                        "name": "1. Ünite: Peygamberimizin Şahsiyeti ve İletişimi",
                        "topics": ["Muhammedü'l-Emîn: Güvenilir İnsan Modeli", "Affediciliği ve İntikamdan Uzak Duruşu", "Muhatabına Değer Verme ve Tebessüm Dili"],
                        "page_range": [11, 42]
                    },
                    {
                        "id": "siyer8_u2",
                        "name": "2. Ünite: Peygamberimizin İstişare ve Adalet İlkesi",
                        "topics": ["Karar Alma Süreçlerinde İstişare (Şûra) Mantığı", "Hukuk Önünde Eşitlik (Fatıma Hadisi)", "Ahde Vefa ve Sözünde Durma"],
                        "page_range": [43, 76]
                    },
                    {
                        "id": "siyer8_u3",
                        "name": "3. Ünite: Peygamberimizin İlim ve Eğitime Verdiği Önem",
                        "topics": ["Suffe Mektebi ve Eğitimin Yaygınlaştırılması", "Kadınların Eğitimine Verilen Önem", "İlmin Amelle Bütünleşmesi"],
                        "page_range": [77, 108]
                    },
                    {
                        "id": "siyer8_u4",
                        "name": "4. Ünite: Günümüz Dünyasında Sünnetin Rehberliği",
                        "topics": ["Sünnetin Anlaşılması ve Yorumlanması", "İsraf Karşıtlığı ve Çevre Bilinci", "Modern Çağın Sorunlarına Nebevî Çözümler"],
                        "page_range": [109, 140]
                    }
                ]
            }
        }
    }
}

def load_curriculum_dict() -> dict:
    """custom_curriculum.json varsa oradan yükler, yoksa varsayılanı döndürür."""
    if CUSTOM_CURRICULUM_PATH.exists():
        try:
            with open(CUSTOM_CURRICULUM_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                # JSON anahtarlarındaki string sayıları (örn "5") int'e çevir
                for subj, sdata in data.items():
                    if "grades" in sdata:
                        int_grades = {}
                        for g_str, g_data in sdata["grades"].items():
                            int_grades[int(g_str)] = g_data
                        sdata["grades"] = int_grades
                return data
        except Exception as e:
            print(f"Error loading custom curriculum: {e}")
    return DEFAULT_CURRICULUM

def save_curriculum_dict(curriculum_data: dict):
    """Müfredat değişikliklerini custom_curriculum.json dosyasına kaydeder."""
    with open(CUSTOM_CURRICULUM_PATH, "w", encoding="utf-8") as f:
        json.dump(curriculum_data, f, ensure_ascii=False, indent=2)

def reset_curriculum_to_default():
    """Öğretmen sıfırlamak isterse özel dosyayı silip varsayılan MEB kütüphanesine döner."""
    if CUSTOM_CURRICULUM_PATH.exists():
        CUSTOM_CURRICULUM_PATH.unlink()

# Canlı referans
CURRICULUM = load_curriculum_dict()

def get_subjects():
    curr = load_curriculum_dict()
    return [{"id": k, "name": v["name"]} for k, v in curr.items()]

def get_grades(subject_id: str):
    curr = load_curriculum_dict()
    if subject_id in curr:
        return list(curr[subject_id]["grades"].keys())
    return [5, 6, 7, 8]

def get_units(subject_id: str, grade: int):
    curr = load_curriculum_dict()
    grade = int(grade)
    if subject_id in curr and grade in curr[subject_id]["grades"]:
        return curr[subject_id]["grades"][grade]["units"]
    return []

def get_pdf_filename(subject_id: str, grade: int):
    curr = load_curriculum_dict()
    grade = int(grade)
    if subject_id in curr and grade in curr[subject_id]["grades"]:
        return curr[subject_id]["grades"][grade]["pdf_pattern"]
    return None


# ==============================================================================
# MEB SENARYO ŞABLONLARI VE YÖNETİM SİSTEMİ (KOCAELİ / DARICA İHO VARSAYILAN ŞABLONU)
# Öğretmen tarafından özelleştirilebilir, konularla ilişkilendirilebilir ve sıfırlanabilir.
# ==============================================================================

DEFAULT_SCENARIOS_PATH = DATA_DIR / "meb_scenarios_default.json"
CUSTOM_SCENARIOS_PATH = DATA_DIR / "custom_scenarios.json"

SUBJECT_TO_COURSE_PREFIX = {
    "dkab": "DKAB",
    "siyer": "SIYER",
    "kuran": "KURAN"
}

COURSE_PREFIX_TO_SUBJECT = {
    "DKAB": "dkab",
    "SIYER": "siyer",
    "KURAN": "kuran"
}

DEFAULT_MEB_SCENARIOS = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "metadata": {
        "academic_year": "2026-2027",
        "institution_type": "İmam Hatip Ortaokulu (İHO)",
        "location": {
            "province": "Kocaeli",
            "district": "Darıca"
        },
        "description": "MEB ÖDSGM ve Kocaeli ÖDM Konu Soru Dağılım Tablolarında yer alan tüm resmi alternatif senaryolar (Senaryo 1, 2, 3 vb.)",
        "version": "3.0.0"
    },
    "levels": [
        {
            "grade": 5,
            "courses": [
                {
                    "course_code": "DKAB-5",
                    "course_name": "Din Kültürü ve Ahlak Bilgisi",
                    "terms": [
                        {
                            "term": "1. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Dengeli Dağılım)",
                                    "total_questions": 6,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Allah İnancı",
                                            "outcome_code": "DKAB.5.1.1",
                                            "outcome_description": "Evrendeki mükemmel düzen ile Allah'ın varlığı ve birliği arasında ilişki kurar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Allah İnancı",
                                            "outcome_code": "DKAB.5.1.2",
                                            "outcome_description": "Allah'ın (c.c.) isim ve sıfatlarının anlamlarını açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Allah İnancı",
                                            "outcome_code": "DKAB.5.1.4",
                                            "outcome_description": "Dua ile ilgili ayet ve hadislerden hareketle duanın anlamını ve önemini yorumlar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Allah İnancı",
                                            "outcome_code": "DKAB.5.1.6",
                                            "outcome_description": "İhlas suresini anlamıyla birlikte analiz eder.",
                                            "question_count": 1
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Kavram ve Sıfat Odaklı)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Allah İnancı",
                                            "outcome_code": "DKAB.5.1.1",
                                            "outcome_description": "Evrendeki mükemmel düzen ile Allah'ın varlığı ve birliği arasında ilişki kurar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Allah İnancı",
                                            "outcome_code": "DKAB.5.1.2",
                                            "outcome_description": "Allah'ın (c.c.) isim ve sıfatlarının anlamlarını açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Allah İnancı",
                                            "outcome_code": "DKAB.5.1.4",
                                            "outcome_description": "Dua ile ilgili ayet ve hadislerden hareketle duanın önemini kavrar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Allah İnancı",
                                            "outcome_code": "DKAB.5.1.6",
                                            "outcome_description": "İhlas suresini ve mesajını açıklar.",
                                            "question_count": 1
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 3,
                                    "name": "Senaryo 3 (Çıkarım ve Muhakeme Odaklı)",
                                    "total_questions": 7,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Allah İnancı",
                                            "outcome_code": "DKAB.5.1.1",
                                            "outcome_description": "Evrendeki mükemmel düzen ile Allah'ın varlığı ve birliği arasında ilişki kurar.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Allah İnancı",
                                            "outcome_code": "DKAB.5.1.2",
                                            "outcome_description": "Allah'ın (c.c.) isim ve sıfatlarının anlamlarını açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Allah İnancı",
                                            "outcome_code": "DKAB.5.1.4",
                                            "outcome_description": "Duanın anlamını ve önemini yorumlar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Allah İnancı",
                                            "outcome_code": "DKAB.5.1.6",
                                            "outcome_description": "İhlas suresini anlamıyla birlikte analiz eder.",
                                            "question_count": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "term": "2. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Oruç ve Adap Dengeli)",
                                    "total_questions": 6,
                                    "items": [
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Ramazan ve Oruç",
                                            "outcome_code": "DKAB.5.2.1",
                                            "outcome_description": "Ramazan ayı ve orucun önemini ayet ve hadislerle açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Ramazan ve Oruç",
                                            "outcome_code": "DKAB.5.2.2",
                                            "outcome_description": "Ramazan ve oruçla ilgili temel kavramları açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Adap ve Nezaket",
                                            "outcome_code": "DKAB.5.3.1",
                                            "outcome_description": "Toplumsal hayatta nezaket kurallarına uymanın önemini fark eder.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Adap ve Nezaket",
                                            "outcome_code": "DKAB.5.3.4",
                                            "outcome_description": "Tahiyyat duasını okur ve anlamını açıklar.",
                                            "question_count": 1
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Kavramsal Ağırlıklı)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Ramazan ve Oruç",
                                            "outcome_code": "DKAB.5.2.1",
                                            "outcome_description": "Ramazan ayı ve orucun önemini açıklar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Ramazan ve Oruç",
                                            "outcome_code": "DKAB.5.2.2",
                                            "outcome_description": "Ramazan ve oruçla ilgili temel kavramları (sahur, iftar, fitre) açıklar.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Adap ve Nezaket",
                                            "outcome_code": "DKAB.5.3.1",
                                            "outcome_description": "Nezaket kurallarının önemini fark eder.",
                                            "question_count": 1
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "course_code": "SIYER-5",
                    "course_name": "Peygamberimizin Hayatı",
                    "terms": [
                        {
                            "term": "1. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Standart Kronoloji)",
                                    "total_questions": 6,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Peygamberimizin Çocukluk Yılları",
                                            "outcome_code": "SIYER.5.1.1",
                                            "outcome_description": "İslam öncesi Arap Yarımadası'nın dini ve sosyal durumunu açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Peygamberimizin Çocukluk Yılları",
                                            "outcome_code": "SIYER.5.1.2",
                                            "outcome_description": "Peygamberimizin ailesini ve sütanneye veriliş sürecini açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Peygamberimizin Çocukluk Yılları",
                                            "outcome_code": "SIYER.5.1.3",
                                            "outcome_description": "Dedesi ve amcası yanındaki çocukluk dönemine ait olayları değerlendirir.",
                                            "question_count": 2
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Aile ve Sosyal Çevre)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Peygamberimizin Çocukluk Yılları",
                                            "outcome_code": "SIYER.5.1.1",
                                            "outcome_description": "Cahiliye dönemi adet ve inançlarını açıklar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Peygamberimizin Çocukluk Yılları",
                                            "outcome_code": "SIYER.5.1.2",
                                            "outcome_description": "Peygamberimizin ailesini ve soyunu açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Peygamberimizin Çocukluk Yılları",
                                            "outcome_code": "SIYER.5.1.3",
                                            "outcome_description": "Çocukluk yıllarındaki erdemli davranışlarını açıklar.",
                                            "question_count": 2
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "term": "2. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Aile ve Çocukluk İlişkileri)",
                                    "total_questions": 6,
                                    "items": [
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Peygamberimiz ve Ailesi",
                                            "outcome_code": "SIYER.5.3.1",
                                            "outcome_description": "Aile fertlerine karşı şefkatli tutumunu örneklerle açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Peygamberimiz ve Ailesi",
                                            "outcome_code": "SIYER.5.3.2",
                                            "outcome_description": "Çocukları ve torunlarıyla ilişkisini tahlil eder.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 4,
                                            "unit_title": "Peygamberimiz ve Arkadaşları",
                                            "outcome_code": "SIYER.5.4.1",
                                            "outcome_description": "Çocuk sahabilere olan yaklaşımını açıklar.",
                                            "question_count": 2
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Örnek Davranışlar)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Peygamberimiz ve Ailesi",
                                            "outcome_code": "SIYER.5.3.1",
                                            "outcome_description": "Aile fertlerine karşı şefkatli tutumunu açıklar.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 4,
                                            "unit_title": "Peygamberimiz ve Arkadaşları",
                                            "outcome_code": "SIYER.5.4.1",
                                            "outcome_description": "Çocuk sahabilere olan yaklaşımını analiz eder.",
                                            "question_count": 2
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "course_code": "KURAN-5",
                    "course_name": "Kur'an-ı Kerim",
                    "terms": [
                        {
                            "term": "1. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Kavram ve Genel Bilgi)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kur'an-ı Kerim'i Tanıyalım",
                                            "outcome_code": "KURAN.5.1.1",
                                            "outcome_description": "Vahiy kavramını ve indiriliş sürecini açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kur'an-ı Kerim'i Tanıyalım",
                                            "outcome_code": "KURAN.5.1.2",
                                            "outcome_description": "Ayet, sure ve cüz kavramlarını tanımlar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kur'an-ı Kerim'i Tanıyalım",
                                            "outcome_code": "KURAN.5.1.3",
                                            "outcome_description": "Kur'an okumanın ve anlamanın önemini değerlendirir.",
                                            "question_count": 1
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Tanım ve Yapı Odaklı)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kur'an-ı Kerim'i Tanıyalım",
                                            "outcome_code": "KURAN.5.1.1",
                                            "outcome_description": "Vahiy kavramını açıklar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kur'an-ı Kerim'i Tanıyalım",
                                            "outcome_code": "KURAN.5.1.2",
                                            "outcome_description": "Ayet, sure ve cüz kavramlarını tanımlar ve özelliklerini yazar.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kur'an-ı Kerim'i Tanıyalım",
                                            "outcome_code": "KURAN.5.1.3",
                                            "outcome_description": "Kur'an okumanın önemini belirtir.",
                                            "question_count": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "term": "2. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Kural ve Uygulama)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Kur'an Okumaya Giriş",
                                            "outcome_code": "KURAN.5.2.3",
                                            "outcome_description": "Cezm, şedde ve tenvin kurallarını ayırt eder.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Ezber Dualar / Sureler",
                                            "outcome_code": "KURAN.5.3.1",
                                            "outcome_description": "Fil ve Kureyş surelerinin temel mesajını kavrar.",
                                            "question_count": 2
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Sure Anlam Odaklı)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Kur'an Okumaya Giriş",
                                            "outcome_code": "KURAN.5.2.3",
                                            "outcome_description": "Harekelerin ve işaretlerin işlevini açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Ezber Dualar / Sureler",
                                            "outcome_code": "KURAN.5.3.1",
                                            "outcome_description": "Fil suresinin ana konusunu ve mesajını açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Ezber Dualar / Sureler",
                                            "outcome_code": "KURAN.5.3.2",
                                            "outcome_description": "Kureyş suresinin ana mesajını özetler.",
                                            "question_count": 1
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "grade": 6,
            "courses": [
                {
                    "course_code": "DKAB-6",
                    "course_name": "Din Kültürü ve Ahlak Bilgisi",
                    "terms": [
                        {
                            "term": "1. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Peygamber ve Kitap İnancı)",
                                    "total_questions": 6,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Peygamber ve İlahi Kitap İnancı",
                                            "outcome_code": "DKAB.6.1.1",
                                            "outcome_description": "Peygamberlik kavramını açıklar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Peygamber ve İlahi Kitap İnancı",
                                            "outcome_code": "DKAB.6.1.2",
                                            "outcome_description": "Peygamberlerin sıfatlarını ve görevlerini örneklerle açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Peygamber ve İlahi Kitap İnancı",
                                            "outcome_code": "DKAB.6.1.3",
                                            "outcome_description": "İlahi kitapları ve peygamberlerini eşleştirir.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Peygamber ve İlahi Kitap İnancı",
                                            "outcome_code": "DKAB.6.1.5",
                                            "outcome_description": "Asr suresini ve mesajını tahlil eder.",
                                            "question_count": 1
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Sıfat ve Sure Odaklı)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Peygamber ve İlahi Kitap İnancı",
                                            "outcome_code": "DKAB.6.1.2",
                                            "outcome_description": "Peygamberlerin sıfatlarını (sıdk, emanet, fetanet, ismet, tebliğ) açıklar.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Peygamber ve İlahi Kitap İnancı",
                                            "outcome_code": "DKAB.6.1.3",
                                            "outcome_description": "İlahi kitapların temel mesajlarını açıklar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Peygamber ve İlahi Kitap İnancı",
                                            "outcome_code": "DKAB.6.1.5",
                                            "outcome_description": "Asr suresinin ana mesajını açıklar.",
                                            "question_count": 1
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 3,
                                    "name": "Senaryo 3 (Detaylı Analiz)",
                                    "total_questions": 7,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Peygamber ve İlahi Kitap İnancı",
                                            "outcome_code": "DKAB.6.1.1",
                                            "outcome_description": "Peygamber ve elçi kavramlarını açıklar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Peygamber ve İlahi Kitap İnancı",
                                            "outcome_code": "DKAB.6.1.2",
                                            "outcome_description": "Peygamberlerin sıfatlarını ve görevlerini açıklar.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Peygamber ve İlahi Kitap İnancı",
                                            "outcome_code": "DKAB.6.1.3",
                                            "outcome_description": "Dört büyük kitap ve suhuf verilen peygamberleri listeler.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Peygamber ve İlahi Kitap İnancı",
                                            "outcome_code": "DKAB.6.1.5",
                                            "outcome_description": "Asr suresini analiz eder.",
                                            "question_count": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "term": "2. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Namaz ve Temizlik)",
                                    "total_questions": 6,
                                    "items": [
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Namaz",
                                            "outcome_code": "DKAB.6.2.1",
                                            "outcome_description": "İslam'da namaz ibadetinin önemini açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Namaz",
                                            "outcome_code": "DKAB.6.2.2",
                                            "outcome_description": "Namazın şartlarını ve rükünlerini açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Namaz",
                                            "outcome_code": "DKAB.6.2.3",
                                            "outcome_description": "Abdest, boy abdesti ve teyemmümün yapılışını açıklar.",
                                            "question_count": 2
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Namazın Farzları Odaklı)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Namaz",
                                            "outcome_code": "DKAB.6.2.1",
                                            "outcome_description": "Namaz ibadetinin önemini açıklar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Namaz",
                                            "outcome_code": "DKAB.6.2.2",
                                            "outcome_description": "Namazın içindeki ve dışındaki farzları açıklar.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Namaz",
                                            "outcome_code": "DKAB.6.2.3",
                                            "outcome_description": "Abdestin farzlarını listeler.",
                                            "question_count": 1
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "course_code": "SIYER-6",
                    "course_name": "Peygamberimizin Hayatı",
                    "terms": [
                        {
                            "term": "1. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Erdem ve Tebliğ)",
                                    "total_questions": 6,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Gençlik Yılları ve Mekke",
                                            "outcome_code": "SIYER.6.1.1",
                                            "outcome_description": "Hilfu'l-Fudul cemiyetindeki rolünü açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Mekke Dönemi",
                                            "outcome_code": "SIYER.6.1.2",
                                            "outcome_description": "İlk vahyin geliş sürecini özetler.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Mekke Dönemi",
                                            "outcome_code": "SIYER.6.1.3",
                                            "outcome_description": "Gizli ve açık davet sürecinde karşılaşılan zorlukları yorumlar.",
                                            "question_count": 2
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (İlk Vahiy ve Zorluklar)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Mekke Dönemi",
                                            "outcome_code": "SIYER.6.1.1",
                                            "outcome_description": "Gençlik yıllarındaki ahlakını açıklar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Mekke Dönemi",
                                            "outcome_code": "SIYER.6.1.2",
                                            "outcome_description": "Hira mağarasındaki ilk vahiy sürecini açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Mekke Dönemi",
                                            "outcome_code": "SIYER.6.1.3",
                                            "outcome_description": "Müşriklerin uyguladığı boykot ve baskıları değerlendirir.",
                                            "question_count": 2
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "term": "2. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Medine Dönemi ve Mücadele)",
                                    "total_questions": 6,
                                    "items": [
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Medine Dönemi",
                                            "outcome_code": "SIYER.6.3.1",
                                            "outcome_description": "Ensar ve Muhacir kardeşliğini açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Medine Dönemi",
                                            "outcome_code": "SIYER.6.3.2",
                                            "outcome_description": "Bedir, Uhud ve Hendek gazvelerinin temel sebeplerini ve sonuçlarını açıklar.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Medine Dönemi",
                                            "outcome_code": "SIYER.6.3.4",
                                            "outcome_description": "Hudeybiye Barış Antlaşması'nın önemini değerlendirir.",
                                            "question_count": 1
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Gazveler ve Antlaşmalar)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Medine Dönemi",
                                            "outcome_code": "SIYER.6.3.1",
                                            "outcome_description": "Muahat uygulamasını açıklar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Medine Dönemi",
                                            "outcome_code": "SIYER.6.3.2",
                                            "outcome_description": "Uhud ve Hendek savaşlarının ibretlik yönlerini tahlil eder.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Medine Dönemi",
                                            "outcome_code": "SIYER.6.3.4",
                                            "outcome_description": "Hudeybiye Antlaşması maddelerini değerlendirir.",
                                            "question_count": 2
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "course_code": "KURAN-6",
                    "course_name": "Kur'an-ı Kerim",
                    "terms": [
                        {
                            "term": "1. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Temel İlkeler ve Med-i Tabiî)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kur'an'ın Temel Özellikleri",
                                            "outcome_code": "KURAN.6.1.1",
                                            "outcome_description": "Kur'an'ın rehber olma özelliğini açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Tecvid Kuralları",
                                            "outcome_code": "KURAN.6.1.2",
                                            "outcome_description": "Medd-i Tabiî kuralını uygular ve açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Sure Tanıma",
                                            "outcome_code": "KURAN.6.1.3",
                                            "outcome_description": "Ayetü'l-Kürsi'nin temel mesajlarını listeler.",
                                            "question_count": 1
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Tecvid Odaklı)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kur'an'ın Temel Özellikleri",
                                            "outcome_code": "KURAN.6.1.1",
                                            "outcome_description": "Kur'an'ın evrensel mesajlarını açıklar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Tecvid Kuralları",
                                            "outcome_code": "KURAN.6.1.2",
                                            "outcome_description": "Medd-i Tabiî kuralına örnek kelimeler verir.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Sure Tanıma",
                                            "outcome_code": "KURAN.6.1.3",
                                            "outcome_description": "Fatiha suresinin anlamını açıklar.",
                                            "question_count": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "term": "2. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Med Çeşitleri ve Kıssalar)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Tecvid Kuralları",
                                            "outcome_code": "KURAN.6.3.1",
                                            "outcome_description": "Medd-i Muttasıl ve Medd-i Munfasıl kurallarını ayırt eder.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 4,
                                            "unit_title": "Kıssalar",
                                            "outcome_code": "KURAN.6.4.1",
                                            "outcome_description": "Hz. Zekeriya ve Hz. Yahya kıssalarından dersler çıkarır.",
                                            "question_count": 2
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Kural Ağırlıklı)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Tecvid Kuralları",
                                            "outcome_code": "KURAN.6.3.1",
                                            "outcome_description": "Med çeşitlerini tanımlar ve sebep-harf ilişkisini açıklar.",
                                            "question_count": 4
                                        },
                                        {
                                            "unit_no": 4,
                                            "unit_title": "Kıssalar",
                                            "outcome_code": "KURAN.6.4.1",
                                            "outcome_description": "Hz. Yahya'nın örnek ahlakını açıklar.",
                                            "question_count": 1
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "grade": 7,
            "courses": [
                {
                    "course_code": "DKAB-7",
                    "course_name": "Din Kültürü ve Ahlak Bilgisi",
                    "terms": [
                        {
                            "term": "1. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Varlıklar Âlemi ve Ahiret)",
                                    "total_questions": 6,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Melek ve Ahiret İnancı",
                                            "outcome_code": "DKAB.7.1.1",
                                            "outcome_description": "Varlıklar âlemini sınıflandırarak meleklerin temel özelliklerini açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Melek ve Ahiret İnancı",
                                            "outcome_code": "DKAB.7.1.2",
                                            "outcome_description": "Dört büyük melek ve görevlerini açıklar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Melek ve Ahiret İnancı",
                                            "outcome_code": "DKAB.7.1.3",
                                            "outcome_description": "Dünya hayatı ile ahiret hayatı arasındaki ilişkiyi açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Melek ve Ahiret İnancı",
                                            "outcome_code": "DKAB.7.1.5",
                                            "outcome_description": "Nas suresinin mesajını tahlil eder.",
                                            "question_count": 1
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Ahiret Aşamaları Odaklı)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Melek ve Ahiret İnancı",
                                            "outcome_code": "DKAB.7.1.1",
                                            "outcome_description": "Görülen ve görülmeyen varlıkları ayırt eder.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Melek ve Ahiret İnancı",
                                            "outcome_code": "DKAB.7.1.3",
                                            "outcome_description": "Ahiret hayatının aşamalarını (kıyamet, ba's, haşr, mizan, cennet/cehennem) açıklar.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Melek ve Ahiret İnancı",
                                            "outcome_code": "DKAB.7.1.5",
                                            "outcome_description": "Nas suresini açıklar.",
                                            "question_count": 1
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 3,
                                    "name": "Senaryo 3 (Kapsamlı)",
                                    "total_questions": 7,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Melek ve Ahiret İnancı",
                                            "outcome_code": "DKAB.7.1.1",
                                            "outcome_description": "Meleklerin özelliklerini cin ve şeytandan ayıran yönlerini açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Melek ve Ahiret İnancı",
                                            "outcome_code": "DKAB.7.1.2",
                                            "outcome_description": "Meleklerin görevlerini açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Melek ve Ahiret İnancı",
                                            "outcome_code": "DKAB.7.1.3",
                                            "outcome_description": "Ahiret inancının insan davranışlarına etkisini değerlendirir.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Melek ve Ahiret İnancı",
                                            "outcome_code": "DKAB.7.1.5",
                                            "outcome_description": "Nas suresinin tefsirini özetler.",
                                            "question_count": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "term": "2. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Hac, Umre ve Kurban)",
                                    "total_questions": 6,
                                    "items": [
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Hac ve Umre",
                                            "outcome_code": "DKAB.7.2.1",
                                            "outcome_description": "İslam'da hac ve umre ibadetinin önemini açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Hac ve Umre",
                                            "outcome_code": "DKAB.7.2.2",
                                            "outcome_description": "Hac ile ilgili kavramları (ihram, tavaf, sa'y, vakfe) açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Kurban İbadeti",
                                            "outcome_code": "DKAB.7.2.4",
                                            "outcome_description": "Kurban ibadetinin bireysel ve toplumsal faydalarını değerlendirir.",
                                            "question_count": 2
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Mekânlar ve Kavramlar)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Hac ve Umre",
                                            "outcome_code": "DKAB.7.2.2",
                                            "outcome_description": "Arafat, Müzdelife, Mina ve Kâbe mekanlarının ibadetteki yerini açıklar.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Kurban İbadeti",
                                            "outcome_code": "DKAB.7.2.4",
                                            "outcome_description": "Kurban çeşitlerini (adak, akika vb.) ve hükümlerini açıklar.",
                                            "question_count": 2
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "course_code": "SIYER-7",
                    "course_name": "Peygamberimizin Hayatı",
                    "terms": [
                        {
                            "term": "1. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Hicret ve Medine Düzeni)",
                                    "total_questions": 6,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Hicret",
                                            "outcome_code": "SIYER.7.1.1",
                                            "outcome_description": "Hicretin nedenlerini ve sonuçlarını açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Mescid-i Nebi",
                                            "outcome_code": "SIYER.7.1.2",
                                            "outcome_description": "Mescid-i Nebi'nin inşasını ve toplumsal işlevini (Suffe) açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Medine Sözleşmesi",
                                            "outcome_code": "SIYER.7.1.3",
                                            "outcome_description": "Medine Sözleşmesi'nin bir arada yaşama kültürüne katkısını değerlendirir.",
                                            "question_count": 2
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Kurumsallaşma Odaklı)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Hicret",
                                            "outcome_code": "SIYER.7.1.1",
                                            "outcome_description": "Hicret güzergahı ve Sevr mağarası olayını değerlendirir.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Mescid-i Nebi",
                                            "outcome_code": "SIYER.7.1.2",
                                            "outcome_description": "Suffe ashabı ve eğitimdeki rolünü açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Medine Sözleşmesi",
                                            "outcome_code": "SIYER.7.1.3",
                                            "outcome_description": "Medine Sözleşmesi'nin maddelerini analiz eder.",
                                            "question_count": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "term": "2. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Fetih ve Veda Hutbesi)",
                                    "total_questions": 6,
                                    "items": [
                                        {
                                            "unit_no": 3,
                                            "unit_title": "İslam'ın Yayılışı",
                                            "outcome_code": "SIYER.7.3.1",
                                            "outcome_description": "İslam'a davet mektuplarının amacını açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Mekke'nin Fethi",
                                            "outcome_code": "SIYER.7.3.2",
                                            "outcome_description": "Mekke'nin fethinde gösterilen merhameti ve genel affı yorumlar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 4,
                                            "unit_title": "Veda Haccı ve Hutbesi",
                                            "outcome_code": "SIYER.7.4.1",
                                            "outcome_description": "Veda Hutbesi'ndeki evrensel insan hakları ilkelerini analiz eder.",
                                            "question_count": 2
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Veda Hutbesi İlkeleri)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Mekke'nin Fethi",
                                            "outcome_code": "SIYER.7.3.2",
                                            "outcome_description": "Mekke'nin fethi sürecini ve sonuçlarını açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 4,
                                            "unit_title": "Veda Haccı ve Hutbesi",
                                            "outcome_code": "SIYER.7.4.1",
                                            "outcome_description": "Veda Hutbesi'ndeki can, mal güvenliği ve kadın hakları ilkelerini değerlendirir.",
                                            "question_count": 3
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "course_code": "KURAN-7",
                    "course_name": "Kur'an-ı Kerim",
                    "terms": [
                        {
                            "term": "1. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Ana Konular ve İhfa/İzhar)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kur'an'ın Ana Konuları",
                                            "outcome_code": "KURAN.7.1.1",
                                            "outcome_description": "İnanç, ibadet ve ahlak konularını açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Tecvid Kuralları",
                                            "outcome_code": "KURAN.7.1.2",
                                            "outcome_description": "İhfa ve İzhar kurallarını metin üzerinden gösterir.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Örnek Dualar",
                                            "outcome_code": "KURAN.7.1.3",
                                            "outcome_description": "Rabbena dualarının anlamını açıklar.",
                                            "question_count": 1
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Tecvid Uygulama Odaklı)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kur'an'ın Ana Konuları",
                                            "outcome_code": "KURAN.7.1.1",
                                            "outcome_description": "Kıssaların anlatılış amacını açıklar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Tecvid Kuralları",
                                            "outcome_code": "KURAN.7.1.2",
                                            "outcome_description": "İzhar harflerini ve ihfa harflerini açıklar ve uygular.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Örnek Dualar",
                                            "outcome_code": "KURAN.7.1.3",
                                            "outcome_description": "Rabbena dualarının mesajını yazar.",
                                            "question_count": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "term": "2. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (İdgam Kuralları ve Ashab-ı Kehf)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Tecvid Kuralları",
                                            "outcome_code": "KURAN.7.3.1",
                                            "outcome_description": "İdgam-ı Meal Gunne ve İdgam-ı Bila Gunne kurallarını ayırt eder.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 4,
                                            "unit_title": "Kıssalar",
                                            "outcome_code": "KURAN.7.4.1",
                                            "outcome_description": "Ashab-ı Kehf kıssasından inanç dersleri çıkarır.",
                                            "question_count": 2
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (İdgam Odaklı)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Tecvid Kuralları",
                                            "outcome_code": "KURAN.7.3.1",
                                            "outcome_description": "Sakin nun ve tenvinden sonra gelen harflere göre idgam türlerini açıklar.",
                                            "question_count": 4
                                        },
                                        {
                                            "unit_no": 4,
                                            "unit_title": "Kıssalar",
                                            "outcome_code": "KURAN.7.4.1",
                                            "outcome_description": "Ashab-ı Kehf olayının ana fikrini yazar.",
                                            "question_count": 1
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "grade": 8,
            "courses": [
                {
                    "course_code": "DKAB-8",
                    "course_name": "Din Kültürü ve Ahlak Bilgisi (LGS Seviyesi)",
                    "terms": [
                        {
                            "term": "1. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Kader ve Evrensel Yasalar)",
                                    "total_questions": 6,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kader İnancı",
                                            "outcome_code": "DKAB.8.1.1",
                                            "outcome_description": "Kader ve kaza inancını ayet ve hadislerle açıklar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kader İnancı",
                                            "outcome_code": "DKAB.8.1.2",
                                            "outcome_description": "Külli irade ve cüzi irade ilişkisini kurar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kader İnancı",
                                            "outcome_code": "DKAB.8.1.3",
                                            "outcome_description": "Fiziksel, biyolojik ve toplumsal yasaların özelliklerini analiz eder.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kader İnancı",
                                            "outcome_code": "DKAB.8.1.6",
                                            "outcome_description": "Ayet el-Kürsi'yi okur, anlamını yorumlar.",
                                            "question_count": 1
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Kavram ve Kıssa Odaklı)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kader İnancı",
                                            "outcome_code": "DKAB.8.1.2",
                                            "outcome_description": "Tevekkül, rızık, ecel ve ömür kavramlarını değerlendirir.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kader İnancı",
                                            "outcome_code": "DKAB.8.1.3",
                                            "outcome_description": "Fiziksel ve biyolojik yasaları örnek olaylarla açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kader İnancı",
                                            "outcome_code": "DKAB.8.1.5",
                                            "outcome_description": "Hz. Musa'nın (a.s.) hayatını ana hatlarıyla özetler.",
                                            "question_count": 1
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 3,
                                    "name": "Senaryo 3 (LGS Mantığı / Çok Yönlü Muhakeme)",
                                    "total_questions": 7,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kader İnancı",
                                            "outcome_code": "DKAB.8.1.1",
                                            "outcome_description": "Kader ve kaza kavramlarını ayırt eder.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kader İnancı",
                                            "outcome_code": "DKAB.8.1.2",
                                            "outcome_description": "İnsanın sorumluluğu ve iradesi bağlamında eylemlerini yorumlar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kader İnancı",
                                            "outcome_code": "DKAB.8.1.3",
                                            "outcome_description": "Üç evrensel yasayı (fiziksel, biyolojik, toplumsal) karşılaştırır.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kader İnancı",
                                            "outcome_code": "DKAB.8.1.5",
                                            "outcome_description": "Hz. Musa'nın firavuna karşı mücadelesini açıklar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Kader İnancı",
                                            "outcome_code": "DKAB.8.1.6",
                                            "outcome_description": "Ayet el-Kürsi'nin ana mesajlarını maddeler.",
                                            "question_count": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "term": "2. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Zekat, Sadaka ve Dinin Gayesi)",
                                    "total_questions": 6,
                                    "items": [
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Zekat ve Sadaka",
                                            "outcome_code": "DKAB.8.2.1",
                                            "outcome_description": "İslam'ın yardımlaşmaya verdiği önemi açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Zekat ve Sadaka",
                                            "outcome_code": "DKAB.8.2.2",
                                            "outcome_description": "Zekat oranlarını, nisap miktarını ve verilecek kimseleri açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Din ve Hayat",
                                            "outcome_code": "DKAB.8.3.1",
                                            "outcome_description": "Zarurat-ı Diniyye (can, nesil, akıl, mal, din korunması) ilkelerini açıklar.",
                                            "question_count": 2
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Hesaplama ve Hükümler)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Zekat ve Sadaka",
                                            "outcome_code": "DKAB.8.2.2",
                                            "outcome_description": "Altın, ticaret malı, küçükbaş/büyükbaş hayvan ve toprak ürünleri zekat oranlarını açıklar.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Din ve Hayat",
                                            "outcome_code": "DKAB.8.3.1",
                                            "outcome_description": "Can ve mal emniyetinin İslam'daki yerini açıklar.",
                                            "question_count": 2
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 3,
                                    "name": "Senaryo 3 (Kapsamlı Zekat ve Fıkhi Boyut)",
                                    "total_questions": 7,
                                    "items": [
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Zekat ve Sadaka",
                                            "outcome_code": "DKAB.8.2.1",
                                            "outcome_description": "Yardımlaşmanın toplumsal dayanışmadaki rolünü analiz eder.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Zekat ve Sadaka",
                                            "outcome_code": "DKAB.8.2.2",
                                            "outcome_description": "Zekat ve sadaka-i cariye farkını ve oranlarını açıklar.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Din ve Hayat",
                                            "outcome_code": "DKAB.8.3.1",
                                            "outcome_description": "Temel hakların korunması ilkelerini yorumlar.",
                                            "question_count": 2
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "course_code": "SIYER-8",
                    "course_name": "Peygamberimizin Hayatı",
                    "terms": [
                        {
                            "term": "1. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Adalet, Merhamet ve İstişare)",
                                    "total_questions": 6,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Ahlaki Örneklik",
                                            "outcome_code": "SIYER.8.1.1",
                                            "outcome_description": "Adalet ve dürüstlük anlayışını somut hadiseler üzerinden açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Ahlaki Örneklik",
                                            "outcome_code": "SIYER.8.1.2",
                                            "outcome_description": "Merhametli ve affedici tavrının toplumsal etkilerini açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Ahlaki Örneklik",
                                            "outcome_code": "SIYER.8.1.3",
                                            "outcome_description": "İstişareye verdiği önemi Uhud ve Hendek örnekleriyle analiz eder.",
                                            "question_count": 2
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Örnek Olay Analizi)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Ahlaki Örneklik",
                                            "outcome_code": "SIYER.8.1.1",
                                            "outcome_description": "Hacerü'l-Esved hakemliği üzerinden adaletini açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Ahlaki Örneklik",
                                            "outcome_code": "SIYER.8.1.3",
                                            "outcome_description": "İstişare ilkesinin yönetim ve aile hayatındaki uygulamalarını tahlil eder.",
                                            "question_count": 3
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "term": "2. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Toplumsal Barış ve Sünnet)",
                                    "total_questions": 6,
                                    "items": [
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Peygamberimiz ve Toplum",
                                            "outcome_code": "SIYER.8.3.1",
                                            "outcome_description": "Farklı inanç mensuplarıyla ilişkilerinde adaleti modeller.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Peygamberimiz ve Toplum",
                                            "outcome_code": "SIYER.8.3.2",
                                            "outcome_description": "Genç sahabilerin İslam tebliğindeki rolünü analiz eder.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 4,
                                            "unit_title": "Sünnetin Önemi",
                                            "outcome_code": "SIYER.8.4.1",
                                            "outcome_description": "Sünnetin dinin anlaşılmasındaki yerini değerlendirir.",
                                            "question_count": 2
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Genç Sahabiler ve Sünnet)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Peygamberimiz ve Toplum",
                                            "outcome_code": "SIYER.8.3.2",
                                            "outcome_description": "Hz. Ali, Cafer b. Ebi Talib, Usame b. Zeyd gibi genç sahabilerin görevlerini açıklar.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 4,
                                            "unit_title": "Sünnetin Önemi",
                                            "outcome_code": "SIYER.8.4.1",
                                            "outcome_description": "Kavli, fiili ve takriri sünnet kavramlarını açıklar.",
                                            "question_count": 2
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "course_code": "KURAN-8",
                    "course_name": "Kur'an-ı Kerim",
                    "terms": [
                        {
                            "term": "1. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (İklab, İdgam ve Sure Mesajı)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Anlama ve Yaşama",
                                            "outcome_code": "KURAN.8.1.1",
                                            "outcome_description": "Kur'an'ın ahlaki olgunlaşma amacını açıklar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Tecvid Kuralları",
                                            "outcome_code": "KURAN.8.1.2",
                                            "outcome_description": "İklab ve İdgam (meal-gunne / bila-gunne) kurallarını açıklar ve örnekler.",
                                            "question_count": 3
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Sure Analizi",
                                            "outcome_code": "KURAN.8.1.3",
                                            "outcome_description": "İnşirah suresinin ayetlerinden mesajlar çıkarır.",
                                            "question_count": 1
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Tecvid Uygulama Ağırlıklı)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 1,
                                            "unit_title": "Anlama ve Yaşama",
                                            "outcome_code": "KURAN.8.1.1",
                                            "outcome_description": "Kur'an'ı hayat rehberi edinmenin ilkelerini açıklar.",
                                            "question_count": 1
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Tecvid Kuralları",
                                            "outcome_code": "KURAN.8.1.2",
                                            "outcome_description": "İklab kuralının harfini ve uygulanışını metin üzerinde gösterir.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 2,
                                            "unit_title": "Tecvid Kuralları",
                                            "outcome_code": "KURAN.8.1.2-B",
                                            "outcome_description": "İdgam-ı Meal Gunne ve Bila Gunne örneklerini ayırt eder.",
                                            "question_count": 2
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "term": "2. Dönem",
                            "exam_number": 1,
                            "scenarios": [
                                {
                                    "scenario_id": 1,
                                    "name": "Senaryo 1 (Kalkale, Ra Hükümleri ve Hucurat)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Tecvid Kuralları",
                                            "outcome_code": "KURAN.8.3.1",
                                            "outcome_description": "Kalkale harflerini ve duraklarda okunuşunu açıklar.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Tecvid Kuralları",
                                            "outcome_code": "KURAN.8.3.2",
                                            "outcome_description": "Ra harfinin kalın ve ince okunduğu durumları ayırt eder.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 4,
                                            "unit_title": "Sure Analizi",
                                            "outcome_code": "KURAN.8.4.1",
                                            "outcome_description": "Hucurat suresindeki ahlaki ilkeleri (suizan, tecessüs, gıybet) açıklar.",
                                            "question_count": 1
                                        }
                                    ]
                                },
                                {
                                    "scenario_id": 2,
                                    "name": "Senaryo 2 (Tecvid Kuralları Derinlik)",
                                    "total_questions": 5,
                                    "items": [
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Tecvid Kuralları",
                                            "outcome_code": "KURAN.8.3.1",
                                            "outcome_description": "Kalkale kuralına verilen ayetlerden 3 örnek bulur.",
                                            "question_count": 2
                                        },
                                        {
                                            "unit_no": 3,
                                            "unit_title": "Tecvid Kuralları",
                                            "outcome_code": "KURAN.8.3.2",
                                            "outcome_description": "Ra harfinin hükümleriyle ilgili kaideleri açıklar.",
                                            "question_count": 3
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}

# Varsayılan şablonu referans olarak diskte de bulundur
try:
    if not DEFAULT_SCENARIOS_PATH.exists():
        with open(DEFAULT_SCENARIOS_PATH, "w", encoding="utf-8") as _f:
            json.dump(DEFAULT_MEB_SCENARIOS, _f, ensure_ascii=False, indent=2)
except Exception:
    pass


def load_scenarios_dict() -> dict:
    """custom_scenarios.json varsa oradan yükler, yoksa DEFAULT_MEB_SCENARIOS döndürür."""
    import copy
    if CUSTOM_SCENARIOS_PATH.exists():
        try:
            with open(CUSTOM_SCENARIOS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading custom scenarios: {e}")
    return copy.deepcopy(DEFAULT_MEB_SCENARIOS)


def save_scenarios_dict(scenarios_data: dict):
    """Senaryo değişikliklerini custom_scenarios.json dosyasına kaydeder."""
    with open(CUSTOM_SCENARIOS_PATH, "w", encoding="utf-8") as f:
        json.dump(scenarios_data, f, ensure_ascii=False, indent=2)


def reset_scenarios_to_default():
    """Öğretmen sıfırlamak isterse özel senaryo dosyasını silip varsayılan şablona döner."""
    if CUSTOM_SCENARIOS_PATH.exists():
        CUSTOM_SCENARIOS_PATH.unlink()


def get_scenarios_for(subject_id: str, grade: int, term: str) -> list:
    """Verilen ders (dkab/siyer/kuran), sınıf (5-8) ve dönem (1. Dönem / 2. Dönem) için senaryo listesini döndürür."""
    data = load_scenarios_dict()
    grade = int(grade)
    prefix = SUBJECT_TO_COURSE_PREFIX.get(subject_id, "DKAB")
    target_code = f"{prefix}-{grade}"

    for lvl in data.get("levels", []):
        if int(lvl.get("grade", 0)) == grade:
            for course in lvl.get("courses", []):
                if course.get("course_code") == target_code or course.get("course_code", "").startswith(prefix):
                    for t_obj in course.get("terms", []):
                        if t_obj.get("term") == term:
                            return t_obj.get("scenarios", [])
    return []


def update_scenarios_for(subject_id: str, grade: int, term: str, scenarios_list: list) -> dict:
    """Belirli bir ders, sınıf ve dönemin senaryo listesini günceller ve kaydeder."""
    data = load_scenarios_dict()
    grade = int(grade)
    prefix = SUBJECT_TO_COURSE_PREFIX.get(subject_id, "DKAB")
    target_code = f"{prefix}-{grade}"

    # Her senaryonun total_questions değerini içindeki maddelerin toplamına göre senkronize et
    for sc in scenarios_list:
        items = sc.get("items", [])
        total_q = sum(int(it.get("question_count", 1)) for it in items)
        sc["total_questions"] = total_q if total_q > 0 else int(sc.get("total_questions", 6))

    updated = False
    for lvl in data.get("levels", []):
        if int(lvl.get("grade", 0)) == grade:
            for course in lvl.get("courses", []):
                if course.get("course_code") == target_code or course.get("course_code", "").startswith(prefix):
                    for t_obj in course.get("terms", []):
                        if t_obj.get("term") == term:
                            t_obj["scenarios"] = scenarios_list
                            updated = True
                            break
                    if not updated:
                        course.setdefault("terms", []).append({
                            "term": term,
                            "exam_number": 1,
                            "scenarios": scenarios_list
                        })
                        updated = True
                    break

    save_scenarios_dict(data)
    return data

