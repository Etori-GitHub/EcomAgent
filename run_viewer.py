#!/usr/bin/env python3
"""
EcomAgent Data Viewer 启动脚本
"""

import sys
from pathlib import Path

# 添加 src 目录到路径
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"

# 确保 src 在路径中
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

try:
    from data_viewer.main import run_server
except ImportError as e:
    print(f"错误：无法导入 data_viewer 模块")
    print(f"详细信息：{e}")
    print(f"当前路径：{SRC_DIR}")
    print(f"路径列表：{sys.path}")
    sys.exit(1)

if __name__ == "__main__":
    run_server()
