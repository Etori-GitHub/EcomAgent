import json

with open(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\processed_names.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

items = data['items']

# 统计翻译质量
truncated = 0
translated = 0
english_only = 0

for item in items:
    sn = item['short_name']
    # 检查是否包含中文
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in sn)
    if has_chinese:
        translated += 1
    elif len(sn) >= 15 and sn[-1].isalpha():
        truncated += 1
    else:
        english_only += 1

print(f'Total items: {len(items)}')
print(f'Translated (with Chinese): {translated}')
print(f'Truncated (likely unprocessed): {truncated}')
print(f'English only (proper): {english_only}')
print()
print('Unprocessed examples (first 30):')
count = 0
for item in items:
    sn = item['short_name']
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in sn)
    if not has_chinese and count < 30:
        print(f'  {item["id"]}: {sn}')
        count += 1
