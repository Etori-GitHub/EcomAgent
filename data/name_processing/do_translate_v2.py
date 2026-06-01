#!/usr/bin/env python3
"""翻译商品名称"""
import json
from datetime import datetime

input_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json'
output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\processed_names.json'

def translate_name(name):
    """翻译商品名称为中文短名称（不超过15字）"""
    name_lower = name.lower()
    
    # ========== Amazon 硬件产品 ==========
    if 'Amazon' in name or 'Fire TV' in name:
        if 'Fire TV Stick 4K Max' in name:
            return 'Fire TV Stick 4K Max'
        elif 'Fire TV Stick 4K Plus' in name:
            return 'Fire TV Stick 4K Plus'
        elif 'Fire TV Stick 4K Select' in name:
            return 'Fire TV Stick 4K Select'
        elif 'Fire TV Stick 4K' in name:
            return 'Fire TV Stick 4K'
        elif 'Fire TV Stick HD' in name:
            return 'Fire TV Stick HD'
        elif 'Fire TV Stick' in name:
            return 'Fire TV Stick'
        elif 'Echo Show 5' in name:
            return 'Echo Show 5'
        elif 'Echo Show 8' in name:
            return 'Echo Show 8'
        elif 'Echo Show 10' in name:
            return 'Echo Show 10'
        elif 'Echo Show 15' in name:
            return 'Echo Show 15'
        elif 'Echo Show' in name:
            return 'Echo Show智能屏'
        elif 'Echo Dot' in name:
            return 'Echo Dot音箱'
        elif 'Echo Pop' in name:
            return 'Echo Pop音箱'
        elif 'Echo' in name and 'Echo' in name:
            return 'Amazon Echo音箱'
        elif 'Kindle Paperwhite' in name:
            return 'Kindle Paperwhite'
        elif 'Kindle Scribe' in name:
            return 'Kindle Scribe'
        elif 'Kindle Colorsoft' in name:
            return 'Kindle彩屏版'
        elif 'Kindle' in name:
            return 'Amazon Kindle'
        elif 'Fire HD 10' in name:
            return 'Fire HD 10平板'
        elif 'Fire HD 8' in name:
            return 'Fire HD 8平板'
        elif 'Fire 7' in name:
            return 'Fire 7平板'
        elif 'Fire Max 11' in name:
            return 'Fire Max 11平板'
        elif 'Fire TV' in name and 'Smart TV' in name:
            return 'Fire智能电视'
        elif 'Luna Controller' in name:
            return 'Luna手柄'
    
    # ========== Ring 智能家居 ==========
    if 'Ring' in name:
        if 'Battery Doorbell' in name or 'Doorbell' in name and 'Battery' in name:
            return 'Ring电池门铃'
        elif 'Wired Doorbell' in name or 'Doorbell Pro' in name:
            return 'Ring有线门铃'
        elif 'Video Doorbell' in name:
            return 'Ring视频门铃'
        elif 'Doorbell' in name:
            return 'Ring门铃'
        elif 'Spotlight Cam Plus' in name:
            return 'Ring聚光摄像头Plus'
        elif 'Spotlight Cam' in name:
            return 'Ring聚光摄像头'
        elif 'Floodlight Cam' in name:
            return 'Ring泛光摄像头'
        elif 'Outdoor Cam Plus' in name:
            return 'Ring户外摄像头Plus'
        elif 'Outdoor Cam' in name:
            return 'Ring户外摄像头'
        elif 'Indoor Cam Plus' in name:
            return 'Ring室内摄像头Plus'
        elif 'Indoor Cam' in name:
            return 'Ring室内摄像头'
        elif 'Stick Up Cam' in name:
            return 'Ring无线摄像头'
        elif 'Chime Pro' in name:
            return 'Ring门铃扩展器Pro'
        elif 'Chime' in name:
            return 'Ring门铃响铃器'
        elif 'Alarm Pro' in name:
            return 'Ring报警系统Pro'
        elif 'Alarm' in name:
            return 'Ring报警系统'
        return 'Ring产品'
    
    # ========== Blink 智能家居 ==========
    if 'Blink' in name or 'blink' in name_lower:
        if 'plus plan' in name_lower or 'subscription' in name_lower:
            return 'Blink订阅服务'
        elif 'ai plan' in name_lower:
            return 'Blink AI订阅'
        elif 'Video Doorbell' in name:
            return 'Blink视频门铃'
        elif 'Doorbell' in name:
            return 'Blink门铃'
        elif 'Outdoor 4' in name:
            return 'Blink Outdoor 4'
        elif 'Outdoor' in name:
            return 'Blink户外摄像头'
        elif 'Mini 2K+' in name or 'Mini 2' in name:
            return 'Blink Mini 2K+'
        elif 'Mini' in name:
            return 'Blink Mini摄像头'
        elif 'Floodlight' in name:
            return 'Blink泛光灯'
        elif 'Sync Module' in name:
            return 'Blink同步模块'
        return 'Blink产品'
    
    # ========== Apple 产品 ==========
    if 'Apple' in name:
        if 'AirPods Pro 2' in name or 'AirPods Pro (2nd' in name:
            return '苹果AirPods Pro 2代'
        elif 'AirPods Pro' in name:
            return '苹果AirPods Pro'
        elif 'AirPods 4' in name:
            return '苹果AirPods 4代'
        elif 'AirPods 3' in name:
            return '苹果AirPods 3代'
        elif 'AirPods 2' in name or 'AirPods (2nd' in name:
            return '苹果AirPods 2代'
        elif 'AirPods Max' in name:
            return '苹果AirPods Max'
        elif 'AirPods' in name:
            return '苹果AirPods'
        elif 'iPhone 16 Pro Max' in name:
            return '苹果iPhone 16 Pro Max'
        elif 'iPhone 16 Pro' in name:
            return '苹果iPhone 16 Pro'
        elif 'iPhone 16 Plus' in name:
            return '苹果iPhone 16 Plus'
        elif 'iPhone 16' in name:
            return '苹果iPhone 16'
        elif 'iPhone 15 Pro Max' in name:
            return '苹果iPhone 15 Pro Max'
        elif 'iPhone 15 Pro' in name:
            return '苹果iPhone 15 Pro'
        elif 'iPhone 15 Plus' in name:
            return '苹果iPhone 15 Plus'
        elif 'iPhone 15' in name:
            return '苹果iPhone 15'
        elif 'iPhone 14 Pro Max' in name:
            return '苹果iPhone 14 Pro Max'
        elif 'iPhone 14 Pro' in name:
            return '苹果iPhone 14 Pro'
        elif 'iPhone 14 Plus' in name:
            return '苹果iPhone 14 Plus'
        elif 'iPhone 14' in name:
            return '苹果iPhone 14'
        elif 'iPhone 13 Pro Max' in name:
            return '苹果iPhone 13 Pro Max'
        elif 'iPhone 13 Pro' in name:
            return '苹果iPhone 13 Pro'
        elif 'iPhone 13 mini' in name:
            return '苹果iPhone 13 mini'
        elif 'iPhone 13' in name:
            return '苹果iPhone 13'
        elif 'iPhone 12 Pro Max' in name:
            return '苹果iPhone 12 Pro Max'
        elif 'iPhone 12 Pro' in name:
            return '苹果iPhone 12 Pro'
        elif 'iPhone 12 mini' in name:
            return '苹果iPhone 12 mini'
        elif 'iPhone 12' in name:
            return '苹果iPhone 12'
        elif 'iPhone SE' in name:
            return '苹果iPhone SE'
        elif 'iPhone' in name:
            return '苹果iPhone'
        elif 'iPad Pro 13' in name:
            return '苹果iPad Pro 13寸'
        elif 'iPad Pro 12.9' in name:
            return '苹果iPad Pro 12.9'
        elif 'iPad Pro 11' in name:
            return '苹果iPad Pro 11寸'
        elif 'iPad Pro' in name:
            return '苹果iPad Pro'
        elif 'iPad Air 13' in name:
            return '苹果iPad Air 13寸'
        elif 'iPad Air 11' in name:
            return '苹果iPad Air 11寸'
        elif 'iPad Air' in name:
            return '苹果iPad Air'
        elif 'iPad mini' in name:
            return '苹果iPad mini'
        elif 'iPad 10.9' in name or 'iPad (10th' in name:
            return '苹果iPad 10代'
        elif 'iPad 10.2' in name or 'iPad (9th' in name:
            return '苹果iPad 9代'
        elif 'iPad' in name:
            return '苹果iPad'
        elif 'MacBook Air 15' in name:
            return 'MacBook Air 15寸'
        elif 'MacBook Air 13' in name or 'MacBook Air M3' in name:
            return 'MacBook Air 13寸'
        elif 'MacBook Air' in name:
            return 'MacBook Air'
        elif 'MacBook Pro 16' in name:
            return 'MacBook Pro 16寸'
        elif 'MacBook Pro 14' in name:
            return 'MacBook Pro 14寸'
        elif 'MacBook Pro' in name:
            return 'MacBook Pro'
        elif 'Mac Studio' in name:
            return 'Mac Studio'
        elif 'Mac mini' in name:
            return 'Mac mini'
        elif 'Apple Watch Ultra 2' in name:
            return 'Apple Watch Ultra 2'
        elif 'Apple Watch Ultra' in name:
            return 'Apple Watch Ultra'
        elif 'Apple Watch Series 10' in name:
            return 'Apple Watch S10'
        elif 'Apple Watch Series 9' in name:
            return 'Apple Watch S9'
        elif 'Apple Watch SE' in name:
            return 'Apple Watch SE'
        elif 'Apple Watch' in name:
            return 'Apple Watch'
        elif 'AirTag 4' in name:
            return '苹果AirTag 4件装'
        elif 'AirTag' in name:
            return '苹果AirTag'
        elif 'EarPods' in name:
            return '苹果EarPods耳机'
        elif 'MagSafe Charger' in name:
            return '苹果MagSafe充电器'
        elif 'MagSafe' in name:
            return '苹果MagSafe配件'
        elif 'Gift Card' in name:
            return '苹果礼品卡'
        elif 'TV 4K' in name:
            return 'Apple TV 4K'
        elif 'Apple TV' in name:
            return 'Apple TV'
        return '苹果产品'
    
    # ========== Sony/PlayStation ==========
    if 'PlayStation' in name or 'PS5' in name or 'PS4' in name:
        if 'DualSense Edge' in name:
            return 'PS5 Edge精英手柄'
        elif 'DualSense' in name:
            return 'PS5 DualSense手柄'
        elif 'PS5 Console' in name or 'PlayStation 5 Console' in name:
            return 'PS5主机'
        elif 'PS5 Digital' in name:
            return 'PS5数字版主机'
        elif 'PS5 Slim' in name:
            return 'PS5 Slim主机'
        elif 'PS5 Pro' in name:
            return 'PS5 Pro主机'
        elif 'PS5' in name:
            return 'PS5产品'
        elif 'PS4' in name:
            return 'PS4产品'
        elif 'Store Gift Card' in name:
            return 'PS商店礼品卡'
        elif 'Gift Card' in name:
            return 'PS礼品卡'
        return 'PlayStation产品'
    
    # ========== Nintendo ==========
    if 'Nintendo' in name or 'Switch' in name:
        if 'Switch 2' in name:
            return '任天堂Switch 2'
        elif 'Switch OLED' in name:
            return '任天堂Switch OLED'
        elif 'Switch Lite' in name:
            return '任天堂Switch Lite'
        elif 'Switch' in name:
            return '任天堂Switch'
        elif 'eShop Card' in name or 'eShop' in name:
            return '任天堂eShop卡'
        elif 'Gift Card' in name:
            return '任天堂礼品卡'
        return '任天堂产品'
    
    # ========== Xbox ==========
    if 'Xbox' in name or 'XBOX' in name:
        if 'Game Pass Ultimate' in name:
            return 'Xbox Game Pass终极版'
        elif 'Game Pass' in name:
            return 'Xbox Game Pass'
        elif 'Wireless Controller' in name or 'Controller' in name:
            return 'Xbox无线手柄'
        elif 'Series X' in name:
            return 'Xbox Series X主机'
        elif 'Series S' in name:
            return 'Xbox Series S主机'
        elif 'Gift Card' in name:
            return 'Xbox礼品卡'
        return 'Xbox产品'
    
    # ========== Samsung ==========
    if 'Samsung' in name or 'Galaxy' in name:
        if 'Galaxy S24 Ultra' in name:
            return '三星S24 Ultra'
        elif 'Galaxy S24+' in name or 'Galaxy S24 Plus' in name:
            return '三星S24+'
        elif 'Galaxy S24' in name:
            return '三星S24'
        elif 'Galaxy S23' in name:
            return '三星S23'
        elif 'Galaxy Z Fold' in name:
            return '三星Z Fold折叠屏'
        elif 'Galaxy Z Flip' in name:
            return '三星Z Flip折叠屏'
        elif 'Galaxy Tab' in name:
            return '三星Galaxy平板'
        elif 'Galaxy' in name:
            return '三星Galaxy'
        elif 'Neo QLED' in name or 'QLED' in name:
            return '三星QLED电视'
        elif 'Crystal UHD' in name:
            return '三星UHD电视'
        return '三星产品'
    
    # ========== DJI ==========
    if 'DJI' in name:
        if 'Mic 2' in name or 'Mic Mini' in name:
            return 'DJI麦克风'
        elif 'Mic' in name:
            return 'DJI麦克风'
        elif 'Mini 4 Pro' in name:
            return 'DJI Mini 4 Pro'
        elif 'Mini 4' in name:
            return 'DJI Mini 4无人机'
        elif 'Mini 3' in name:
            return 'DJI Mini 3无人机'
        elif 'Air 3' in name:
            return 'DJI Air 3无人机'
        elif 'Mavic' in name:
            return 'DJI Mavic无人机'
        elif 'Osmo' in name:
            return 'DJI Osmo云台'
        return 'DJI产品'
    
    # ========== Logitech ==========
    if 'Logitech' in name or 'Logi' in name:
        if 'G502' in name:
            return '罗技G502鼠标'
        elif 'G305' in name:
            return '罗技G305鼠标'
        elif 'G Pro' in name:
            return '罗技G Pro鼠标'
        elif 'MX Master' in name:
            return '罗技MX Master鼠标'
        elif 'MX Keys' in name:
            return '罗技MX Keys键盘'
        elif 'Driving Force' in name:
            return '罗技方向盘'
        elif 'G923' in name:
            return '罗技G923方向盘'
        elif 'G29' in name:
            return '罗技G29方向盘'
        return '罗技产品'
    
    # ========== Razer ==========
    if 'Razer' in name:
        if 'BlackShark' in name:
            return '雷蛇BlackShark耳机'
        elif 'DeathAdder' in name:
            return '雷蛇DeathAdder鼠标'
        elif 'BlackWidow' in name:
            return '雷蛇BlackWidow键盘'
        return '雷蛇产品'
    
    # ========== 电视/显示器 ==========
    if 'INSIGNIA' in name:
        if 'Fire TV' in name:
            return 'INSIGNIA Fire智能电视'
        return 'INSIGNIA电视'
    if 'TCL' in name:
        if 'QLED' in name:
            return 'TCL QLED电视'
        elif 'Roku TV' in name:
            return 'TCL Roku电视'
        return 'TCL电视'
    if 'Hisense' in name:
        return '海信电视'
    if 'LG OLED' in name:
        return 'LG OLED电视'
    if 'LG' in name:
        return 'LG电视'
    if 'VIZIO' in name:
        return 'VIZIO电视'
    
    # ========== 礼品卡 ==========
    if 'Gift Card' in name or 'eGift Card' in name:
        if 'Amazon' in name:
            return '亚马逊礼品卡'
        elif 'Google Play' in name:
            return 'Google Play礼品卡'
        elif 'Steam' in name:
            return 'Steam礼品卡'
        elif 'Roblox' in name:
            return 'Roblox礼品卡'
        elif 'Spotify' in name:
            return 'Spotify礼品卡'
        elif 'Netflix' in name:
            return 'Netflix礼品卡'
        return '礼品卡'
    
    # ========== 软件/订阅 ==========
    if 'Norton' in name:
        return 'Norton杀毒软件'
    if 'McAfee' in name:
        return 'McAfee杀毒软件'
    if 'VPN' in name:
        return 'VPN服务'
    if 'TurboTax' in name:
        return 'TurboTax报税软件'
    if 'Microsoft 365' in name or 'Office 365' in name:
        return 'Microsoft 365'
    if 'Microsoft Office' in name:
        return 'Microsoft Office'
    if 'Windows' in name:
        return 'Windows系统'
    
    # ========== 游戏相关 ==========
    if 'Steam' in name:
        if 'Deck' in name:
            return 'Steam Deck掌机'
        return 'Steam产品'
    if 'Roblox' in name:
        return 'Roblox游戏卡'
    if 'Pokemon' in name:
        return '宝可梦产品'
    if 'Minecraft' in name:
        return '我的世界游戏'
    
    # ========== 食品饮料 ==========
    if 'Coffee' in name or 'Nespresso' in name or 'Lavazza' in name:
        return '咖啡产品'
    if 'Energy Drink' in name or 'Monster' in name or 'CELSIUS' in name:
        return '能量饮料'
    if 'Protein' in name:
        return '蛋白产品'
    
    # ========== 宠物用品 ==========
    if 'Cat' in name or 'Kitten' in name:
        return '猫用品'
    if 'Dog' in name or 'Puppy' in name:
        return '狗用品'
    if 'Pet' in name:
        return '宠物用品'
    
    # ========== 其他电子产品 ==========
    if 'Headphone' in name or 'Headset' in name or 'Earbud' in name:
        return '耳机'
    if 'Mouse' in name and 'Pad' not in name:
        return '鼠标'
    if 'Keyboard' in name:
        return '键盘'
    if 'Charger' in name:
        return '充电器'
    if 'Cable' in name:
        return '线缆'
    if 'Battery' in name:
        return '电池'
    
    # ========== 默认截取前15字符 ==========
    short = name[:15] if len(name) > 15 else name
    return short

# 读取输入文件
with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

batch_id = data['batch_id']
items = data['items']

# 翻译处理
processed_items = []
for item in items:
    item_id = item['id']
    name = item['name']
    short_name = translate_name(name)
    processed_items.append({
        'id': item_id,
        'short_name': short_name
    })

# 输出结果
output_data = {
    'batch_id': batch_id,
    'items': processed_items
}

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f'已完成 {len(processed_items)} 条商品名称翻译')
print(f'输出文件: {output_path}')
