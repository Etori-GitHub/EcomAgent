import sqlite3
import os

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)
cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"Tables: {tables}")

for table in tables:
    cursor = conn.execute(f"PRAGMA table_info({table[0]})")
    cols = cursor.fetchall()
    print(f"\n{table[0]} columns:")
    for col in cols:
        print(f"  {col}")