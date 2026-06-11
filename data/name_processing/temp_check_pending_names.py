import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
cursor = conn.cursor()

# 总记录数
cursor.execute('SELECT COUNT(*) FROM product_master')
print(f'Total records: {cursor.fetchone()[0]}')

# 有name但没有short_name的记录
cursor.execute('SELECT COUNT(*) FROM product_master WHERE (short_name IS NULL OR short_name = "") AND name IS NOT NULL AND name != ""')
print(f'Pending translation (has name, no short_name): {cursor.fetchone()[0]}')

# 有short_name的记录数
cursor.execute('SELECT COUNT(*) FROM product_master WHERE short_name IS NOT NULL AND short_name != ""')
print(f'Already translated: {cursor.fetchone()[0]}')

# 查看translation_status分布
cursor.execute('SELECT translation_status, COUNT(*) FROM product_master GROUP BY translation_status')
print(f'\nTranslation status distribution: {cursor.fetchall()}')

# 查看几条有name的记录
cursor.execute('SELECT ecom_code, name, short_name FROM product_master WHERE name IS NOT NULL AND name != "" LIMIT 5')
print(f'\nSample records: {cursor.fetchall()}')

conn.close()