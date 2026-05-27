import sqlite3
import json

# 导出需要翻译的商品名称
def export_names():
    # Amazon
    conn_amazon = sqlite3.connect('data/amazon.db')
    cursor_amazon = conn_amazon.cursor()
    cursor_amazon.execute('SELECT asin, name FROM products')
    amazon_products = cursor_amazon.fetchall()
    conn_amazon.close()
    
    # TikTok
    conn_tiktok = sqlite3.connect('data/tiktok.db')
    cursor_tiktok = conn_tiktok.cursor()
    cursor_tiktok.execute('SELECT id, name FROM tiktok_products')
    tiktok_products = cursor_tiktok.fetchall()
    conn_tiktok.close()
    
    # 保存到文件
    data = {
        "amazon": [{"id": p[0], "name": p[1]} for p in amazon_products],
        "tiktok": [{"id": str(p[0]), "name": p[1]} for p in tiktok_products]
    }
    
    with open('data/name_processing/all_products.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Amazon: {len(amazon_products)} 个商品")
    print(f"TikTok: {len(tiktok_products)} 个商品")
    print(f"总计: {len(amazon_products) + len(tiktok_products)} 个商品")
    print(f"已保存到: data/name_processing/all_products.json")

if __name__ == "__main__":
    export_names()
