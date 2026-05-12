import re

with open('category_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 查找所有包含 /product/ 的链接
product_links = re.findall(r'<a[^>]*href=["\'](/product/[^"\']+)["\'][^>]*>([^<]+)</a>', html)
print(f'找到 {len(product_links)} 个商品链接')
for i, (href, text) in enumerate(product_links[:5]):
    print(f'{i+1}. /product/{href}')
    print(f'   Text: {text[:100]}')
    print()

# 查找包含价格模式的元素
price_pattern = r'<[^>]*>.*?\$[\d,.]+.*?</[^>]*>|<[^>]*>.*?¥[\d,.]+.*?</[^>]*>|<[^>]*>.*?元[\d,.]+.*?</[^>]*/>'
price_matches = re.findall(price_pattern, html[:50000], re.DOTALL)
print(f'找到 {len(price_matches)} 个价格元素')
for i, match in enumerate(price_matches[:5]):
    print(f'{i+1}. {match[:100]}')
    print()
