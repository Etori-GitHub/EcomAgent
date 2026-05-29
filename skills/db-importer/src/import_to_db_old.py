#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EcomAgent Database Importer
扫描 output/scraping 目录，将 JSON 数据导入 SQLite 数据库
支持增量更新：按唯一 ID + 日期判断，每天每个商品只保留一条最新记录
支持图片下载和变更追踪
"""

import json
import os
import re
import sqlite3
import sys
import io
from datetime import datetime
from pathlib import Path
from typing import Optional

# 强制 UTF-8 输出（Windows 兼容）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 导入商品主库模块
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts"))
from create_product_master import get_or_create_product
from extract_product_name import extract_product_name

# 导入图片处理模块
from image_processor import ImageProcessor, ImageChangeTracker


class DatabaseImporter:
    """数据库导入器"""
    
    def __init__(self, base_dir: Optional[str] = None):
        # 如果未指定 base_dir，使用脚本所在目录的父目录
        if base_dir is None:
            script_dir = Path(__file__).resolve().parent
            self.base_dir = script_dir.parent.parent.parent
        else:
            self.base_dir = Path(base_dir)
        
        self.scraping_dir = self.base_dir / "output" / "scraping"
        self.data_dir = self.base_dir / "data"
        
        # 初始化图片处理器
        self.image_processor = ImageProcessor(self.base_dir)
        self.image_tracker = ImageChangeTracker(self.data_dir / "image_changes.db")
    
    def generate_short_name(self, name: str) -> str:
        """从商品名称生成简短描述"""
        if not name:
            return ""
        
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
        words = name.split()
        brand = words[0] if words else ""
        
        found_type = None
        for ptype in product_types:
            if ptype in name_lower:
                found_type = ptype.title()
                break
        
        if found_type:
            brand_short = brand if len(brand) <= 15 else brand[:12] + "..."
            return f"{brand_short} {found_type}"
        
        return name[:30] + "..." if len(name) > 30 else name
        
    def parse_sales_count(self, sold_str: Optional[str]) -> Optional[int]:
        """解析销售数量字符串"""
        if not sold_str:
            return None
        
        match = re.search(r'([\d.]+)\s*K', sold_str)
        if match:
            return int(float(match.group(1)) * 1000)
        
        match = re.search(r'([\d]+)\s*已售出', sold_str)
        if match:
            return int(match.group(1))
        
        return None
    
    def extract_date_from_filename(self, filename: str) -> str:
        """从文件名提取日期"""
        match = re.search(r'(\d{8})', filename)
        if match:
            date_str = match.group(1)
            return f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
        return datetime.now().strftime("%Y-%m-%d")
    
    def process_image(
        self, 
        platform: str, 
        platform_id: str, 
        new_image_url: str,
        date: str
    ) -> Optional[str]:
        """
        处理图片：下载、压缩、保存
        
        逻辑：
        1. 查询数据库中该商品的当前图片 URL
        2. 如果 URL 相同，返回现有路径
        3. 如果 URL 不同，下载新图片，记录变更
        4. 如果是新商品，直接下载保存
        
        Returns:
            本地图片路径（相对路径）
        """
        if not new_image_url:
            return None
        
        # 查询当前图片信息
        conn = None
        current_image_url = None
        current_local_path = None
        
        try:
            if platform == 'amazon':
                db_path = self.data_dir / "amazon.db"
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT image_url, local_image_path FROM products WHERE asin = ?", (platform_id,))
            else:
                db_path = self.data_dir / "tiktok.db"
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT image_url, local_image_path FROM tiktok_products WHERE tiktokshop_id = ?", (platform_id,))
            
            result = cursor.fetchone()
            if result:
                current_image_url = result[0]
                current_local_path = result[1]
        except Exception as e:
            print(f"[WARN] 查询图片信息失败: {e}")
        finally:
            if conn:
                conn.close()
        
        # 判断图片是否变更
        if current_image_url and current_image_url == new_image_url:
            # URL 相同，使用现有图片
            print(f"[INFO] 图片未变更: {platform}_{platform_id}")
            return current_local_path
        
        # 下载新图片
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_local_path = self.image_processor.save_image(
            platform=platform,
            platform_id=platform_id,
            image_url=new_image_url,
            timestamp=timestamp
        )
        
        if not new_local_path:
            print(f"[WARN] 图片下载失败: {platform}_{platform_id}")
            return current_local_path
        
        # 记录变更
        if current_image_url and current_image_url != new_image_url:
            self.image_tracker.record_change(
                platform=platform,
                platform_id=platform_id,
                old_image_url=current_image_url,
                new_image_url=new_image_url,
                old_local_path=current_local_path,
                new_local_path=new_local_path,
                change_date=date
            )
            print(f"[INFO] 图片已变更: {platform}_{platform_id}")
        
        return new_local_path
    
    def import_amazon(self, file_path: Path):
        """导入 Amazon 数据"""
        print(f"\n{'='*60}")
        print(f"Importing Amazon data from: {file_path.name}")
        print(f"{'='*60}")
        
        db_path = self.data_dir / "amazon.db"
        if not db_path.exists():
            print(f"[ERROR] Database not found: {db_path}")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            products = data
        elif isinstance(data, dict):
            products = data.get('products', [])
        else:
            print(f"[ERROR] Unexpected data format: {type(data)}")
            return
        
        date = self.extract_date_from_filename(file_path.name)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        inserted_products = 0
        inserted_sales = 0
        updated_sales = 0
        skipped_duplicates = 0
        images_processed = 0
        
        for product in products:
            asin = product.get('asin')
            if not asin:
                continue
            
            full_title = product.get('name', '')
            product_name = extract_product_name(full_title)
            short_name = self.generate_short_name(product_name)
            product_url = product.get('product_url', f"https://www.amazon.com/dp/{asin}" if asin else '')
            image_url = product.get('image_url', '')
            
            # 处理图片
            local_image_path = None
            if image_url:
                local_image_path = self.process_image('amazon', asin, image_url, date)
                images_processed += 1
            
            # 关联商品主库
            master_id = get_or_create_product(
                platform='amazon',
                platform_id=asin,
                name=product_name,
                short_name=short_name,
                search_keyword=full_title,
                product_url=product_url,
                category=product.get('category')
            )
            
            # 插入或更新商品
            cursor.execute("""
                INSERT INTO products (asin, name, short_name, search_keyword, product_url, category, subcategory, platform, master_id, image_url, local_image_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'amazon', ?, ?, ?)
                ON CONFLICT(asin) DO UPDATE SET
                    short_name = COALESCE(short_name, excluded.short_name),
                    search_keyword = COALESCE(search_keyword, excluded.search_keyword),
                    product_url = COALESCE(product_url, excluded.product_url),
                    master_id = COALESCE(master_id, excluded.master_id),
                    image_url = COALESCE(image_url, excluded.image_url),
                    local_image_path = COALESCE(local_image_path, excluded.local_image_path)
            """, (asin, product_name, short_name, full_title, product_url, product.get('category'), product.get('subcategory'), master_id, image_url, local_image_path))
            
            cursor.execute("SELECT id FROM products WHERE asin = ?", (asin,))
            result = cursor.fetchone()
            
            if result:
                product_id = result[0]
                
                try:
                    price = float(product.get('price')) if product.get('price') else None
                except (TypeError, ValueError):
                    price = None
                
                cursor.execute("""
                    SELECT id FROM daily_sales 
                    WHERE product_id = ? AND date = ?
                """, (product_id, date))
                existing = cursor.fetchone()
                
                if existing:
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
        
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM daily_sales")
        total_sales = cursor.fetchone()[0]
        
        print(f"[OK] Amazon import complete!")
        print(f"   Total products in DB: {total_products}")
        print(f"   Total sales records: {total_sales}")
        print(f"   New sales inserted: {inserted_sales}")
        print(f"   Sales updated: {updated_sales}")
        print(f"   Images processed: {images_processed}")
        print(f"   Skipped (duplicates): {skipped_duplicates}")
        
        conn.close()
    
    def import_tiktok(self, file_path: Path):
        """导入 TikTok 数据"""
        print(f"\n{'='*60}")
        print(f"Importing TikTok data from: {file_path.name}")
        print(f"{'='*60}")
        
        db_path = self.data_dir / "tiktok.db"
        if not db_path.exists():
            print(f"[ERROR] Database not found: {db_path}")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, dict):
            metadata = data.get('metadata', {})
            products = data.get('products', [])
        elif isinstance(data, list):
            metadata = {}
            products = data
        else:
            print(f"[ERROR] Unexpected data format: {type(data)}")
            return
        
        category = metadata.get('category', 'Unknown')
        date = self.extract_date_from_filename(file_path.name)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        inserted_products = 0
        inserted_sales = 0
        updated_sales = 0
        skipped_duplicates = 0
        images_processed = 0
        
        seen_tiktokshop_ids = set()
        seen_names = set()
        
        for product in products:
            tiktokshop_id = product.get('tiktokshop_id')
            name = product.get('name')
            
            if not tiktokshop_id and not name:
                continue
            
            if tiktokshop_id and tiktokshop_id in seen_tiktokshop_ids:
                continue
            if name and name in seen_names:
                continue
            
            if tiktokshop_id:
                seen_tiktokshop_ids.add(tiktokshop_id)
            if name:
                seen_names.add(name)
            
            full_title = product.get('name', '')
            product_name = extract_product_name(full_title)
            short_name = self.generate_short_name(product_name)
            product_url = product.get('product_url', '')
            tiktokshop_id = product.get('tiktokshop_id')
            image_url = product.get('image_url', '')
            
            # 处理图片
            local_image_path = None
            if image_url and tiktokshop_id:
                local_image_path = self.process_image('tiktok', tiktokshop_id, image_url, date)
                images_processed += 1
            
            master_id = None
            if tiktokshop_id:
                master_id = get_or_create_product(
                    platform='tiktok',
                    platform_id=tiktokshop_id,
                    name=product_name,
                    short_name=short_name,
                    search_keyword=full_title,
                    product_url=product_url,
                    category=category
                )
            
            if tiktokshop_id:
                cursor.execute("""
                    INSERT INTO tiktok_products (name, short_name, search_keyword, product_url, category, platform, tiktokshop_id, master_id, rank, image_url, local_image_path)
                    VALUES (?, ?, ?, ?, ?, 'tiktok', ?, ?, ?, ?, ?)
                    ON CONFLICT(tiktokshop_id) DO UPDATE SET
                        short_name = COALESCE(short_name, excluded.short_name),
                        search_keyword = COALESCE(search_keyword, excluded.search_keyword),
                        product_url = COALESCE(product_url, excluded.product_url),
                        master_id = COALESCE(master_id, excluded.master_id),
                        rank = COALESCE(rank, excluded.rank),
                        image_url = COALESCE(image_url, excluded.image_url),
                        local_image_path = COALESCE(local_image_path, excluded.local_image_path)
                """, (product_name, short_name, full_title, product_url, category, tiktokshop_id, master_id, product.get('rank'), image_url, local_image_path))
                
                cursor.execute("SELECT id FROM tiktok_products WHERE tiktokshop_id = ?", (tiktokshop_id,))
            else:
                cursor.execute("""
                    INSERT INTO tiktok_products (name, short_name, search_keyword, product_url, category, platform)
                    VALUES (?, ?, ?, ?, 'tiktok')
                """, (product_name, short_name, full_title, product_url, category))
                
                cursor.execute("SELECT id FROM tiktok_products WHERE name = ?", (product_name,))
            
            result = cursor.fetchone()
            
            if result:
                product_id = result[0]
                
                try:
                    price = float(product.get('price')) if product.get('price') else None
                except (TypeError, ValueError):
                    price = None
                
                try:
                    original_price = float(product.get('original_price')) if product.get('original_price') else None
                except (TypeError, ValueError):
                    original_price = None
                
                sales_count = self.parse_sales_count(product.get('sold'))
                
                cursor.execute("""
                    SELECT id FROM tiktok_daily_sales 
                    WHERE product_id = ? AND date = ?
                """, (product_id, date))
                existing = cursor.fetchone()
                
                if existing:
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
        
        cursor.execute("SELECT COUNT(*) FROM tiktok_products")
        total_products = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tiktok_daily_sales")
        total_sales = cursor.fetchone()[0]
        
        print(f"[OK] TikTok import complete!")
        print(f"   Total products in DB: {total_products}")
        print(f"   Total sales records: {total_sales}")
        print(f"   New sales inserted: {inserted_sales}")
        print(f"   Sales updated: {updated_sales}")
        print(f"   Images processed: {images_processed}")
        print(f"   Skipped (duplicates): {skipped_duplicates}")
        
        conn.close()
    
    def scan_and_import(self):
        """扫描目录并导入所有 JSON 文件"""
        print(f"\n{'#'*60}")
        print(f"# EcomAgent Database Importer")
        print(f"# Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"# Incremental update enabled (by unique ID + date)")
        print(f"# Image processing enabled")
        print(f"{'#'*60}")
        
        if not self.scraping_dir.exists():
            print(f"[ERROR] Scraping directory not found: {self.scraping_dir}")
            return
        
        json_files = list(self.scraping_dir.glob("*.json"))
        print(f"\nFound {len(json_files)} JSON files to process\n")
        
        if not json_files:
            print("[OK] No JSON files found. Nothing to import.")
            return
        
        amazon_files = [f for f in json_files if f.name.startswith("amazon_")]
        tiktok_files = [f for f in json_files if f.name.startswith("tiktok_")]
        
        print(f"Amazon files: {len(amazon_files)}")
        print(f"TikTok files: {len(tiktok_files)}")
        
        for file_path in amazon_files:
            try:
                self.import_amazon(file_path)
            except Exception as e:
                print(f"[ERROR] Error importing {file_path.name}: {e}")
        
        for file_path in tiktok_files:
            try:
                self.import_tiktok(file_path)
            except Exception as e:
                print(f"[ERROR] Error importing {file_path.name}: {e}")
        
        print(f"\n{'#'*60}")
        print(f"# Import complete at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'#'*60}\n")


def main():
    """主函数"""
    importer = DatabaseImporter()
    importer.scan_and_import()


if __name__ == "__main__":
    main()

