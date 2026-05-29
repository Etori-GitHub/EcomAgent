#!/usr/bin/env python3
"""修复 processed_names.json 中的格式问题"""
import json
from pathlib import Path

file_path = Path(r"C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\processed_names.json")

# 读取原始字节
with open(file_path, 'rb') as f:
    raw = f.read()

# 移除 BOM
if raw.startswith(b'\xef\xbb\xbf'):
    raw = raw[3:]

# 解码
content = raw.decode('utf-8')

# 问题：最后一项的 short_name 值包含了 "} 和 \r
# 正确格式应该是: "short_name": "苹果iPhone SE 2"},
# 当前错误格式: "short_name": "苹果iPhone SE 2}\r"

# 修复：替换错误的结尾
# 找到最后一个条目并修复
content = content.replace(
    '"short_name": "苹果iPhone SE 2}\r\n  ]\r\n}',
    '"short_name": "苹果iPhone SE 2"}\n  ]\n}'
)

# 写回文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed the last item")

# 验证
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Valid JSON with {len(data.get('items', []))} items")
except json.JSONDecodeError as e:
    print(f"JSON error: {e}")
