import sqlite3

# 检查 tiktok.db
conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\tiktok.db')
cursor = conn.cursor()

# 列出所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables in tiktok.db:')
for t in tables:
    print(f'  {t[0]}')

# 检查表结构
for t in tables:
    table_name = t[0]
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"\n{table_name} columns: {columns}")

conn.close()
