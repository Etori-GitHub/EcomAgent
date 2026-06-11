import sqlite3

amazon_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
conn = sqlite3.connect(amazon_path)
cursor = conn.cursor()

# 查看具体的 ASIN 数据
asins = ['B0DDZMFDS3', 'B08VLMQ3KS', 'B0C21QMW48', 'B0BX4XG53Z', 'B0C544TBQM']

for asin in asins:
    cursor.execute("SELECT * FROM products WHERE asin = ?", (asin,))
    row = cursor.fetchone()
    if row:
        cols = [desc[0] for desc in cursor.description]
        print(f"\n{asin}:")
        for i, col in enumerate(cols):
            print(f"  {col}: {row[i]}")
    else:
        print(f"\n{asin}: NOT FOUND")

conn.close()