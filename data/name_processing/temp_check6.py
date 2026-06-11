import sqlite3

conn = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db')
c = conn.cursor()

# 通过 products.id 查找 events
asins = ['B0BVH5QWM8', 'B0C1RC5Y7F', 'B0D6R7FSBF']
for asin in asins:
    # 先获取 product id
    c.execute("SELECT id, asin, name FROM products WHERE asin = ?", (asin,))
    product = c.fetchone()
    if product:
        product_id = product[0]
        print(f"Product {asin} (id={product_id}): name='{product[2]}'")
        
        # 查找 events
        c.execute("SELECT event_type, old_value, new_value, created_at FROM events WHERE product_id = ? ORDER BY created_at DESC LIMIT 5", (product_id,))
        events = c.fetchall()
        if events:
            print(f"  Events ({len(events)}):")
            for e in events:
                print(f"    {e[0]}: {e[1]} -> {e[2]} ({e[3]})")
        else:
            print("  No events")

conn.close()