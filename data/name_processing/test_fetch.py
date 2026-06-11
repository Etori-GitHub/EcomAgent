import sqlite3
import json
import time

# 简单测试：用 OpenClaw 的 web_fetch 来获取页面标题
# 但 web_fetch 可能更适合，让我先测试

import requests
from urllib.parse import unquote

master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(master_db)
c = conn.cursor()

c.execute("""
    SELECT ecom_code, product_url, platform, platform_id 
    FROM product_master 
    WHERE translation_status = 'pending'
    LIMIT 5
""")
pending_items = c.fetchall()
conn.close()

print("Testing Amazon API approach...")

# 使用 Amazon Product Advertising API 的替代方法
# 尝试从 URL 的 Open Graph 标签获取标题
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

for ecom_code, url, platform, platform_id in pending_items:
    print(f"\n{ecom_code}: {url}")
    try:
        resp = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        print(f"  Status: {resp.status_code}")
        print(f"  Final URL: {resp.url}")
        
        # 检查 HTML 中的标题
        html = resp.text
        import re
        
        # 尝试提取各种标题格式
        # 1. <title> 标签
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        if title_match:
            print(f"  <title>: {title_match.group(1)[:80]}")
        
        # 2. og:title
        og_match = re.search(r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']+)["\']', html, re.IGNORECASE)
        if og_match:
            print(f"  og:title: {og_match.group(1)[:80]}")
        
        # 3. data-product-title
        data_match = re.search(r'data-product-title=["\']([^"\']+)["\']', html)
        if data_match:
            print(f"  data-product-title: {data_match.group(1)[:80]}")
            
    except Exception as e:
        print(f"  Error: {e}")
    
    time.sleep(1)