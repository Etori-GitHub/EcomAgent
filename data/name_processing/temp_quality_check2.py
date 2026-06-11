import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
cursor = conn.cursor()

# 检查 short_name 长度 <= 10 的记录（可能质量问题）
print("short_name 长度 <= 10 的记录 (前30条):")
cursor.execute("""
    SELECT id, ecom_code, name, short_name 
    FROM product_master 
    WHERE LENGTH(short_name) <= 10
    LIMIT 30
""")
for row in cursor.fetchall():
    print(f"  ID: {row[0]}, ecom_code: {row[1]}")
    print(f"    name: {row[2]}")
    print(f"    short_name: {row[3]}")
    print()

# 检查 short_name 以英文结尾的（可能截断）
print("\nshort_name 以英文字母结尾的记录 (前20条):")
cursor.execute("""
    SELECT id, ecom_code, name, short_name 
    FROM product_master 
    WHERE short_name LIKE '%a' OR short_name LIKE '%b' OR short_name LIKE '%c' 
       OR short_name LIKE '%d' OR short_name LIKE '%e' OR short_name LIKE '%f'
       OR short_name LIKE '%g' OR short_name LIKE '%h' OR short_name LIKE '%i'
       OR short_name LIKE '%j' OR short_name LIKE '%k' OR short_name LIKE '%l'
       OR short_name LIKE '%m' OR short_name LIKE '%n' OR short_name LIKE '%o'
       OR short_name LIKE '%p' OR short_name LIKE '%q' OR short_name LIKE '%r'
       OR short_name LIKE '%s' OR short_name LIKE '%t' OR short_name LIKE '%u'
       OR short_name LIKE '%v' OR short_name LIKE '%w' OR short_name LIKE '%x'
       OR short_name LIKE '%y' OR short_name LIKE '%z'
    LIMIT 20
""")
for row in cursor.fetchall():
    print(f"  ID: {row[0]}, ecom_code: {row[1]}")
    print(f"    name: {row[2]}")
    print(f"    short_name: {row[3]}")
    print()

conn.close()
