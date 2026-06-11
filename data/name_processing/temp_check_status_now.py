import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
cursor = conn.cursor()

# 检查 translation_status 分布
print("translation_status 分布:")
cursor.execute("SELECT translation_status, COUNT(*) FROM product_master GROUP BY translation_status")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

# 检查 short_name 为空的记录
print("\nshort_name 为空的记录:")
cursor.execute("SELECT COUNT(*) FROM product_master WHERE short_name IS NULL OR short_name = ''")
print(f"  {cursor.fetchone()[0]} 条")

# 查看最近的记录
print("\n最近5条记录:")
cursor.execute("""
    SELECT id, ecom_code, name, short_name, translation_status 
    FROM product_master 
    ORDER BY id DESC
    LIMIT 5
""")
for row in cursor.fetchall():
    print(f"  ID: {row[0]}, ecom_code: {row[1]}")
    print(f"    name: {row[2]}")
    print(f"    short_name: {row[3]}")
    print()

conn.close()
