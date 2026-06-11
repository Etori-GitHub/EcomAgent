import json

# 读取已获取的数据
with open(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 提取成功获取名称的商品
valid_items = []
invalid_asins = []

for item in data['items']:
    if item['name'] and item['name'] != 'Amazon.com':
        valid_items.append(item)
    else:
        invalid_asins.append(item['id'])

print(f"Valid items: {len(valid_items)}")
print(f"Invalid items (need manual fetch): {len(invalid_asins)}")
print("\nValid items:")
for item in valid_items:
    print(f"  {item['id']}: {item['name'][:60]}...")
