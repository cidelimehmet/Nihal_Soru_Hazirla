"""
SQLite Veritabanı Modülü - Genişletilmiş ve Otomatik Migrasyonlu Sürüm
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from config import DATA_DIR, get_config

DB_PATH = DATA_DIR / "soru_hazirla.db"

def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Kullanıcı tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        teacher_name TEXT,
        school_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # Sınavlar tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        exam_type TEXT DEFAULT 'yazili_sinav',
        subject TEXT NOT NULL,
        grade INTEGER NOT NULL,
        term TEXT NOT NULL,
        exam_no TEXT NOT NULL,
        scenario TEXT,
        layout TEXT DEFAULT '2_column',
        total_points INTEGER DEFAULT 100,
        question_count INTEGER DEFAULT 0,
        header_info TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # Sınav Soruları tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exam_id INTEGER NOT NULL,
        q_order INTEGER NOT NULL,
        question_text TEXT NOT NULL,
        points INTEGER DEFAULT 10,
        learning_outcome TEXT,
        answer_text TEXT,
        rubric_json TEXT,
        question_type TEXT DEFAULT 'acik_uclu',
        arabic_text TEXT,
        cognitive_level TEXT DEFAULT 'Analiz',
        difficulty TEXT DEFAULT 'Orta',
        source_book TEXT,
        source_page TEXT,
        source_context TEXT,
        options_json TEXT,
        FOREIGN KEY (exam_id) REFERENCES exams (id) ON DELETE CASCADE
    );
    """)

    # Soru Bankası Tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS question_bank (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        grade INTEGER NOT NULL,
        unit_name TEXT,
        topic TEXT,
        learning_outcome TEXT,
        question_text TEXT NOT NULL,
        answer_text TEXT,
        rubric_json TEXT,
        question_type TEXT DEFAULT 'acik_uclu',
        arabic_text TEXT,
        cognitive_level TEXT DEFAULT 'Analiz',
        difficulty TEXT DEFAULT 'Orta',
        source_book TEXT,
        source_page TEXT,
        source_context TEXT,
        options_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Soru Kullanım Takip Tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS question_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_bank_id INTEGER,
        exam_id INTEGER,
        exam_title TEXT,
        used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (question_bank_id) REFERENCES question_bank(id) ON DELETE CASCADE,
        FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE
    );
    """)
    conn.commit()
    
    # --- MİGRASYON KONTROLLERİ (Eski tabloları güncelle) ---
    def add_column_if_missing(table, col_name, col_type):
        try:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type};")
            conn.commit()
        except sqlite3.OperationalError:
            pass # Zaten var

    add_column_if_missing("exams", "exam_type", "TEXT DEFAULT 'yazili_sinav'")
    add_column_if_missing("questions", "cognitive_level", "TEXT DEFAULT 'Analiz'")
    add_column_if_missing("questions", "difficulty", "TEXT DEFAULT 'Orta'")
    add_column_if_missing("questions", "source_book", "TEXT")
    add_column_if_missing("questions", "source_page", "TEXT")
    add_column_if_missing("questions", "source_context", "TEXT")
    add_column_if_missing("questions", "options_json", "TEXT")
    
    cfg = get_config()
    cursor.execute("SELECT id FROM users WHERE username = ?", (cfg["login_username"],))
    user = cursor.fetchone()
    if not user:
        cursor.execute("""
        INSERT INTO users (username, password, teacher_name, school_name)
        VALUES (?, ?, ?, ?)
        """, (cfg["login_username"], cfg["login_password"], cfg["teacher_name"], cfg["school_name"]))
        conn.commit()
        
    conn.close()

def save_exam(exam_data: dict) -> int:
    """Sınav kaydeder veya günceller; soruları soru bankasıyla ve kullanım takibiyle ilişkilendirir."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    exam_id = exam_data.get("id")
    header_info_json = json.dumps(exam_data.get("header_info", {}), ensure_ascii=False)
    exam_title = exam_data.get("title", "İsimsiz Sınav")
    
    if exam_id:
        cursor.execute("""
        UPDATE exams SET
            title = ?, exam_type = ?, subject = ?, grade = ?, term = ?, exam_no = ?,
            scenario = ?, layout = ?, total_points = ?, question_count = ?,
            header_info = ?, updated_at = ?
        WHERE id = ?
        """, (
            exam_title,
            exam_data.get("exam_type", "yazili_sinav"),
            exam_data.get("subject", ""),
            exam_data.get("grade", 5),
            exam_data.get("term", "1. Dönem"),
            exam_data.get("exam_no", "1. Yazılı"),
            exam_data.get("scenario", "Senaryo 1"),
            exam_data.get("layout", "2_column"),
            exam_data.get("total_points", 100),
            len(exam_data.get("questions", [])),
            header_info_json,
            now,
            exam_id
        ))
        cursor.execute("DELETE FROM questions WHERE exam_id = ?", (exam_id,))
    else:
        cursor.execute("""
        INSERT INTO exams (
            title, exam_type, subject, grade, term, exam_no, scenario, layout,
            total_points, question_count, header_info, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            exam_title,
            exam_data.get("exam_type", "yazili_sinav"),
            exam_data.get("subject", ""),
            exam_data.get("grade", 5),
            exam_data.get("term", "1. Dönem"),
            exam_data.get("exam_no", "1. Yazılı"),
            exam_data.get("scenario", "Senaryo 1"),
            exam_data.get("layout", "2_column"),
            exam_data.get("total_points", 100),
            len(exam_data.get("questions", [])),
            header_info_json,
            now,
            now
        ))
        exam_id = cursor.lastrowid

    questions = exam_data.get("questions", [])
    for idx, q in enumerate(questions):
        rubric_str = json.dumps(q.get("rubric", []), ensure_ascii=False) if isinstance(q.get("rubric"), (list, dict)) else str(q.get("rubric", ""))
        options_str = json.dumps(q.get("options", []), ensure_ascii=False) if isinstance(q.get("options"), list) else ""
        
        cursor.execute("""
        INSERT INTO questions (
            exam_id, q_order, question_text, points, learning_outcome,
            answer_text, rubric_json, question_type, arabic_text,
            cognitive_level, difficulty, source_book, source_page, source_context, options_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            exam_id,
            idx + 1,
            q.get("question_text", ""),
            q.get("points", 10),
            q.get("learning_outcome", ""),
            q.get("answer_text", ""),
            rubric_str,
            q.get("question_type", "acik_uclu"),
            q.get("arabic_text", ""),
            q.get("cognitive_level", "Analiz"),
            q.get("difficulty", "Orta"),
            q.get("source_book", ""),
            q.get("source_page", ""),
            q.get("source_context", ""),
            options_str
        ))

        q_text = q.get("question_text", "").strip()
        cursor.execute("SELECT id FROM question_bank WHERE question_text = ?", (q_text,))
        bank_item = cursor.fetchone()
        
        bank_id = None
        if bank_item:
            bank_id = bank_item["id"]
        else:
            cursor.execute("""
            INSERT INTO question_bank (
                subject, grade, unit_name, topic, learning_outcome, question_text,
                answer_text, rubric_json, question_type, arabic_text,
                cognitive_level, difficulty, source_book, source_page, source_context, options_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                exam_data.get("subject", "dkab"),
                exam_data.get("grade", 5),
                q.get("unit_name", ""),
                q.get("topic", ""),
                q.get("learning_outcome", ""),
                q_text,
                q.get("answer_text", ""),
                rubric_str,
                q.get("question_type", "acik_uclu"),
                q.get("arabic_text", ""),
                q.get("cognitive_level", "Analiz"),
                q.get("difficulty", "Orta"),
                q.get("source_book", ""),
                q.get("source_page", ""),
                q.get("source_context", ""),
                options_str
            ))
            bank_id = cursor.lastrowid
            
        if bank_id:
            cursor.execute("""
            INSERT INTO question_usage (question_bank_id, exam_id, exam_title)
            VALUES (?, ?, ?)
            """, (bank_id, exam_id, exam_title))

    conn.commit()
    conn.close()
    return exam_id

def get_exam(exam_id: int) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exams WHERE id = ?", (exam_id,))
    exam_row = cursor.fetchone()
    if not exam_row:
        conn.close()
        return None
        
    exam = dict(exam_row)
    if exam.get("header_info"):
        try:
            exam["header_info"] = json.loads(exam["header_info"])
        except Exception:
            pass
            
    cursor.execute("SELECT * FROM questions WHERE exam_id = ? ORDER BY q_order ASC", (exam_id,))
    q_rows = cursor.fetchall()
    questions = []
    for r in q_rows:
        qd = dict(r)
        if qd.get("rubric_json"):
            try:
                qd["rubric"] = json.loads(qd["rubric_json"])
            except Exception:
                qd["rubric"] = qd["rubric_json"]
        if qd.get("options_json"):
            try:
                qd["options"] = json.loads(qd["options_json"])
            except Exception:
                qd["options"] = []
        questions.append(qd)
        
    exam["questions"] = questions
    conn.close()
    return exam

def list_exams() -> list:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, exam_type, subject, grade, term, exam_no, scenario, total_points, question_count, updated_at FROM exams ORDER BY updated_at DESC")
    rows = cursor.fetchall()
    exams = [dict(r) for r in rows]
    conn.close()
    return exams

def delete_exam(exam_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM exams WHERE id = ?", (exam_id,))
    cursor.execute("DELETE FROM questions WHERE exam_id = ?", (exam_id,))
    cursor.execute("DELETE FROM question_usage WHERE exam_id = ?", (exam_id,))
    conn.commit()
    conn.close()
    return True

def get_question_bank_items(subject: str = None, grade: int = None, difficulty: str = None, q_type: str = None, search: str = None) -> list:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT qb.*, 
           COUNT(qu.id) as usage_count,
           GROUP_CONCAT(qu.exam_title, ' || ') as used_in_exams
    FROM question_bank qb
    LEFT JOIN question_usage qu ON qb.id = qu.question_bank_id
    WHERE 1=1
    """
    params = []
    
    if subject:
        query += " AND qb.subject = ?"
        params.append(subject)
    if grade:
        query += " AND qb.grade = ?"
        params.append(int(grade))
    if difficulty:
        query += " AND qb.difficulty = ?"
        params.append(difficulty)
    if q_type:
        query += " AND qb.question_type = ?"
        params.append(q_type)
    if search:
        query += " AND (qb.question_text LIKE ? OR qb.learning_outcome LIKE ? OR qb.unit_name LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])
        
    query += " GROUP BY qb.id ORDER BY qb.id DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    items = []
    for r in rows:
        d = dict(r)
        if d.get("rubric_json"):
            try:
                d["rubric"] = json.loads(d["rubric_json"])
            except Exception:
                d["rubric"] = []
        if d.get("options_json"):
            try:
                d["options"] = json.loads(d["options_json"])
            except Exception:
                d["options"] = []
        if d.get("used_in_exams"):
            d["used_in_exams_list"] = list(set([t.strip() for t in d["used_in_exams"].split(" || ") if t.strip()]))
        else:
            d["used_in_exams_list"] = []
        items.append(d)
        
    conn.close()
    return items

def add_question_to_bank(q_data: dict) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    rubric_str = json.dumps(q_data.get("rubric", []), ensure_ascii=False) if isinstance(q_data.get("rubric"), list) else str(q_data.get("rubric", ""))
    options_str = json.dumps(q_data.get("options", []), ensure_ascii=False) if isinstance(q_data.get("options"), list) else ""
    
    cursor.execute("""
    INSERT INTO question_bank (
        subject, grade, unit_name, topic, learning_outcome, question_text,
        answer_text, rubric_json, question_type, arabic_text,
        cognitive_level, difficulty, source_book, source_page, source_context, options_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        q_data.get("subject", "dkab"),
        q_data.get("grade", 5),
        q_data.get("unit_name", ""),
        q_data.get("topic", ""),
        q_data.get("learning_outcome", ""),
        q_data.get("question_text", ""),
        q_data.get("answer_text", ""),
        rubric_str,
        q_data.get("question_type", "acik_uclu"),
        q_data.get("arabic_text", ""),
        q_data.get("cognitive_level", "Analiz"),
        q_data.get("difficulty", "Orta"),
        q_data.get("source_book", ""),
        q_data.get("source_page", ""),
        q_data.get("source_context", ""),
        options_str
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def delete_question_from_bank(qid: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM question_bank WHERE id = ?", (qid,))
    cursor.execute("DELETE FROM question_usage WHERE question_bank_id = ?", (qid,))
    conn.commit()
    conn.close()
    return True

init_db()
