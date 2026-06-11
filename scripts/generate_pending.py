#!/usr/bin/env python3
import json
import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PROCESSING_DIR = DATA_DIR / "name_processing"
PENDING_FILE = PROCESSING_DIR / "pending_names.json"

def is_chinese_short_name(short_name: str) -> bool:
    """判断简称是否已经是中文"""
    if not short_name:
        return False
    for char in short_name:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False

conn = sqlite3.connect(DATA_DIR / "product_master.db")
cursor = conn.cursor()

# 获取 translated 状态但没有中文简称的记录
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

conn.close()

print(f"Found {len(needs_translation)} items needing translation")

# 创建输出目录
PROCESSING_DIR.mkdir(parents=True, exist_ok=True)

# 生成 JSON
batch_id = datetime.now().strftime("%Y%m%d_%H%M")
data = {
    "batch_id": batch_id,
    "created_at": datetime.now().isoformat(),
    "count": len(needs_translation),
    "items": needs_translation
}

with open(PENDING_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Generated: {PENDING_FILE}")
print(f"Batch ID: {batch_id}")
print(f"Count: {len(needs_translation)}")
