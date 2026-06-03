import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
c = conn.execute('SELECT COUNT(*) FROM product_master WHERE (short_name IS NULL OR short_name = "") AND name IS NOT NULL AND name != ""')
print(f'有名称但无短名称的产品数: {c.fetchone()[0]}')

c = conn.execute('SELECT COUNT(*) FROM product_master WHERE (short_name IS NULL OR short_name = "") AND (name IS NULL OR name = "")')
print(f'无名称也无短名称的产品数: {c.fetchone()[0]}')