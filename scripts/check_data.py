import sqlite3
from pathlib import Path

DATA_DIR = Path('data')

# 检查 Amazon 数据
print("=== Amazon 数据检查 ===")
amazon_db = DATA_DIR / 'amazon.db'
conn = sqlite3.connect(str(amazon_db))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM products WHERE name IS NULL OR name = ""')
empty_names = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM products')
total = cursor.fetchone()[0]
print(f'Total products: {total}')
print(f'Empty names: {empty_names}')

cursor.execute('SELECT id, asin, name FROM products WHERE name != "" AND name IS NOT NULL LIMIT 3')
print('Products with names:')
for row in cursor.fetchall():
    print(f"  {dict(row)}")

conn.close()

# 检查 TikTok 数据
print("\n=== TikTok 数据检查 ===")
tiktok_db = DATA_DIR / 'tiktok.db'
conn = sqlite3.connect(str(tiktok_db))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM tiktok_products WHERE name IS NULL OR name = ""')
empty_names = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM tiktok_products')
total = cursor.fetchone()[0]
print(f'Total products: {total}')
print(f'Empty names: {empty_names}')

conn.close()

# 检查 product_master 数据
print("\n=== Product Master 数据检查 ===")
master_db = DATA_DIR / 'product_master.db'
conn = sqlite3.connect(str(master_db))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM product_master WHERE name IS NULL OR name = ""')
empty_names = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM product_master')
total = cursor.fetchone()[0]
print(f'Total products: {total}')
print(f'Empty names: {empty_names}')

cursor.execute('SELECT id, ecom_code, name, short_name FROM product_master LIMIT 5')
print('Sample products:')
for row in cursor.fetchall():
    print(f"  {dict(row)}")

conn.close()

# 检查抓取的原始数据
print("\n=== 原始抓取数据检查 ===")
output_dir = Path('output/scraping')
if output_dir.exists():
    import json
    files = list(output_dir.glob('amazon_*.json'))
    print(f'Found {len(files)} Amazon JSON files')
    if files:
        with open(files[0], 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f'First file: {files[0].name}')
            print(f'Products count: {len(data)}')
            if data:
                print(f'Sample product keys: {list(data[0].keys())}')
                print(f'Sample product: {data[0]}')
