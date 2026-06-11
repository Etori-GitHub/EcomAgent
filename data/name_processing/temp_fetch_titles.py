import sqlite3
import requests
from bs4 import BeautifulSoup
import time

# Get pending products
master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(master_db)
cursor = conn.cursor()

cursor.execute('''
    SELECT ecom_code, platform_id, product_url 
    FROM product_master 
    WHERE translation_status = 'pending'
''')
items = cursor.fetchall()
conn.close()

print(f'Found {len(items)} pending items')

# Try to fetch real names from Amazon
results = []
for ecom_code, asin, url in items:
    print(f'Fetching {asin}...')
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        response = requests.get(f'https://www.amazon.com/dp/{asin}', headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title_elem = soup.find('span', {'id': 'productTitle'})
            if title_elem:
                title = title_elem.get_text().strip()
                results.append({'id': ecom_code, 'name': title})
                print(f'  Found: {title[:80]}...')
            else:
                print(f'  No title found')
        else:
            print(f'  Status: {response.status_code}')
        time.sleep(1)
    except Exception as e:
        print(f'  Error: {e}')

print(f'\nFetched {len(results)} titles')
for r in results[:3]:
    print(f'{r["id"]}: {r["name"][:60]}...')
