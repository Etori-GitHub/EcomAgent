#!/usr/bin/env python3
"""修复被截断的 processed_names.json 文件"""

import json
from pathlib import Path

PROCESSED_FILE = Path(r"C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\processed_names.json")

def fix_json():
    # 读取文件内容
    with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 找到最后一个完整的记录（以 },\n 结尾的行）
    lines = content.split('\n')
    
    # 从后往前找最后一个完整的记录
    last_complete_idx = -1
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        if line.endswith('},'):
            last_complete_idx = i
            break
    
    if last_complete_idx > 0:
        # 截取到最后一个完整记录，并添加 JSON 结尾
        fixed_lines = lines[:last_complete_idx+1]
        # 移除最后一行的逗号
        fixed_lines[-1] = fixed_lines[-1].rstrip(',\n')
        fixed_content = '\n'.join(fixed_lines) + '\n  ]\n}'
        
        # 验证修复后的 JSON
        try:
            data = json.loads(fixed_content)
            print(f'[OK] 修复成功，共 {len(data.get("items", []))} 条记录')
            
            # 保存修复后的文件
            with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print('[OK] 文件已保存')
            return True
        except json.JSONDecodeError as e:
            print(f'[ERROR] 修复失败: {e}')
            return False
        print('[ERROR] 无法找到完整记录')
        return False

if __name__ == "__main__":
    fix_json()
