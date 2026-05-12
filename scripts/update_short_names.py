#!/usr/bin/env python3
"""
更新数据库中的 short_name 字段
"""

import sqlite3
from pathlib import Path


def generate_short_name(name: str) -> str:
    """从商品名称生成简短描述"""
    if not name:
        return ""
    
    # 常见产品类型关键词
    product_types = [
        'body wash', 'face wash', 'cleanser', 'toner', 'serum', 'cream', 'lotion',
        'moisturizer', 'shampoo', 'conditioner', 'oil', 'mask', 'scrub', 'gel',
        'spray', 'powder', 'soap', 'balm', 'treatment', 'essence', 'sunscreen',
        'lip balm', 'eye cream', 'night cream', 'day cream', 'hand cream',
        'vitamin', 'supplement', 'capsule', 'tablet', 'gummies',
        'headphones', 'earbuds', 'speaker', 'charger', 'cable', 'adapter',
        'phone case', 'screen protector', 'stand', 'holder', 'mount',
        'knife', 'knife set', 'pan', 'pot', 'utensil', 'cutting board',
        'blender', 'mixer', 'toaster', 'air fryer', 'coffee maker',
        'dress', 'shirt', 'pants', 'shoes', 'socks', 'jacket', 'coat',
        'bag', 'backpack', 'wallet', 'belt', 'watch', 'sunglasses',
        'pad', 'patch', 'mask', 'swabs', 'cotton'
    ]
    
    name_lower = name.lower()
    
    # 1. 尝试提取品牌名（前 1-3 个单词）
    words = name.split()
    brand = words[0] if words else ""
    
    # 2. 查找产品类型
    found_type = None
    for ptype in product_types:
        if ptype in name_lower:
            found_type = ptype.title()
            break
    
    # 3. 组合结果
    if found_type:
        brand_short = brand if len(brand) <= 15 else brand[:12] + "..."
        return f"{brand_short} {found_type}"
    
    # 如果没找到产品类型，返回前 30 个字符
    return name[:30] + "..." if len(name) > 30 else name


def update_amazon_short_names():
    """更新 Amazon 数据库的 short_name"""
    db_path = Path("C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/amazon.db")
    
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 获取所有产品
    cursor.execute("SELECT id, name FROM products WHERE short_name IS NULL OR short_name = ''")
    rows = cursor.fetchall()
    
    print(f"📊 Found {len(rows)} products to update")
    
    updated = 0
    for product_id, name in rows:
        short_name = generate_short_name(name)
        cursor.execute("UPDATE products SET short_name = ? WHERE id = ?", (short_name, product_id))
        updated += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ Updated {updated} Amazon products")


def update_tiktok_short_names():
    """更新 TikTok 数据库的 short_name"""
    db_path = Path("C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/tiktok.db")
    
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 获取所有产品
    cursor.execute("SELECT id, name FROM tiktok_products WHERE short_name IS NULL OR short_name = ''")
    rows = cursor.fetchall()
    
    print(f"📊 Found {len(rows)} products to update")
    
    updated = 0
    for product_id, name in rows:
        short_name = generate_short_name(name)
        cursor.execute("UPDATE tiktok_products SET short_name = ? WHERE id = ?", (short_name, product_id))
        updated += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ Updated {updated} TikTok products")


if __name__ == "__main__":
    print("=" * 60)
    print("Updating short_name fields")
    print("=" * 60)
    
    update_amazon_short_names()
    print()
    update_tiktok_short_names()
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
