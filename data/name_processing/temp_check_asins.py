import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db')
c = conn.cursor()

asins = ['B0DDZRY1W2', 'B0CLPGQWNB', 'B0DNMJ694B']

for asin in asins:
    c.execute('SELECT id, asin, name FROM products WHERE asin = ?', (asin,))
    r = c.fetchone()
    if r:
        print(f'Found: id={r[0]}, asin={r[1]}, name={r[2]}')
        # 检查 events
        c2 = conn.cursor()
        c2.execute('SELECT COUNT(*) FROM events WHERE product_id = ?', (r[0],))
        count = c2.fetchone()[0]
        print(f'  Events count: {count}')
    else:
        print(f'Not found: {asin}')

conn.close()
