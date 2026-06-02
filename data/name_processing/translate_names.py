#!/usr/bin/env python3
"""翻译商品名称"""
import json
import re

# 读取待处理文件
with open(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

batch_id = data['batch_id']
items = data['items']

def translate_name(name):
    name = name.strip()
    
    # ===== 新增规则 (2026-06-02) =====
    # INSIGNIA 电视
    if 'INSIGNIA' in name and 'Fire TV' in name: return 'INSIGNIA Fire TV 4K'
    if 'INSIGNIA' in name and 'TV' in name: return 'INSIGNIA智能电视'
    
    # Ring 配件
    if 'Ring Rechargeable Quick Release Battery' in name: return 'Ring可充电电池包'
    
    # iPhone 翻新版
    if 'iPhone (Renewed Premium) 16 Pro Max' in name: return '苹果iPhone 16 Pro Max翻新版'
    if 'iPhone (Renewed Premium) 16 Pro' in name: return '苹果iPhone 16 Pro翻新版'
    if 'iPhone (Renewed' in name: return '苹果iPhone翻新版'
    
    # 制冰机
    if 'Portable Countertop Ice Maker' in name: return '便携式制冰机'
    if 'Countertop Ice Maker' in name: return '台面制冰机'
    if 'Ice Maker' in name: return '制冰机'
    
    # 除湿机
    if 'NineSky Dehumidifiers' in name: return 'NineSky除湿机'
    if 'Dehumidifier' in name: return '除湿机'
    
    # 游戏
    if 'Magic Tiles 3 PRO' in name: return 'Magic Tiles 3 PRO'
    if 'Challenge: Runway Wars' in name: return 'Runway Wars游戏'
    if 'Dream Chaser' in name: return 'Dream Chaser游戏'
    
    # 工艺用品
    if 'Pagather' in name and 'Acrylic Paint' in name: return 'Pagather丙烯马克笔'
    if 'Acrylic Paint Markers' in name: return '丙烯马克笔'
    
    # 首饰配件
    if 'Ring Sizer Adjuster' in name: return '戒指尺寸调节器'
    
    # 书籍
    if 'Project Hail Mary' in name: return 'Project Hail Mary'
    if 'Contend:' in name: return 'Contend基督教书籍'
    if 'Revolution:' in name and 'Nation' in name: return 'Revolution历史书籍'
    if 'Take Me to Your Leader' in name: return 'Take Me to Your Leader'
    if 'Carry The Light' in name: return 'Carry The Light'
    
    # 音乐
    if "BTS The 5th Album" in name: return 'BTS ARIRANG专辑'
    if 'ARIRANG' in name: return 'BTS ARIRANG专辑'
    
    # 望远镜
    if 'Vortex Optics Crossfire HD' in name: return 'Vortex Crossfire HD望远镜'
    if 'Vortex Optics Diamondback HD' in name: return 'Vortex Diamondback HD望远镜'
    if 'Vortex Optics Triumph HD' in name: return 'Vortex Triumph HD望远镜'
    if 'Vortex' in name: return 'Vortex望远镜'
    
    # 家居清洁
    if 'All-Purpose Stainless Steel Shower Squeegee' in name: return '不锈钢浴室刮水器'
    if 'Shower Squeegee' in name: return '浴室刮水器'
    
    # 亚马逊基础
    if 'Amazon Basics Microfiber Cleaning Cloths' in name: return '亚马逊超细纤维清洁布'
    if 'Amazon Basics Microfiber' in name: return '亚马逊超细纤维布'
    
    # 手机配件
    if 'Lamicall Bike Phone Holder' in name: return 'Lamicall自行车手机支架'
    if 'Phone Holder' in name: return '手机支架'
    
    # 婴儿用品
    if "Dr. Brown's Natural Flow" in name: return "Dr. Brown's奶瓶奶嘴"
    if "Dr. Brown's" in name: return "Dr. Brown's婴儿用品"
    if 'Huggies Size 4 Diapers' in name: return 'Huggies 4号纸尿裤'
    if 'Huggies' in name: return 'Huggies纸尿裤'
    
    # 服装
    if 'OEAK' in name and 'Bra' in name: return 'OEAK文胸'
    if 'Zeagoo' in name: return 'Zeagoo女装'
    
    # 纪念币
    if '250 Anniversary' in name: return '250周年纪念币'
    if 'Lincoln Wheat' in name: return '林肯小麦便士'
    if 'DD-214 Veteran' in name: return '退伍军人纪念品'
    
    # 电子产品
    if 'havit HV-F2056' in name: return 'havit笔记本散热垫'
    if 'havit' in name: return 'havit散热器'
    if 'Apple' in name and 'Computer' in name: return '苹果电脑'
    if 'Fujifilm' in name: return '富士相机'
    if 'Instax' in name: return 'Instax相机'
    if 'Oura' in name: return 'Oura智能戒指'
    
    # 收藏卡
    if '2026 Topps Disney' in name: return '2026迪士尼卡片'
    if '2021 Topps Garbage' in name: return 'Garbage Pail Kids卡'
    if 'JLA/Avengers' in name: return 'JLA/Avengers漫画'
    
    # 饮料
    if 'Monster' in name and 'Tea' in name: return 'Monster茶饮'
    if 'Monster Energy' in name: return 'Monster能量饮料'
    
    # 电影/蓝光
    if 'The People vs. Larry Flynt' in name: return 'Larry Flynt 4K限量版'
    if 'Billy Joel: The 100th' in name: return 'Billy Joel演唱会蓝光'
    if 'Ju-On: The Grudge' in name: return '咒怨4K限量版'
    if 'Avatar: Fire And Ash' in name: return '阿凡达：火与灰烬'
    if 'Cartoon Network: Over the Garden Wall' in name: return '花园墙外蓝光'
    if 'Troy [Limited' in name: return '特洛伊限量版蓝光'
    if 'Identity [Limit' in name: return '身份之谜限量版'
    if 'Frozen Heart' in name: return '冰冻之心'
    if 'Wish You Were H' in name: return 'Wish You Were Here'
    if 'Limited Edition' in name and '4K' in name: return '4K限量版蓝光'
    if 'Limited Edition' in name: return '限量版蓝光'
    if '[Blu-ray]' in name: return name.split('[')[0].strip()[:10] + '蓝光'
    
    # 音频设备
    if 'Hollyland Lark A1' in name: return 'Hollyland无线麦克风'
    if 'OneOdio Wired Over Ear' in name: return 'OneOdio有线监听耳机'
    if 'Amazon Basics XLR' in name: return '亚马逊XLR麦克风线'
    if 'MAYBESTA Wireless Mini' in name: return 'MAYBESTA无线麦克风'
    if 'Wireless Mini Microphone' in name: return '无线迷你麦克风'
    if 'DJI Mic Mini' in name: return 'DJI Mic Mini麦克风'
    if 'FIFINE USB/XLR' in name: return 'FIFINE播客麦克风'
    if 'Karaoke Machine' in name: return '卡拉OK机'
    if 'Bubble Machine' in name: return '泡泡机'
    
    # 音乐设备
    if 'Amazon Basics Portable Adjustable Folding Guitar' in name: return '亚马逊折叠吉他架'
    if 'UGREEN USB B to USB C' in name: return 'UGREEN打印机线'
    if 'WINGO Guitar Capo' in name: return 'WINGO吉他变调夹'
    
    # 办公用品
    if 'Amazon Basics Multipurpose Copy Printer Paper' in name: return '亚马逊打印纸'
    if 'HP 67 Black/Tri-Color' in name: return 'HP 67墨盒套装'
    if 'HP Printer Paper' in name: return 'HP打印纸'
    if 'HP 64 Black & Tri-Color' in name: return 'HP 64墨盒套装'
    if 'Sharpie Permanent Markers' in name: return 'Sharpie记号笔'
    if 'Scotch Heavy Duty Shipping Packing Tape, Clear' in name: return 'Scotch透明封箱胶带'
    if 'Amazon Basics Sheet Protectors' in name: return '亚马逊文件保护套'
    if 'Amazon Basics Clear Thermal Laminating' in name: return '亚马逊塑封膜'
    if 'EZlifego Double Sided Tape' in name: return 'EZlifego双面胶'
    if 'Scotch Heavy Duty Shipping Packing Tape' in name: return 'Scotch封箱胶带'
    if 'Scotch Magic Tape' in name: return 'Scotch隐形胶带'
    if 'Amazon Basics Sturdy File Folders' in name: return '亚马逊文件夹'
    if 'Aothia Non-Slip' in name: return 'Aothia桌垫'
    if 'Hammermill Printer Paper' in name: return 'Hammermill打印纸'
    if 'HP 67XL Black' in name: return 'HP 67XL墨盒'
    if 'BIC Round Stic' in name: return 'BIC圆珠笔'
    if 'Ddaowanx Gel Pens' in name: return 'Ddaowanx中性笔'
    if 'HP 62 Black Ink' in name: return 'HP 62墨盒'
    if 'Amazon Basics Wide Ruled' in name: return '亚马逊记事本'
    
    # 园艺/宠物
    if "Wagner's 53002" in name: return "Wagner鸟食"
    if 'Ortho Home Defense' in name: return 'Ortho杀虫剂'
    if "Bonide Captain Jack's Neem Oil" in name: return 'Bonide印楝油'
    if 'Kaytee Hummingbird' in name: return 'Kaytee蜂鸟花蜜'
    if 'UDC Parts' in name: return 'John Deere配件'
    if 'Miracle-Gro Water Soluble' in name: return 'Miracle-Gro肥料'
    if 'First Saturday Lime' in name: return '石灰杀虫剂'
    if 'AUTOMAN-Garden-Hose' in name: return '花园水管喷嘴'
    if "Roundup Weed and Grass" in name: return 'Roundup除草剂套装'
    if 'Zevo 2 Flying Insect' in name: return 'Zevo飞虫诱捕器'
    if 'Spruce Weed Killer' in name: return '除草剂补充装'
    if 'HTH 52036R Pool Care' in name: return 'HTH泳池消毒剂'
    if "Dr. Elsey's Ultra" in name: return "Dr. Elsey's猫砂"
    if 'Purina Fancy Feast' in name: return 'Purina猫粮'
    
    # 宠物用品
    if 'Amazon Basics Leak-Proof Dog' in name: return '亚马逊狗狗尿垫'
    if 'Earth Rated Poop Bags' in name: return 'Earth Rated狗屎袋'
    if 'Greenies Pill Pockets' in name: return 'Greenies药片零食'
    if 'Fresh Step Odor Shield' in name: return 'Fresh Step猫砂'
    if 'INABA Churu Cat Treats' in name: return 'INABA猫零食'
    if 'Purina Pro Plan' in name: return 'Purina专业猫粮'
    if 'Blue Buffalo Life Protection' in name: return 'Blue Buffalo狗粮'
    if 'HONEY CARE All-Absorb' in name: return 'Honey Care狗狗尿垫'
    if 'Sheba Perfect Portions' in name: return 'Sheba猫粮'
    if 'Pur Luv Chicken Jerky' in name: return 'Pur Luv狗零食'
    if 'Earth Rated Pet Wipes' in name: return 'Earth Rated宠物湿巾'
    if 'Temptations Cat Treats' in name: return 'Temptations猫零食'
    if 'ARM & HAMMER Clump' in name: return 'ARM & HAMMER猫砂'
    if 'Milk-Bone Original' in name: return 'Milk-Bone狗饼干'
    if 'Blue Buffalo Health Bars' in name: return 'Blue Buffalo狗零食'
    if 'Pedigree Dentastix' in name: return 'Pedigree狗零食'
    if 'Amazon Basics Dog Poop' in name: return '亚马逊狗屎袋'
    if 'Milk-Bone Soft & Chewy' in name: return 'Milk-Bone软狗零食'
    
    # 软件
    if 'TurboTax Deluxe' in name: return 'TurboTax报税软件'
    if 'Microsoft Office Home' in name: return '微软Office家庭版'
    if 'Microsoft Office Home & Business' in name: return '微软Office家庭商务版'
    if 'Norton 360 Deluxe' in name: return 'Norton 360安全软件'
    if 'Norton 360 Premium' in name: return 'Norton 360高级版'
    if 'H&R Block Tax Software' in name: return 'H&R Block报税软件'
    if 'McAfee Total Protection' in name: return 'McAfee安全软件'
    if 'Bitdefender Total Security' in name: return 'Bitdefender安全软件'
    if 'Microsoft System Builder' in name: return '微软系统安装版'
    if 'Mullvad VPN' in name: return 'Mullvad VPN'
    if 'Windows 11 Pro Upgrade' in name: return 'Windows 11专业版'
    if 'NordVPN' in name: return 'NordVPN'
    if 'Wyze Security Plan' in name: return 'Wyze安全订阅'
    if 'Malwarebytes Premium' in name: return 'Malwarebytes安全软件'
    if 'Quicken Classic' in name: return 'Quicken财务软件'
    if 'Laplink PCmover' in name: return 'Laplink电脑迁移软件'
    
    # 运动器材
    if 'Seago Swim Goggles' in name: return 'Seago泳镜'
    if 'Amazon Basics Neoprene Dumbbell' in name: return '亚马逊哑铃'
    if 'Google Fitbit Air' in name: return 'Fitbit Air手表'
    if 'Zeerun Weighted Vest' in name: return 'Zeerun负重背心'
    if 'ZELUS Weighted Vest' in name: return 'ZELUS负重背心'
    if 'BAND-AID Brand Travel' in name: return 'Band-Aid便携急救包'
    if 'Rainleaf Microfiber Towel' in name: return 'Rainleaf速干毛巾'
    if 'Callaway Golf Supersoft' in name: return 'Callaway高尔夫球'
    if 'Speedo Kids\' Swim Goggles' in name: return 'Speedo儿童泳镜'
    if 'HEETA Dry Bag' in name: return 'HEETA防水袋'
    if 'Fit Simplify Resistance' in name: return 'Fit Simplify弹力带'
    if 'AEOCOO Puddle Float' in name: return 'AEOCOO儿童浮力背心'
    if 'IDAODAN Electric Balloon' in name: return 'IDAODAN电动充气泵'
    
    # 收藏卡
    if '2025-26 Topps Signature' in name: return '25-26 Topps签名篮球卡'
    if '2025-26 Topps Hoops' in name: return '25-26 Topps篮球卡'
    if '100 Vintage Baseball' in name: return '100张复古棒球卡'
    if '2024-25 Topps Chrome Basketball' in name: return '24-25 Topps篮球卡'
    if '2026 Topps Baseball' in name: return '2026 Topps棒球卡'
    if 'Jalen Brunson' in name: return 'Jalen Brunson球星卡'
    if '2025 Panini SCORE' in name: return '2025 Panini橄榄球卡'
    if '2025/26 Topps Match' in name: return '25-26 Topps足球卡'
    if 'High Cheese Baseball' in name: return '棒球神秘卡包'
    if '100 Vintage Football' in name: return '100张复古橄榄球卡'
    if '2023 Topps Series' in name: return '2023 Topps棒球卡'
    if '2025 Panini Donruss' in name: return '2025 Panini橄榄球卡'
    if 'Topps, Upper deck' in name: return '复古体育卡套装'
    if 'Upper Deck Series One Hockey' in name: return 'Upper Deck冰球卡'
    if '2025–26 Panini Absolute' in name: return '25-26 Panini橄榄球卡'
    if 'Upper Deck Hockey' in name: return 'Upper Deck冰球卡'
    if '2026 Soccer Trading' in name: return '2026足球卡'
    if 'Premier League 2026' in name: return '2026英超卡'
    if '2026 Bowman Baseball' in name: return '2026 Bowman棒球卡'
    if 'Pokemon Cards Collection' in name: return '宝可梦卡片套装'
    if 'Bicycle Standard Playing Cards' in name: return 'Bicycle扑克牌'
    
    # 滤芯
    if 'GE XWFE Refrigerator Water' in name: return 'GE冰箱滤芯'
    if 'Brita Plus Water Filter' in name: return 'Brita滤芯'
    if 'everydrop by Whirlpool' in name: return 'Whirlpool冰箱滤芯'
    if 'Samsung HAF-QIN' in name: return 'Samsung冰箱滤芯'
    if 'Brita Filter Replacements' in name: return 'Brita替换滤芯'
    if 'GE RPWFE Refrigerator' in name: return 'GE冰箱滤芯'
    if 'ZeroWater Official Replacement' in name: return 'ZeroWater滤芯'
    
    # 气球/派对用品
    if 'Bezente Assorted Rainbow' in name: return '彩虹气球套装'
    if 'PartyWoo Black Balloons' in name: return 'PartyWoo黑色气球'
    if 'PartySticks Glow Sticks' in name: return '荧光棒100支'
    
    # 玩具
    if 'Midou Slow Rising' in name: return '饺子捏捏乐'
    if 'Dumpling Squishy' in name: return '饺子捏捏乐'
    if 'CUPKIN Animals Habitat' in name: return 'CUPKIN儿童贴纸书'
    if 'Play Doh Modeling' in name: return 'Play-Doh彩泥10色'
    if 'SEREED Baby Balance' in name: return 'SEREED儿童平衡车'
    if 'Infinno Baby Wrist' in name: return 'Infinno婴儿手摇铃'
    if 'Bright Starts Oball' in name: return 'Bright Starts球'
    if 'Horizon Group USA Bluey' in name: return 'Bluey水画套装'
    if 'Step2 Rain Showers' in name: return 'Step2儿童水桌'
    if 'SkaterTrainers' in name: return '滑板训练器'
    if 'Joking Hazard' in name: return 'Joking Hazard卡牌游戏'
    if 'Kinsa Smart' in name: return 'Kinsa智能体温计'
    if '1MORE Triple Driver' in name: return '1MORE三单元耳机'
    if 'The Door Balancer' in name: return '门支撑器'
    if 'Promixx FORM Protein' in name: return 'Promixx摇摇杯'
    if 'KiddyCare Diaper Caddy' in name: return 'KiddyCare尿布收纳盒'
    if 'White Leaf Organic' in name: return 'White Leaf有机婴儿食品'
    if 'Supa Ant Canning' in name: return '罐头制作套装'
    if 'Fire Blanket' in name: return '灭火毯'
    if 'Inflatable Tanning Pool' in name: return '充气泳池浮床'
    
    # 食品
    if 'Rhythm Superfoods Beet' in name: return 'Rhythm有机薯片'
    
    # 游戏主机/配件
    if 'Nintendo Switch 2 System' in name: return 'Nintendo Switch 2主机'
    if 'PlayStation DualSense Edge' in name: return 'PlayStation Edge手柄'
    if 'PlayStation DualSense' in name: return 'PlayStation手柄'
    if 'XBOX Wireless Gaming' in name: return 'XBOX无线手柄'
    if 'XBOX Game Pass Ultimate' in name: return 'XBOX Game Pass'
    if 'Logitech G Driving Force' in name: return 'Logitech方向盘换挡器'
    if 'Logitech G502 Hero' in name: return 'Logitech G502鼠标'
    if 'Logitech G305 Lightspeed' in name: return 'Logitech G305鼠标'
    if 'Razer BlackShark V2 X' in name: return 'Razer BlackShark耳机'
    if 'Turtle Beach Stealth 500' in name: return 'Turtle Beach耳机'
    if 'amFilm Auto-Alignment' in name: return 'amFilm自动贴膜'
    
    # 游戏
    if 'Tomodachi Life' in name: return 'Tomodachi Life游戏'
    if 'Star Fox' in name: return 'Star Fox游戏'
    if '007 First Light' in name: return '007 First Light游戏'
    if 'Luna Premium' in name: return 'Luna Premium订阅'
    
    # 礼品卡
    if 'Nintendo eShop Gift' in name: return 'Nintendo礼品卡$10'
    if 'Xbox Gift Card' in name: return 'Xbox礼品卡$10'
    if 'PlayStation Store Gift' in name: return 'PlayStation礼品卡$10'
    if 'Roblox Digital Gift' in name: return 'Roblox礼品卡'
    
    # 家居装饰
    if 'RIVER OF GOODS' in name: return 'RIVER OF GOODS灯具'
    if 'Stained Glass Bird' in name: return '彩绘玻璃鸟灯'
    if 'Supa Ant 6x8ft' in name: return 'Supa Ant桌旗'
    
    # 喷漆
    if 'Rust-Oleum' in name: return 'Rust-Oleum喷漆'
    
    # TikTok 商品 (ECTK)
    if 'Punk Style Ripped Gloves' in name: return '朋克破洞手套'
    if '50Pcs Little Jesus Figures' in name: return '50件迷你耶稣摆件'
    if 'Pukomc Motion Sensor Trash' in name: return 'Pukomc感应垃圾桶'
    if 'Rechargeable Portable Mini Washing' in name: return '可充电迷你洗衣机'
    if 'Sweetcrispy 9QT Dual Basket Air Fryer' in name: return 'Sweetcrispy双篮炸锅'
    if 'Elite Cuisine 3-Cup Electric Citrus' in name: return 'Elite橙汁机'
    if 'Vacuum Duo Bundle' in name: return '吸尘器套装'
    if 'Cordless Blender' in name: return '无线搅拌机'
    if 'DREAME Aero Wet Dry' in name: return 'DREAME洗地机'
    if 'Faucet Leak-Proof Sealing' in name: return '防漏水龙头密封垫'
    if 'TADEKERU Mist Cooling' in name: return 'TADEKERU喷雾风扇'
    if 'Adjustable car fan' in name: return '车载风扇'
    if 'Morrerfresh Odor Eliminator' in name: return 'Morrerfresh除味器'
    if 'VEVOR Electric Roaster' in name: return 'VEVOR电烤炉'
    if 'USB Portable Blender' in name: return 'USB便携搅拌机'
    if 'Indoor Smokeless Electric Korean BBQ' in name: return '室内无烟韩式烧烤炉'
    if 'Floral Print Bed Skirt' in name: return '碎花床裙套装'
    if 'Clothing Label Gun' in name: return '服装标签枪套装'
    if 'Leaf Elastic Print Sofa' in name: return '树叶弹性沙发套'
    if 'Portable Handheld Sewing' in name: return '便携手持缝纫机'
    if 'Fluffy Queen Comforter' in name: return '蓬松四件套'
    if 'Egyptian Conform' in name: return '埃及棉四件套'
    if 'Marble Patterned Corridor' in name: return '大理石纹走廊地毯'
    if 'Lush Decor Cottage' in name: return 'Lush Decor床单'
    if 'Stitch Gun for Clothes' in name: return '缝纫枪'
    if 'Mosquito Repellent Sticks' in name: return '驱蚊香'
    if 'Portable Pressure Washer' in name: return '便携高压清洗机'
    if 'RGB Touch Table Lamp' in name: return 'RGB触摸台灯'
    if 'Magnetic Wind Chime' in name: return '磁性风铃'
    
    # 3D打印耗材
    if 'SUNLU PLA' in name: return 'SUNLU PLA耗材'
    if 'PLA' in name: return 'PLA打印耗材'
    
    # 厨房用品
    if 'Cisily Sponge Holder' in name: return 'Cisily海绵架'
    if 'Sponge Holder' in name: return '海绵架'
    
    # 亚马逊基础
    if 'Amazon Basics 4' in name: return '亚马逊电池'
    
    # 魔术贴
    if 'VELCRO Brand' in name: return 'VELCRO魔术贴'
    
    # 首饰
    if 'Small Gold or S' in name: return '小号金银首饰'
    
    # 亚马逊设备
    if 'Fire TV Stick 4K Plus' in name: return '亚马逊Fire TV 4K Plus'
    if 'Fire TV Stick 4K Max' in name: return '亚马逊Fire TV 4K Max'
    if 'Fire TV Stick 4K Select' in name: return '亚马逊Fire TV 4K Select'
    if 'Fire TV Stick 4K' in name: return '亚马逊Fire TV 4K'
    if 'Fire TV Stick HD' in name: return '亚马逊Fire TV HD'
    if 'Kindle Paperwhite' in name: return '亚马逊Kindle Paperwhite'
    if 'Kindle' in name: return '亚马逊Kindle'
    if 'Echo Show 5' in name: return '亚马逊Echo Show 5'
    if 'Echo Dot' in name: return '亚马逊Echo Dot'
    if 'Fire 7 Kids tablet' in name: return '亚马逊Fire 7儿童平板'
    if 'Fire HD 10 tablet' in name: return '亚马逊Fire HD 10平板'
    if 'eero 6' in name: return '亚马逊eero 6扩展器'
    
    # 苹果设备
    if 'MacBook Air 13-inch' in name and 'M5' in name: return '苹果MacBook Air M5'
    if 'MacBook Air 15-inch' in name: return '苹果MacBook Air 15'
    if 'MacBook Pro' in name and 'M5' in name: return '苹果MacBook Pro M5'
    if 'MacBook Neo' in name: return '苹果MacBook Neo'
    if 'iPhone 16 Pro Max' in name: return '苹果iPhone 16 Pro Max'
    if 'iPhone 16 Pro' in name: return '苹果iPhone 16 Pro'
    if 'iPhone 16e' in name: return '苹果iPhone 16e'
    if 'iPhone 15 Pro Max' in name: return '苹果iPhone 15 Pro Max'
    if 'iPhone 15 Pro' in name: return '苹果iPhone 15 Pro'
    if 'iPhone 15' in name: return '苹果iPhone 15'
    if 'iPhone 14 Pro Max' in name: return '苹果iPhone 14 Pro Max'
    if 'iPhone 14 Pro' in name: return '苹果iPhone 14 Pro'
    if 'iPhone 14 Plus' in name: return '苹果iPhone 14 Plus'
    if 'iPhone 14' in name: return '苹果iPhone 14'
    if 'iPhone 13 Mini' in name: return '苹果iPhone 13 Mini'
    if 'iPhone 13' in name: return '苹果iPhone 13'
    if 'iPhone 12' in name: return '苹果iPhone 12'
    if 'iPhone SE 3rd' in name: return '苹果iPhone SE 3代'
    if 'iPhone SE 2nd' in name: return '苹果iPhone SE 2代'
    if 'iPad 11-inch' in name: return '苹果iPad 11寸A16'
    if 'iPad 2021' in name: return '苹果iPad 2021 WiFi'
    if 'iPad 2020' in name: return '苹果iPad 2020 WiFi'
    if 'iPad, 10.2-Inch' in name: return '苹果iPad 10.2寸WiFi'
    if 'AirPods Pro 3' in name: return '苹果AirPods Pro 3'
    if 'AirPods Pro' in name: return '苹果AirPods Pro'
    if 'AirPods 4' in name: return '苹果AirPods 4'
    if 'AirPods 2' in name: return '苹果AirPods 2代'
    if 'AirTag (2nd' in name: return '苹果AirTag 2代'
    if 'Watch Series 11' in name: return '苹果Watch Series 11'
    if 'Watch Series 7' in name: return '苹果Watch Series 7'
    if 'EarPods' in name: return '苹果EarPods USB-C'
    
    # Ring/Blink
    if 'Ring Battery Doorbell' in name: return 'Ring电池门铃'
    if 'Ring Indoor Cam Plus' in name: return 'Ring室内摄像头Plus'
    if 'Ring Indoor Cam' in name: return 'Ring室内摄像头'
    if 'Ring Outdoor Cam Plus' in name: return 'Ring户外摄像头Plus'
    if 'Ring Spotlight Cam Plus' in name: return 'Ring Spotlight电池版'
    if 'Ring Chime' in name: return 'Ring门铃'
    if 'Blink Outdoor 4' in name: return 'Blink户外摄像头4代'
    if 'Blink Video Doorbell' in name: return 'Blink视频门铃'
    if 'Blink Mini 2K+' in name: return 'Blink Mini 2K+摄像头'
    if 'blink plus ai' in name.lower(): return 'Blink AI月度订阅'
    if 'blink plus plan' in name.lower(): return 'Blink Plus月度订阅'
    
    # 制冰机
    if 'EUHOMY Nugget Ice Maker' in name: return 'EUHOMY Nugget制冰机'
    if 'EUHOMY Ice Maker' in name or 'EUHOMY Countertop Ice' in name: return 'EUHOMY制冰机'
    if 'DUMOS Ice Maker' in name: return 'DUMOS制冰机'
    if 'NEWBULIG Ice Makers' in name: return 'NEWBULIG制冰机'
    if 'Kismile Nugget' in name: return 'Kismile Nugget制冰机'
    if 'Silonn Ice Maker' in name: return 'Silonn制冰机'
    if 'Antarctic Star Nugget' in name: return 'Antarctic Nugget制冰机'
    if 'Antarctic Star Countertop' in name: return 'Antarctic Star制冰机'
    if 'COWSAR Ice Maker' in name: return 'COWSAR制冰机'
    if 'OLIXIS' in name: return 'OLIXIS制冰机'
    if 'Igloo Portable Ice' in name: return 'Igloo制冰机'
    if 'Nugget Ice Maker' in name: return 'Nugget制冰机'
    if 'Countertop Ice Maker' in name and '8 Ice' in name: return '制冰机8块6分钟'
    if 'Frostorm' in name: return 'Frostorm 3.2尺小冰箱'
    if 'Midea MERC' in name: return 'Midea冰柜'
    
    # 游戏
    if name == 'Minecraft': return 'Minecraft游戏'
    if 'Geometry Dash' in name: return 'Geometry Dash游戏'
    if 'Noob Ninja' in name: return 'Noob Ninja游戏'
    if 'Runaway Maze' in name: return 'Runaway Maze游戏'
    if 'Snack Sprint' in name: return 'Snack Sprint游戏'
    if 'Bucket Crusher' in name: return 'Bucket Crusher游戏'
    if 'Monster Uplift' in name: return 'Monster Uplift游戏'
    if 'Dummy Break' in name: return 'Dummy Break游戏'
    if 'Shift Race' in name: return 'Shift Race赛车游戏'
    if 'Magic Tiles 3' in name: return 'Magic Tiles 3 PRO'
    if 'Naughty Baby' in name: return 'Naughty Baby模拟器'
    if 'Mental Might' in name: return 'Mental Might游戏'
    if "Bowman's Journey" in name: return "Bowman's Journey游戏"
    if 'Katana Clash' in name: return 'Katana Clash游戏'
    if 'Titans Legion' in name: return 'Titans Legion游戏'
    if 'Calm Energy' in name: return 'Calm Energy健身'
    if 'Rhythm: Motion' in name: return 'Rhythm游戏'
    if 'Challenge: Race' in name: return 'Challenge游戏'
    if 'Jurassic Merge' in name: return 'Jurassic Merge游戏'
    if 'Blade Master' in name: return 'Blade Master游戏'
    
    # 纸尿裤/湿巾
    if 'Pampers Swaddlers' in name: return 'Pampers纸尿裤'
    if 'Pampers Sensitive' in name: return 'Pampers敏感湿巾'
    if 'Pampers Swim' in name: return 'Pampers游泳纸尿裤'
    if 'Pampers Training' in name: return 'Pampers训练裤'
    if 'Pampers Diapers' in name: return 'Pampers纸尿裤'
    if 'Huggies Natural Care' in name: return 'Huggies湿巾'
    if 'Huggies Size Newborn' in name: return 'Huggies新生儿纸尿裤'
    if 'Huggies Size 5' in name: return 'Huggies 5号纸尿裤'
    if 'Huggies Simply Clean' in name: return 'Huggies湿巾'
    if 'Huggies Little Swimmers' in name: return 'Huggies游泳纸尿裤'
    if 'Honest Company Baby Wipes' in name: return 'Honest湿巾'
    if 'Honest Company 2-in-1' in name: return 'Honest洗发沐浴'
    if 'WaterWipes' in name: return 'WaterWipes湿巾'
    if "Dr. Brown's" in name: return "Dr. Brown's奶嘴"
    if 'Desitin' in name: return 'Desitin护臀膏'
    if 'Momcozy' in name: return 'Momcozy清洗配件'
    if 'Gaiatop' in name: return 'Gaiatop婴儿车风扇'
    
    # 美妆护肤
    if 'medicube Toner Pads' in name: return 'Medicube零毛孔棉片2.0'
    if 'eos Shea Better' in name: return 'eos身体乳'
    if 'eos Body Wash' in name: return 'eos沐浴露'
    if 'Mighty Patch' in name: return 'Mighty Patch痘痘贴'
    if 'Neutrogena Makeup' in name: return 'Neutrogena卸妆湿巾'
    if 'Neutrogena Ultra Sheer' in name: return 'Neutrogena防晒SPF70'
    if 'The Ordinary' in name: return 'The Ordinary甘醇酸'
    if 'BIODANCE' in name: return 'BIODANCE胶原面膜'
    if 'PanOxyl' in name: return 'PanOxyl 10%祛痘洗面'
    if 'Clean Skin Club' in name: return 'Clean Skin Club毛巾'
    if 'Maybelline' in name: return 'Maybelline睫毛膏'
    if "MRS. MEYER'S" in name: return "MRS. MEYER'S洗手液"
    if 'EltaMD' in name: return 'EltaMD防晒'
    if 'Nizoral' in name: return 'Nizoral去屑洗发水'
    if "Paula's Choice" in name: return "Paula's Choice BHA"
    if 'Blue Lizard' in name: return 'Blue Lizard防晒SPF50'
    if 'Aquaphor' in name: return 'Aquaphor修复膏'
    
    # 书籍系列
    if 'Dungeon Crawler Carl' in name: return 'Dungeon Crawler Carl'
    if "Carl's Doomsday" in name: return "Carl's Doomsday"
    if 'Dungeon Anarchist' in name: return 'Dungeon Cookbook'
    if 'Gate of the Feral Gods' in name: return 'Feral Gods Book 4'
    if "Butcher's Masquerade" in name: return "Butcher's Masquerade"
    if 'Eye of the Bedlam Bride' in name: return 'Bedlam Bride Book 6'
    if 'Inevitable Ruin' in name: return 'Inevitable Ruin'
    if 'Parade of Horribles' in name: return 'Dungeon Carl Book 8'
    if 'Primal Hunter' in name: return 'Primal Hunter 14'
    if 'Harry Potter and the Deathly' in name: return '哈利波特死亡圣器'
    if 'Harry Potter and the Sorcerer' in name: return '哈利波特魔法石'
    if 'The Deal' in name: return 'The Deal小说'
    if 'The Mistake' in name: return 'The Mistake小说'
    if 'The Score' in name: return 'The Score小说'
    if 'The Goal' in name: return 'The Goal小说'
    if 'The Legacy' in name: return 'The Legacy小说'
    if 'Yesteryear' in name: return 'Yesteryear小说'
    if 'Theo of Golden' in name: return 'Theo of Golden小说'
    if 'Project Hail Mary' in name: return 'Project Hail Mary'
    if 'The Divorce' in name: return 'The Divorce小说'
    if 'The Correspondent' in name: return 'The Correspondent小说'
    if 'Calamity Club' in name: return 'The Calamity Club小说'
    if 'Let Them Theory' in name: return 'The Let Them Theory'
    if 'Remarkably Bright' in name: return 'Remarkably Bright Creatures'
    if "The Killer" in name: return "The Killer Isn't Alice"
    if 'Very Hungry Caterpillar' in name: return '好饿的毛毛虫'
    if 'Rainbow Fish' in name: return '彩虹鱼绘本'
    if 'I Love You to the Moon' in name: return 'I Love You to the Moon'
    if 'Oh, the Places' in name: return "Oh, Places You'll Go!"
    if 'Strangers: A Memoir' in name: return 'Strangers回忆录'
    if 'Stitched' in name: return 'Stitched小说'
    if 'A Painted House' in name: return 'A Painted House小说'
    if 'Fever Dream' in name: return 'Fever Dream小说'
    if 'Rules for the Summer' in name: return 'Rules for Summer小说'
    if 'Made (Manhattan' in name: return 'Made小说'
    if 'Vicious Devil' in name: return 'Vicious Devil小说'
    if 'Crown Me Dead' in name: return 'Crown Me Dead小说'
    if 'Mile High' in name: return 'Mile High小说'
    if 'Bad Boy Era' in name: return 'Bad Boy Era小说'
    if 'Dear Debbie' in name: return 'Dear Debbie小说'
    if 'Dire Bound' in name: return 'Dire Bound小说'
    
    # 汽车用品
    if 'Mobil 1' in name: return 'Mobil 1机油'
    if 'Valvoline Advanced' in name: return 'Valvoline 0W-20机油'
    if 'Valvoline MaxLife' in name: return 'Valvoline 5W-30机油'
    if 'CARORY' in name: return 'CARORY空调滤芯'
    if 'USANOOKS' in name: return 'USANOOKS超细纤维布'
    if 'Chemical Guys' in name: return 'Chemical Guys清洁剂'
    if 'AstroAI' in name: return 'AstroAI充气泵'
    if 'CERAKOTE' in name: return 'CERAKOTE大灯修复'
    if "Meguiar's" in name: return "Meguiar's抛光剂"
    if 'NOCO Boost' in name: return 'NOCO GB40应急电源'
    if 'NOCO GENIUS' in name: return 'NOCO GENIUS1充电器'
    if 'Camco TST' in name: return 'Camco RV马桶清洁剂'
    if 'EcoNour' in name: return 'EcoNour遮阳挡'
    if 'Kaistyle' in name: return 'Kaistyle MagSafe支架'
    if 'Drift Car Air Freshener' in name: return '车载香薰'
    
    # 望远镜
    if 'Hontry' in name: return 'Hontry望远镜'
    if 'Elikliv' in name: return 'Elikliv显微镜1000x'
    if 'Vortex Crossfire' in name: return 'Vortex Crossfire HD'
    if 'Vortex Triumph' in name: return 'Vortex Triumph HD'
    if 'Vortex Diamondback' in name: return 'Vortex Diamondback HD'
    if 'Aurosports' in name: return 'Aurosports望远镜'
    if 'Gskyer Telescope' in name: return 'Gskyer天文望远镜'
    if '15x55' in name: return '15x55望远镜'
    if '15x52' in name: return '15x52高清望远镜'
    if '12x50' in name: return '12x50望远镜'
    if 'Binoculars for Kids' in name: return '儿童望远镜'
    if 'Mini Compact Binoculars' in name: return '迷你望远镜'
    if 'Compact Binoculars' in name: return '便携望远镜'
    if 'Binoculars for Adults' in name: return '成人望远镜'
    
    # 音乐/黑胶
    if "Short n' Sweet" in name: return "Short n' Sweet黑胶"
    if 'Back to Black' in name: return 'Back to Black黑胶'
    if 'Rumours' in name: return 'Rumours黑胶'
    if 'Currents' in name: return 'Currents黑胶'
    if 'Cinematic' in name: return 'Cinematic黑胶'
    if 'Prizefighter' in name: return 'Prizefighter黑胶'
    if 'Number Ones' in name: return 'Number Ones黑胶'
    if 'Abbey Road' in name: return 'Abbey Road周年版'
    if 'Dark Side of the Moon' in name: return 'Dark Side 50周年'
    if 'Art of Loving' in name: return 'The Art of Loving黑胶'
    if 'Great Divide' in name: return 'The Great Divide黑胶'
    if 'DeBÍ TiRAR' in name: return 'DeBÍ TiRAR黑胶'
    if 'The Romantic' in name: return 'The Romantic黑胶'
    if 'Dandelion' in name: return 'Dandelion黑胶'
    if name == 'Red': return 'Red黑胶'
    if name == 'Thriller': return 'Thriller专辑'
    if name == 'Bad': return 'Bad专辑'
    if 'Off The Wall' in name: return 'Off The Wall专辑'
    if 'Dungeon Lane' in name: return 'Dungeon Lane专辑'
    
    # 手机配件
    if 'SUPFINE' in name: return 'SUPFINE iPhone 17壳'
    if 'FNTCASE for iPhone 17' in name: return 'FNTCASE iPhone 17壳'
    if 'FNTCASE for iPhone 15' in name: return 'FNTCASE iPhone 15壳'
    if 'PEHAEL' in name: return 'PEHAEL iPhone 17膜'
    if 'Miracase for iPhone 17e' in name: return 'Miracase iPhone 17e壳'
    if 'Miracase Magnetic for iPhone 17' in name: return 'Miracase iPhone 17壳'
    if 'TOCOL' in name: return 'TOCOL iPhone 15膜'
    if 'Ailun' in name: return 'Ailun iPhone 16膜'
    if 'SuydanBox' in name: return 'SuydanBox iPhone 17壳'
    if 'iPhone 17 16 15 Charger' in name: return 'iPhone Type-C快充'
    if 'INIU 45W' in name: return 'INIU 45W充电宝'
    if 'Hiearcool' in name: return 'Hiearcool防水袋'
    
    # 服装
    if 'Hanes mens Underwear' in name: return 'Hanes男士内裤'
    if "Hanes Men's Undershirt" in name: return 'Hanes男士汗衫'
    if 'Gildan' in name: return 'Gildan男士T恤'
    if 'LetsJoli' in name: return 'LetsJoli女士内衣'
    if 'COOFANDY' in name: return 'COOFANDY男士亚麻衫'
    if 'Nippies' in name: return 'Nippies乳贴'
    if 'OEAK Womens Deep' in name: return 'OEAK女士内衣'
    if 'OEAK Women Jelly' in name: return 'OEAK果冻内衣'
    if 'AUTOMET' in name: return 'AUTOMET女士背心'
    if 'Carhartt' in name: return 'Carhartt K87 T恤'
    if 'ANRABESS' in name: return 'ANRABESS女士上衣'
    if "Crocs Kid's" in name: return 'Crocs儿童洞洞鞋'
    if 'Crocs Unisex' in name: return 'Crocs成人洞洞鞋'
    if 'Water Shoes' in name: return '涉水鞋'
    if 'Wrangler' in name: return 'Wrangler工装短裤'
    if 'CHICME' in name: return 'CHICME内置内衣背心'
    if 'KuaiLu' in name: return 'KuaiLu女士拖鞋'
    if 'OFEEFAN' in name: return 'OFEEFAN女士上衣'
    if 'COCOMARTS' in name: return 'COCOMARTS果冻内衣'
    if 'Hstyle' in name: return 'Hstyle蕾丝袜6双'
    
    # 纪念币
    if 'USA 250th Anniversary' in name or '250th Anniversary' in name: return '美国250周年纪念币'
    if 'U.S. Army Commemorative' in name: return '美军250周年纪念币'
    if '250 Years of Freedom' in name: return '退伍军人纪念币'
    if '250 Anniversary 2 Dollar' in name or '250th Anniversary Collectible' in name: return '250周年2美元'
    if 'Semiquincentennial' in name: return '250周年25分币'
    if 'World Coins' in name: return '世界硬币套装'
    if name == '2026': return '2026纪念币'
    if '2026 P' in name: return '2026 P纪念币'
    if 'Wheat Pennies' in name or 'Wheat Penny' in name: return '小麦便士50枚'
    if 'Morgan Silver' in name: return '摩根银元'
    if 'Gamer Decision Coin' in name: return '游戏决策币'
    if 'Indian Head' in name: return '1877印第安人头币'
    if 'Final Cent' in name: return '纪念币1909-2025'
    if '1795 Liberty' in name: return '1795自由女神币'
    if 'WWII Coin' in name: return '二战便士套装'
    if 'Unsearched Wheat' in name: return '小麦便士卷'
    if 'British Sixpence' in name: return '英国六便士币'
    
    # 电脑/电子
    if 'TP-Link Deco 7' in name: return 'TP-Link WiFi 7路由器'
    if 'TP-Link Deco' in name: return 'TP-Link Deco'
    if 'TP-Link AX1800' in name: return 'TP-Link AX1800路由器'
    if 'Anker USB C Hub' in name: return 'Anker USB-C扩展坞'
    if 'Anker Laptop Docking' in name: return 'Anker双屏扩展坞'
    if 'Anker MacBook Pro Charger' in name: return 'Anker MacBook充电器'
    if 'Mac Book Pro Charger' in name: return 'MacBook充电器'
    if '65W USB C' in name or 'VJYUIJAY' in name: return '65W USB-C充电器'
    if 'Charger Compatible with HP' in name: return 'HP笔记本充电器'
    if 'UGREEN USB C Hub' in name: return 'UGREEN USB-C扩展坞'
    if 'USB C Docking Station' in name: return 'USB-C双屏扩展坞'
    if 'BESIGN' in name: return 'BESIGN笔记本支架'
    if 'Roku Streaming Stick 4K' in name: return 'Roku 4K流媒体棒'
    if 'Roku Streaming Stick HD' in name: return 'Roku HD流媒体棒'
    if 'Roku TV Remote' in name: return 'Roku遥控器'
    if 'Replacement Remote Control' in name: return 'Roku遥控器2件套'
    if 'Wall Charger, Surge' in name: return '插排充电器'
    if 'Surge Protector Power' in name: return '电源插排'
    if 'JLab Go Air' in name: return 'JLab Go Air Pop+耳机'
    if 'TAGRY' in name: return 'TAGRY蓝牙耳机'
    
    # 收藏卡
    if 'Stray Kids' in name: return 'Stray Kids激光小卡'
    if 'Michael Jackson' in name: return 'Michael Jackson Funko'
    if 'Star Wars 2023' in name: return '星球大战卡片盒'
    if 'Star Wars The Book' in name: return '波巴菲特卡片'
    if 'Topps Chrome Star Wars' in name: return '2025星战铬卡片'
    if 'KATSEYE' in name: return 'KATSEYE贴纸套装'
    if 'Katseye Photocards' in name: return 'Katseye小卡'
    if 'My Little Pony' in name: return '小马宝莉卡片'
    if 'Hazbin Hotel' in name: return 'Hazbin Hotel卡片'
    if 'Superman/Spider-Man' in name: return '超人蜘蛛侠漫画'
    if 'Spider-Man/Superman' in name: return '蜘蛛侠超人漫画'
    if 'Pokemon Scarlet' in name: return '宝可梦151C收藏卡'
    if 'Trump Trading' in name: return '特朗普交易卡'
    if 'Pawg Stars' in name: return 'Pawg Stars杂志'
    if 'Ben 10' in name: return 'Ben 10漫画'
    if 'Invincible Season' in name: return 'Invincible卡片盒'
    if 'Desert Storm' in name: return '沙漠风暴卡片盒'
    if 'Original Simplified Chinese' in name: return '简体中文版'
    
    # 礼品卡
    if 'Amazon eGift Card' in name: return '亚马逊礼品卡'
    if 'Amazon Gift Card Balance' in name: return '亚马逊礼品卡充值'
    if 'Amazon Physical Gift Card' in name: return '亚马逊实体礼品卡'
    if 'Amazon Printable Gift Card' in name: return '亚马逊打印礼品卡'
    if 'Apple Gift Card' in name: return '苹果礼品卡'
    if 'Visa Physical Gift Card' in name and '$100' in name: return 'Visa礼品卡$100'
    if 'Visa Physical Gift Card' in name and '$50' in name: return 'Visa礼品卡$50'
    if 'Visa Physical Gift Card' in name and '$200' in name: return 'Visa礼品卡$200'
    if 'DoorDash' in name: return 'DoorDash礼品卡'
    if 'Uber eGift' in name: return 'Uber礼品卡'
    if 'Google Play' in name: return 'Google Play礼品卡'
    if 'Starbucks' in name: return '星巴克礼品卡'
    
    # 食品饮料
    if 'CELSIUS' in name: return 'CELSIUS饮料套装'
    if 'Nespresso' in name: return 'Nespresso胶囊'
    if 'Banana Bunch' in name: return '香蕉4根'
    if 'Premier Protein' in name: return 'Premier蛋白奶昔'
    if 'Monster Energy' in name: return 'Monster零糖能量饮料'
    if 'Naturesweet' in name: return 'NatureSweet小番茄'
    if 'DaVinci' in name: return 'DaVinci蓝莓糖浆'
    if 'Sparkling Ice' in name: return 'Sparkling Ice饮料'
    if 'Diet Coke' in name: return '健怡可乐'
    if 'Core Power Elite' in name: return 'Core Power蛋白奶昔'
    if 'Core Power Protein' in name: return 'Core Power蛋白奶昔'
    if 'Bloom Nutrition' in name: return 'Bloom能量饮料'
    if 'Blueberries' in name: return '蓝莓1品脱'
    if 'Avocado' in name: return '牛油果'
    if name == 'Strawberries': return '草莓'
    if 'PUR Gum' in name: return 'PUR口香糖'
    if 'Propel' in name: return 'Propel运动饮料'
    if 'Lavazza' in name: return 'Lavazza咖啡豆'
    
    # 家居
    if 'Bounty Quick' in name or 'Bounty Select' in name: return 'Bounty厨房纸'
    if 'Scott ComfortPlus' in name: return 'Scott卫生纸'
    if 'Scott Professional' in name: return 'Scott卫生纸'
    if 'Angel Soft' in name: return 'Angel Soft卫生纸'
    if 'Charmin' in name: return 'Charmin卫生纸'
    if 'Quilted Northern' in name: return 'Quilted Northern卫生纸'
    if 'Dixie' in name: return 'Dixie纸盘'
    if 'DUDE Wipes' in name: return 'DUDE湿巾'
    if 'Cottonelle' in name: return 'Cottonelle湿巾'
    if 'Sparkle' in name: return 'Sparkle厨房纸'
    if 'LMNT' in name: return 'LMNT电解质'
    if 'Pure Encapsulations' in name: return 'Pure镁补充剂'
    if "Miss Mouth's" in name: return "Miss Mouth's去渍喷雾"
    if 'Optimum Nutrition' in name: return 'ON肌酸粉'
    if 'Liquid I.V.' in name: return 'Liquid I.V.补水粉'
    if 'Terro' in name: return 'Terro蚂蚁药'
    if 'Queen Size 4 Piece' in name: return '四件套床单'
    if 'Owala FreeSip' in name: return 'Owala保温杯'
    if 'Zevo Flying' in name: return 'Zevo飞虫诱捕器'
    if 'HOME GROWN' in name: return 'Zinnia种子'
    if 'Summit' in name: return 'Summit蚊子药'
    if 'Barossa' in name: return 'Barossa浴帘'
    if 'BigFoot' in name: return 'BigFoot浴帘'
    if 'Niagara' in name: return 'Niagara床垫'
    if 'BEDLORE' in name: return 'BEDLORE床垫套'
    if 'Utopia Bedding Queen' in name: return 'Utopia四件套'
    if 'Utopia Bedding Down' in name: return 'Utopia枕头'
    if 'Zulay' in name: return 'Zulay打奶泡器'
    if 'Supmedic' in name: return 'Supmedic手套'
    if 'MedPride' in name: return 'MedPride手套'
    if 'Inspire Cobalt' in name: return 'Inspire蓝色手套'
    if 'Inspire Black' in name: return 'Inspire黑色手套'
    if 'FifthPulse' in name: return 'FifthPulse粉色手套'
    if 'Fygrip' in name: return 'Fygrip真空压缩袋'
    if 'Cozy Essential' in name: return 'Cozy真空压缩袋'
    if 'Swihauk' in name: return 'Swihauk粘毛器'
    if 'Tork' in name: return 'Tork擦手纸'
    if 'DIYMAG' in name: return 'DIYMAG磁性挂钩'
    if 'Gorilla Super Glue' in name: return 'Gorilla强力胶'
    if 'Loctite Super' in name: return 'Loctite强力胶'
    if "Molly's Suds" in name: return "Molly's洗碗机球"
    if 'Chapin' in name: return 'Chapin喷壶'
    if 'SWIFTLITE' in name: return 'SWIFTLITE手套'
    
    # 电池/亚马逊基础
    if 'Amazon Basics 20-Pack AA' in name: return '亚马逊AA电池20节'
    if 'Amazon Basics AAA' in name: return '亚马逊AAA电池'
    if 'Amazon Basics 2-Ply Soft' in name: return '亚马逊卫生纸'
    if 'Amazon Basics 2-Ply Flex' in name: return '亚马逊厨房纸'
    if 'Amazon Basics Everyday' in name: return '亚马逊纸盘'
    if 'Amazon Basics Double' in name: return '亚马逊双头棉签'
    if 'Amazon Basics Hypoallergenic' in name: return '亚马逊低敏化妆棉'
    if 'Amazon Basics Gentle' in name: return '亚马逊洗手液'
    if 'Amazon Basics Slim' in name: return '亚马逊防滑衣架'
    if 'Amazon Brand' in name: return '亚马逊品牌'
    
    # 工艺/文具
    if 'Handcraft Blends' in name: return 'Handcraft薄荷精油'
    if 'ARTISTRO' in name: return 'ARTISTRO 36色马克笔'
    if 'Secopad' in name: return 'Secopad剪贴胶带'
    if 'iBayam' in name: return 'iBayam剪刀3件套'
    if 'B7000' in name: return 'B7000珠宝胶水'
    if '100% Pure Tea Tree' in name: return '100%茶树精油'
    if "Elmer's" in name: return "Elmer's紫色胶棒"
    if 'Bandle' in name: return 'Bandle粉笔马克笔'
    if '100% Pure Rosemary' in name: return '100%迷迭香精油'
    if 'RED HEART' in name: return 'RED HEART毛线白色'
    if 'Tulip One-Step' in name: return 'Tulip扎染套装'
    if 'Neenah' in name: return 'Neenah卡纸'
    if 'ScotchBlue' in name: return 'ScotchBlue美纹胶带'
    if 'FITTDYHE' in name: return 'FITTDYHE布料胶水'
    
    # 其他商品
    if 'Hearth' in name and 'Homestead' in name: return 'Hearth牛油护肤膏'
    if 'Titanium Cutting' in name: return '钛切菜板'
    if 'Taba Squishy' in name: return 'Taba仓鼠捏捏乐'
    if 'Sereney' in name: return 'Sereney女孩礼物'
    if 'Bible Verses' in name: return '圣经经文罐'
    if 'Retirement Gift' in name: return '退休礼物钥匙扣'
    if '16th Birthday' in name: return '16岁生日贺卡'
    if 'ID Tags' in name: return '宠物ID牌'
    if 'Tallowbourn' in name: return 'Tallowbourn润唇膏'
    if 'MAMAGIFTREE' in name: return '情侣礼物'
    if 'Sweet Water' in name: return 'Sweet Water蜡烛'
    if 'Opal Nose Ring' in name: return 'Opal鼻环'
    if 'LUCKYJEWUS' in name: return 'LUCKYJEWUS鼻钉'
    if 'Lipfidence' in name: return 'Lipfidence唇霜'
    if 'Obsidian Crystal' in name: return '黑曜石能量蜡烛'
    if 'Loc Spray' in name: return 'Loc喷雾'
    if 'PEALICIOUS' in name: return 'PEALICIOUS吐司钥匙扣'
    if 'Odor Eliminating' in name: return '除味蜡烛4件套'
    if 'No-Touch Thermometer' in name: return '非接触式体温计'
    
    # 厨房
    if 'Etekcity Food' in name: return 'Etekcity厨房秤'
    if 'STANLEY Quencher H2.0' in name: return 'STANLEY保温杯'
    if 'STANLEY Quencher ProTour' in name: return 'STANLEY保温杯Pro'
    if 'HydroJug' in name: return 'HydroJug水杯'
    if 'Alpha Grillers' in name: return 'Alpha Grillers温度计'
    if 'KitchenAid All Purpose' in name: return 'KitchenAid剪刀'
    if 'KitchenAid Classic' in name: return 'KitchenAid开罐器'
    if 'bella 2 Slice' in name: return 'bella烤面包机'
    if 'Air Fryer Paper' in name: return '空气炸锅纸'
    if 'Homaxy' in name: return 'Homaxy厨房毛巾'
    if 'TrendPlain' in name: return 'TrendPlain调料瓶'
    if 'Reynolds Kitchens' in name: return 'Reynolds烘焙纸'
    if 'Instant Read' in name: return '即读温度计'
    if 'Amazon Basics Digital Kitchen' in name: return '亚马逊厨房秤'
    if 'Owala SmoothSip' in name: return 'Owala水杯'
    if 'TempPro' in name: return 'TempPro温度计'
    if 'Ninja Nutri-Plus' in name: return 'Ninja搅拌机'
    if 'Socomi' in name: return 'Socomi桌旗'
    
    # DVD/蓝光
    if 'Kill Bill' in name: return 'Kill Bill蓝光'
    if 'Avatar: Fire' in name: return 'Avatar: Fire And Ash'
    if 'Talladega Nights' in name: return 'Talladega Nights蓝光'
    if 'Super Mario Galaxy' in name: return 'Super Mario Galaxy电影'
    if 'Speed Racer' in name: return 'Speed Racer蓝光'
    if 'Bringing Out the Dead' in name: return 'Bringing Out the Dead'
    if 'Robin Hood' in name: return 'Robin Hood蓝光'
    if 'Fight Club' in name: return 'Fight Club蓝光'
    if 'Evil Dead' in name: return 'Evil Dead 45周年'
    if 'Nirvanna, The Band' in name: return 'Nirvanna电影'
    if 'KPop Demon' in name: return 'KPop Demon Hunters'
    if 'Hoppers' in name: return 'Hoppers电影'
    if 'Interstellar' in name: return 'Interstellar蓝光'
    if 'Super Mario Bros.' in name: return 'Super Mario Bros电影'
    
    # 音乐设备
    if 'Labstandard' in name: return 'Labstandard麦克风'
    if 'Ernie Ball' in name: return 'Ernie Ball琴弦'
    if 'Mini Mic Pro' in name: return 'Mini Mic Pro'
    if "D'Addario Acoustic" in name: return "D'Addario琴弦"
    if "D'Addario Guitar" in name: return "D'Addario琴弦"
    if "D'Addario Eclipse" in name: return "D'Addario调音器"
    
    # 默认返回截取后的名称
    if len(name) > 15:
        return name[:15]
    return name

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