import sqlite3
import json
from datetime import datetime

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'

# Get products without short_name AND without name
conn = sqlite3.connect(db_path)
cursor = conn.execute('''
    SELECT id, ecom_code, name, product_url 
    FROM product_master 
    WHERE (short_name IS NULL OR short_name = '') 
    AND (name IS NULL OR name = '')
    LIMIT 50
''')
results = cursor.fetchall()
conn.close()

print(f"Found {len(results)} products without name and short_name")

if results:
    data = {
        "batch_id": f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "items": [
            {
                "id": row[1],  # ecom_code
                "name": "",    # empty, will be fetched
                "url": row[3]  # product_url
            }
            for row in results
        ]
    }
    
    output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Created pending_names.json with {len(results)} items")
    for row in results[:5]:
        print(f"  [{row[1]}] {row[3]}")