import sqlite3

# Check amazon.db
conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db')
cursor = conn.execute("SELECT COUNT(*) FROM products WHERE name IS NOT NULL AND name != ''")
total = cursor.fetchone()[0]
cursor = conn.execute("SELECT COUNT(*) FROM products WHERE name IS NOT NULL AND name != '' AND master_id IS NOT NULL")
linked = cursor.fetchone()[0]
print(f'Amazon products with name: {total}')
print(f'Amazon products linked to master: {linked}')
conn.close()

# Check tiktok.db
conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\tiktok.db')
cursor = conn.execute("PRAGMA table_info(tiktok_products)")
columns = cursor.fetchall()
print('\nTikTok products columns:')
for col in columns:
    print(f'  {col[1]} ({col[2]})')
cursor = conn.execute("SELECT COUNT(*) FROM tiktok_products WHERE name IS NOT NULL AND name != ''")
total = cursor.fetchone()[0]
print(f'\nTikTok products with name: {total}')
conn.close()