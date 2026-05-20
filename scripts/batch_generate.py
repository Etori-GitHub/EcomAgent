import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def get_pending_count():
    conn = sqlite3.connect(DATA_DIR / "product_master.db")
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM product_master WHERE short_name IS NULL OR short_name = ""')
    count = c.fetchone()[0]
    conn.close()
    return count

def get_pending_products(limit=50):
    conn = sqlite3.connect(DATA_DIR / "product_master.db")
    c = conn.cursor()
    c.execute('''
        SELECT ecom_code, name
        FROM product_master
        WHERE (short_name IS NULL OR short_name = "")
        AND (name IS NOT NULL AND name != "")
        ORDER BY id ASC
        LIMIT ?
    ''', (limit,))
    rows = c.fetchall()
    conn.close()
    return [{"id": row[0], "name": row[1]} for row in rows]

def save_pending(items):
    PROCESSING_DIR = DATA_DIR / "name_processing"
    PROCESSING_DIR.mkdir(parents=True, exist_ok=True)
    
    from datetime import datetime
    batch_id = datetime.now().strftime("%Y%m%d_%H%M")
    
    data = {
        "batch_id": batch_id,
        "created_at": datetime.now().isoformat(),
        "count": len(items),
        "items": items
    }
    
    with open(PROCESSING_DIR / "pending_names.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"已生成 pending_names.json，共 {len(items)} 条")

if __name__ == "__main__":
    pending = get_pending_count()
    print(f"待翻译商品: {pending}")
    
    if pending > 0:
        items = get_pending_products(50)
        save_pending(items)
    else:
        print("没有待翻译的商品")