#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
亚马逊 Best Sellers 分类抓取脚本
动态获取分类列表，抓取每个分类的热销商品
使用已登录的 Chrome Profile 减少反爬限制
"""

import json
import random
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright


def random_wait(min_ms=1000, max_ms=3000):
    """随机等待，避免被反爬"""
    wait_ms = random.randint(min_ms, max_ms)
    print(f"[INFO] 等待 {wait_ms}ms 避免反爬...")
    return wait_ms


def extract_categories(page):
    """从 Best Sellers 主页提取分类列表"""
    
    print(f"[INFO] 正在提取分类列表...")
    
    category_js = """
        () => {
            const categories = [];
            
            // 找到分类列表容器
            const container = document.querySelector('div[role="group"][aria-label="Navigation Tree"]');
            if (!container) {
                console.log('未找到分类容器');
                return categories;
            }
            
            // 找到 ul 列表
            const ul = container.querySelector('ul');
            if (!ul) {
                console.log('未找到 ul 列表');
                return categories;
            }
            
            // 遍历每个 li
            const items = ul.querySelectorAll('li');
            items.forEach((li, idx) => {
                const link = li.querySelector('a');
                if (link && link.href) {
                    const name = link.innerText.trim();
                    const href = link.getAttribute('href');
                    
                    if (name && href) {
                        categories.push({
                            name: name,
                            url: 'https://www.amazon.com' + href,
                            subcategory: 'Best Sellers in ' + name
                        });
                        
                        if (categories.length <= 5) {
                            console.log('[' + (categories.length-1) + '] ' + name + ' -> ' + href);
                        }
                    }
                }
            });
            
            return categories;
        }
    """
    
    categories = page.evaluate(category_js)
    print(f"[OK] 找到 {len(categories)} 个分类")
    
    return categories


def fetch_category_bestsellers(page, category):
    """抓取指定分类的 Best Sellers 榜单（1页，约25个商品）"""
    
    print(f"\n=== 抓取分类: {category['name']} ===")
    
    # 访问分类页面
    print(f"[INFO] URL: {category['url']}")
    page.goto(category['url'], timeout=60000)
    
    page.wait_for_timeout(random_wait(10000, 20000))
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(random_wait(5000, 10000))
    
    # 提取商品数据
    js_code = """
        () => {
            const results = [];
            const rows = document.querySelectorAll('li.zg-no-numbers');
            
            console.log(`找到 ${rows.length} 个商品行`);
            
            rows.forEach((row, idx) => {
                try {
                    const rankEl = row.querySelector('.zg-bdg-text');
                    const rank = rankEl ? parseInt(rankEl.innerText.replace('#', '').trim()) : idx + 1;
                    
                    const links = row.querySelectorAll('a.a-link-normal.aok-block');
                    const link = links[1] || links[0];
                    const href = link?.href || '';
                    
                    const asinMatch = href.match(/\\/dp\\/([A-Z0-9]{10})/);
                    const asin = asinMatch ? asinMatch[1] : '';
                    
                    const name = link?.innerText?.trim() || '';
                    
                    const priceLink = links[2] || links[1] || links[0];
                    const priceText = priceLink?.innerText?.trim() || '';
                    const price = priceText ? parseFloat(priceText.replace(/[^\\d.]/g, '')) : 0;
                    
                    const ratingEl = row.querySelector('.a-icon-alt');
                    const ratingText = ratingEl?.innerText || '';
                    const ratingMatch = ratingText.match(/([\\d.]+)/);
                    const rating = ratingMatch ? parseFloat(ratingMatch[1]) : 0;
                    
                    const countEls = row.querySelectorAll('span.a-size-small');
                    const countText = countEls[0]?.innerText || '';
                    const ratingCount = parseInt(countText.replace(/[^\\d]/g, '')) || 0;
                    
                    // 提取图片 URL
                    const imgEl = row.querySelector('img');
                    const imageUrl = imgEl?.src || '';
                    
                    if (asin) {
                        const productUrl = `https://www.amazon.com/dp/${asin}`;
                        
                        results.push({
                            rank,
                            name,
                            asin,
                            product_url: productUrl,
                            image_url: imageUrl,
                            price,
                            rating,
                            rating_count: ratingCount,
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
    
    page_js_code = js_code.replace('CATEGORY_PLACEHOLDER', category['name']).replace('SUBCATEGORY_PLACEHOLDER', category['subcategory'])
    items = page.evaluate(page_js_code)
    
    print(f"[OK] 提取 {len(items)} 个商品")
    
    return items


def fetch_and_save_category(page, category, base_dir):
    """抓取单个分类并保存到独立文件"""
    
    output_dir = base_dir / "output" / "scraping"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    
    # 生成文件名（处理特殊字符）
    category_slug = category['name'].lower().replace(' ', '_').replace('&', 'and').replace(',', '').replace('/', '_')
    output_file = output_dir / f"amazon_{category_slug}_{timestamp}.json"
    
    # 抓取数据
    data = fetch_category_bestsellers(page, category)
    
    if not data:
        print(f"[WARN] 没有抓取到数据")
        return None
    
    # 保存到 JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 数据已保存到: {output_file.name}")
    
    # 打印示例
    if data:
        print("[示例] 前3条:")
        for item in data[:3]:
            print(f"  - {item['rank']}. {item['name'][:40]}... (${item['price']})")
    
    return data


def fetch_all_categories():
    """动态获取分类列表并抓取所有分类的热销商品"""
    
    print(f"[INFO] 开始抓取 Amazon Best Sellers...")
    
    base_dir = Path(__file__).parent.parent.parent.parent
    
    with sync_playwright() as p:
        # 使用已登录的 Chrome Profile（和 TikTok 一样）
        user_data_dir = r"C:\Users\Etroi\AppData\Local\Google\Chrome\User Data\Profile 1"
        
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            slow_mo=500,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--allow-running-insecure-content'
            ]
        )
        page = browser.new_page()
        
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        # 访问 Best Sellers 主页
        print(f"[INFO] 访问 Best Sellers 主页...")
        page.goto("https://www.amazon.com/Best-Sellers/zgbs", timeout=60000)
        
        page.wait_for_timeout(random_wait(10000, 20000))
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(random_wait(5000, 10000))
        
        # 提取分类列表
        categories = extract_categories(page)
        
        if not categories:
            print(f"[ERROR] 没有提取到分类列表！")
            browser.close()
            return
        
        # 保存分类列表
        categories_file = base_dir / "output" / "amazon_categories.json"
        categories_file.parent.mkdir(parents=True, exist_ok=True)
        with open(categories_file, "w", encoding="utf-8") as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)
        print(f"[OK] 分类列表已保存到: {categories_file}")
        
        # 抓取每个分类（测试模式：只抓第一个分类）
        total_items = 0
        for i, category in enumerate(categories[:1]):
            fetch_and_save_category(page, category, base_dir)
            total_items += 1
            
            if i < len(categories[:1]) - 1:
                wait_ms = random_wait(10000, 20000)
                print(f"\n[INFO] 等待 {wait_ms}ms 后开始下一个分类...")
                import time
                time.sleep(wait_ms / 1000)
        
        browser.close()
    
    print(f"\n[OK] 抓取完成！共 {len(categories[:1])} 个分类")


if __name__ == "__main__":
    fetch_all_categories()