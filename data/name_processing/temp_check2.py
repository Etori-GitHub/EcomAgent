import sqlite3

amazon_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
conn = sqlite3.connect(amazon_db)
cursor = conn.cursor()

# Get table schema
cursor.execute('PRAGMA table_info(products)')
columns = cursor.fetchall()
print('Columns in products table:')
for col in columns:
    print(f'  {col[1]} ({col[2]})')

# Check one product
cursor.execute('SELECT * FROM products WHERE asin = "B0DDZRY1W2" LIMIT 1')
row = cursor.fetchone()
if row:
    print('\nSample product B0DDZRY1W2:')
    col_names = [desc[0] for desc in cursor.description]
    for i, val in enumerate(row):
        if val:
            print(f'  {col_names[i]}: {str(val)[:100]}')

conn.close()
