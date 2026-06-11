import sqlite3
import json
import requests
from bs4 import BeautifulSoup
import time
import re

# Amazon 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

def get_amazon_product_name(asin):
    """从 Amazon 页面获取商品名称"""
    url = f"https://www.amazon.com/dp/{asin}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 尝试多种选择器
            title_selectors = [
                '#productTitle',
                '#title span',
                'h1.a-size-large',
                'h1.product-title',
                'span[data-purpose="product-title"]',
            ]
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    name = title_elem.get_text(strip=True)
                    if name:
                        return name
            
            # 备用：从 title 标签获取
            title_tag = soup.find('title')
            if title_tag:
                name = title_tag.get_text(strip=True)
                # 清理 Amazon 后缀
                name = re.sub(r'\s*:\s*Amazon\.com:.*$', '', name)
                name = re.sub(r'\s*-\s*Amazon\.com$', '', name)
                if name and len(name) > 5:
                    return name
                    
        print(f"  Status: {response.status_code}")
    except Exception as e:
        print(f"  Error: {e}")
    
    return None

# 主程序
master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
amazon_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'

conn_master = sqlite3.connect(master_db)
conn_amazon = sqlite3.connect(amazon_db)

# 获取 pending 商品
c = conn_master.cursor()
c.execute('''
    SELECT ecom_code, platform_id 
    FROM product_master 
    WHERE translation_status = 'pending'
    ORDER BY ecom_code
''')
pending_items = c.fetchall()

print(f"Found {len(pending_items)} pending items to fetch names")

items = []
success_count = 0
fail_count = 0

for i, (ecom_code, asin) in enumerate(pending_items):
    print(f"\n[{i+1}/{len(pending_items)}] {ecom_code} (ASIN: {asin})")
    
    name = get_amazon_product_name(asin)
    
    if name:
        print(f"  ✓ Got: {name[:60]}..." if len(name) > 60 else f"  ✓ Got: {name}")
        items.append({'id': ecom_code, 'name': name})
        success_count += 1
        
        # 更新 amazon.db
        c2 = conn_amazon.cursor()
        c2.execute('UPDATE products SET name = ? WHERE asin = ?', (name, asin))
        
        # 延迟避免被封
        time.sleep(2)
    else:
        print(f"  ✗ Failed to get name")
        fail_count += 1
        time.sleep(1)

# 提交数据库更新
conn_amazon.commit()
conn_master.close()
conn_amazon.close()

# 生成 JSON
data = {
    'batch_id': 'batch_20260605_2000',
    'items': items
}

output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*50}")
print(f"Completed: {success_count} success, {fail_count} failed")
print(f"Output saved to: {output_path}")
