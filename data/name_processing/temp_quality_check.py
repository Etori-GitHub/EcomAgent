import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
cursor = conn.cursor()

# 检查 short_name 长度分布
print("short_name 长度分布:")
cursor.execute("SELECT LENGTH(short_name) as len, COUNT(*) as cnt FROM product_master GROUP BY len ORDER BY len")
for row in cursor.fetchall():
    print(f"  长度 {row[0]}: {row[1]} 条")

# 检查 short_name 是英文截断的记录（可能质量问题）
print("\n可能截断的 short_name (以英文结尾且很短):")
cursor.execute("""
    SELECT id, ecom_code, name, short_name 
    FROM product_master 
    WHERE LENGTH(short_name) < 15 
    AND short_name REGEXP '[a-zA-Z]$'
    LIMIT 20
""")
for row in cursor.fetchall():
    print(f"  ID: {row[0]}, ecom_code: {row[1]}")
    print(f"    name: {row[2]}")
    print(f"    short_name: {row[3]}")
    print()

conn.close()
