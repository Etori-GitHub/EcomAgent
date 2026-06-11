import sqlite3

master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
amazon_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
tiktok_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\tiktok.db'

conn_master = sqlite3.connect(master_db)
conn_amazon = sqlite3.connect(amazon_db)
conn_tiktok = sqlite3.connect(tiktok_db)

cursor = conn_master.cursor()
cursor.execute('''
    SELECT ecom_code, name, product_url, platform, platform_id 
    FROM product_master 
    WHERE translation_status = 'pending'
''')
pending_items = cursor.fetchall()

print(f'Total pending: {len(pending_items)}')
print()

items_with_name = 0
items_without_name = 0

for row in pending_items:
    ecom_code, name, url, platform, platform_id = row
    
    # 如果 name 为空，从源数据库获取
    if not name:
        if platform == 'amazon':
            asin = platform_id
            c = conn_amazon.cursor()
            c.execute('SELECT name FROM products WHERE asin = ?', (asin,))
            result = c.fetchone()
            if result and result[0]:
                name = result[0]
                print(f'{ecom_code} (amazon {asin}): Found name in amazon.db')
                print(f'  -> {name[:80]}...' if len(name) > 80 else f'  -> {name}')
                items_with_name += 1
            else:
                print(f'{ecom_code} (amazon {asin}): NO NAME in amazon.db')
                items_without_name += 1
        elif platform == 'tiktok':
            c = conn_tiktok.cursor()
            c.execute('SELECT name FROM products WHERE product_id = ?', (platform_id,))
            result = c.fetchone()
            if result and result[0]:
                name = result[0]
                print(f'{ecom_code} (tiktok {platform_id}): Found name in tiktok.db')
                print(f'  -> {name[:80]}...' if len(name) > 80 else f'  -> {name}')
                items_with_name += 1
            else:
                print(f'{ecom_code} (tiktok {platform_id}): NO NAME in tiktok.db')
                items_without_name += 1
        else:
            print(f'{ecom_code} (unknown platform {platform}): Unknown platform')
            items_without_name += 1
    else:
        print(f'{ecom_code}: Already has name: {name[:60]}...' if len(name) > 60 else f'{ecom_code}: Already has name: {name}')
        items_with_name += 1

print()
print(f'Items with name: {items_with_name}')
print(f'Items without name: {items_without_name}')

conn_master.close()
conn_amazon.close()
conn_tiktok.close()