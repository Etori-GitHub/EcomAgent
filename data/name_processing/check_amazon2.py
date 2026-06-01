import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
conn = sqlite3.connect(db_path)

# 查看 amazon products 有 name 的数据
cursor = conn.execute("""
    SELECT id, asin, name, category
    FROM products 
    WHERE name IS NOT NULL AND name != ''
    ORDER BY id
    LIMIT 10
""")
results = cursor.fetchall()
print("Sample products WITH name:")
for row in results:
    name_preview = row[2][:60] if row[2] and len(row[2]) > 60 else (row[2] or 'NULL')
    print(f"  [{row[1]}] {name_preview}")

# 统计
cursor = conn.execute("SELECT COUNT(*) FROM products WHERE name IS NOT NULL AND name != ''")
with_name = cursor.fetchone()[0]

print(f"\nTotal products with name: {with_name}")