import sqlite3
import json

# 连接数据库
amazon_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'

conn_amazon = sqlite3.connect(amazon_db)
conn_master = sqlite3.connect(master_db)

c_amazon = conn_amazon.cursor()
c_master = conn_master.cursor()

# 获取所有 pending 商品的 ASIN 和对应的 product_id
c_master.execute("""
    SELECT ecom_code, platform_id 
    FROM product_master 
    WHERE translation_status = 'pending' AND platform = 'amazon'
""")
pending_items = c_master.fetchall()

# 构建 ASIN 到 ecom_code 的映射
asin_to_ecom = {asin: ecom_code for ecom_code, asin in pending_items}

# 获取所有 pending 商品的 product_id
asins = [asin for _, asin in pending_items]
placeholders = ','.join(['?' for _ in asins])

c_amazon.execute(f"""
    SELECT p.id, p.asin, p.name
    FROM products p
    WHERE p.asin IN ({placeholders})
""", asins)
products = c_amazon.fetchall()

product_ids = [p[0] for p in products]
print(f"Found {len(products)} products in amazon.db")

# 检查所有 name_changed 事件，查找旧名称
c_amazon.execute(f"""
    SELECT e.product_id, e.old_value, e.new_value, p.asin
    FROM events e
    JOIN products p ON e.product_id = p.id
    WHERE e.event_type = 'name_changed' 
    AND e.product_id IN ({','.join(['?' for _ in product_ids])})
    ORDER BY e.created_at DESC
""", product_ids)

name_events = c_amazon.fetchall()
print(f"Found {len(name_events)} name_changed events")

# 构建 product_id 到最新名称的映射
product_names = {}
for product_id, old_value, new_value, asin in name_events:
    if product_id not in product_names:
        # 优先使用 old_value（因为 new_value 可能是 NULL）
        name = old_value if old_value else new_value
        if name:
            product_names[product_id] = name

print(f"Found names for {len(product_names)} products from events")

# 生成结果
items = []
for product_id, asin, db_name in products:
    if product_id in product_names:
        name = product_names[product_id]
        ecom_code = asin_to_ecom.get(asin)
        if ecom_code and name:
            items.append({'id': ecom_code, 'name': name})
            print(f"{ecom_code}: {name[:60]}...")

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