import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

# 查找需要翻译的：有 name 但没有 short_name
cursor = conn.execute("""
    SELECT id, ecom_code, name 
    FROM product_master 
    WHERE (short_name IS NULL OR short_name = '') 
      AND name IS NOT NULL 
      AND name != ''
    LIMIT 50
""")
results = cursor.fetchall()
print(f"Products needing translation: {len(results)}")

# 统计
cursor = conn.execute("""
    SELECT COUNT(*) FROM product_master 
    WHERE (short_name IS NULL OR short_name = '') 
      AND name IS NOT NULL 
      AND name != ''
""")
need_count = cursor.fetchone()[0]
print(f"Total needing translation: {need_count}")

if results:
    print("\nSample products:")
    for row in results[:5]:
        print(f"  [{row[1]}] {row[2][:70]}..." if len(row[2]) > 70 else f"  [{row[1]}] {row[2]}")