#!/usr/bin/env python3
"""检查数据库日期"""

import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

print(f"Python datetime.now(): {datetime.now()}")
print(f"Python datetime.now(UTC): {datetime.now()}")
print()

# 检查 SQLite 的 date('now')
amazon_db = DATA_DIR / "amazon.db"
if amazon_db.exists():
    conn = sqlite3.connect(amazon_db)
    cursor = conn.cursor()
    cursor.execute("SELECT date('now')")
    print(f"SQLite date('now'): {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT datetime('now')")
    print(f"SQLite datetime('now'): {cursor.fetchone()[0]}")
    
    # 检查最新的 daily_sales 日期
    cursor.execute("SELECT DISTINCT date FROM daily_sales ORDER BY date DESC LIMIT 5")
    print(f"\n最新的 daily_sales 日期:")
    for row in cursor.fetchall():
        print(f"  {row[0]}")
    
    conn.close()

tiktok_db = DATA_DIR / "tiktok.db"
if tiktok_db.exists():
    conn = sqlite3.connect(tiktok_db)
    cursor = conn.cursor()
    
    # 检查最新的 tiktok_daily_sales 日期
    cursor.execute("SELECT DISTINCT date FROM tiktok_daily_sales ORDER BY date DESC LIMIT 5")
    print(f"\n最新的 tiktok_daily_sales 日期:")
    for row in cursor.fetchall():
        print(f"  {row[0]}")
    
    conn.close()
