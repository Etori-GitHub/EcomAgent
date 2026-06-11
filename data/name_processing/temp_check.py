import sqlite3

# Check product details
master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
amazon_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'

conn_master = sqlite3.connect(master_db)
conn_amazon = sqlite3.connect(amazon_db)

cursor = conn_master.cursor()
cursor.execute('''
    SELECT ecom_code, name, product_url, platform_id 
    FROM product_master 
    WHERE translation_status = 'pending'
    LIMIT 3
''')
pending_items = cursor.fetchall()

for row in pending_items:
    ecom_code, name, url, platform_id = row
    print(f'ECOM: {ecom_code}, Name: {name}, ASIN: {platform_id}')
    
    # Check amazon db
    asin = platform_id
    c = conn_amazon.cursor()
    c.execute('SELECT name FROM products WHERE asin = ?', (asin,))
    result = c.fetchone()
    if result:
        print(f'  Amazon name: {result[0]}')
    print()

conn_master.close()
conn_amazon.close()
