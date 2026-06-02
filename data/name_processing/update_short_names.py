#!/usr/bin/env python3
"""将翻译结果更新到数据库"""
import sqlite3
import json
from pathlib import Path

# 读取翻译结果
processed_path = Path(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\processed_names.json')
with open(processed_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 连接数据库
db_path = Path(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 更新每条记录
updated = 0
for item in data['items']:
    ecom_code = item['id']
    short_name = item['short_name']
    
    cursor.execute(
        'UPDATE product_master SET short_name = ? WHERE ecom_code = ?',
        (short_name, ecom_code)
    )
    if cursor.rowcount > 0:
        updated += 1

conn.commit()
conn.close()

print(f'成功更新 {updated}/{len(data["items"])} 条记录')
