import sqlite3
import json

# 从 pending_asins.py 复制的已知名称
KNOWN_NAMES = {
    "ECAM26001434": "ELEGOO PLA Filament 1.75mm Black 1KG, 3D Printer Filament Dimensional Accuracy +/- 0.02mm, 1kg Cardboard Spool(2.2lbs) 3D Printing Filament Fits for Most FDM 3D Printers",
    "ECAM26001637": "200 PCS Funny Holographic Stickers for Adults, Waterproof Vinyl Sarcastic Meme Decals for Laptop, Water Bottle, Phone, Kindle, Journal, Scrapbook, Bumper, Skateboard, Luggage, No Repeats",
    "ECAM26001675": "Nocs Provisions Standard Issue 10x25 Waterproof Binoculars, 10X Magnification, Bak4 Prism, Wide View Multi-Coated Lenses for Bird Watching, Hiking & Backpacking - Pacific Blue II",
    "ECAM26001696": "20x50 High Powered Binoculars for Adults, Waterproof Compact Binoculars with Low Light Vision Easy Focus for Bird Watching Hunting Travel Stargazing Cruise with Carrying Bag",
    "ECAM26001798": "6 Pack Slimes, Pink Slime Kids, Cloud Slime kit for Girls 8-12, Toys for Girls and Boys",
    "ECAM26001857": "Wiaocit 3 Pack Tempered Glass Privacy Screen Protector for iPhone 16 Pro Max with 3 Pack Camera Lens Protector, 9H Hardness, Bubble Free, Case Friendly",
    "ECAM26001866": "[4 Pack] USB C Charger Block Fast Charging Multiport Adapter [PD 20W USB-C & QC 3.0 USB-A Port] for iPhone 17/16/15/14/13/12/11/X/8, iPad, Galaxy, Google & More",
}

# 获取当前 pending 的商品
conn_master = sqlite3.connect(r'C:\Users\Etroi\.openclaw\workspace\code\EcomAgent\data\product_master.db')
c = conn_master.cursor()
c.execute('''
    SELECT ecom_code, platform_id 
    FROM product_master 
    WHERE translation_status = 'pending'
''')
pending_items = c.fetchall()
conn_master.close()

print(f'Total pending: {len(pending_items)}')

# 检查哪些在 KNOWN_NAMES 里
found = []
not_found = []

for ecom_code, platform_id in pending_items:
    if ecom_code in KNOWN_NAMES:
        found.append({'id': ecom_code, 'name': KNOWN_NAMES[ecom_code]})
        print(f'FOUND: {ecom_code}')
    else:
        not_found.append({'id': ecom_code, 'asin': platform_id})
        print(f'NOT FOUND: {ecom_code} (ASIN: {platform_id})')

print(f'\nFound in KNOWN_NAMES: {len(found)}')
print(f'Not found: {len(not_found)}')
