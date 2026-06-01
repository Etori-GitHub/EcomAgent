import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')

# Get table schema
cursor = conn.execute("PRAGMA table_info(product_master)")
columns = cursor.fetchall()

print("product_master table columns:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

conn.close()
