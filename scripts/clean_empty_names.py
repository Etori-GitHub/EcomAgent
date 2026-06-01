#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据清洗脚本 - 删除空名称商品
"""

import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


def clean_empty_names():
    """删除名称为空的商品"""
    print(f"\n{'='*60}")
    print(f"数据清洗 - 删除空名称商品")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # 1. 商品总库
    master_db = DATA_DIR / "product_master.db"
    if master_db.exists():
        conn = sqlite3.connect(master_db)
        cursor = conn.cursor()
        
        # 查询空名称商品
        cursor.execute("SELECT id, ecom_code, platform, name FROM product_master WHERE name IS NULL OR name = ''")
        empty_items = cursor.fetchall()
        
        if empty_items:
            print(f"[product_master] 发现 {len(empty_items)} 个空名称商品:")
            for item in empty_items[:10]:
                print(f"  - id={item[0]}, ecom_code={item[1]}, platform={item[2]}")
            if len(empty_items) > 10:
                print(f"  ... 还有 {len(empty_items) - 10} 个")
            
            # 删除
            cursor.execute("DELETE FROM product_master WHERE name IS NULL OR name = ''")
            deleted = cursor.rowcount
            conn.commit()
            print(f"[OK] product_master: 删除了 {deleted} 条空名称记录")
        else:
            print(f"[OK] product_master: 没有空名称商品")
        
        conn.close()
    
    # 2. Amazon 数据库
    amazon_db = DATA_DIR / "amazon.db"
    if amazon_db.exists():
        conn = sqlite3.connect(amazon_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, asin, name FROM products WHERE name IS NULL OR name = ''")
        empty_items = cursor.fetchall()
        
        if empty_items:
            print(f"\n[amazon.products] 发现 {len(empty_items)} 个空名称商品:")
            for item in empty_items[:10]:
                print(f"  - id={item[0]}, asin={item[1]}")
            
            # 先删除关联的 daily_sales
            cursor.execute("""
                DELETE FROM daily_sales 
                WHERE product_id IN (SELECT id FROM products WHERE name IS NULL OR name = '')
            """)
            sales_deleted = cursor.rowcount
            
            cursor.execute("DELETE FROM products WHERE name IS NULL OR name = ''")
            deleted = cursor.rowcount
            conn.commit()
            print(f"[OK] amazon: 删除了 {deleted} 条商品记录, {sales_deleted} 条销售记录")
        else:
            print(f"\n[OK] amazon.products: 没有空名称商品")
        
        conn.close()
    
    # 3. TikTok 数据库
    tiktok_db = DATA_DIR / "tiktok.db"
    if tiktok_db.exists():
        conn = sqlite3.connect(tiktok_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, tiktokshop_id, name FROM tiktok_products WHERE name IS NULL OR name = ''")
        empty_items = cursor.fetchall()
        
        if empty_items:
            print(f"\n[tiktok_products] 发现 {len(empty_items)} 个空名称商品:")
            for item in empty_items[:10]:
                print(f"  - id={item[0]}, tiktokshop_id={item[1]}")
            
            # 删除关联的 daily_sales
            cursor.execute("""
                DELETE FROM tiktok_daily_sales 
                WHERE product_id IN (SELECT id FROM tiktok_products WHERE name IS NULL OR name = '')
            """)
            sales_deleted = cursor.rowcount
            
            cursor.execute("DELETE FROM tiktok_products WHERE name IS NULL OR name = ''")
            deleted = cursor.rowcount
            conn.commit()
            print(f"[OK] tiktok: 删除了 {deleted} 条商品记录, {sales_deleted} 条销售记录")
        else:
            print(f"\n[OK] tiktok_products: 没有空名称商品")
        
        conn.close()
    
    print(f"\n{'='*60}")
    print(f"数据清洗完成")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    clean_empty_names()