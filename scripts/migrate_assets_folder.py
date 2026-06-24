# -*- coding: utf-8 -*-
"""
迁移素材文件夹：从 ecom_code 改名为 sourcing_code
"""

import sqlite3
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = DATA_DIR / "assets"
SOURCING_DB = DATA_DIR / "sourcing.db"
ASSETS_DB = DATA_DIR / "assets.db"

def migrate():
    print("=" * 60)
    print("素材文件夹迁移")
    print("=" * 60)
    
    # 1. 获取货源编码映射
    conn = sqlite3.connect(str(SOURCING_DB))
    conn.row_factory = sqlite3.Row
    cursor = conn.execute("SELECT ecom_code, offer_id, sourcing_code FROM sourcing_1688")
    rows = cursor.fetchall()
    
    # 构建 ecom_code -> sourcing_code 映射
    code_map = {}
    for row in rows:
        code_map[row['ecom_code']] = row['sourcing_code']
    
    print(f"货源编码映射: {code_map}")
    
    # 2. 检查素材文件夹
    if not ASSETS_DIR.exists():
        print("素材目录不存在，无需迁移")
        return
    
    folders = [f for f in ASSETS_DIR.iterdir() if f.is_dir()]
    print(f"现有素材文件夹: {[f.name for f in folders]}")
    
    # 3. 重命名文件夹
    for folder in folders:
        ecom_code = folder.name
        
        if ecom_code not in code_map:
            print(f"⚠️ {ecom_code} 未找到对应的 sourcing_code，跳过")
            continue
        
        sourcing_code = code_map[ecom_code]
        new_folder = ASSETS_DIR / sourcing_code
        
        if new_folder.exists():
            print(f"⚠️ {sourcing_code} 已存在，跳过")
            continue
        
        print(f"重命名: {ecom_code} → {sourcing_code}")
        shutil.move(str(folder), str(new_folder))
    
    # 4. 更新素材数据库
    if ASSETS_DB.exists():
        print("\n更新素材数据库...")
        conn = sqlite3.connect(str(ASSETS_DB))
        
        for old_code, new_code in code_map.items():
            conn.execute(
                "UPDATE sourcing_assets SET sourcing_code = ? WHERE ecom_code = ?",
                (new_code, old_code)
            )
        
        conn.commit()
        
        # 验证
        cursor = conn.execute("SELECT COUNT(*) FROM sourcing_assets WHERE sourcing_code IS NOT NULL")
        count = cursor.fetchone()[0]
        print(f"已更新 {count} 条素材记录")
        conn.close()
    
    print("\n迁移完成！")

if __name__ == "__main__":
    migrate()