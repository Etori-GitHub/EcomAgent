import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
cursor = conn.cursor()

# 检查 translation_status 分布
print('translation_status 分布:')
cursor.execute('SELECT translation_status, COUNT(*) FROM product_master GROUP BY translation_status')
for row in cursor.fetchall():
    print(f'  {row[0]}: {row[1]}')

# 检查是否有 pending 状态
cursor.execute("SELECT COUNT(*) FROM product_master WHERE translation_status = 'pending'")
pending_count = cursor.fetchone()[0]
print(f'\npending 状态记录数: {pending_count}')

# 检查最近翻译的几条
print('\n最近翻译的示例:')
cursor.execute("SELECT id, name, short_name FROM product_master WHERE translation_status = 'translated' ORDER BY id DESC LIMIT 5")
for row in cursor.fetchall():
    name = row[1][:50] if row[1] else 'N/A'
    print(f'  {row[0]}: {name}... -> {row[2]}')

conn.close()
