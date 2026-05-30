import json
import os

translated_dir = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\translated'
all_items = []

# Read all translated batches
for filename in sorted(os.listdir(translated_dir)):
    if filename.endswith('.json'):
        filepath = os.path.join(translated_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            items = data.get('items', [])
            all_items.extend(items)
            print(f'Loaded {filename}: {len(items)} items')

print(f'\nTotal translated items: {len(all_items)}')

# Save merged result
output = {
    'batch_id': 'merged_all',
    'items': all_items
}

output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\processed_names.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f'Saved to processed_names.json')
