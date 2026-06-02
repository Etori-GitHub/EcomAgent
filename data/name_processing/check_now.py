import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

# Check products without short_name
cursor = conn.execute("""
    SELECT ecom_code, name, short_name 
    FROM product_master 
    WHERE (short_name IS NULL OR short_name = '') 
    AND name IS NOT NULL AND name != ''
    LIMIT 10
""")
results = cursor.fetchall()
print(f"Found {len(results)} products without short_name:")
for row in results:
    name_display = row[1][:80] if len(row[1]) > 80 else row[1]
    print(f"  [{row[0]}] {name_display} | short_name: '{row[2]}'")

# Check total
cursor = conn.execute("""
    SELECT COUNT(*) 
    FROM product_master 
    WHERE (short_name IS NULL OR short_name = '') 
    AND name IS NOT NULL AND name != ''
""")
print(f"\nTotal products needing translation: {cursor.fetchone()[0]}")