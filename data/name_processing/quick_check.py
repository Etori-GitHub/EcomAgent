import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

c = conn.cursor()
c.execute('SELECT COUNT(*) FROM product_master WHERE name IS NOT NULL AND name != ""')
print('Products with name:', c.fetchone()[0])

c.execute('SELECT COUNT(*) FROM product_master WHERE short_name IS NOT NULL AND short_name != ""')
print('Products with short_name:', c.fetchone()[0])

c.execute('SELECT COUNT(*) FROM product_master WHERE name IS NOT NULL AND name != "" AND short_name IS NOT NULL AND short_name != ""')
print('Products with both:', c.fetchone()[0])

c.execute('SELECT COUNT(*) FROM product_master')
print('Total products:', c.fetchone()[0])

# 查看一些有名称但没有short_name的（应该为0）
c.execute('SELECT ecom_code, name FROM product_master WHERE name IS NOT NULL AND name != "" AND (short_name IS NULL OR short_name = "") LIMIT 5')
rows = c.fetchall()
print('Products with name but no short_name:', len(rows))
for r in rows:
    print(f'  {r[0]}: {r[1][:50]}')

# 查看一些翻译示例
c.execute('SELECT ecom_code, name, short_name FROM product_master WHERE name IS NOT NULL AND short_name IS NOT NULL AND short_name != "" LIMIT 10')
rows = c.fetchall()
print('\nTranslation examples:')
for r in rows:
    print(f'  {r[0]}: "{r[1][:40]}..." -> "{r[2]}"')