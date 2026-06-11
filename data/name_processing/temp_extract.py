import sqlite3
import re

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')

# Get pending items and extract name from URL
c = conn.execute('''
    SELECT ecom_code, name, product_url 
    FROM product_master 
    WHERE translation_status = "pending" 
    LIMIT 5
''')
print('Pending items:')
for row in c.fetchall():
    ecom_code, name, url = row
    # Extract name from URL (TikTok format)
    # URL format: https://shop.tiktok.com/us/pdp/product-name-slug/123456
    extracted_name = ""
    if url:
        match = re.search(r'/pdp/([^/]+)/', url)
        if match:
            slug = match.group(1)
            # Convert slug to readable name
            extracted_name = slug.replace('-', ' ').title()
    
    print(f'\n  ecom_code: {ecom_code}')
    print(f'  name: {name}')
    print(f'  extracted: {extracted_name[:60]}...')

conn.close()
