import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')

# Check all columns for TikTok items with empty name
c = conn.execute('''
    SELECT ecom_code, name, short_name, product_url, platform, master_id 
    FROM product_master 
    WHERE translation_status = "pending" 
    LIMIT 5
''')
print('Pending items (all columns):')
for row in c.fetchall():
    print(f'\n  ecom_code: {row[0]}')
    print(f'  name: {row[1]}')
    print(f'  short_name: {row[2]}')
    print(f'  url: {row[3]}')
    print(f'  platform: {row[4]}')
    print(f'  master_id: {row[5]}')

conn.close()
