#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EcomAgent 数据导入器 v2.0
"""

import json
import re
import sqlite3
import sys
import io
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

# Windows UTF-8 兼容
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 导入模块
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts"))
from create_product_master import get_or_create_product
from extract_product_name import extract_product_name


class DataImporter:
    """数据导入器"""
    
    def __init__(self, base_dir: Path = None):
        if base_dir is None:
            base_dir = Path(__file__).parent.parent.parent.parent
        
        self.base_dir = base_dir
        self.scraping_dir = base_dir / "output" / "scraping"
        self.data_dir = base_dir / "data"
    
    def extract_date(self, filename: str) -> str:
        """从文件名提取日期"""
        match = re.search(r'(\d{8})', filename)
        if match:
            d = match.group(1)
            return f"{d[0:4]}-{d[4:6]}-{d[6:8]}"
        return datetime.now().strftime("%Y-%m-%d")
    
    def record_event(self, cursor, product_id: int, event_type: str, old_value: str = None, new_value: str = None):
        """记录事件"""
        cursor.execute("""
            INSERT INTO events (product_id, event_type, old_value, new_value, created_at)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (product_id, event_type, old_value, new_value))
        print(f"[EVENT] {event_type}: product_id={product_id}")
    
    def import_amazon(self, file_path: Path):
        """导入 Amazon 数据"""
        print(f"\n{'='*60}")
        print(f"Importing Amazon: {file_path.name}")
        print(f"{'='*60}")
        
        db_path = self.data_dir / "amazon.db"
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        products = data.get('products', []) if isinstance(data, dict) else data
        date = self.extract_date(file_path.name)
        
        conn = sqlite3.connect(db_path, timeout=30)
        cursor = conn.cursor()
        
        stats = {'new': 0, 'upd': 0, 'sales_new': 0, 'sales_upd': 0, 'events': 0}
        
        for p in products:
            asin = p.get('asin')
            if not asin:
                continue
            
            name = extract_product_name(p.get('name', ''))
            image_url = p.get('image_url', '')
            product_url = p.get('product_url', f"https://www.amazon.com/dp/{asin}")
            
            cursor.execute("SELECT id, name, image_url FROM products WHERE asin = ?", (asin,))
            existing = cursor.fetchone()
            
            if existing:
                product_id, old_name, old_image = existing
                
                if old_name and old_name != name:
                    self.record_event(cursor, product_id, 'name_changed', old_name, name)
                    stats['events'] += 1
                
                if old_image and old_image != image_url:
                    self.record_event(cursor, product_id, 'cover_image_changed', old_image, image_url)
                    stats['events'] += 1
                
                cursor.execute("UPDATE products SET name=?, image_url=?, updated_at=datetime('now') WHERE asin=?", (name, image_url, asin))
                stats['upd'] += 1
            else:
                master_id = get_or_create_product('amazon', asin, name, product_url=product_url, category=p.get('category'))
                cursor.execute("INSERT INTO products (asin, name, image_url, master_id) VALUES (?, ?, ?, ?)", (asin, name, image_url, master_id))
                product_id = cursor.lastrowid
                stats['new'] += 1
            
            # 销售数据
            cursor.execute("SELECT id FROM daily_sales WHERE product_id=? AND date=?", (product_id, date))
            if cursor.fetchone():
                cursor.execute("UPDATE daily_sales SET price=?, rating=?, rating_count=?, rank=? WHERE product_id=? AND date=?", 
                    (p.get('price'), p.get('rating'), p.get('rating_count'), p.get('rank'), product_id, date))
                stats['sales_upd'] += 1
            else:
                cursor.execute("INSERT INTO daily_sales (product_id, date, price, rating, rating_count, rank, category) VALUES (?,?,?,?,?,?,?)",
                    (product_id, date, p.get('price'), p.get('rating'), p.get('rating_count'), p.get('rank'), p.get('category')))
                stats['sales_new'] += 1
        
        conn.commit()
        conn.close()
        print(f"[OK] Amazon: {stats['new']} new, {stats['upd']} upd, {stats['sales_new']}+{stats['sales_upd']} sales, {stats['events']} events")
    
    def import_tiktok(self, file_path: Path):
        """导入 TikTok 数据"""
        print(f"\n{'='*60}")
        print(f"Importing TikTok: {file_path.name}")
        print(f"{'='*60}")
        
        db_path = self.data_dir / "tiktok.db"
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        products = data.get('products', []) if isinstance(data, dict) else data
        date = self.extract_date(file_path.name)
        
        conn = sqlite3.connect(db_path, timeout=30)
        cursor = conn.cursor()
        
        stats = {'new': 0, 'upd': 0, 'sales_new': 0, 'sales_upd': 0, 'events': 0}
        
        for p in products:
            tid = p.get('tiktokshop_id')
            if not tid:
                continue
            
            name = extract_product_name(p.get('name', ''))
            image_url = p.get('image_url', '')
            product_url = p.get('product_url', '')
            sold = p.get('sold', '')
            
            # 解析销量
            sales_count = None
            if sold:
                km = re.search(r'([\d.]+)\s*K', sold)
                if km:
                    sales_count = int(float(km.group(1)) * 1000)
                else:
                    nm = re.search(r'(\d+)', sold)
                    if nm:
                        sales_count = int(nm.group(1))
            
            cursor.execute("SELECT id, name, image_url FROM tiktok_products WHERE tiktokshop_id = ?", (tid,))
            existing = cursor.fetchone()
            
            if existing:
                product_id, old_name, old_image = existing
                
                if old_name and old_name != name:
                    self.record_event(cursor, product_id, 'name_changed', old_name, name)
                    stats['events'] += 1
                
                if old_image and old_image != image_url:
                    self.record_event(cursor, product_id, 'cover_image_changed', old_image, image_url)
                    stats['events'] += 1
                
                cursor.execute("UPDATE tiktok_products SET name=?, image_url=?, updated_at=datetime('now') WHERE tiktokshop_id=?", (name, image_url, tid))
                stats['upd'] += 1
            else:
                master_id = get_or_create_product('tiktok', tid, name, product_url=product_url)
                cursor.execute("INSERT INTO tiktok_products (tiktokshop_id, name, image_url, master_id) VALUES (?, ?, ?, ?)", (tid, name, image_url, master_id))
                product_id = cursor.lastrowid
                stats['new'] += 1
            
            # 销售数据
            cursor.execute("SELECT id FROM tiktok_daily_sales WHERE product_id=? AND date=?", (product_id, date))
            if cursor.fetchone():
                cursor.execute("UPDATE tiktok_daily_sales SET price=?, rating=?, sales_count=? WHERE product_id=? AND date=?", 
                    (p.get('price'), p.get('rating'), sales_count, product_id, date))
                stats['sales_upd'] += 1
            else:
                cursor.execute("INSERT INTO tiktok_daily_sales (product_id, date, price, rating, sales_count) VALUES (?,?,?,?,?)",
                    (product_id, date, p.get('price'), p.get('rating'), sales_count))
                stats['sales_new'] += 1
        
        conn.commit()
        conn.close()
        print(f"[OK] TikTok: {stats['new']} new, {stats['upd']} upd, {stats['sales_new']}+{stats['sales_upd']} sales, {stats['events']} events")
    
    def scan_and_import(self):
        """扫描并导入"""
        print(f"\n{'#'*60}")
        print(f"# EcomAgent Data Importer v2.0")
        print(f"# {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'#'*60}")
        
        if not self.scraping_dir.exists():
            print(f"[ERROR] Dir not found: {self.scraping_dir}")
            return
        
        files = list(self.scraping_dir.glob("*.json"))
        amazon = sorted([f for f in files if f.name.startswith("amazon_")])
        tiktok = sorted([f for f in files if f.name.startswith("tiktok_")])
        
        print(f"Amazon: {len(amazon)}, TikTok: {len(tiktok)}")
        
        for f in amazon:
            try:
                self.import_amazon(f)
            except Exception as e:
                print(f"[ERROR] {f.name}: {e}")
        
        for f in tiktok:
            try:
                self.import_tiktok(f)
            except Exception as e:
                print(f"[ERROR] {f.name}: {e}")
        
        print(f"\n{'#'*60}")
        print(f"# Done: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'#'*60}")


if __name__ == "__main__":
    DataImporter().scan_and_import()
