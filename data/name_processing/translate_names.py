import json

# 读取 pending_names.json
input_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json'
with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 翻译规则
def translate_name(name):
    """
    翻译商品名称
    1. 保留品牌名
    2. 翻译产品类型和特征
    3. 简洁但完整（15字以内）
    """
    # 品牌名列表（不翻译）
    brand_names = [
        'Apple', 'Amazon', 'Amazon Basics', 'Batman', 'DC', 'Cisily', 
        'Dumpling', 'Swamp Thing', 'Ju-On'
    ]
    
    # 翻译映射
    translations = {
        # 产品类型
        'Desktop Computer': '台式电脑',
        'Computer': '电脑',
        'Yoga Mat': '瑜伽垫',
        'Exercise Yoga Mat': '瑜伽垫',
        'Sponge Holder': '海绵收纳架',
        'Kitchen Sink': '厨房水槽',
        'Mystery Box': '盲盒',
        'comic book': '漫画书',
        'comic': '漫画',
        'Limited Edition': '限量版',
        '4K Ultra HD': '4K超高清',
        
        # 特征词
        'Extra Thick': '加厚',
        'with M4 chip': 'M4芯片',
        
        # 产品名称（特定翻译）
        'Mac mini': 'Mac mini',
        
        # 其他
        'VF/NM': 'VF/NM',  # 漫画品相等级，保留
    }
    
    result = name
    
    # 按照特定规则处理
    # 1. Apple 2024 Mac mini Desktop Computer with M4 chip
    if 'Apple 2024 Mac mini Desktop Computer with M4 chip' in name:
        return '苹果Mac mini M4芯片台式电脑'
    
    # 2. Amazon Basics Extra Thick Exercise Yoga Mat
    if 'Amazon Basics Extra Thick Exercise Yoga Mat' in name:
        return '亚马逊加厚瑜伽垫'
    
    # 3. Batman (3rd Series) #163A VF/NM ; DC comic book
    if 'Batman' in name and 'comic book' in name:
        return '蝙蝠侠漫画书#163A'
    
    # 4. Swamp Thing 1989#1A VF/NM ; DC comic book
    if 'Swamp Thing' in name and 'comic book' in name:
        return '沼泽怪物漫画书#1A'
    
    # 5. Cisily Sponge Holder for Kitchen Sink
    if 'Cisily Sponge Holder for Kitchen Sink' in name:
        return 'Cisily厨房海绵收纳架'
    
    # 6. Dumpling Squishy Mystery Box
    if 'Dumpling Squishy Mystery Box' in name:
        return '饺子解压玩具盲盒'
    
    # 7. Identity [Limited Edition] [4K Ultra HD]
    if 'Identity' in name and 'Limited Edition' in name:
        return '《身份》限量版4K超高清'
    
    # 8. Ju-On: The Grudge [Limited Edition] [4K Ultra HD]
    if 'Ju-On' in name and 'Limited Edition' in name:
        return '《咒怨》限量版4K超高清'
    
    return result

# 翻译所有商品名称
items = []
for item in data['items']:
    short_name = translate_name(item['name'])
    items.append({
        'id': item['id'],
        'short_name': short_name
    })

# 生成输出
output_data = {
    'batch_id': data['batch_id'],
    'items': items
}

# 保存到 processed_names.json
output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\processed_names.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"翻译完成，共 {len(items)} 个商品:")
for item in items:
    print(f"  {item['id']}: {item['short_name']}")

print(f"\n保存到: {output_path}")