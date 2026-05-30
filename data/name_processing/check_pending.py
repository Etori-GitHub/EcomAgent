import sqlite3
import json

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\ecomagent.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Check if short_name column exists
c.execute("PRAGMA table_info(products)")
columns = [col[1] for col in c.fetchall()]
print("Columns:", columns)

# Count products without short_name
if 'short_name' in columns:
    c.execute("SELECT COUNT(*) FROM products WHERE short_name IS NULL OR short_name = ''")
    print("Products without short_name:", c.fetchone()[0])
    
    # Get some samples
    c.execute("SELECT id, name FROM products WHERE short_name IS NULL OR short_name = '' LIMIT 5")
    samples = c.fetchall()
    print("\nSample products:")
    for s in samples:
        print(f"  {s[0]}: {s[1][:50]}...")
else:
    print("short_name column does not exist")

conn.close()
