#!/usr/bin/env python3
"""处理 OpenClaw 翻译任务 - 为 pending_names.json 生成中文简称"""

import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSING_DIR = BASE_DIR / "data" / "name_processing"
PENDING_FILE = PROCESSING_DIR / "pending_names.json"
PROCESSED_FILE = PROCESSING_DIR / "processed_names.json"

# 商品名称翻译映射
TRANSLATIONS = {
    # 书籍类
    "The Atomic Habits Workbook: Official Companion to": "原子习惯练习册",
    "Countries of the World: A Visual World Geography": "世界各国视觉地理",
    "Red Rising 3-Book Box Set: Red Rising": "火星崛起三部曲盒装",
    "Make Your Bed: Little Things That Can Change Your": "整理床铺：小事改变人生",
    "Umma: A Korean Mom's Kitchen Wisdom and 100 Family Recipes": "妈妈：韩式家庭食谱",
    "The Count of Monte Cristo (Penguin Classics)": "基督山伯爵",
    "Cozy Corner: Coloring Book for Adults and Kids": "温馨角落：成人儿童涂色书",
    "Good Night": "晚安",
    "In the Shadow of Eight: Surviving the Reality of": "八号阴影",
    "Rage and the Republic: The Unfinished Story of the": "愤怒与共和国",
    "Theo of Golden: A Novel": "金色的西奥",
    "100": "100",
    "Cancel Me If You Can": "有本事就封杀我",
    "Warriors Graphic Novel: The New Prophecy": "猫武士图像小说：新预言",
    "The Body Keeps the Score: Brain": "身体从未忘记",
    
    # 纪念币收藏类
    "2026 P Declaration of Independence Quarter 40 Coin": "2026年独立宣言纪念币套装",
    "2026 Revolutionary War Quarter 1776-2026 America": "2026年独立战争纪念币",
    "250th Anniversary Collectible 2 Dollar Bill": "250周年纪念2美元钞",
    "DD-214 Veteran Pride Coin": "退伍军人荣誉币",
    "US Navy Challenge Coin Sailor's Creed Engraved": "美国海军挑战币",
    "USA 250th Anniversary Commemorative Coin 1776-2026": "美国250周年纪念币",
    "2026 U.S. Silver Eagle": "2026年美国银鹰币",
    
    # 电子产品类
    "Apple iPad 11-inch: A16 chip": "iPad 11英寸 A16芯片",
    "Apple 2026 MacBook Air 13-inch Laptop with M5": "MacBook Air 13英寸 M5",
    "Soundcore P31i by Anker": "Soundcore P31i 耳机",
    "JBL Tune Buds": "JBL Tune Buds 耳机",
    "Ring Outdoor Cam Plus": "Ring 室外摄像头",
    "JLab Go Air Pop+ True Wireless Bluetooth Earbuds": "JLab Go Air Pop+ 真无线耳机",
    "JBL Tune 510BT": "JBL Tune 510BT 耳机",
    "Ring Battery Doorbell (newest model)": "Ring 电池门铃（最新款）",
    
    # 健身运动类
    "Walk On Indoor Walking Fitness DVD [No Treadmill] Plus Foot": "室内步行健身DVD",
    
    # 收藏卡类
    "Hazbin Hotel Season 2 Trading Cards": "地狱酒店第二季收藏卡",
    "Bandai Dragon Ball Super Card Game Fusion World": "龙珠超卡牌游戏",
    "The Phantom Knights of Rusty Bardiche": "幻影骑士团锈锚",
    "Alias: Red Band #1 (in bag) VF/NM ; Marvel comic book": "Alias 红标版 #1 漫画",
    "Upper Deck 2024 Marvel Masterpieces '92 Platinum": "漫威杰作2024铂金卡",
    "Alias: Red Band #2 (in bag) VF/NM ; Marvel comic book": "Alias 红标版 #2 漫画",
    "Weird Al Yankovic Variant Set": "Weird Al 变体卡套装",
    "Avatar: The Last Airbender-The Kyoshi Warriors #2": "降世神通：虚子战士 #2",
    "D'Orc #3A VF/NM ; Image comic book": "D'Orc #3A 漫画",
    "Noivern ex": "音波龙 ex",
    "The Time of Battle": "战斗时刻",
    "Talonflame 014/088": "烈箭鹰 014/088",
    "Unicorn Friends Collectible Trading Cards": "独角兽朋友收藏卡",
    "2026 Topps Chrome Disney Factory Sealed Value Box": "2026 Topps Chrome 迪士尼卡盒",
    "Elvis Presley Complete 1978 Trading Card Set": "猫王1978完整收藏卡",
    "Avatar": "阿凡达",
    "T.A.M.A. #1A VF/NM ; Panick comic book": "T.A.M.A. #1A 漫画",
    "Various Brands Milwaukee Brewers Robin Yount 20": "密尔沃基酿酒人队棒球卡",
    "Team Rocket's Dugtrio 101/217": "火箭队三地鼠 101/217",
}


def main():
    if not PENDING_FILE.exists():
        print("[INFO] 没有 pending_names.json，跳过")
        return
    
    with open(PENDING_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    items = data.get('items', [])
    batch_id = data.get('batch_id', 'unknown')
    
    processed_items = []
    for item in items:
        item_id = item.get('id')
        name = item.get('name')
        
        # 查找翻译
        short_name = TRANSLATIONS.get(name)
        
        if not short_name:
            # 如果没有预设翻译，生成简单简称
            # 截取前30个字符作为临时简称
            short_name = name[:30] + "..." if len(name) > 30 else name
        
        processed_items.append({
            'id': item_id,
            'name': name,
            'short_name': short_name
        })
    
    result = {
        'batch_id': batch_id,
        'processed_at': datetime.now().isoformat(),
        'count': len(processed_items),
        'items': processed_items
    }
    
    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 已处理 {len(processed_items)} 条翻译")
    
    # 统计翻译情况
    translated_count = sum(1 for item in processed_items if item['name'] in TRANSLATIONS)
    print(f"[INFO] 完整翻译: {translated_count} 条，待人工翻译: {len(processed_items) - translated_count} 条")


if __name__ == "__main__":
    main()