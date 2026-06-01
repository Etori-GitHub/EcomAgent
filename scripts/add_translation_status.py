#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加翻译状态字段到 product_master 表
"""

import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
MASTER_DB = DATA_DIR / "product_master.db"

def main():
    print("=== 添加翻译状态字段 ===")
    
    conn = sqlite3.connect(str(MASTER_DB))
    cursor = conn.cursor()
    
    # 检查字段是否已存在
    cursor.execute("PRAGMA table_info(product_master)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'translation_status' in columns:
        print("字段 translation_status 已存在，跳过")
        conn.close()
        return
    
    # 添加字段
    print("添加 translation_status 字段...")
    cursor.execute("""
        ALTER TABLE product_master 
        ADD COLUMN translation_status TEXT DEFAULT 'pending'
    """)
    
    # 更新现有数据：有 short_name 的标记为 translated，否则为 pending
    print("更新现有数据的翻译状态...")
    cursor.execute("""
        UPDATE product_master 
        SET translation_status = 'translated' 
        WHERE short_name IS NOT NULL AND short_name != ''
    """)
    
    cursor.execute("""
        UPDATE product_master 
        SET translation_status = 'pending' 
        WHERE short_name IS NULL OR short_name = ''
    """)
    
    conn.commit()
    
    # 统计
    cursor.execute("SELECT COUNT(*) FROM product_master WHERE translation_status = 'translated'")
    translated = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM product_master WHERE translation_status = 'pending'")
    pending = cursor.fetchone()[0]
    
    print(f"已翻译: {translated}")
    print(f"待翻译: {pending}")
    
    conn.close()
    print("完成!")

if __name__ == "__main__":
    main()