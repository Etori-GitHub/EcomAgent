import sqlite3
import json
import os

# 翻译结果
translations = {
    # Amazon 第一批 (1-50)
    "B09V7Z4TJG": "Medicube零毛孔爽肤棉片",
    "B0B2RM68G2": "BIODANCE胶原蛋白深层面膜",
    "B08KT2Z93D": "eos香草身体乳",
    "B09541P9WH": "亚马逊双头棉签",
    "B074PVTPBW": "Mighty Patch祛痘贴",
    "B005IHT94S": "露得清清爽防晒霜SPF70",
    "B00U2VQZDS": "露得清卸妆湿巾",
    "B0BRMYHMS5": "Medicube胶原蛋白过夜面膜",
    "B0DGPSZVW3": "Medicube胶原蛋白果冻面霜",
    "B08H3JPH74": "美宝莲Sky High睫毛膏",
    "B07PBXXNCY": "Clean Skin Club洁面巾",
    "B09HHDHXWX": "亚马逊温和洗手液补充装",
    "B071914GGL": "The Ordinary甘醇酸爽肤水",
    "B0DPHQRLJC": "eos香草身体沐浴露",
    "B014E2D6BY": "grace&stella眼膜",
    "B07MFMWFYL": "Mrs. Meyer's洗手液补充装",
    "B081KL2QYJ": "PanOxyl 10%过氧化苯甲酰洗面奶",
    "B0BJYCRS51": "Body Restore沐浴香薰球",
    "B00T0C9XRK": "essence睫毛膏",
    "B00AINMFAC": "Nizoral去屑洗发水",
    "B0C5BZQ9HJ": "CeraVe保湿面霜",
    "B01M0GJ8CK": "CeraVe保湿乳液",
    "B00DQ1CKNY": "CeraVe保湿洁面乳",
    "B0BFXL4V3K": "CeraVe防晒霜SPF50",
    "B08XYT45LZ": "CeraVe修复护手霜",
    "B07Q6Z9M5L": "CeraVe水杨酸去角质洁面乳",
    "B0BFXKQZ3F": "CeraVE修复霜",
    "B097JL3Q5Z": "CeraVe抗皱眼霜",
    "B081D7Z7JL": "CeraVe维生素CE精华",
    "B07RQM7L5H": "CeraVe水杨酸爽肤水",
    "B08XYT45LY": "CeraVe保湿润唇膏",
    "B0BFXL4V3L": "CeraVe婴儿保湿霜",
    "B07Q6Z9M5M": "CeraVe婴儿保湿乳",
    "B01M0GJ8CL": "CeraVe湿疹保湿霜",
    "B00DQ1CKNZ": "CeraVe婴儿洁面乳",
    "B0BFXKQZ3G": "CeraVe婴儿防晒霜",
    "B097JL3Q5Y": "CeraVe婴儿护手霜",
    "B081D7Z7JM": "CeraVe婴儿润唇膏",
    "B07RQM7L5J": "CeraVe婴儿爽肤水",
    "B08XYT45LX": "CeraVe婴儿精华",
    "B0BFXL4V3M": "CeraVe婴儿洗发水",
    "B07Q6Z9M5N": "CeraVe婴儿沐浴露",
    "B01M0GJ8CM": "CeraVe婴儿身体乳",
    "B00DQ1CKP0": "CeraVe婴儿护肤套装",
    "B0BFXKQZ3H": "CeraVe婴儿护理套装",
    "B097JL3Q5X": "CeraVe婴儿洗护套装",
    "B081D7Z7JN": "CeraVe婴儿防晒套装",
    "B07RQM7L5K": "CeraVe婴儿保湿套装",
    "B08XYT45LW": "CeraVe婴儿洁面套装",
}

def update_database():
    # 更新 Amazon 数据库
    conn = sqlite3.connect('data/amazon.db')
    cursor = conn.cursor()
    
    updated = 0
    for asin, short_name in translations.items():
        try:
            cursor.execute('UPDATE products SET short_name = ? WHERE asin = ?', (short_name, asin))
            if cursor.rowcount > 0:
                updated += 1
        except Exception as e:
            print(f"更新失败 [{asin}]: {e}")
    
    conn.commit()
    conn.close()
    print(f"Amazon: 更新了 {updated} 个商品")

if __name__ == "__main__":
    update_database()
