import sqlite3
import json

# 连接数据库
amazon_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'

conn_amazon = sqlite3.connect(amazon_db)
conn_master = sqlite3.connect(master_db)

c_amazon = conn_amazon.cursor()
c_master = conn_master.cursor()

# 检查 events 表数据样本
print("Events 表数据样本:")
c_amazon.execute("SELECT * FROM events LIMIT 3")
for row in c_amazon.fetchall():
    print(f"  {row}")

# 检查 products 表的 id 和 asin 关联
print("\nProducts 表数据样本:")
c_amazon.execute("SELECT id, asin, name FROM products LIMIT 5")
for row in c_amazon.fetchall():
    print(f"  id={row[0]}, asin={row[1]}, name={row[2][:50] if row[2] else 'NULL'}")

# 检查 pending 商品是否有对应的 products 表记录
print("\nPending 商品检查:")
pending_asins = ['B0DDZMFDS3', 'B08VLMQ3KS', 'B0C21QMW48']
for asin in pending_asins:
    c_amazon.execute("SELECT id, asin, name FROM products WHERE asin = ?", (asin,))
    product = c_amazon.fetchone()
    if product:
        print(f"  ASIN {asin}: id={product[0]}, name={product[2][:50] if product[2] else 'NULL'}")
        # 检查这个产品的 events
        c_amazon.execute("SELECT event_type, old_value, new_value FROM events WHERE product_id = ? LIMIT 3", (product[0],))
        events = c_amazon.fetchall()
        if events:
            for e in events:
                print(f"    Event: type={e[0]}, old={e[1][:30] if e[1] else 'NULL'}, new={e[2][:30] if e[2] else 'NULL'}")
    else:
        print(f"    No events for product_id {product[0]}")

conn_amazon.close()
conn_master.close()