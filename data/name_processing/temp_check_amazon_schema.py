import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", [t[0] for t in tables])

# Check products table schema
for t in tables:
    cursor.execute(f"PRAGMA table_info({t[0]})")
    cols = cursor.fetchall()
    print(f"\n{t[0]} columns: {[c[1] for c in cols]}")
    cursor.execute(f"SELECT COUNT(*) FROM {t[0]}")
    count = cursor.fetchone()[0]
    print(f"  Count: {count}")
    if count > 0:
        cursor.execute(f"SELECT * FROM {t[0]} LIMIT 1")
        print(f"  Sample: {cursor.fetchone()}")

conn.close()