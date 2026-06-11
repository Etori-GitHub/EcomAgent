import sqlite3
import json

# Check product_master.db
conn = sqlite3.connect('C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/product_master.db')
cursor = conn.cursor()

# Get tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables in product_master.db:', [t[0] for t in tables])

# Check for products with short_name status
for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"\n{table_name} columns: {columns}")
    
    # Check if has short_name column
    if 'short_name' in columns:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE short_name IS NULL OR short_name = ''")
        null_count = cursor.fetchone()[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total = cursor.fetchone()[0]
        print(f"  Total: {total}, Missing short_name: {null_count}")
        
        # Get sample of missing
        if null_count > 0:
            cursor.execute(f"SELECT master_id, name FROM {table_name} WHERE short_name IS NULL OR short_name = '' LIMIT 5")
            samples = cursor.fetchall()
            print(f"  Sample missing: {samples[:3]}")

conn.close()
