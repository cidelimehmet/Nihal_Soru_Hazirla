# Tevfik İleri İmam Hatip Ortaokulu
## MEB 2026 OYSS Soru Hazırlama & Sınav Kağıdı Sistemi

Bu uygulama, Ankara Tevfik İleri İmam Hatip Ortaokulu öğretmenlerimizin MEB ders kitaplarını baz alarak **2026 MEB Ortak Yazılı Sınav Sistemi (OYSS)** ve **Türkiye Yüzyılı Maarif Modeli** standartlarına %100 uyumlu yazılı sınav kağıtları hazırlaması için geliştirilmiştir.

---

### 🚀 Hızlı Başlangıç (Nasıl Çalıştırılır?)

1. **Uygulamayı Başlatma:**
   - Klasör içindeki `baslat.bat` dosyasına çift tıklayın.
   - Sistem arka planda sunucuyu başlatacak ve internet tarayıcınızda otomatik olarak açılacaktır:
     👉 **`http://localhost:8000`**

2. **Giriş Bilgileri:**
   - **Kullanıcı Adı:** `nihal`
   - **Şifre:** `1234`
   *(Ayarlar ekranından veya `.env` dosyasından dilediğiniz zaman değiştirebilirsiniz).*

3. **Google Gemini API Tanımlama (İsteğe Bağlı):**
   - Canlı yapay zeka ile kitaplardan anlık soru üretmek için klasördeki `.env` dosyasına `GEMINI_API_KEY=...` şeklinde anahtarınızı yazabilirsiniz.
   - Veya program açıldığında sağ üstteki **"⚙️ Ayarlar"** butonuna basarak API anahtarınızı yapıştırabilirsiniz.
   - *Not:* API anahtarı girilmediğinde bile sistem MEB 2026 standartlarında zengin pedagojik açık uçlu sorular ve rubrikler üretmeye devam eder.

---

### ✨ Öne Çıkan Özellikler

1. **Tam A4 ve MEB 2 Sütunlu Sayfa Düzeni:**
   - MEB sınav kağıdı standardı olan ortadan dikey çizgili 2 sütun düzeni.
   - İsteğe göre tek sütun veya 2 sütun arasında tek tıkla geçiş imkânı.
   - T.C. Millî Eğitim Bakanlığı ve Tevfik İleri İHL resmi anteti.
   - Öğrenci Adı Soyadı, Sınıf/Şube, No, Tarih ve Not kutuları.

2. **Canlı ve İnteraktif Düzenleme:**
   - Sınav kağıdındaki tüm soru metinlerini doğrudan üzerine tıklayarak değiştirebilirsiniz.
   - Her sorunun puanını kutucuktan değiştirdiğinizde, sağ üstteki **Toplam Puan** otomatik olarak anında yeniden hesaplanır.
   - Beğenmediğiniz soruyu tek tıkla silebilir, yeni soru ekleyebilir veya "🔄 Yenile" butonu ile sadece o soruyu yapay zekaya yeniden ürettirebilirsiniz.

3. **Arapça ve Tecvid Desteği:**
   - Kur'an-ı Kerim dersi için Arapça ayetler ve tecvidli kelimeler net, okunaklı, büyük ve tam harekeli olarak sunulur.

4. **Dereceli Puanlama Anahtarı (Rubrik):**
   - "🔑 Cevap Anahtarı & Rubrik" sekmesinde her sorunun çözümünün yanı sıra öğrencinin adım adım alacağı kısmi puan dağılım kriterleri yer alır.

5. **Çıktı Seçenekleri:**
   - **🖨️ A4 Yazdır / PDF:** Tarayıcı üzerinden kenar boşlukları ayarlanmış 1:1 A4 baskı veya PDF kaydetme.
   - **📥 Word (.docx) İndir:** Düzenlenebilir, 2 sütunlu Tevfik İleri İHL şablonunda Word sınav kağıdı indirme.
   - **📥 Rubrik Word (.docx) İndir:** Öğretmen cevap anahtarını ve puanlama tablosunu Word olarak indirme.
   - **💾 Sınavı Kaydet:** Hazırladığınız sınavı veritabanına kaydedip daha sonra tekrar açabilme.

---

### 📂 Klasörün Başka Bilgisayara Taşınması

Bu klasörü (`Nihal_Soru_Hazirla`) USB bellek veya harici disk ile eşinizin bilgisayarına kopyaladığınızda:
- Bilgisayarda Python kurulu olması yeterlidir (`python.org`).
- `baslat.bat` dosyasına tıklandığında tüm gereksinimler otomatik hazırlanır ve uygulama çalışır.
- Tüm hazırlanan sınavlar klasör içindeki yerel veritabanında (`data/soru_hazirla.db`) saklanır, taşındığında hiçbir sınav kaybolmaz.
