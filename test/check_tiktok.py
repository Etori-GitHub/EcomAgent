import sqlite3

conn = sqlite3.connect('data/tiktok.db')
cursor = conn.cursor()

# 查看表结构
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("TikTok 数据库表:", tables)

if tables:
    for table in tables:
        table_name = table[0]
        print(f"\n表 {table_name} 结构:")
        schema = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
        for col in schema:
            print(f"  {col}")
        
        count = cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"  记录数: {count}")
