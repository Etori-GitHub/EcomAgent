#!/usr/bin/env python3
"""更新 TikTok 商品的分类"""
import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
IMPORTED_DIR = BASE_DIR / "output" / "imported"

# 连接数据库
tiktok_db = sqlite3.connect(DATA_DIR / "tiktok.db")
master_db = sqlite3.connect(DATA_DIR / "product_master.db")

# 遍历所有 TikTok JSON 文件
updated = 0
for json_file in IMPORTED_DIR.glob("tiktok_*.json"):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    category = data.get('metadata', {}).get('category')
    if not category:
        continue
    
    products = data.get('products', [])
    for p in products:
        tid = p.get('tiktokshop_id')
        if not tid:
            continue
        
        # 更新 tiktok_products 表
        tiktok_db.execute("UPDATE tiktok_products SET category = ? WHERE tiktokshop_id = ?", (category, tid))
        
        # 更新 product_master 表
        tiktok_db.execute("SELECT master_id FROM tiktok_products WHERE tiktokshop_id = ?", (tid,))
        row = tiktok_db.execute("SELECT master_id FROM tiktok_products WHERE tiktokshop_id = ?", (tid,)).fetchone()
        if row and row[0]:
            master_db.execute("UPDATE product_master SET category = ? WHERE id = ?", (category, row[0]))
        
        updated += 1

tiktok_db.commit()
master_db.commit()
tiktok_db.close()
master_db.close()

print(f"[OK] 更新了 {updated} 个商品的分类")
