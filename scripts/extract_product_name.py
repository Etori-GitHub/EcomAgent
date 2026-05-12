#!/usr/bin/env python3
"""
智能商品名提取器
从完整的商品标题中提取真正的商品名
"""

import re


def extract_product_name(full_title: str) -> str:
    """
    从完整商品标题中提取商品名
    
    策略：
    1. 品牌名：第一个单词或连续的大写开头单词
    2. 产品名：品牌后直到分隔符或规格信息
    3. 分隔符：| , - (带空格)
    4. 规格标志：数字+单位 (Pads, oz, Count, Pack, ml, g, kg, pcs, pieces)
    
    示例：
    输入: "medicube Toner Pads Zero Pore Pad 2.0 | Dual-Textured Facial Pad..."
    输出: "medicube Toner Pads Zero Pore Pad 2.0"
    
    输入: "eos Shea Better Body Lotion Vanilla Cashmere, 24-Hour Moisture..."
    输出: "eos Shea Better Body Lotion Vanilla Cashmere"
    """
    if not full_title:
        return ""
    
    # 清理标题
    title = full_title.strip()
    
    # 规格单位关键词（遇到这些就截断）
    spec_patterns = [
        r'\d+\s*(Pads|Pad|Count|Pack|pcs|pieces|oz|fl\s*oz|ml|g|kg|lb|lbs|oz|inch|inches|cm|mm)',
        r'\d+x\d+',
        r'\d+\.\d+\s*(oz|ml|g|kg)',
        r'\(\d+\s*[a-zA-Z]+\)',  # (70 Pads), (1 Pack)
        r'x\s*\d+',  # x 4ea, x 36
    ]
    
    # 分隔符（遇到这些就截断）
    separators = ['|', ' - ', ' – ', ' — ']
    
    # 1. 先按分隔符截断
    for sep in separators:
        if sep in title:
            title = title.split(sep)[0].strip()
    
    # 2. 按逗号截断（但要保留品牌+产品名部分）
    # 检查逗号后是否是规格信息
    if ',' in title:
        parts = title.split(',')
        # 检查每个逗号后的部分
        result_parts = []
        for i, part in enumerate(parts):
            part = part.strip()
            # 如果这部分包含规格信息，截断
            if any(re.search(p, part, re.IGNORECASE) for p in spec_patterns):
                break
            # 如果这部分是宣传语（常见关键词），截断
            promo_keywords = ['for', 'with', 'ideal', 'perfect', 'best', 'great', 'amazing', 
                             'essential', 'travel', 'gift', 'women', 'men', 'kids', 'all',
                             'korean', 'japanese', 'american', 'natural', 'organic', 'vegan']
            if any(kw in part.lower() for kw in promo_keywords) and i > 0:
                # 检查是否是规格前的宣传语
                if not any(re.search(p, part, re.IGNORECASE) for p in spec_patterns):
                    break
            result_parts.append(part)
        title = ', '.join(result_parts)
    
    # 3. 按规格信息截断
    for pattern in spec_patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            # 截断到规格信息之前
            title = title[:match.start()].strip()
            # 如果截断后太短，保留规格信息
            if len(title) < 10:
                title = full_title.split('|')[0].split(',')[0].strip()
            break
    
    # 4. 清理结尾的标点符号
    title = title.rstrip(',|-–—:;')
    
    # 5. 如果结果太长（超过60字符），再截断
    if len(title) > 60:
        # 尝试在逗号处截断
        if ',' in title:
            title = title.split(',')[0].strip()
        # 尝试在空格处截断，保留完整单词
        if len(title) > 60:
            words = title.split()
            result = []
            for word in words:
                result.append(word)
                if len(' '.join(result)) > 50:
                    result.pop()
                    break
            title = ' '.join(result)
    
    return title.strip()


def test_extractor():
    """测试提取器"""
    test_cases = [
        "medicube Toner Pads Zero Pore Pad 2.0 | Dual-Textured Facial Pad for Exfoliation and Pore Care with 4.5% AHA Lactic Acid, 0.45% BHA Salicylic Acid | Ideal for All, Korean Skin Care, 70 Pads (1 Pack)",
        "BIODANCE Bio-Collagen Real Deep Mask, Hydrating Overnight Hydrogel Face Mask, Pore Minimizing, Elasticity, Plumping, Travel Essentials & Self Care Gifts for Women, Korean Skin Care | 1.19oz(34g) x 4ea",
        "eos Shea Better Body Lotion Vanilla Cashmere, 24-Hour Moisture Skin Care, Lightweight & Non-Greasy, Natural Shea, Vegan, Vanilla Body Lotion, 16 fl oz",
        "Amazon Basics Double-Tipped Cotton Swabs for Personal Hygiene and Baby Care, Cotton, Versatile, Baby Safe, 500 Count",
        "Mighty Patch Original Patch from Hero Cosmetics - #1 Hydrocolloid Acne Pimple Patches for Face, Shrinking Zits & Whiteheads in 1 Use, Nighttime Spot Pimple Stickers for Face, 36 Count",
        "Apple iPhone 15 Pro Max 256GB Natural Titanium",
        "Samsung Galaxy S24 Ultra 512GB Titanium Black",
    ]
    
    print("=" * 80)
    print("Product Name Extractor Test")
    print("=" * 80)
    
    for title in test_cases:
        extracted = extract_product_name(title)
        print(f"\n原文: {title[:60]}...")
        print(f"提取: {extracted}")
        print("-" * 40)


if __name__ == "__main__":
    test_extractor()