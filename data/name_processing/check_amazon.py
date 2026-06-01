import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
conn = sqlite3.connect(db_path)

# 查看 amazon products 数据
cursor = conn.execute("""
    SELECT id, asin, name, category
    FROM products 
    ORDER BY id
    LIMIT 10
""")
results = cursor.fetchall()
print("Sample data from amazon.products:")
for row in results:
    name_preview = row[2][:50] if row[2] and len(row[2]) > 50 else (row[2] or 'NULL')
    print(f"  id={row[0]}, asin={row[1]}, name='{name_preview}', cat={row[3]}")

# 统计
cursor = conn.execute("SELECT COUNT(*) FROM products")
total = cursor.fetchone()[0]

cursor = conn.execute("SELECT COUNT(*) FROM products WHERE name IS NOT NULL AND name != ''")
with_name = cursor.fetchone()[0]

print(f"\nStats:")
print(f"  Total: {total}")
print(f"  With name: {with_name}")