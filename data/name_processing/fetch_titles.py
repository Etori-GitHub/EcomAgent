import requests
from bs4 import BeautifulSoup
import json
import time
import re

def get_amazon_title(url):
    """Fetch product title from Amazon using requests"""
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

print(f"Fetching titles for {len(data['items'])} products...")

for i, item in enumerate(data['items']):
    print(f"[{i+1}/{len(data['items'])}] {item['id']}...", end=' ', flush=True)
    title = get_amazon_title(item['url'])
    if title:
        item['name'] = title
        display_title = title[:60] + '...' if len(title) > 60 else title
        print(f"OK: {display_title}")
    else:
        print("FAILED")
    time.sleep(0.5)  # Rate limiting

# Save updated file
output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved to {output_path}")

# Summary
success_count = sum(1 for item in data['items'] if item['name'])
print(f"Successfully fetched: {success_count}/{len(data['items'])}")