#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""保存亚马逊热销数据"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "amazon.db")

# 示例数据（Electronics 分类前 5 个商品）
products = [
    {
        'name': 'blink plus plan with monthly auto-renewal',
        'asin': 'B08JHCVHTY',
        'price': 11.99,
        'rank': 1,
        'rating': 4.4,
        'rating_count': 273418,
        'category': 'Electronics',
        'subcategory': 'Best Sellers in Electronics',
        'platform': 'amazon'
    },
    {
        'name': 'Apple EarPods Headphones with USB-C Plug, Wired Ear Buds with Built-in Remote to Control Music, Phone Calls, and Volume',
        'asin': 'B0DCH8VDXF',
        'price': 19.00,
        'rank': 2,
        'rating': 4.6,
        'rating_count': 11544,
        'category': 'Electronics',
        'subcategory': 'Best Sellers in Electronics',
        'platform': 'amazon'
    },
    {
        'name': 'Apple AirPods 4 Wireless Earbuds, Bluetooth Headphones, Personalized Spatial Audio, Sweat and Water Resistant, USB-C Charging Case, H2 Chip, Up to 30 Hours of Battery Life, Effortless Setup for iPhone',
        'asin': 'B0DGHMNQ5Z',
        'price': 114.95,
        'rank': 3,
        'rating': 4.5,
        'rating_count': 44891,
        'category': 'Electronics',
        'subcategory': 'Best Sellers in Electronics',
        'platform': 'amazon'
    },
    {
        'name': 'Apple AirTag 2nd Generation Tracker',
        'asin': 'B0GJTFXNRX',
        'price': 29.00,
        'rank': 4,
        'rating': 4.6,
        'rating_count': 1216,
        'category': 'Electronics',
        'subcategory': 'Best Sellers in Electronics',
        'platform': 'amazon'
    },
    {
        'name': 'Apple AirPods Pro 3 Wireless Earbuds, Active Noise Cancellation, Live Translation, Heart Rate Sensing, Hearing Aid Feature, Bluetooth Headphones, Spatial Audio, High-Fidelity Sound, USB-C Charging',
        'asin': 'B0FQFB8FMG',
        'price': 224.00,
        'rank': 5,
        'rating': 4.4,
        'rating_count': 7179,
        'category': 'Electronics',
        'subcategory': 'Best Sellers in Electronics',
        'platform': 'amazon'
    }
]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 保存商品
for product in products:
    # 检查 asin 是否存在
    cursor.execute("SELECT id FROM products WHERE asin = ?", (product['asin'],))
    existing = cursor.fetchone()
    
    if existing:
        product_id = existing[0]
    else:
        cursor.execute("""
        INSERT INTO products (asin, name, platform, category, subcategory, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            product['asin'],
            product['name'],
            product['platform'],
            product['category'],
            product['subcategory'],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        product_id = cursor.lastrowid
    
    # 保存快照
    date = datetime.now().strftime('%Y-%m-%d')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute("""
    INSERT INTO daily_sales (product_id, date, timestamp, price, rank, rating, rating_count, category, subcategory, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        product_id,
        date,
        timestamp,
        product['price'],
        product['rank'],
        product['rating'],
        product['rating_count'],
        product['category'],
        product['subcategory'],
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))

conn.commit()
conn.close()

print(f"[OK] 保存成功: {len(products)} 个商品")

# 查询结果
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
SELECT p.name, ds.price, ds.rating, ds.rating_count, ds.category, ds.created_at
FROM daily_sales ds
JOIN products p ON ds.product_id = p.id
ORDER BY ds.rank
LIMIT 10
""")
results = cursor.fetchall()
conn.close()

print("\n=== 热销商品 Top 10 ===")
for i, (name, price, rating, rating_count, category, created_at) in enumerate(results, 1):
    print(f"{i}. {name}")
    print(f"   价格: ${price:.2f} | 评分: {rating} ({rating_count:,} 评论)")
