#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理翻译任务相关文件
"""

from pathlib import Path
import json

BASE_DIR = Path(__file__).parent.parent
PROCESSING_DIR = BASE_DIR / "data" / "name_processing"

# 清理待翻译和已翻译文件
pending_file = PROCESSING_DIR / "pending_names.json"
processed_file = PROCESSING_DIR / "processed_names.json"

if pending_file.exists():
    pending_file.unlink()
    print(f"[删除] {pending_file.name}")

if processed_file.exists():
    processed_file.unlink()
    print(f"[删除] {processed_file.name}")

# 创建空的文件
with open(pending_file, 'w', encoding='utf-8') as f:
    json.dump({"batch_id": "", "items": []}, f, ensure_ascii=False)
print(f"[创建] {pending_file.name} (空)")

print("\n清理完成！")