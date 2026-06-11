import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查看 pending 商品的完整信息
cursor.execute('SELECT ecom_code, name, short_name, platform, product_url FROM product_master WHERE translation_status = "pending" LIMIT 20')
print("Pending items details:")
for row in cursor.fetchall():
    ecom_code, name, short_name, platform, product_url = row
    print(f"  {ecom_code}: platform={platform}")
    print(f"    name: '{name}'")
    print(f"    short_name: '{short_name}'")
    print(f"    url: {product_url}")
    print()

conn.close()