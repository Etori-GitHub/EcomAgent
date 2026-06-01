import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)
cursor = conn.execute('''
    SELECT id, ecom_code, name, product_url, category 
    FROM product_master 
    WHERE ecom_code IN ('ECAM26000794', 'ECAM26000795')
''')
for row in cursor.fetchall():
    print(row)
conn.close()
