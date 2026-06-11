import sqlite3

# 连接数据库
conn = sqlite3.connect('data/product_master.db')
cursor = conn.cursor()

# 查看这些记录的完整信息
cursor.execute("SELECT id, ecom_code, platform, platform_id, product_url, name, short_name FROM product_master WHERE short_name IS NULL OR short_name = ''")
records = cursor.fetchall()
print(f'Found {len(records)} pending records:\n')
for r in records:
    print(f'ID: {r[0]}')
    print(f'  ecom_code: {r[1]}')
    print(f'  platform: {r[2]}')
    print(f'  platform_id: {r[3]}')
    print(f'  product_url: {r[4]}')
    print(f'  name: {r[5]}')
    print(f'  short_name: {r[6]}')
    print()

conn.close()