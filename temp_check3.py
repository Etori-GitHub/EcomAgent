import sqlite3
from pathlib import Path

db_path = Path('data/product_master.db')
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# 用价格查商品 - 需要关联平台数据获取价格
cursor.execute('''
    SELECT pm.ecom_code, pm.platform, pm.category, pm.name, pm.short_name
    FROM product_master pm
    WHERE pm.category LIKE '%Beauty%'
''')
rows = cursor.fetchall()

# 需要从 amazon/tiktok 表获取价格
amazon_db = Path('data/amazon.db')
tiktok_db = Path('data/tiktok.db')

print('美妆个护分类中价格接近 13.93 的商品:')
for row in rows:
    ecom_code, platform, category, name, short_name = row
    
    if platform == 'amazon':
        try:
            aconn = sqlite3.connect(str(amazon_db))
            acursor = aconn.cursor()
            acursor.execute('''
                SELECT ds.price FROM products p
                JOIN daily_sales ds ON p.id = ds.product_id
                WHERE p.master_id = ?
                ORDER BY ds.date DESC LIMIT 1
            ''', (ecom_code.replace('ECAM', ''),))  # 尝试用 id 匹配
            result = acursor.fetchone()
            aconn.close()
        except:
            continue
    else:
        continue

conn.close()
