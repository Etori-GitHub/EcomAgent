import sqlite3
import json

# Read pending names
with open(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

ids = [item['id'] for item in data['items']]
print(f'Pending IDs count: {len(ids)}')
print(f'First 5 IDs: {ids[:5]}')

# Check database
db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

# Check what ecom_code format looks like
cursor = conn.execute('SELECT id, ecom_code, name, short_name FROM product_master LIMIT 5')
print('\nSample products:')
for r in cursor.fetchall():
    name_preview = r[2][:50] if r[2] else "NULL"
    print(f'  id={r[0]}, ecom_code={r[1]}, name={name_preview}..., short_name={r[3]}')

# Try to find by ecom_code
placeholders = ','.join(['?' for _ in ids[:10]])
cursor = conn.execute(f'SELECT ecom_code, name, short_name FROM product_master WHERE ecom_code IN ({placeholders})', ids[:10])
print(f'\nLookup by ecom_code:')
for r in cursor.fetchall():
    name_preview = r[1][:50] if r[1] else "NULL"
    print(f'  {r[0]}: name={name_preview}..., short_name={r[2]}')

conn.close()
