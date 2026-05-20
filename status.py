import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

def get_status():
    conn = sqlite3.connect(DATA_DIR / "product_master.db")
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM product_master WHERE short_name IS NULL OR short_name = ""')
    pending = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM product_master WHERE short_name IS NOT NULL AND short_name != ""')
    done = c.fetchone()[0]
    conn.close()
    return pending, done

if __name__ == "__main__":
    pending, done = get_status()
    print(f"待翻译: {pending}, 已翻译: {done}")