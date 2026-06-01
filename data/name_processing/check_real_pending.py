import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

# Check for products WITH name but WITHOUT short_name
cursor = conn.execute('''
    SELECT id, ecom_code, name, short_name 
    FROM product_master 
    WHERE name IS NOT NULL AND name != '' AND (short_name IS NULL OR short_name = '')
    LIMIT 20
''')
rows = cursor.fetchall()

if rows:
    print(f"Found {len(rows)} products with name but no short_name:")
    for r in rows:
        name_preview = (r[2][:60] + '...') if r[2] and len(r[2]) > 60 else (r[2] or 'N/A')
        print(f"  {r[1]}: {name_preview}")
else:
    print("All products with names already have short_name!")
    
    # Show count
    cursor = conn.execute('SELECT COUNT(*) FROM product_master WHERE name IS NOT NULL AND name != ""')
    total_with_name = cursor.fetchone()[0]
    cursor = conn.execute('SELECT COUNT(*) FROM product_master WHERE short_name IS NOT NULL AND short_name != ""')
    total_with_short = cursor.fetchone()[0]
    print(f"\nTotal products with name: {total_with_name}")
    print(f"Total products with short_name: {total_with_short}")

conn.close()
