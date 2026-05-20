#!/usr/bin/env python3
"""
数据库迁移脚本 - 添加图片字段
添加新字段：image_url, local_image_path
"""

import sqlite3
from pathlib import Path


def migrate_amazon_db():
    """迁移 Amazon 数据库"""
    db_path = Path("C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/amazon.db")
    
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return
    
    print(f"📂 Using database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查字段是否已存在
    cursor.execute("PRAGMA table_info(products)")
    columns = [col[1] for col in cursor.fetchall()]
    
    # 添加 image_url 字段
    if 'image_url' not in columns:
        cursor.execute("ALTER TABLE products ADD COLUMN image_url TEXT")
        print("✅ Added image_url column to products")
    
    # 添加 local_image_path 字段
    if 'local_image_path' not in columns:
        cursor.execute("ALTER TABLE products ADD COLUMN local_image_path TEXT")
        print("✅ Added local_image_path column to products")
    
    conn.commit()
    conn.close()
    print("✅ Amazon database migration complete!")


def migrate_tiktok_db():
    """迁移 TikTok 数据库"""
    db_path = Path("C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/tiktok.db")
    
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return
    
    print(f"📂 Using database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查字段是否已存在
    cursor.execute("PRAGMA table_info(tiktok_products)")
    columns = [col[1] for col in cursor.fetchall()]
    
    # 添加 image_url 字段
    if 'image_url' not in columns:
        cursor.execute("ALTER TABLE tiktok_products ADD COLUMN image_url TEXT")
        print("✅ Added image_url column to tiktok_products")
    
    # 添加 local_image_path 字段
    if 'local_image_path' not in columns:
        cursor.execute("ALTER TABLE tiktok_products ADD COLUMN local_image_path TEXT")
        print("✅ Added local_image_path column to tiktok_products")
    
    conn.commit()
    conn.close()
    print("✅ TikTok database migration complete!")


def create_image_changes_table():
    """创建图片变更记录表"""
    db_path = Path("C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/image_changes.db")
    
    print(f"📂 Creating database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 图片变更记录表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS image_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            platform_id TEXT NOT NULL,
            old_image_url TEXT,
            new_image_url TEXT NOT NULL,
            old_local_path TEXT,
            new_local_path TEXT NOT NULL,
            change_date TEXT NOT NULL,
            change_time TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 创建索引
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_image_changes_platform_id 
        ON image_changes(platform, platform_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_image_changes_date 
        ON image_changes(change_date)
    """)
    
    conn.commit()
    conn.close()
    print("✅ Image changes table created!")


if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration Script - Image Fields")
    print("=" * 60)
    
    migrate_amazon_db()
    print()
    migrate_tiktok_db()
    print()
    create_image_changes_table()
    
    print("\n" + "=" * 60)
    print("All migrations complete!")
    print("=" * 60)