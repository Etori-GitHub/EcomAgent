#!/usr/bin/env python3
"""
EcomAgent OpenClaw 自动配置模块

功能：
1. 检查 OpenClaw 是否安装
2. 检查定时任务是否已配置
3. 自动创建缺失的定时任务
4. 同步配置状态

任务命名规范：
- 所有 EcomAgent 任务以 "ecomagent-" 开头
- 格式：ecomagent-<功能名>

配置文件：config/openclaw_settings.json
OpenClaw 数据库：~/.openclaw/state/openclaw.sqlite

使用方法：
python scripts/openclaw_config.py check    # 检查配置状态
python scripts/openclaw_config.py setup    # 自动配置缺失的任务
python scripts/openclaw_config.py sync     # 从 OpenClaw 同步状态到本地配置
"""

import sys
import os
import json
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime

# 项目路径（跨平台）
PROJECT_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_DIR / "config"
SETTINGS_FILE = CONFIG_DIR / "openclaw_settings.json"

# OpenClaw 路径
OPENCLAW_DIR = Path.home() / ".openclaw"
OPENCLAW_STATE_DB = OPENCLAW_DIR / "state" / "openclaw.sqlite"

# 任务前缀
TASK_PREFIX = "ecomagent-"

# 任务定义
TASKS = {
    "amazon_fetch": {
        "name": f"{TASK_PREFIX}amazon-fetch",
        "description": "EcomAgent 每日 Amazon 数据抓取",
        "schedule": {"kind": "cron", "expr": "0 3 * * *", "tz": "Asia/Shanghai"},
        "sessionTarget": "isolated",
        "wakeMode": "now",
        "payload": {
            "kind": "agentTurn",
            "message": f"请执行 EcomAgent Amazon 每日数据抓取任务：\n\n1. 先检查配置文件 {PROJECT_DIR}/config/openclaw_settings.json\n2. 如果 amazon_fetch.enabled 为 false，跳过执行并报告「已禁用」\n3. 否则执行：python {PROJECT_DIR}/scripts/daily_fetch.py amazon\n\n执行完成后报告结果：\n- 抓取了多少商品\n- 导入了多少记录\n- 下载了多少图片"
        },
        "delivery": {"mode": "none"}
    },
    "translation_pipeline": {
        "name": f"{TASK_PREFIX}translation",
        "description": "EcomAgent 商品名称翻译流水线（每 30 分钟）",
        "schedule": {"kind": "every", "everyMs": 1800000},
        "sessionTarget": "isolated",
        "wakeMode": "now",
        "payload": {
            "kind": "agentTurn",
            "message": f"请执行 EcomAgent 商品名称翻译任务：\n\n1. 先检查配置文件 {PROJECT_DIR}/config/openclaw_settings.json\n2. 如果 translation_pipeline.enabled 为 false，跳过执行并报告「已禁用」\n3. 否则执行：python {PROJECT_DIR}/scripts/generate_pending_names.py\n\n4. 等待 2 分钟后检查 {PROJECT_DIR}/data/name_processing/processed_names.json 是否存在\n\n5. 如果存在，执行：python {PROJECT_DIR}/scripts/import_processed_names.py\n\n6. 报告翻译了多少商品"
        },
        "delivery": {"mode": "none"}
    }
}

# 默认设置
DEFAULT_SETTINGS = {
    "amazon_fetch": {
        "enabled": True,
        "schedule": "0 3 * * *",
        "description": "每日凌晨 3:00 抓取 Amazon 数据"
    },
    "translation_pipeline": {
        "enabled": True,
        "interval_minutes": 30,
        "description": "每 30 分钟执行商品名称翻译"
    }
}


def check_openclaw_installed() -> bool:
    """检查 OpenClaw 是否安装"""
    return OPENCLAW_DIR.exists()


def get_local_settings() -> dict:
    """读取本地配置"""
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_SETTINGS.copy()


def save_local_settings(settings: dict):
    """保存本地配置"""
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def get_cron_jobs_from_db() -> dict:
    """从 OpenClaw 数据库读取所有 ecomagent 任务"""
    if not OPENCLAW_STATE_DB.exists():
        return {}
    
    try:
        conn = sqlite3.connect(OPENCLAW_STATE_DB)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT job_id, name, enabled FROM cron_jobs WHERE name LIKE ?",
            (f"{TASK_PREFIX}%",)
        )
        
        jobs = {}
        for row in cursor.fetchall():
            job_id, name, enabled = row
            jobs[name] = {
                "job_id": job_id,
                "enabled": bool(enabled)
            }
        
        conn.close()
        return jobs
    except Exception as e:
        print(f"[ERROR] 读取数据库失败: {e}")
        return {}


def check_task_exists(task_name: str) -> tuple:
    """检查任务是否存在，返回 (exists, enabled)"""
    jobs = get_cron_jobs_from_db()
    if task_name in jobs:
        return (True, jobs[task_name]["enabled"])
    return (False, False)


