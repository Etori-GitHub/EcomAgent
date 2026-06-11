import sqlite3

master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(master_db)
c = conn.cursor()

# 检查 pending 商品的 URL
c.execute("""
    SELECT ecom_code, product_url, platform, platform_id 
    FROM product_master 
    WHERE translation_status = 'pending'
    LIMIT 5
""")
rows = c.fetchall()
print(f"Sample pending items with URLs:")
for row in rows:
    ecom_code, url, platform, platform_id = row
    print(f"  {ecom_code}: {platform}, {platform_id}")
    print(f"    URL: {url}")

conn.close()