import sqlite3

master_conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
tiktok_conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\tiktok.db')

master_cursor = master_conn.cursor()
tiktok_cursor = tiktok_conn.cursor()

# 检查 master_id 关联
master_cursor.execute('''
    SELECT ecom_code, platform_id 
    FROM product_master 
    WHERE translation_status = 'pending'
    AND platform = 'tiktok'
    LIMIT 5
''')
pending_items = master_cursor.fetchall()

print('Checking master_id association:')
for ecom_code, platform_id in pending_items:
    # 尝试通过 master_id 关联
    tiktok_cursor.execute('SELECT tiktokshop_id, name, master_id FROM tiktok_products WHERE master_id = (SELECT id FROM product_master WHERE ecom_code = ?)', (ecom_code,))
    result = tiktok_cursor.fetchone()
    if result:
        print(f'{ecom_code}: master_id match -> {result[1][:50] if result[1] else "NULL"}...')
    else:
        print(f'{ecom_code}: No match found (platform_id: {platform_id})')

# 检查 tiktok_products 中的 master_id
tiktok_cursor.execute('SELECT tiktokshop_id, name, master_id FROM tiktok_products WHERE master_id IS NOT NULL LIMIT 5')
print('\nTikTok products with master_id:')
for row in tiktok_cursor.fetchall():
    print(f'  tiktokshop_id: {row[0]}, master_id: {row[2]}, name: {row[1][:40] if row[1] else "NULL"}...')

master_conn.close()
tiktok_conn.close()
