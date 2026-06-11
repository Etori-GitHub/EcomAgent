import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')

c = conn.execute('SELECT COUNT(*) FROM product_master WHERE short_name IS NULL OR short_name = ""')
print('Empty short_name:', c.fetchone()[0])

c = conn.execute('SELECT COUNT(*) FROM product_master WHERE name IS NOT NULL AND name != ""')
print('Has name:', c.fetchone()[0])

c = conn.execute('SELECT COUNT(*) FROM product_master')
print('Total:', c.fetchone()[0])

c = conn.execute('SELECT COUNT(*) FROM product_master WHERE name IS NOT NULL AND name != "" AND (short_name IS NULL OR short_name = "")')
print('Has name but no short_name:', c.fetchone()[0])

conn.close()
