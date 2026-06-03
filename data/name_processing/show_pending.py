import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
c = conn.execute('SELECT id, ecom_code, name FROM product_master WHERE short_name IS NULL OR short_name = "" LIMIT 30')
for r in c.fetchall():
    name = r[2][:80] if r[2] else "N/A"
    print(f'{r[0]}|{r[1]}|{name}')
