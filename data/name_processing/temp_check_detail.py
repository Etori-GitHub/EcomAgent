import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
cursor = conn.cursor()

# 查看 pending 状态商品的详细信息
cursor.execute('''
    SELECT ecom_code, platform, platform_id, product_url, name, short_name 
    FROM product_master 
    WHERE translation_status = 'pending'
    LIMIT 10
''')
print('Pending items details:')
for row in cursor.fetchall():
    print(f'  ecom_code: {row[0]}')
    print(f'  platform: {row[1]}')
    print(f'  platform_id: {row[2]}')
    print(f'  product_url: {row[3]}')
    print(f'  name: {row[4]!r}')
    print(f'  short_name: {row[5]!r}')
    print()

conn.close()
