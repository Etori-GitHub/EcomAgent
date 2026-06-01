#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化类目和任务相关的数据库表
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def init_tables():
    """创建数据库表"""
    
    # 1. categories.db - 类目基础信息
    categories_db = DATA_DIR / "categories.db"
    conn = sqlite3.connect(categories_db)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            platform TEXT NOT NULL,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            enabled INTEGER DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_scraped_at TIMESTAMP,
            last_products_count INTEGER,
            total_scrapes INTEGER DEFAULT 0,
            total_products INTEGER DEFAULT 0,
            UNIQUE(platform, name)
        )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_categories_platform ON categories(platform)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_categories_enabled ON categories(enabled)')
    
    conn.commit()
    conn.close()
    print(f"[OK] categories.db 初始化完成")
    
    # 2. category_daily.db - 每日抓取记录
    daily_db = DATA_DIR / "category_daily.db"
    conn = sqlite3.connect(daily_db)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS category_daily (
            id INTEGER PRIMARY KEY,
            category_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            products_count INTEGER,
            task_id TEXT,
            scraped_at TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id),
            UNIQUE(category_id, date)
        )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_daily_date ON category_daily(date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_daily_category ON category_daily(category_id)')
    
    conn.commit()
    conn.close()
    print(f"[OK] category_daily.db 初始化完成")
    
    # 3. tasks.db - 任务记录
    tasks_db = DATA_DIR / "tasks.db"
    conn = sqlite3.connect(tasks_db)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            task_id TEXT UNIQUE NOT NULL,
            platform TEXT NOT NULL,
            status TEXT DEFAULT 'running',
            started_at TIMESTAMP,
            finished_at TIMESTAMP,
            total_categories INTEGER,
            completed_categories INTEGER DEFAULT 0,
            total_products INTEGER DEFAULT 0,
            error_message TEXT
        )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_platform ON tasks(platform)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)')
    
    conn.commit()
    conn.close()
    print(f"[OK] tasks.db 初始化完成")
    
    # 4. 创建任务目录
    tasks_dir = BASE_DIR / "output" / "tasks"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    print(f"[OK] output/tasks/ 目录创建完成")
    
    print(f"\n全部初始化完成！")


if __name__ == "__main__":
    init_tables()
