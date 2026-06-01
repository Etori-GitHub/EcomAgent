#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清除今天抓取的 Amazon 数据
"""

import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

today = datetime.now().strftime("%Y-%m-%d")
print(f"清除 {today} 的 Amazon 数据...\n")

# 1. Amazon 数据库
amazon_db = DATA_DIR / "amazon.db"
if amazon_db.exists():
    conn = sqlite3.connect(amazon_db)
    cursor = conn.cursor()
    
    # 删除今天的 daily_sales
    cursor.execute("DELETE FROM daily_sales WHERE date = ?", (today,))
    sales_deleted = cursor.rowcount
    print(f"[amazon] 删除 daily_sales: {sales_deleted} 条")
    
    conn.commit()
    conn.close()

# 2. 商品总库 - 删除今天的 Amazon 商品
master_db = DATA_DIR / "product_master.db"
if master_db.exists():
    conn = sqlite3.connect(master_db)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM product_master WHERE platform = 'amazon' AND date(first_seen_at) = ?", (today,))
    master_deleted = cursor.rowcount
    print(f"[product_master] 删除 Amazon 商品: {master_deleted} 条")
    
    conn.commit()
    conn.close()

# 3. 清理抓取文件
scraping_dir = BASE_DIR / "output" / "scraping"
if scraping_dir.exists():
    import os
    for f in scraping_dir.glob("amazon_*.json"):
        f.unlink()
        print(f"[删除文件] {f.name}")

print("\n清除完成！")