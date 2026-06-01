import sqlite3

db_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
conn = sqlite3.connect(db_path)

# Check ECAM26000801 specifically
cursor = conn.execute('''
    SELECT id, ecom_code, name, short_name
    FROM product_master 
    WHERE ecom_code = 'ECAM26000801'
''')
row = cursor.fetchone()
if row:
    print(f"Product ECAM26000801:")
    print(f"  id: {row[0]}")
    print(f"  ecom_code: {row[1]}")
    print(f"  name: '{row[2]}'")
    print(f"  short_name: {row[3]}")

# Check amazon db for this product
amazon_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
conn2 = sqlite3.connect(amazon_db)
cursor2 = conn2.execute('''
    SELECT asin, title, product_title 
    FROM products 
    WHERE asin = 'ECAM26000801'
''')
row2 = cursor2.fetchone()
if row2:
    print(f"\nAmazon data for ECAM26000801:")
    print(f"  asin: {row2[0]}")
    print(f"  title: '{row2[1]}'")
    print(f"  product_title: '{row2[2]}'")
else:
    print("\nNo Amazon data found for ECAM26000801")
    
    # Try to find it by checking the schema
    cursor2 = conn2.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor2.fetchall()
    print(f"\nTables in amazon.db: {[t[0] for t in tables]}")

conn.close()
conn2.close()
