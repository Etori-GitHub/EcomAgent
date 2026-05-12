#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
亚马逊 Best Sellers 全分类抓取脚本
功能：
1. 从主页面提取所有子分类
2. 抓取每个子分类的前 2 页数据
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


def extract_all_categories(page):
    """从主页面提取所有子分类"""
    
    print(f"\n[INFO] 正在提取所有子分类...")
    
    extract_js = """
        () => {
            const categories = [];
            
            // 查找导航树父元素
            const parent = document.querySelector('[data-card-metrics-id="p13n-zg-nav-tree-all_zeitgeist-lists_1"]');
            if (!parent) {
                console.log('未找到导航树元素');
                return categories;
            }
            
            // 查找 ul 列表
            const ul = parent.querySelector('ul.a-unordered-list.a-nostyle.a-vertical');
            if (!ul) {
                console.log('未找到 ul 列表');
                return categories;
            }
            
            // 提取所有分类链接
            const links = ul.querySelectorAll('a[href*="/Best-Sellers-"][href*="/zgbs/"]');
            
            links.forEach((link, idx) => {
                const href = link.getAttribute('href');
                const text = link.innerText.trim();
                
                if (href && text) {
                    // 构建完整 URL
                    const full_url = 'https://www.amazon.com' + href;
                    
                    categories.push({
                        name: text,
                        url: full_url,
                        slug: href.match(/\\/zgbs\\/([^/]+)/)?.[1] || '',
                        index: idx
                    });
                }
            });
            
            return categories;
        }
    """
    
    categories = page.evaluate(extract_js)
    print(f"[OK] 找到 {len(categories)} 个子分类")
    
    return categories


def fetch_category_bestsellers_pages(category_url, category_name, subcategory, pages=2):
    """抓取指定分类的 Best Sellers 榜单（前 N 页）"""
    
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
        
        page.set_viewport_size({"width": 1920, "height": 5000})
        
        # 简化的数据提取
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
                        
                        console.log(`商品 ${idx}: rank=${rank}, asin=${asin}, name=${name.substring(0, 30)}...`);
                        
                        if (asin) {
                            results.push({
                                rank,
                                name,
                                asin,
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
        
        for page_num in range(1, pages + 1):
            # 构建分页 URL
            if page_num == 1:
                url = category_url
            else:
                # 第 2 页开始，将 ref=zg_bs_{slug}_sm 改为 ref=zg_bs_pg_2_{slug}_0
                url = category_url.replace('/ref=zg_bs_', f'/ref=zg_bs_pg_{page_num}_')
            
            print(f"[INFO] 访问第 {page_num} 页：{url}")
            page.goto(url, timeout=60000)
            
            page.wait_for_timeout(random_wait(10000, 20000))  # 随机等待 10-20 秒
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(random_wait(5000, 10000))  # 随机等待 5-10 秒
            
            # 使用字符串替换注入变量
            page_js_code = js_code.replace('CATEGORY_PLACEHOLDER', category_name).replace('SUBCATEGORY_PLACEHOLDER', subcategory)
            items = page.evaluate(page_js_code)
            
            print(f"[INFO] 第 {page_num} 页成功提取 {len(items)} 个商品")
            all_items.extend(items)
        
        browser.close()
    
    return all_items


def fetch_and_save_category(category, pages=2):
    """抓取单个分类并保存到独立文件"""
    base_dir = Path(__file__).parent.parent.parent.parent
    output_dir = base_dir / "output" / "scraping"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    
    # 生成文件名（使用分类 slug）
    category_slug = category['slug'].lower().replace(' ', '_').replace('&', 'and').replace('/', '_')
    output_file = output_dir / f"amazon_{category_slug}_{timestamp}.json"
    
    print(f"\n=== 抓取分类：{category['name']} (前 {pages} 页) ===")
    
    # 添加重试机制
    max_retries = 3
    retry_count = 0
    last_error = None
    
    while retry_count < max_retries:
        try:
            data = fetch_category_bestsellers_pages(
                category['url'],
                category['name'],
                category['slug'],
                pages
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
                    print(f"  - {item['rank']}. {item['name']} (${item['price']}) - {item['rating']}★ ({item['rating_count']}评)")
            
            return data
        except Exception as e:
            retry_count += 1
            last_error = e
            print(f"[WARN] 失败 {retry_count}/{max_retries}: {e}")
            if retry_count < max_retries:
                wait_ms = random_wait(10000, 20000)
                print(f"[INFO] 等待 {wait_ms}ms 后重试...")
                import time
                time.sleep(wait_ms / 1000)
    
    print(f"[ERROR] 分类 {category['name']} 抓取失败（已达最大重试次数）")
    raise last_error


def fetch_all_categories():
    """抓取所有 Best Sellers 分类的前 2 页数据"""
    
    print(f"[INFO] 开始抓取所有 Best Sellers 分类...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        # 访问主页面
        print(f"[INFO] 访问 Amazon Best Sellers 主页面...")
        page.goto("https://www.amazon.com/gp/bestsellers/", timeout=120000)
        page.wait_for_timeout(random_wait(10000, 15000))
        
        # 提取所有分类
        categories = extract_all_categories(page)
        
        if not categories:
            print(f"[ERROR] 没有提取到任何分类！")
            browser.close()
            return
        
        # 保存分类列表
        categories_file = Path(__file__).parent.parent / "screenshots" / "categories.json"
        categories_file.parent.mkdir(parents=True, exist_ok=True)
        with open(categories_file, "w", encoding="utf-8") as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)
        print(f"[OK] 类目列表已保存到：{categories_file}")
        
        # 抓取每个分类
        for i, category in enumerate(categories):
            fetch_and_save_category(category, pages=2)
            if i < len(categories) - 1:
                wait_ms = random_wait(10000, 20000)
                print(f"\n[INFO] 等待 {wait_ms}ms 后开始下一个分类...")
                import time
                time.sleep(wait_ms / 1000)
        
        browser.close()
    
    print(f"\n[OK] 所有分类抓取完成！")


if __name__ == "__main__":
    fetch_all_categories()
