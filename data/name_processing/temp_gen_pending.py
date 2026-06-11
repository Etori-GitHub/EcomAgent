import sqlite3
import json

# 连接数据库
master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
amazon_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
tiktok_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\tiktok.db'

conn_master = sqlite3.connect(master_db)
conn_amazon = sqlite3.connect(amazon_db)
conn_tiktok = sqlite3.connect(tiktok_db)

# 获取 pending 商品
cursor = conn_master.cursor()
cursor.execute('''
    SELECT ecom_code, name, product_url, platform, platform_id 
    FROM product_master 
    WHERE translation_status = 'pending'
''')
pending_items = cursor.fetchall()

items = []
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
                print(f"Got name from amazon.db for {ecom_code}: {name[:50]}...")
        elif platform == 'tiktok':
            c = conn_tiktok.cursor()
            c.execute('SELECT name FROM products WHERE product_id = ?', (platform_id,))
            result = c.fetchone()
            if result and result[0]:
                name = result[0]
                print(f"Got name from tiktok.db for {ecom_code}")
    
    if name:
        items.append({'id': ecom_code, 'name': name})
    else:
        print(f"WARNING: No name found for {ecom_code} (platform={platform}, platform_id={platform_id})")

conn_master.close()
conn_amazon.close()
conn_tiktok.close()

# 生成 JSON
data = {
    'batch_id': 'batch_20260605_2000',
    'items': items
}

output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nGenerated {len(items)} items to {output_path}')
