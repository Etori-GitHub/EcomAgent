import sqlite3

# 连接数据库
amazon_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
conn = sqlite3.connect(amazon_db)
c = conn.cursor()

asins = ['B0DDZMFDS3', 'B08VLMQ3KS', 'B0GY49NMDM', 'B0BVH5QWM8', 'B0CGVPMJBP']
for asin in asins:
    c.execute('SELECT asin, name FROM products WHERE asin = ?', (asin,))
    result = c.fetchone()
    if result:
        name = result[1][:80] if result[1] else 'NULL'
        print(f'{result[0]}: {name}')
    else:
        print(f'{asin}: NOT FOUND')

conn.close()
