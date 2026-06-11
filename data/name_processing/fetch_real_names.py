import sqlite3
import json

conn_amazon = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db')
conn_master = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')

# 获取 pending 的 ASIN 列表
master_cursor = conn_master.cursor()
master_cursor.execute('''
    SELECT ecom_code, platform_id 
    FROM product_master 
    WHERE translation_status = 'pending' AND platform = 'amazon'
''')
pending_items = master_cursor.fetchall()

print(f'Found {len(pending_items)} pending Amazon items')

items = []
for ecom_code, asin in pending_items:
    # 从 products 表获取 product_id
    c = conn_amazon.cursor()
    c.execute('SELECT id, name FROM products WHERE asin = ?', (asin,))
    result = c.fetchone()
    
    if result:
        product_id, name = result
        
        # 如果 name 是 "Amazon.com"，尝试从 events 获取
        if name == 'Amazon.com' or not name:
            c2 = conn_amazon.cursor()
            c2.execute('''
                SELECT old_value FROM events 
                WHERE product_id = ? AND event_type = 'name_changed' 
                ORDER BY id DESC LIMIT 1
            ''', (product_id,))
            event_result = c2.fetchone()
            if event_result and event_result[0]:
                name = event_result[0]
                print(f'{ecom_code}: Found name from events: {name[:60]}...')
        
        if name and name != 'Amazon.com':
            items.append({'id': ecom_code, 'name': name})
        else:
            print(f'{ecom_code}: No valid name found (ASIN: {asin})')
    else:
        print(f'{ecom_code}: Product not found in amazon.db (ASIN: {asin})')

conn_amazon.close()
conn_master.close()

# 生成 JSON
data = {
    'batch_id': 'batch_20260605_2035',
    'items': items
}

output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nGenerated {len(items)} items with valid names')
