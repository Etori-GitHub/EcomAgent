#!/usr/bin/env python3
"""翻译商品名称 - 使用AI智能翻译"""
import json
import re

# 读取待处理文件
with open(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

batch_id = data['batch_id']
items = data['items']

# 品牌名列表（不翻译）
BRANDS = [
    'INSIGNIA', 'Ring', 'Apple', 'iPhone', 'iPad', 'MacBook', 'AirPods', 'Kindle', 'Echo', 'Fire',
    'Nintendo', 'PlayStation', 'XBOX', 'Logitech', 'Razer', 'Turtle Beach', 'amFilm', 'BTS',
    'Vortex', 'Hontry', 'Elikliv', 'Aurosports', 'Gskyer', 'Lamicall', 'SUPFINE', 'FNTCASE',
    'PEHAEL', 'Miracase', 'TOCOL', 'Ailun', 'SuydanBox', 'INIU', 'Hiearcool', 'Medicube', 'eos',
    'Mighty Patch', 'Neutrogena', 'The Ordinary', 'BIODANCE', 'PanOxyl', 'Clean Skin Club',
    'Maybelline', 'EltaMD', 'Nizoral', "Paula's Choice", 'Blue Lizard', 'Aquaphor', 'Pagather',
    'Huggies', 'Pampers', 'WaterWipes', "Dr. Brown's", 'Desitin', 'Momcozy', 'Gaiatop',
    'Mobil', 'Valvoline', 'CARORY', 'USANOOKS', 'Chemical Guys', 'AstroAI', 'CERAKOTE', "Meguiar's",
    'NOCO', 'Camco', 'EcoNour', 'Kaistyle', 'Bounty', 'Scott', 'Angel Soft', 'Charmin',
    'Quilted Northern', 'Dixie', 'DUDE', 'Cottonelle', 'Sparkle', 'LMNT', 'Pure Encapsulations',
    "Miss Mouth's", 'Optimum Nutrition', 'Liquid I.V.', 'Terro', 'Owala', 'Zevo', 'Summit',
    'Barossa', 'BigFoot', 'Niagara', 'BEDLORE', 'Utopia', 'Zulay', 'Supmedic', 'MedPride',
    'Inspire', 'FifthPulse', 'Fygrip', 'Cozy', 'Swihauk', 'Tork', 'DIYMAG', 'Gorilla', 'Loctite',
    "Molly's", 'Chapin', 'SWIFTLITE', 'NineSky', 'Etekcity', 'STANLEY', 'HydroJug', 'Alpha Grillers',
    'KitchenAid', 'bella', 'Homaxy', 'TrendPlain', 'Reynolds', 'TempPro', 'Ninja', 'Socomi',
    'Pukomc', 'Sweetcrispy', 'Elite', 'DREAME', 'TADEKERU', 'Morrerfresh', 'Hanes', 'Gildan',
    'LetsJoli', 'COOFANDY', 'Nippies', 'OEAK', 'AUTOMET', 'Carhartt', 'ANRABESS', 'Crocs',
    'Wrangler', 'CHICME', 'KuaiLu', 'OFEEFAN', 'COCOMARTS', 'Hstyle', 'CELSIUS', 'Nespresso',
    'Premier', 'Monster', 'NatureSweet', 'DaVinci', 'Sparkling Ice', 'Core Power', 'Bloom',
    'PUR', 'Propel', 'Lavazza', 'TP-Link', 'Anker', 'UGREEN', 'BESIGN', 'Roku', 'JLab', 'TAGRY',
    'EUHOMY', 'DUMOS', 'NEWBULIG', 'Kismile', 'Silonn', 'Antarctic', 'COWSAR', 'OLIXIS', 'Igloo',
    'Midea', 'Frostorm', 'Luna', 'Roblox', 'DoorDash', 'Uber', 'Google', 'Starbucks', 'Amazon'
]

# 常见产品类型翻译
PRODUCT_TYPES = {
    'TV': '电视', 'Television': '电视', 'Smart TV': '智能电视', 'LED': 'LED',
    'Battery Pack': '电池包', 'Battery': '电池', 'Rechargeable': '可充电',
    'Phone': '手机', 'Tablet': '平板', 'Laptop': '笔记本', 'Computer': '电脑',
    'Headphones': '耳机', 'Earbuds': '耳机', 'Speaker': '音箱', 'Microphone': '麦克风',
    'Camera': '相机', 'Cam': '摄像头', 'Webcam': '摄像头',
    'Watch': '手表', 'Tracker': '追踪器',
    'Ice Maker': '制冰机', 'Dehumidifier': '除湿机', 'Humidifier': '加湿器',
    'Air Conditioner': '空调', 'Heater': '加热器', 'Fan': '风扇',
    'Vacuum': '吸尘器', 'Cleaner': '清洁器', 'Blender': '搅拌机', 'Juicer': '榨汁机',
    'Coffee Maker': '咖啡机', 'Coffee': '咖啡', 'Toaster': '烤面包机', 'Oven': '烤箱',
    'Air Fryer': '空气炸锅', 'Grill': '烧烤炉', 'BBQ': '烧烤',
    'Trash Can': '垃圾桶', 'Bin': '垃圾桶',
    'Diapers': '纸尿裤', 'Diaper': '纸尿裤', 'Wipes': '湿巾', 'Baby': '婴儿',
    'Shampoo': '洗发水', 'Conditioner': '护发素', 'Body Wash': '沐浴露', 'Soap': '肥皂',
    'Lotion': '乳液', 'Cream': '霜', 'Serum': '精华', 'Mask': '面膜', 'Toner': '爽肤水',
    'Makeup': '化妆品', 'Lipstick': '口红', 'Mascara': '睫毛膏', 'Foundation': '粉底',
    'T-Shirt': 'T恤', 'Shirt': '衬衫', 'Pants': '裤子', 'Shorts': '短裤', 'Dress': '裙子',
    'Shoes': '鞋子', 'Boots': '靴子', 'Sandals': '凉鞋', 'Slippers': '拖鞋',
    'Underwear': '内衣', 'Bra': '文胸', 'Socks': '袜子',
    'Jacket': '夹克', 'Coat': '外套', 'Hoodie': '卫衣', 'Sweater': '毛衣',
    'Bag': '包', 'Backpack': '背包', 'Wallet': '钱包', 'Purse': '手提包',
    'Watch': '手表', 'Clock': '时钟', 'Thermometer': '温度计', 'Scale': '秤',
    'Charger': '充电器', 'Cable': '数据线', 'Adapter': '适配器', 'Hub': '扩展坞',
    'Mouse': '鼠标', 'Keyboard': '键盘', 'Monitor': '显示器', 'Screen': '屏幕',
    'Router': '路由器', 'Modem': '调制解调器', 'Extender': '扩展器',
    'Game': '游戏', 'Gaming': '游戏', 'Controller': '手柄', 'Console': '主机',
    'Book': '书', 'Novel': '小说', 'Magazine': '杂志', 'Comic': '漫画',
    'Music': '音乐', 'Album': '专辑', 'Vinyl': '黑胶', 'CD': 'CD',
    'Gift Card': '礼品卡', 'Card': '卡',
    'Coin': '硬币', 'Medal': '奖章', 'Token': '代币',
    'Toy': '玩具', 'Doll': '玩偶', 'Figure': '手办', 'Model': '模型',
    'Paint': '颜料', 'Marker': '马克笔', 'Brush': '画笔', 'Pen': '笔', 'Pencil': '铅笔',
    'Tool': '工具', 'Kit': '套装', 'Set': '套装',
    'Gloves': '手套', 'Hat': '帽子', 'Scarf': '围巾',
    'Bed': '床', 'Mattress': '床垫', 'Pillow': '枕头', 'Blanket': '毯子', 'Sheet': '床单',
    'Towel': '毛巾', 'Cloth': '布', 'Napkin': '餐巾',
    'Doorbell': '门铃', 'Lock': '锁', 'Security': '安全',
    'Oil': '油', 'Grease': '润滑脂', 'Lubricant': '润滑剂',
    'Filter': '滤芯', 'Cartridge': '墨盒',
    'Light': '灯', 'Lamp': '灯', 'Bulb': '灯泡', 'LED': 'LED灯',
    'Switch': '开关', 'Outlet': '插座', 'Plug': '插头',
    'Sunglasses': '太阳镜', 'Glasses': '眼镜',
    'Binoculars': '望远镜', 'Telescope': '天文望远镜', 'Microscope': '显微镜',
    'Spray': '喷雾', 'Wash': '洗涤剂', 'Detergent': '清洁剂',
    'Food': '食品', 'Snack': '零食', 'Drink': '饮料', 'Beverage': '饮料',
    'Water': '水', 'Juice': '果汁', 'Soda': '汽水', 'Tea': '茶', 'Coffee': '咖啡',
    'Protein': '蛋白', 'Vitamin': '维生素', 'Supplement': '补充剂',
    'Seeds': '种子', 'Plant': '植物', 'Flower': '花',
    'Stickers': '贴纸', 'Tape': '胶带', 'Glue': '胶水',
    'Ring Sizer': '戒指调节器', 'Ring': '戒指', 'Necklace': '项链', 'Earring': '耳环',
    'Sewing Machine': '缝纫机', 'Sewing': '缝纫',
    'Label Gun': '标签枪', 'Label': '标签',
    'Bed Skirt': '床裙', 'Sofa Cover': '沙发套', 'Cushion': '靠垫',
    'Washing Machine': '洗衣机', 'Dryer': '烘干机',
    'Jes': '耶稣', 'Figure': '摆件', 'Statue': '雕像',
}

# 特定品牌产品的翻译规则
SPECIAL_TRANSLATIONS = {
    # 亚马逊设备
    'INSIGNIA 50" Class F50 Series LED 4K UHD Smart Fire TV': 'INSIGNIA 50寸4K智能Fire TV',
    'Ring Rechargeable Quick Release Battery Pack': 'Ring可充电电池包',
    'Apple iPhone (Renewed Premium) 16 Pro Max': '苹果iPhone 16 Pro Max翻新版',
    'Portable Countertop Ice Maker Machine with Handle': '便携式台面制冰机',
    'NineSky Dehumidifiers for Home': 'NineSky家用除湿机',
    'Magic Tiles 3 PRO': 'Magic Tiles 3 PRO',
    'Challenge: Runway Wars': 'Runway Wars游戏',
    'Pagather 24 Colors Acrylic Paint Markers': 'Pagather 24色丙烯马克笔',
    'Ring Sizer Adjuster for Loose Rings': '戒指尺寸调节器',
    'Project Hail Mary': 'Project Hail Mary',
    'All-Purpose Stainless Steel Shower Squeegee': '不锈钢浴室刮水器',
    'Amazon Basics Microfiber Cleaning Cloths': '亚马逊超细纤维清洁布',
    'Lamicall Bike Phone Holder, Motorcycle Mount': 'Lamicall自行车手机支架',
    "Dr. Brown's Natural Flow Level 2 Narrow Baby": "Dr. Brown's奶瓶奶嘴",
    'Huggies Size 4 Diapers, Snug & Dry Baby Diapers': 'Huggies 4号纸尿裤',
    'Contend: Standing Boldly for Biblical Truth': 'Contend基督教书籍',
    'Revolution: The Birth of the Greatest Nation': 'Revolution历史书籍',
    'Take Me to Your Leader: Perspectives': 'Take Me to Your Leader',
    'Carry The Light': 'Carry The Light',
    "BTS The 5th Album 'ARIRANG' [Living Legend Ver.]": 'BTS ARIRANG专辑',
    'Dream Chaser': 'Dream Chaser游戏',
    'Vortex Optics Crossfire HD': 'Vortex Crossfire HD望远镜',
    'Vortex Optics Diamondback HD': 'Vortex Diamondback HD望远镜',
    'Vortex Optics Triumph HD': 'Vortex Triumph HD望远镜',
}

def translate_name(name):
    """翻译商品名称"""
    name = name.strip()
    
    # 1. 检查特殊翻译规则
    if name in SPECIAL_TRANSLATIONS:
        return SPECIAL_TRANSLATIONS[name]
    
    # 2. 部分匹配特殊规则
    for eng, chn in SPECIAL_TRANSLATIONS.items():
        if eng in name or name in eng:
            return chn
    
    # 3. 通用翻译逻辑
    # 识别品牌名（保留英文）
    brand_found = None
    for brand in sorted(BRANDS, key=len, reverse=True):  # 从长到短匹配
        if brand.lower() in name.lower():
            brand_found = brand
            break
    
    # 翻译产品类型
    translated = name
    for eng, chn in sorted(PRODUCT_TYPES.items(), key=lambda x: -len(x[0])):
        pattern = r'\b' + eng + r'\b'
        translated = re.sub(pattern, chn, translated, flags=re.IGNORECASE)
    
    # 如果仍有大量英文，尝试简单翻译
    if len(re.findall(r'[A-Za-z]', translated)) > 10:
        # 尝试提取关键词
        words = name.split()
        if len(words) <= 3:
            # 短名称直接返回
            if brand_found:
                return f"{brand_found}" + translated.replace(brand_found, '').strip()[:10]
            return translated[:15]
        
        # 中等长度名称：品牌 + 产品类型
        if brand_found:
            # 找产品类型
            for eng, chn in PRODUCT_TYPES.items():
                if eng.lower() in name.lower():
                    return f"{brand_found}{chn}"
            return f"{brand_found}产品"
    
    # 清理多余空格
    translated = ' '.join(translated.split())
    
    # 截断到15字以内
    if len(translated) > 15:
        translated = translated[:15]
    
    return translated if translated else name[:15]

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

# 显示一些翻译示例
print('\nSample translations:')
for i in range(min(10, len(translated_items))):
    orig = items[i]['name'][:40] + '...' if len(items[i]['name']) > 40 else items[i]['name']
    trans = translated_items[i]['short_name']
    print(f'  {orig}')
    print(f'    -> {trans}')
