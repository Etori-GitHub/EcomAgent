#!/usr/bin/env python3
"""
数据库迁移脚本
添加新字段：product_url, short_name, search_keyword
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
    
    # 添加 product_url 字段
    if 'product_url' not in columns:
        cursor.execute("ALTER TABLE products ADD COLUMN product_url TEXT")
        print("✅ Added product_url column to products")
    
    # 添加 short_name 字段（商品简短描述）
    if 'short_name' not in columns:
        cursor.execute("ALTER TABLE products ADD COLUMN short_name TEXT")
        print("✅ Added short_name column to products")
    
    # 添加 search_keyword 字段（搜索关键词，原 name 改名）
    if 'search_keyword' not in columns:
        cursor.execute("ALTER TABLE products ADD COLUMN search_keyword TEXT")
        print("✅ Added search_keyword column to products")
    
    # 更新 product_url（基于 asin）
    cursor.execute("""
        UPDATE products 
        SET product_url = 'https://www.amazon.com/dp/' || asin 
        WHERE product_url IS NULL AND asin IS NOT NULL
    """)
    print(f"✅ Updated {cursor.rowcount} product URLs")
    
    # 将现有 name 复制到 search_keyword
    cursor.execute("""
        UPDATE products 
        SET search_keyword = name 
        WHERE search_keyword IS NULL
    """)
    print(f"✅ Copied {cursor.rowcount} names to search_keyword")
    
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
    
    # 添加 product_url 字段
    if 'product_url' not in columns:
        cursor.execute("ALTER TABLE tiktok_products ADD COLUMN product_url TEXT")
        print("✅ Added product_url column to tiktok_products")
    
    # 添加 short_name 字段
    if 'short_name' not in columns:
        cursor.execute("ALTER TABLE tiktok_products ADD COLUMN short_name TEXT")
        print("✅ Added short_name column to tiktok_products")
    
    # 添加 search_keyword 字段
    if 'search_keyword' not in columns:
        cursor.execute("ALTER TABLE tiktok_products ADD COLUMN search_keyword TEXT")
        print("✅ Added search_keyword column to tiktok_products")
    
    # 将现有 name 复制到 search_keyword
    cursor.execute("""
        UPDATE tiktok_products 
        SET search_keyword = name 
        WHERE search_keyword IS NULL
    """)
    print(f"✅ Copied {cursor.rowcount} names to search_keyword")
    
    conn.commit()
    conn.close()
    print("✅ TikTok database migration complete!")


if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration Script")
    print("=" * 60)
    
    migrate_amazon_db()
    print()
    migrate_tiktok_db()
    
    print("\n" + "=" * 60)
    print("All migrations complete!")
    print("=" * 60)