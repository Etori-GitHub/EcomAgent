import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
c = conn.cursor()

# 完整状态统计
c.execute('SELECT COUNT(*) FROM product_master')
total = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM product_master WHERE short_name IS NOT NULL AND short_name != ''")
has_short_name = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM product_master WHERE translation_status = 'completed'")
completed = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM product_master WHERE translation_status = 'pending'")
pending = c.fetchone()[0]

print(f'Total products: {total}')
print(f'Has short_name: {has_short_name}')
print(f'Status completed: {completed}')
print(f'Status pending: {pending}')

# 检查是否有真正需要翻译的
c.execute('''
    SELECT COUNT(*) FROM product_master 
    WHERE (short_name IS NULL OR short_name = "") 
    AND name IS NOT NULL AND name != ""
''')
need_translate = c.fetchone()[0]
print(f'Need translation (name exists but no short_name): {need_translate}')

conn.close()
