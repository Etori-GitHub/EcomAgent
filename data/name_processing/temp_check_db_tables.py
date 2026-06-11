import sqlite3
import os

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\product_master.db'
print(f'DB exists: {os.path.exists(db_path)}')
print(f'DB size: {os.path.getsize(db_path) if os.path.exists(db_path) else 0}')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f'Tables: {[t[0] for t in tables]}')

conn.close()
