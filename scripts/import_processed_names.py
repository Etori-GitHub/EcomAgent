#!/usr/bin/env python3
"""
导入 OpenClaw AI 翻译后的商品简称
读取 processed_names.json，根据 id 更新商品主库中的简称字段
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSING_DIR = DATA_DIR / "name_processing"

PENDING_FILE = PROCESSING_DIR / "pending_names.json"
PROCESSED_FILE = PROCESSING_DIR / "processed_names.json"


def import_processed_names():
    """导入翻译后的简称"""
    
    if not PROCESSED_FILE.exists():
        if PENDING_FILE.exists():
            print(f"[INFO] OpenClaw 还未处理完成，跳过")
        else:
            print(f"[INFO] 没有待处理的数据，跳过")
        return False
    
    try:
        with open(PROCESSED_FILE, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] 读取文件失败: {e}")
        return False
    
    items = data.get("items", [])
    batch_id = data.get("batch_id", "unknown")
    
    if not items:
        print(f"[INFO] 没有数据")
        PROCESSED_FILE.unlink()
        return False
    
    print(f"[INFO] 开始导入批次 {batch_id}，共 {len(items)} 条")
    
    db_path = DATA_DIR / "product_master.db"
    if not db_path.exists():
        print(f"[ERROR] 数据库不存在")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    updated = 0
    skipped = 0
    
    for item in items:
        ecom_code = item.get("id")
        short_name = item.get("short_name")
        
        if not ecom_code or not short_name:
            skipped += 1
            continue
        
        # 优先使用 ecom_code 匹配，其次尝试 platform_id
        cursor.execute("SELECT id FROM product_master WHERE ecom_code = ?", (ecom_code,))
        if not cursor.fetchone():
            # 尝试 platform_id (ASIN)
            cursor.execute("SELECT id FROM product_master WHERE platform_id = ?", (ecom_code,))
            if not cursor.fetchone():
                skipped += 1
                continue
            cursor.execute("""
                UPDATE product_master 
                SET short_name = ?, last_updated_at = ?
                WHERE platform_id = ?
            """, (short_name, datetime.now().isoformat(), ecom_code))
        else:
            cursor.execute("""
                UPDATE product_master 
                SET short_name = ?, last_updated_at = ?
                WHERE ecom_code = ?
            """, (short_name, datetime.now().isoformat(), ecom_code))
        
        updated += 1
        print(f"[OK] {ecom_code}: {short_name}")
    
    conn.commit()
    conn.close()
    
    print(f"\n[OK] 导入完成: 更新 {updated} 条，跳过 {skipped} 条")
    
    # 删除文件
    PROCESSED_FILE.unlink()
    if PENDING_FILE.exists():
        PENDING_FILE.unlink()
    
    return True


if __name__ == "__main__":
    import_processed_names()