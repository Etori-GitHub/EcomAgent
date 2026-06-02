import sqlite3
import json
from datetime import datetime

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

# 查找有名称但没有 short_name 的产品
cursor = conn.execute("""
    SELECT id, ecom_code, name 
    FROM product_master 
    WHERE (short_name IS NULL OR short_name = '') AND name IS NOT NULL AND name != ''
    LIMIT 50
""")
results = cursor.fetchall()
print(f"Found {len(results)} products without short_name")

if results:
    # 创建 pending_names.json
    data = {
        "batch_id": f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "items": [
            {"id": row[1], "name": row[2]}  # ecom_code, name
            for row in results
        ]
    }
    
    output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Created pending_names.json with {len(results)} items")
else:
    print("No products need translation")
