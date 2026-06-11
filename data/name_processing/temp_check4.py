import sqlite3

master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(master_db)
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables in product_master.db:')
for t in tables:
    print(f'  {t[0]}')

# Check events table if exists
try:
    cursor.execute('SELECT COUNT(*) FROM events')
    count = cursor.fetchone()[0]
    print(f'\nEvents count: {count}')
    
    # Check if events have title info
    cursor.execute('PRAGMA table_info(events)')
    cols = cursor.fetchall()
    print('Events columns:')
    for c in cols:
        print(f'  {c[1]} ({c[2]})')
except:
    print('No events table')

conn.close()