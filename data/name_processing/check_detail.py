import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

# Check products without short_name, including those without name
cursor = conn.execute("""
    SELECT ecom_code, name, short_name 
    FROM product_master 
    WHERE short_name IS NULL OR short_name = ''
    LIMIT 20
""")
results = cursor.fetchall()
print(f"Products without short_name (first 20):")
for row in results:
    name_display = row[1][:60] if row[1] and len(row[1]) > 60 else (row[1] or 'NULL')
    print(f"  [{row[0]}] {name_display}")

# Check how many have name
cursor = conn.execute("""
    SELECT COUNT(*) 
    FROM product_master 
    WHERE (short_name IS NULL OR short_name = '') 
    AND name IS NOT NULL AND name != ''
""")
print(f"\nProducts without short_name but WITH name: {cursor.fetchone()[0]}")

# Check how many have no name
cursor = conn.execute("""
    SELECT COUNT(*) 
    FROM product_master 
    WHERE (short_name IS NULL OR short_name = '') 
    AND (name IS NULL OR name = '')
""")
print(f"Products without short_name AND without name: {cursor.fetchone()[0]}")