import sqlite3
import json

# 查看所有数据库名称信息

amazon_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
conn = sqlite3.connect(amazon_db)
c = conn.cursor()

# 查看 products 表结构和数据
print("Amazon products table structure:")
c.execute("PRAGMA table_info(products)")
for col in c.fetchall():
    print(f"  {col}")

# 查看 products 表数据量
c.execute("SELECT COUNT(*) FROM products")
print(f"Total products: {c.fetchone()[0]}")

# 查看有 name 的 products 数量
c.execute("SELECT COUNT(*) FROM products WHERE name IS NOT NULL AND name != ''")
print(f"Products with name: {c.fetchone()[0]}")

# 查看 pending 的 ASIN 列表
pending_asins = [
    'B0DDZMFDS3', 'B08VLMQ3KS', 'B0C21QMW48', 'B0BX4XG53Z', 'B0C544TBQM',
    'B0GY49NMDM', 'B0C1G2G2QK', 'B0BRYTP75X', 'B0CM6FRW8N', 'B0BVH5QWM8'
]

print("\nChecking pending ASINs:")
for asin in pending_asins:
    c.execute("SELECT * FROM products WHERE asin = ?", (asin,))
    row = c.fetchone()
    print(f"  {asin}: {row}")

# 查看 events 表是否有名称信息
print("\nChecking events table:")
c.execute("PRAGMA table_info(events)")
for col in c.fetchall():
    print(f"  {col}")

c.execute("SELECT * FROM events WHERE asin = 'B0DDZMFDS3' LIMIT 1")
print(f"Sample event: {c.fetchone()}")

conn.close()