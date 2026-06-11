import sqlite3
import requests
from bs4 import BeautifulSoup
import time
import json

# 获取所有 pending 的 ASIN 和 URL
master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(master_db)
c = conn.cursor()
c.execute('SELECT ecom_code, platform_id, product_url FROM product_master WHERE translation_status = "pending"')
pending = c.fetchall()
conn.close()

print(f"Total pending: {len(pending)}")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

items = []
for ecom_code, asin, url in pending:
    try:
        print(f"Fetching {asin}...")
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 尝试多种选择器获取标题
        title = None
        title_elem = soup.find('span', {'id': 'productTitle'})
        if title_elem:
            title = title_elem.get_text().strip()
        
        if not title:
            title_elem = soup.find('h1', {'id': 'title'})
            if title_elem:
                title = title_elem.get_text().strip()
        
        if title:
            print(f"  -> {title[:60]}...")
            items.append({'id': ecom_code, 'name': title})
        else:
            print(f"  -> NO TITLE FOUND")
            
        time.sleep(1)  # 避免请求过快
        
    except Exception as e:
        print(f"  -> ERROR: {e}")

print(f"\nFetched {len(items)} items with titles")

# 生成 JSON
data = {
    'batch_id': 'batch_20260605_1631',
    'items': items
}

output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Saved to {output_path}")
