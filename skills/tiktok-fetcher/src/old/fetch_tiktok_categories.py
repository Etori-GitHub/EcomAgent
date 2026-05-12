#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok Shop 热销榜单抓取脚本
抓取多个分类的热销商品数据

版本：2.0 - 改用 TikTok 主站搜索方式
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


def fetch_tiktok_category_bestsellers(category_name, search_query):
    """通过搜索抓取指定分类的商品"""
    
    all_items = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        # 模拟真实用户
        page.add_init_script("""
            () => {
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                navigator.languages = ['en-US', 'en'];
                navigator.plugins = [1, 2, 3, 4, 5];
            }
        """)
        
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        # 访问 TikTok 主站并搜索
        search_url = f"https://www.tiktok.com/search?q={search_query}&type=live"
        print(f"[INFO] 访问搜索页面：{search_url}")
        page.goto(search_url, timeout=60000)
        
        page.wait_for_timeout(random_wait(10000, 20000))
        
        # 提取商品数据的 JavaScript 代码
        js_code = """
            () => {
                const results = [];
                
                // 调试：打印所有包含价格的元素
                const allElements = document.querySelectorAll('*');
                const priceElements = Array.from(allElements).filter(el => {
                    const text = el.innerText || el.textContent || '';
                    return text.includes('$') || text.includes('¥');
                });
                
                console.log('=== 包含价格的元素数:', priceElements.length);
                
                // 打印前 10 个包含价格的元素
                priceElements.slice(0, 10).forEach((el, idx) => {
                    const text = (el.innerText || el.textContent || '').trim().substring(0, 100);
                    const className = (el.className || '').toString().substring(0, 100);
                    console.log('[' + idx + '] [' + className + '] ' + text);
                });
                
                // 尝试提取商品信息
                priceElements.forEach((el, idx) => {
                    const text = el.innerText ? el.innerText.trim() : '';
                    const className = (el.className || '').toString();
                    
                    const priceMatch = text.match(/[$¥](\d+\.?\d*)/);
                    const ratingMatch = text.match(/(\d+\.\d+)/);
                    
                    if (priceMatch) {
                        results.push({
                            tag: el.tagName,
                            className: className.substring(0, 200),
                            text: text.substring(0, 200),
                            price: priceMatch[1],
                            rating: ratingMatch ? ratingMatch[1] : null
                        });
                    }
                });
                
                console.log('=== 找到 ' + results.length + ' 个疑似商品 ===');
                results.slice(0, 5).forEach((item, idx) => {
                    console.log('[' + idx + '] ' + item.text);
                    console.log('    Class: ' + item.className);
                    console.log('    Price: ' + item.price);
                });
                
                return results;
            }
        """
        
        items = page.evaluate(js_code)
        
        print(f"[INFO] 页面结构分析完成，找到 {len(items)} 个疑似商品")
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
    
    print(f"\n=== 抓取分类：{category['name']} ===")
    
    data = fetch_tiktok_category_bestsellers(
        category['name'],
        category['search_query']
    )
    
    # 保存到 JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 分类 {category['name']} 抓取完成，共 {len(data)} 个商品")
    print(f"[OK] 数据已保存到：{output_file}")
    
    # 打印前 5 条数据作为示例
    if data:
        print("\n[示例数据] 前 5 条:")
        for item in data[:5]:
            print(f"  - {item.get('text', 'N/A')} (${item.get('price', 'N/A')})")
    else:
        print("\n[警告] 没有抓取到任何商品数据！")
    
    return data


def fetch_all_categories():
    """抓取所有 TikTok Shop 分类的热销数据"""
    
    print(f"[INFO] 开始抓取 TikTok Shop 所有分类...")
    
    # 使用搜索方式抓取分类
    categories = [
        {
            "name": "Beauty",
            "search_query": "beauty products trending"
        },
        {
            "name": "Electronics",
            "search_query": "electronics trending"
        },
        {
            "name": "Fashion",
            "search_query": "fashion trending"
        },
        {
            "name": "Home",
            "search_query": "home decor trending"
        },
        {
            "name": "Sports",
            "search_query": "sports equipment trending"
        }
    ]
    
    print(f"[INFO] 准备抓取 {len(categories)} 个分类")
    
    # 限制测试数量，避免死循环
    test_categories = categories[:3]  # 只测试前 3 个分类
    print(f"[INFO] 测试模式：仅抓取前 {len(test_categories)} 个分类")
    
    for i, category in enumerate(test_categories):
        fetch_and_save_category(category)
        if i < len(test_categories) - 1:
            wait_ms = random_wait(3000, 8000)
            print(f"\n[INFO] 等待 {wait_ms}ms 后开始下一个分类...")
            import time
            time.sleep(wait_ms / 1000)
    
    print(f"\n[OK] 测试抓取完成！")


if __name__ == "__main__":
    fetch_all_categories()
