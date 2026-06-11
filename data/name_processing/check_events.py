import sqlite3
import json

# 连接数据库
amazon_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
conn = sqlite3.connect(amazon_db)
c = conn.cursor()

# 检查 events 表结构
print("Events 表结构:")
c.execute("PRAGMA table_info(events)")
for col in c.fetchall():
    print(f"  {col}")

# 检查 events 表数据量
c.execute("SELECT COUNT(*) FROM events")
print(f"\nEvents 总数: {c.fetchone()[0]}")

# 检查 pending ASIN 的 events
pending_asins = ['B0DDZMFDS3', 'B08VLMQ3KS', 'B0C21QMW48']
for asin in pending_asins:
    c.execute("SELECT * FROM events WHERE asin = ? LIMIT 1", (asin,))
    row = c.fetchone()
    print(f"\nASIN {asin} event: {row}")

conn.close()