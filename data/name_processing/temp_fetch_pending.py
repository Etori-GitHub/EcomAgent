import sqlite3
import json

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查询待翻译的商品
cursor.execute("SELECT ecom_code, name FROM product_master WHERE translation_status = 'pending' LIMIT 50")
rows = cursor.fetchall()

result = {
    'batch_id': 'batch_20260604_1731',
    'items': [{'id': row[0], 'name': row[1]} for row in rows]
}

print(json.dumps(result, ensure_ascii=False, indent=2))
conn.close()
