import sqlite3

# Check product_master for products without short_name
conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
cursor = conn.cursor()

# Get total count
cursor.execute('SELECT COUNT(*) FROM product_master')
total = cursor.fetchone()[0]

# Get count with short_name
cursor.execute("SELECT COUNT(*) FROM product_master WHERE short_name IS NOT NULL AND short_name != ''")
with_name = cursor.fetchone()[0]

print(f'Total products: {total}')
print(f'Products with short_name: {with_name}')
print(f'Products without short_name: {total - with_name}')

# Get sample of products
cursor.execute('SELECT ecom_code, name, short_name FROM product_master LIMIT 5')
samples = cursor.fetchall()
print('\nSample products:')
for s in samples:
    name_preview = s[1][:50] if s[1] else 'N/A'
    print(f'  {s[0]}: {name_preview}... -> {s[2]}')

conn.close()