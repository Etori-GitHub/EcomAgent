import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
cursor = conn.cursor()

# 查看已翻译的记录示例
print("已翻译的记录示例 (前20条):")
cursor.execute("""
    SELECT id, ecom_code, name, short_name 
    FROM product_master 
    LIMIT 20
""")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, ecom_code: {row[1]}")
    print(f"  name: {row[2][:80]}..." if len(row[2]) > 80 else f"  name: {row[2]}")
    print(f"  short_name: {row[3]}")
    print()

# 统计总数
cursor.execute("SELECT COUNT(*) FROM product_master")
print(f"总计: {cursor.fetchone()[0]} 条记录")

conn.close()
