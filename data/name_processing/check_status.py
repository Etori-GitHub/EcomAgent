import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
c = conn.cursor()

# 检查是否有short_name为空但name不为空的商品
c.execute('''
    SELECT COUNT(*) FROM product_master 
    WHERE (short_name IS NULL OR short_name = "") 
    AND name IS NOT NULL AND name != ""
''')
print(f'Items with name but no short_name: {c.fetchone()[0]}')

# 检查最近更新的商品
c.execute('''
    SELECT ecom_code, name, short_name, translation_status 
    FROM product_master 
    ORDER BY rowid DESC LIMIT 5
''')
print('\nRecent items:')
for row in c.fetchall():
    name_preview = row[1][:30] if row[1] else "NULL"
    print(f'  {row[0]}: name={name_preview}..., short_name={row[2]}, status={row[3]}')

conn.close()