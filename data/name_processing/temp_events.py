import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db')
c = conn.cursor()

# Check events table schema
c.execute("PRAGMA table_info(events)")
print("Events schema:", c.fetchall())

# Check if events has title/name
c.execute("SELECT * FROM events LIMIT 1")
print("\nSample event:", c.fetchone())

conn.close()
