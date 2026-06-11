import sqlite3

conn = sqlite3.connect('C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/product_master.db')
cursor = conn.cursor()

# Check for any pending translations
cursor.execute('''SELECT id, name, short_name, translation_status 
                 FROM product_master 
                 WHERE translation_status != 'translated' 
                    OR short_name IS NULL 
                    OR short_name = '' 
                 LIMIT 20''')
pending = cursor.fetchall()

print(f"Found {len(pending)} pending items:")
for row in pending:
    print(f"  {row[0]}: {row[1][:50] if row[1] else 'NULL'}... -> [{row[2]}] status={row[3]}")

conn.close()
