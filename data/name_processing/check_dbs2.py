import sqlite3

# 检查主数据库
conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('product_master.db Tables:', [t[0] for t in tables])

for t in tables:
    cursor.execute(f'SELECT COUNT(*) FROM {t[0]}')
    count = cursor.fetchone()[0]
    print(f'  {t[0]}: {count} rows')
    cursor.execute(f"PRAGMA table_info({t[0]})")
    columns = cursor.fetchall()
    print(f'    Columns: {[c[1] for c in columns]}')

conn.close()

print('\n' + '='*50 + '\n')

# 检查amazon数据库
conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('amazon.db Tables:', [t[0] for t in tables])

for t in tables:
    cursor.execute(f'SELECT COUNT(*) FROM {t[0]}')
    count = cursor.fetchone()[0]
    print(f'  {t[0]}: {count} rows')
    cursor.execute(f"PRAGMA table_info({t[0]})")
    columns = cursor.fetchall()
    print(f'    Columns: {[c[1] for c in columns]}')

conn.close()
