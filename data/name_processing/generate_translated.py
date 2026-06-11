import json

# 已找到的商品名称（从网络搜索）
FOUND_NAMES = {
    # B07KXQX3S3 -> ECAM26001841
    "ECAM26001841": "SanDisk 128GB microSDXC Memory Card, Licensed for Nintendo Switch",
    
    # B01JHMVG5O -> ECAM26001612
    "ECAM26001612": "BIC Xtra-Smooth Mechanical Pencil (MPP40MJ), Medium Point (0.7mm), 40-Count",
    
    # B00YLTG7DA -> ECAM26001671
    "ECAM26001671": "Kindle Paperwhite 3rd Generation (2015)",
    
    # B088P1NST3 -> ECAM26001734
    "ECAM26001734": "Amazon Kindle Paperwhite (11th Generation), 16GB",
    
    # B07G2HWJWC -> ECAM26001892
    "ECAM26001892": "Amazon Fire HD 8 Kids Edition (8th Generation) tablet, 32GB",
    
    # B0CLPGQWNB -> ECAM26001046
    "ECAM26001046": "Comfy Cubs Muslin Burp Cloths, 6-Pack 100% Cotton, 20\"x10\"",
    
    # B0D8J2ZB8P -> ECAM26001447
    "ECAM26001447": "Powcan 26oz Insulated Water Bottle with 2-in-1 Straw Lid",
    
    # B0DDCHN5WW -> ECAM26001574
    "ECAM26001574": "KUKIHO Wireless Lavalier Microphone for iPhone/iPad/Android",
    
    # B0B5TNSJKF -> ECAM26001628
    "ECAM26001628": "AIGOSTAR Food Steamer",
    
    # B0GL59P3WM -> ECAM26001680
    "ECAM26001680": "AIGOSTAR Food Steamer",
}

# 未找到名称的 ASIN（无法搜索到）
NOT_FOUND = [
    "ECAM26001010",  # B0DDZRY1W2
    "ECAM26001242",  # B0DNMJ694B
    "ECAM26001313",  # B0D9Q5MZRD
    "ECAM26001427",  # B09K58K13V
    "ECAM26001445",  # B0FNWM5WW8
    "ECAM26001626",  # B0CJC2C3F5
    "ECAM26001687",  # B0DGCKWLL8
    "ECAM26001688",  # B0GQ6F965V
    "ECAM26001689",  # B0BRGT4699
    "ECAM26001844",  # B0F3J1GXTD
    "ECAM26001855",  # B0GCD9F4LC
]

# 翻译后的短名称
TRANSLATED_NAMES = {
    "ECAM26001841": "SanDisk 128GB 任天堂Switch内存卡",
    "ECAM26001612": "BIC自动铅笔40支装0.7mm",
    "ECAM26001671": "Kindle Paperwhite 3代电子书阅读器",
    "ECAM26001734": "Kindle Paperwhite 11代16GB电子书阅读器",
    "ECAM26001892": "亚马逊Fire HD 8儿童版平板32GB",
    "ECAM26001046": "Comfy Cubs纯棉纱布口水巾6片装",
    "ECAM26001447": "Powcan保温水杯26oz双盖设计",
    "ECAM26001574": "KUKIHO无线领夹麦克风",
    "ECAM26001628": "AIGOSTAR食品蒸锅",
    "ECAM26001680": "AIGOSTAR食品蒸锅",
}

print(f"找到名称的商品: {len(FOUND_NAMES)}")
print(f"无法搜索到的商品: {len(NOT_FOUND)}")
print(f"已翻译的商品: {len(TRANSLATED_NAMES)}")

# 生成输出
items = []
for ecom_code, short_name in TRANSLATED_NAMES.items():
    items.append({"id": ecom_code, "short_name": short_name})

data = {
    "batch_id": "batch_20260605_2035",
    "items": items
}

output_path = r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\name_processing\processed_names.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n已保存 {len(items)} 个翻译结果到 processed_names.json")
print(f"\n无法获取名称的商品 ({len(NOT_FOUND)} 个):")
for ecom_code in NOT_FOUND:
    print(f"  {ecom_code}")
