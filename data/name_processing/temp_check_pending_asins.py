import sqlite3
import requests
from bs4 import BeautifulSoup

# 获取所有 pending 的 ASIN
master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(master_db)
c = conn.cursor()
c.execute('SELECT ecom_code, platform_id FROM product_master WHERE translation_status = "pending"')
pending = c.fetchall()
conn.close()

print(f"Total pending: {len(pending)}")

# 检查 amazon.db 中是否有这些 ASIN
amazon_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
conn = sqlite3.connect(amazon_db)
c = conn.cursor()

asins = [p[1] for p in pending]
for asin in asins[:5]:
    c.execute('SELECT asin, name FROM products WHERE asin = ?', (asin,))
    result = c.fetchone()
    if result and result[1]:
        print(f'{asin}: {result[1][:60]}')
    else:
        print(f'{asin}: NO NAME in amazon.db')

conn.close()
