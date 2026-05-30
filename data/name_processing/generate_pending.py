import json
import os

# Load all items
with open(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\all_items.json', 'r', encoding='utf-8') as f:
    all_items = json.load(f)

# Load translated items
translated_dir = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\translated'
translated_ids = set()

for filename in os.listdir(translated_dir):
    if filename.endswith('.json'):
        with open(os.path.join(translated_dir, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data.get('items', []):
                translated_ids.add(item['id'])

# Find pending items
pending = [item for item in all_items if item['id'] not in translated_ids]
print(f'Total items: {len(all_items)}')
print(f'Translated: {len(translated_ids)}')
print(f'Pending: {len(pending)}')

# Save pending items
if pending:
    output = {
        'batch_id': f'pending_{len(pending)}',
        'items': pending[:100]  # First 100 for processing
    }
    with open(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f'Saved {len(output["items"])} items to pending_names.json')
