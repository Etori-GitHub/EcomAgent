import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
conn = sqlite3.connect(db_path)

# List tables
cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables in amazon.db:', [t[0] for t in tables])

# Check each table structure
for table in tables:
    table_name = table[0]
    cursor = conn.execute(f'PRAGMA table_info({table_name})')
    cols = cursor.fetchall()
    print(f'\n{table_name} columns: {[c[1] for c in cols]}')
    cursor = conn.execute(f'SELECT * FROM {table_name} LIMIT 2')
    rows = cursor.fetchall()
    for r in rows:
        print(f'  Sample: {str(r)[:200]}')

conn.close()
