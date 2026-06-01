import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db')
cursor = conn.execute("SELECT id, name FROM products WHERE short_name IS NULL OR short_name = '' LIMIT 10")
results = cursor.fetchall()
print(f"Found {len(results)} products without short_name:")
for row in results:
    print(f"  {row[0]}: {row[1][:80]}..." if len(row[1]) > 80 else f"  {row[0]}: {row[1]}")