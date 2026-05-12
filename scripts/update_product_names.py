#!/usr/bin/env python3
"""
更新现有数据库中的商品名
使用智能提取器从完整标题中提取真正的商品名
"""

import sqlite3
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))
from extract_product_name import extract_product_name


def update_product_master_names():
    """更新商品主库的商品名"""
    db_path = Path("C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/product_master.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 获取所有商品
    cursor.execute("SELECT id, search_keyword FROM product_master WHERE search_keyword IS NOT NULL")
    products = cursor.fetchall()
    
    print(f"📦 Updating {len(products)} products in product_master...")
    
    updated = 0
    for product_id, search_keyword in products:
        if not search_keyword:
            continue
        
        # 提取商品名
        product_name = extract_product_name(search_keyword)
        
        # 更新
        cursor.execute("UPDATE product_master SET name = ? WHERE id = ?", (product_name, product_id))
        updated += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ Updated {updated} products in product_master")


def update_amazon_names():
    """更新 Amazon 数据库的商品名"""
    db_path = Path("C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/amazon.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 获取所有商品
    cursor.execute("SELECT id, search_keyword FROM products WHERE search_keyword IS NOT NULL")
    products = cursor.fetchall()
    
    print(f"📦 Updating {len(products)} products in Amazon...")
    
    updated = 0
    for product_id, search_keyword in products:
        if not search_keyword:
            continue
        
        # 提取商品名
        product_name = extract_product_name(search_keyword)
        
        # 更新
        cursor.execute("UPDATE products SET name = ? WHERE id = ?", (product_name, product_id))
        updated += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ Updated {updated} products in Amazon")


def update_tiktok_names():
    """更新 TikTok 数据库的商品名"""
    db_path = Path("C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/tiktok.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 获取所有商品
    cursor.execute("SELECT id, search_keyword FROM tiktok_products WHERE search_keyword IS NOT NULL")
    products = cursor.fetchall()
    
    print(f"📦 Updating {len(products)} products in TikTok...")
    
    updated = 0
    for product_id, search_keyword in products:
        if not search_keyword:
            continue
        
        # 提取商品名
        product_name = extract_product_name(search_keyword)
        
        # 更新
        cursor.execute("UPDATE tiktok_products SET name = ? WHERE id = ?", (product_name, product_id))
        updated += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ Updated {updated} products in TikTok")


if __name__ == "__main__":
    print("=" * 60)
    print("Updating Product Names")
    print("=" * 60)
    
    update_product_master_names()
    print()
    update_amazon_names()
    print()
    update_tiktok_names()
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
