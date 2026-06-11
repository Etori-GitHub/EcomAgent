import sqlite3

conn = sqlite3.connect('product_master.db')
cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables:', [t[0] for t in tables])

for table in tables:
    table_name = table[0]
    cursor = conn.execute(f'PRAGMA table_info({table_name})')
    cols = cursor.fetchall()
    print(f'\n{table_name} columns: {[c[1] for c in cols]}')
    cursor = conn.execute(f'SELECT COUNT(*) FROM {table_name}')
    count = cursor.fetchone()[0]
    print(f'  Count: {count}')

conn.close()
