import sqlite3
import os

# 检查所有数据库文件
db_files = [f for f in os.listdir('.') if f.endswith('.db')]
print('Available databases:', db_files)

for db_file in db_files:
    print(f'\n=== {db_file} ===')
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    for table in tables:
        print(f'  Table: {table[0]}')
    conn.close()
