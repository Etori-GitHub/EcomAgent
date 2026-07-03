#!/usr/bin/env python3
"""检查翻译状态"""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
db_path = BASE_DIR / "data" / "product_master.db"

if not db_path.exists():
    print(f"数据库不存在: {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM product_master")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM product_master WHERE translation_status = 'done'")
    done = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM product_master WHERE translation_status = 'pending' OR translation_status IS NULL")
    pending = cursor.fetchone()[0]
    
    print(f"总商品数: {total}")
    print(f"已翻译: {done}")
    print(f"待翻译: {pending}")
    
    conn.close()
