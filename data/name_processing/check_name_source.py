import sqlite3

# Check product_master for the pending IDs
pm_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
amazon_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'

pm_conn = sqlite3.connect(pm_path)
amazon_conn = sqlite3.connect(amazon_path)

# Get pending product details from product_master
cursor = pm_conn.execute('''
    SELECT id, ecom_code, platform, platform_id, name, short_name, product_url
    FROM product_master 
    WHERE ecom_code LIKE 'ECAM260008%' 
    ORDER BY ecom_code
    LIMIT 10
''')
rows = cursor.fetchall()
print('Products from product_master (ECAM260008xx):')
for r in rows:
    print(f'  id={r[0]}, ecom_code={r[1]}, platform={r[2]}')
    print(f'    platform_id={r[3]}, name={r[4]}, url={r[6]}')

# Check if these products have platform_id (ASIN for Amazon)
cursor = pm_conn.execute('''
    SELECT id, ecom_code, platform_id, product_url
    FROM product_master 
    WHERE ecom_code LIKE 'ECAM260008%' AND platform_id IS NOT NULL AND platform_id != ''
    LIMIT 10
''')
rows = cursor.fetchall()
print(f'\nProducts with platform_id:')
for r in rows:
    print(f'  ecom_code={r[1]}, platform_id={r[2]}, url={r[3]}')

pm_conn.close()
amazon_conn.close()
