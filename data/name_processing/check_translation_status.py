import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 检查 translation_status 分布
cursor.execute('PRAGMA table_info(product_master)')
columns = [col[1] for col in cursor.fetchall()]
print(f"Columns: {columns}")
print()

if 'translation_status' in columns:
    cursor.execute('SELECT translation_status, COUNT(*) FROM product_master GROUP BY translation_status')
    print("Translation status distribution:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")
    print()
    
    # 查看 pending 的商品
    cursor.execute('SELECT ecom_code, name FROM product_master WHERE translation_status = "pending" LIMIT 5')
    print("Pending items:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1][:50]}...")

# 查看没有 short_name 的商品
cursor.execute('SELECT ecom_code, name, translation_status FROM product_master WHERE short_name IS NULL OR short_name = "" LIMIT 10')
print("\nItems without short_name:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1][:50]}... (status: {row[2]})")

conn.close()
