#!/usr/bin/env python3
"""
创建商品主库（Product Master）- 性能优化版
使用 INTEGER 主键 + TEXT 编码
"""

import sqlite3
from pathlib import Path
from datetime import datetime


# 平台代码映射
PLATFORM_CODES = {
    'amazon': 'AM',
    'tiktok': 'TK',
    'jd': 'JD',
    'taobao': 'TB',
}


def create_product_master_db():
    """创建商品主库"""
    db_path = Path("C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/product_master.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建商品主表 - INTEGER 主键优化
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_master (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ecom_code TEXT UNIQUE NOT NULL,
            platform TEXT NOT NULL,
            platform_id TEXT NOT NULL,
            product_url TEXT,
            name TEXT,
            short_name TEXT,
            search_keyword TEXT,
            category TEXT,
            first_seen_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(platform, platform_id)
        )
    """)
    
    # 创建索引
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_platform ON product_master(platform)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_platform_id ON product_master(platform_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ecom_code ON product_master(ecom_code)")
    
    conn.commit()
    conn.close()
    
    print(f"✅ Created product_master database: {db_path}")


def generate_ecom_code(platform: str, sequence: int) -> str:
    """生成统一商品编码
    
    格式: EC{平台代码}{年份}{6位序号}
    示例: ECAM26000001
    """
    platform_code = PLATFORM_CODES.get(platform.lower(), 'XX')
    year_code = str(datetime.now().year)[2:]
    seq_str = str(sequence).zfill(6)
    
    return f"EC{platform_code}{year_code}{seq_str}"


def get_or_create_product(platform: str, platform_id: str, name: str, 
                          short_name: str = None, search_keyword: str = None,
                          product_url: str = None, category: str = None) -> int:
    """
    获取或创建商品记录
    返回 id (INTEGER)
    """
    db_path = Path("C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/product_master.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查找是否已存在
    cursor.execute("""
        SELECT id FROM product_master 
        WHERE platform = ? AND platform_id = ?
    """, (platform, platform_id))
    
    result = cursor.fetchone()
    
    if result:
        # 已存在，更新信息
        product_id = result[0]
        cursor.execute("""
            UPDATE product_master SET
                name = COALESCE(?, name),
                short_name = COALESCE(?, short_name),
                search_keyword = COALESCE(?, search_keyword),
                product_url = COALESCE(?, product_url),
                category = COALESCE(?, category),
                last_updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (name, short_name, search_keyword, product_url, category, product_id))
        conn.commit()
        conn.close()
        return product_id
    
    # 不存在，创建新记录
    # 获取当前平台的下一个序号
    cursor.execute("""
        SELECT ecom_code FROM product_master 
        WHERE platform = ? 
        ORDER BY id DESC LIMIT 1
    """, (platform,))
    
    last_ecom_code = cursor.fetchone()
    
    if last_ecom_code:
        # 从最后一个 ecom_code 提取序号: ECAM26000001
        last_id = last_ecom_code[0]
        last_seq = int(last_id[6:])  # 取第7位开始的6位数字
        next_seq = last_seq + 1
    else:
        next_seq = 1
    
    ecom_code = generate_ecom_code(platform, next_seq)
    
    cursor.execute("""
        INSERT INTO product_master 
        (ecom_code, platform, platform_id, product_url, name, short_name, search_keyword, category)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ecom_code, platform, platform_id, product_url, name, short_name, search_keyword, category))
    
    product_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return product_id


def migrate_existing_products():
    """迁移现有商品数据到商品主库"""
    
    # 迁移 Amazon 商品
    amazon_db = Path("C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/amazon.db")
    if amazon_db.exists():
        conn_amazon = sqlite3.connect(amazon_db)
        cursor_amazon = conn_amazon.cursor()
        
        cursor_amazon.execute("""
            SELECT asin, name, short_name, search_keyword, product_url, category
            FROM products
        """)
        
        amazon_products = cursor_amazon.fetchall()
        conn_amazon.close()
        
        print(f"📦 Migrating {len(amazon_products)} Amazon products...")
        
        for asin, name, short_name, search_keyword, product_url, category in amazon_products:
            get_or_create_product(
                platform='amazon',
                platform_id=asin,
                name=name,
                short_name=short_name,
                search_keyword=search_keyword,
                product_url=product_url,
                category=category
            )
        
        print(f"✅ Amazon products migrated")
    
    # 迁移 TikTok 商品
    tiktok_db = Path("C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/data/tiktok.db")
    if tiktok_db.exists():
        conn_tiktok = sqlite3.connect(tiktok_db)
        cursor_tiktok = conn_tiktok.cursor()
        
        cursor_tiktok.execute("""
            SELECT tiktokshop_id, name, short_name, search_keyword, product_url, category
            FROM tiktok_products
            WHERE tiktokshop_id IS NOT NULL AND tiktokshop_id != ''
        """)
        
        tiktok_products = cursor_tiktok.fetchall()
        conn_tiktok.close()
        
        print(f"📦 Migrating {len(tiktok_products)} TikTok products...")
        
        for tiktokshop_id, name, short_name, search_keyword, product_url, category in tiktok_products:
            get_or_create_product(
                platform='tiktok',
                platform_id=tiktokshop_id,
                name=name,
                short_name=short_name,
                search_keyword=search_keyword,
                product_url=product_url,
                category=category
            )
        
        print(f"✅ TikTok products migrated")


if __name__ == "__main__":
    print("=" * 60)
    print("Product Master Database Setup (Performance Optimized)")
    print("=" * 60)
    
    # 创建数据库
    create_product_master_db()
    
    # 迁移现有数据
    print("\n" + "=" * 60)
    print("Migrating existing products...")
    print("=" * 60)
    migrate_existing_products()
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
