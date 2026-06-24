# -*- coding: utf-8 -*-
"""
数据库迁移：给货源表添加 sourcing_code 字段

执行方式：
python scripts/add_sourcing_code.py
"""

import sqlite3
from pathlib import Path

# 项目路径
BASE_DIR = Path(__file__).resolve().parent.parent
SOURCING_DB = BASE_DIR / "data" / "sourcing.db"

def migrate():
    """执行迁移"""
    conn = sqlite3.connect(str(SOURCING_DB))
    conn.row_factory = sqlite3.Row
    
    print(f"连接数据库: {SOURCING_DB}")
    
    # 1. 检查字段是否已存在
    cursor = conn.execute("PRAGMA table_info(sourcing_1688)")
    columns = [row['name'] for row in cursor.fetchall()]
    
    if 'sourcing_code' in columns:
        print("字段 sourcing_code 已存在，跳过迁移")
        conn.close()
        return
    
    # 2. 添加字段
    print("添加 sourcing_code 字段...")
    try:
        conn.execute('ALTER TABLE sourcing_1688 ADD COLUMN sourcing_code TEXT')
        conn.commit()
        print("字段添加成功")
    except Exception as e:
        print(f"添加字段失败: {e}")
        conn.close()
        return
    
    # 3. 为现有数据生成 sourcing_code
    # 规则：使用 offer_id（如果唯一），否则使用 ecom_code_offer_id
    print("生成 sourcing_code...")
    
    cursor = conn.execute("SELECT id, ecom_code, offer_id FROM sourcing_1688")
    rows = cursor.fetchall()
    
    for row in rows:
        # 使用 ecom_code_offer_id 组合作为唯一标识
        sourcing_code = f"{row['ecom_code']}_{row['offer_id']}"
        
        conn.execute(
            "UPDATE sourcing_1688 SET sourcing_code = ? WHERE id = ?",
            (sourcing_code, row['id'])
        )
    
    conn.commit()
    print(f"已为 {len(rows)} 条记录生成 sourcing_code")
    
    # 4. 创建唯一索引
    print("创建唯一索引...")
    try:
        conn.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_sourcing_code ON sourcing_1688(sourcing_code)')
        conn.commit()
        print("索引创建成功")
    except Exception as e:
        print(f"索引创建失败: {e}")
    
    # 5. 验证
    cursor = conn.execute("SELECT COUNT(*) FROM sourcing_1688 WHERE sourcing_code IS NULL")
    null_count = cursor.fetchone()[0]
    
    cursor = conn.execute("SELECT COUNT(*) FROM sourcing_1688")
    total_count = cursor.fetchone()[0]
    
    print(f"\n迁移完成:")
    print(f"  总记录数: {total_count}")
    print(f"  空 sourcing_code 数: {null_count}")
    
    conn.close()

if __name__ == "__main__":
    migrate()
