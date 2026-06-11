import json

with open('processed_names.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'Total items: {len(data["items"])}')
print('Last 10 items:')
for item in data['items'][-10:]:
    print(f"  {item['id']}: {item['short_name']}")
