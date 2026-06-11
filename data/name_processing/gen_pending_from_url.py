import sqlite3
import json
import uuid
import re

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')

# Get pending items and extract name from URL
c = conn.execute('''
    SELECT ecom_code, name, product_url 
    FROM product_master 
    WHERE translation_status = "pending" 
    LIMIT 100
''')

items = []
for row in c.fetchall():
    ecom_code, name, url = row
    
    # If name is empty, extract from URL
    if not name and url:
        match = re.search(r'/pdp/([^/]+)/', url)
        if match:
            slug = match.group(1)
            # Convert slug to readable name
            name = slug.replace('-', ' ')
            # Clean up
            name = re.sub(r'\s+', ' ', name).strip()
    
    if name:
        items.append({"id": ecom_code, "name": name})

conn.close()

data = {
    "batch_id": str(uuid.uuid4()),
    "items": items
}

output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Generated {len(items)} items')
print(f'Output: {output_path}')
for item in items[:5]:
    print(f'{item["id"]}: {item["name"][:60]}...' if len(item["name"]) > 60 else f'{item["id"]}: {item["name"]}')