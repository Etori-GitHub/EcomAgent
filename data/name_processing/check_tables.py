import sqlite3

conn = sqlite3.connect('product_master.db')
c = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = c.fetchall()
print("Tables:", [t[0] for t in tables])

for table in tables:
    c = conn.execute(f"SELECT COUNT(*) FROM {table[0]}")
    print(f"{table[0]}: {c.fetchone()[0]} rows")

conn.close()
