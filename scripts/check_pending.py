#!/usr/bin/env python3
import sqlite3
conn = sqlite3.connect('data/product_master.db')
cursor = conn.cursor()

# 检查表结构
cursor.execute('PRAGMA table_info(product_master)')
columns = [col[1] for col in cursor.fetchall()]
print(f"表结构: {columns}")

# 检查最近导入的商品（按 id 排序）
cursor.execute('''
    SELECT ecom_code, name, short_name, translation_status
    FROM product_master 
    ORDER BY id DESC
    LIMIT 20
''')
rows = cursor.fetchall()
print("\n最近导入的商品:")
for row in rows:
    ecom_code, name, short_name, status = row
    name_preview = (name[:50] + "...") if name and len(name) > 50 else (name or "(空)")
    short_preview = short_name or "(无)"
    print(f"{ecom_code}: {name_preview} -> {short_preview} [{status}]")

conn.close()