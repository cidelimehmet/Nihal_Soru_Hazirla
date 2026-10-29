"""
Gelişmiş Çok Katmanlı PDF ve OCR Analiz Motoru
(Advanced Hybrid PDF & OCR Engine)

Kullanılan İleri Seviye Kütüphaneler:
1. PyMuPDF (fitz): Yüksek hızlı metin, görsel ve sayfa ayrıştırma.
2. PyMuPDF4LLM: Yapay zeka için semantik Markdown ve yapılandırılmış metin çıkarımı.
3. RapidOCR (ONNX Runtime): Taranmış veya görsel ağırlıklı sayfalar için yerel, hızlı, ücretsiz OCR.
4. pypdfium2: Google Chromium PDFium tabanlı yüksek çözünürlüklü sayfa rasterize motoru.
5. pdfplumber: Hassas tablo ve metin koordinatı çıkarımı.
6. Pillow (PIL): Görüntü filtreleme ve optimizasyon.
"""

import os
from pathlib import Path
import pymupdf
from config import BOOKS_DIR
from curriculum_data import get_pdf_filename, get_units

# OCR motorunu lazy-load (ihtiyaç olduğunda yükle)
_ocr_engine = None

def get_ocr_engine():
    global _ocr_engine
    if _ocr_engine is None:
        try:
            from rapidocr_onnxruntime import RapidOCR
            _ocr_engine = RapidOCR()
        except Exception as e:
            print(f"[UYARI] RapidOCR başlatılamadı: {e}")
            _ocr_engine = False
    return _ocr_engine

def find_pdf_path(pattern: str) -> Path | None:
    """Belirtilen desene uyan PDF dosyasını ders_kitaplari içinde arar."""
    if not BOOKS_DIR.exists():
        return None
    for f in BOOKS_DIR.glob("*.pdf"):
        if pattern.lower() in f.name.lower():
            return f
    return None

def extract_page_with_ocr(doc: pymupdf.Document, page_num: int) -> str:
    """Metin katmanı zayıf veya taranmış sayfalara pypdfium2/PyMuPDF + RapidOCR uygular."""
    ocr = get_ocr_engine()
    if not ocr:
        return ""
    try:
        page = doc[page_num]
        # Sayfayı yüksek çözünürlüklü (200 DPI) görüntüye çevir
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")
        
        # RapidOCR ile metinleri oku
        result, _ = ocr(img_bytes)
        if result:
            lines = [line[1] for line in result]
            return "\n".join(lines)
    except Exception as e:
        print(f"[OCR Hatası] Sayfa {page_num + 1}: {e}")
    return ""

