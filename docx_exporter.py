"""
Word (.docx) MEB Sınav Kağıdı ve Cevap Anahtarı Üretici
python-docx kullanarak A4 boyutunda, MEB ve Tevfik İleri İHL standartlarında yazılı kağıdı üretir.
"""

from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from config import EXPORTS_DIR, get_config

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Hücre içi kenar boşluklarını ayarlar."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    """Hücre kenarlıklarını belirler."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'w:{edge}'
            element = OxmlElement(tag)
            element.set(qn('w:val'), edge_data.get('val', 'single'))
            element.set(qn('w:sz'), str(edge_data.get('sz', 4)))
            element.set(qn('w:space'), '0')
            element.set(qn('w:color'), edge_data.get('color', 'CCCCCC'))
            tcBorders.append(element)
    tcPr.append(tcBorders)

def generate_exam_docx(exam_data: dict, layout: str = "2_column") -> Path:
    """MEB formatında öğrenci sınav kağıdı Word (.docx) dosyasını üretir."""
    doc = Document()
    cfg = get_config()
    
    # A4 Kenar Boşlukları (Dar kenar boşlukları - 1.27 cm / 0.5 inç)
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)
        section.page_width = Inches(8.27)  # A4
        section.page_height = Inches(11.69)
        
    header_info = exam_data.get("header_info", {})
    school_header = header_info.get("school_header") or cfg.get("school_header", "T.C. MİLLÎ EĞİTİM BAKANLIĞI")
    school_name = header_info.get("school_name") or cfg.get("school_name", "KOCAELİ / DARICA - Tevfik İleri İmam Hatip Ortaokulu")
    
    subject_title = exam_data.get("subject_name", exam_data.get("subject", "Din Kültürü ve Ahlak Bilgisi"))
    grade = exam_data.get("grade", 5)
    term = exam_data.get("term", "1. Dönem")
    exam_no = exam_data.get("exam_no", "1. Yazılı")
    scenario = exam_data.get("scenario", "Senaryo 1")
    total_points = exam_data.get("total_points", 100)
    
    # 1. Başlık Anteti
    p_hdr = doc.add_paragraph()
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_hdr.add_run(f"{school_header}\n")
    r1.bold = True
    r1.font.size = Pt(10)
    r1.font.name = "Arial"
    
    r2 = p_hdr.add_run(f"{school_name}\n")
    r2.bold = True
    r2.font.size = Pt(10.5)
    r2.font.name = "Arial"
    
    r3 = p_hdr.add_run(f"2025-2026 EĞİTİM ÖĞRETİM YILI {grade}. SINIF {subject_title.upper()} DERSİ\n")
    r3.bold = True
    r3.font.size = Pt(10)
    r3.font.name = "Arial"
    
    r4 = p_hdr.add_run(f"{term.upper()} {exam_no.upper()} SINAVI ({scenario.upper()})")
    r4.bold = True
    r4.font.size = Pt(10.5)
    r4.font.name = "Arial"
    p_hdr.paragraph_format.space_after = Pt(4)
    
    # 2. Öğrenci Bilgi Tablosu
    info_table = doc.add_table(rows=2, cols=4)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_table.autofit = False
    
    col_widths = [Inches(1.2), Inches(3.2), Inches(1.5), Inches(1.3)]
    for row in info_table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width
            set_cell_margins(row.cells[idx], top=60, bottom=60, left=100, right=100)
            set_cell_border(row.cells[idx], 
                            top={'val': 'single', 'sz': 4, 'color': '888888'},
                            bottom={'val': 'single', 'sz': 4, 'color': '888888'},
                            left={'val': 'single', 'sz': 4, 'color': '888888'},
                            right={'val': 'single', 'sz': 4, 'color': '888888'})
                            
    # 1. Satır: Adı Soyadı & Puan Kutusu
    c0 = info_table.rows[0].cells[0]
    p = c0.paragraphs[0]
    r = p.add_run("Adı ve Soyadı:")
    r.bold = True
    r.font.size = Pt(9)
    r.font.name = "Arial"
    
    c1 = info_table.rows[0].cells[1]
    p = c1.paragraphs[0]
    p.add_run(".............................................................")
    
    c2 = info_table.rows[0].cells[2]
    p = c2.paragraphs[0]
    r = p.add_run("ALDIĞI PUAN:")
    r.bold = True
    r.font.size = Pt(9)
    r.font.name = "Arial"
    
    c3 = info_table.rows[0].cells[3]
    p = c3.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"....... / {total_points}")
    r.bold = True
    r.font.size = Pt(10)
    r.font.name = "Arial"
    
    # 2. Satır: Sınıf/Şube & No & Tarih
    c0 = info_table.rows[1].cells[0]
    p = c0.paragraphs[0]
    r = p.add_run("Sınıfı / Şubesi:")
    r.bold = True
    r.font.size = Pt(9)
    r.font.name = "Arial"
    
    c1 = info_table.rows[1].cells[1]
    p = c1.paragraphs[0]
    p.add_run(f"{grade} / .....       Okul No: ...............")
    
    c2 = info_table.rows[1].cells[2]
    p = c2.paragraphs[0]
    r = p.add_run("Tarih / İmza:")
    r.bold = True
    r.font.size = Pt(9)
    r.font.name = "Arial"
    
    c3 = info_table.rows[1].cells[3]
    p = c3.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("...../...../2026")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    questions = exam_data.get("questions", [])
    
    # Düzen: 2 Sütunlu (2_column) veya Tek Sütunlu (1_column)
    if layout == "2_column" and len(questions) > 1:
        # 2 Sütunlu Tablo ile MEB Sınav Düzeni
        mid = (len(questions) + 1) // 2
        col1_questions = questions[:mid]
        col2_questions = questions[mid:]
        
        main_table = doc.add_table(rows=1, cols=2)
        main_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        main_table.autofit = False
        
        c_left = main_table.rows[0].cells[0]
        c_right = main_table.rows[0].cells[1]
        
        c_left.width = Inches(3.6)
        c_right.width = Inches(3.6)
        
        # Ortaya dikey kesikli ayrım çizgisi
        set_cell_border(c_left, right={'val': 'dashed', 'sz': 6, 'color': 'AAAAAA'})
        set_cell_margins(c_left, top=50, bottom=50, left=50, right=100)
        set_cell_margins(c_right, top=50, bottom=50, left=100, right=50)
        
        def render_questions_into_cell(cell, q_list):
            for idx, q in enumerate(q_list):
                p_q = cell.add_paragraph()
                r_num = p_q.add_run(f"Soru {q.get('q_order')}) ")
                r_num.bold = True
                r_num.font.size = Pt(9.5)
                r_num.font.name = "Arial"
                
                r_pts = p_q.add_run(f"({q.get('points', 10)} Puan) ")
                r_pts.bold = True
                r_pts.font.size = Pt(8.5)
                r_pts.font.color.rgb = RGBColor(100, 100, 100)
                r_pts.font.name = "Arial"
                
                p_q.paragraph_format.space_after = Pt(2)
                p_q.paragraph_format.line_spacing = 1.15
                
                # Arapça metin varsa ekle
                ar_txt = q.get("arabic_text", "").strip()
                if ar_txt:
                    p_ar = cell.add_paragraph()
                    p_ar.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    r_ar = p_ar.add_run(ar_txt)
                    r_ar.font.name = "Traditional Arabic"
                    r_ar.font.size = Pt(14)
                    r_ar.bold = True
                    p_ar.paragraph_format.space_after = Pt(2)
                    
                # Soru metni
                p_text = cell.add_paragraph()
                r_txt = p_text.add_run(q.get("question_text", ""))
                r_txt.font.size = Pt(9)
                r_txt.font.name = "Arial"
                p_text.paragraph_format.space_after = Pt(4)
                
                # Cevap çizgileri
                p_lines = cell.add_paragraph()
                p_lines.paragraph_format.line_spacing = 1.3
                p_lines.paragraph_format.space_after = Pt(12)
                # Çizgili boşluk
                lines_str = "Cevap:\n" + ("................................................................................\n" * 4)
                r_ln = p_lines.add_run(lines_str)
                r_ln.font.size = Pt(8)
                r_ln.font.color.rgb = RGBColor(180, 180, 180)

        render_questions_into_cell(c_left, col1_questions)
        render_questions_into_cell(c_right, col2_questions)
        
    else:
        # Tek Sütunlu Sayfa Düzeni
        for q in questions:
            p_q = doc.add_paragraph()
            r_num = p_q.add_run(f"Soru {q.get('q_order')}) ")
            r_num.bold = True
            r_num.font.size = Pt(10)
            r_num.font.name = "Arial"
            
            r_pts = p_q.add_run(f"({q.get('points', 10)} Puan)")
            r_pts.bold = True
            r_pts.font.size = Pt(9)
            r_pts.font.color.rgb = RGBColor(100, 100, 100)
            
            ar_txt = q.get("arabic_text", "").strip()
            if ar_txt:
                p_ar = doc.add_paragraph()
                p_ar.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r_ar = p_ar.add_run(ar_txt)
                r_ar.font.name = "Traditional Arabic"
                r_ar.font.size = Pt(15)
                r_ar.bold = True
                
            p_text = doc.add_paragraph()
            r_txt = p_text.add_run(q.get("question_text", ""))
            r_txt.font.size = Pt(9.5)
            r_txt.font.name = "Arial"
            
            # Cevap çizgileri
            p_lines = doc.add_paragraph()
            p_lines.paragraph_format.space_after = Pt(14)
            p_lines.add_run("Cevap:\n" + ("...............................................................................................................................\n" * 4))
            
    # Alt Not
    p_ft = doc.add_paragraph()
    p_ft.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ft = p_ft.add_run("Sınav süresi 40 dakikadır. Başarılar dilerim.")
    r_ft.font.italic = True
    r_ft.font.size = Pt(8.5)
    r_ft.font.name = "Arial"
    
    file_id = exam_data.get("id", "yeni")
    filename = f"Sinav_Kagidi_{subject_title}_{grade}Sinif_{term}_{file_id}.docx".replace(" ", "_")
    output_path = EXPORTS_DIR / filename
    doc.save(str(output_path))
    return output_path

