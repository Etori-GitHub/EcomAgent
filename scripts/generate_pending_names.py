#!/usr/bin/env python3
"""
生成待翻译的商品名称 JSON
从商品主库中选取没有简称或简称是英文的商品，生成 JSON 供 OpenClaw AI 翻译
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path


# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSING_DIR = DATA_DIR / "name_processing"

# 输出文件
PENDING_FILE = PROCESSING_DIR / "pending_names.json"

# 每批处理数量
BATCH_SIZE = 50

# 超时时间（分钟）
TIMEOUT_MINUTES = 30


def is_chinese_short_name(short_name: str) -> bool:
    """判断简称是否已经是中文"""
    if not short_name:
        return False
    for char in short_name:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False


def check_pending_file_status() -> tuple:
    """检查 pending_names.json 状态"""
    if not PENDING_FILE.exists():
        return (False, False, "文件不存在，可以生成")
    
    mtime = datetime.fromtimestamp(PENDING_FILE.stat().st_mtime)
    age = datetime.now() - mtime
    
    if age < timedelta(minutes=TIMEOUT_MINUTES):
        return (True, True, f"文件存在且未超时，等待处理")
    else:
        return (True, False, f"文件已超时，将删除重新生成")


def get_pending_products(limit: int = BATCH_SIZE) -> list:
    """从商品主库获取待翻译的商品"""
    db_path = DATA_DIR / "product_master.db"
    
    if not db_path.exists():
        print(f"[ERROR] 数据库不存在: {db_path}")
        return []
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT ecom_code, name, short_name
        FROM product_master
        ORDER BY id ASC
    """)
    
    all_rows = cursor.fetchall()
    conn.close()
    
    # 过滤出需要翻译的（没有简称或简称不含中文）
    pending = []
    for row in all_rows:
        ecom_code, name, short_name = row
        if not is_chinese_short_name(short_name):
            pending.append({
                "id": ecom_code,
                "name": name
            })
            if len(pending) >= limit:
                break
    
    return pending


def generate_pending_json():
    """生成待翻译的 JSON 文件"""
    
    PROCESSING_DIR.mkdir(parents=True, exist_ok=True)
    
    exists, should_skip, reason = check_pending_file_status()
    print(f"[INFO] {reason}")
    
    if should_skip:
        print(f"[INFO] 跳过生成，等待 OpenClaw 处理")
        return False
    
    if exists:
        PENDING_FILE.unlink()
        print(f"[INFO] 已删除超时文件")
    
    items = get_pending_products()
    
    if not items:
        print(f"[INFO] 没有待翻译的商品")
        return False
    
    batch_id = datetime.now().strftime("%Y%m%d_%H%M")
    
    data = {
        "batch_id": batch_id,
        "created_at": datetime.now().isoformat(),
        "count": len(items),
        "items": items
    }
    
    with open(PENDING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 已生成 pending_names.json，共 {len(items)} 条")
    for item in items[:3]:
        print(f"     - {item['id']}: {item['name'][:40]}...")
    
    return True


if __name__ == "__main__":
    generate_pending_json()