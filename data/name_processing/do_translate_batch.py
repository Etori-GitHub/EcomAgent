#!/usr/bin/env python3
"""批量翻译商品名称 - 简化版"""
import json
import re

def translate_name(name):
    """翻译商品名称为简洁中文"""
    name = name.strip()
    
    # 苹果产品
    if 'Apple' in name or 'iPad' in name or 'iPhone' in name or 'AirPods' in name or 'MacBook' in name or 'AirTag' in name or 'Watch' in name:
        if 'iPhone 16 Pro Max' in name: return '苹果iPhone 16 Pro Max'
        if 'iPhone 16 Pro' in name: return '苹果iPhone 16 Pro'
        if 'iPhone 16e' in name: return '苹果iPhone 16e'
        if 'iPhone 15 Pro Max' in name: return '苹果iPhone 15 Pro Max'
        if 'iPhone 15 Pro' in name: return '苹果iPhone 15 Pro'
        if 'iPhone 15' in name: return '苹果iPhone 15'
        if 'iPhone 14 Pro Max' in name: return '苹果iPhone 14 Pro Max'
        if 'iPhone 14 Plus' in name: return '苹果iPhone 14 Plus'
        if 'iPhone 14 Pro' in name: return '苹果iPhone 14 Pro'
        if 'iPhone 14' in name: return '苹果iPhone 14'
        if 'iPhone 13 Mini' in name: return '苹果iPhone 13 Mini'
        if 'iPhone 13' in name: return '苹果iPhone 13'
        if 'iPhone 12' in name: return '苹果iPhone 12'
        if 'iPhone SE 3rd' in name or 'iPhone SE 3' in name: return '苹果iPhone SE 3代'
        if 'iPhone SE 2nd' in name or 'iPhone SE 2' in name: return '苹果iPhone SE 2代'
        if 'iPhone SE' in name: return '苹果iPhone SE'
        if 'AirPods Pro 3' in name: return '苹果AirPods Pro 3'
        if 'AirPods Pro' in name: return '苹果AirPods Pro'
        if 'AirPods 4' in name: return '苹果AirPods 4'
        if 'AirPods 2' in name: return '苹果AirPods 2'
        if 'AirPods' in name: return '苹果AirPods'
        if 'AirTag 2nd' in name or 'AirTag 2' in name: return '苹果AirTag 2代'
        if 'AirTag' in name: return '苹果AirTag'
        if 'Watch Series 11' in name: return '苹果Watch Series 11'
        if 'Watch Series 7' in name: return '苹果Watch Series 7'
        if 'MacBook Air M5' in name:
            if '15' in name: return '苹果MacBook Air M5 15寸'
            return '苹果MacBook Air M5 13寸'
        if 'MacBook Pro M5' in name: return '苹果MacBook Pro M5'
        if 'MacBook Neo' in name: return '苹果MacBook Neo 13寸'
        if 'iPad 11-inch' in name or 'iPad 11寸' in name: return '苹果iPad 11寸'
        if 'iPad 2021' in name: return '苹果iPad 2021 10.2寸'
        if 'iPad 2020' in name: return '苹果iPad 2020 10.2寸'
        if 'iPad' in name: return '苹果iPad 10.2寸'
        if 'EarPods' in name: return '苹果EarPods耳机'
    
    # 亚马逊产品
    if 'Amazon' in name or 'Fire' in name or 'Echo' in name or 'Kindle' in name or 'eero' in name:
        if 'Fire TV Stick 4K Max' in name: return '亚马逊Fire TV 4K Max'
        if 'Fire TV Stick 4K Plus' in name: return '亚马逊Fire TV 4K Plus'
        if 'Fire TV Stick 4K Select' in name: return '亚马逊Fire TV 4K Select'
        if 'Fire TV Stick 4K' in name: return '亚马逊Fire TV 4K'
        if 'Fire TV Stick HD' in name: return '亚马逊Fire TV HD'
        if 'Fire HD 10' in name: return '亚马逊Fire HD 10平板'
        if 'Fire 7' in name: return '亚马逊Fire 7儿童平板'
        if 'Echo Show 5' in name: return '亚马逊Echo Show 5'
        if 'Echo Dot' in name: return '亚马逊Echo Dot'
        if 'Kindle Paperwhite' in name: return '亚马逊Kindle Paperwhite'
        if 'Kindle' in name: return '亚马逊Kindle'
        if 'eero 6' in name: return '亚马逊eero 6扩展器'
        if 'Amazon Basics' in name or 'Amazon Brand' in name:
            if 'Microfiber' in name or 'Cleaning Cloth' in name: return '亚马逊超细纤维布'
            if 'Toilet Paper' in name: return '亚马逊卫生纸'
            if 'Paper Towels' in name: return '亚马逊纸巾'
            if 'Cotton Swabs' in name: return '亚马逊双头棉签'
            if 'Cotton Rounds' in name: return '亚马逊化妆棉'
            if 'Hand Soap' in name: return '亚马逊洗手液'
            if 'Batteries' in name: return '亚马逊电池'
            if 'Paper' in name: return '亚马逊打印纸'
            if 'File Folders' in name: return '亚马逊文件夹'
            if 'Hanging File' in name: return '亚马逊挂式文件夹'
            if 'Sheet Protectors' in name: return '亚马逊文件保护套'
            if 'Laminating' in name: return '亚马逊塑封膜'
            if 'Dumbbell' in name: return '亚马逊哑铃'
            if 'Note Pads' in name: return '亚马逊笔记本'
            return '亚马逊品牌'
        if 'Gift Card' in name or 'eGift Card' in name: return '亚马逊电子礼品卡'
        if 'Physical Gift Card' in name: return '亚马逊实体礼品卡'
        if 'Printable Gift Card' in name: return '亚马逊可打印礼品卡'
        if 'Gift Card Balance' in name: return '亚马逊礼品卡充值'
    
    # Ring/Blink 智能家居
    if 'Ring' in name:
        if 'Battery Doorbell' in name: return 'Ring电池门铃'
        if 'Video Doorbell' in name: return 'Ring视频门铃'
        if 'Indoor Cam Plus' in name: return 'Ring室内摄像头Plus'
        if 'Indoor Cam' in name: return 'Ring室内摄像头'
        if 'Outdoor Cam Plus' in name: return 'Ring户外摄像头Plus'
        if 'Outdoor Cam' in name: return 'Ring户外摄像头'
        if 'Spotlight Cam Plus' in name: return 'Ring聚光灯摄像头Plus'
        if 'Spotlight Cam' in name: return 'Ring聚光灯摄像头'
        if 'Chime' in name: return 'Ring门铃响铃器'
        return 'Ring智能门铃'
    
    if 'Blink' in name:
        if 'Outdoor 4' in name: return 'Blink Outdoor 4摄像头'
        if 'Video Doorbell' in name: return 'Blink视频门铃'
        if 'Mini 2K' in name: return 'Blink Mini 2K+摄像头'
        if 'Plus plan' in name or 'Plus Plan' in name: return 'Blink Plus订阅计划'
        if 'AI plan' in name: return 'Blink AI订阅计划'
        return 'Blink智能家居'
    
    # 制冰机
    if 'Ice Maker' in name:
        if 'Nugget' in name:
            if 'EUHOMY' in name: return 'EUHOMY颗粒制冰机'
            if 'Kismile' in name: return 'Kismile颗粒制冰机'
            if 'Antarctic Star' in name: return 'Antarctic Star颗粒制冰机'
            return '颗粒制冰机'
        if 'EUHOMY' in name: return 'EUHOMY制冰机'
        if 'DUMOS' in name: return 'DUMOS制冰机'
        if 'NEWBULIG' in name: return 'NEWBULIG制冰机'
        if 'Silonn' in name: return 'Silonn制冰机'
        if 'COWSAR' in name: return 'COWSAR制冰机'
        if 'OLIXIS' in name: return 'OLIXIS制冰机'
        if 'Igloo' in name: return 'Igloo便携制冰机'
        if 'Antarctic Star' in name: return 'Antarctic Star制冰机'
        return '制冰机'
    
    # 小冰箱/冷柜
    if 'Mini Fridge' in name or 'Freezer' in name:
        if 'Frostorm' in name: return 'Frostorm 3.2立方小冰箱'
        if 'Midea' in name: return 'Midea冷柜'
        return '小冰箱'
    
    # 三星
    if 'Samsung' in name:
        if 'Galaxy S24' in name: return '三星Galaxy S24 Ultra'
        if 'Refrigerator' in name: return '三星冰箱滤芯'
        return '三星产品'
    
    # TP-Link
    if 'TP-Link' in name or 'Deco' in name:
        if 'WiFi 7' in name: return 'TP-Link WiFi 7路由器'
        if 'WiFi 6' in name: return 'TP-Link WiFi 6路由器'
        if 'Deco' in name: return 'TP-Link Deco路由器'
        return 'TP-Link路由器'
    
    # Roku
    if 'Roku' in name:
        if 'Streaming Stick 4K' in name: return 'Roku 4K电视棒'
        if 'Streaming Stick HD' in name: return 'Roku HD电视棒'
        if 'Remote' in name: return 'Roku电视遥控器'
        return 'Roku电视棒'
    
    # Anker
    if 'Anker' in name:
        if 'USB C Hub' in name or 'Docking Station' in name: return 'Anker USB-C扩展坞'
        if 'Charger' in name: return 'Anker充电器'
        return 'Anker配件'
    
    # UGREEN
    if 'UGREEN' in name:
        if 'USB C Hub' in name: return 'UGREEN USB-C扩展坞'
        return 'UGREEN配件'
    
    # 护肤品/化妆品
    if 'Neutrogena' in name:
        if 'Sunscreen' in name: return 'Neutrogena防晒霜SPF70'
        if 'Makeup Remover' in name: return 'Neutrogena卸妆湿巾'
        return 'Neutrogena护肤品'
    
    if 'Maybelline' in name: return 'Maybelline睫毛膏'
    if 'eos ' in name.lower():
        if 'Body Wash' in name: return 'eos沐浴露香草味'
        if 'Body Lotion' in name: return 'eos身体乳香草味'
        return 'eos护肤品'
    
    if 'The Ordinary' in name: return 'The Ordinary甘醇酸爽肤水'
    if 'Paula\'s Choice' in name: return 'Paula\'s Choice BHA爽肤水'
    if 'EltaMD' in name: return 'EltaMD防晒霜'
    if 'BIODANCE' in name: return 'BIODANCE胶原蛋白面膜'
    if 'Blue Lizard' in name: return 'Blue Lizard防晒霜SPF50'
    if 'Mighty Patch' in name: return 'Mighty Patch痘痘贴'
    if 'Clean Skin Club' in name: return 'Clean Skin Club毛巾'
    if 'Nizoral' in name: return 'Nizoral去屑洗发水'
    if 'PanOxyl' in name: return 'PanOxyl 10%祛痘洗面奶'
    if 'Aquaphor' in name: return 'Aquaphor修复霜'
    if 'Medicube' in name: return 'Medicube零毛孔爽肤棉片2.0'
    
    # 纸尿裤/婴儿用品
    if 'Pampers' in name:
        if 'Swim' in name: return 'Pampers游泳纸尿裤'
        if 'Training' in name: return 'Pampers训练裤'
        if 'Sensitive' in name: return 'Pampers敏感湿巾'
        return 'Pampers纸尿裤'
    
    if 'Huggies' in name:
        if 'Little Swimmers' in name or 'Swim' in name: return 'Huggies游泳纸尿裤'
        if 'Natural Care' in name: return 'Huggies湿巾'
        if 'Simply Clean' in name: return 'Huggies清洁湿巾'
        if 'Little Snugglers' in name: return 'Huggies新生儿纸尿裤'
        if 'Diapers' in name: return 'Huggies纸尿裤'
        return 'Huggies纸尿裤'
    
    if 'WaterWipes' in name: return 'WaterWipes湿巾'
    if 'Honest' in name:
        if 'Wipes' in name: return 'Honest湿巾'
        if 'Shampoo' in name: return 'Honest二合一洗发水'
        return 'Honest婴儿用品'
    
    if 'Desitin' in name: return 'Desitin护臀膏'
    if 'Dr. Brown' in name: return 'Dr. Brown\'s奶嘴'
    if 'Momcozy' in name: return 'Momcozy洗涤块'
    if 'Gaiatop' in name: return 'Gaiatop婴儿车风扇'
    
    # 机油/汽车用品
    if 'Mobil' in name: return 'Mobil 0W-20机油'
    if 'Valvoline' in name:
        if '0W-20' in name: return 'Valvoline 0W-20机油'
        if '5W-30' in name: return 'Valvoline 5W-30机油'
        return 'Valvoline机油'
    if 'Meguiar' in name: return 'Meguiar\'s抛光剂'
    if 'NOCO' in name:
        if 'GB40' in name: return 'NOCO GB40启动电源'
        if 'GENIUS' in name: return 'NOCO GENIUS1充电器'
        return 'NOCO汽车配件'
    if 'AstroAI' in name: return 'AstroAI充气泵'
    if 'Chemical Guys' in name: return 'Chemical Guys清洁剂'
    if 'CERAKOTE' in name: return 'CERAKOTE大灯修复套装'
    if 'CARORY' in name: return 'CARORY空调滤芯'
    if 'EcoNour' in name: return 'EcoNour遮阳帘'
    
    # 哈利波特
    if 'Harry Potter' in name:
        if 'Deathly Hallows' in name: return '哈利波特死亡圣器'
        if 'Sorcerer' in name: return '哈利波特魔法石'
        return '哈利波特'
    
    # 小说/书籍
    if 'Dungeon Crawler Carl' in name:
        if 'Book 8' in name or 'Parade of Horribles' in name: return 'Dungeon Crawler Carl 8'
        if 'Book 7' in name or 'Inevitable Ruin' in name: return 'Dungeon Crawler Carl 7'
        if 'Book 6' in name or 'Eye of the Bedlam Bride' in name: return 'Dungeon Crawler Carl 6'
        if 'Book 5' in name or 'Butcher\'s Masquerade' in name: return 'Dungeon Crawler Carl 5'
        if 'Book 4' in name or 'Gate of the Feral Gods' in name: return 'Dungeon Crawler Carl 4'
        if 'Book 3' in name or 'Dungeon Anarchist' in name: return 'Dungeon Crawler Carl 3'
        if 'Book 2' in name or 'Doomsday Scenario' in name: return 'Dungeon Crawler Carl 2'
        return 'Dungeon Crawler Carl'
    
    if 'The Deal' in name: return 'The Deal小说'
    if 'The Mistake' in name: return 'The Mistake小说'
    if 'The Score' in name: return 'The Score小说'
    if 'The Goal' in name: return 'The Goal小说'
    if 'The Legacy' in name: return 'The Legacy小说'
    if 'The Divorce' in name: return 'The Divorce小说'
    if 'Yesteryear' in name: return 'Yesteryear小说'
    if 'Project Hail Mary' in name: return 'Project Hail Mary小说'
    if 'Theo of Golden' in name: return 'Theo of Golden小说'
    if 'The Correspondent' in name: return 'The Correspondent小说'
    if 'The Calamity Club' in name: return 'The Calamity Club小说'
    if 'The Let Them Theory' in name: return 'The Let Them Theory'
    if 'Remarkably Bright' in name: return 'Remarkably Bright Creatures'
    if 'Strangers' in name: return 'Strangers回忆录'
    if 'Stitched' in name: return 'Stitched小说'
    if 'Oh, the Places' in name: return 'Oh, the Places You\'ll Go!'
    if 'Very Hungry Caterpillar' in name: return '好饿的毛毛虫'
    if 'Rainbow Fish' in name: return '彩虹鱼'
    if 'I Love You to the Moon' in name: return 'I Love You to the Moon'
    if 'Primal Hunter' in name: return 'The Primal Hunter 14'
    
    # 望远镜
    if 'Binoculars' in name:
        if 'Vortex' in name:
            if 'Crossfire' in name: return 'Vortex Crossfire HD望远镜'
            if 'Triumph' in name: return 'Vortex Triumph HD望远镜'
            if 'Diamondback' in name: return 'Vortex Diamondback HD望远镜'
            return 'Vortex望远镜'
        if 'Hontry' in name: return 'Hontry双筒望远镜'
        if 'Aurosports' in name: return 'Aurosports双筒望远镜'
        if 'Compact' in name: return '便携双筒望远镜'
        if 'Kids' in name: return '儿童双筒望远镜'
        if 'UHD' in name:
            if '15x55' in name: return '15x55 UHD双筒望远镜'
            if '12x50' in name: return '12x50 UHD双筒望远镜'
        if 'HD' in name:
            if '15x52' in name: return '15x52 HD双筒望远镜'
        if 'Mini' in name: return '迷你双筒望远镜'
        return '双筒望远镜'
    
    if 'Telescope' in name:
        if 'Gskyer' in name: return 'Gskyer望远镜'
        return '望远镜'
    
    if 'Microscope' in name:
        if 'Elikliv' in name: return 'Elikliv数字显微镜'
        return '显微镜'
    
    # 音乐专辑
    if 'Thriller' in name: return 'Thriller专辑'
    if 'Off The Wall' in name: return 'Off The Wall专辑'
    if 'Bad' in name: return 'Bad专辑'
    if 'Short n\' Sweet' in name: return 'Short n\' Sweet专辑'
    if 'Back to Black' in name: return 'Back to Black专辑'
    if 'The Great Divide' in name: return 'The Great Divide专辑'
    if 'Rumours' in name: return 'Rumours专辑'
    if 'The Art of Loving' in name: return 'The Art of Loving专辑'
    if 'Number Ones' in name: return 'Number Ones专辑'
    if 'Abbey Road' in name: return 'Abbey Road周年版'
    if 'Currents' in name: return 'Currents专辑'
    if 'Cinematic' in name: return 'Cinematic专辑'
    if 'Dark Side of the Moon' in name: return 'Dark Side of the Moon'
    if 'Prizefighter' in name: return 'Prizefighter专辑'
    if 'The Romantic' in name: return 'The Romantic专辑'
    if 'Dandelion' in name: return 'Dandelion专辑'
    if 'Red' in name: return 'Red专辑'
    if 'DeBÍ TiRAR' in name: return 'DeBÍ TiRAR MáS FOToS'
    
    # 手机壳/配件
    if 'iPhone' in name and ('Case' in name or 'Protector' in name or 'Screen' in name):
        if 'SUPFINE' in name: return 'SUPFINE iPhone 17手机壳'
        if 'FNTCASE' in name:
            if '17' in name: return 'FNTCASE iPhone 17手机壳'
            return 'FNTCASE iPhone 15手机壳'
        if 'PEHAEL' in name: return 'PEHAEL iPhone 17钢化膜'
        if 'Miracase' in name:
            if '17e' in name: return 'Miracase iPhone 17e手机壳'
            return 'Miracase磁吸手机壳'
        if 'TOCOL' in name: return 'TOCOL iPhone 15钢化膜'
        if 'Ailun' in name: return 'Ailun iPhone 16隐私膜'
        if 'SuydanBox' in name: return 'SuydanBox iPhone 17手机壳'
        return 'iPhone配件'
    
    if 'Charger' in name and ('USB' in name or 'Type C' in name or 'Fast' in name):
        if 'INIU' in name: return 'INIU 45W充电宝'
        if 'VJYUIJAY' in name: return 'VJYUIJAY 65W充电器'
        if 'MacBook' in name: return 'MacBook Pro充电器'
        if 'HP' in name: return 'HP笔记本充电器'
        return '充电器'
    
    # 服装
    if 'Hanes' in name:
        if 'Underwear' in name: return 'Hanes男士内裤'
        if 'Undershirt' in name: return 'Hanes男士汗衫'
        return 'Hanes内衣'
    
    if 'Gildan' in name: return 'Gildan男士T恤多件装'
    if 'Carhartt' in name: return 'Carhartt经典T恤'
    if 'Wrangler' in name: return 'Wrangler男士工装短裤'
    if 'Crocs' in name:
        if 'Kid' in name: return 'Crocs儿童洞洞鞋'
        return 'Crocs洞洞鞋'
    if 'KuaiLu' in name: return 'KuaiLu女士拖鞋'
    if 'Water Shoes' in name: return '男女涉水鞋'
    
    if 'LetsJoli' in name: return 'LetsJoli女士内衣'
    if 'COOFANDY' in name: return 'COOFANDY男士亚麻衬衫'
    if 'Nippies' in name: return 'Nippies乳贴'
    if 'OEAK' in name:
        if 'Jelly' in name: return 'OEAK果冻内衣'
        return 'OEAK女士内衣'
    if 'AUTOMET' in name: return 'AUTOMET女士背心'
    if 'ANRABESS' in name: return 'ANRABESS女士上衣'
    if 'CHICME' in name: return 'CHICME女士背心'
    if 'OFEEFAN' in name: return 'OFEEFAN女士上衣'
    if 'COCOMARTS' in name: return 'COCOMARTS果冻内衣'
    
    # 纪念币
    if '250th' in name or '250 Anniversary' in name:
        if 'Army' in name: return '美国陆军250周年纪念币'
        if 'Veteran' in name: return '250周年退伍军人纪念币'
        if 'Bill' in name: return '250周年2美元纸币'
        return '美国250周年纪念币'
    if 'Coin' in name:
        if 'Wheat Penn' in name: return '麦穗便士收藏'
        if 'Morgan' in name: return '摩根银元'
        if 'World Coins' in name: return '世界硬币混合装'
        if 'Gamer' in name: return '游戏决策硬币'
        if 'Indian Head' in name: return '1877印第安人头像便士'
        if 'Final Cent' in name: return '最终便士纪念币'
        if 'Liberty' in name: return '1795自由女神硬币复制品'
        if 'Quarters' in name: return '250周年纪念硬币套装'
        if 'Sixpence' in name: return '1954-1970英国六便士'
        return '纪念币'
    if '2026' in name and len(name) < 10: return '2026纪念品'
    
    # 礼品卡
    if 'Gift Card' in name:
        if 'Amazon' in name:
            if 'Physical' in name: return '亚马逊实体礼品卡'
            if 'Printable' in name: return '亚马逊可打印礼品卡'
            return '亚马逊电子礼品卡'
        if 'Apple' in name: return '苹果礼品卡'
        if 'DoorDash' in name: return 'DoorDash礼品卡'
        if 'Uber' in name: return 'Uber礼品卡'
        if 'Visa' in name:
            if '$100' in name: return 'Visa礼品卡$100'
            if '$50' in name: return 'Visa礼品卡$50'
            if '$200' in name: return 'Visa礼品卡$200'
            return 'Visa礼品卡'
        if 'PlayStation' in name: return 'PlayStation礼品卡'
        if 'Xbox' in name: return 'Xbox礼品卡'
        if 'Nintendo' in name: return '任天堂礼品卡'
        if 'Google Play' in name: return 'Google Play礼品卡'
        if 'Starbucks' in name: return '星巴克礼品卡'
        if 'Roblox' in name: return 'Roblox礼品卡'
        return '礼品卡'
    
    # 游戏
    if 'Minecraft' in name: return '我的世界游戏'
    if 'Geometry Dash' in name: return '几何冲刺游戏'
    if 'Noob Ninja' in name: return 'Noob Ninja游戏'
    if 'Runaway Maze' in name: return 'Runaway Maze游戏'
    if 'Snack Sprint' in name: return 'Snack Sprint游戏'
    if 'Bucket Crusher' in name: return 'Bucket Crusher游戏'
    if 'Monster Uplift' in name: return 'Monster Uplift游戏'
    if 'Dummy Break' in name: return 'Dummy Break游戏'
    if 'Shift Race' in name: return 'Shift Race赛车游戏'
    if 'Magic Tiles' in name: return 'Magic Tiles 3 PRO'
    if 'Naughty Baby' in name: return 'Naughty Baby游戏'
    if 'Mental Might' in name: return 'Mental Might游戏'
    if 'Bowman' in name: return 'Bowman\'s Journey游戏'
    if 'Katana Clash' in name: return 'Katana Clash游戏'
    if 'Titans Legion' in name: return 'Titans Legion游戏'
    if 'Calm Energy' in name: return 'Calm Energy健身'
    if 'Rhythm' in name: return 'Rhythm运动控制'
    if 'Challenge' in name: return 'Challenge游戏'
    if 'Jurassic Merge' in name: return 'Jurassic Merge游戏'
    if 'Blade Master' in name: return 'Blade Master游戏'
    
    # 手工艺/文具
    if 'Essential Oil' in name:
        if 'Peppermint' in name: return 'Peppermint精油'
        if 'Tea Tree' in name: return '100%茶树精油'
        if 'Rosemary' in name: return '100%迷迭香精油'
        return '精油'
    if 'Markers' in name or 'Paint Markers' in name:
        if 'ARTISTRO' in name: return 'ARTISTRO 36色马克笔'
        if 'Bandle' in name: return 'Bandle粉笔马克笔'
        return '马克笔'
    if 'Scissors' in name:
        if 'iBayam' in name: return 'iBayam剪刀3件套'
        return '剪刀'
    if 'Glue' in name:
        if 'B7000' in name: return 'B7000珠宝胶水'
        if 'Elmer' in name: return 'Elmer\'s紫色胶棒'
        if 'Fabric' in name: return 'FITTDYHE布料胶水'
        return '胶水'
    if 'Tape' in name:
        if 'Secopad' in name: return 'Secopad胶带'
        if 'ScotchBlue' in name: return 'ScotchBlue美纹纸胶带'
        if 'Double Sided' in name: return 'EZlifego双面胶'
        if 'VELCRO' in name: return 'VELCRO强力魔术贴'
        if 'Scotch' in name: return 'Scotch胶带'
        if 'Packing' in name: return 'Scotch封箱胶带'
        return '胶带'
    if 'Yarn' in name: return 'RED HEART毛线白色'
    if 'Tie Dye' in name: return 'Tulip扎染套装'
    if 'Cardstock' in name: return 'Neenah卡纸'
    if 'Paper' in name:
        if 'Copy' in name or 'Printer' in name: return '亚马逊打印纸'
        if 'Hammermill' in name: return 'Hammermill打印纸'
        return '纸张'
    if 'Sharpie' in name: return 'Sharpie记号笔'
    if 'BIC' in name: return 'BIC圆珠笔'
    if 'Gel Pens' in name: return 'Ddaowanx中性笔'
    if 'Desk Pad' in name: return 'Aothia桌垫'
    
    # 汽车配件
    if 'Car Air Freshener' in name or 'Drift' in name: return '车载香薰'
    if 'Car Mount' in name or 'Magsafe' in name: return 'Kaistyle磁吸支架'
    if 'Cabin Air Filter' in name: return 'CARORY空调滤芯'
    if 'Headlight Restoration' in name: return 'CERAKOTE大灯修复套装'
    
    # 家居清洁
    if 'Paper Towels' in name:
        if 'Bounty' in name: return 'Bounty纸巾'
        if 'Sparkle' in name: return 'Sparkle纸巾'
        if 'Amazon' in name: return '亚马逊纸巾'
        return '纸巾'
    if 'Toilet Paper' in name:
        if 'Scott' in name: return 'Scott卫生纸'
        if 'Angel Soft' in name: return 'Angel Soft卫生纸'
        if 'Charmin' in name: return 'Charmin卫生纸'
        if 'Quilted Northern' in name: return 'Quilted Northern卫生纸'
        return '卫生纸'
    if 'Wipes' in name:
        if 'DUDE' in name: return 'DUDE Wipes湿巾'
        if 'Cottonelle' in name: return 'Cottonelle湿巾'
        if 'Pet Wipes' in name: return 'Earth Rated宠物湿巾'
        return '湿巾'
    if 'Microfiber' in name or 'Cleaning Cloth' in name:
        if 'USANOOKS' in name: return 'USANOOKS超细纤维布'
        return '超细纤维布'
    if 'Squeegee' in name: return '不锈钢刮水器'
    if 'Hand Soap' in name:
        if 'MRS. MEYER' in name: return 'MRS. MEYER\'S洗手液'
        return '洗手液'
    if 'Lint Roller' in name: return 'Swihauk粘毛器'
    
    # 厨房用品
    if 'Kitchen Scale' in name or 'Food Scale' in name:
        if 'Etekcity' in name: return 'Etekcity厨房秤'
        return '厨房秤'
    if 'Meat Thermometer' in name:
        if 'Alpha Grillers' in name: return 'Alpha Grillers肉类温度计'
        if 'TempPro' in name: return 'TempPro肉类温度计'
        return '肉类温度计'
    if 'Tumbler' in name or 'Water Bottle' in name:
        if 'Stanley' in name: return 'Stanley保温杯'
        if 'Owala' in name:
            if 'SmoothSip' in name: return 'Owala SmoothSip保温杯'
            return 'Owala保温杯'
        if 'HydroJug' in name: return 'HydroJug水瓶'
        return '保温杯'
    if 'Kitchen Shears' in name: return 'KitchenAid厨房剪刀'
    if 'Toaster' in name: return 'bella烤面包机'
    if 'Air Fryer Paper' in name: return '空气炸锅纸垫'
    if 'Can Opener' in name: return 'KitchenAid开罐器'
    if 'Dish Cloths' in name: return 'Homaxy洗碗布'
    if 'Parchment Paper' in name: return 'Reynolds烘焙纸'
    if 'Blender' in name: return 'Ninja搅拌机'
    if 'Milk Frother' in name: return 'Zulay打奶器'
    if 'Cheesecloth' in name: return 'Socomi桌旗'
    
    # 食品饮料
    if 'CELSIUS' in name: return 'CELSIUS能量饮料'
    if 'Nespresso' in name: return 'Nespresso胶囊咖啡'
    if 'Premier Protein' in name: return 'Premier蛋白奶昔'
    if 'Monster Energy' in name: return 'Monster能量饮料'
    if 'Core Power' in name: return 'Core Power蛋白奶昔'
    if 'Bloom Nutrition' in name: return 'Bloom气泡能量饮料'
    if 'Sparkling Ice' in name: return 'Sparkling Ice气泡水'
    if 'Diet Coke' in name: return '健怡可乐'
    if 'Propel' in name: return 'Propel运动饮料'
    if 'Lavazza' in name: return 'Lavazza咖啡豆'
    if 'Banana' in name: return '香蕉'
    if 'Blueberries' in name: return '蓝莓'
    if 'Avocado' in name: return '牛油果'
    if 'Strawberries' in name: return '草莓'
    if 'Tomato' in name: return '小番茄'
    if 'PUR Gum' in name: return 'PUR口香糖'
    if 'DaVinci' in name: return 'DaVinci糖浆'
    
    # 宠物用品
    if 'Cat Litter' in name:
        if 'Dr. Elsey' in name: return 'Dr. Elsey\'s猫砂'
        if 'ARM & HAMMER' in name: return 'ARM & HAMMER猫砂'
        if 'Fresh Step' in name: return 'Fresh Step猫砂'
        return '猫砂'
    if 'Dog Treats' in name or 'Dog Food' in name:
        if 'Purina' in name: return 'Purina狗粮'
        if 'Blue Buffalo' in name: return 'Blue Buffalo狗粮'
        if 'Milk-Bone' in name: return 'Milk-Bone狗零食'
        if 'Pedigree' in name: return 'Pedigree狗零食'
        if 'Pur Luv' in name: return 'Pur Luv狗零食'
        return '狗粮'
    if 'Cat Treats' in name or 'Cat Food' in name:
        if 'Purina' in name: return 'Purina猫粮'
        if 'Sheba' in name: return 'Sheba猫粮'
        if 'INABA' in name: return 'INABA猫零食'
        if 'Temptations' in name: return 'Temptations猫零食'
        if 'FortiFlora' in name: return 'FortiFlora猫用益生菌'
        return '猫粮'
    if 'Poop Bags' in name: return 'Earth Rated拾便袋'
    if 'Greenies' in name: return 'Greenies狗零食'
    if 'Dog Wrap' in name: return 'HONEY CARE狗尿垫'
    if 'Potty Pads' in name: return '亚马逊狗尿垫'
    
    # 园艺/户外
    if 'Bird Food' in name:
        if 'Wagner' in name: return 'Wagner鸟食'
        if 'Kaytee' in name: return 'Kaytee蜂鸟花蜜'
        return '鸟食'
    if 'Plant Food' in name or 'Fertilizer' in name:
        if 'Miracle-Gro' in name: return 'Miracle-Gro植物营养'
        return '植物营养'
    if 'Insect Killer' in name or 'Ant Killer' in name:
        if 'Ortho' in name: return 'Ortho杀虫剂'
        if 'Terro' in name: return 'Terro杀蚁剂'
        return '杀虫剂'
    if 'Fly Trap' in name: return 'Zevo捕蝇器'
    if 'Weed Killer' in name: return 'Roundup除草剂'
    if 'Mosquito' in name: return 'Summit蚊子防治'
    if 'Neem Oil' in name: return 'Bonide印楝油'
    if 'Garden Hose' in name or 'Hose Nozzle' in name: return 'AUTOMAN水管喷头'
    if 'Sprayer' in name: return 'Chapin喷雾器'
    if 'Seeds' in name: return 'HOME GROWN花种子'
    if 'Lime' in name: return 'First Saturday石灰'
    if 'Deer Corn' in name: return '鹿玉米'
    if 'UDC Parts' in name: return 'UDC John Deere配件'
    
    # 派对用品
    if 'Balloons' in name:
        if 'Bezente' in name: return 'Bezente彩色气球'
        if 'PartyWoo' in name:
            if 'Pink' in name: return 'PartyWoo粉色气球'
            return 'PartyWoo黑色气球'
        return '气球'
    if 'Glow Sticks' in name: return 'PartySticks荧光棒'
    if 'Candles' in name:
        if 'Odor Eliminating' in name: return '除味蜡烛套装'
        return '蜡烛'
    if 'Fire Blanket' in name: return 'Supa Ant防火毯'
    if 'Welding Blanket' in name: return 'Supa Ant焊接毯'
    if 'Bubble Machine' in name: return '泡泡机'
    if 'Balloon Pump' in name: return 'IDAODAN气球泵'
    
    # 玩具
    if 'Squishy' in name:
        if 'Midou' in name: return 'Midou解压玩具'
        return '解压玩具'
    if 'Playing Cards' in name: return 'Bicycle扑克牌'
    if 'Funko' in name: return 'Michael Jackson Funko'
    if 'Pokemon' in name or 'Pokémon' in name: return '宝可梦卡片'
    if 'St