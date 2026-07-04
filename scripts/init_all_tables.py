#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化 Amazon 和 TikTok 数据库表结构
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


def init_amazon_db():
    """创建 Amazon 数据库表"""
    db_path = DATA_DIR / "amazon.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # products 表 - 商品信息
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asin TEXT UNIQUE NOT NULL,
            name TEXT,
            image_url TEXT,
            product_url TEXT,
            category TEXT,
            master_id INTEGER,
            local_image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # daily_sales 表 - 每日销售数据
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            price REAL,
            rating REAL,
            rating_count INTEGER,
            rank INTEGER,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id),
            UNIQUE(product_id, date)
        )
    ''')
    
    # events 表 - 事件记录
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            old_value TEXT,
            new_value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_asin ON products(asin)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sales_product ON daily_sales(product_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sales_date ON daily_sales(date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_product ON events(product_id)')
    
    conn.commit()
    conn.close()
    print(f"[OK] amazon.db 表结构初始化完成")


def init_tiktok_db():
    """创建 TikTok 数据库表"""
    db_path = DATA_DIR / "tiktok.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # tiktok_products 表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tiktok_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tiktokshop_id TEXT UNIQUE,
            name TEXT,
            image_url TEXT,
            product_url TEXT,
            category TEXT,
            master_id INTEGER,
            local_image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # tiktok_daily_sales 表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tiktok_daily_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            price REAL,
            rating REAL,
            sales_count INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES tiktok_products(id),
            UNIQUE(product_id, date)
        )
    ''')
    
    # tiktok_events 表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tiktok_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            old_value TEXT,
            new_value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES tiktok_products(id)
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tiktok_id ON tiktok_products(tiktokshop_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tiktok_sales_product ON tiktok_daily_sales(product_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tiktok_sales_date ON tiktok_daily_sales(date)')
    
    conn.commit()
    conn.close()
    print(f"[OK] tiktok.db 表结构初始化完成")


def init_product_master_db():
    """创建商品主库表"""
    db_path = DATA_DIR / "product_master.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_master (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ecom_code TEXT UNIQUE NOT NULL,
            platform TEXT NOT NULL,
            platform_id TEXT NOT NULL,
            product_url TEXT,
            name TEXT,
            short_name TEXT,
            search_keyword TEXT,
            category TEXT,
            first_seen_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(platform, platform_id)
        )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_platform ON product_master(platform)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_platform_id ON product_master(platform_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_ecom_code ON product_master(ecom_code)')
    
    conn.commit()
    conn.close()
    print(f"[OK] product_master.db 表结构初始化完成")


if __name__ == "__main__":
    print("=" * 60)
    print("初始化 EcomAgent 数据库表结构")
    print("=" * 60)
    
    init_amazon_db()
    init_tiktok_db()
    init_product_master_db()
    
    print("\n全部数据库表结构初始化完成！")