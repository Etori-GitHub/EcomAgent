import sqlite3

amazon_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
conn = sqlite3.connect(amazon_db)
c = conn.cursor()

# 查看有有效名称的产品
c.execute("SELECT asin, name FROM products WHERE name IS NOT NULL AND name != '' AND name != 'Amazon.com' LIMIT 10")
for row in c.fetchall():
    print(f'{row[0]}: {row[1][:80]}')
conn.close()
