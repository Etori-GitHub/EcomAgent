import sqlite3

conn_amazon = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db')
conn_master = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')

# 获取 pending 的 ASIN 列表
c = conn_master.cursor()
c.execute('''
    SELECT ecom_code, platform_id, name 
    FROM product_master 
    WHERE translation_status = 'pending'
''')
pending_items = c.fetchall()

print('Checking name sources for pending items:')
print('-' * 80)

for ecom_code, asin, master_name in pending_items:
    c2 = conn_amazon.cursor()
    c2.execute('SELECT id, name FROM products WHERE asin = ?', (asin,))
    amazon_result = c2.fetchone()
    
    amazon_name = amazon_result[1] if amazon_result else 'NOT FOUND'
    
    print(f'{ecom_code} (ASIN: {asin}):')
    print(f'  master.name: {master_name}')
    print(f'  amazon.name: {amazon_name}')
    print()

conn_amazon.close()
conn_master.close()