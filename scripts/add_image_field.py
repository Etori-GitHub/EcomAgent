#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加 local_image_path 字段到数据库表
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


def add_image_field(db_path: Path, table: str):
    """添加 local_image_path 字段"""
    if not db_path.exists():
        print(f"[SKIP] {db_path.name} 不存在")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查字段是否存在
    cursor.execute(f"PRAGMA table_info({table})")
    fields = [row[1] for row in cursor.fetchall()]
    
    if 'local_image_path' in fields:
        print(f"[OK] {db_path.name}.{table} 已有 local_image_path 字段")
        conn.close()
        return
    
    # 添加字段
    try:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN local_image_path TEXT")
        conn.commit()
        print(f"[OK] {db_path.name}.{table} 添加 local_image_path 字段成功")
    except Exception as e:
        print(f"[ERROR] {db_path.name}.{table} 添加字段失败: {e}")
    
    conn.close()


def main():
    print("\n添加 local_image_path 字段...\n")
    
    # Amazon
    add_image_field(DATA_DIR / "amazon.db", "products")
    
    # TikTok
    add_image_field(DATA_DIR / "tiktok.db", "tiktok_products")
    
    print("\n完成!\n")


if __name__ == "__main__":
    main()