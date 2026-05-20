# 批量翻译执行脚本
# 这个脚本会循环执行：生成待翻译 -> 等待AI翻译 -> 导入结果

import subprocess
import time
import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def get_pending_count():
    conn = sqlite3.connect(DATA_DIR / "product_master.db")
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM product_master WHERE short_name IS NULL OR short_name = ""')
    count = c.fetchone()[0]
    conn.close()
    return count

def run_script(script_path):
    """运行 Python 脚本"""
    result = subprocess.run(
        ["python", script_path],
        capture_output=True,
        text=True,
        cwd=BASE_DIR
    )
    return result.stdout, result.stderr, result.returncode

def main():
    total_pending = get_pending_count()
    print(f"开始批量翻译，待翻译商品: {total_pending}")
    
    batch_num = 0
    while True:
        batch_num += 1
        pending = get_pending_count()
        
        if pending == 0:
            print("\n所有商品已翻译完成！")
            break
        
        print(f"\n=== 批次 {batch_num} (剩余 {pending} 个) ===")
        
        # 步骤1: 生成待翻译文件
        print("1. 生成待翻译文件...")
        stdout, stderr, code = run_script("scripts/generate_pending_names.py")
        if code != 0:
            print(f"生成失败: {stderr}")
            break
        print(stdout.strip())
        
        # 检查是否有待翻译的商品
        pending_file = DATA_DIR / "name_processing" / "pending_names.json"
        if not pending_file.exists():
            print("没有待翻译文件生成，退出")
            break
        
        with open(pending_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if data.get("count", 0) == 0:
            print("没有待翻译的商品，退出")
            break
        
        # 步骤2: AI翻译 (通过调用 OpenClaw API)
        print("2. 等待 AI 翻译...")
        print("   请手动运行翻译任务，或等待定时任务执行")
        print("   翻译完成后，运行: python scripts/import_processed_names.py")
        
        # 这里我们不自动翻译，因为需要 AI 来做
        # 用户需要手动触发翻译任务
        break
    
    print("\n完成！")

if __name__ == "__main__":
    main()