import sqlite3
import json

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
cursor = conn.cursor()

cursor.execute('''
    SELECT ecom_code, name 
    FROM product_master 
    WHERE translation_status = 'pending' 
    AND name IS NOT NULL AND name != ''
''')

items = []
for row in cursor.fetchall():
    print(f'{row[0]}: {row[1]}')
    items.append({
        'id': row[0],
        'name': row[1]
    })

print(f'\nTotal: {len(items)} items')
conn.close()
