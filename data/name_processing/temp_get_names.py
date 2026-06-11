import sqlite3
import json

# 连接两个数据库
master_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db'
amazon_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db'
tiktok_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\tiktok.db'

# 获取待翻译的商品
master_conn = sqlite3.connect(master_path)
master_cursor = master_conn.cursor()

master_cursor.execute("""
    SELECT ecom_code, platform, platform_id, name 
    FROM product_master 
    WHERE translation_status = 'pending' 
    LIMIT 50
""")
pending_items = master_cursor.fetchall()
print(f"Found {len(pending_items)} pending items")

# 检查哪些有名字
items_with_name = [(item[0], item[1], item[2], item[3]) for item in pending_items if item[3]]
items_without_name = [(item[0], item[1], item[2]) for item in pending_items if not item[3]]

print(f"With name: {len(items_with_name)}")
print(f"Without name: {len(items_without_name)}")

# 对于没有名字的，尝试从源数据库获取
if items_without_name:
    amazon_conn = sqlite3.connect(amazon_path)
    amazon_cursor = amazon_conn.cursor()
    
    tiktok_conn = sqlite3.connect(tiktok_path)
    tiktok_cursor = tiktok_conn.cursor()
    
    # 检查 tiktok 表结构
    tiktok_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print(f"TikTok tables: {[t[0] for t in tiktok_cursor.fetchall()]}")
    
    for ecom_code, platform, platform_id in items_without_name[:5]:
        print(f"\n{ecom_code}: platform={platform}, platform_id={platform_id}")
        
        if platform == 'amazon':
            amazon_cursor.execute("SELECT name FROM products WHERE asin = ?", (platform_id,))
            result = amazon_cursor.fetchone()
            if result:
                print(f"  Amazon name: {result[0]}")
        elif platform == 'tiktok':
            tiktok_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = tiktok_cursor.fetchall()
            # 尝试 products 表
            try:
                tiktok_cursor.execute("SELECT * FROM products WHERE id = ? LIMIT 1", (platform_id,))
                cols = [desc[0] for desc in tiktok_cursor.description]
                print(f"  TikTok columns: {cols}")
            except:
                pass
    
    amazon_conn.close()
    tiktok_conn.close()

master_conn.close()