#!/usr/bin/env python3
"""翻译商品名称"""
import json
import re
from pathlib import Path

input_path = Path(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json')
output_path = Path(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\processed_names.json')

with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

def translate_name(name):
    name_lower = name.lower()
    
    # Amazon 设备
    if 'amazon' in name_lower or 'fire tv' in name_lower or 'echo' in name_lower or 'kindle' in name_lower:
        if 'fire tv stick 4k max' in name_lower:
            return 'Fire TV 4K Max'
        elif 'fire tv stick 4k plus' in name_lower:
            return 'Fire TV 4K Plus'
        elif 'fire tv stick 4k select' in name_lower:
            return 'Fire TV 4K'
        elif 'fire tv stick 4k' in name_lower:
            return 'Fire TV 4K'
        elif 'fire tv stick hd' in name_lower:
            return 'Fire TV HD'
        elif 'echo dot' in name_lower:
            return 'Echo Dot'
        elif 'echo show 5' in name_lower:
            return 'Echo Show 5'
        elif 'echo show' in name_lower:
            return 'Echo Show'
        elif 'kindle paperwhite' in name_lower:
            return 'Kindle PW'
        elif 'kindle' in name_lower:
            return 'Kindle'
        elif 'fire hd' in name_lower:
            return 'Fire HD平板'
        elif 'fire 7' in name_lower:
            return 'Fire 7平板'
        elif 'amazon basics' in name_lower or 'amazon brand' in name_lower:
            return 'Amazon Basics'
        elif 'gift card' in name_lower or 'egift' in name_lower:
            return 'Amazon礼品卡'
        elif 'reload' in name_lower:
            return 'Amazon余额充值'
    
    # Ring/Blink 智能家居
    if 'ring' in name_lower:
        if 'battery doorbell' in name_lower:
            return 'Ring电池门铃'
        elif 'doorbell' in name_lower:
            return 'Ring门铃'
        elif 'indoor cam plus' in name_lower:
            return 'Ring室内摄像头Plus'
        elif 'indoor cam' in name_lower:
            return 'Ring室内摄像头'
        elif 'outdoor cam plus' in name_lower:
            return 'Ring户外摄像头Plus'
        elif 'spotlight cam' in name_lower:
            return 'Ring聚光灯摄像头'
        elif 'chime' in name_lower:
            return 'Ring门铃铃声器'
        return 'Ring产品'
    
    if 'blink' in name_lower:
        if 'video doorbell' in name_lower:
            return 'Blink视频门铃'
        elif 'outdoor 4' in name_lower:
            return 'Blink户外摄像头4'
        elif 'outdoor' in name_lower:
            return 'Blink户外摄像头'
        elif 'mini 2k' in name_lower:
            return 'Blink Mini 2K摄像头'
        elif 'mini' in name_lower:
            return 'Blink Mini摄像头'
        elif 'plus plan' in name_lower or 'plus ai' in name_lower:
            return 'Blink订阅服务'
        return 'Blink产品'
    
    # Apple 产品
    if 'apple' in name_lower:
        if 'macbook air 15' in name_lower:
            return 'MacBook Air 15英寸'
        elif 'macbook air 13' in name_lower:
            return 'MacBook Air 13英寸'
        elif 'macbook pro' in name_lower:
            return 'MacBook Pro'
        elif 'macbook neo' in name_lower:
            return 'MacBook Neo 13英寸'
        elif 'iphone 16 pro max' in name_lower:
            return 'iPhone 16 Pro Max'
        elif 'iphone 16 pro' in name_lower:
            return 'iPhone 16 Pro'
        elif 'iphone 16e' in name_lower:
            return 'iPhone 16e'
        elif 'iphone 16' in name_lower:
            return 'iPhone 16'
        elif 'iphone 15 pro max' in name_lower:
            return 'iPhone 15 Pro Max'
        elif 'iphone 15' in name_lower:
            return 'iPhone 15'
        elif 'iphone 14 pro max' in name_lower:
            return 'iPhone 14 Pro Max'
        elif 'iphone 14 plus' in name_lower:
            return 'iPhone 14 Plus'
        elif 'iphone 14' in name_lower:
            return 'iPhone 14'
        elif 'iphone 13 mini' in name_lower:
            return 'iPhone 13 Mini'
        elif 'iphone 13' in name_lower:
            return 'iPhone 13'
        elif 'iphone 12' in name_lower:
            return 'iPhone 12'
        elif 'iphone se' in name_lower and '3rd' in name_lower:
            return 'iPhone SE 3代'
        elif 'iphone se' in name_lower and '2nd' in name_lower:
            return 'iPhone SE 2代'
        elif 'iphone' in name_lower:
            return 'iPhone'
        elif 'ipad 11-inch' in name_lower or 'ipad 10.9' in name_lower:
            return 'iPad 11英寸'
        elif 'ipad 10.2' in name_lower:
            return 'iPad 10.2英寸'
        elif 'ipad' in name_lower:
            return 'iPad'
        elif 'airpods pro 3' in name_lower:
            return 'AirPods Pro 3'
        elif 'airpods pro' in name_lower:
            return 'AirPods Pro'
        elif 'airpods 4' in name_lower:
            return 'AirPods 4'
        elif 'airpods 2' in name_lower:
            return 'AirPods 2'
        elif 'airpods' in name_lower:
            return 'AirPods'
        elif 'watch series 11' in name_lower:
            return 'Apple Watch 11'
        elif 'watch series 7' in name_lower:
            return 'Apple Watch 7'
        elif 'watch' in name_lower:
            return 'Apple Watch'
        elif 'airtag 2nd' in name_lower:
            return 'AirTag 2代'
        elif 'airtag' in name_lower:
            return 'AirTag'
        elif 'earpods' in name_lower:
            return 'EarPods'
        elif 'gift card' in name_lower:
            return 'Apple礼品卡'
    
    # 游戏主机
    if 'playstation' in name_lower or 'ps' in name_lower or 'dualsense' in name_lower:
        if 'dualsense edge' in name_lower:
            return 'PS Edge手柄'
        elif 'dualsense' in name_lower:
            return 'PS DualSense手柄'
        elif 'store gift card' in name_lower or 'gift card' in name_lower:
            return 'PS礼品卡'
        return 'PlayStation产品'
    
    if 'nintendo' in name_lower or 'switch 2' in name_lower:
        if 'switch 2' in name_lower:
            return '任天堂Switch 2'
        elif 'eshop' in name_lower or 'gift card' in name_lower:
            return '任天堂礼品卡'
        elif 'switch' in name_lower:
            return '任天堂Switch'
        return '任天堂产品'
    
    if 'xbox' in name_lower:
        if 'game pass' in name_lower:
            return 'Xbox Game Pass'
        elif 'wireless controller' in name_lower or 'gaming controller' in name_lower:
            return 'Xbox无线手柄'
        elif 'gift card' in name_lower:
            return 'Xbox礼品卡'
        return 'Xbox产品'
    
    # Roku
    if 'roku' in name_lower:
        if 'streaming stick 4k' in name_lower:
            return 'Roku Stick 4K'
        elif 'streaming stick hd' in name_lower:
            return 'Roku Stick HD'
        elif 'remote' in name_lower:
            return 'Roku遥控器'
        return 'Roku产品'
    
    # 电子产品配件
    if 'iphone' in name_lower and ('case' in name_lower or 'protector' in name_lower or 'screen' in name_lower):
        return 'iPhone配件'
    if 'magsafe' in name_lower or 'magnetic' in name_lower and 'mount' in name_lower:
        return 'MagSafe车载支架'
    if 'charger' in name_lower and ('usb c' in name_lower or 'laptop' in name_lower):
        return 'USB-C笔记本充电器'
    if 'portable charger' in name_lower or 'power bank' in name_lower:
        return '便携充电宝'
    if 'usb c hub' in name_lower or 'docking station' in name_lower:
        return 'USB-C扩展坞'
    if 'phone pouch' in name_lower and 'waterproof' in name_lower:
        return '防水手机袋'
    if 'car mount' in name_lower:
        return '车载支架'
    if 'headphones' in name_lower or 'earbuds' in name_lower:
        if 'wireless' in name_lower:
            return '无线耳机'
        return '耳机'
    
    # TP-Link 网络
    if 'tp-link' in name_lower or 'deco' in name_lower:
        if 'wifi 7' in name_lower:
            return 'TP-Link WiFi 7路由'
        elif 'wifi 6' in name_lower:
            return 'TP-Link WiFi 6路由'
        elif 'deco' in name_lower:
            return 'TP-Link Deco Mesh'
        return 'TP-Link路由器'
    if 'eero' in name_lower:
        return 'Amazon eero Mesh'
    
    # 冰箱/冰块机
    if 'ice maker' in name_lower:
        if 'nugget' in name_lower:
            return 'Nugget冰块机'
        return '制冰机'
    if 'mini fridge' in name_lower or 'freezer' in name_lower:
        return '小型冰柜'
    if 'chest freezer' in name_lower:
        return '立式冰柜'
    
    # 墨盒/打印
    if 'ink cartridge' in name_lower or 'hp 67' in name_lower or 'hp 64' in name_lower:
        return 'HP墨盒'
    if 'printer paper' in name_lower or 'copy paper' in name_lower:
        return '打印纸'
    if 'laminating' in name_lower:
        return '塑封膜'
    
    # 美妆护肤
    if 'medicube' in name_lower:
        if 'toner pads' in name_lower or 'pore pad' in name_lower:
            return 'Medicube零毛孔棉片'
        return 'Medicube护肤'
    if 'eos' in name_lower:
        if 'body wash' in name_lower:
            return 'eos沐浴露'
        elif 'body lotion' in name_lower:
            return 'eos身体乳'
        return 'eos产品'
    if 'mighty patch' in name_lower or 'hero cosmetics' in name_lower:
        return '痘痘贴'
    if 'neutrogena' in name_lower:
        return 'Neutrogena护肤'
    if 'the ordinary' in name_lower:
        return 'The Ordinary护肤'
    if 'biodance' in name_lower and 'mask' in name_lower:
        return 'BIODANCE面膜'
    if 'eltaMD' in name_lower:
        return 'EltaMD防晒'
    if 'blue lizard' in name_lower:
        return 'Blue Lizard防晒'
    if 'aquaphor' in name_lower:
        return 'Aquaphor修护膏'
    if 'panoxyl' in name_lower:
        return 'PanOxyl洁面'
    if 'paula' in name_lower and 'choice' in name_lower:
        return 'Paulas Choice护肤'
    if 'maybelline' in name_lower:
        return 'Maybelline彩妆'
    if 'clean skin club' in name_lower:
        return 'Clean Skin Club毛巾'
    if 'cotton rounds' in name_lower or 'cotton swabs' in name_lower:
        return '化妆棉'
    if 'hand soap' in name_lower:
        return '洗手液'
    if 'sunscreen' in name_lower or 'spf' in name_lower:
        return '防晒霜'
    if 'nizoral' in name_lower:
        return 'Nizoral洗发水'
    if 'mrs. meyer' in name_lower:
        return 'Mrs. Meyer清洁'
    
    # 婴儿用品
    if 'pampers' in name_lower:
        if 'swim' in name_lower:
            return 'Pampers游泳裤'
        elif 'training' in name_lower:
            return 'Pampers训练裤'
        elif 'sensitive' in name_lower and 'wipes' in name_lower:
            return 'Pampers敏感湿巾'
        return 'Pampers纸尿裤'
    if 'huggies' in name_lower:
        if 'swimmers' in name_lower:
            return 'Huggies游泳裤'
        elif 'little snugglers' in name_lower:
            return 'Huggies新生儿尿裤'
        elif 'wipes' in name_lower:
            return 'Huggies湿巾'
        return 'Huggies纸尿裤'
    if 'waterwipes' in name_lower:
        return 'WaterWipes湿巾'
    if 'honest company' in name_lower:
        if 'wipes' in name_lower:
            return 'Honest湿巾'
        elif 'shampoo' in name_lower:
            return 'Honest婴儿洗护'
        return 'Honest婴儿用品'
    if 'desitin' in name_lower:
        return 'Desitin护臀膏'
    if 'dr. brown' in name_lower:
        return 'Dr. Browns奶瓶'
    if 'baby' in name_lower and ('wipe' in name_lower or 'diaper' in name_lower):
        return '婴儿用品'
    if 'stroller fan' in name_lower:
        return '婴儿车风扇'
    if 'thermometer' in name_lower and 'no-touch' in name_lower:
        return '非接触体温计'
    
    # 食品饮料
    if 'celsius' in name_lower:
        return 'CELSIUS能量饮料'
    if 'monster' in name_lower and 'energy' in name_lower:
        return 'Monster能量饮料'
    if 'premier protein' in name_lower:
        return 'Premier蛋白奶昔'
    if 'core power' in name_lower:
        return 'Core Power蛋白奶昔'
    if 'sparkling ice' in name_lower:
        return 'Sparkling Ice气泡水'
    if 'diet coke' in name_lower:
        return '无糖可乐'
    if 'propel' in name_lower:
        return 'Propel运动饮料'
    if 'nespresso' in name_lower:
        return 'Nespresso咖啡胶囊'
    if 'lavazza' in name_lower:
        return 'Lavazza咖啡豆'
    if 'bloom nutrition' in name_lower:
        return 'Bloom能量饮料'
    if 'banana' in name_lower:
        return '香蕉'
    if 'blueberri' in name_lower:
        return '蓝莓'
    if 'avocado' in name_lower:
        return '牛油果'
    if 'strawberri' in name_lower:
        return '草莓'
    if 'tomato' in name_lower:
        return '番茄'
    if 'davinci' in name_lower and 'syrup' in name_lower:
        return 'DaVinci糖浆'
    if 'pur gum' in name_lower:
        return 'PUR口香糖'
    
    # 服装
    if 'hanes' in name_lower:
        if 'underwear' in name_lower or 'boxer' in name_lower:
            return 'Hanes男士内裤'
        elif 'undershirt' in name_lower:
            return 'Hanes男士内衣'
        return 'Hanes服装'
    if 'gildan' in name_lower and 't-shirt' in name_lower:
        return 'GildanT恤'
    if 'carhartt' in name_lower:
        return 'Carhartt工装T恤'
    if 'crocs' in name_lower:
        return 'Crocs洞洞鞋'
    if 'wrangler' in name_lower:
        return 'Wrangler短裤'
    if 'water shoes' in name_lower:
        return '涉水鞋'
    if 'bra' in name_lower:
        return '女士内衣'
    if 'nipple covers' in name_lower:
        return '乳贴'
    if 'tank top' in name_lower:
        return '女士背心'
    if 'flip flop' in name_lower:
        return '凉拖鞋'
    if 'linen shirt' in name_lower:
        return '亚麻衬衫'
    if 'ruffle sock' in name_lower:
        return '荷叶边袜子'
    
    # 家居清洁
    if 'bounty' in name_lower:
        return 'Bounty厨房纸'
    if 'scott' in name_lower:
        if 'toilet' in name_lower:
            return 'Scott卫生纸'
        return 'Scott纸巾'
    if 'charmin' in name_lower:
        return 'Charmin卫生纸'
    if 'angel soft' in name_lower:
        return 'Angel Soft卫生纸'
    if 'quilted northern' in name_lower:
        return 'Quilted Northern卫生纸'
    if 'paper towel' in name_lower:
        return '厨房纸巾'
    if 'toilet paper' in name_lower:
        return '卫生纸'
    if 'dixie' in name_lower and 'plate' in name_lower:
        return 'Dixie纸盘'
    if 'paper plate' in name_lower:
        return '纸盘'
    if 'dude wipe' in name_lower:
        return 'DUDE湿巾'
    if 'cottonelle' in name_lower:
        return 'Cottonelle湿巾'
    if 'sparkle' in name_lower:
        return 'Sparkle厨房纸'
    if 'surge protector' in name_lower or 'power strip' in name_lower:
        return '电源插座'
    if 'battery' in name_lower:
        return '电池'
    if 'lint roller' in name_lower:
        return '粘毛滚筒'
    if 'nitrile glove' in name_lower or 'exam glove' in name_lower:
        return '丁腈手套'
    if 'magnesium' in name_lower and 'glycinate' in name_lower:
        return '镁补充剂'
    if 'creatine' in name_lower:
        return '肌酸粉'
    if 'liquid i.v' in name_lower:
        return 'Liquid I.V电解质'
    if 'lmnt' in name_lower:
        return 'LMNT电解质'
    if 'ant killer' in name_lower or 'terro' in name_lower:
        return '蚂蚁诱饵'
    if 'zevo' in name_lower:
        return 'Zevo昆虫诱捕'
    if 'stain treater' in name_lower:
        return '污渍去除剂'
    
    # 家居用品
    if 'sheet set' in name_lower:
        return '床单套装'
    if 'mattress topper' in name_lower:
        return '床垫垫层'
    if 'mattress protector' in name_lower:
        return '床垫保护套'
    if 'pillow' in name_lower:
        return '枕头'
    if 'shower curtain' in name_lower or 'shower liner' in name_lower:
        return '浴帘'
    if 'water bottle' in name_lower or 'tumbler' in name_lower:
        if 'owala' in name_lower:
            return 'Owala水瓶'
        elif 'stanley' in name_lower:
            return 'Stanley水杯'
        elif 'hydrojug' in name_lower:
            return 'HydroJug水瓶'
        return '水瓶'
    if 'velvet hanger' in name_lower:
        return '丝绒衣架'
    if 'vacuum storage bag' in name_lower:
        return '真空收纳袋'
    if 'magnetic hook' in name_lower:
        return '磁力挂钩'
    if 'velcro' in name_lower:
        return '魔术贴'
    if 'super glue' in name_lower or 'gorilla glue' in name_lower:
        return '强力胶'
    if 'double sided tape' in name_lower:
        return '双面胶'
    if 'dishwasher pod' in name_lower:
        return '洗碗机洗涤块'
    
    # 厨房用品
    if 'kitchen scale' in name_lower or 'food scale' in name_lower:
        return '厨房秤'
    if 'meat thermometer' in name_lower:
        return '肉类温度计'
    if 'can opener' in name_lower:
        return '开罐器'
    if 'kitchen shears' in name_lower:
        return '厨房剪刀'
    if 'toaster' in name_lower:
        return '吐司机'
    if 'air fryer paper' in name_lower:
        return '空气炸锅纸'
    if 'parchment paper' in name_lower:
        return '烘焙纸'
    if 'dish cloth' in name_lower:
        return '洗碗布'
    if 'blender' in name_lower or 'nutri' in name_lower:
        return '搅拌机'
    if 'milk frother' in name_lower:
        return '奶泡器'
    if 'cheesecloth' in name_lower:
        return '纱布桌旗'
    if 'cutting board' in name_lower:
        return '菜板'
    if 'tallow' in name_lower:
        return '牛油护肤'
    
    # 汽车用品
    if 'motor oil' in name_lower:
        return '机油'
    if 'cabin air filter' in name_lower:
        return '汽车空气滤芯'
    if 'tire inflator' in name_lower or 'air compressor' in name_lower:
        return '车载充气泵'
    if 'jump starter' in name_lower:
        return '应急启动电源'
    if 'battery charger' in name_lower and 'smart' in name_lower:
        return '智能充电器'
    if 'sunshade' in name_lower and 'windshield' in name_lower:
        return '汽车遮阳挡'
    if 'headlight restoration' in name_lower:
        return '大灯修复套装'
    if 'cleaning cloth' in name_lower and 'microfiber' in name_lower:
        return '超细纤维清洁布'
    if 'interior cleaner' in name_lower:
        return '汽车内饰清洁'
    if 'squeegee' in name_lower:
        return '刮水器'
    if 'meguiar' in name_lower:
        return 'Meguiars汽车护理'
    if 'car air freshener' in name_lower:
        return '车载香氛'
    
    # 书籍
    if 'dungeon crawler carl' in name_lower:
        return 'Dungeon Carl'
    if 'harry potter' in name_lower:
        return '哈利波特'
    if 'project hail mary' in name_lower:
        return 'Hail Mary'
    if 'yesteryear' in name_lower:
        return 'Yesteryear'
    if 'the deal' in name_lower or 'the mistake' in name_lower or 'the score' in name_lower or 'the goal' in name_lower or 'the legacy' in name_lower:
        return 'Off-Campus系列'
    if 'the divorce' in name_lower:
        return 'The Divorce'
    if 'theo of golden' in name_lower:
        return 'Theo of Golden'
    if 'the calamity club' in name_lower:
        return 'Calamity Club'
    if 'the correspondent' in name_lower:
        return 'Correspondent'
    if 'the primal hunter' in name_lower:
        return 'Primal Hunter'
    if 'oh, the places' in name_lower:
        return 'Oh the Places'
    if 'the very hungry caterpillar' in name_lower:
        return '好饿的毛毛虫'
    if 'the rainbow fish' in name_lower:
        return '彩虹鱼'
    if 'i love you to the moon' in name_lower:
        return '我爱你到月球'
    if 'remarkably bright' in name_lower:
        return 'Remarkably Bright Creatures'
    if 'the let them theory' in name_lower:
        return 'The Let Them Theory'
    if 'book' in name_lower or 'novel' in name_lower:
        return '书籍'
    
    # 音乐/电影
    if 'vinyl' in name_lower or 'lp' in name_lower or 'album' in name_lower:
        return '黑胶唱片'
    if '4k ultra hd' in name_lower or 'blu-ray' in name_lower or 'dvd' in name_lower:
        if 'avatar' in name_lower:
            return 'Avatar蓝光电影'
        elif 'mario' in name_lower:
            return '马里奥电影蓝光'
        elif 'interstellar' in name_lower:
            return 'Interstellar蓝光'
        elif 'fight club' in name_lower:
            return 'Fight Club蓝光'
        elif 'kill bill' in name_lower:
            return 'Kill Bill蓝光'
        elif 'talladega' in name_lower:
            return 'Talladega Nights蓝光'
        elif 'speed racer' in name_lower:
            return 'Speed Racer蓝光'
        elif 'robin hood' in name_lower:
            return 'Robin Hood蓝光'
        return '蓝光电影'
    if 'short n sweet' in name_lower or 'sabrina' in name_lower:
        return 'Short n Sweet黑胶'
    if 'back to black' in name_lower:
        return 'Back to Black黑胶'
    if 'rumours' in name_lower:
        return 'Rumours黑胶'
    if 'abbey road' in name_lower:
        return 'Abbey Road黑胶'
    if 'dark side of the moon' in name_lower:
        return 'Dark Side黑胶'
    if 'thriller' in name_lower:
        return 'Thriller黑胶'
    if 'red' in name_lower and 'taylor' in name_lower:
        return 'Red黑胶'
    if 'currents' in name_lower:
        return 'Currents黑胶'
    
    # 游戏相关
    if 'minecraft' in name_lower:
        return 'Minecraft'
    if 'geometry dash' in name_lower:
        return 'Geometry Dash'
    if 'valorant' in name_lower:
        return 'VALORANT'
    if 'roblox' in name_lower and 'gift' in name_lower:
        return 'Roblox礼品卡'
    if '007' in name_lower:
        return '007 First Light'
    if 'tomodachi life' in name_lower:
        return 'Tomodachi Life'
    if 'star fox' in name_lower:
        return 'Star Fox'
    
    # 游戏配件
    if 'logitech g502' in name_lower:
        return '罗技G502鼠标'
    if 'logitech g305' in name_lower:
        return '罗技G305鼠标'
    if 'logitech g driving' in name_lower:
        return '罗技G换挡器'
    if 'razer blackshark' in name_lower:
        return '雷蛇BlackShark耳机'
    
    # 音频设备
    if 'dji mic' in name_lower:
        return 'DJI麦克风'
    if 'hollyland' in name_lower:
        return 'Hollyland无线麦克风'
    if 'wireless microphone' in name_lower or 'lapel mic' in name_lower:
        return '无线麦克风'
    if 'focusrite' in name_lower:
        return 'Focusrite音频接口'
    if 'karaoke' in name_lower:
        return '卡拉OK机'
    if 'bubble machine' in name_lower:
        return '泡泡机'
    if 'guitar string' in name_lower or 'daddario' in name_lower:
        return '吉他弦'
    if 'guitar tuner' in name_lower:
        return '吉他调音器'
    if 'oneodio' in name_lower:
        return 'OneOdio耳机'
    if 'jlab' in name_lower:
        return 'JLab耳机'
    if 'tagry' in name_lower:
        return 'TAGRY耳机'
    if 'fifine' in name_lower:
        return 'FIFINE麦克风'
    
    # 手工艺品
    if 'essential oil' in name_lower:
        return '精油'
    if 'acrylic paint' in name_lower or 'artistro' in name_lower:
        return '丙烯马克笔'
    if 'scrapbook tape' in name_lower:
        return '手工胶带'
    if 'scissors' in name_lower:
        return '剪刀'
    if 'glue' in name_lower and ('jewelry' in name_lower or 'fabric' in name_lower):
        return '专用胶水'
    if 'chalk marker' in name_lower:
        return '粉笔马克笔'
    if 'yarn' in name_lower:
        return '毛线'
    if 'tie dye' in name_lower:
        return '扎染套装'
    if 'cardstock' in name_lower:
        return '卡纸'
    if 'painters tape' in name_lower:
        return '美工胶带'
    if 'elmer' in name_lower and 'glue' in name_lower:
        return 'Elmer胶棒'
    
    # 玩具收藏
    if 'funko' in name_lower:
        return 'Funko Pop人偶'
    if 'pokemon card' in name_lower or 'pokemon' in name_lower and 'card' in name_lower:
        return '宝可梦卡'
    if 'star wars' in name_lower and 'card' in name_lower:
        return '星球大战卡'
    if 'trading card' in name_lower or 'topps' in name_lower:
        if 'baseball' in name_lower:
            return '棒球卡'
        elif 'football' in name_lower:
            return '足球卡'
        elif 'basketball' in name_lower:
            return '篮球卡'
        elif 'hockey' in name_lower:
            return '冰球卡'
        elif 'fifa' in name_lower or 'world cup' in name_lower:
            return '世界杯贴纸'
        return '收藏卡'
    if 'photocard' in name_lower or 'kpop' in name_lower:
        return 'KPop卡片'
    if 'marvel' in name_lower and 'legend' in name_lower:
        return 'Marvel人偶'
    if 'coin' in name_lower:
        return '收藏硬币'
    if 'vintage' in name_lower and ('baseball' in name_lower or 'football' in name_lower):
        return '复古收藏卡'
    if 'wheat penny' in name_lower:
        return '小麦 penny'
    if 'morgan' in name_lower and 'silver' in name_lower:
        return '摩根银币'
    if 'anniversary' in name_lower and ('250' in name_lower or '1776' in name_lower):
        return '250周年纪念币'
    
    # 礼品卡
    if 'gift card' in name_lower:
        if 'visa' in name_lower:
            return 'Visa礼品卡'
        elif 'doordash' in name_lower:
            return 'DoorDash礼品卡'
        elif 'uber' in name_lower:
            return 'Uber礼品卡'
        elif 'starbucks' in name_lower:
            return '星巴克礼品卡'
        elif 'google play' in name_lower:
            return 'Google Play礼品卡'
        return '礼品卡'
    
    # 纪念品/礼物
    if 'keychain' in name_lower:
        return '钥匙扣'
    if 'birthday card' in name_lower:
        return '生日贺卡'
    if 'nose ring' in name_lower or 'nose stud' in name_lower:
        return '鼻环'
    if 'candle' in name_lower:
        return '香薰蜡烛'
    if 'squishy' in name_lower:
        return '解压玩具'
    if 'id tag' in name_lower and 'pet' in name_lower:
        return '宠物ID牌'
    if 'lip balm' in name_lower:
        return '唇膏'
    if 'lip cream' in name_lower:
        return '唇膏'
    if 'gifts for' in name_lower:
        return '礼物套装'
    if 'bible verse' in name_lower:
        return '圣经经文罐'
    if 'retirement' in name_lower:
        return '退休礼物'
    
    # 眼镜望远镜
    if 'binocular' in name_lower:
        return '望远镜'
    if 'telescope' in name_lower:
        return '天文望远镜'
    if 'microscope' in name_lower:
        return '显微镜'
    if 'vortex optics' in name_lower:
        return 'Vortex望远镜'
    if 'sunglass' in name_lower:
        return '太阳镜'
    if 'swim goggles' in name_lower:
        return '泳镜'
    
    # 宠物用品
    if 'cat litter' in name_lower:
        return '猫砂'
    if 'cat treat' in name_lower or 'churu' in name_lower:
        return '猫零食'
    if 'cat food' in name_lower:
        return '猫粮'
    if 'dog treat' in name_lower or 'milk-bone' in name_lower:
        return '狗零食'
    if 'dog food' in name_lower:
        return '狗粮'
    if 'dog wrap' in name_lower:
        return '狗狗尿垫'
    if 'poop bag' in name_lower:
        return '宠物拾便袋'
    if 'pet wipe' in name_lower:
        return '宠物湿巾'
    if 'pill pocket' in name_lower:
        return '喂药零食'
    if 'potty pad' in name_lower:
        return '宠物尿垫'
    if 'bird food' in name_lower:
        return '鸟食'
    if 'hummingbird' in name_lower:
        return '蜂鸟喂食器'
    
    # 园艺
    if 'plant food' in name_lower or 'miracle-gro' in name_lower:
        return '植物肥料'
    if 'wild bird food' in name_lower:
        return '野生鸟食'
    if 'neem oil' in name_lower:
        return 'Neem油'
    if 'garden hose' in name_lower or 'nozzle' in name_lower:
        return '园艺喷头'
    if 'weed killer' in name_lower or 'roundup' in name_lower:
        return '除草剂'
    if 'insect killer' in name_lower or 'ortho' in name_lower:
        return '杀虫剂'
    if 'lime' in name_lower and 'insect' in name_lower:
        return '石灰驱虫'
    if 'mosquito' in name_lower:
        return '灭蚊剂'
    if 'sprayer' in name_lower:
        return '喷壶'
    if 'seed' in name_lower:
        return '种子'
    if 'fly trap' in name_lower:
        return '捕蝇器'
    if 'fruit fly' in name_lower:
        return '果蝇诱捕'
    
    # 运动健身
    if 'dumbbell' in name_lower or 'hand weight' in name_lower:
        return '哑铃'
    if 'weighted vest' in name_lower:
        return '负重马甲'
    if 'resistance band' in name_lower:
        return '阻力带'
    if 'fitness' in name_lower:
        return '健身用品'
    if 'golf ball' in name_lower:
        return '高尔夫球'
    if 'dry bag' in name_lower:
        return '防水袋'
    if 'balloon pump' in name_lower:
        return '气球泵'
    if 'travel towel' in name_lower:
        return '旅行毛巾'
    if 'band-aid' in name_lower:
        return '急救包'
    if 'fitbit' in name_lower or 'google fitbit' in name_lower:
        return 'Fitbit手环'
    
    # 办公用品
    if 'sharpie' in name_lower:
        return 'Sharpie马克笔'
    if 'scotch tape' in name_lower:
        return 'Scotch胶带'
    if 'file folder' in name_lower:
        return '文件夹'
    if 'pen' in name_lower:
        return '笔'
    if 'gel pen' in name_lower:
        return '凝胶笔'
    if 'desk pad' in name_lower:
        return '桌垫'
    if 'note pad' in name_lower or 'writing pad' in name_lower:
        return '记事本'
    if 'sheet protector' in name_lower:
        return '文件保护页'
    if 'playing card' in name_lower or 'bicycle' in name_lower and 'card' in name_lower:
        return '扑克牌'
    if 'joking hazard' in name_lower:
        return 'Joking Hazard桌游'
    
    # 软件服务
    if 'turbotax' in name_lower:
        return 'TurboTax报税软件'
    if 'h&r block' in name_lower:
        return 'H&R Block报税软件'
    if 'norton' in name_lower:
        return 'Norton杀毒软件'
    if 'mcafee' in name_lower:
        return 'McAfee杀毒软件'
    if 'bitdefender' in name_lower:
        return 'Bitdefender杀毒软件'
    if 'webroot' in name_lower:
        return 'Webroot杀毒软件'
    if 'malwarebytes' in name_lower:
        return 'Malwarebytes杀毒软件'
    if 'vpn' in name_lower or 'nordvpn' in name_lower or 'mullvad' in name_lower:
        return 'VPN服务'
    if 'microsoft office' in name_lower:
        return 'Microsoft Office'
    if 'windows 11' in name_lower or 'windows' in name_lower:
        return 'Windows系统'
    if 'quicken' in name_lower:
        return 'Quicken财务软件'
    if 'wyze' in name_lower and 'plan' in name_lower:
        return 'Wyze订阅服务'
    
    # 水过滤器
    if 'water filter' in name_lower or 'brita' in name_lower or 'everydrop' in name_lower:
        return '水过滤器'
    if 'zerowater' in name_lower:
        return 'ZeroWater滤芯'
    if 'ge' in name_lower and 'filter' in name_lower:
        return 'GE滤芯'
    if 'samsung' in name_lower and 'filter' in name_lower:
        return '三星滤芯'
    
    # INSIGNIA电视
    if 'insignia' in name_lower and 'tv' in name_lower:
        return 'INSIGNIA智能电视'
    
    # 气球派对
    if 'balloon' in name_lower:
        return '气球'
    if 'glow stick' in name_lower:
        return '荧光棒'
    if 'sticker book' in name_lower:
        return '贴纸书'
    if 'play doh' in name_lower:
        return 'Play-Doh彩泥'
    if 'baby bike' in name_lower:
        return '婴儿平衡车'
    if 'rattle' in name_lower:
        return '婴儿摇铃'
    if 'oball' in name_lower:
        return 'Oball婴儿球'
    if 'bluey' in name_lower:
        return 'Bluey玩具'
    if 'skateboard' in name_lower and 'trainer' in name_lower:
        return '滑板训练器'
    if 'kin sa' in name_lower:
        return '智能体温计'
    
    # Instax
    if 'instax' in name_lower and 'film' in name_lower:
        return 'Instax相纸'
    
    # 其他默认处理
    # 截取前15字符作为兜底
    short = name[:15] if len(name) > 15 else name
    return short.strip()

items = []
for item in data['items']:
    short_name = translate_name(item['name'])
    # 确保不超过15字符
    if len(short_name) > 15:
        short_name = short_name[:15]
    items.append({'id': item['id'], 'short_name': short_name})

result = {
    'batch_id': data['batch_id'],
    'items': items
}

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f'已翻译 {len(items)} 条商品名称')