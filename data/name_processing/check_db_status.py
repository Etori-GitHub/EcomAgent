import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

# Get tables
cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"Tables: {[t[0] for t in tables]}")

# Check product_master table
for table in tables:
    table_name = table[0]
    cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"  {table_name}: {count} rows")

# Check columns in product_master
cursor = conn.execute("PRAGMA table_info(product_master)")
columns = cursor.fetchall()
print(f"\nColumns in product_master:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

# Sample data
cursor = conn.execute("SELECT * FROM product_master LIMIT 3")
rows = cursor.fetchall()
if rows:
    print(f"\nSample data:")
    for row in rows:
        print(f"  {row}")

conn.close()
