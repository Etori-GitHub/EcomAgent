import json
from pathlib import Path

# 检查最近导入的 Amazon 文件
imported_dir = Path('output/imported')
files = sorted(imported_dir.glob('amazon_*.json'), key=lambda x: x.stat().st_mtime, reverse=True)[:3]

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
    products = data.get('products', [])
    print(f'File: {f.name}')
    print(f'  Products: {len(products)}')
    if products:
        p = products[0]
        name = p.get('name', '')[:30]
        price = p.get('price')
        rating = p.get('rating')
        rank = p.get('rank')
        print(f'  Sample: name={name}, price={price}, rating={rating}, rank={rank}')
    print()