def generate_answer_key_docx(exam_data: dict) -> Path:
    """Öğretmen Cevap Anahtarı ve Puanlama Rubriği Word dosyasını üretir."""
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)
        
    subject_title = exam_data.get("subject_name", exam_data.get("subject", "Din Kültürü ve Ahlak Bilgisi"))
    grade = exam_data.get("grade", 5)
    term = exam_data.get("term", "1. Dönem")
    exam_no = exam_data.get("exam_no", "1. Yazılı")
    scenario = exam_data.get("scenario", "Senaryo 1")
    
    cfg = get_config()
    school_title = exam_data.get("header_info", {}).get("school_name") or cfg.get("school_name", "KOCAELİ / DARICA - Tevfik İleri İmam Hatip Ortaokulu")
    
    p_hdr = doc.add_paragraph()
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_hdr.add_run(f"{school_title}\n")
    r1.bold = True
    r1.font.size = Pt(11)
    
    r2 = p_hdr.add_run(f"{grade}. SINIF {subject_title.upper()} {term.upper()} {exam_no.upper()} ({scenario.upper()})\nCEVAP ANAHTARI VE DERECELİ PUANLAMA ANAHTARI (RUBRİK)")
    r2.bold = True
    r2.font.size = Pt(11.5)
    r2.font.color.rgb = RGBColor(0, 51, 102)
    p_hdr.paragraph_format.space_after = Pt(10)
    
    questions = exam_data.get("questions", [])
    for q in questions:
        # Soru Başlığı
        p_q = doc.add_paragraph()
        r_num = p_q.add_run(f"SORU {q.get('q_order')} [Toplam: {q.get('points', 10)} Puan] ")
        r_num.bold = True
        r_num.font.size = Pt(10)
        
        outcome = q.get("learning_outcome", "")
        if outcome:
            r_out = p_q.add_run(f" | Kazanım: {outcome}")
            r_out.font.italic = True
            r_out.font.size = Pt(8.5)
            r_out.font.color.rgb = RGBColor(120, 120, 120)
            
        p_q.paragraph_format.space_after = Pt(2)
        
        # Soru Metni
        p_txt = doc.add_paragraph()
        r_txt = p_txt.add_run(q.get("question_text", ""))
        r_txt.font.size = Pt(9.5)
        p_txt.paragraph_format.space_after = Pt(4)
        
        # Model Cevap
        p_ans = doc.add_paragraph()
        r_at = p_ans.add_run("Beklenen Örnek Cevap:\n")
        r_at.bold = True
        r_at.font.size = Pt(9.5)
        r_at.font.color.rgb = RGBColor(0, 102, 51)
        r_ac = p_ans.add_run(q.get("answer_text", ""))
        r_ac.font.size = Pt(9.5)
        p_ans.paragraph_format.space_after = Pt(4)
        
        # Rubrik Tablosu
        rubric = q.get("rubric", [])
        if rubric and isinstance(rubric, list):
            rubric_table = doc.add_table(rows=1, cols=2)
            rubric_table.autofit = False
            rubric_table.rows[0].cells[0].width = Inches(6.0)
            rubric_table.rows[0].cells[1].width = Inches(1.2)
            
            # Başlık
            h0 = rubric_table.rows[0].cells[0]
            h0.paragraphs[0].add_run("Puanlama Kriteri (Kısmi Puan Basamakları)").bold = True
            h1 = rubric_table.rows[0].cells[1]
            h1.paragraphs[0].add_run("Puan").bold = True
            h1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            set_cell_border(h0, bottom={'val': 'single', 'sz': 4, 'color': '888888'})
            set_cell_border(h1, bottom={'val': 'single', 'sz': 4, 'color': '888888'})
            
            for item in rubric:
                row = rubric_table.add_row()
                row.cells[0].width = Inches(6.0)
                row.cells[1].width = Inches(1.2)
                
                c_text = item.get("criterion", "") if isinstance(item, dict) else str(item)
                c_pts = item.get("points", "") if isinstance(item, dict) else ""
                
                row.cells[0].paragraphs[0].add_run(f"• {c_text}").font.size = Pt(9)
                p_p = row.cells[1].paragraphs[0]
                p_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_p.add_run(f"{c_pts} Puan" if c_pts else "").font.size = Pt(9)
                
                set_cell_margins(row.cells[0], top=40, bottom=40, left=60, right=60)
                set_cell_margins(row.cells[1], top=40, bottom=40, left=60, right=60)
                set_cell_border(row.cells[0], bottom={'val': 'single', 'sz': 2, 'color': 'DDDDDD'})
                set_cell_border(row.cells[1], bottom={'val': 'single', 'sz': 2, 'color': 'DDDDDD'})
                
        doc.add_paragraph().paragraph_format.space_after = Pt(8)
        
    file_id = exam_data.get("id", "yeni")
    filename = f"Cevap_Anahtari_{subject_title}_{grade}Sinif_{term}_{file_id}.docx".replace(" ", "_")
    output_path = EXPORTS_DIR / filename
    doc.save(str(output_path))
    return output_path
