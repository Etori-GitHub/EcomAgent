import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

# 查看所有数据
cursor = conn.execute("""
    SELECT id, ecom_code, name, short_name
    FROM product_master 
    ORDER BY id
    LIMIT 10
""")
results = cursor.fetchall()
print("Sample data from product_master:")
for row in results:
    print(f"  id={row[0]}, ecom_code={row[1]}, name='{row[2][:50] if row[2] else 'NULL'}...', short_name={row[3]}")

# 统计
cursor = conn.execute("SELECT COUNT(*) FROM product_master")
total = cursor.fetchone()[0]

cursor = conn.execute("SELECT COUNT(*) FROM product_master WHERE name IS NOT NULL AND name != ''")
with_name = cursor.fetchone()[0]

cursor = conn.execute("SELECT COUNT(*) FROM product_master WHERE short_name IS NOT NULL AND short_name != ''")
with_short_name = cursor.fetchone()[0]

print(f"\nStats:")
print(f"  Total: {total}")
print(f"  With name: {with_name}")
print(f"  With short_name: {with_short_name}")