import json
from pathlib import Path

# 查看最近抓取的文件，看看有什么字段
file = Path('output/imported/amazon_electronics_20260601_032501.json')
with open(file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print('=== 抓取数据结构 ===')
print(f'商品数量: {len(data["products"])}')
print(f'字段: {list(data["products"][0].keys())}')

# 看看前5个商品的详细数据
for i, p in enumerate(data['products'][:5]):
    print(f'\n商品 {i+1}:')
    for k, v in p.items():
        print(f'  {k}: {v}')
