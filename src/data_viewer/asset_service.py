# -*- coding: utf-8 -*-
"""素材管理服务"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 项目路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = DATA_DIR / "assets"
ASSETS_DB_PATH = DATA_DIR / "assets.db"


# 素材目录
ASSETS_DIR.mkdir(parents=True, exist_ok=True)


def get_assets_db():
    """获取素材数据库连接"""
    conn = sqlite3.connect(ASSETS_DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # 创建表
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sourcing_assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ecom_code TEXT NOT NULL,
            asset_type TEXT NOT NULL,
            group_index INTEGER NOT NULL,
            files TEXT NOT NULL,
            params TEXT,
            task_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(ecom_code, asset_type, group_index)
        )
    ''')
    
    conn.commit()
    return conn


def get_assets(ecom_code: str) -> Dict:
    """
    获取货源的所有素材
    
    Returns:
        {
            "showcase": [...],
            "video": [...],
            "detail": [...]
        }
    """
    conn = get_assets_db()
    try:
        cursor = conn.execute(
            "SELECT * FROM sourcing_assets WHERE ecom_code = ? ORDER BY asset_type, group_index",
            (ecom_code,)
        )
        rows = cursor.fetchall()
        
        result = {
            "showcase": [],
            "video": [],
            "detail": []
        }
        
        for row in rows:
            asset = {
                "id": row["id"],
                "ecom_code": row["ecom_code"],
                "asset_type": row["asset_type"],
                "group_index": row["group_index"],
                "files": json.loads(row["files"]),
                "params": json.loads(row["params"]) if row["params"] else None,
                "task_id": row["task_id"],
                "created_at": row["created_at"]
            }
            
            if row["asset_type"] in result:
                result[row["asset_type"]].append(asset)
        
        return result
    finally:
        conn.close()


def save_asset(
    ecom_code: str,
    asset_type: str,
    group_index: int,
    files: List[str],
    params: Optional[Dict] = None,
    task_id: Optional[str] = None
) -> int:
    """
    保存素材记录
    
    Returns:
        asset_id
    """
    conn = get_assets_db()
    try:
        conn.execute('''
            INSERT OR REPLACE INTO sourcing_assets
            (ecom_code, asset_type, group_index, files, params, task_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            ecom_code,
            asset_type,
            group_index,
            json.dumps(files),
            json.dumps(params) if params else None,
            task_id,
            datetime.now().isoformat()
        ))
        conn.commit()
        
        # 获取插入的 ID
        cursor = conn.execute(
            "SELECT id FROM sourcing_assets WHERE ecom_code = ? AND asset_type = ? AND group_index = ?",
            (ecom_code, asset_type, group_index)
        )
        row = cursor.fetchone()
        return row["id"] if row else 0
    finally:
        conn.close()


def delete_asset(ecom_code: str, asset_type: str, group_index: int) -> bool:
    """
    删除素材记录和文件
    
    Returns:
        success
    """
    conn = get_assets_db()
    try:
        # 获取文件列表
        cursor = conn.execute(
            "SELECT files FROM sourcing_assets WHERE ecom_code = ? AND asset_type = ? AND group_index = ?",
            (ecom_code, asset_type, group_index)
        )
        row = cursor.fetchone()
        
        if row:
            files = json.loads(row["files"])
            
            # 删除文件
            for file_path in files:
                full_path = DATA_DIR / file_path
                if full_path.exists():
                    full_path.unlink()
            
            # 删除目录（如果为空）
            asset_dir = ASSETS_DIR / ecom_code / asset_type / f"group_{group_index}"
            if asset_dir.exists() and not any(asset_dir.iterdir()):
                asset_dir.rmdir()
            
            # 删除数据库记录
            conn.execute(
                "DELETE FROM sourcing_assets WHERE ecom_code = ? AND asset_type = ? AND group_index = ?",
                (ecom_code, asset_type, group_index)
            )
            conn.commit()
            return True
        
        return False
    finally:
        conn.close()


def get_next_group_index(ecom_code: str, asset_type: str) -> int:
    """
    获取下一个可用的组编号
    
    Returns:
        group_index
    """
    conn = get_assets_db()
    try:
        cursor = conn.execute(
            "SELECT MAX(group_index) as max_group FROM sourcing_assets WHERE ecom_code = ? AND asset_type = ?",
            (ecom_code, asset_type)
        )
        row = cursor.fetchone()
        return (row["max_group"] or 0) + 1
    finally:
        conn.close()


def get_asset_stats(ecom_code: str) -> Dict:
    """
    获取素材统计
    
    Returns:
        {
            "showcase_count": int,
            "video_count": int,
            "detail_count": int
        }
    """
    conn = get_assets_db()
    try:
        stats = {}
        for asset_type in ["showcase", "video", "detail"]:
            cursor = conn.execute(
                "SELECT COUNT(*) as count FROM sourcing_assets WHERE ecom_code = ? AND asset_type = ?",
                (ecom_code, asset_type)
            )
            row = cursor.fetchone()
            stats[f"{asset_type}_count"] = row["count"]
        
        return stats
    finally:
        conn.close()


def scan_assets_from_disk(ecom_code: str) -> Dict:
    """
    从磁盘扫描素材目录，更新数据库
    
    用于同步磁盘文件和数据库记录
    """
    assets = {
        "showcase": [],
        "video": [],
        "detail": []
    }
    
    ecom_dir = ASSETS_DIR / ecom_code
    if not ecom_dir.exists():
        return assets
    
    for asset_type in ["showcase", "video", "detail"]:
        type_dir = ecom_dir / asset_type
        if not type_dir.exists():
            continue
        
        for group_dir in type_dir.iterdir():
            if not group_dir.is_dir() or not group_dir.name.startswith("group_"):
                continue
            
            try:
                group_index = int(group_dir.name.split("_")[1])
            except:
                continue
            
            files = []
            for f in group_dir.iterdir():
                if f.suffix in [".mp4", ".png", ".jpg", ".jpeg"]:
                    files.append(str(f.relative_to(DATA_DIR)))
            
            if files:
                # 同步到数据库
                save_asset(ecom_code, asset_type, group_index, files)
                
                assets[asset_type].append({
                    "group_index": group_index,
                    "files": files,
                    "dir": str(group_dir)
                })
    
    return assets