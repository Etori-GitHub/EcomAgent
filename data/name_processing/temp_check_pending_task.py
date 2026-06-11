import sqlite3

conn = sqlite3.connect('C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/product_master.db')
cursor = conn.cursor()

# 检查翻译状态
cursor.execute('SELECT translation_status, COUNT(*) FROM product_master GROUP BY translation_status')
print('Translation status:', cursor.fetchall())

# 检查是否有空的short_name
cursor.execute("SELECT COUNT(*) FROM product_master WHERE short_name IS NULL OR short_name = ''")
print('Empty short_name count:', cursor.fetchone()[0])

# 查看几个样本
cursor.execute('SELECT id, name, short_name FROM product_master LIMIT 5')
print('Sample products:')
for row in cursor.fetchall():
    print(f'  {row[0]}: {row[1][:50]}... -> {row[2]}')

conn.close()
