#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok 数据去重脚本
处理今天已抓取的 JSON 文件，使用 tiktokshop_id 去重
"""

import json
import re
from datetime import datetime
from pathlib import Path


def deduplicate_products(products):
    """使用 tiktokshop_id 去重"""
    seen_ids = set()
    unique_products = []
    duplicates = 0
    
    for product in products:
        tiktokshop_id = product.get('tiktokshop_id')
        if tiktokshop_id and tiktokshop_id not in seen_ids:
            seen_ids.add(tiktokshop_id)
            unique_products.append(product)
        elif tiktokshop_id:
            duplicates += 1
    
    return unique_products, duplicates


def process_file(file_path):
    """处理单个 JSON 文件"""
    print(f"\n{'='*60}")
    print(f"处理文件：{file_path.name}")
    print(f"{'='*60}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 提取产品列表
        if isinstance(data, dict):
            products = data.get('products', [])
            metadata = data.get('metadata', {})
        elif isinstance(data, list):
            products = data
            metadata = {}
        else:
            print(f"❌ 未知数据格式：{type(data)}")
            return 0, 0
        
        original_count = len(products)
        
        if original_count == 0:
            print(f"⚠️  文件为空，跳过")
            return 0, 0
        
        # 去重
        unique_products, duplicates = deduplicate_products(products)
        new_count = len(unique_products)
        
        if duplicates == 0:
            print(f"✅ 无需去重：原始 {original_count} 个，重复 0 个")
            return 0, 0
        
        # 更新元数据
        if isinstance(data, dict):
            data['products'] = unique_products
            data['metadata']['total_items'] = new_count
            data['metadata']['deduplicated_at'] = datetime.now().isoformat()
            data['metadata']['duplicates_removed'] = duplicates
        
        # 保存回原文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 去重完成：原始 {original_count} 个，去重后 {new_count} 个，删除 {duplicates} 个重复项")
        print(f"📊 保存率：{new_count/original_count*100:.1f}%")
        
        return new_count, duplicates
        
    except Exception as e:
        print(f"❌ 处理失败：{e}")
        return 0, 0


def main():
    """主函数"""
    print(f"\n{'#'*60}")
    print(f"# TikTok 数据去重脚本")
    print(f"# 运行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*60}")
    
    # 获取项目根目录
    base_dir = Path(__file__).parent.parent
    scraping_dir = base_dir / "output" / "scraping"
    
    if not scraping_dir.exists():
        print(f"❌ 抓取目录不存在：{scraping_dir}")
        return
    
    # 获取所有 TikTok JSON 文件
    tiktok_files = sorted([f for f in scraping_dir.glob("tiktok_*.json")])
    
    if not tiktok_files:
        print(f"✅ 未找到 TikTok JSON 文件")
        return
    
    print(f"\n找到 {len(tiktok_files)} 个 TikTok JSON 文件\n")
    
    total_original = 0
    total_unique = 0
    total_duplicates = 0
    
    # 处理每个文件
    for file_path in tiktok_files:
        new_count, duplicates = process_file(file_path)
        total_original += new_count + duplicates
        total_unique += new_count
        total_duplicates += duplicates
    
    # 总结
    print(f"\n{'='*60}")
    print(f"去重总结")
    print(f"{'='*60}")
    print(f"处理文件数：{len(tiktok_files)}")
    print(f"原始商品数：{total_original:,}")
    print(f"去重后商品数：{total_unique:,}")
    print(f"删除重复项：{total_duplicates:,}")
    print(f"总体保存率：{total_unique/total_original*100:.1f}%")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