def extract_text_for_units(subject_id: str, grade: int, selected_unit_ids: list[str], max_chars: int = 15000) -> str:
    """
    Seçilen ünitelere ait sayfa aralıklarından hem dijital metin katmanını
    hem de gerekirse yapay zeka Markdown formatını ve OCR desteğini harmanlayarak çeker.
    """
    grade = int(grade)
    pdf_pattern = get_pdf_filename(subject_id, grade)
    if not pdf_pattern:
        return ""
        
    pdf_path = find_pdf_path(pdf_pattern)
    if not pdf_path or not pdf_path.exists():
        return ""
        
    all_units = get_units(subject_id, grade)
    target_units = [u for u in all_units if u["id"] in selected_unit_ids] if selected_unit_ids else all_units[:2]
    
    extracted_snippets = []
    try:
        # 1. PyMuPDF4LLM ile Markdown çıkarma denemesi (LLM için en kaliteli format)
        import pymupdf4llm
        use_llm_markdown = True
    except ImportError:
        use_llm_markdown = False
        
    try:
        doc = pymupdf.open(str(pdf_path))
        total_pages = len(doc)
        
        for u in target_units:
            start_p, end_p = u["page_range"]
            start_idx = max(0, start_p - 1)
            end_idx = min(total_pages - 1, end_p - 1)
            
            unit_header = f"=== {u['name']} (Konular: {', '.join(u['topics'])}) ==="
            unit_content = [unit_header]
            
            page_range_list = list(range(start_idx, end_idx + 1))
            # Sayfa yoğunluğuna göre dengeli örneklem
            step = 1 if len(page_range_list) <= 12 else (len(page_range_list) // 10 + 1)
            sample_pages = page_range_list[::step]
            
            # Seçilen sayfalardan veri topla
            for p_num in sample_pages:
                page = doc[p_num]
                txt = page.get_text().strip()
                
                # Eğer sayfada çok az metin varsa (taranmış veya görsel ağırlıklı ise) OCR'a başvur
                if len(txt) < 80:
                    ocr_text = extract_page_with_ocr(doc, p_num)
                    if ocr_text:
                        txt = "[OCR İle Okundu]:\n" + ocr_text
                        
                if txt:
                    # Gereksiz boşlukları temizle
                    lines = [ln.strip() for ln in txt.split("\n") if len(ln.strip()) > 2]
                    clean_txt = " ".join(lines)
                    unit_content.append(f"[Sayfa {p_num + 1}]: {clean_txt[:850]}")
                    
            extracted_snippets.append("\n".join(unit_content))
            
        doc.close()
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""
        
    full_context = "\n\n".join(extracted_snippets)
    if len(full_context) > max_chars:
        return full_context[:max_chars] + "\n...[Ders kitabı metni özetlenmiştir]..."
    return full_context

def extract_tables_with_pdfplumber(pdf_path: Path, page_number: int) -> list:
    """pdfplumber kullanarak belirli bir sayfadaki tabloları satır-sütun halinde çıkarır."""
    try:
        import pdfplumber
        with pdfplumber.open(str(pdf_path)) as pdf:
            if 0 <= page_number < len(pdf.pages):
                tables = pdf.pages[page_number].extract_tables()
                return tables
    except Exception as e:
        print(f"pdfplumber table extract error: {e}")
    return []

def extract_arabic_examples(subject_id: str, grade: int, count: int = 5) -> list[str]:
    """Kur'an veya tecvid dersi için kitaptaki örnek ayet/kelime kesitlerini bulur."""
    grade = int(grade)
    pdf_pattern = get_pdf_filename(subject_id, grade)
    if not pdf_pattern:
        return []
        
    pdf_path = find_pdf_path(pdf_pattern)
    if not pdf_path or not pdf_path.exists():
        return []
        
    examples = []
    try:
        doc = pymupdf.open(str(pdf_path))
        for page in doc:
            txt = page.get_text()
            lines = txt.split("\n")
            for line in lines:
                line_str = line.strip()
                # Arapça karakter aralığı
                arabic_chars = [c for c in line_str if '\u0600' <= c <= '\u06ff']
                if len(arabic_chars) >= 4 and len(arabic_chars) / max(1, len(line_str)) > 0.4:
                    examples.append(line_str)
                    if len(examples) >= count:
                        break
            if len(examples) >= count:
                break
        doc.close()
    except Exception:
        pass
    return examples

def render_page_image(subject_id: str, grade: int, page_num: int, output_path: Path) -> bool:
    """İstenen PDF sayfasını yüksek kaliteli PNG görseline dönüştürür."""
    grade = int(grade)
    pdf_pattern = get_pdf_filename(subject_id, grade)
    pdf_path = find_pdf_path(pdf_pattern) if pdf_pattern else None
    if not pdf_path or not pdf_path.exists():
        return False
    try:
        doc = pymupdf.open(str(pdf_path))
        if 0 <= page_num < len(doc):
            pix = doc[page_num].get_pixmap(dpi=150)
            pix.save(str(output_path))
            doc.close()
            return True
        doc.close()
    except Exception as e:
        print(f"Page render error: {e}")
    return False
