"""
Konfigürasyon Yöneticisi
.env ve config.json ayarlarını yükler ve yönetir.
"""

import os
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
CONFIG_JSON_PATH = BASE_DIR / "config.json"
DATA_DIR = BASE_DIR / "data"
BOOKS_DIR = BASE_DIR / "ders_kitaplari"
EXPORTS_DIR = BASE_DIR / "exports"

# Dizinleri garanti et
DATA_DIR.mkdir(exist_ok=True)
EXPORTS_DIR.mkdir(exist_ok=True)

def load_env_file(filepath: Path) -> dict:
    env_vars = {}
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip().strip('"').strip("'")
    return env_vars

def get_config() -> dict:
    """Güncel ayarları her çağrıda taze olarak .env ve config.json dosyasından okur."""
    env_dict = load_env_file(ENV_PATH)
    
    cfg = {
        "gemini_api_key": env_dict.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", "")),
        "gemini_model": env_dict.get("GEMINI_MODEL", "gemini-3.8-flash"),
        "school_header": env_dict.get("SCHOOL_HEADER", "T.C. MİLLÎ EĞİTİM BAKANLIĞI"),
        "school_name": env_dict.get("SCHOOL_NAME", "KOCAELİ / DARICA - Tevfik İleri İmam Hatip Ortaokulu"),
        "teacher_name": env_dict.get("TEACHER_NAME", "Nihal YILDIZ"),
        "login_username": env_dict.get("LOGIN_USERNAME", "nihal"),
        "login_password": env_dict.get("LOGIN_PASSWORD", "12345"),
        "port": int(env_dict.get("PORT", "8000")),
    }
    
    # config.json varsa üzerine yaz
    if CONFIG_JSON_PATH.exists():
        try:
            with open(CONFIG_JSON_PATH, "r", encoding="utf-8") as f:
                override = json.load(f)
                cfg.update(override)
        except Exception:
            pass
            
    return cfg

def save_config(new_values: dict):
    """Ayarları günceller ve hem config.json hem .env dosyasına yazar."""
    current = get_config()
    current.update(new_values)
    
    with open(CONFIG_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(current, f, ensure_ascii=False, indent=2)
        
    try:
        lines = []
        if ENV_PATH.exists():
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                lines = f.readlines()
        
        mapping = {
            "GEMINI_API_KEY": current.get("gemini_api_key", ""),
            "GEMINI_MODEL": current.get("gemini_model", "gemini-3.8-flash"),
            "SCHOOL_HEADER": current.get("school_header", ""),
            "SCHOOL_NAME": current.get("school_name", ""),
            "TEACHER_NAME": current.get("teacher_name", ""),
            "LOGIN_USERNAME": current.get("login_username", ""),
            "LOGIN_PASSWORD": current.get("login_password", ""),
            "PORT": str(current.get("port", 8000))
        }
        
        new_lines = []
        written_keys = set()
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and "=" in stripped:
                k = stripped.split("=", 1)[0].strip()
                if k in mapping:
                    new_lines.append(f"{k}={mapping[k]}\n")
                    written_keys.add(k)
                    continue
            new_lines.append(line)
            
        for k, v in mapping.items():
            if k not in written_keys:
                new_lines.append(f"{k}={v}\n")
                
        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    except Exception as e:
        print(f"Error saving to .env: {e}")
