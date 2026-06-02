import sqlite3
db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

total = conn.execute('SELECT COUNT(*) FROM product_master').fetchone()[0]
with_short = conn.execute("SELECT COUNT(*) FROM product_master WHERE short_name IS NOT NULL AND short_name != ''").fetchone()[0]
with_name = conn.execute("SELECT COUNT(*) FROM product_master WHERE name IS NOT NULL AND name != ''").fetchone()[0]
platforms = conn.execute('SELECT platform, COUNT(*) FROM product_master GROUP BY platform').fetchall()

print(f'Total products: {total}')
print(f'With name: {with_name}')
print(f'With short_name: {with_short}')
print()
print('By platform:')
for p in platforms:
    print(f'  {p[0]}: {p[1]}')

conn.close()