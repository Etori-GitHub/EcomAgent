import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')

# Check the actual data
c = conn.execute('SELECT ecom_code, name, short_name FROM product_master WHERE short_name IS NULL OR short_name = "" LIMIT 10')
print('Items with empty short_name:')
for row in c.fetchall():
    print(f'  {row[0]}: name="{row[1][:50] if row[1] else "NULL"}...", short_name="{row[2]}"')

# Check translation_status
c = conn.execute('SELECT COUNT(*) FROM product_master WHERE translation_status = "pending"')
print('\nPending translation_status:', c.fetchone()[0])

c = conn.execute('SELECT COUNT(*) FROM product_master WHERE translation_status IS NULL OR translation_status = ""')
print('NULL/empty translation_status:', c.fetchone()[0])

conn.close()
