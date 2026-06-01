import sqlite3

# Check amazon.db
print("=== amazon.db ===")
try:
    conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db')
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Tables: {[t[0] for t in tables]}")
    
    for table in tables:
        table_name = table[0]
        cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  {table_name}: {count} rows")
    
    # Check for products with names in amazon tables
    for table in tables:
        table_name = table[0]
        if 'product' in table_name.lower() or 'bestseller' in table_name.lower():
            cursor = conn.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            print(f"\n  {table_name} columns: {columns}")
            
            if 'title' in columns or 'name' in columns:
                name_col = 'title' if 'title' in columns else 'name'
                cursor = conn.execute(f"SELECT {name_col} FROM {table_name} WHERE {name_col} IS NOT NULL AND {name_col} != '' LIMIT 3")
                samples = cursor.fetchall()
                if samples:
                    print(f"  Sample names from {table_name}:")
                    for s in samples:
                        print(f"    - {s[0][:80]}...")
    conn.close()
except Exception as e:
    print(f"Error: {e}")

# Check tiktok.db
print("\n=== tiktok.db ===")
try:
    conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\tiktok.db')
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Tables: {[t[0] for t in tables]}")
    
    for table in tables:
        table_name = table[0]
        cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  {table_name}: {count} rows")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
