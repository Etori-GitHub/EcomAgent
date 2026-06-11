import sqlite3
import json
import requests
from bs4 import BeautifulSoup
import time
import re

master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'

conn = sqlite3.connect(master_db)
c = conn.cursor()

# 获取 pending 商品
c.execute("""
    SELECT ecom_code, product_url, platform, platform_id 
    FROM product_master 
    WHERE translation_status = 'pending'
""")
pending_items = c.fetchall()
conn.close()

print(f"Found {len(pending_items)} pending items to fetch names")

items = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

for i, row in enumerate(pending_items):
    ecom_code, url, platform, platform_id = row
    
    if platform == 'amazon':
        # 从 Amazon 页面获取标题
        try:
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 尝试多种选择器
            title_elem = soup.select_one('#productTitle')
            if not title_elem:
                title_elem = soup.select_one('span[data-product-title]')
            if not title_elem:
                title_elem = soup.select_one('h1.a-size-large')
            
            if title_elem:
                name = title_elem.get_text().strip()
                items.append({'id': ecom_code, 'name': name})
                print(f"[{i+1}/{len(pending_items)}] {ecom_code}: {name[:50]}...")
            else:
                print(f"[{i+1}/{len(pending_items)}] {ecom_code}: No title found")
                
            time.sleep(1)  # 避免请求过快
            
        except Exception as e:
            print(f"[{i+1}/{len(pending_items)}] {ecom_code}: Error - {e}")
    else:
        print(f"[{i+1}/{len(pending_items)}] {ecom_code}: Platform {platform} not supported")

print(f"\nSuccessfully fetched {len(items)} names")

# 生成 JSON
if items:
    data = {
        'batch_id': 'batch_20260605_1501',
        'items': items
    }
    
    output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved to {output_path}")
else:
    print("No items to save")