import sqlite3
import json

# 连接数据库
amazon_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'

conn_amazon = sqlite3.connect(amazon_db)
conn_master = sqlite3.connect(master_db)

c_amazon = conn_amazon.cursor()
c_master = conn_master.cursor()

# 获取所有 pending 商品的 ASIN
c_master.execute("""
    SELECT ecom_code, platform_id 
    FROM product_master 
    WHERE translation_status = 'pending' AND platform = 'amazon'
""")
pending_items = c_master.fetchall()

print(f"Found {len(pending_items)} pending Amazon items")

items = []
for ecom_code, asin in pending_items:
    # 获取产品 id
    c_amazon.execute("SELECT id FROM products WHERE asin = ?", (asin,))
    product_row = c_amazon.fetchone()
    
    if product_row:
        product_id = product_row[0]
        
        # 查找 name_changed 事件
        c_amazon.execute("""
            SELECT new_value 
            FROM events 
            WHERE product_id = ? AND event_type = 'name_changed'
            ORDER BY created_at DESC
            LIMIT 1
        """, (product_id,))
        name_event = c_amazon.fetchone()
        
        if name_event and name_event[0]:
            name = name_event[0]
            items.append({'id': ecom_code, 'name': name})
            print(f"{ecom_code}: {name[:60]}...")
        else:
            # 尝试获取 products 表的 name
            c_amazon.execute("SELECT name FROM products WHERE id = ?", (product_id,))
            name_row = c_amazon.fetchone()
            if name_row and name_row[0]:
                name = name_row[0]
                items.append({'id': ecom_code, 'name': name})
                print(f"{ecom_code}: {name[:60]}... (from products table)")
            else:
                print(f"{ecom_code}: No name found")
    else:
        print(f"{ecom_code}: Product not found in amazon.db")

conn_amazon.close()
conn_master.close()

# 生成 JSON
data = {
    'batch_id': 'batch_20260605_1501',
    'items': items
}

output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(items)} items to pending_names.json")