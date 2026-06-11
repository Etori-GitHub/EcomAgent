import sqlite3
import os

# 查找所有数据库
db_files = []
for root, dirs, files in os.walk('data'):
    for f in files:
        if f.endswith('.db'):
            db_files.append(os.path.join(root, f))

print('Found databases:', db_files[:10])

# 检查每个数据库
for db_path in db_files[:5]:
    print(f'\n=== {db_path} ===')
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print('Tables:', [t[0] for t in tables])
        conn.close()
    except Exception as e:
        print('Error:', e)