#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清除今天的抓取状态记录
"""

import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

today = datetime.now().strftime("%Y-%m-%d")
print(f"清除 {today} 的抓取状态...\n")

# 清除 category_daily 表
daily_db = DATA_DIR / "daily_records.db"
if daily_db.exists():
    conn = sqlite3.connect(daily_db)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM category_daily WHERE date = ?", (today,))
    deleted = cursor.rowcount
    print(f"[daily_records] 删除 category_daily: {deleted} 条")
    
    conn.commit()
    conn.close()
else:
    print("[INFO] daily_records.db 不存在")

print("\n清除完成！现在可以重新抓取了。")