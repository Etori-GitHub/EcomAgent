import sqlite3

amazon_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
conn = sqlite3.connect(amazon_db)
c = conn.cursor()

# 检查表结构
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables in amazon.db:", c.fetchall())

# 检查 products 表结构
c.execute("PRAGMA table_info(products)")
print("\nProducts table columns:")
for col in c.fetchall():
    print(f"  {col}")

# 检查是否有数据
c.execute("SELECT COUNT(*) FROM products")
print(f"\nTotal products in amazon.db: {c.fetchone()[0]}")

# 检查是否有 name 字段
c.execute("SELECT asin, name FROM products LIMIT 5")
print("\nSample products:")
for row in c.fetchall():
    print(f"  ASIN: {row[0]}, Name: {row[1][:50] if row[1] else 'None'}...")

# 检查是否能找到这些 ASIN
test_asins = ['B0BVH5QWM8', 'B0BMGBBPTT', 'B0DDZRY1W2']
c.execute(f"SELECT asin, name FROM products WHERE asin IN ({','.join(['?' for _ in test_asins])})", test_asins)
print("\nSearching for test ASINs:")
for row in c.fetchall():
    print(f"  Found: {row[0]} - {row[1][:50] if row[1] else 'None'}...")

conn.close()
