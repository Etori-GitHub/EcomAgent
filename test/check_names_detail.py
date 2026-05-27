import sqlite3

conn = sqlite3.connect('data/product_master.db')
c = conn.cursor()

# 检查前20个商品的简称
c.execute('''
    SELECT ecom_code, name, short_name 
    FROM product_master 
    WHERE short_name IS NOT NULL AND short_name != ""
    ORDER BY ecom_code
    LIMIT 20
''')
rows = c.fetchall()
print("商品简称检查:")
for r in rows:
    print(f"  {r[0]}: name={r[1][:30] if r[1] else 'NULL'}... | short_name={r[2]}")

conn.close()