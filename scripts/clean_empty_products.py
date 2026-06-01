#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理数据库：删除英文名称为空的商品
"""

import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def clean_amazon():
    """清理 Amazon 数据库"""
    print("=== 清理 Amazon 数据库 ===")
    db_path = DATA_DIR / "amazon.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # 统计
    cursor.execute("SELECT COUNT(*) FROM products WHERE name IS NULL OR name = ''")
    empty_names = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM products")
    total = cursor.fetchone()[0]
    print(f"总商品数: {total}")
    print(f"空名称商品: {empty_names}")
    
    # 获取要删除的商品 ID
    cursor.execute("SELECT id FROM products WHERE name IS NULL OR name = ''")
    ids_to_delete = [row[0] for row in cursor.fetchall()]
    
    if ids_to_delete:
        placeholders = ','.join('?' * len(ids_to_delete))
        
        # 删除销售记录
        cursor.execute(f"DELETE FROM daily_sales WHERE product_id IN ({placeholders})", ids_to_delete)
        sales_deleted = cursor.rowcount
        print(f"删除销售记录: {sales_deleted}")
        
        # 删除商品
        cursor.execute(f"DELETE FROM products WHERE id IN ({placeholders})", ids_to_delete)
        products_deleted = cursor.rowcount
        print(f"删除商品: {products_deleted}")
        
        conn.commit()
    else:
        print("没有需要删除的商品")
    
    conn.close()
    return products_deleted if ids_to_delete else 0

def clean_tiktok():
    """清理 TikTok 数据库"""
    print("\n=== 清理 TikTok 数据库 ===")
    db_path = DATA_DIR / "tiktok.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # 统计
    cursor.execute("SELECT COUNT(*) FROM tiktok_products WHERE name IS NULL OR name = ''")
    empty_names = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tiktok_products")
    total = cursor.fetchone()[0]
    print(f"总商品数: {total}")
    print(f"空名称商品: {empty_names}")
    
    if empty_names > 0:
        # 获取要删除的商品 ID
        cursor.execute("SELECT id FROM tiktok_products WHERE name IS NULL OR name = ''")
        ids_to_delete = [row[0] for row in cursor.fetchall()]
        
        placeholders = ','.join('?' * len(ids_to_delete))
        
        # 删除销售记录
        cursor.execute(f"DELETE FROM tiktok_daily_sales WHERE product_id IN ({placeholders})", ids_to_delete)
        sales_deleted = cursor.rowcount
        print(f"删除销售记录: {sales_deleted}")
        
        # 删除商品
        cursor.execute(f"DELETE FROM tiktok_products WHERE id IN ({placeholders})", ids_to_delete)
        products_deleted = cursor.rowcount
        print(f"删除商品: {products_deleted}")
        
        conn.commit()
    else:
        print("没有需要删除的商品")
        products_deleted = 0
    
    conn.close()
    return products_deleted

def clean_product_master():
    """清理商品主库"""
    print("\n=== 清理商品主库 ===")
    db_path = DATA_DIR / "product_master.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # 统计
    cursor.execute("SELECT COUNT(*) FROM product_master WHERE name IS NULL OR name = ''")
    empty_names = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM product_master")
    total = cursor.fetchone()[0]
    print(f"总商品数: {total}")
    print(f"空名称商品: {empty_names}")
    
    if empty_names > 0:
        # 删除空名称商品
        cursor.execute("DELETE FROM product_master WHERE name IS NULL OR name = ''")
        products_deleted = cursor.rowcount
        print(f"删除商品: {products_deleted}")
        conn.commit()
    else:
        print("没有需要删除的商品")
        products_deleted = 0
    
    conn.close()
    return products_deleted

def reset_translation_status():
    """将所有商品标记为未翻译"""
    print("\n=== 重置翻译状态 ===")
    db_path = DATA_DIR / "product_master.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # 更新所有商品的翻译状态为 pending
    cursor.execute("UPDATE product_master SET translation_status = 'pending'")
    updated = cursor.rowcount
    conn.commit()
    
    # 统计
    cursor.execute("SELECT COUNT(*) FROM product_master WHERE translation_status = 'pending'")
    pending = cursor.fetchone()[0]
    
    conn.close()
    print(f"已将 {updated} 个商品标记为待翻译")
    return updated

def main():
    print("开始清理数据库...\n")
    
    amazon_deleted = clean_amazon()
    tiktok_deleted = clean_tiktok()
    master_deleted = clean_product_master()
    translation_reset = reset_translation_status()
    
    print(f"\n{'='*60}")
    print("清理完成!")
    print(f"Amazon 删除: {amazon_deleted}")
    print(f"TikTok 删除: {tiktok_deleted}")
    print(f"商品主库删除: {master_deleted}")
    print(f"翻译状态重置: {translation_reset}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
