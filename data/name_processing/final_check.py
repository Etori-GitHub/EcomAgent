import sqlite3

master_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(master_db)

# 查看所有需要翻译的产品（有 name 无 short_name）
cursor = conn.execute("""
    SELECT ecom_code, platform, platform_id, name, short_name
    FROM product_master 
    WHERE (short_name IS NULL OR short_name = '')
      AND (name IS NOT NULL AND name != '')
    LIMIT 20
""")
results = cursor.fetchall()

if results:
    print(f"Products needing translation: {len(results)}")
    for row in results:
        name_preview = row[3][:50] if row[3] and len(row[3]) > 50 else row[3]
        print(f"  [{row[0]}] {row[1]}/{row[2]}: {name_preview}")
else:
    print("All products with names have short_name")

# 统计
cursor = conn.execute("SELECT COUNT(*) FROM product_master")
total = cursor.fetchone()[0]

cursor = conn.execute("SELECT COUNT(*) FROM product_master WHERE name IS NOT NULL AND name != ''")
with_name = cursor.fetchone()[0]

cursor = conn.execute("SELECT COUNT(*) FROM product_master WHERE short_name IS NOT NULL AND short_name != ''")
with_short = cursor.fetchone()[0]

print(f"\nStats:")
print(f"  Total: {total}")
print(f"  With name: {with_name}")
print(f"  With short_name: {with_short}")
print(f"  Coverage: {with_short}/{with_name} = {100*with_short/with_name:.1f}%" if with_name > 0 else "  N/A")