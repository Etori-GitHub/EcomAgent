import sqlite3

conn = sqlite3.connect('data/product_master.db')
c = conn.cursor()

c.execute('SELECT COUNT(*) FROM product_master WHERE short_name IS NULL OR short_name = ""')
pending = c.fetchone()[0]

c.execute('SELECT COUNT(*) FROM product_master WHERE short_name IS NOT NULL AND short_name != ""')
done = c.fetchone()[0]

print(f"待翻译: {pending}")
print(f"已翻译: {done}")

conn.close()