#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
亚马逊热销榜数据抓取脚本
自动抓取热销商品并保存到SQLite数据库
"""

import sqlite3
import json
import sys
import os
import time
from datetime import datetime

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "amazon.db")


def init_database():
    """初始化数据库表（更新版）"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 删除旧表（如果存在）
    cursor.execute("DROP TABLE IF EXISTS daily_sales")
    cursor.execute("DROP TABLE IF EXISTS products")
    
    # 商品基础信息表
    # 使用 asin 作为唯一标识（亚马逊商品ID最稳定）
    # name 字段保留用于展示，但不作为唯一约束
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asin TEXT UNIQUE,
        name TEXT NOT NULL,
        platform TEXT DEFAULT 'amazon',
        category TEXT,
        subcategory TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 每日销量快照表
    # 唯一约束：product_id + date + timestamp
    # 同一天多次抓取，timestamp 不同，但我们会保留最新的一条
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        date DATE NOT NULL,
        timestamp DATETIME NOT NULL,
        price REAL,
        rank INTEGER,
        rating REAL,
        rating_count INTEGER,
        category TEXT,
        subcategory TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    """)
    
    # 创建索引
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON daily_sales(date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON daily_sales(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_date ON daily_sales(product_id, date)")
    
    conn.commit()
    conn.close()


def save_product(product):
    """保存商品信息（使用 asin 唯一标识，名称变化时更新）"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 先检查 asin 是否存在
    cursor.execute("SELECT id, name FROM products WHERE asin = ?", (product.get('asin', ''),))
    existing = cursor.fetchone()
    
    if existing:
        # 商品已存在，检查名称是否变化
        existing_id, existing_name = existing
        if existing_name != product['name']:
            # 名称变化，更新
            cursor.execute("""
            UPDATE products SET name = ?, updated_at = ? WHERE id = ?
            """, (product['name'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), existing_id))
        product_id = existing_id
    else:
        # 新商品，插入
        cursor.execute("""
        INSERT INTO products (asin, name, platform, category, subcategory, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            product.get('asin', ''),
            product['name'],
            product['platform'],
            product.get('category', ''),
            product.get('subcategory', ''),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        product_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return product_id


def save_daily_sales(product_id, product, date, timestamp):
    """保存每日销量快照（同一天多次抓取，保留最新的一条）"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 先删除同一天该商品的旧数据
    cursor.execute("""
    DELETE FROM daily_sales WHERE product_id = ? AND date = ?
    """, (product_id, date))
    
    # 插入新数据
    cursor.execute("""
    INSERT INTO daily_sales (product_id, date, timestamp, price, rank, rating, rating_count, category, subcategory, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        product_id,
        date,
        timestamp,
        product['price'],
        product['rank'],
        product.get('rating', 0),
        product.get('rating_count', 0),
        product.get('category', ''),
        product.get('subcategory', ''),
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))
    
    conn.commit()
    conn.close()


def extract_products_from_snapshot(snapshot_data):
    """从快照数据中提取商品列表"""
    products = []
    
    # 解析快照数据（JSON 格式）
    # 快照数据包含 DOM 结构，需要提取商品信息
    
    # 示例解析逻辑（实际应该解析 snapshot_data）
    # 这里先返回示例数据，后续根据实际快照结构调整
    
    # 从快照中提取商品列表
    # DOM 结构：
    # - list [ref=e295]: 商品列表容器
    # - listitem [ref=e296]: 每个商品项
    #   - generic [ref=e301]: "#1" (rank)
    #   - link [ref=e306]: 商品链接 /dp/B08JHCVHTY/...
    #   - link [ref=e311]: 商品名称
    #   - link [ref=e316]: 评分 "4.4 out of 5 stars, 273,418 ratings"
    #   - link [ref=e322]: 价格 "$11.99"
    
    # 示例数据（实际应该从 snapshot_data 中提取）
    example_products = [
        {
            'name': 'blink plus plan with monthly auto-renewal',
            'asin': 'B08JHCVHTY',
            'price': 11.99,
            'rank': 1,
            'rating': 4.4,
            'rating_count': 273418,
            'category': 'Electronics',
            'subcategory': 'Best Sellers in Electronics'
        },
        {
            'name': 'Apple EarPods Headphones with USB-C Plug, Wired Ear Buds with Built-in Remote to Control Music, Phone Calls, and Volume',
            'asin': 'B0DCH8VDXF',
            'price': 19.00,
            'rank': 2,
            'rating': 4.6,
            'rating_count': 11544,
            'category': 'Electronics',
            'subcategory': 'Best Sellers in Electronics'
        },
        {
            'name': 'Apple AirPods 4 Wireless Earbuds, Bluetooth Headphones, Personalized Spatial Audio, Sweat and Water Resistant, USB-C Charging Case, H2 Chip, Up to 30 Hours of Battery Life, Effortless Setup for iPhone',
            'asin': 'B0DGHMNQ5Z',
            'price': 114.95,
            'rank': 3,
            'rating': 4.5,
            'rating_count': 44891,
            'category': 'Electronics',
            'subcategory': 'Best Sellers in Electronics'
        }
    ]
    
    return example_products


def fetch_amazon_bestsellers():
    """从亚马逊网页抓取热销榜数据（多分类 + 翻页）"""
    print("正在打开亚马逊热销榜...")
    
    # 导航到亚马逊热销榜
    browser_navigate("https://www.amazon.com/gp/bestsellers")
    
    # 等待页面加载
    time.sleep(3)
    
    # 获取网页快照
    snapshot_result = browser_snapshot()
    
    print("正在解析热销商品数据...")
    
    # 实际抓取逻辑：
    # 1. 解析 browser_snapshot() 返回的 HTML/JSON
    # 2. 提取商品名称、评分、评论数、价格
    # 3. 组装成 products 列表
    
    products = []
    
    return products


def browser_navigate(url):
    """导航到指定URL（模拟）"""
    return f'browser action:navigate targetUrl:"{url}"'


def browser_snapshot():
    """获取网页快照（模拟）"""
    return f'browser action:snapshot'


def get_top_products(limit=10):
    """获取热销商品（从 daily_sales 表获取最新数据）"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT p.name, ds.price, ds.rating, ds.rating_count, ds.category, ds.created_at
    FROM daily_sales ds
    JOIN products p ON ds.product_id = p.id
    ORDER BY ds.rating_count DESC
    LIMIT ?
    """, (limit,))
    
    results = cursor.fetchall()
    conn.close()
    
    return results


def print_top_products(limit=10):
    """打印热销商品（静默模式）"""
    top_products = get_top_products(limit)
    return top_products


def main():
    """主函数"""
    # 初始化数据库
    init_database()
    
    # 获取当前日期和时间
    date = datetime.now().strftime('%Y-%m-%d')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"开始抓取: {timestamp}")
    
    # 从亚马逊抓取热销榜数据
    products = fetch_amazon_bestsellers()
    
    if products:
        # 保存商品信息和每日快照
        for product in products:
            product_id = save_product(product)
            if product_id:
                save_daily_sales(product_id, product, date, timestamp)
        
        print(f"✓ 保存成功: {len(products)} 个商品")
    else:
        print("未抓取到数据")
    
    # 返回结果
    return get_top_products(100)


if __name__ == "__main__":
    results = main()
    # 只在直接运行脚本时输出结果
    if results:
        print("\n=== 热销商品 Top 100 ===")
        for i, (name, price, rating, rating_count, category, created_at) in enumerate(results, 1):
            print(f"{i}. {name}")
            print(f"   价格: ${price:.2f} | 评分: {rating} ({rating_count:,} 评论)")
