#!/usr/bin/env python3
"""翻译商品名称 - 完整版"""
import json
import re

# 读取待处理文件
with open(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

batch_id = data['batch_id']
items = data['items']

def translate_name(name):
    name = name.strip()
    original = name
    
    # ===== 特殊规则（完全匹配）=====
    SPECIAL = {
        # 电影/蓝光
        'The People vs. Larry Flynt {Limited Edition] [4K Ultra HD]': 'Larry Flynt 4K限量版',
        'Billy Joel: The 100th: Live at Madison Square': 'Billy Joel演唱会蓝光',
        'Ju-On: The Grudge [Limited Edition] [4K Ultra HD]': '咒怨4K限量版',
        'Avatar: Fire And Ash': '阿凡达：火与灰烬',
        'Cartoon Network: Over the Garden Wall S1 (Blu-ray)': '花园墙外第一季蓝光',
        'Karaoke Machine': '卡拉OK机',
        
        # 麦克风/音频
        'Hollyland Lark A1 Wireless Microphone for iPhone & Android': 'Hollyland无线麦克风',
        'OneOdio Wired Over Ear Headphones Hi-Res Studio': 'OneOdio有线监听耳机',
        'Amazon Basics XLR Male to Female Microphone Cable': '亚马逊XLR麦克风线',
        'MAYBESTA Wireless Mini Microphone for iPhone, Android Phone': 'MAYBESTA无线迷你麦克风',
        'Wireless Mini Microphone for iPhone, Android': '无线迷你麦克风',
        'DJI Mic Mini (2 TX + 1 Mobile RX)': 'DJI Mic Mini麦克风套装',
        'FIFINE USB/XLR Dynamic Microphone for Podcast Recording': 'FIFINE播客麦克风',
        'Bubble Machine': '泡泡机',
        
        # 音乐设备
        'Amazon Basics Portable Adjustable Folding Guitar': '亚马逊折叠吉他架',
        'UGREEN USB B to USB C 6 FT Printer Cable': 'UGREEN打印机数据线',
        'WINGO Guitar Capo for Acoustic and Electric Guitars': 'WINGO吉他变调夹',
        
        # 办公用品
        'Amazon Basics Multipurpose Copy Printer Paper': '亚马逊打印纸',
        'HP 67 Black/Tri-Color Ink Cartridges (2-Pack)': 'HP 67墨盒套装',
        'HP Printer Paper': 'HP打印纸',
        'HP 64 Black & Tri-Color Ink Cartridges Printers (Combo Pack)': 'HP 64墨盒套装',
        'Sharpie Permanent Markers, Fine Tip, Black': 'Sharpie黑色记号笔',
        'Scotch Heavy Duty Shipping Packing Tape, Clear': 'Scotch透明封箱胶带',
        'Amazon Basics Sheet Protectors for 3 Ring Binder': '亚马逊文件保护套',
        'Amazon Basics Clear Thermal Laminating Sheets for': '亚马逊塑封膜',
        'EZlifego Double Sided Tape Heavy Duty': 'EZlifego强力双面胶',
        'Scotch Heavy Duty Shipping Packing Tape': 'Scotch封箱胶带',
        'Scotch Magic Tape': 'Scotch隐形胶带',
        'Amazon Basics Sturdy File Folders with Reinforced': '亚马逊文件夹',
        'Aothia Non-Slip Waterproof PU Leather Desk Pad': 'Aothia防水桌垫',
        'Hammermill Printer Paper': 'Hammermill打印纸',
        'HP 67XL Black High-Yield Ink Cartridge': 'HP 67XL黑色墨盒',
        'BIC Round Stic Xtra Life Ballpoint Pen': 'BIC圆珠笔',
        'Ddaowanx Gel Pens': 'Ddaowanx中性笔',
        'HP 62 Black Ink Cartridge': 'HP 62黑色墨盒',
        'Amazon Basics Wide Ruled Lined Writing Note Pads': '亚马逊记事本',
        
        # 园艺/宠物
        "Wagner's 53002 Farmer's Delight Wild Bird Food": 'Wagner野生鸟食',
        'Ortho Home Defense Insect Killer for Indoor and': 'Ortho室内杀虫剂',
        "Bonide Captain Jack's Neem Oil": 'Bonide印楝油',
        'Kaytee Hummingbird ElectroNectar Wild Bird Food': 'Kaytee蜂鸟花蜜',
        'UDC Parts GX20072 John Deere': 'John Deere配件',
        'Miracle-Gro Water Soluble All Purpose Plant Food': 'Miracle-Gro植物肥料',
        'First Saturday Lime Insect Deterrent': '石灰杀虫剂',
        'AUTOMAN-Garden-Hose-Nozzle': '花园水管喷嘴',
        "Roundup Weed and Grass Killer₄ with Pump 'N Go 2 Sprayer": 'Roundup除草剂套装',
        'Zevo 2 Flying Insect Traps & 2 Refill Cartridges': 'Zevo飞虫诱捕器套装',
        'Spruce Weed Killer Refill': '除草剂补充装',
        'HTH 52036R Pool Care Shock Advanced, Swimming Pool Chemical': 'HTH泳池消毒剂',
        "Dr. Elsey's Ultra UnScented Clumping Clay Cat Litter": "Dr. Elsey's猫砂",
        'Purina Fancy Feast Gravy Lovers Poultry and Beef': 'Purina猫粮',
        
        # 游戏/收藏
        '2026 Topps Disney Pristine Baseball': '2026迪士尼卡片',
        '2021 Topps Garbage Pail Kids': '2021 Garbage Pail Kids卡',
        'JLA/Avengers #1': 'JLA/Avengers漫画',
        'Lincoln Wheat C': '林肯小麦便士',
        'DD-214 Veteran ': '退伍军人纪念币',
        '250 Anniversary': '250周年纪念币',
        
        # 其他
        'havit HV-F2056 ': 'havit笔记本散热垫',
        'Apple电脑': '苹果电脑',
        'Fujifilm, Insta': '富士Instax相机',
        'Oura 戒指 5 Sizin': 'Oura智能戒指5',
        'Monster茶': 'Monster茶饮',
        'OEAK文胸': 'OEAK文胸',
        'Zeagoo Womens T': 'Zeagoo女士T恤',
    }
    
    # 检查完全匹配
    if name in SPECIAL:
        return SPECIAL[name]
    
    # ===== 部分匹配规则 =====
    
    # 电影/蓝光
    if '[4K Ultra HD]' in name or '[Blu-ray]' in name:
        # 提取电影名
        title = name.split('[')[0].strip()
        if 'Limited Edition' in name:
            return f'{title[:10]}4K限量版'
        return f'{title[:12]}蓝光'
    
    # 麦克风
    if 'Microphone' in name:
        if 'Wireless' in name:
            return '无线麦克风'
        if 'Mini' in name:
            return '迷你麦克风'
        return '麦克风'
    
    # 耳机
    if 'Headphones' in name or 'Headphone' in name:
        if 'Over Ear' in name:
            return '头戴式耳机'
        if 'Wireless' in name:
            return '无线耳机'
        return '耳机'
    
    # 墨盒
    if 'Ink Cartridge' in name:
        brand = ''
        if 'HP' in name:
            brand = 'HP '
        if 'Black' in name and 'Color' in name:
            return f'{brand}墨盒套装'
        if 'XL' in name:
            return f'{brand}大容量墨盒'
        return f'{brand}墨盒'
    
    # 打印纸
    if 'Printer Paper' in name:
        brand = name.split()[0] if name.split() else ''
        return f'{brand}打印纸' if brand else '打印纸'
    
    # 胶带
    if 'Tape' in name:
        if 'Double Sided' in name:
            return '双面胶'
        if 'Packing' in name or 'Shipping' in name:
            return '封箱胶带'
        if 'Magic' in name:
            return '隐形胶带'
        return '胶带'
    
    # 记号笔/笔
    if 'Marker' in name or 'Pen' in name:
        if 'Permanent' in name:
            return '记号笔'
        if 'Gel' in name:
            return '中性笔'
        if 'Ballpoint' in name:
            return '圆珠笔'
        return '笔'
    
    # 鸟食/宠物食品
    if 'Bird Food' in name:
        return '鸟食'
    if 'Cat Litter' in name:
        return '猫砂'
    if 'Cat Food' in name or 'Purina' in name:
        return '猫粮'
    if 'Dog Food' in name:
        return '狗粮'
    
    # 杀虫剂/除草剂
    if 'Insect Killer' in name or 'Insect Deterrent' in name:
        return '杀虫剂'
    if 'Weed Killer' in name:
        return '除草剂'
    
    # 园艺用品
    if 'Plant Food' in name or 'Fertilizer' in name:
        return '植物肥料'
    if 'Garden Hose' in name:
        return '花园水管'
    
    # 泳池用品
    if 'Pool' in name:
        if 'Chemical' in name:
            return '泳池化学品'
        return '泳池用品'
    
    # 吉他配件
    if 'Guitar' in name:
        if 'Capo' in name:
            return '吉他变调夹'
        if 'Stand' in name:
            return '吉他架'
        if 'String' in name:
            return '吉他弦'
        return '吉他配件'
    
    # 数据线
    if 'Cable' in name:
        if 'USB' in name:
            return 'USB数据线'
        if 'Printer' in name:
            return '打印机线'
        return '数据线'
    
    # 办公用品
    if 'File Folder' in name:
        return '文件夹'
    if 'Note Pad' in name or 'Notebook' in name:
        return '记事本'
    if 'Laminating' in name:
        return '塑封膜'
    if 'Sheet Protector' in name:
        return '文件保护套'
    if 'Desk Pad' in name:
        return '桌垫'
    
    # 桌面/电脑配件
    if 'Laptop Stand' in name or 'Notebook Stand' in name:
        return '笔记本支架'
    if 'Cooling' in name:
        return '散热垫'
    
    # 相机/摄影
    if 'Instax' in name:
        return 'Instax相机'
    if 'Camera' in name:
        return '相机'
    
    # 智能设备
    if 'Oura' in name:
        return 'Oura智能戒指'
    if 'Smart Ring' in name:
        return '智能戒指'
    
    # 卡片/收藏品
    if 'Topps' in name:
        return f'{name[:20]}卡片'
    if 'Trading Card' in name:
        return '交易卡'
    if 'Coin' in name and 'Collector' in name:
        return '收藏币'
    
    # 纪念币
    if 'Wheat' in name and ('Penny' in name or 'Cent' in name):
        return '小麦便士'
    if 'Veteran' in name:
        return '退伍军人纪念品'
    if 'Anniversary' in name and 'Coin' in name:
        return '周年纪念币'
    
    # 服装
    if 'Womens' in name or "Women's" in name:
        if 'T-Shirt' in name or 'T Shirt' in name:
            return '女士T恤'
        if 'Dress' in name:
            return '女士连衣裙'
        if 'Bra' in name:
            return '文胸'
        return '女士服装'
    if 'Mens' in name or "Men's" in name:
        if 'T-Shirt' in name or 'T Shirt' in name:
            return '男士T恤'
        return '男士服装'
    
    # 饮料
    if 'Monster' in name and 'Energy' in name:
        return 'Monster能量饮料'
    if 'Tea' in name and 'Drink' in name:
        return '茶饮料'
    
    # ===== 品牌名处理 =====
    BRANDS = [
        'INSIGNIA', 'Ring', 'Apple', 'iPhone', 'Nintendo', 'PlayStation', 'XBOX',
        'Logitech', 'Razer', 'Turtle Beach', 'amFilm', 'BTS', 'Vortex', 'Hontry',
        'Medicube', 'eos', 'Huggies', 'Pampers', 'WaterWipes', "Dr. Brown's",
        'Amazon Basics', 'Amazon', 'HP', 'Sharpie', 'Scotch', 'BIC', 'Hammermill',
        'Hollyland', 'OneOdio', 'MAYBESTA', 'DJI', 'FIFINE', 'UGREEN', 'WINGO',
        'Ortho', 'Bonide', 'Kaytee', 'Miracle-Gro', 'Roundup', 'Zevo', 'HTH',
        "Dr. Elsey's", 'Purina', 'Oura', 'Fujifilm', 'Instax', 'havit'
    ]
    
    # 提取品牌
    brand_found = None
    for brand in sorted(BRANDS, key=len, reverse=True):
        if brand.lower() in name.lower():
            brand_found = brand
            break
    
    # ===== 通用翻译 =====
    # 产品类型翻译词典
    TYPE_MAP = {
        'TV': '电视', 'Television': '电视', 'Monitor': '显示器',
        'Headphones': '耳机', 'Earbuds': '耳机', 'Speaker': '音箱',
        'Phone': '手机', 'Tablet': '平板', 'Laptop': '笔记本',
        'Camera': '相机', 'Watch': '手表', 'Ring': '戒指',
        'Battery': '电池', 'Charger': '充电器', 'Cable': '数据线',
        'Ice Maker': '制冰机', 'Dehumidifier': '除湿机',
        'Vacuum': '吸尘器', 'Blender': '搅拌机', 'Fan': '风扇',
        'Diapers': '纸尿裤', 'Wipes': '湿巾',
        'Shampoo': '洗发水', 'Lotion': '乳液', 'Cream': '霜',
        'T-Shirt': 'T恤', 'Shirt': '衬衫', 'Pants': '裤子', 'Shoes': '鞋子',
        'Game': '游戏', 'Album': '专辑', 'Book': '书',
        'Gift Card': '礼品卡', 'Card': '卡',
        'Coin': '硬币', 'Toy': '玩具', 'Tool': '工具', 'Kit': '套装',
    }
    
    # 应用类型翻译
    translated = name
    for eng, chn in sorted(TYPE_MAP.items(), key=lambda x: -len(x[0])):
        if eng.lower() in translated.lower():
            translated = re.sub(re.escape(eng), chn, translated, flags=re.IGNORECASE)
            break
    
    # 如果翻译后与原文差别不大，使用品牌+类型
    if translated == name and brand_found:
        for eng, chn in TYPE_MAP.items():
            if eng.lower() in name.lower():
                return f'{brand_found}{chn}'
        return f'{brand_found}产品'
    
    # 清理并截断
    translated = ' '.join(translated.split())
    if len(translated) > 15:
        translated = translated[:15]
    
    return translated if translated and translated != name else name[:15]

# 翻译所有项目
translated_items = []
for item in items:
    short_name = translate_name(item['name'])
    translated_items.append({
        'id': item['id'],
        'short_name': short_name
    })

# 保存结果
result = {
    'batch_id': batch_id,
    'items': translated_items
}

output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\processed_names.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f'Translated {len(translated_items)} items')
print(f'Saved to {output_path}')

# 显示翻译示例
print('\nSample translations:')
for i in range(min(15, len(translated_items))):
    orig = items[i]['name'][:45] + '...' if len(items[i]['name']) > 45 else items[i]['name']
    trans = translated_items[i]['short_name']
    print(f'  {orig}')
    print(f'    -> {trans}')
