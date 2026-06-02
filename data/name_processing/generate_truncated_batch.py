import sqlite3
import json
import uuid
from datetime import datetime

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

# 查找 short_name 只是截断版本的商品
truncated = conn.execute('''
    SELECT ecom_code, name, short_name 
    FROM product_master 
    WHERE short_name IS NOT NULL 
    AND short_name != ''
    AND name IS NOT NULL
    AND (
        short_name = SUBSTR(name, 1, 15)
        OR short_name = SUBSTR(name, 1, 14)
        OR short_name = SUBSTR(name, 1, 13)
        OR short_name = name
    )
    ORDER BY ecom_code
''').fetchall()

print(f'Found {len(truncated)} products with truncated short_name')

# 创建待翻译批次
batch_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
items = []

for t in truncated:
    items.append({
        'id': t[0],
        'name': t[1]
    })

data = {
    'batch_id': batch_id,
    'items': items
}

# 保存到 pending_names.json
output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Created batch: {batch_id}')
print(f'Total items: {len(items)}')
print(f'Saved to: {output_path}')

conn.close()
