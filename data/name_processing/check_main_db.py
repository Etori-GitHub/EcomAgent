import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
c = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = c.fetchall()
print("Tables:", [t[0] for t in tables])

for table in tables:
    c = conn.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = c.fetchone()[0]
    print(f"\n{table[0]}: {count} rows")
    
    # Get columns
    c = conn.execute(f"PRAGMA table_info({table[0]})")
    cols = [col[1] for col in c.fetchall()]
    print(f"Columns: {cols}")

conn.close()
