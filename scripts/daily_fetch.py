#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EcomAgent 每日数据抓取任务
- 抓取 Amazon Best Sellers
- 抓取 TikTok Shop 热销
- 导入数据库
- 下载图片
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

# Windows UTF-8 兼容
if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')
    # 子进程也用 UTF-8
    os.environ['PYTHONIOENCODING'] = 'utf-8'

BASE_DIR = Path(__file__).parent.parent

# 脚本路径
AMAZON_FETCHER = BASE_DIR / "skills" / "amazon-fetcher" / "src" / "fetch_amazon_all_categories.py"
TIKTOK_FETCHER = BASE_DIR / "skills" / "tiktok-fetcher" / "src" / "fetch_tiktok_categories.py"
DB_IMPORTER = BASE_DIR / "skills" / "db-importer" / "src" / "import_to_db.py"
IMAGE_DOWNLOADER = BASE_DIR / "scripts" / "download_images.py"


def run_script(script_path: Path, args: list = None, desc: str = ""):
    """运行脚本"""
    print(f"\n{'='*60}")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {desc or script_path.name}")
    print(f"{'='*60}")
    
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)
    
    try:
        # Windows 下设置环境变量确保 UTF-8
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'
        
        result = subprocess.run(
            cmd, 
            cwd=str(BASE_DIR), 
            env=env,
            capture_output=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] 运行失败: {e}")
        return False
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='EcomAgent 每日数据抓取')
    parser.add_argument('platform', nargs='?', default='all', 
                        choices=['amazon', 'tiktok', 'all', 'import', 'images'],
                        help='执行平台或步骤')
    parser.add_argument('--skip-import', action='store_true', help='跳过数据导入')
    parser.add_argument('--skip-images', action='store_true', help='跳过图片下载')
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"EcomAgent 每日数据抓取")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    success = True
    
    # Amazon 抓取
    if args.platform in ['amazon', 'all']:
        if AMAZON_FETCHER.exists():
            if not run_script(AMAZON_FETCHER, desc="Amazon Best Sellers 抓取"):
                success = False
        else:
            print(f"[SKIP] Amazon 抓取脚本不存在")
    
    # TikTok 抓取
    if args.platform in ['tiktok', 'all']:
        if TIKTOK_FETCHER.exists():
            if not run_script(TIKTOK_FETCHER, desc="TikTok Shop 热销抓取"):
                success = False
        else:
            print(f"[SKIP] TikTok 抓取脚本不存在")
    
    # 数据导入（tiktok/amazon 也触发导入）
    if args.platform in ['import', 'all', 'tiktok', 'amazon'] and not args.skip_import:
        if DB_IMPORTER.exists():
            if not run_script(DB_IMPORTER, desc="数据导入数据库"):
                success = False
        else:
            print(f"[SKIP] 数据导入脚本不存在")
    
    # 图片下载
    if args.platform in ['images', 'all'] and not args.skip_images:
        if IMAGE_DOWNLOADER.exists():
            if not run_script(IMAGE_DOWNLOADER, ['all'], desc="下载商品图片"):
                success = False
        else:
            print(f"[SKIP] 图片下载脚本不存在")
    
    print(f"\n{'='*60}")
    print(f"完成: {'成功' if success else '有错误'}")
    print(f"{'='*60}")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())