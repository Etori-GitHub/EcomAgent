#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok Shop 热销榜单抓取脚本
抓取多个分类的热销商品数据
"""

import json
import random
import re
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright


def random_wait(min_ms=1000, max_ms=3000):
    """随机等待，避免被反爬"""
    wait_ms = random.randint(min_ms, max_ms)
    print(f"[INFO] 等待 {wait_ms}ms 避免反爬...")
    return wait_ms


def fetch_tiktok_category_bestsellers(category_url, category_name, subcategory):
    """抓取指定分类的 Best Sellers 榜单"""
    
    all_items = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.set_viewport_size({"width": 1920, "height": 5000})
        
        print(f"[INFO] 访问分类: {category_name}")
        page.goto(category_url, timeout=60000)
        
        page.wait_for_timeout(random_wait(5000, 10000))
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(random_wait(3000, 6000))
        
        # 提取商品数据的 JavaScript 代码
        js_code = """
            () => {
                const results = [];
                
                // TikTok Shop 的商品列表选择器
                // 根据页面结构，商品卡片可能包含以下特征
                const productCards = document.querySelectorAll('[class*="product"], [class*="item"], [class*="card"], [class*="Product"]');
                
                console.log(`找到 ${productCards.length} 个商品卡片`);
                
                productCards.forEach((card, idx) => {
                    try {
                        // 尝试提取各种信息
                        let rank = idx + 1;
                        let name = '';
                        let price = 0;
                        let rating = 0;
                        let ratingCount = 0;
                        let soldCount = 0;
                        
                        // 提取名称 - 尝试多种选择器
                        name = card.querySelector('h3, h2, h4, .title, .name, [class*="title"], [class*="name"]')?.innerText.trim() || '';
                        
                        // 如果没有提取到，尝试从链接中获取
                        if (!name) {
                            name = card.querySelector('a')?.innerText.trim() || '';
                        }
                        
                        // 提取价格
                        const priceEl = card.querySelector('[class*="price"], [class*="cost"], .price, .cost');
                        if (priceEl) {
                            const priceText = priceEl.innerText.trim();
                            const match = priceText.match(/([\\d,.]+)/);
                            if (match) {
                                price = parseFloat(match[1].replace(',', ''));
                            }
                        }
                        
                        // 提取评分
                        const ratingEl = card.querySelector('[class*="rating"], [class*="star"], .rating, .stars');
                        if (ratingEl) {
                            const ratingText = ratingEl.innerText.trim();
                            const match = ratingText.match(/([\\d.]+)/);
                            if (match) {
                                rating = parseFloat(match[1]);
                            }
                        }
                        
                        // 提取评价数量
                        const ratingCountEl = card.querySelector('[class*="review"], [class*="comment"], .review, .comment');
                        if (ratingCountEl) {
                            const countText = ratingCountEl.innerText.trim();
                            const match = countText.match(/([\\d,.]+)/);
                            if (match) {
                                ratingCount = parseInt(match[1].replace(',', ''));
                            }
                        }
                        
                        // 提取销量
                        const soldEl = card.querySelector('[class*="sold"], [class*="sell"], [class*="sale"], .sold, .sell, .sale');
                        if (soldEl) {
                            const soldText = soldEl.innerText.trim();
                            const match = soldText.match(/([\\d,.]+)/);
                            if (match) {
                                soldCount = parseInt(match[1].replace(',', ''));
                            }
                        }
                        
                        if (name) {
                            results.push({
                                rank,
                                name,
                                price,
                                rating,
                                rating_count: ratingCount,
                                sold_count: soldCount,
                                category: 'CATEGORY_PLACEHOLDER',
                                subcategory: 'SUBCATEGORY_PLACEHOLDER'
                            });
                        }
                    } catch (e) {
                        console.log(`商品 ${idx} 解析失败:`, e.message);
                    }
                });
                
                return results;
            }
        """
        
        # 使用字符串替换注入变量
        page_js_code = js_code.replace('CATEGORY_PLACEHOLDER', category_name).replace('SUBCATEGORY_PLACEHOLDER', subcategory)
        items = page.evaluate(page_js_code)
        
        print(f"[INFO] 成功提取 {len(items)} 个商品")
        all_items.extend(items)
        
        browser.close()
    
    return all_items


def fetch_and_save_category(category):
    """抓取单个分类并保存到独立文件"""
    base_dir = Path(__file__).parent.parent.parent.parent
    output_dir = base_dir / "output" / "scraping"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"tiktok_{category['name']}_{timestamp}.json"
    
    print(f"\n=== 抓取分类: {category['name']} ===")
    
    data = fetch_tiktok_category_bestsellers(
        category['url'],
        category['name'],
        category.get('subcategory', category['name'])
    )
    
    # 保存到 JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 分类 {category['name']} 抓取完成，共 {len(data)} 个商品")
    print(f"[OK] 数据已保存到: {output_file}")
    
    # 打印前5条数据作为示例
    if data:
        print("\n[示例数据] 前5条:")
        for item in data[:5]:
            print(f"  - {item['rank']}. {item['name']} (${item['price']}) - {item['rating']}★")
    
    return data


def fetch_all_categories():
    """抓取所有 TikTok Shop 分类的热销数据"""
    
    print(f"[INFO] 开始抓取 TikTok Shop 所有分类...")
    
    # TikTok Shop 的正确 URL 是 https://www.tiktok.com/shop
    categories = [
        {
            "name": "Electronics",
            "url": "https://www.tiktok.com/shop",
            "subcategory": "Best Sellers in Electronics"
        },
        {
            "name": "Fashion",
            "url": "https://www.tiktok.com/shop",
            "subcategory": "Best Sellers in Fashion"
        },
        {
            "name": "Beauty",
            "url": "https://www.tiktok.com/shop",
            "subcategory": "Best Sellers in Beauty"
        },
        {
            "name": "Home & Living",
            "url": "https://www.tiktok.com/shop",
            "subcategory": "Best Sellers in Home & Living"
        },
        {
            "name": "Sports & Outdoors",
            "url": "https://www.tiktok.com/shop",
            "subcategory": "Best Sellers in Sports & Outdoors"
        },
        {
            "name": "Toys & Kids",
            "url": "https://www.tiktok.com/shop",
            "subcategory": "Best Sellers in Toys & Kids"
        }
    ]
    
    for i, category in enumerate(categories):
        fetch_and_save_category(category)
        if i < len(categories) - 1:
            wait_ms = random_wait(3000, 8000)
            print(f"\n[INFO] 等待 {wait_ms}ms 后开始下一个分类...")
            import time
            time.sleep(wait_ms / 1000)
    
    print(f"\n[OK] 所有分类抓取完成！")


if __name__ == "__main__":
    fetch_all_categories()
