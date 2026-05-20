#!/usr/bin/env python3
"""
生成测试销售数据
为商品库中的商品生成近7天的销售趋势数据
"""

import sqlite3
import random
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def generate_sales_trend(base_sales: int, days: int = 7) -> list:
    """生成销售趋势数据，模拟真实波动"""
    trend = []
    current_sales = base_sales
    
    for i in range(days):
        # 随机波动 -20% 到 +20%
        change = random.uniform(-0.2, 0.2)
        current_sales = max(1, int(current_sales * (1 + change)))
        trend.append(current_sales)
    
    return trend


def main():
    print("=== 生成测试销售数据 ===")
    
    # 连接商品主库
    master_db = DATA_DIR / "product_master.db"
    if not master_db.exists():
        print("❌ 商品主库不存在")
        return
    
    master_conn = sqlite3.connect(master_db)
    master_cursor = master_conn.cursor()
    
    # 获取所有商品
    master_cursor.execute("SELECT id, ecom_code, platform, platform_id FROM product_master")
    products = master_cursor.fetchall()
    print(f"找到 {len(products)} 个商品")
    
    # 生成近7天的日期
    today = datetime.now().date()
    dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
    
    # Amazon 数据库
    amazon_db = DATA_DIR / "amazon.db"
    amazon_conn = None
    amazon_cursor = None
    if amazon_db.exists():
        amazon_conn = sqlite3.connect(amazon_db)
        amazon_cursor = amazon_conn.cursor()
        # 检查 sales_count 列是否存在
        amazon_cursor.execute("PRAGMA table_info(daily_sales)")
        columns = [row[1] for row in amazon_cursor.fetchall()]
        if 'sales_count' not in columns:
            print("添加 sales_count 列到 Amazon daily_sales 表...")
            amazon_cursor.execute("ALTER TABLE daily_sales ADD COLUMN sales_count INTEGER")
            amazon_conn.commit()
    
    # TikTok 数据库
    tiktok_db = DATA_DIR / "tiktok.db"
    tiktok_conn = None
    tiktok_cursor = None
    if tiktok_db.exists():
        tiktok_conn = sqlite3.connect(tiktok_db)
        tiktok_cursor = tiktok_conn.cursor()
    
    amazon_updated = 0
    tiktok_updated = 0
    
    for product in products:
        master_id, ecom_code, platform, platform_id = product
        
        # 生成基础销量（随机 100-10000）
        base_sales = random.randint(100, 10000)
        trend = generate_sales_trend(base_sales, 7)
        
        if platform == 'amazon' and amazon_cursor:
            # 查找 Amazon 产品
            amazon_cursor.execute("SELECT id FROM products WHERE master_id = ?", (master_id,))
            result = amazon_cursor.fetchone()
            if result:
                product_id = result[0]
                for i, date in enumerate(dates):
                    # 检查是否已有该日期的记录
                    amazon_cursor.execute(
                        "SELECT id FROM daily_sales WHERE product_id = ? AND date = ?",
                        (product_id, date)
                    )
                    existing = amazon_cursor.fetchone()
                    
                    if existing:
                        # 更新销量
                        amazon_cursor.execute(
                            "UPDATE daily_sales SET sales_count = ? WHERE id = ?",
                            (trend[i], existing[0])
                        )
                    else:
                        # 插入新记录
                        amazon_cursor.execute("""
                            INSERT INTO daily_sales (product_id, date, timestamp, sales_count)
                            VALUES (?, ?, datetime('now'), ?)
                        """, (product_id, date, trend[i]))
                amazon_updated += 1
        
        elif platform == 'tiktok' and tiktok_cursor:
            # 查找 TikTok 产品
            tiktok_cursor.execute("SELECT id FROM tiktok_products WHERE master_id = ?", (master_id,))
            result = tiktok_cursor.fetchone()
            if result:
                product_id = result[0]
                for i, date in enumerate(dates):
                    # 检查是否已有该日期的记录
                    tiktok_cursor.execute(
                        "SELECT id FROM tiktok_daily_sales WHERE product_id = ? AND date = ?",
                        (product_id, date)
                    )
                    existing = tiktok_cursor.fetchone()
                    
                    if existing:
                        # 更新销量
                        tiktok_cursor.execute(
                            "UPDATE tiktok_daily_sales SET sales_count = ? WHERE id = ?",
                            (trend[i], existing[0])
                        )
                    else:
                        # 插入新记录
                        tiktok_cursor.execute("""
                            INSERT INTO tiktok_daily_sales (product_id, date, timestamp, sales_count)
                            VALUES (?, ?, datetime('now'), ?)
                        """, (product_id, date, trend[i]))
                tiktok_updated += 1
    
    # 提交更改
    if amazon_conn:
        amazon_conn.commit()
        amazon_conn.close()
    if tiktok_conn:
        tiktok_conn.commit()
        tiktok_conn.close()
    
    master_conn.close()
    
    print(f"✅ 完成！Amazon 更新 {amazon_updated} 个商品，TikTok 更新 {tiktok_updated} 个商品")


if __name__ == "__main__":
    main()
