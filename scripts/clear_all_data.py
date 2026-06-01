#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清除所有商品数据（不删库，只清空表）
"""

import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def clear_amazon():
    """清除 Amazon 数据库"""
    print("=== 清除 Amazon 数据库 ===")
    db_path = DATA_DIR / "amazon.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # 清空表数据
    cursor.execute("DELETE FROM daily_sales")
    sales_deleted = cursor.rowcount
    print(f"清空 daily_sales: {sales_deleted} 条")
    
    cursor.execute("DELETE FROM products")
    products_deleted = cursor.rowcount
    print(f"清空 products: {products_deleted} 条")
    
    # 重置自增 ID
    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('products', 'daily_sales')")
    
    conn.commit()
    conn.close()
    print("Amazon 数据库已清空\n")

def clear_tiktok():
    """清除 TikTok 数据库"""
    print("=== 清除 TikTok 数据库 ===")
    db_path = DATA_DIR / "tiktok.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM tiktok_daily_sales")
    sales_deleted = cursor.rowcount
    print(f"清空 tiktok_daily_sales: {sales_deleted} 条")
    
    cursor.execute("DELETE FROM tiktok_products")
    products_deleted = cursor.rowcount
    print(f"清空 tiktok_products: {products_deleted} 条")
    
    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('tiktok_products', 'tiktok_daily_sales')")
    
    conn.commit()
    conn.close()
    print("TikTok 数据库已清空\n")

def clear_product_master():
    """清除商品主库"""
    print("=== 清除商品主库 ===")
    db_path = DATA_DIR / "product_master.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM product_master")
    products_deleted = cursor.rowcount
    print(f"清空 product_master: {products_deleted} 条")
    
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'product_master'")
    
    conn.commit()
    conn.close()
    print("商品主库已清空\n")

def clear_categories():
    """清除分类数据库"""
    print("=== 清除分类数据库 ===")
    
    # categories.db
    db_path = DATA_DIR / "categories.db"
    if db_path.exists():
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for (table,) in tables:
            cursor.execute(f"DELETE FROM {table}")
            print(f"清空 {table}: {cursor.rowcount} 条")
        
        conn.commit()
        conn.close()
    
    # category_daily.db
    db_path = DATA_DIR / "category_daily.db"
    if db_path.exists():
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for (table,) in tables:
            cursor.execute(f"DELETE FROM {table}")
            print(f"清空 {table}: {cursor.rowcount} 条")
        
        conn.commit()
        conn.close()
    
    print("分类数据库已清空\n")

def clear_sourcing():
    """清除货源数据库"""
    print("=== 清除货源数据库 ===")
    db_path = DATA_DIR / "sourcing.db"
    if db_path.exists():
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM sourcing_1688")
        print(f"清空 sourcing_1688: {cursor.rowcount} 条")
        
        conn.commit()
        conn.close()
    print("货源数据库已清空\n")

def clear_tasks():
    """清除任务数据库"""
    print("=== 清除任务数据库 ===")
    db_path = DATA_DIR / "tasks.db"
    if db_path.exists():
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM tasks")
        print(f"清空 tasks: {cursor.rowcount} 条")
        
        conn.commit()
        conn.close()
    print("任务数据库已清空\n")

def clear_name_processing():
    """清除翻译处理目录中的JSON文件"""
    print("=== 清除翻译处理文件 ===")
    processing_dir = DATA_DIR / "name_processing"
    if processing_dir.exists():
        import os
        for f in processing_dir.glob("*.json"):
            f.unlink()
            print(f"删除: {f.name}")
    print("翻译处理文件已清空\n")

def main():
    print("开始清除所有商品数据...\n")
    
    clear_amazon()
    clear_tiktok()
    clear_product_master()
    clear_categories()
    clear_sourcing()
    clear_tasks()
    clear_name_processing()
    
    print("="*60)
    print("所有商品数据已清除完成！")
    print("数据库结构保留，可以重新抓取数据。")
    print("="*60)

if __name__ == "__main__":
    main()
