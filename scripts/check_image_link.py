import sqlite3

master_conn = sqlite3.connect('data/product_master.db')
master_cursor = master_conn.cursor()

master_cursor.execute("SELECT id, ecom_code, platform, platform_id FROM product_master WHERE platform='amazon' LIMIT 1")
row = master_cursor.fetchone()
print(f'商品主库: id={row[0]}, ecom_code={row[1]}, platform_id={row[3]}')

master_id = row[0]
asin = row[3]

amazon_conn = sqlite3.connect('data/amazon.db')
amazon_cursor = amazon_conn.cursor()
amazon_cursor.execute('SELECT id, asin, local_image_path, master_id FROM products WHERE asin = ?', (asin,))
amazon_row = amazon_cursor.fetchone()
print(f'Amazon表: id={amazon_row[0]}, asin={amazon_row[1]}, local_image_path={amazon_row[2]}, master_id={amazon_row[3]}')

if amazon_row[3] == master_id:
    print('关联正确')
else:
    print(f'关联不匹配: Amazon.master_id={amazon_row[3]}, 主库.id={master_id}')

amazon_conn.close()
master_conn.close()