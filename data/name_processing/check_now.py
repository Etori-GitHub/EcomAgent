import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

# Total count
total = conn.execute('SELECT COUNT(*) FROM product_master').fetchone()[0]

# With short_name
with_short = conn.execute('SELECT COUNT(*) FROM product_master WHERE short_name IS NOT NULL AND short_name != ""').fetchone()[0]

# Without short_name
without_short = total - with_short

# Sample
sample = conn.execute('SELECT ecom_code, name, short_name FROM product_master WHERE short_name IS NOT NULL AND short_name != "" LIMIT 5').fetchall()

conn.close()

print(f"Total products: {total}")
print(f"With short_name: {with_short}")
print(f"Without short_name: {without_short}")
print(f"\nSample:")
for row in sample:
    print(f"  {row[0]}: {row[1][:40]}... -> {row[2]}")
