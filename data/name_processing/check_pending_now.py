import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

# Check products without name
cursor = conn.execute("""
    SELECT COUNT(*) FROM product_master 
    WHERE name IS NULL OR name = ''
""")
no_name = cursor.fetchone()[0]

# Check products with name but no short_name
cursor = conn.execute("""
    SELECT COUNT(*) FROM product_master 
    WHERE (short_name IS NULL OR short_name = '') 
    AND name IS NOT NULL AND name != ''
""")
pending = cursor.fetchone()[0]

# Check translated
cursor = conn.execute("""
    SELECT COUNT(*) FROM product_master 
    WHERE short_name IS NOT NULL AND short_name != ''
""")
translated = cursor.fetchone()[0]

# Check total
cursor = conn.execute("SELECT COUNT(*) FROM product_master")
total = cursor.fetchone()[0]

print(f"总产品数: {total}")
print(f"已翻译: {translated}")
print(f"待翻译(有名称无短名): {pending}")
print(f"无名称: {no_name}")
print(f"校验: {translated + pending + no_name} = {total}")

conn.close()