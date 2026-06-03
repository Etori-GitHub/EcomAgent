import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

# 检查不同的 NULL 和空字符串情况
cursor = conn.execute("""
    SELECT COUNT(*) FROM product_master 
    WHERE short_name IS NULL
""")
print(f"short_name IS NULL: {cursor.fetchone()[0]}")

cursor = conn.execute("""
    SELECT COUNT(*) FROM product_master 
    WHERE short_name = ''
""")
print(f"short_name = '': {cursor.fetchone()[0]}")

cursor = conn.execute("""
    SELECT COUNT(*) FROM product_master 
    WHERE short_name IS NULL OR short_name = ''
""")
print(f"short_name IS NULL OR = '': {cursor.fetchone()[0]}")

cursor = conn.execute("""
    SELECT ecom_code, name, short_name 
    FROM product_master 
    WHERE short_name IS NULL OR short_name = ''
    LIMIT 10
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: name='{row[1][:30]}...', short_name='{row[2]}'")