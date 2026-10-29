"""
Müfredat, Kazanımlar ve Kitap Sayfa Haritası Modülü
İmam Hatip Ortaokulu 5, 6, 7 ve 8. Sınıf Din Kültürü, Kur'an-ı Kerim ve Peygamberimizin Hayatı
derslerinin 2026 yılı MEB müfredat ünite, tema ve kazanımlarını içerir.
"""

CURRICULUM = {
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

def get_subjects():
    return [
        {"id": k, "name": v["name"]}
        for k, v in CURRICULUM.items()
    ]

def get_grades(subject_id: str):
    if subject_id in CURRICULUM:
        return list(CURRICULUM[subject_id]["grades"].keys())
    return [5, 6, 7, 8]

def get_units(subject_id: str, grade: int):
    grade = int(grade)
    if subject_id in CURRICULUM and grade in CURRICULUM[subject_id]["grades"]:
        return CURRICULUM[subject_id]["grades"][grade]["units"]
    return []

def get_pdf_filename(subject_id: str, grade: int):
    grade = int(grade)
    if subject_id in CURRICULUM and grade in CURRICULUM[subject_id]["grades"]:
        return CURRICULUM[subject_id]["grades"][grade]["pdf_pattern"]
    return None
