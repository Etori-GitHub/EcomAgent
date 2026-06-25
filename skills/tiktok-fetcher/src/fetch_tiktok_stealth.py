#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok Shop 热销榜单抓取脚本 - Playwright Stealth 版本
使用 playwright-stealth 插件绑过反爬检测

功能：
1. 使用 stealth 插件隐藏自动化特征
2. 模拟真实用户行为
3. 从首页提取类目列表
4. 提取商品数据并保存到 JSON 文件

依赖：pip install playwright-stealth
"""

import json
import os
import random
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Windows UTF-8 兼容
if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

# 尝试导入 stealth
try:
    from playwright_stealth import stealth_sync
    HAS_STEALTH = True
    print("[OK] playwright-stealth 已加载")
except ImportError:
    HAS_STEALTH = False
    print("[WARN] playwright-stealth 未安装，使用基础反检测")
    print("[WARN] 安装命令: pip install playwright-stealth")


def random_wait(min_ms=1000, max_ms=3000):
    """随机等待，模拟人类行为"""
    wait_ms = random.randint(min_ms, max_ms)
    print(f"[INFO] 等待 {wait_ms}ms...")
    return wait_ms


def human_like_scroll(page):
    """模拟人类滚动行为"""
    for _ in range(random.randint(3, 6)):
        scroll_amount = random.randint(300, 800)
        page.evaluate(f"window.scrollBy(0, {scroll_amount})")
        time.sleep(random.uniform(0.5, 1.5))


def extract_categories(page):
    """从首页提取类目列表"""
    print(f"\n[INFO] 正在提取类目列表...")
    
    category_js = """
        () => {
            const categories = [];
            const allLinks = Array.from(document.querySelectorAll('a'));
            
            allLinks.forEach((link) => {
                const href = link.href;
                const text = (link.innerText || link.textContent || '').trim();
                
                const isCategoryLink = href && (
                    href.includes('shop.tiktok.com') && href.includes('/c/') ||
                    href.includes('/shop/c/')
                ) && text && text.length > 0 && text.length < 50;
                
                if (isCategoryLink) {
                    categories.push({
                        name: text,
                        url: href
                    });
                }
            });
            
            return categories;
        }
    """
    
    categories = page.evaluate(category_js)
    print(f"[OK] 找到 {len(categories)} 个类目")
    return categories


def fetch_category_products(page, category_name):
    """从已打开的页面抓取商品数据"""
    page.wait_for_timeout(random_wait(8000, 15000))
    
    # 模拟人类滚动
    print(f"[INFO] 滚动页面加载商品...")
    human_like_scroll(page)
    
    # 点击"查看更多"
    try:
        load_more_btn = page.get_by_role("button", name="查看更多").first
        if load_more_btn.is_enabled():
            load_more_btn.click()
            page.wait_for_timeout(random_wait(5000, 10000))
    except:
        pass
    
    # 提取商品
    print(f"[INFO] 正在提取商品数据...")
    
    product_js = """
        () => {
            const products = [];
            const priceElements = Array.from(document.querySelectorAll('*')).filter(el => {
                const text = el.innerText || el.textContent || '';
                return text.includes('$') && /\\$\\d+\\.\\d+/.test(text);
            });
            
            priceElements.forEach((priceEl) => {
                try {
                    const text = priceEl.innerText.trim();
                    if (text.includes('Orders') || text.includes('销售')) return;
                    
                    let container = priceEl.parentElement;
                    let depth = 0;
                    
                    while (container && depth < 6) {
                        const nameEl = container.querySelector('h3');
                        const ratingEl = container.querySelector('span');
                        
                        if (nameEl && ratingEl) {
                            const name = nameEl.innerText.trim();
                            if (!name || name.length < 5) {
                                container = container.parentElement;
                                depth++;
                                continue;
                            }
                            
                            const ratingMatch = ratingEl.innerText.match(/(\\d+\\.\\d+)/);
                            const rating = ratingMatch ? parseFloat(ratingMatch[1]) : null;
                            
                            const soldEl = Array.from(container.querySelectorAll('span')).find(el => 
                                el.innerText.includes('已售出')
                            );
                            const sold = soldEl ? soldEl.innerText.trim() : null;
                            
                            const priceMatch = text.match(/\\$(\\d+\\.\\d+)/);
                            const price = priceMatch ? parseFloat(priceMatch[1]) : null;
                            
                            const linkEl = container.querySelector('a[href*="/shop/pdp/"]');
                            let tiktokshop_id = null;
                            let product_url = null;
                            
                            if (linkEl && linkEl.href) {
                                product_url = linkEl.href;
                                const urlMatch = product_url.match(/\/shop\/pdp\/[^/]+\/(\d+)/);
                                if (urlMatch) tiktokshop_id = urlMatch[1];
                            }
                            
                            const imgEl = container.querySelector('img');
                            const imageUrl = imgEl?.src || '';
                            
                            products.push({
                                name, rating, sold, price,
                                tiktokshop_id, product_url,
                                image_url: imageUrl,
                                rank: products.length + 1
                            });
                            break;
                        }
                        
                        container = container.parentElement;
                        depth++;
                    }
                } catch (e) {}
            });
            
            return products;
        }
    """
    
    products = page.evaluate(product_js)
    print(f"[OK] 找到 {len(products)} 个商品")
    return products


def fetch_and_save_category(category, page):
    """抓取单个分类并保存"""
    base_dir = Path(__file__).parent.parent.parent.parent
    output_dir = base_dir / "output" / "scraping"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    beijing_tz = timezone(timedelta(hours=8))
    now = datetime.now(beijing_tz)
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    
    category_slug = category['name'].lower().replace(' ', '_').replace('&', 'and').replace('/', '_')
    output_file = output_dir / f"tiktok_{category_slug}_{timestamp}.json"
    
    print(f"\n=== 抓取分类：{category['name']} ===")
    
    try:
        page.goto(category['url'], timeout=120000)
    except Exception as e:
        print(f"[ERROR] 访问页面失败：{e}")
        return None
    
    data = fetch_category_products(page, category['name'])
    
    if not data:
        print(f"[WARN] 没有抓取到商品数据")
        return None
    
    # 去重
    seen_ids = set()
    unique_products = []
    for product in data:
        tiktokshop_id = product.get('tiktokshop_id')
        if tiktokshop_id and tiktokshop_id not in seen_ids:
            seen_ids.add(tiktokshop_id)
            unique_products.append(product)
            if len(unique_products) >= 20:
                break
    
    data = unique_products
    
    enriched_data = {
        "metadata": {
            "platform": "tiktok",
            "category": category['name'],
            "category_url": category['url'],
            "scraped_at": now.isoformat(),
            "total_items": len(data),
            "method": "playwright-stealth"
        },
        "products": data
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(enriched_data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 分类 {category['name']} 抓取完成，共 {len(data)} 个商品")
    print(f"[OK] 数据已保存到：{output_file}")
    
    return enriched_data


def fetch_all_categories():
    """主函数 - 使用 Playwright Stealth"""
    print(f"[INFO] 开始抓取 TikTok Shop (Playwright Stealth 版本)...")
    
    with sync_playwright() as p:
        # 启动浏览器 - 强化反检测参数
        browser = p.chromium.launch(
            headless=False,
            slow_mo=100,  # 减慢操作速度
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-site-isolation-trials',
                '--disable-features=BlockInsecurePrivateNetworkRequests',
                '--disable-infobars',
                '--window-size=1920,1080',
                '--start-maximized',
            ]
        )
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York',
        )
        
        page = context.new_page()
        
        # 应用 stealth 插件
        if HAS_STEALTH:
            stealth_sync(page)
            print("[OK] Stealth 插件已应用")
        
        # 访问首页
        print(f"[INFO] 访问 TikTok Shop 首页...")
        
        try:
            page.goto("https://shop.tiktok.com", timeout=60000, wait_until='domcontentloaded')
        except Exception as e:
            print(f"[ERROR] 访问首页失败：{e}")
            browser.close()
            return
        
        page.wait_for_timeout(random_wait(10000, 15000))
        
        # 检查是否被封
        content = page.content()
        if '{"code":100000}' in content:
            print(f"[ERROR] 检测到封禁响应 code:100000")
            print(f"[INFO] 尝试等待更长时间...")
            page.wait_for_timeout(30000)
            
            # 再次检查
            content = page.content()
            if '{"code":100000}' in content:
                print(f"[ERROR] 仍然被封，建议：")
                print(f"  1. 换 IP（VPN/代理）")
                print(f"  2. 使用 undetected-chromedriver 版本")
                print(f"  3. 考虑 Android App 抓包方案")
                browser.close()
                return
        
        # 等待用户确认
        print(f"\n{'='*60}")
        print(f"[重要] 请在浏览器中检查：")
        print(f"1. 页面是否正常显示（不是 code:100000）")
        print(f"2. 是否需要通过验证码")
        print(f"3. 完成后按 Enter 继续抓取...")
        print(f"{'='*60}\n")
        input("按 Enter 继续...")
        
        # 滚动加载
        print(f"[INFO] 滚动页面加载更多内容...")
        human_like_scroll(page)
        
        # 提取类目
        categories = extract_categories(page)
        
        if not categories:
            print(f"[ERROR] 没有提取到任何类目！")
            browser.close()
            return
        
        # 保存类目列表
        categories_file = Path(__file__).parent.parent / "screenshots" / "categories_stealth.json"
        categories_file.parent.mkdir(parents=True, exist_ok=True)
        with open(categories_file, "w", encoding="utf-8") as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)
        print(f"[OK] 类目列表已保存")
        
        # 抓取第一个类目（测试）
        test_categories = categories[:1]
        for category in test_categories:
            fetch_and_save_category(category, page)
        
        browser.close()
    
    print(f"\n[OK] 抓取完成！")


if __name__ == "__main__":
    fetch_all_categories()
