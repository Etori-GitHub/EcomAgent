import sqlite3

conn = sqlite3.connect('data/amazon.db')
cursor = conn.cursor()

# 统计
total = cursor.execute('SELECT COUNT(*) FROM products').fetchone()[0]
with_short = cursor.execute('SELECT COUNT(*) FROM products WHERE short_name IS NOT NULL AND short_name != ""').fetchone()[0]
need_translate = total - with_short

print(f"总商品数: {total}")
print(f"有简称: {with_short}")
print(f"需翻译: {need_translate}")

# 查看前20个商品的name
print("\n前20个商品名称:")
cursor.execute('SELECT asin, name FROM products LIMIT 20')
for i, row in enumerate(cursor.fetchall(), 1):
    print(f"{i}. [{row[0]}] {row[1][:80]}")
