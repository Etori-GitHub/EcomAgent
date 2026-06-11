import sqlite3

master = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
amazon = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db')

# Get pending items
pending = master.execute("SELECT ecom_code, platform_id, name FROM product_master WHERE translation_status = 'pending'").fetchall()
print(f'Pending count: {len(pending)}')

found = 0
not_found = []
for ecom_code, asin, master_name in pending:
    result = amazon.execute('SELECT name FROM products WHERE asin = ?', (asin,)).fetchone()
    if result and result[0]:
        found += 1
        print(f'{ecom_code}: {asin} -> {result[0][:60]}')
    else:
        not_found.append((ecom_code, asin, master_name))

print(f'\nFound: {found}, Not found: {len(not_found)}')
if not_found:
    print('\nNot found items:')
    for ecom_code, asin, master_name in not_found[:5]:
        print(f'{ecom_code}: {asin} (master_name: {master_name})')

master.close()
amazon.close()