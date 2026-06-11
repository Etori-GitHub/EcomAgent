import sqlite3

amazon_db = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
conn = sqlite3.connect(amazon_db)
cursor = conn.cursor()

asins = ['B0DDZRY1W2', 'B0DNMJ694B', 'B0D9Q5MZRD', 'B09K58K13V', 'B0CJC2C3F5', 
         'B0GQ6F965V', 'B0BRGT4699', 'B0F3J1GXTD', 'B0GCD9F4LC']

for asin in asins:
    cursor.execute('SELECT asin, name FROM products WHERE asin = ?', (asin,))
    result = cursor.fetchone()
    if result:
        name = result[1][:80] if result[1] else "NULL"
        print(f'{result[0]}: {name}')
    else:
        print(f'{asin}: NOT FOUND')

conn.close()