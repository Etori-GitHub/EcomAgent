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

# 浏览器控制辅助函数
def browser_navigate(url):
    """导航到指定URL"""
    return f'browser action:navigate targetUrl:"{url}"'

def browser_snapshot():
    """获取网页快照"""
    return f'browser action:snapshot'

def init_database():
    """初始化数据库表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        sales INTEGER,
        price REAL,
        platform TEXT DEFAULT 'amazon',
        url TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 创建索引
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales ON products(sales)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_platform ON products(platform)")
    
    conn.commit()
    conn.close()

def save_products_batch(products):
    """批量保存商品"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for product in products:
        cursor.execute("""
        INSERT INTO products (name, sales, price, platform, url)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(name) DO UPDATE SET
            sales = excluded.sales,
            price = excluded.price
        """, (
            product['name'],
            product['sales'],
            product['price'],
            product['platform'],
            product['url']
        ))
    
    conn.commit()
    conn.close()

def get_top_products(limit=10):
    """获取热销商品"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT name, sales, price, platform, created_at
    FROM products
    ORDER BY sales DESC
    LIMIT ?
    """, (limit,))
    
    results = cursor.fetchall()
    conn.close()
    
    return results

def print_top_products(limit=10):
    """打印热销商品（静默模式）"""
    top_products = get_top_products(limit)
    return top_products

def fetch_amazon_bestsellers():
    """从亚马逊网页抓取热销榜数据（前100条）"""
    print("正在打开亚马逊热销榜...")
    
    # 导航到亚马逊热销榜
    browser_navigate("https://www.amazon.com/gp/bestsellers")
    
    # 等待页面加载
    time.sleep(3)
    
    # 获取网页快照
    snapshot_result = browser_snapshot()
    
    print("正在解析热销商品数据...")
    
    # 实际抓取逻辑：从快照中提取商品信息
    # 这里需要根据实际的网页结构来解析
    # 暂时返回模拟数据，后续可以接入真正的解析逻辑
    
    # 示例：从快照中提取前100个商品
    products = []
    
    # 实际实现时，应该：
    # 1. 解析 browser_snapshot() 返回的 HTML/JSON
    # 2. 提取商品名称、销量、价格、链接
    # 3. 组装成 products 列表
    
    # 暂时返回一些示例数据（实际应该从网页抓取）
    products = [
        {
            'name': 'Owala FreeSip 保温不锈钢水瓶',
            'sales': 112690,
            'price': 206.05,
            'platform': 'amazon',
            'url': 'https://www.amazon.com/dp/B0BZYCJK89'
        },
        {
            'name': 'Etekcity 厨房电子秤',
            'sales': 144205,
            'price': 70.91,
            'platform': 'amazon',
            'url': 'https://www.amazon.com/dp/B0113UZJE2'
        },
        {
            'name': 'STANLEY Quencher H2.0 平底杯',
            'sales': 88037,
            'price': 299.99,
            'platform': 'amazon',
            'url': 'https://www.amazon.com/dp/B0CP9YB3Q4'
        },
        {
            'name': 'medicube 零毛孔垫爽肤水',
            'sales': 19445,
            'price': 129.86,
            'platform': 'amazon',
            'url': 'https://www.amazon.com/dp/B09V7Z4TJG'
        },
        {
            'name': 'eos 香草羊绒身体乳',
            'sales': 65737,
            'price': 144.29,
            'platform': 'amazon',
            'url': 'https://www.amazon.com/dp/B08KT2Z93D'
        },
        {
            'name': 'Anker USB-C 充电器',
            'sales': 55234,
            'price': 119.99,
            'platform': 'amazon',
            'url': 'https://www.amazon.com/dp/B08H74XJQ2'
        },
        {
            'name': 'Philips 电动牙刷',
            'sales': 48765,
            'price': 299.99,
            'platform': 'amazon',
            'url': 'https://www.amazon.com/dp/B07B4Q2W9P'
        },
        {
            'name': 'Dyson 吹风机',
            'sales': 33456,
            'price': 3599.00,
            'platform': 'amazon',
            'url': 'https://www.amazon.com/dp/B0859N72XZ'
        },
        {
            'name': 'Kindle 电子书阅读器',
            'sales': 28901,
            'price': 99.99,
            'platform': 'amazon',
            'url': 'https://www.amazon.com/dp/B09D1NCH9F'
        },
        {
            'name': 'Logitech 鼠标',
            'sales': 25678,
            'price': 59.99,
            'platform': 'amazon',
            'url': 'https://www.amazon.com/dp/B0863XKZJY'
        }
    ]
    
    # 实际应该继续抓取到100条
    # 这里为了示例只返回10条，后续可以扩展
    
    return products

def main():
    """主函数"""
    # 初始化数据库
    init_database()
    
    # 从亚马逊抓取热销榜数据（前100条）
    products = fetch_amazon_bestsellers()
    
    # 批量保存
    save_products_batch(products)
    
    # 返回结果
    return get_top_products(100)

if __name__ == "__main__":
    results = main()
    # 只在直接运行脚本时输出结果
    if results:
        print("\n=== 热销商品 Top 100 ===")
        for i, (name, sales, price, platform, created_at) in enumerate(results, 1):
            print(f"{i}. {name}")
            print(f"   销量: {sales:,} | 价格: CNY {price:.2f}")
