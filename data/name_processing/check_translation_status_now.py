import sqlite3

master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(master_db)
cursor = conn.cursor()

# Check translation status distribution
cursor.execute('''
    SELECT translation_status, COUNT(*) 
    FROM product_master 
    GROUP BY translation_status
''')
status_counts = cursor.fetchall()
print('Translation status distribution:')
for status, count in status_counts:
    print(f'  {status or "NULL"}: {count}')

# Check total
cursor.execute('SELECT COUNT(*) FROM product_master')
total = cursor.fetchone()[0]
print(f'\nTotal products: {total}')

# Check if all have short_name
cursor.execute('SELECT COUNT(*) FROM product_master WHERE short_name IS NOT NULL AND short_name != ""')
with_name = cursor.fetchone()[0]
print(f'With short_name: {with_name}')

# Sample some translated items
cursor.execute('SELECT ecom_code, name, short_name FROM product_master WHERE short_name IS NOT NULL LIMIT 5')
samples = cursor.fetchall()
print('\nSample translated items:')
for ecom_code, name, short_name in samples:
    print(f'  {ecom_code}: {name[:40]}... -> {short_name}')

conn.close()
