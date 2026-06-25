#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复素材数据库中的路径
问题：数据库中存储的是 assets\ECTK26000403\... 
实际：assets\ECTK26000403_986281346010\...
"""

import sqlite3
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = DATA_DIR / "assets"
ASSETS_DB = DATA_DIR / "assets.db"


def get_actual_folder_name(ecom_code: str) -> str:
    """根据 ecom_code 查找实际文件夹名称"""
    # 可能的文件夹名称：
    # 1. ecom_code (如 ECTK26000403)
    # 2. ecom_code_数字 (如 ECTK26000403_986281346010)
    
    # 先尝试精确匹配
    exact_path = ASSETS_DIR / ecom_code
    if exact_path.exists():
        return ecom_code
    
    # 查找带后缀的文件夹
    for folder in ASSETS_DIR.iterdir():
        if folder.is_dir() and folder.name.startswith(ecom_code):
            return folder.name
    
    # 没找到，返回原始值
    return ecom_code


def fix_paths():
    """修复数据库中的路径"""
    if not ASSETS_DB.exists():
        print("[ERROR] assets.db 不存在")
        return
    
    conn = sqlite3.connect(ASSETS_DB)
    cursor = conn.cursor()
    
    # 获取所有记录
    cursor.execute("SELECT id, ecom_code, files FROM sourcing_assets")
    rows = cursor.fetchall()
    
    print(f"[INFO] 找到 {len(rows)} 条记录")
    
    fixed_count = 0
    
    for row in rows:
        id, ecom_code, files_str = row
        
        # 查找实际文件夹名称
        actual_folder = get_actual_folder_name(ecom_code)
        
        if actual_folder != ecom_code:
            # 需要修复路径
            files = json.loads(files_str)
            
            new_files = []
            for f in files:
                # 替换路径中的 ecom_code 为实际文件夹名称
                # assets\ECTK26000403\... -> assets\ECTK26000403_986281346010\...
                new_f = re.sub(
                    f'assets[/\\\\]{ecom_code}',
                    f'assets/{actual_folder}',
                    f
                )
                new_files.append(new_f)
            
            # 更新数据库
            new_files_str = json.dumps(new_files)
            cursor.execute(
                "UPDATE sourcing_assets SET files = ? WHERE id = ?",
                (new_files_str, id)
            )
            
            print(f"[FIX] {ecom_code} -> {actual_folder}")
            fixed_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n[OK] 修复完成，共 {fixed_count} 条")


if __name__ == "__main__":
    fix_paths()