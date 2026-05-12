#!/usr/bin/env python3
"""
EcomAgent Database Importer
扫描 output/scraping 目录，将 JSON 数据导入 SQLite 数据库
支持增量更新：按唯一 ID + 日期判断，每天每个商品只保留一条最新记录
"""

import json
import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

# 导入商品主库模块
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts"))
from create_product_master import get_or_create_product
from extract_product_name import extract_product_name


class DatabaseImporter:
    """数据库导入器"""
    
    def __init__(self, base_dir: Optional[str] = None):
        # 如果未指定 base_dir，使用脚本所在目录的父目录
        if base_dir is None:
            # 脚本路径：EcomAgent/skills/db-importer/src/import_to_db.py
            # 向上数 3 层：src -> db-importer -> skills -> EcomAgent
            script_dir = Path(__file__).resolve().parent
            self.base_dir = script_dir.parent.parent.parent
        else:
            self.base_dir = Path(base_dir)
        
        self.scraping_dir = self.base_dir / "output" / "scraping"
        self.data_dir = self.base_dir / "data"
    
    def generate_short_name(self, name: str) -> str:
        """从商品名称生成简短描述
        
        策略：
        1. 提取品牌名（通常是前几个单词）
        2. 提取关键产品类型（如 Body Wash, Toner, Cream 等）
        3. 组合成简短描述
        """
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
            'bag', 'backpack', 'wallet', 'belt', 'watch', 'sunglasses'
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
            # 如果品牌名太长，只取第一个单词
            brand_short = brand if len(brand) <= 15 else brand[:12] + "..."
            return f"{brand_short} {found_type}"
        
        # 如果没找到产品类型，返回前 30 个字符
        return name[:30] + "..." if len(name) > 30 else name
        
    def parse_sales_count(self, sold_str: Optional[str]) -> Optional[int]:
        """解析销售数量字符串，如 '57.8K 已售出' -> 57800"""
        if not sold_str:
            return None
        
        # 匹配数字 + K 格式
        match = re.search(r'([\d.]+)\s*K', sold_str)
        if match:
            return int(float(match.group(1)) * 1000)
        
        # 匹配纯数字
        match = re.search(r'([\d]+)\s*已售出', sold_str)
        if match:
            return int(match.group(1))
        
        return None
    
    def extract_date_from_filename(self, filename: str) -> str:
        """从文件名提取日期，格式：YYYYMMDD -> YYYY-MM-DD"""
        match = re.search(r'(\d{8})', filename)
        if match:
            date_str = match.group(1)
            return f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
        return datetime.now().strftime("%Y-%m-%d")
    
    def import_amazon(self, file_path: Path):
        """导入 Amazon 数据"""
        print(f"\n{'='*60}")
        print(f"Importing Amazon data from: {file_path.name}")
        print(f"{'='*60}")
        
        db_path = self.data_dir / "amazon.db"
        if not db_path.exists():
            print(f"❌ Database not found: {db_path}")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Amazon JSON is a direct array, not {"products": [...]}
        if isinstance(data, list):
            products = data
        elif isinstance(data, dict):
            products = data.get('products', [])
        else:
            print(f"❌ Unexpected data format: {type(data)}")
            return
        
        date = self.extract_date_from_filename(file_path.name)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        inserted_products = 0
        inserted_sales = 0
        updated_sales = 0
        skipped_duplicates = 0
        
        for product in products:
            asin = product.get('asin')
            if not asin:
                continue
            
            # Insert or get product
            full_title = product.get('name', '')
            product_name = extract_product_name(full_title)  # 提取真正的商品名
            short_name = self.generate_short_name(product_name)  # 基于商品名生成简短描述
            product_url = product.get('product_url', f"https://www.amazon.com/dp/{asin}" if asin else '')
            
            # 关联商品主库
            master_id = get_or_create_product(
                platform='amazon',
                platform_id=asin,
                name=product_name,  # 使用提取的商品名
                short_name=short_name,
                search_keyword=full_title,  # 完整标题作为搜索关键词
                product_url=product_url,
                category=product.get('category')
            )
            
            cursor.execute("""
                INSERT OR IGNORE INTO products (asin, name, short_name, search_keyword, product_url, category, subcategory, platform, master_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'amazon', ?)
            """, (asin, product_name, short_name, full_title, product_url, product.get('category'), product.get('subcategory'), master_id))
            
            # 如果记录已存在，更新字段
            cursor.execute("""
                UPDATE products SET 
                    short_name = COALESCE(short_name, ?),
                    search_keyword = COALESCE(search_keyword, ?),
                    product_url = COALESCE(product_url, ?),
                    master_id = COALESCE(master_id, ?)
                WHERE asin = ? AND (short_name IS NULL OR search_keyword IS NULL OR product_url IS NULL OR master_id IS NULL)
            """, (short_name, full_title, product_url, master_id, asin))
            
            cursor.execute("SELECT id FROM products WHERE asin = ?", (asin,))
            result = cursor.fetchone()
            
            if result:
                product_id = result[0]
                
                # Insert sales data (incremental update)
                try:
                    price = float(product.get('price')) if product.get('price') else None
                except (TypeError, ValueError):
                    price = None
                
                # Check if record for this date already exists
                cursor.execute("""
                    SELECT id FROM daily_sales 
                    WHERE product_id = ? AND date = ?
                """, (product_id, date))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing record
                    cursor.execute("""
                        UPDATE daily_sales SET
                            timestamp = datetime('now'),
                            price = ?,
                            rank = ?,
                            rating = ?,
                            rating_count = ?,
                            category = ?,
                            subcategory = ?
                        WHERE id = ?
                    """, (
                        price,
                        product.get('rank'),
                        product.get('rating'),
                        product.get('rating_count'),
                        product.get('category'),
                        product.get('subcategory'),
                        existing[0]
                    ))
                    updated_sales += 1
                else:
                    # Insert new record
                    cursor.execute("""
                        INSERT INTO daily_sales 
                        (product_id, date, timestamp, price, rank, rating, rating_count, category, subcategory)
                        VALUES (?, ?, datetime('now'), ?, ?, ?, ?, ?, ?)
                    """, (
                        product_id, date, price,
                        product.get('rank'),
                        product.get('rating'),
                        product.get('rating_count'),
                        product.get('category'),
                        product.get('subcategory')
                    ))
                    inserted_sales += 1
            else:
                skipped_duplicates += 1
        
        conn.commit()
        
        # Get counts
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM daily_sales")
        total_sales = cursor.fetchone()[0]
        
        print(f"✅ Amazon import complete!")
        print(f"   Total products in DB: {total_products}")
        print(f"   Total sales records: {total_sales}")
        print(f"   New sales inserted: {inserted_sales}")
        print(f"   Sales updated: {updated_sales}")
        print(f"   Skipped (duplicates): {skipped_duplicates}")
        
        conn.close()
    
    def import_tiktok(self, file_path: Path):
        """导入 TikTok 数据"""
        print(f"\n{'='*60}")
        print(f"Importing TikTok data from: {file_path.name}")
        print(f"{'='*60}")
        
        db_path = self.data_dir / "tiktok.db"
        if not db_path.exists():
            print(f"❌ Database not found: {db_path}")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # TikTok JSON has metadata and products
        if isinstance(data, dict):
            metadata = data.get('metadata', {})
            products = data.get('products', [])
        elif isinstance(data, list):
            # Fallback: treat as products array
            metadata = {}
            products = data
        else:
            print(f"❌ Unexpected data format: {type(data)}")
            return
        
        category = metadata.get('category', 'Unknown')
        date = self.extract_date_from_filename(file_path.name)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        inserted_products = 0
        inserted_sales = 0
        updated_sales = 0
        skipped_duplicates = 0
        
        # Use tiktokshop_id as unique identifier (if available), fallback to name
        seen_tiktokshop_ids = set()
        seen_names = set()
        
        for product in products:
            tiktokshop_id = product.get('tiktokshop_id')
            name = product.get('name')
            
            if not tiktokshop_id and not name:
                continue
            
            # Deduplicate by tiktokshop_id first (preferred), then by name
            if tiktokshop_id and tiktokshop_id in seen_tiktokshop_ids:
                continue
            if name and name in seen_names:
                continue
            
            if tiktokshop_id:
                seen_tiktokshop_ids.add(tiktokshop_id)
            if name:
                seen_names.add(name)
            
            # Insert or get product
            full_title = product.get('name', '')
            product_name = extract_product_name(full_title)  # 提取真正的商品名
            short_name = self.generate_short_name(product_name)  # 基于商品名生成简短描述
            product_url = product.get('product_url', '')
            tiktokshop_id = product.get('tiktokshop_id')
            
            # 关联商品主库
            master_id = None
            if tiktokshop_id:
                master_id = get_or_create_product(
                    platform='tiktok',
                    platform_id=tiktokshop_id,
                    name=product_name,  # 使用提取的商品名
                    short_name=short_name,
                    search_keyword=full_title,  # 完整标题作为搜索关键词
                    product_url=product_url,
                    category=category
                )
            
            if tiktokshop_id:
                cursor.execute("""
                    INSERT OR IGNORE INTO tiktok_products (name, short_name, search_keyword, product_url, category, platform, tiktokshop_id, master_id, rank)
                    VALUES (?, ?, ?, ?, ?, 'tiktok', ?, ?, ?)
                """, (product_name, short_name, full_title, product_url, category, tiktokshop_id, master_id, product.get('rank')))
                
                # 更新字段
                cursor.execute("""
                    UPDATE tiktok_products SET 
                        short_name = COALESCE(short_name, ?),
                        search_keyword = COALESCE(search_keyword, ?),
                        product_url = COALESCE(product_url, ?),
                        master_id = COALESCE(master_id, ?),
                        rank = COALESCE(rank, ?)
                    WHERE tiktokshop_id = ? AND (short_name IS NULL OR search_keyword IS NULL OR product_url IS NULL OR master_id IS NULL OR rank IS NULL)
                """, (short_name, full_title, product_url, master_id, product.get('rank'), tiktokshop_id))
                
                cursor.execute("SELECT id FROM tiktok_products WHERE tiktokshop_id = ?", (tiktokshop_id,))
            else:
                cursor.execute("""
                    INSERT OR IGNORE INTO tiktok_products (name, short_name, search_keyword, product_url, category, platform)
                    VALUES (?, ?, ?, ?, 'tiktok')
                """, (product_name, short_name, full_title, product_url, category))
                
                cursor.execute("SELECT id FROM tiktok_products WHERE name = ?", (product_name,))
            
            result = cursor.fetchone()
            
            if result:
                product_id = result[0]
                
                # Insert sales data (incremental update)
                try:
                    price = float(product.get('price')) if product.get('price') else None
                except (TypeError, ValueError):
                    price = None
                
                try:
                    original_price = float(product.get('original_price')) if product.get('original_price') else None
                except (TypeError, ValueError):
                    original_price = None
                
                sales_count = self.parse_sales_count(product.get('sold'))
                
                # Check if record for this date already exists
                cursor.execute("""
                    SELECT id FROM tiktok_daily_sales 
                    WHERE product_id = ? AND date = ?
                """, (product_id, date))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing record
                    cursor.execute("""
                        UPDATE tiktok_daily_sales SET
                            timestamp = datetime('now'),
                            price = ?,
                            original_price = ?,
                            rating = ?,
                            sales_count = ?,
                            category = ?
                        WHERE id = ?
                    """, (
                        price, original_price,
                        product.get('rating'),
                        sales_count,
                        category,
                        existing[0]
                    ))
                    updated_sales += 1
                else:
                    # Insert new record
                    cursor.execute("""
                        INSERT INTO tiktok_daily_sales 
                        (product_id, date, timestamp, price, original_price, rating, sales_count, category)
                        VALUES (?, ?, datetime('now'), ?, ?, ?, ?, ?)
                    """, (
                        product_id, date, price, original_price,
                        product.get('rating'),
                        sales_count,
                        category
                    ))
                    inserted_sales += 1
            else:
                skipped_duplicates += 1
        
        conn.commit()
        
        # Get counts
        cursor.execute("SELECT COUNT(*) FROM tiktok_products")
        total_products = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tiktok_daily_sales")
        total_sales = cursor.fetchone()[0]
        
        print(f"✅ TikTok import complete!")
        print(f"   Total products in DB: {total_products}")
        print(f"   Total sales records: {total_sales}")
        print(f"   New sales inserted: {inserted_sales}")
        print(f"   Sales updated: {updated_sales}")
        print(f"   Skipped (duplicates): {skipped_duplicates}")
        
        conn.close()
    
    def scan_and_import(self):
        """扫描目录并导入所有 JSON 文件"""
        print(f"\n{'#'*60}")
        print(f"# EcomAgent Database Importer")
        print(f"# Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"# Incremental update enabled (by unique ID + date)")
        print(f"{'#'*60}")
        
        if not self.scraping_dir.exists():
            print(f"❌ Scraping directory not found: {self.scraping_dir}")
            return
        
        json_files = list(self.scraping_dir.glob("*.json"))
        print(f"\nFound {len(json_files)} JSON files to process\n")
        
        if not json_files:
            print("✅ No JSON files found. Nothing to import.")
            return
        
        amazon_files = [f for f in json_files if f.name.startswith("amazon_")]
        tiktok_files = [f for f in json_files if f.name.startswith("tiktok_")]
        
        print(f"Amazon files: {len(amazon_files)}")
        print(f"TikTok files: {len(tiktok_files)}")
        
        # Import Amazon files
        for file_path in amazon_files:
            try:
                self.import_amazon(file_path)
            except Exception as e:
                print(f"❌ Error importing {file_path.name}: {e}")
        
        # Import TikTok files
        for file_path in tiktok_files:
            try:
                self.import_tiktok(file_path)
            except Exception as e:
                print(f"❌ Error importing {file_path.name}: {e}")
        
        print(f"\n{'#'*60}")
        print(f"# Import complete at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'#'*60}\n")


def main():
    """主函数"""
    # 使用默认路径（脚本所在目录的父目录）
    importer = DatabaseImporter()
    importer.scan_and_import()


if __name__ == "__main__":
    main()
