import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db')
c = conn.cursor()

# 检查 name_changed 事件
c.execute("""
    SELECT e.product_id, e.old_value, e.new_value, p.asin
    FROM events e
    JOIN products p ON e.product_id = p.id
    WHERE e.event_type = 'name_changed'
    LIMIT 10
""")
rows = c.fetchall()
for r in rows:
    print(f'product_id={r[0]}, asin={r[3]}')
    print(f'  old: {r[1][:80] if r[1] else "NULL"}...')
    print(f'  new: {r[2][:80] if r[2] else "NULL"}...')
    print()

conn.close()