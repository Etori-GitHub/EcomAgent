import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\product_master.db')
cursor = conn.cursor()

# 检查表结构
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables:', [t[0] for t in tables])

for t in tables:
    cursor.execute(f'SELECT COUNT(*) FROM {t[0]}')
    count = cursor.fetchone()[0]
    print(f'{t[0]}: {count} rows')
    
    # 获取表结构
    cursor.execute(f"PRAGMA table_info({t[0]})")
    columns = cursor.fetchall()
    print(f'  Columns: {[c[1] for c in columns]}')

conn.close()
