import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
c = conn.execute('''
    SELECT COUNT(*) 
    FROM product_master 
    WHERE (short_name IS NULL OR short_name = '') 
    AND name IS NOT NULL AND name != ''
''')
print('Pending count:', c.fetchone()[0])
conn.close()