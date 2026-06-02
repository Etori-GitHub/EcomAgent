import sqlite3
conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')

# Check products with names
cursor = conn.execute('''
    SELECT ecom_code, name, short_name, platform_id 
    FROM product_master 
    WHERE name IS NOT NULL AND name != "" 
    LIMIT 10
''')
print("Products with names:")
for row in cursor.fetchall():
    name_display = row[1][:50] + '...' if len(row[1]) > 50 else row[1]
    print(f"  {row[0]}: {name_display} | short: {row[2]} | ASIN: {row[3]}")

# Count products with/without names
cursor = conn.execute('SELECT COUNT(*) FROM product_master WHERE name IS NOT NULL AND name != ""')
with_name = cursor.fetchone()[0]
cursor = conn.execute('SELECT COUNT(*) FROM product_master WHERE name IS NULL OR name = ""')
without_name = cursor.fetchone()[0]
print(f"\nTotal: {with_name + without_name} | With names: {with_name} | Without names: {without_name}")

# Check products without short_name but with name
cursor = conn.execute('''
    SELECT ecom_code, name, platform_id 
    FROM product_master 
    WHERE (short_name IS NULL OR short_name = '') AND name IS NOT NULL AND name != ""
    LIMIT 10
''')
print("\nProducts with name but no short_name:")
for row in cursor.fetchall():
    name_display = row[1][:50] + '...' if len(row[1]) > 50 else row[1]
    print(f"  {row[0]}: {name_display} | ASIN: {row[2]}")
