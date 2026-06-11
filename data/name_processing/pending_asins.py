import sqlite3
import json
import time
import sys

# 待获取的 ASIN 列表
PENDING_ASINS = [
    ("ECAM26000824", "B0BVH5QWM8"),
    ("ECAM26000914", "B0BMGBBPTT"),
    ("ECAM26001010", "B0DDZRY1W2"),
    ("ECAM26001046", "B0CLPGQWNB"),
    ("ECAM26001179", "B09FT58QQP"),
    ("ECAM26001242", "B0DNMJ694B"),
    ("ECAM26001313", "B0D9Q5MZRD"),
    ("ECAM26001363", "B09FFCGLHK"),
    ("ECAM26001369", "B088BWBD95"),
    ("ECAM26001419", "B0CZCVPX41"),
    ("ECAM26001422", "B0D3HYC8H1"),
    ("ECAM26001427", "B09K58K13V"),
    ("ECAM26001429", "B096G6QJ93"),
    ("ECAM26001436", "B0C4TNQZYY"),
    ("ECAM26001442", "B0CP4XY9QC"),
    ("ECAM26001445", "B0FNWM5WW8"),
    ("ECAM26001447", "B0D8J2ZB8P"),
    ("ECAM26001458", "B0CHGFG64S"),
    ("ECAM26001494", "B09WZJ81JQ"),
    ("ECAM26001574", "B0DDCHN5WW"),
    ("ECAM26001612", "B01JHMVG5O"),
    ("ECAM26001626", "B0CJC2C3F5"),
    ("ECAM26001628", "B0B5TNSJKF"),
    ("ECAM26001637", "B0F8B58PBN"),
    ("ECAM26001648", "B01N0BZQQO"),
    ("ECAM26001663", "B00B8CG602"),
    ("ECAM26001671", "B00YLTG7DA"),
    ("ECAM26001675", "B0CTJC2LZW"),
    ("ECAM26001678", "B08FMM86JN"),
    ("ECAM26001680", "B0GL59P3WM"),
    ("ECAM26001681", "B09841HG7D"),
    ("ECAM26001687", "B0DGCKWLL8"),
    ("ECAM26001688", "B0GQ6F965V"),
    ("ECAM26001689", "B0BRGT4699"),
    ("ECAM26001696", "B0GN94CHLT"),
    ("ECAM26001734", "B088P1NST3"),
    ("ECAM26001741", "B0BTLXZ8FH"),
    ("ECAM26001798", "B0CYT6D2ZS"),
    ("ECAM26001841", "B07KXQX3S3"),
    ("ECAM26001844", "B0F3J1GXTD"),
    ("ECAM26001845", "B0DN1S1YLV"),
    ("ECAM26001855", "B0GCD9F4LC"),
    ("ECAM26001857", "B0DNP6LRBB"),
    ("ECAM26001866", "B0B2WLSY9D"),
    ("ECAM26001892", "B07G2HWJWC"),
]

# 已知成功的商品（从之前的抓取结果）
KNOWN_NAMES = {
    "ECAM26001434": "ELEGOO PLA Filament 1.75mm Black 1KG, 3D Printer Filament Dimensional Accuracy +/- 0.02mm, 1kg Cardboard Spool(2.2lbs) 3D Printing Filament Fits for Most FDM 3D Printers",
    "ECAM26001637": "200 PCS Funny Holographic Stickers for Adults, Waterproof Vinyl Sarcastic Meme Decals for Laptop, Water Bottle, Phone, Kindle, Journal, Scrapbook, Bumper, Skateboard, Luggage, No Repeats",
    "ECAM26001675": "Nocs Provisions Standard Issue 10x25 Waterproof Binoculars, 10X Magnification, Bak4 Prism, Wide View Multi-Coated Lenses for Bird Watching, Hiking & Backpacking - Pacific Blue II",
    "ECAM26001696": "20x50 High Powered Binoculars for Adults, Waterproof Compact Binoculars with Low Light Vision Easy Focus for Bird Watching Hunting Travel Stargazing Cruise with Carrying Bag",
    "ECAM26001798": "6 Pack Slimes, Pink Slime Kids, Cloud Slime kit for Girls Ages 8-12, Toys for Girls and Boys, for Kids Slime Set Party kit Goodie Bag Stuffers, 4 5 6 7 8 9 10 Year Old Girl Birthday Gift Cute Stuff",
    "ECAM26001857": "Wiaocit 3 Pack Tempered Glass Privacy Screen Protector for iPhone 16 Pro Max with 3 Pack Camera Lens Protector, 9H Hardness, Bubble Free, Case Friendly",
    "ECAM26001866": "[4 Pack] USB C Charger Block Fast Charging Multiport Adpater [PD 20W USB-C & QC 3.0 USB-A Port] for iPhone 17/16/15/14/13/12/11/X/8, iPad, Galaxy, Google & More",
}

# 输出需要搜索的 ASIN
print("ASINs to search (copy this list):")
print("-" * 50)
for ecom_code, asin in PENDING_ASINS:
    if ecom_code not in KNOWN_NAMES:
        print(f"{ecom_code}: {asin}")