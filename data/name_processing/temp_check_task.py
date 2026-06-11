import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\product_master.db')
cursor = conn.cursor()

# Check pending count
cursor.execute("SELECT COUNT(*) FROM product_master WHERE short_name IS NULL OR short_name = ''")
pending = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM product_master')
total = cursor.fetchone()[0]

print(f'Total: {total}, Pending translation: {pending}')

# Show some samples
cursor.execute('SELECT id, ecom_code, name, short_name FROM product_master LIMIT 5')
for row in cursor.fetchall():
    name_preview = row[2][:50] if row[2] else 'N/A'
    print(f'{row[0]}: {row[1]} | {name_preview}... -> {row[3]}')

conn.close()
