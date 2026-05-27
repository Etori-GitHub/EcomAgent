"""
导入翻译结果到数据库
"""
import sqlite3
import json
import os
import glob

def import_translations():
    translated_dir = 'data/name_processing/translated'
    
    amazon_conn = sqlite3.connect('data/amazon.db')
    amazon_cursor = amazon_conn.cursor()
    
    tiktok_conn = sqlite3.connect('data/tiktok.db')
    tiktok_cursor = tiktok_conn.cursor()
    
    amazon_updated = 0
    tiktok_updated = 0
    
    for filepath in glob.glob(f'{translated_dir}/batch_*.json'):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        batch_num = data.get('batch_num', '?')
        translations = data.get('translations', [])
        
        print(f"处理批次 {batch_num}: {len(translations)} 个商品")
        
        for item in translations:
            platform = item.get('platform', '')
            product_id = item.get('id', '')
            short_name = item.get('short_name', '')
            
            if not product_id or not short_name:
                continue
            
            try:
                if platform == 'amazon':
                    amazon_cursor.execute(
                        'UPDATE products SET short_name = ? WHERE asin = ?',
                        (short_name, product_id)
                    )
                    if amazon_cursor.rowcount > 0:
                        amazon_updated += 1
                elif platform == 'tiktok':
                    tiktok_cursor.execute(
                        'UPDATE tiktok_products SET short_name = ? WHERE id = ?',
                        (short_name, int(product_id))
                    )
                    if tiktok_cursor.rowcount > 0:
                        tiktok_updated += 1
            except Exception as e:
                print(f"  更新失败 [{product_id}]: {e}")
    
    amazon_conn.commit()
    tiktok_conn.commit()
    amazon_conn.close()
    tiktok_conn.close()
    
    print(f"\n导入完成:")
    print(f"  Amazon: 更新 {amazon_updated} 个商品")
    print(f"  TikTok: 更新 {tiktok_updated} 个商品")
    print(f"  总计: {amazon_updated + tiktok_updated} 个商品")

if __name__ == "__main__":
    import_translations()
