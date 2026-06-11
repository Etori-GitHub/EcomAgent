import sqlite3
import json
import os

# 连接数据库
master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(master_db)
c = conn.cursor()

# 获取已翻译商品（用于参考）
c.execute("""
    SELECT ecom_code, short_name, name
    FROM product_master
    WHERE translation_status = 'translated' AND name IS NOT NULL AND name != ''
    ORDER BY RANDOM()
    LIMIT 5
""")
translated_samples = c.fetchall()

print("已翻译商品名称模式分析:")
for row in translated_samples:
    ecom_code, short_name, name = row
    print(f"  ID: {ecom_code}")
    print(f"  short_name: {short_name}")
    if name:
        print(f"  original name: {name[:80]}...")
    print()

# 获取 pending 商品列表
c.execute("""
    SELECT ecom_code, platform, platform_id
    FROM product_master
    WHERE translation_status = 'pending'
    ORDER BY ecom_code
""")
pending_items = c.fetchall()

print(f"Pending 商品数量: {len(pending_items)}")
print(f"Pending 商品 ASIN 前10个: {[item[2] for item in pending_items[:10]]}")

conn.close()