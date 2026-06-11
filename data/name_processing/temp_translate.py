import json
import re

# 读取待翻译数据
input_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json'
with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 显示前10个商品名称
print(f'Total items: {len(data["items"])}')
print('Sample items:')
for item in data['items'][:10]:
    print(f'  {item["id"]}: {item["name"]}')
