import sqlite3

tiktok_conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\tiktok.db')
tiktok_cursor = tiktok_conn.cursor()

# 检查 tiktok_products 表中有多少条记录
tiktok_cursor.execute('SELECT COUNT(*) FROM tiktok_products')
count = tiktok_cursor.fetchone()[0]
print(f'Total TikTok products: {count}')

# 查看一些记录
tiktok_cursor.execute('SELECT tiktokshop_id, name FROM tiktok_products WHERE name IS NOT NULL AND name != "" LIMIT 5')
print('\nSample products with names:')
for row in tiktok_cursor.fetchall():
    print(f'  {row[0]}: {row[1][:60]}...')

# 检查有多少记录有名称
tiktok_cursor.execute('SELECT COUNT(*) FROM tiktok_products WHERE name IS NOT NULL AND name != ""')
with_name = tiktok_cursor.fetchone()[0]
print(f'\nProducts with names: {with_name}')

tiktok_conn.close()
