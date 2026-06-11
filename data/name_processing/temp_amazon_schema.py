import sqlite3

# 查看 amazon.db 表结构
amazon_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
conn = sqlite3.connect(amazon_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Amazon tables:", [t[0] for t in tables])

# 查看第一个表的结构
if tables:
    cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{tables[0][0]}'")
    print(f"\n{tables[0][0]} schema:")
    print(cursor.fetchone()[0])
    
    # 看几条数据
    cursor.execute(f"SELECT * FROM {tables[0][0]} LIMIT 2")
    cols = [desc[0] for desc in cursor.description]
    print(f"\nColumns: {cols}")
    for row in cursor.fetchall():
        print(row)

conn.close()