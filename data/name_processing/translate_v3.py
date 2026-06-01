#!/usr/bin/env python3
"""商品名称翻译脚本 - 简洁版"""
import json
import re

# 读取待翻译文件
with open(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def translate_item(item):
    id, name = item['id'], item['name']
    
    # 品牌名保留列表
    brands = ['Apple', 'Samsung', 'Sony', 'Nike', 'Adidas', 'Crocs', 'Vortex', 'Anker', 'TP-Link', 'medicube', 'GAOY', 'Hanes', 'Gildan', 'Wrangler', 'Huggies', 'Pampers', 'NOCO', 'Valvoline', 'Mobil', 'Meguiar', 'Chemical Guys', 'Bounty', 'Scott', 'Charmin', 'STANLEY', 'KitchenAid', 'Ninja', 'Roku', 'JLab', 'TAGRY', 'Hollyland', 'Fujifilm', 'Instax', 'EltaMD', 'Neutrogena', 'PanOxyl', 'BIODANCE', 'Paula', 'The Ordinary', 'Mighty Patch', 'eos', 'Amazon Basics', 'Minecraft', 'Geometry', 'Hontry', 'Elikliv', 'Aurosports', 'Gskyer', 'SUPFINE', 'FNTCASE', 'Miracase', 'TOCOL', 'Ailun', 'INIU', 'Hiearcool', 'COOFANDY', 'OEAK', 'AUTOMET', 'Carhartt', 'ANRABESS', 'CHICME', 'KuaiLu', 'OFEEFAN', 'COCOMARTS', 'CELSIUS', 'Nespresso', 'Premier', 'Monster', 'Naturesweet', 'DaVinci', 'Sparkling', 'Core Power', 'Bloom', 'Lavazza', 'Hearth', 'Sereney', 'Sensemory', 'Tallowbourn', 'MAMAGIFTREE', 'Sweet Water', 'Opal', 'LUCKYJEWUS', 'Lipfidence', 'Hstyle', 'PEALICIOUS', 'Angel Soft', 'Dixie', 'Quilted Northern', 'Miss Mouth', 'Optimum Nutrition', 'Liquid I.V.', 'Terro', 'Owala', 'Zevo', 'HOME GROWN', 'Summit', 'Barossa', 'Niagara', 'BEDLORE', 'Chapin', 'Utopia', 'Zulay', 'BigFoot', 'Supmedic', 'MedPride', 'Gorilla', 'Molly', 'Inspire', 'Fygrip', 'Cozy', 'FifthPulse', 'Swihauk', 'Tork', 'Loctite', 'DIYMAG', 'VELCRO', 'Etekcity', 'HydroJug', 'Alpha Grillers', 'bella', 'KitchenAid', 'Homaxy', 'TrendPlain', 'Reynolds', 'TempPro', 'Socomi', 'Labstandard', 'Ernie Ball', 'DJI', 'OneOdio', 'MAYBESTA', 'FIFINE', 'Focusrite', 'DAddario', 'Jim Dunlop', 'HP', 'Sharpie', 'Scotch', 'Hammermill', 'BIC', 'Aothia', 'Ddaowanx', 'Ortho', 'Wagner', 'Bonide', 'Kaytee', 'UDC Parts', 'Miracle-Gro', 'First Saturday', 'AUTOMAN', 'Roundup', 'Safer Home', 'TERRO', 'Dr. Elsey', 'Purina', 'Earth Rated', 'Greenies', 'Fresh Step', 'INABA', 'Blue Buffalo', 'FortiFlora', 'HONEY CARE', 'Sheba', 'Pur Luv', 'Milk-Bone', 'Temptations', 'ARM & HAMMER', 'Pedigree', 'TurboTax', 'Microsoft Office', 'Norton', 'McAfee', 'H&R Block', 'Windows', 'Bitdefender', 'NordVPN', 'Mullvad', 'Webroot', 'Quicken', 'Wyze', 'Malwarebytes', 'Rainleaf', 'Callaway', 'Speedo', 'Fit Simplify', 'HEETA', 'IDAODAN', 'goodr', 'NOCO']
    
    # 产品类型关键词翻译
    product_types = {
        'Chest Freezer': '卧式冰柜', 'Freezer': '冰柜',
        'Binoculars': '双筒望远镜', 'Telescope': '天文望远镜', 'Microscope': '显微镜',
        'Game': '游戏', 'Adventure': '冒险', 'Racing': '竞速', 'Simulator': '模拟',
        'Essential Oil': '精油', 'Marker': '马克笔', 'Paint': '颜料', 'Tape': '胶带', 'Glue': '胶水', 'Scissors': '剪刀', 'Yarn': '毛线', 'Kit': '套装',
        'Novel': '小说', 'Book': '书', 'Edition': '版',
        'Motor Oil': '机油', 'Air Filter': '滤芯', 'Tire Inflator': '充气泵', 'Jump Starter': '启动电源', 'Battery Charger': '充电器', 'Sunshade': '遮阳板', 'Car Mount': '车载支架', 'Air Freshener': '香薰',
        'Diapers': '纸尿裤', 'Wipes': '湿巾', 'Baby Wipes': '婴儿湿巾', 'Shampoo': '洗发', 'Body Wash': '沐浴露', 'Training Pants': '训练裤', 'Thermometer': '体温计', 'Fan': '风扇', 'Bottle': '奶瓶',
        'Toner Pads': '爽肤棉片', 'Body Lotion': '身体乳', 'Patch': '贴', 'Cotton Swabs': '棉签', 'Makeup Remover': '卸妆', 'Mask': '面膜', 'Hand Soap': '洗手液', 'Sunscreen': '防晒霜', 'Face Wash': '洗面奶', 'Towel': '毛巾', 'Mascara': '睫毛膏', 'Body Wash': '沐浴露', 'Lip Balm': '唇膏', 'Lip Cream': '唇膏', 'Nail': '指甲', 'Nose Ring': '鼻钉',
        'Album': '专辑', 'LP': '唱片', 'CD': 'CD',
        'Case': '手机壳', 'Screen Protector': '钢化膜', 'Privacy Screen': '防窥膜', 'Charger': '充电器', 'Power Bank': '移动电源', 'Phone Pouch': '手机袋', 'Data Cable': '数据线',
        'Underwear': '内裤', 'Bra': '内衣', 'T-Shirt': 'T恤', 'Shirt': '衬衫', 'Tank Top': '背心', 'Nipple Cover': '乳贴', 'Clog': '洞洞鞋', 'Shoes': '鞋', 'Shorts': '短裤', 'Flip Flops': '人字拖', 'Socks': '袜子',
        'Coin': '硬币', 'Bill': '钞票', 'Penny': '分币', 'Dime': '银币', 'Silver Dollar': '银币',
        'Laptop': '笔记本电脑', 'Router': '路由器', 'Hub': '扩展坞', 'Docking Station': '扩展坞', 'Stand': '支架', 'Earbuds': '耳机', 'Headphones': '耳机', 'Watch': '手表', 'Tablet': '平板', 'Streaming Stick': '流媒体棒', 'Remote': '遥控器', 'Surge Protector': '浪涌保护', 'Film': '相纸',
        'Gift Card': '礼品卡', 'eGift Card': '电子礼品卡',
        'Protein Shake': '蛋白奶昔', 'Energy Drink': '能量饮料', 'Coffee': '咖啡', 'Capsules': '胶囊', 'Banana': '香蕉', 'Blueberries': '蓝莓', 'Avocado': '牛油果', 'Strawberries': '草莓', 'Gum': '口香糖',
        'Toy': '玩具', 'Gift': '礼物', 'Keychain': '钥匙扣', 'Card': '卡', 'Candle': '蜡烛',
        'Paper Towels': '厨房纸巾', 'Toilet Paper': '卫生纸', 'Batteries': '电池', 'Paper Plates': '纸盘', 'Electrolytes': '电解质', 'Flushable Wipes': '湿厕纸', 'Magnesium': '镁补充剂', 'Creatine': '肌酸', 'Ant Killer': '蚂蚁药', 'Sheet Set': '床单套装', 'Water Bottle': '水壶', 'Insect Trap': '飞虫诱捕器', 'Seeds': '种子', 'Mosquito': '蚊虫', 'Shower Curtain': '浴帘', 'Hanger': '衣架', 'Mattress Protector': '床垫保护套', 'Sprayer': '喷洒器', 'Pillow': '枕头', 'Milk Frother': '奶泡器', 'Gloves': '手套', 'Nitrile Gloves': '丁腈手套', 'Super Glue': '强力胶', 'Dishwasher Pods': '洗碗机清洁块', 'Vacuum Bag': '真空收纳袋', 'Hand Towel': '擦手纸', 'Lint Roller': '粘毛滚筒', 'Magnetic Hook': '磁性挂钩', 'Fastener': '魔术贴',
        'Kitchen Scale': '厨房秤', 'Tumbler': '保温杯', 'Meat Thermometer': '肉类温度计', 'Kitchen Shears': '厨房剪刀', 'Toaster': '烤面包机', 'Air Fryer': '空气炸锅', 'Can Opener': '开罐器', 'Dish Cloth': '洗碗布', 'Parchment Paper': '烘焙纸', 'Blender': '搅拌机', 'Table Runner': '桌旗',
        'Movie': '电影', '4K': '4K', 'DVD': 'DVD', 'Blu-ray': '蓝光',
        'Microphone': '麦克风', 'Guitar String': '吉他弦', 'Karaoke': '卡拉OK', 'Audio': '音频',
        'Paper': '纸', 'Ink': '墨盒', 'Marker': '马克笔', 'Pen': '笔', 'File Folder': '文件夹', 'Laminating': '塑封', 'Tape': '胶带', 'Note Pad': '笔记本',
        'Insect Killer': '杀虫剂', 'Plant Food': '植物肥料', 'Neem Oil': '印楝油', 'Bird Food': '鸟食', 'Garden Hose': '花园水管', 'Weed Killer': '除草剂', 'Fly Trap': '苍蝇诱捕器',
        'Cat Litter': '猫砂', 'Dog Pad': '狗垫', 'Cat Food': '猫粮', 'Dog Treat': '狗零食', 'Poop Bag': '粪便袋', 'Pill Pocket': '药丸袋', 'Pet Wipe': '宠物湿巾',
        'Tax Software': '税务软件', 'Security': '安全软件', 'VPN': 'VPN', 'Office': 'Office软件',
        'Weight Vest': '负重马甲', 'Dumbbell': '哑铃', 'Swim Goggles': '游泳眼镜', 'Resistance Band': '阻力带', 'Dry Bag': '防水袋', 'Golf Ball': '高尔夫球', 'Balloon Pump': '气球泵', 'Sunglasses': '太阳镜', 'Trading Card': '收藏卡', 'Sticker': '贴纸',
    }
    
    # 特定翻译规则
    special_rules = {
        'medicube Toner Pads Zero Pore Pad 2.0': 'medicube零毛孔爽肤棉片2.0',
        'Amazon Basics': 'Amazon Basics',
        'Apple AirTag': 'Apple AirTag',
        'Apple AirPods': 'Apple AirPods',
        'Apple iPad': 'Apple iPad',
        'Apple Watch': 'Apple Watch',
        'Apple MacBook': 'Apple MacBook',
        'Apple EarPods': 'Apple EarPods',
        'Huggies': '好奇',
        'Pampers': '帮宝适',
        'Crocs': 'Crocs',
        'NOCO': 'NOCO',
        'STANLEY': 'STANLEY',
        'The Deal': 'The Deal小说',
        'The Mistake': 'The Mistake小说',
        'The Score': 'The Score小说',
        'The Goal': 'The Goal小说',
        'The Legacy': 'The Legacy小说',
        'The Divorce': 'The Divorce小说',
        'Dungeon Crawler Carl': 'Dungeon Crawler Carl小说',
        'Project Hail Mary': 'Project Hail Mary科幻小说',
        'Harry Potter': '哈利波特',
        'Michael Jackson': 'Michael Jackson',
        'Thriller': 'Thriller专辑',
        'Red': 'Red专辑',
        'Back to Black': 'Back to Black专辑',
        'Rumours': 'Rumours专辑',
        'Abbey Road': 'Abbey Road专辑',
        'Currents': 'Currents专辑',
        'Fight Club': '搏击俱乐部',
        'Interstellar': '星际穿越',
        'The Very Hungry Caterpillar': '好饿的毛毛虫绘本',
        'The Rainbow Fish': '彩虹鱼绘本',
        'I Love You to the Moon and Back': '爱你到月球再回来绘本',
        "Oh, the Places You'll Go!": '你要去的地方绘本',
        'Minecraft': 'Minecraft游戏',
        'Geometry Dash': 'Geometry Dash游戏',
        'Star Wars': '星球大战',
        'Pokemon': '宝可梦',
        'Marvel': 'Marvel',
        'DC': 'DC',
        'Nintendo': 'Nintendo',
        'Xbox': 'Xbox',
        'PlayStation': 'PlayStation',
        'Roblox': 'Roblox',
        'Diet Coke': '健怡可乐',
        'DJI Mic': 'DJI麦克风',
        'FIFINE': 'FIFINE麦克风',
        'Focusrite': 'Focusrite音频接口',
    }
    
    # 检查特殊规则
    for key, value in special_rules.items():
        if key in name:
            # 保留品牌，翻译其他部分
            remaining = name.replace(key, '').strip()
            if remaining:
                return value + remaining.translate({
                    'Pro': 'Pro', 'Max': 'Max', 'Mini': 'Mini',
                    'Wireless': '无线', 'Earbuds': '耳机', 'Headphones': '耳机',
                    'Case': '手机壳', 'Charger': '充电器',
                })
            return value
    
    # 简化翻译：直接返回原名，因为大多是品牌名+产品类型
    # 检查是否主要是品牌名
    for brand in brands:
        if brand in name:
            # 翻译产品类型部分
            result = brand
            remaining = name.replace(brand, '').strip()
            for eng, cn in product_types.items():
                if eng in remaining:
                    result += cn
                    remaining = remaining.replace(eng, '').strip()
            if remaining and len(remaining) > 2:
                # 处理剩余部分
                remaining = remaining.replace(',', '').replace('-', '').replace('&', '').replace('(', '').replace(')', '').strip()
                if remaining:
                    result += remaining[:10]  # 截断过长的部分
            return result[:15] if len(result) > 15 else result
    
    # 默认返回截断的名称
    return name[:15] if len(name) > 15 else name

# 处理所有商品
processed_items = []
for item in data['items']:
    short_name = translate_item(item)
    processed_items.append({
        'id': item['id'],
        'short_name': short_name
    })

# 创建输出
output = {
    'batch_id': data['batch_id'],
    'items': processed_items
}

# 写入输出
with open(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\processed_names.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f'已翻译 {len(processed_items)} 条商品名称')