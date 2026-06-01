import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

cursor = conn.execute('SELECT COUNT(*) FROM product_master')
print(f'Total products: {cursor.fetchone()[0]}')

cursor = conn.execute('SELECT COUNT(*) FROM product_master WHERE short_name IS NOT NULL AND short_name != ""')
print(f'With short_name: {cursor.fetchone()[0]}')

cursor = conn.execute('SELECT COUNT(*) FROM product_master WHERE short_name IS NULL OR short_name = ""')
print(f'Without short_name: {cursor.fetchone()[0]}')

# 显示一些样例
cursor = conn.execute('SELECT id, ecom_code, name, short_name FROM product_master LIMIT 5')
print("\nSample products:")
for row in cursor.fetchall():
    print(f"  [{row[1]}] {row[2][:50]}... -> {row[3]}")
