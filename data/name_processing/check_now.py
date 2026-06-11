import sqlite3

master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(master_db)
cursor = conn.cursor()

# 检查表结构
cursor.execute("PRAGMA table_info(product_master)")
columns = cursor.fetchall()
print('Table columns:')
for col in columns:
    print(f'  {col[1]} ({col[2]})')

print()

# 检查 short_name 情况
cursor.execute('''
    SELECT COUNT(*) FROM product_master WHERE short_name IS NOT NULL AND short_name != ""
''')
has_short_name = cursor.fetchone()[0]
print(f'Items with short_name: {has_short_name}')

# 获取几条示例
cursor.execute('''
    SELECT ecom_code, name, short_name 
    FROM product_master 
    LIMIT 5
''')
samples = cursor.fetchall()
print('\nSample items:')
for row in samples:
    print(f'  {row[0]}: {row[1][:50]}... -> {row[2]}')

conn.close()
