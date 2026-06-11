import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
c = conn.cursor()

# Check translation_status distribution
c.execute("SELECT translation_status, COUNT(*) FROM product_master GROUP BY translation_status")
results = c.fetchall()
print("Translation status distribution:")
for status, count in results:
    print(f"  {status}: {count}")

# Check pending count
c.execute("SELECT COUNT(*) FROM product_master WHERE translation_status = 'pending'")
pending = c.fetchone()[0]
print(f"\nPending count: {pending}")

conn.close()