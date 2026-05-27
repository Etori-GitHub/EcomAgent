import json
import os

translated_dir = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\translated'
output_file = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\processed_names.json'
all_items = []

for i in range(1, 32):
    filename = f'batch_{i:03d}.json'
    filepath = os.path.join(translated_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'items' in data:
                all_items.extend(data['items'])
                print(f'Loaded {filename}: {len(data["items"])} items')

print(f'Total items: {len(all_items)}')

# Save merged result
result = {
    "batch_id": "merged_all_batches",
    "items": all_items
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f'Saved to {output_file}')
