#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复数据库中缺失的 price/rating 数据
用于补救早期抓取/导入导致的数据缺失
"""

import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output" / "imported"


def fix_amazon_missing_prices():
    """修复 Amazon 缺失的 price 数据"""
    amazon_db = DATA_DIR / "amazon.db"
    conn = sqlite3.connect(amazon_db)
    cursor = conn.cursor()
    
    # 找出 price 为 NULL 的记录
    cursor.execute('''
        SELECT ds.id, ds.product_id, ds.date, p.asin
        FROM daily_sales ds
        JOIN products p ON ds.product_id = p.id
        WHERE ds.price IS NULL
    ''')
    
    null_records = cursor.fetchall()
    print(f"[INFO] 找到 {len(null_records)} 条 price 为 NULL 的记录")
    
    if not null_records:
        conn.close()
        return
    
    # 从 JSON 文件中查找对应的价格
    fixed = 0
    for record_id, product_id, date, asin in null_records:
        # 查找对应日期的 JSON 文件
        for json_file in OUTPUT_DIR.glob(f"amazon_*_{date.replace('-', '')}*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for product in data.get('products', []):
                    if product.get('asin') == asin and product.get('price'):
                        cursor.execute(
                            'UPDATE daily_sales SET price = ? WHERE id = ?',
                            (product['price'], record_id)
                        )
                        fixed += 1
                        break
            except Exception as e:
                print(f"[WARN] 处理文件 {json_file.name} 失败: {e}")
    
    conn.commit()
    conn.close()
    print(f"[OK] 修复了 {fixed} 条 Amazon price 记录")


def fix_tiktok_missing_ratings():
    """修复 TikTok 缺失的 rating 数据 - 需要重新抓取"""
    tiktok_db = DATA_DIR / "tiktok.db"
    conn = sqlite3.connect(tiktok_db)
    cursor = conn.cursor()
    
    # 统计 rating 为 NULL 的记录
    cursor.execute('SELECT COUNT(*) FROM tiktok_daily_sales WHERE rating IS NULL')
    null_count = cursor.fetchone()[0]
    
    conn.close()
    
    if null_count > 0:
        print(f"[INFO] TikTok 有 {null_count} 条 rating 为 NULL 的记录")
        print(f"[提示] TikTok rating 需要重新抓取数据才能补充")
        print(f"[提示] 请运行 TikTok 抓取脚本后重新导入")


if __name__ == "__main__":
    print("=" * 60)
    print("修复缺失的 price/rating 数据")
    print("=" * 60)
    
    fix_amazon_missing_prices()
    fix_tiktok_missing_ratings()
    
    print("\n[完成] 数据修复完成")