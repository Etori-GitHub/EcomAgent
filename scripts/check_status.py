#!/usr/bin/env python3
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
db_path = DATA_DIR / "product_master.db"

def is_chinese_short_name(short_name: str) -> bool:
    """判断简称是否已经是中文"""
    if not short_name:
        return False
    for char in short_name:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 检查 translated 但没有中文简称的记录
cursor.execute('SELECT ecom_code, name, short_name FROM product_master WHERE translation_status = "translated"')
rows = cursor.fetchall()

needs_translation = []
for row in rows:
    ecom_code, name, short_name = row
    if name and name.strip() and not is_chinese_short_name(short_name):
        needs_translation.append({
            "id": ecom_code,
            "name": name
        })

print(f"Total translated without Chinese short_name: {len(needs_translation)}")
print("\nFirst 10:")
for item in needs_translation[:10]:
    print(f"  {item['id']}: {item['name'][:60]}...")

conn.close()
