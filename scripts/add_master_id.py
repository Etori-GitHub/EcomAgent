#!/usr/bin/env python3
"""
为平台产品表添加 master_id 字段
关联到商品主库
"""

import sqlite3
from pathlib import Path


def add_master_id_to_amazon():
    """Amazon 产品表添加 master_id"""
    db_path = Path("C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/amazon.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查字段是否已存在
    cursor.execute("PRAGMA table_info(products)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'master_id' not in columns:
        cursor.execute("ALTER TABLE products ADD COLUMN master_id INTEGER REFERENCES product_master(id)")
        print("✅ Added master_id to Amazon products")
    else:
        print("ℹ️ master_id already exists in Amazon products")
    
    conn.commit()
    conn.close()


def add_master_id_to_tiktok():
    """TikTok 产品表添加 master_id"""
    db_path = Path("C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/tiktok.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查字段是否已存在
    cursor.execute("PRAGMA table_info(tiktok_products)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'master_id' not in columns:
        cursor.execute("ALTER TABLE tiktok_products ADD COLUMN master_id INTEGER REFERENCES product_master(id)")
        print("✅ Added master_id to TikTok products")
    else:
        print("ℹ️ master_id already exists in TikTok products")
    
    conn.commit()
    conn.close()


def link_existing_products():
    """关联现有产品到商品主库"""
    master_db = Path("C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/product_master.db")
    
    # 关联 Amazon
    amazon_db = Path("C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/amazon.db")
    conn_amazon = sqlite3.connect(amazon_db)
    cursor_amazon = conn_amazon.cursor()
    
    conn_master = sqlite3.connect(master_db)
    cursor_master = conn_master.cursor()
    
    # 获取所有 Amazon 产品
    cursor_amazon.execute("SELECT id, asin FROM products WHERE master_id IS NULL")
    amazon_products = cursor_amazon.fetchall()
    
    print(f"📦 Linking {len(amazon_products)} Amazon products...")
    
    for product_id, asin in amazon_products:
        # 从商品主库查找对应的 master_id
        cursor_master.execute("""
            SELECT id FROM product_master 
            WHERE platform = 'amazon' AND platform_id = ?
        """, (asin,))
        
        result = cursor_master.fetchone()
        if result:
            master_id = result[0]
            cursor_amazon.execute("UPDATE products SET master_id = ? WHERE id = ?", (master_id, product_id))
    
    conn_amazon.commit()
    conn_amazon.close()
    
    print(f"✅ Amazon products linked")
    
    # 关联 TikTok
    tiktok_db = Path("C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/tiktok.db")
    conn_tiktok = sqlite3.connect(tiktok_db)
    cursor_tiktok = conn_tiktok.cursor()
    
    cursor_tiktok.execute("SELECT id, tiktokshop_id FROM tiktok_products WHERE master_id IS NULL AND tiktokshop_id IS NOT NULL")
    tiktok_products = cursor_tiktok.fetchall()
    
    print(f"📦 Linking {len(tiktok_products)} TikTok products...")
    
    for product_id, tiktokshop_id in tiktok_products:
        cursor_master.execute("""
            SELECT id FROM product_master 
            WHERE platform = 'tiktok' AND platform_id = ?
        """, (tiktokshop_id,))
        
        result = cursor_master.fetchone()
        if result:
            master_id = result[0]
            cursor_tiktok.execute("UPDATE tiktok_products SET master_id = ? WHERE id = ?", (master_id, product_id))
    
    conn_tiktok.commit()
    conn_tiktok.close()
    conn_master.close()
    
    print(f"✅ TikTok products linked")


if __name__ == "__main__":
    print("=" * 60)
    print("Adding master_id to platform tables")
    print("=" * 60)
    
    add_master_id_to_amazon()
    add_master_id_to_tiktok()
    
    print("\n" + "=" * 60)
    print("Linking existing products...")
    print("=" * 60)
    link_existing_products()
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
