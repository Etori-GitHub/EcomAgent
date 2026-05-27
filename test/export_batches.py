"""
分批导出商品名称，每批 50 个
用于手动翻译
"""
import sqlite3
import json
import os

BATCH_SIZE = 50
OUTPUT_DIR = 'data/name_processing/batches'

def export_batches():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
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
    
    # 合并
    all_products = []
    for p in amazon_products:
        all_products.append({"platform": "amazon", "id": p[0], "name": p[1]})
    for p in tiktok_products:
        all_products.append({"platform": "tiktok", "id": str(p[0]), "name": p[1]})
    
    # 分批
    batch_count = (len(all_products) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for i in range(0, len(all_products), BATCH_SIZE):
        batch = all_products[i:i+BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        
        filename = f"{OUTPUT_DIR}/batch_{batch_num:03d}_of_{batch_count:03d}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "batch_num": batch_num,
                "total_batches": batch_count,
                "items": batch
            }, f, ensure_ascii=False, indent=2)
        
        print(f"导出批次 {batch_num}/{batch_count}: {len(batch)} 个商品 -> {filename}")
    
    print(f"\n总计 {len(all_products)} 个商品，分为 {batch_count} 批")

if __name__ == "__main__":
    export_batches()
