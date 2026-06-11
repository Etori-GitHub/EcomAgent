import sqlite3

master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(master_db)
cursor = conn.cursor()

cursor.execute('''
    SELECT ecom_code, platform, platform_id, product_url 
    FROM product_master 
    WHERE translation_status = 'pending'
''')
items = cursor.fetchall()
conn.close()

print(f'Pending items: {len(items)}')
for ecom_code, platform, platform_id, url in items:
    print(f'{ecom_code}: platform={platform}, id={platform_id}')
    print(f'  URL: {url}')
