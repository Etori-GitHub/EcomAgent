import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
db_path = BASE_DIR / "data" / "product_master.db"

print(f"Checking: {db_path}")
print(f"Exists: {db_path.exists()}")

if db_path.exists():
    conn = sqlite3.connect(db_path)
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
        if count > 0:
            cursor = conn.execute(f'SELECT * FROM {table_name} LIMIT 3')
            for row in cursor.fetchall():
                print(f'  Sample: {str(row)[:150]}')
    
    conn.close()
else:
    print("Database does not exist!")
