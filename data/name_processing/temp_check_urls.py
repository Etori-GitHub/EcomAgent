import sqlite3

conn_master = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
c = conn_master.cursor()

c.execute('''
    SELECT ecom_code, platform_id, product_url 
    FROM product_master 
    WHERE translation_status = 'pending' AND platform = 'amazon'
    LIMIT 5
''')
rows = c.fetchall()
for r in rows:
    print(f'{r[0]}: ASIN={r[1]}')
    print(f'  URL: {r[2]}')
    print()

conn_master.close()
