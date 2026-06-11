import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db')
c = conn.cursor()
c.execute("SELECT DISTINCT event_type FROM events")
types = c.fetchall()
print('Event types:', [t[0] for t in types])
conn.close()