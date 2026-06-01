import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')

# Check products without short_name
cursor = conn.execute('''
    SELECT id, ecom_code, name, product_url
    FROM product_master 
    WHERE short_name IS NULL OR short_name = ''
    LIMIT 10
''')
rows = cursor.fetchall()

print(f"Products without short_name (sample):")
for row in rows:
    print(f"\nID: {row[0]}")
    print(f"  ecom_code: {row[1]}")
    print(f"  name: [{row[2]}]")
    print(f"  url: {row[3][:80] if row[3] else 'None'}...")

# Count total
cursor = conn.execute('SELECT COUNT(*) FROM product_master WHERE short_name IS NULL OR short_name = ""')
total = cursor.fetchone()[0]
print(f"\n\nTotal products without short_name: {total}")

conn.close()
