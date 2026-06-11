import sqlite3
import os

# 检查所有数据库文件
data_dir = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data'
db_files = [f for f in os.listdir(data_dir) if f.endswith('.db')]
print(f"Database files: {db_files}")

for db_file in db_files:
    db_path = os.path.join(data_dir, db_file)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # 获取所有表
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    print(f"\n{db_file} tables: {[t[0] for t in tables]}")
    
    # 检查是否有 name 相关字段
    for table in tables:
        c.execute(f"PRAGMA table_info({table[0]})")
        cols = c.fetchall()
        for col in cols:
            if 'name' in col[1].lower() or 'title' in col[1].lower():
                print(f"  {table[0]}.{col[1]}: found")
    
    conn.close()