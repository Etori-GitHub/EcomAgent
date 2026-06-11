import json

# 已收集的商品名称数据
collected_names = {
    # 从网页抓取成功
    "ECAM26001434": "ELEGOO PLA Filament 1.75mm Black 1KG, 3D Printer Filament",
    "ECAM26001637": "200 PCS Funny Holographic Stickers for Adults",
    "ECAM26001675": "Nocs Provisions Standard Issue 10x25 Waterproof Binoculars",
    "ECAM26001696": "20x50 High Powered Binoculars for Adults",
    "ECAM26001798": "6 Pack Slimes, Pink Slime Kids, Cloud Slime kit for Girls",
    "ECAM26001857": "Wiaocit 3 Pack Tempered Glass Privacy Screen Protector for iPhone 16 Pro Max",
    "ECAM26001866": "[4 Pack] USB C Charger Block Fast Charging Multiport Adapter",
    
    # 从网络搜索获取
    "ECAM26000824": "FIREGAS Black Range Hood 36 in Under Cabinet, 300 CFM",
    "ECAM26000914": "TOZO A1 Mini Wireless Earbuds",
    "ECAM26001179": "TOZO A1 Wireless Earbuds Bluetooth 5.3",
    "ECAM26001363": "JOREST 40-piece Small Precision Screwdriver Set",
    "ECAM26001369": "Amazon Basics 20x20x1 Air Filter 6-Pack, MERV 11",
    "ECAM26001419": "TJOY A19 LED Light Bulbs 6-Pack, 60W Equivalent",
    "ECAM26001422": "Dealusy 50 Pack Meal Prep Containers Reusable with Lids",
    "ECAM26001429": "ADIIL 20 PCS Q Hanger Hooks with Safety Buckle",
    "ECAM26001436": "Creality 1.75mm Hyper PLA Filament for High-Speed Printing, 2-Pack White",
    "ECAM26001442": "YARRAMATE 2-in-1 Glass Oil Sprayer Bottle",
    "ECAM26001458": "ChefAide 5 Pieces Silicone Spatula Set",
    "ECAM26001494": "Cutter Backyard Bug Control Spray Concentrate",
    "ECAM26001648": "PetArmor Plus Flea & Tick Topical for Cats",
    "ECAM26001663": "Seresto Flea and Tick Collar for Dogs",
    "ECAM26001678": "Pankoo 16X52 Monocular Telescope",
    "ECAM26001681": "Bushnell H2O 7x50 Waterproof Porro Binoculars",
    "ECAM26001741": "Diamont Vented Over Clear Safety Glasses, ANSI Z87.1",
    "ECAM26001845": "ANDERY Car Phone Holder for MagSafe",
}

# 翻译后的简短名称
translated_names = {
    # 从网页抓取成功的商品
    "ECAM26001434": "ELEGOO PLA 3D打印耗材",
    "ECAM26001637": "200张搞笑全息贴纸",
    "ECAM26001675": "Nocs 10x25防水双筒望远镜",
    "ECAM26001696": "20x50高倍双筒望远镜",
    "ECAM26001798": "6包粉色云朵史莱姆玩具",
    "ECAM26001857": "Wiaocit iPhone 16 Pro Max防窥膜",
    "ECAM26001866": "4口USB-C快充充电器",
    
    # 从网络搜索获取的商品
    "ECAM26000824": "FIREGAS 36寸黑色抽油烟机",
    "ECAM26000914": "TOZO A1迷你无线耳机",
    "ECAM26001179": "TOZO A1蓝牙5.3无线耳机",
    "ECAM26001363": "JOREST 40件精密螺丝刀套装",
    "ECAM26001369": "亚马逊基础款20x20x1空气滤网6件装",
    "ECAM26001419": "TJOY A19 LED灯泡6只装",
    "ECAM26001422": "Dealusy 50套带盖餐盒",
    "ECAM26001429": "ADIIL 20个防风Q型挂钩",
    "ECAM26001436": "Creality高速PLA 3D打印耗材白色双卷装",
    "ECAM26001442": "YARRAMATE二合一玻璃喷油瓶",
    "ECAM26001458": "ChefAide 5件套硅胶锅铲",
    "ECAM26001494": "Cutter后院杀虫喷雾浓缩液",
    "ECAM26001648": "PetArmor Plus猫咪跳蚤蜱虫滴剂",
    "ECAM26001663": "Seresto狗狗跳蚤蜱虫项圈",
    "ECAM26001678": "Pankoo 16x52单筒望远镜",
    "ECAM26001681": "Bushnell H2O 7x50防水双筒望远镜",
    "ECAM26001741": "Diamont通风式护目镜36副装",
    "ECAM26001845": "ANDERY MagSafe车载手机支架",
}

# 待处理（未能获取名称的商品）
pending_items = [
    "ECAM26001010",  # B0DDZRY1W2
    "ECAM26001046",  # B0CLPGQWNB
    "ECAM26001242",  # B0DNMJ694B
    "ECAM26001313",  # B0D9Q5MZRD
    "ECAM26001427",  # B09K58K13V
    "ECAM26001445",  # B0FNWM5WW8
    "ECAM26001447",  # B0D8J2ZB8P
    "ECAM26001574",  # B0DDCHN5WW
    "ECAM26001612",  # B01JHMVG5O
    "ECAM26001626",  # B0CJC2C3F5
    "ECAM26001628",  # B0B5TNSJKF
    "ECAM26001671",  # B00YLTG7DA
    "ECAM26001680",  # B0GL59P3WM
    "ECAM26001687",  # B0DGCKWLL8
    "ECAM26001688",  # B0GQ6F965V
    "ECAM26001689",  # B0BRGT4699
    "ECAM26001734",  # B088P1NST3
    "ECAM26001841",  # B07KXQX3S3
    "ECAM26001844",  # B0F3J1GXTD
    "ECAM26001855",  # B0GCD9F4LC
    "ECAM26001892",  # B07G2HWJWC
]

# 生成输出
items = []
for ecom_code, short_name in translated_names.items():
    items.append({"id": ecom_code, "short_name": short_name})

# 按ID排序
items.sort(key=lambda x: x["id"])

data = {
    "batch_id": "batch_20260605_2000",
    "items": items
}

output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\processed_names.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Generated {len(items)} translated items")
print(f"\nPending items (no name found): {len(pending_items)}")
for item in pending_items:
    print(f"  {item}")
