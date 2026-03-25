#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""查看数据库内容"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "amazon.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=== 商品表 (products) ===")
cursor.execute("SELECT * FROM products")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, ASIN: {row[1]}, Name: {row[2]}, Category: {row[4]}")

print("\n=== 快照表 (daily_sales) ===")
cursor.execute("""
SELECT p.asin, p.name, ds.date, ds.timestamp, ds.price, ds.rank, ds.rating, ds.rating_count
FROM daily_sales ds
JOIN products p ON ds.product_id = p.id
ORDER BY ds.rank
""")
for row in cursor.fetchall():
    print(f"ASIN: {row[0]}, Name: {row[1]}, Date: {row[2]}, Price: ${row[4]:.2f}, Rank: {row[5]}, Rating: {row[6]} ({row[7]:,})")

conn.close()