def create_cron_job_via_cli(task_key: str) -> bool:
    """通过 openclaw cron 命令创建任务（备用方案）"""
    task = TASKS.get(task_key)
    if not task:
        return False
    
    # 这个方法需要 openclaw 命令行工具支持，暂时返回 False
    # 实际创建由启动脚本通过 cron 工具完成
    return False


def check_config_status():
    """检查配置状态"""
    print("\n" + "=" * 60)
    print("EcomAgent OpenClaw 配置检查")
    print("=" * 60 + "\n")
    
    # 1. 检查 OpenClaw 安装
    if check_openclaw_installed():
        print(f"[OK] OpenClaw 已安装: {OPENCLAW_DIR}")
    else:
        print("[INFO] OpenClaw 未安装")
        print("\n[RESULT] 无法使用定时任务功能")
        return
    
    print()
    
    # 2. 检查定时任务配置
    jobs = get_cron_jobs_from_db()
    
    print("[STATUS] 定时任务配置状态：\n")
    
    all_configured = True
    for task_key, task_def in TASKS.items():
        task_name = task_def["name"]
        if task_name in jobs:
            enabled = jobs[task_name]["enabled"]
            status = "[ON] " if enabled else "[OFF]"
            print(f"  {status} {task_def['description']}")
            print(f"         名称: {task_name}")
            print(f"         ID: {jobs[task_name]['job_id']}")
        else:
            print(f"  [MISS] 未配置 {task_def['description']}")
            print(f"         名称: {task_name}")
            all_configured = False
        print()
    
    # 3. 检查本地配置文件
    settings = get_local_settings()
    if SETTINGS_FILE.exists():
        print(f"[OK] 本地配置文件: {SETTINGS_FILE}")
    else:
        print(f"[INFO] 本地配置文件不存在，将使用默认配置")
    
    print()
    
    # 4. 总结
    if all_configured:
        print("[RESULT] 所有定时任务已配置")
    else:
        print("[RESULT] 部分任务未配置，请运行：python scripts/openclaw_config.py setup")


def setup_tasks():
    """自动配置缺失的任务"""
    print("\n" + "=" * 60)
    print("EcomAgent OpenClaw 自动配置")
    print("=" * 60 + "\n")
    
    # 1. 检查 OpenClaw 安装
    if not check_openclaw_installed():
        print("[ERROR] OpenClaw 未安装，无法配置定时任务")
        return False
    
    print(f"[OK] OpenClaw 已安装: {OPENCLAW_DIR}\n")
    
    # 2. 检查现有任务
    jobs = get_cron_jobs_from_db()
    
    # 3. 创建本地配置文件
    settings = get_local_settings()
    
    # 从数据库同步状态
    for task_key, task_def in TASKS.items():
        task_name = task_def["name"]
        if task_name in jobs:
            settings[task_key]["enabled"] = jobs[task_name]["enabled"]
    
    save_local_settings(settings)
    print(f"[OK] 已同步本地配置: {SETTINGS_FILE}\n")
    
    # 4. 检查缺失的任务
    missing = []
    for task_key, task_def in TASKS.items():
        task_name = task_def["name"]
        if task_name not in jobs:
            missing.append(task_key)
    
    if missing:
        print(f"[INFO] 发现 {len(missing)} 个未配置的任务")
        print("[INFO] 请在 OpenClaw 主会话中运行以下命令创建任务：")
        print()
        for task_key in missing:
            task = TASKS[task_key]
            print(f"  # 创建 {task['description']}")
            print(f"  # 任务名称: {task['name']}")
            print()
    else:
        print("[OK] 所有任务已配置")
    
    return True


def sync_settings():
    """从 OpenClaw 数据库同步状态到本地配置"""
    print("\n" + "=" * 60)
    print("EcomAgent OpenClaw 状态同步")
    print("=" * 60 + "\n")
    
    if not check_openclaw_installed():
        print("[ERROR] OpenClaw 未安装")
        return False
    
    jobs = get_cron_jobs_from_db()
    settings = get_local_settings()
    
    updated = 0
    for task_key, task_def in TASKS.items():
        task_name = task_def["name"]
        if task_name in jobs:
            old_enabled = settings.get(task_key, {}).get("enabled", True)
            new_enabled = jobs[task_name]["enabled"]
            
            if old_enabled != new_enabled:
                settings[task_key]["enabled"] = new_enabled
                updated += 1
                action = "启用" if new_enabled else "禁用"
                print(f"[SYNC] {task_name}: {action}")
    
    save_local_settings(settings)
    
    print(f"\n[OK] 同步完成，更新 {updated} 项")
    return True


def main():
    """主入口"""
    if len(sys.argv) < 2:
        print("用法: python scripts/openclaw_config.py <command>")
        print("命令:")
        print("  check  - 检查配置状态")
        print("  setup  - 自动配置缺失的任务")
        print("  sync   - 从 OpenClaw 同步状态到本地配置")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "check":
        check_config_status()
    elif command == "setup":
        setup_tasks()
    elif command == "sync":
        sync_settings()
    else:
        print(f"[ERROR] 未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
