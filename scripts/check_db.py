import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("UPDATE product_master SET translation_status = 'pending' WHERE name IS NOT NULL AND name != ''")
print('Updated:', c.rowcount)
conn.commit()

c.execute("SELECT translation_status, COUNT(*) FROM product_master GROUP BY translation_status")
print('By translation_status:', c.fetchall())

conn.close()