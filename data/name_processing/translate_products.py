#!/usr/bin/env python3
"""翻译商品名称"""
import json
import sqlite3
from pathlib import Path

db_path = Path(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\amazon.db')
output_path = Path(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\processed_names.json')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT asin, name FROM products WHERE name IS NOT NULL AND name != ''")
rows = cursor.fetchall()
conn.close()

def translate_name(name, asin):
    # 游戏主机相关
    if 'PlayStation' in name or 'PS' in name:
        if 'DualSense' in name and 'Edge' in name:
            return 'PS Edge手柄'
        elif 'DualSense' in name:
            return 'PS DualSense手柄'
        elif 'Store Gift Card' in name:
            return 'PS商店礼品卡'
        elif 'Gift Card' in name:
            return 'PS礼品卡'
    
    if 'Nintendo' in name or 'Switch' in name:
        if 'Switch 2' in name:
            return '任天堂Switch 2主机'
        elif 'eShop' in name or 'Gift Card' in name:
            return '任天堂礼品卡'
        elif 'Switch' in name:
            return '任天堂Switch配件'
    
    if 'Xbox' in name or 'XBOX' in name:
        if 'Game Pass' in name:
            return 'Xbox Game Pass'
        elif 'Wireless' in name and 'Controller' in name:
            return 'Xbox无线手柄'
        elif 'Gift Card' in name:
            return 'Xbox礼品卡'
    
    # Apple产品
    if 'Apple' in name:
        if 'AirPods Pro' in name:
            return 'Apple AirPods Pro'
        elif 'AirPods' in name:
            return 'Apple AirPods'
        elif 'iPhone' in name:
            return 'Apple iPhone'
        elif 'iPad' in name:
            return 'Apple iPad'
        elif 'MacBook Air' in name:
            return 'MacBook Air'
        elif 'MacBook Pro' in name:
            return 'MacBook Pro'
        elif 'Apple Watch' in name:
            return 'Apple Watch'
        elif 'AirTag' in name:
            return 'Apple AirTag'
        elif 'EarPods' in name:
            return 'Apple EarPods'
        elif 'Gift Card' in name:
            return 'Apple礼品卡'
    
    # Amazon产品
    if 'Amazon' in name or 'Fire TV' in name or 'Echo' in name or 'Kindle' in name:
        if 'Fire TV Stick 4K Max' in name:
            return 'Fire TV Stick 4K Max'
        elif 'Fire TV Stick 4K Plus' in name:
            return 'Fire TV Stick 4K Plus'
        elif 'Fire TV Stick' in name:
            return 'Fire TV Stick'
        elif 'Echo Dot' in name:
            return 'Amazon Echo Dot'
        elif 'Echo Show' in name:
            return 'Amazon Echo Show'
        elif 'Kindle Paperwhite' in name:
            return 'Kindle Paperwhite'
        elif 'Kindle' in name:
            return 'Amazon Kindle'
        elif 'Fire HD' in name:
            return 'Fire HD平板'
        elif 'Fire 7' in name:
            return 'Fire 7平板'
        elif 'Gift Card' in name or 'eGift Card' in name:
            return 'Amazon礼品卡'
        elif 'Basic' in name or 'Basics' in name:
            return 'Amazon Basics'
    
    # Ring/Blink智能家居
    if 'Ring' in name:
        if 'Doorbell' in name:
            return 'Ring门铃'
        elif 'Cam' in name:
            return 'Ring摄像头'
        elif 'Chime' in name:
            return 'Ring门铃'
        return 'Ring产品'
    
    if 'Blink' in name:
        if 'Doorbell' in name:
            return 'Blink门铃'
        elif 'Mini' in name:
            return 'Blink Mini摄像头'
        elif 'Outdoor' in name:
            return 'Blink户外摄像头'
        return 'Blink产品'
    
    # 罗技产品
    if 'Logitech' in name or 'Logi' in name:
        if 'G502' in name:
            return '罗技G502鼠标'
        elif 'G305' in name:
            return '罗技G305鼠标'
        elif 'Driving Force' in name:
            return '罗技G换挡器'
        return '罗技产品'
    
    # 雷蛇产品
    if 'Razer' in name:
        if 'BlackShark' in name:
            return '雷蛇BlackShark耳机'
        return '雷蛇产品'
    
    # DJI产品
    if 'DJI' in name:
        if 'Mic' in name:
            return 'DJI麦克风'
        return 'DJI产品'
    
    # 食品饮料
    if 'Coffee' in name or 'Nespresso' in name or 'Lavazza' in name:
        return '咖啡产品'
    if 'Energy Drink' in name or 'Monster' in name or 'CELSIUS' in name:
        return '能量饮料'
    if 'Protein' in name and 'Shake' in name:
        return '蛋白奶昔'
    if 'Banana' in name:
        return '香蕉'
    if 'Blueberri' in name:
        return '蓝莓'
    if 'Avocado' in name:
        return '牛油果'
    if 'Strawberri' in name:
        return '草莓'
    if 'Tomato' in name:
        return '番茄'
    
    # 宠物用品
    if 'Cat' in name or 'Kitten' in name:
        if 'Litter' in name:
            return '猫砂'
        elif 'Food' in name or 'Treat' in name:
            return '猫粮/零食'
        return '猫用品'
    if 'Dog' in name or 'Puppy' in name:
        if 'Food' in name or 'Treat' in name:
            return '狗粮/零食'
        return '狗用品'
    if 'Pet' in name:
        return '宠物用品'
    
    # 办公用品
    if 'Paper' in name:
        if 'Printer' in name:
            return '打印纸'
        elif 'Towel' in name:
            return '厨房纸'
        elif 'Toilet' in name:
            return '卫生纸'
        return '纸张'
    if 'Ink' in name or 'Cartridge' in name:
        return '墨盒'
    if 'Pen' in name:
        return '笔'
    if 'Notebook' in name:
        return '笔记本'
    
    # 清洁用品
    if 'Towel' in name or 'Wipe' in name:
        return '清洁用品'
    
    # 电子产品
    if 'Headphone' in name or 'Headset' in name or 'Earbud' in name:
        return '耳机'
    if 'Mouse' in name:
        return '鼠标'
    if 'Keyboard' in name:
        return '键盘'
    if 'Charger' in name:
        return '充电器'
    if 'Cable' in name:
        return '线缆'
    if 'Battery' in name:
        return '电池'
    
    # 软件服务
    if 'Norton' in name:
        return 'Norton杀毒软件'
    if 'McAfee' in name:
        return 'McAfee杀毒软件'
    if 'VPN' in name:
        return 'VPN服务'
    if 'TurboTax' in name:
        return 'TurboTax报税软件'
    if 'Microsoft Office' in name:
        return 'Microsoft Office'
    if 'Windows' in name:
        return 'Windows系统'
    
    # 运动健身
    if 'Dumbbell' in name or 'Weight' in name:
        return '健身器材'
    if 'Swim' in name or 'Goggle' in name:
        return '游泳用品'
    if 'Golf' in name:
        return '高尔夫球'
    
    # 收藏卡
    if 'Trading Card' in name or 'Baseball Card' in name:
        return '收藏卡'
    if 'Pokemon' in name:
        return '宝可梦卡'
    if 'Star Wars' in name:
        return '星球大战卡'
    
    # 电影音乐
    if 'Blu-ray' in name or '4K' in name and 'Movie' in name:
        return '蓝光电影'
    if 'DVD' in name:
        return 'DVD电影'
    if 'Vinyl' in name or 'LP' in name:
        return '黑胶唱片'
    
    # 书籍
    if 'Book' in name or 'Novel' in name:
        return '书籍'
    
    # 玩具
    if 'Toy' in name or 'Game' in name:
        return '玩具/游戏'
    
    # 礼品卡
    if 'Gift Card' in name:
        return '礼品卡'
    
    # 默认截取前15字符
    short = name[:15] if len(name) > 15 else name
    return short

items = []
for asin, name in rows:
    ecom_code = f'ECAM{asin}'
    short_name = translate_name(name, asin)
    items.append({'id': ecom_code, 'short_name': short_name})

data = {
    'batch_id': '20260530_2301',
    'items': items
}

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'已处理 {len(items)} 条商品名称')
