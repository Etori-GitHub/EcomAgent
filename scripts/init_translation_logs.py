#!/usr/bin/env python3
"""
初始化翻译日志表
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def init_translation_logs_table():
    """创建翻译日志表"""
    db_path = DATA_DIR / "product_master.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # 创建翻译日志表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS translation_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            total_count INTEGER DEFAULT 0,
            success_count INTEGER DEFAULT 0,
            failed_count INTEGER DEFAULT 0,
            started_at TEXT,
            completed_at TEXT,
            error_message TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 创建索引
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_translation_logs_batch_id 
        ON translation_logs(batch_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_translation_logs_status 
        ON translation_logs(status)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_translation_logs_created_at 
        ON translation_logs(created_at DESC)
    """)
    
    conn.commit()
    conn.close()
    print("✅ 翻译日志表已创建")

if __name__ == "__main__":
    init_translation_logs_table()