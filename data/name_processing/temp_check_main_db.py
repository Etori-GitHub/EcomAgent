import sqlite3
import os

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
print(f'DB exists: {os.path.exists(db_path)}')
print(f'DB size: {os.path.getsize(db_path) if os.path.exists(db_path) else 0}')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f'Tables: {[t[0] for t in tables]}')

# Check for pending translations
for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    print(f'\n{table_name} columns: {columns}')
    
    if 'short_name' in columns:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE short_name IS NULL OR short_name = ''")
        pending = cursor.fetchone()[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total = cursor.fetchone()[0]
        print(f'  Total: {total}, Pending: {pending}')

conn.close()
