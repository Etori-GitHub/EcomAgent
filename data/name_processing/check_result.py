import json
f=open(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\processed_names.json','r',encoding='utf-8')
data=json.load(f)
f.close()
print(f'Total items: {len(data["items"])}')
print(f'Batch ID: {data["batch_id"]}')
print('Sample items:')
for i in range(3):
    print(f'  {data["items"][i]}')