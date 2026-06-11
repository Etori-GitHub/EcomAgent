import sqlite3

# Check for recent products
conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
cursor = conn.cursor()

# Check last_updated_at
cursor.execute('''
SELECT COUNT(*) FROM product_master 
WHERE datetime(last_updated_at) > datetime('now', '-1 day')
''')
recent = cursor.fetchone()[0]
print(f'Products updated in last 24h: {recent}')

# Check first_seen_at for new products
cursor.execute('''
SELECT COUNT(*) FROM product_master 
WHERE datetime(first_seen_at) > datetime('now', '-1 day')
''')
new_products = cursor.fetchone()[0]
print(f'New products in last 24h: {new_products}')

# Get latest 5 products
cursor.execute('''
SELECT ecom_code, name, short_name, first_seen_at 
FROM product_master 
ORDER BY first_seen_at DESC 
LIMIT 5
''')
latest = cursor.fetchall()
print('\nLatest 5 products:')
for p in latest:
    name_preview = p[1][:40] if p[1] else 'N/A'
    print(f'  {p[0]}: {name_preview}... -> {p[2]}')

conn.close()
