#!/usr/bin/env python3
"""检查 product_master 数据库状态"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "product_master.db"

if not DB_PATH.exists():
    print(f"数据库不存在: {DB_PATH}")
else:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM product_master")
    print(f"商品总数: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM product_master WHERE translation_status = 'done'")
    print(f"已翻译: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM product_master WHERE translation_status = 'pending'")
    print(f"待翻译: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM product_master WHERE translation_status IS NULL")
    print(f"无状态: {cursor.fetchone()[0]}")
    
    # 检查有名称但无翻译状态的商品
    cursor.execute("""SELECT COUNT(*) FROM product_master 
                       WHERE (translation_status IS NULL OR translation_status = 'pending')
                       AND name IS NOT NULL AND name != ''""")
    print(f"符合翻译条件: {cursor.fetchone()[0]}")
    
    # 检查无名称的商品
    cursor.execute("SELECT COUNT(*) FROM product_master WHERE name IS NULL OR name = ''")
    print(f"无名称商品: {cursor.fetchone()[0]}")
    
    conn.close()