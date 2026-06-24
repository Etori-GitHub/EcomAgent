#!/usr/bin/env python3
"""临时翻译处理脚本"""

import json
from pathlib import Path
from datetime import datetime

pending_file = Path(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\pending_names.json')
processed_file = Path(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\processed_names.json')

with open(pending_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 翻译映射
translations = {
    'Even In Arcadia Sleep Token Band Logo Sticker With': 'Sleep Token 乐队 Logo 贴纸',
    '131pcs Base Ten Blocks for Math - Place Value': '131件套数学十进制教具 - 位值学习',
    'JoyCat Jumbo Triangular Easy-Grip Kids Crayons': 'JoyCat 大号三角易握儿童蜡笔',
    'Faux Pearl Decorated Necklace & Earrings': '人造珍珠装饰项链耳环套装',
    'EAMTI 1.5CT 925 Sterling Silver Wedding Band': 'EAMTI 1.5克拉925纯银婚戒',
    'Jewelry Mystery Box with Random Fine Jewelry': '珠宝神秘盒 - 随机精品首饰',
    '2 Pairs Earrings for Women Hypoallergenic': '女士防过敏耳环2对装',
    "Women's Boho Style Alloy Chain Fashion Necklace Set": '女士波西米亚风合金项链套装',
    '7-Piece Bohemian Earthy Vacation Style': '7件套波西米亚度假风首饰',
    'Elegant imitation pearl necklace for women': '女士优雅仿珍珠项链',
    'Fashion Vintage Stainless Steel Letter Bracelet': '时尚复古不锈钢字母手镯',
    'Unisex Zodiac Necklace': '中性款星座项链',
    "Men's Accessories Upgrade": '男士配饰升级套装',
    'KissYan Initial Letter Pendant Necklace for Men & Women': 'KissYan 中性款首字母吊坠项链',
    "Women's 14K Gold Plated Vintage Spoon Ring": '女士14K镀金复古勺形戒指',
    'GLD 14k White Gold Plated Rope Bracelet': 'GLD 14K镀白金绳纹手镯',
    'Elegant Crystal Dangle Teardrop Earrings for Women': '女士优雅水晶泪滴耳环',
    'Star Wars Darth Vader Retractable Badge Reel ID': '星球大战达斯维达伸缩证件夹',
    'Writech Multi Colored Liquid Ink Rollerball Pens 0.': 'Writech 多色液态墨水中性笔',
    "Always Coming Back Funny Father's Day Card": '父亲节趣味贺卡',
    'Loteria Custom Decal Credit Card Cover Vinyl Skin Sticker': 'Loteria 定制信用卡贴纸',
    'Raiders Football Splatter Design Glitter Badge Reel': '突袭者队橄榄球闪光证件夹',
    'The Bible Made Clear Notebook': '圣经学习笔记本',
    'TBC The Best Crafts 120-Color Acrylic Markers': 'TBC 120色丙烯马克笔',
    'Glitter My Badge funny get that bread badge reel': '趣味面包主题闪光证件夹',
    'Triangle Medal Holder': '三角形奖牌展示架',
    '10 Pcs Book Lover Collector Pin Set Book Shelf': '10件套书籍爱好者收藏徽章',
    '104 pages of 75 soft challenge notebooks&planners': '75页软挑战笔记本计划本',
    'Washed Vintage Loose Tapered Work Pants': '水洗复古宽松锥形工装裤',
    'Later Alligator Shirt': '鳄鱼主题趣味T恤',
    'Retro Heavy Limited Sannin Jraija Code Letter': '复古限量版忍者主题字母T恤',
    '4th Strong Lion With Cross Christian Faith': '第四面狮子十字架基督教信仰T恤',
    'Custom Birthday ShirtReel Cool Dad T-Shirt': '生日定制酷爸爸T恤',
    "Retro Racing Style Men's Casual Shorts": '男士复古赛车风格休闲短裤',
    'Y2K Fashion Cartoon Print Loose-Fit T-Shirt for': 'Y2K风卡通印花宽松T恤',
    "Plus Size Men's Letter Print Tee & Shorts Set": '大码男士字母印花T恤短裤套装',
    'Fashion Casual Plain Sleeveless Tank Tops': '时尚休闲纯色无袖背心',
    "Men's Floral Printed Short Sleeve Shirt": '男士花卉印花短袖衬衫',
    "Men's new leopard print casual loose trend hoodie": '男士新款豹纹休闲连帽衫',
    'Unisex Striped Wide Leg Pants': '中性款条纹阔腿裤',
    "Men's Classic Korean Style Fashion Streetwear High": '男士韩风时尚街头风',
    "Men's Casual Jacket with Mexican Letter Print": '男士墨西哥字母印花夹克',
    "Women's Gentle Warm Gradient Long Scarf Headscarf": '女士温柔暖色渐变长围巾',
    '1 High Waist Button Fly Wide Leg Pants Women': '女士高腰纽扣阔腿裤',
    "Men's High-Quality Dubai Khftan Thioub": '男士高品质迪拜长袍',
    'Middle Eastern Ramadan Eid Islamic Abaya': '中东斋月伊斯兰长袍',
    "Boys' African Dashiki Kaftan Set Outfits": '男童非洲风达西基长袍套装',
    "Women's Colorblock Shawl": '女士拼色披肩',
    'Slant Shoulder Collar Waist Solid Color Wide Leg': '斜肩收腰纯色阔腿裤套装',
    "Women's Elegant Pleated Robe Caftan": '女士优雅褶皱长袍'
}

processed_items = []
for item in data['items']:
    translated_name = translations.get(item['name'], item['name'][:20] + '（待人工翻译）')
    processed_items.append({
        'id': item['id'],
        'name': item['name'],
        'translated_name': translated_name
    })

result = {
    'batch_id': data['batch_id'],
    'processed_at': datetime.now().isoformat(),
    'count': len(processed_items),
    'items': processed_items
}

processed_file.parent.mkdir(parents=True, exist_ok=True)
with open(processed_file, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f'[OK] 已处理 {len(processed_items)} 条翻译')
