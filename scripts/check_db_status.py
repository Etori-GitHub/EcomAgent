#!/usr/bin/env python3
"""检查数据库状态"""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

print("=" * 50)
print("EcomAgent 数据库状态检查")
print("=" * 50)

# Product Master
conn = sqlite3.connect(DATA_DIR / "product_master.db")
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM product_master")
total = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM product_master WHERE short_name IS NOT NULL AND short_name != ''")
translated = c.fetchone()[0]
print(f"\n商品主库: {total} 个商品")
print(f"  已翻译: {translated} 个")
print(f"  待翻译: {total - translated} 个")
conn.close()

# Amazon
conn = sqlite3.connect(DATA_DIR / "amazon.db")
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM products")
amazon_products = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM daily_sales")
amazon_sales = c.fetchone()[0]
print(f"\nAmazon: {amazon_products} 个商品, {amazon_sales} 条销售记录")
conn.close()

# TikTok
conn = sqlite3.connect(DATA_DIR / "tiktok.db")
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM tiktok_products")
tiktok_products = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM tiktok_daily_sales")
tiktok_sales = c.fetchone()[0]
print(f"\nTikTok: {tiktok_products} 个商品, {tiktok_sales} 条销售记录")
conn.close()

print("\n" + "=" * 50)
