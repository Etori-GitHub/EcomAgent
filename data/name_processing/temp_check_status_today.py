import sqlite3

conn = sqlite3.connect('C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/product_master.db')
cursor = conn.cursor()

# Check translation_status distribution
cursor.execute('SELECT translation_status, COUNT(*) FROM product_master GROUP BY translation_status')
status_counts = cursor.fetchall()
print('Translation status distribution:')
for status, count in status_counts:
    print(f'  {status}: {count}')

# Check pending items
cursor.execute("SELECT COUNT(*) FROM product_master WHERE translation_status = 'pending'")
pending = cursor.fetchone()[0]
print(f'\nPending items: {pending}')

# Check for items with null/empty short_name
cursor.execute("SELECT COUNT(*) FROM product_master WHERE short_name IS NULL OR short_name = ''")
missing = cursor.fetchone()[0]
print(f'Items missing short_name: {missing}')

conn.close()
