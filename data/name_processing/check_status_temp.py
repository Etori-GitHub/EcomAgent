import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')

# Count pending
c = conn.execute('''
    SELECT COUNT(*) FROM product_master 
    WHERE (short_name IS NULL OR short_name = '') 
    AND name IS NOT NULL AND name != ''
''')
pending = c.fetchone()[0]

# Count completed
c = conn.execute('''
    SELECT COUNT(*) FROM product_master 
    WHERE short_name IS NOT NULL AND short_name != ''
''')
completed = c.fetchone()[0]

# Total
c = conn.execute('SELECT COUNT(*) FROM product_master')
total = c.fetchone()[0]

conn.close()

print(f'Total products: {total}')
print(f'With short_name: {completed}')
print(f'Pending translation: {pending}')
