#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""初始化数据库"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "amazon.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 删除旧表
cursor.execute("DROP TABLE IF EXISTS daily_sales")
cursor.execute("DROP TABLE IF EXISTS products")

# 商品表
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

# 快照表
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

# 索引
cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON daily_sales(date)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON daily_sales(timestamp)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_date ON daily_sales(product_id, date)")

conn.commit()
conn.close()

print("Database initialized successfully!")
