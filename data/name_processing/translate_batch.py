import json
import sqlite3
import re

# 翻译规则函数
def translate_name(name):
    if not name or not name.strip():
        return '商品信息缺失'
    
    name = name.strip()
    
    # 知名品牌映射
    brand_map = {
        'Apple': '苹果',
        'Samsung': '三星',
        'Sony': '索尼',
        'Nike': '耐克',
        'Adidas': '阿迪达斯',
        'Microsoft': '微软',
        'Google': '谷歌',
        'Amazon': '亚马逊',
        'Crocs': 'Crocs',
        'Midea': '美的',
        'Anker': 'Anker',
        'TP-Link': 'TP-Link',
        'NOCO': 'NOCO',
        'Pampers': '帮宝适',
        'Huggies': 'Huggies',
        'Neutrogena': 'Neutrogena',
        'Meguiars': "Meguiar's",
        'Valvoline': 'Valvoline',
        'Mobil': 'Mobil',
        'Igloo': 'Igloo',
        'Medicube': 'Medicube',
        'Honest': 'Honest',
        'WaterWipes': 'WaterWipes',
        'Desitin': 'Desitin',
        'Carhartt': 'Carhartt',
        'Hanes': 'Hanes',
        'Gildan': 'Gildan',
        'Wrangler': 'Wrangler',
        'Dr. Brown': "Dr. Brown's",
        'Elmer': "Elmer's",
        'Mrs. Meyer': "Mrs. Meyer's",
        'Bounty': 'Bounty',
        'Charmin': 'Charmin',
        'Scott': 'Scott',
        'AstroAI': 'AstroAI',
        'Nizoral': 'Nizoral',
        'PanOxyl': 'PanOxyl',
        'Aquaphor': 'Aquaphor',
        'CERAKOTE': 'CERAKOTE',
        'Chemical Guys': 'Chemical Guys',
        'Roku': 'Roku',
        'JLab': 'JLab',
        'UGREEN': 'UGREEN',
        'Fujifilm': '富士',
        'Instax': 'Instax',
        'Nespresso': 'Nespresso',
        'Lavazza': 'Lavazza',
        'Monster': 'Monster',
        'Premier': 'Premier',
        'Core Power': 'Core Power',
        'Propel': 'Propel',
        'PUR': 'PUR',
        'Bloom': 'Bloom',
        'Sparkling Ice': 'Sparkling Ice',
        'DaVinci': 'DaVinci',
        'CELSIUS': 'CELSIUS',
        'Tulip': 'Tulip',
        'Neenah': 'Neenah',
        'ScotchBlue': 'ScotchBlue',
        'Scotch': 'Scotch',
        'EltaMD': 'EltaMD',
        'Paula': "Paula's Choice",
        'Blue Lizard': 'Blue Lizard',
        'Mighty Patch': 'Mighty Patch',
        'BIODANCE': 'BIODANCE',
        'eos': 'eos',
        'The Ordinary': 'The Ordinary',
        'Maybelline': '美宝莲',
        'Clean Skin Club': 'Clean Skin Club',
        'ARTISTRO': 'ARTISTRO',
        'RED HEART': 'RED HEART',
        'Gskyer': 'Gskyer',
        'Vortex': 'Vortex',
        'Hontry': 'Hontry',
        'Elikliv': 'Elikliv',
        'Aurosports': 'Aurosports',
        'OWALA': 'Owala',
        'Owala': 'Owala',
        'STANLEY': 'STANLEY',
        'HydroJug': 'HydroJug',
        'KitchenAid': 'KitchenAid',
        'Ninja': 'Ninja',
        'Dixie': 'Dixie',
        'Angel Soft': 'Angel Soft',
        'Quilted Northern': 'Quilted Northern',
        'LMNT': 'LMNT',
        'Terro': 'Terro',
        'Zevo': 'Zevo',
        'Miracle-Gro': 'Miracle-Gro',
        'Kaytee': 'Kaytee',
        'Blue Buffalo': 'Blue Buffalo',
        'Purina': 'Purina',
        'Fancy Feast': 'Fancy Feast',
        'Fresh Step': 'Fresh Step',
        'INABA': 'INABA',
        'Milk-Bone': 'Milk-Bone',
        'Temptations': 'Temptations',
        'Greenies': 'Greenies',
        'Earth Rated': 'Earth Rated',
        'Arm & Hammer': 'Arm & Hammer',
        'Dr. Elsey': "Dr. Elsey's",
        'TurboTax': 'TurboTax',
        'Norton': 'Norton',
        'McAfee': 'McAfee',
        'Bitdefender': 'Bitdefender',
        'NordVPN': 'NordVPN',
        'Mullvad': 'Mullvad',
        'Webroot': 'Webroot',
        'Quicken': 'Quicken',
        'Malwarebytes': 'Malwarebytes',
        'Wyze': 'Wyze',
        'H&R Block': 'H&R Block',
        'Logitech': 'Logitech',
        'Razer': 'Razer',
        'DJI': 'DJI',
        'Hollyland': 'Hollyland',
        'MAYBESTA': 'MAYBESTA',
        'FIFINE': 'FIFINE',
        'Focusrite': 'Focusrite',
        'DAddario': "D'Addario",
        'Ernie Ball': 'Ernie Ball',
        'Jim Dunlop': 'Jim Dunlop',
        'HP': 'HP',
        'Sharpie': 'Sharpie',
        'Hammermill': 'Hammermill',
        'BIC': 'BIC',
        'Ortho': 'Ortho',
        'Bonide': 'Bonide',
        'Roundup': 'Roundup',
        'Wagner': "Wagner's",
        'Callaway': 'Callaway',
        'Speedo': 'Speedo',
        'Fit Simplify': 'Fit Simplify',
        'goodr': 'goodr',
        'Topps': 'Topps',
        'Panini': 'Panini',
        'Upper Deck': 'Upper Deck',
        'Bicycle': 'Bicycle',
        'Marvel': 'Marvel',
        'DC': 'DC',
        'Pokemon': '宝可梦',
        'Minecraft': '我的世界',
        'PlayStation': 'PlayStation',
        'Xbox': 'Xbox',
        'Nintendo': '任天堂',
        'Roblox': 'Roblox',
        'Luna': 'Luna',
        'Valorant': 'ValorANT',
        'Tomodachi': 'Tomodachi',
        'Star Fox': 'Star Fox',
        'Katseye': 'Katseye',
        'KATSEYE': 'KATSEYE',
        'Hazbin Hotel': 'Hazbin Hotel',
        'Ben 10': 'Ben 10',
        'Trump': '特朗普',
        'Michael Jackson': 'Michael Jackson',
        'Stray Kids': 'Stray Kids',
        'Harry Potter': '哈利波特',
        'Dungeon Crawler Carl': 'Dungeon Crawler Carl',
        'Project Hail Mary': 'Project Hail Mary',
        'The Primal Hunter': 'The Primal Hunter',
        'The Let Them Theory': 'The Let Them Theory',
        'Remarkably Bright Creatures': 'Remarkably Bright Creatures',
        'Magic Tiles': 'Magic Tiles',
        'Geometry Dash': 'Geometry Dash',
    }
    
    # 产品类型关键词翻译
    product_keywords = {
        'Ice Maker': '制冰机',
        'Nugget Ice Maker': 'nugget制冰机',
        'Mini Fridge': '迷你冰箱',
        'Chest Freezer': '卧式冷柜',
        'Freezer': '冷柜',
        'Diaper': '纸尿裤',
        'Diapers': '纸尿裤',
        'Wipes': '湿巾',
        'Baby Wipes': '婴儿湿巾',
        'Sunscreen': '防晒霜',
        'Body Lotion': '身体乳',
        'Toner': '爽肤水',
        'Pad': '棉片',
        'Mask': '面膜',
        'Mascara': '睫毛膏',
        'Makeup': '化妆品',
        'Acne': '祛痘',
        'Essential Oil': '精油',
        'Marker': '马克笔',
        'Paint Markers': '马克笔',
        'Scissors': '剪刀',
        'Glue': '胶水',
        'Tape': '胶带',
        'Yarn': '毛线',
        'Paper': '纸',
        'Cardstock': '卡纸',
        'Notebook': '笔记本',
        'Pen': '笔',
        'Book': '书',
        'Novel': '小说',
        'Album': '专辑',
        'LP': '黑胶',
        'Vinyl': '黑胶',
        'Case': '保护壳',
        'Screen Protector': '屏幕保护膜',
        'Charger': '充电器',
        'Power Bank': '充电宝',
        'Cable': '数据线',
        'Hub': '扩展坞',
        'Router': '路由器',
        'Tablet': '平板',
        'Laptop': '笔记本',
        'Headphones': '耳机',
        'Earbuds': '耳机',
        'Speaker': '音箱',
        'Microphone': '麦克风',
        'Watch': '手表',
        'Binoculars': '望远镜',
        'Telescope': '望远镜',
        'Microscope': '显微镜',
        'Camera': '相机',
        'Gift Card': '礼品卡',
        'Coffee': '咖啡',
        'Tea': '茶',
        'Energy Drink': '能量饮料',
        'Protein': '蛋白',
        'Shake': '奶昔',
        'Water': '水',
        'Juice': '果汁',
        'Fruit': '水果',
        'Battery': '电池',
        'Tire Inflator': '轮胎充气泵',
        'Jump Starter': '应急启动电源',
        'Motor Oil': '机油',
        'Air Filter': '滤芯',
        'Cleaner': '清洁剂',
        'Towel': '毛巾',
        'Tissue': '纸巾',
        'Toilet Paper': '卫生纸',
        'Paper Towel': '厨房纸',
        'Soap': '肥皂',
        'Shampoo': '洗发水',
        'Conditioner': '护发素',
        'Lotion': '乳液',
        'Cream': '霜',
        'Serum': '精华',
        'Vitamin': '维生素',
        'Supplement': '补充剂',
        'Electrolyte': '电解质',
        'Creatine': '肌酸',
        'Gloves': '手套',
        'Shirt': '衬衫',
        'T-Shirt': 'T恤',
        'Pants': '裤子',
        'Shorts': '短裤',
        'Shoes': '鞋子',
        'Sandals': '凉鞋',
        'Underwear': '内衣',
        'Bra': '文胸',
        'Socks': '袜子',
        'Hat': '帽子',
        'Bag': '包',
        'Backpack': '背包',
        'Wallet': '钱包',
        'Jewelry': '珠宝',
        'Necklace': '项链',
        'Ring': '戒指',
        'Earrings': '耳环',
        'Coin': '硬币',
        'Trading Card': '交易卡',
        'Comic': '漫画',
        'Toy': '玩具',
        'Game': '游戏',
        'Puzzle': '拼图',
        'Sticker': '贴纸',
        'Balloon': '气球',
        'Party': '派对',
        'Decoration': '装饰',
        'Gift': '礼物',
        'Candle': '蜡烛',
        'Fan': '风扇',
        'Heater': '加热器',
        'Humidifier': '加湿器',
        'Air Purifier': '空气净化器',
        'Vacuum': '吸尘器',
        'Mop': '拖把',
        'Broom': '扫帚',
        'Brush': '刷子',
        'Comb': '梳子',
        'Mirror': '镜子',
        'Scale': '秤',
        'Thermometer': '温度计',
        'Timer': '计时器',
        'Clock': '时钟',
        'Lamp': '灯',
        'Light': '灯',
        'Flashlight': '手电筒',
        'Tool': '工具',
        'Screwdriver': '螺丝刀',
        'Hammer': '锤子',
        'Wrench': '扳手',
        'Drill': '电钻',
        'Saw': '锯子',
        'Knife': '刀',
        'Cutting Board': '切菜板',
        'Pot': '锅',
        'Pan': '平底锅',
        'Blender': '搅拌机',
        'Mixer': '混合器',
        'Toaster': '烤面包机',
        'Coffee Maker': '咖啡机',
        'Kettle': '水壶',
        'Oven': '烤箱',
        'Microwave': '微波炉',
        'Refrigerator': '冰箱',
        'Dishwasher': '洗碗机',
        'Washing Machine': '洗衣机',
        'Dryer': '烘干机',
        'Iron': '熨斗',
        'Sewing Machine': '缝纫机',
    }
    
    # 代际/版本关键词
    gen_patterns = [
        (r'(\d+)(?:st|nd|rd|th)\s+Generation', r'\1代'),
        (r'(\d+)(?:st|nd|rd|th)\s+Gen', r'\1代'),
        (r'Generation\s+(\d+)', r'\1代'),
        (r'Gen\s+(\d+)', r'\1代'),
        (r'Series\s+(\d+)', r'Series \1'),
        (r'Pro\s+Max', 'Pro Max'),
        (r'Pro\s+(\d+)', r'Pro \1'),
        (r'Book\s+(\d+)', r'\1'),
        (r'Vol\.?\s+(\d+)', r'\1卷'),
        (r'Season\s+(\d+)', r'第\1季'),
        (r'Part\s+(\d+)', r'\1'),
    ]
    
    short_name = name
    
    # 提取代际信息
    gen_suffix = ''
    for pattern, replacement in gen_patterns:
        match = re.search(pattern, name, re.IGNORECASE)
        if match:
            if replacement == r'\1代':
                gen_suffix = match.group(1) + '代'
            elif replacement == r'Series \1':
                gen_suffix = 'Series ' + match.group(1)
            elif replacement == r'Pro \1':
                gen_suffix = 'Pro ' + match.group(1)
            elif replacement == r'\1':
                gen_suffix = match.group(1)
            else:
                gen_suffix = match.group(0)
            break
    
    # 简化名称
    # 移除过多描述
    name_clean = re.sub(r'\s*[-–|]\s*.*$', '', name)  # 移除竖线/破折号后的内容
    name_clean = re.sub(r'\s*\([^)]*\)', '', name_clean)  # 移除括号内容
    name_clean = re.sub(r'\s*\[[^\]]*\]', '', name_clean)  # 移除方括号内容
    name_clean = re.sub(r',.*$', '', name_clean)  # 移除逗号后的内容
    name_clean = name_clean.strip()
    
    # 特殊处理一些常见模式
    # iPhone/iPad/MacBook
    if 'iPhone' in name:
        match = re.search(r'iPhone\s*(\d+(?:\s*Pro\s*Max|\s*Pro|\s*Plus|\s*e)?)', name, re.IGNORECASE)
        if match:
            model = match.group(1).strip()
            short_name = f'iPhone {model}'
            if gen_suffix:
                short_name += f' {gen_suffix}'
            return short_name[:15]
    
    if 'iPad' in name:
        match = re.search(r'iPad\s*(\d+-inch|\d+|\s*Pro|\s*Air|\s*mini)?', name, re.IGNORECASE)
        if match:
            model = match.group(1) if match.group(1) else ''
            short_name = f'iPad {model}'.strip()
            if gen_suffix:
                short_name += f' {gen_suffix}'
            return short_name[:15]
    
    if 'MacBook' in name:
        match = re.search(r'MacBook\s*(Air|Pro)\s*(\d+-inch)?', name, re.IGNORECASE)
        if match:
            model = match.group(1)
            inch = match.group(2) if match.group(2) else ''
            chip_match = re.search(r'(M\d+|A\d+)', name)
            chip = chip_match.group(1) if chip_match else ''
            short_name = f'苹果MacBook {model} {inch} {chip}'.strip()
            return short_name[:15]
    
    if 'AirPods' in name:
        match = re.search(r'AirPods\s*(Pro\s*)?(\d+)?', name, re.IGNORECASE)
        if match:
            pro = 'Pro ' if match.group(1) else ''
            gen = match.group(2) if match.group(2) else ''
            short_name = f'苹果AirPods {pro}{gen}代'.strip()
            return short_name[:15]
    
    if 'AirTag' in name:
        gen = re.search(r'(\d+)(?:st|nd|rd|th)\s*Generation', name, re.IGNORECASE)
        gen_num = gen.group(1) if gen else ''
        short_name = f'苹果AirTag {gen_num}代'.strip()
        return short_name[:15]
    
    if 'Watch' in name and 'Apple' in name:
        match = re.search(r'Watch\s*Series\s*(\d+)', name, re.IGNORECASE)
        if match:
            short_name = f'苹果Watch Series {match.group(1)}'
            return short_name[:15]
    
    # Gift Cards
    if 'Gift Card' in name or 'gift card' in name:
        brand = ''
        for b in ['Amazon', 'Apple', 'Google Play', 'Visa', 'DoorDash', 'Uber', 'Starbucks', 'PlayStation', 'Xbox', 'Nintendo', 'Roblox', 'Luna']:
            if b.lower() in name.lower():
                brand = b
                break
        if brand:
            if 'Physical' in name:
                short_name = f'{brand}实体礼品卡'
            elif 'Printable' in name or 'Print' in name:
                short_name = f'{brand}可打印礼品卡'
            else:
                short_name = f'{brand}电子礼品卡'
            return short_name[:15]
    
    # 婴儿用品
    if 'Diaper' in name or 'Diapers' in name:
        for brand in ['Pampers', 'Huggies', 'Honest']:
            if brand.lower() in name.lower():
                if 'Swim' in name:
                    return f'{brand}泳裤'[:15]
                if 'Training' in name:
                    return f'{brand}训练裤'[:15]
                return f'{brand}纸尿裤'[:15]
    
    if 'Baby Wipes' in name or 'Wipes' in name:
        for brand in ['Huggies', 'Pampers', 'Honest', 'WaterWipes']:
            if brand.lower() in name.lower():
                return f'{brand}婴儿湿巾'[:15]
    
    # 书籍
    if any(x in name for x in ['Novel', 'Book', 'Edition']):
        # 提取书名
        title_match = re.match(r'^([A-Za-z\s\':]+?)(?:\s*[:–-]|\s*\(|\s*,|\s+Book|\s+Novel)', name)
        if title_match:
            title = title_match.group(1).strip()
            if len(title) > 12:
                title = title[:12]
            return title[:15]
        return name_clean[:15]
    
    # 游戏和应用
    if any(x in name for x in ['Game', 'Simulator', 'Dash', 'Run', 'Race', 'Clash']):
        # 提取游戏名
        title = name_clean.split(':')[0].strip()
        if len(title) > 12:
            title = title[:12]
        return title[:15]
    
    # 黑胶唱片
    if 'LP' in name or 'Vinyl' in name:
        title = name_clean.replace('LP', '').replace('Vinyl', '').strip()
        if len(title) > 12:
            title = title[:12]
        return f'{title}黑胶'[:15]
    
    # 默认处理：提取品牌+产品类型
    result = ''
    
    # 检查品牌
    for eng, chn in brand_map.items():
        if eng.lower() in name.lower():
            result = chn
            break
    
    # 检查产品类型
    for eng, chn in product_keywords.items():
        if eng.lower() in name.lower():
            if result:
                result += chn
            else:
                result = chn
            break
    
    if result:
        if gen_suffix:
            result += gen_suffix
        return result[:15]
    
    # 如果没有匹配到任何规则，返回清理后的名称
    if len(name_clean) > 15:
        # 尝试提取前几个单词
        words = name_clean.split()
        if len(words) >= 2:
            result = ' '.join(words[:2])
        else:
            result = name_clean[:15]
    else:
        result = name_clean
    
    return result[:15]

# 读取数据库
conn = sqlite3.connect('data/product_master.db')
cursor = conn.execute('SELECT ecom_code, name FROM product_master WHERE short_name IS NULL')
items = []
for r in cursor.fetchall():
    short_name = translate_name(r[1])
    items.append({'id': r[0], 'short_name': short_name})

# 保存结果
result = {
    'batch_id': '09bb0ea4-c765-493f-97b9-8838d0f7a163',
    'items': items
}

with open('data/name_processing/processed_names.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f'Processed {len(items)} items')
print('Sample output:')
for i in items[:10]:
    print(f'  {i}')
