import sqlite3
import json
import uuid

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
c = conn.execute('''
    SELECT id, ecom_code, name 
    FROM product_master 
    WHERE (short_name IS NULL OR short_name = '') 
    AND name IS NOT NULL AND name != ''
    LIMIT 100
''')
rows = c.fetchall()
conn.close()

items = [{"id": r[1], "name": r[2]} for r in rows]

data = {
    "batch_id": str(uuid.uuid4()),
    "items": items
}

output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Generated {len(items)} items')
print(f'Output: {output_path}')
for item in items[:5]:
    print(f'{item["id"]}: {item["name"][:60]}...' if len(item["name"]) > 60 else f'{item["id"]}: {item["name"]}')