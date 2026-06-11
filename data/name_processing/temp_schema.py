import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables:", c.fetchall())

# Check schema of products table
c.execute("PRAGMA table_info(products)")
print("\nProducts schema:", c.fetchall())

# Check if there's any data with name
c.execute("SELECT asin, name, title FROM products WHERE name IS NOT NULL AND name != '' LIMIT 5")
print("\nSample with name:", c.fetchall())

conn.close()
