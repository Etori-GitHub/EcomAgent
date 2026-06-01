import requests
from bs4 import BeautifulSoup
import json
import time
import sqlite3

def get_amazon_title(asin):
    """Fetch product title from Amazon using ASIN"""
    url = f"https://www.amazon.com/dp/{asin}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try productTitle span first
        title_elem = soup.find('span', id='productTitle')
        if title_elem:
            return title_elem.get_text().strip()
        
        # Try title tag as fallback
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip()
            # Clean up Amazon title format
            if ':' in title:
                title = title.split(':')[0]
            if '|' in title:
                title = title.split('|')[0]
            return title.strip()
        
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

# Load pending names
input_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json'
with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get ASINs from database
pm_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
pm_conn = sqlite3.connect(pm_path)

# Build ecom_code -> asin mapping
ids = [item['id'] for item in data['items']]
placeholders = ','.join(['?' for _ in ids])
cursor = pm_conn.execute(f'SELECT ecom_code, platform_id FROM product_master WHERE ecom_code IN ({placeholders})', ids)
asin_map = {row[0]: row[1] for row in cursor.fetchall()}
pm_conn.close()

print(f"Fetching titles for {len(data['items'])} products...")

results = []
for i, item in enumerate(data['items']):
    ecom_code = item['id']
    asin = asin_map.get(ecom_code)
    
    if not asin:
        print(f"[{i+1}/{len(data['items'])}] {ecom_code}: No ASIN")
        continue
    
    print(f"[{i+1}/{len(data['items'])}] {ecom_code} (ASIN: {asin})...", end=' ', flush=True)
    title = get_amazon_title(asin)
    if title:
        display_title = title[:60] + '...' if len(title) > 60 else title
        print(f"OK: {display_title}")
        results.append({'id': ecom_code, 'name': title})
    else:
        print("FAILED")
    
    time.sleep(1)  # Rate limiting

# Save fetched names
output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\fetched_names.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump({'batch_id': data['batch_id'], 'items': results}, f, ensure_ascii=False, indent=2)

print(f"\nSaved to {output_path}")
print(f"Successfully fetched: {len(results)}/{len(data['items'])}")
