import sqlite3
import json
from datetime import datetime

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

# 查找有名称但没有 short_name 的产品
cursor = conn.execute("""
    SELECT ecom_code, name, short_name 
    FROM product_master 
    WHERE short_name IS NULL
    LIMIT 20
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: name='{row[1]}', short_name='{row[2]}'")