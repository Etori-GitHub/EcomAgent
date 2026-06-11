import sqlite3
master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(master_db)
cursor = conn.cursor()

# 统计各状态数量
cursor.execute('''
    SELECT translation_status, COUNT(*) 
    FROM product_master 
    GROUP BY translation_status
''')
print('Translation status counts:')
for row in cursor.fetchall():
    status = row[0] if row[0] else 'NULL'
    print(f'  {status}: {row[1]}')

# 检查总数
cursor.execute('SELECT COUNT(*) FROM product_master')
total = cursor.fetchone()[0]
print(f'\nTotal products: {total}')

# 检查有 short_name 的数量
cursor.execute("SELECT COUNT(*) FROM product_master WHERE short_name IS NOT NULL AND short_name != ''")
with_short = cursor.fetchone()[0]
print(f'With short_name: {with_short}')

conn.close()
