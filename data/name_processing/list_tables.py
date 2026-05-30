import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\ecomagent.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# List all tables
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = c.fetchall()
print("Tables in database:")
for t in tables:
    print(f"  - {t[0]}")

conn.close()
