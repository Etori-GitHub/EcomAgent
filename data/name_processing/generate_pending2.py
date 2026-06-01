import sqlite3
import json
from datetime import datetime

amazon_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'

# 连接两个数据库
amazon_conn = sqlite3.connect(amazon_db)
master_conn = sqlite3.connect(master_db)

# 找出 amazon 中有 name 但在 master 中没有对应 short_name 的产品
# amazon products 通过 asin 关联，master 中有 platform_id = asin
amazon_cursor = amazon_conn.execute("""
    SELECT p.asin, p.name
    FROM products p
    WHERE p.name IS NOT NULL AND p.name != ''
    ORDER BY p.id
    LIMIT 50
""")

amazon_products = amazon_cursor.fetchall()
print(f"Found {len(amazon_products)} products from amazon.db")

# 检查哪些已经在 master 中翻译过
items = []
for asin, name in amazon_products:
    # 检查 master 中是否已有此产品的翻译
    master_cursor = master_conn.execute("""
        SELECT short_name FROM product_master 
        WHERE platform = 'amazon' AND platform_id = ?
    """, (asin,))
    result = master_cursor.fetchone()
    
    if not result or not result[0]:
        # 需要翻译
        items.append({
            "id": f"ECAM{amazon_conn.execute('SELECT id FROM products WHERE asin = ?', (asin,)).fetchone()[0]:05d}",
            "name": name
        })

print(f"Products needing translation: {len(items)}")

if items:
    data = {
        "batch_id": f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "items": items
    }
    
    output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Created: {output_path}")
    print("\nSample items:")
    for item in items[:5]:
        name_preview = item['name'][:60] if len(item['name']) > 60 else item['name']
        print(f"  [{item['id']}] {name_preview}")
else:
    print("No products need translation")