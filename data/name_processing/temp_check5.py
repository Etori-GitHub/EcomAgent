import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db')
c = conn.cursor()

# 检查所有表
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables:", c.fetchall())

# 检查 events 表是否存在
c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='events'")
schema = c.fetchone()
if schema:
    print("\nEvents schema:")
    print(schema[0])
    
    # 查找这些 ASIN 的 events
    asins = ['B0BVH5QWM8', 'B0C1RC5Y7F', 'B0D6R7FSBF']
    for asin in asins:
        c.execute("SELECT * FROM events WHERE asin = ? LIMIT 1", (asin,))
        result = c.fetchone()
        if result:
            print(f"\nASIN {asin}: {result[:5]}...")
else:
    print("No events table")

conn.close()
