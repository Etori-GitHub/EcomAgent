import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

# Check for products without short_name
cursor = conn.execute('''
    SELECT id, ecom_code, name, short_name 
    FROM product_master 
    WHERE short_name IS NULL OR short_name = ''
    LIMIT 20
''')
rows = cursor.fetchall()

if rows:
    print(f"Found {len(rows)} products without short_name:")
    for r in rows:
        print(f"  {r[1]}: {r[2][:60] if r[2] else 'N/A'}... -> {r[3]}")
else:
    print("All products have short_name already!")
    
    # Show some examples
    cursor = conn.execute('''
        SELECT id, ecom_code, name, short_name 
        FROM product_master 
        LIMIT 10
    ''')
    print("\nSample products:")
    for r in cursor.fetchall():
        name_preview = (r[2][:50] + '...') if r[2] and len(r[2]) > 50 else (r[2] or 'N/A')
        print(f"  {r[1]}: {name_preview} -> {r[3]}")

conn.close()
