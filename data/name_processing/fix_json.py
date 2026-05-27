#!/usr/bin/env python3
"""修复被截断的 processed_names.json"""

import re
from pathlib import Path

PROCESSED_FILE = Path(__file__).parent / "processed_names.json"

with open(PROCESSED_FILE, "r", encoding="utf-8-sig") as f:
    content = f.read()

# 找所有完整条目
pattern = r'\{"id": "[^"]+", "short_name": "[^"]*"\}'
matches = re.findall(pattern, content)

print(f"找到 {len(matches)} 个完整条目")
if matches:
    print(f"最后一个条目: {matches[-1]}")

# 重建 JSON
fixed_json = '{\n  "batch_id": "ecomagent-translate-names-20260524",\n  "items": [\n'
fixed_json += ",\n".join(["    " + m for m in matches])
fixed_json += "\n  ]\n}"

# 写入修复后的文件
with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
    f.write(fixed_json)

print(f"\n已修复文件，共 {len(matches)} 条记录")
