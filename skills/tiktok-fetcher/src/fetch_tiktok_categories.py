#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok Shop 热销榜单抓取脚本 - 正式版
关键：访问时带上 Google Referer 绕过封禁
"""

import json
import random
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright


def random_wait(min_ms=1000, max_ms=3000):
    """随机等待"""
    wait_ms = random.randint(min_ms, max_ms)
    time.sleep(wait_ms / 1000)
    return wait_ms


def extract_categories(page):
    """提取类目列表"""
    print(f"\n[INFO] 提取类目列表...")
    
    categories = page.evaluate("""
        () => {
            const cats = [];
            document.querySelectorAll('a').forEach(a => {
                const href = a.href;
                const text = a.innerText.trim();
                if (href && href.includes('/c/') && text && text.length > 0 && text.length < 50) {
                    cats.push({name: text, url: href});
                }
            });
            
            const seen = new Set();
            return cats.filter(cat => {
                if (seen.has(cat.url)) return false;
                seen.add(cat.url);
                return true;
            });
        }
    """)
    
    print(f"[OK] 找到 {len(categories)} 个类目")
    return categories


def fetch_category_products(page, category_name, category_url):
    """抓取类目商品"""
    print(f"\n[INFO] 访问类目: {category_name}")
    
    # 添加参数
    if '?' not in category_url:
        category_url += '?source=ecommerce_mall&enter_method=categories&first_entrance=google&first_entrance_tt_scene=seo'
    
    # 关键：用 Google Referer！
    page.goto(category_url, timeout=60000, referer="https://www.google.com/")
    
    # 等待页面加载
    print(f"[INFO] 等待页面加载...")
    random_wait(8000, 12000)
    
    # 检查是否被封
    content = page.content()
    if '{"code":100000}' in content:
        print(f"[ERROR] 类目页面被封")
        return None
    
    # 滚动加载更多商品
    print(f"[INFO] 滚动加载商品...")
    for i in range(8):
        page.evaluate(f"window.scrollBy(0, {600 + random.randint(100, 400)})")
        time.sleep(0.8)
    
    # 再等待让商品渲染
    random_wait(3000, 5000)
    
    # 提取商品
    print(f"[INFO] 提取商品...")
    
    products = page.evaluate("""
        () => {
            const items = [];
            
            // 找所有商品链接
            const productLinks = document.querySelectorAll('a[href*="/shop/pdp/"]');
            
            productLinks.forEach(link => {
                try {
                    // 找商品容器 - 修复：先定义 container
                    const container = link.closest('[class*="product"]') || 
                                     link.closest('[class*="item"]') || 
                                     link.closest('[class*="card"]') ||
                                     link.parentElement?.parentElement?.parentElement;
                    
                    // 找商品名称
                    let name = '';
                    
                    // 尝试从链接本身获取文本
                    const linkText = link.innerText.trim();
                    if (linkText && linkText.length >= 5 && linkText.length < 100) {
                        name = linkText;
                    }
                    
                    // 如果链接没有文本，从容器找
                    if (!name && container) {
                        const textEls = container.querySelectorAll('span, div, p, h3, h4');
                        for (const el of textEls) {
                            const t = el.innerText.trim();
                            if (t.length >= 5 && t.length < 100 && !t.includes('$') && !t.includes('已售') && !t.includes('sold')) {
                                name = t;
                                break;
                            }
                        }
                    }
                    
                    if (!name || name.length < 5) return;
                    
                    // 找图片 - 修复：container 已定义
                    let imageUrl = '';
                    if (container) {
                        const img = container.querySelector('img');
                        if (img && img.src) {
                            imageUrl = img.src;
                        }
                    }
                    
                    // 找价格 - 修复：container 已定义
                    let price = null;
                    if (container) {
                        const allText = container.innerText;
                        const priceMatch = allText.match(/\\$([\\d.]+)/);
                        if (priceMatch) {
                            price = parseFloat(priceMatch[1]);
                        }
                    }
                    
                    // 找评分
                    let rating = null;
                    if (container) {
                        const ratingMatch = container.innerText.match(/([\\d.]+)\\s*(stars?|星)/i);
                        if (ratingMatch) {
                            rating = parseFloat(ratingMatch[1]);
                        }
                    }
                    
                    // 找销量
                    let sold = null;
                    if (container) {
                        const soldMatch = container.innerText.match(/([\\d.]+[KkMm]?)\\s*(sold|已售|Sold)/i);
                        if (soldMatch) {
                            sold = soldMatch[0];
                        }
                    }
                    
                    // 提取 tiktokshop_id
                    const idMatch = link.href.match(/\/shop\/pdp\/([A-Za-z0-9]+)/);
                    const tiktokshopId = idMatch ? idMatch[1] : '';
                    
                    items.push({
                        name: name.substring(0, 100),
                        price: price,
                        rating: rating,
                        sold: sold,
                        image_url: imageUrl,
                        product_url: link.href,
                        tiktokshop_id: tiktokshopId
                    });
                } catch (e) {}
            });
            
            // 去重
            const seen = new Set();
            return items.filter(item => {
                if (seen.has(item.tiktokshop_id)) return false;
                seen.add(item.tiktokshop_id);
                return true;
            }).slice(0, 50);
        }
    """)
    
    print(f"[OK] 找到 {len(products)} 个商品")
    
    if products:
        print(f"[示例] 前3个商品:")
        for i, p in enumerate(products[:3]):
            print(f"  {i+1}. {p['name'][:50]}... - ${p.get('price')} - {p.get('sold')} - {p.get('rating')}★")
    
    return products


def save_category_data(category, products):
    """保存类目数据"""
    base_dir = Path(__file__).parent.parent.parent.parent
    output_dir = base_dir / "output" / "scraping"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    beijing_tz = timezone(timedelta(hours=8))
    now = datetime.now(beijing_tz)
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    
    category_slug = category['name'].lower().replace(' ', '_').replace('&', 'and').replace('/', '_')
    output_file = output_dir / f"tiktok_{category_slug}_{timestamp}.json"
    
    data = {
        "metadata": {
            "platform": "tiktok",
            "category": category['name'],
            "category_url": category['url'],
            "scraped_at": now.isoformat(),
            "total_items": len(products),
        },
        "products": products
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 已保存: {output_file}")


def fetch_all_categories():
    """主函数"""
    print(f"[INFO] 启动 TikTok Shop 抓取...")
    print(f"[关键] 使用 Google Referer 绕过封禁")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # ========== 关键：带上 Google Referer 访问首页 ==========
        print(f"\n[步骤 1] 访问 TikTok Shop 首页 (带 Google Referer)...")
        
        page.goto(
            "https://shop.tiktok.com/us",
            timeout=60000,
            referer="https://www.google.com/"  # 关键！
        )
        random_wait(5000, 8000)
        
        # 检查是否成功
        content = page.content()
        if '{"code":100000}' in content:
            print(f"[ERROR] 仍然被封！")
            browser.close()
            return
        
        print(f"[OK] 首页访问成功！")
        
        # 等待用户确认
        print(f"\n{'='*60}")
        print(f"[提示] 请确认页面正常显示商品内容")
        print(f"[提示] 按 Enter 继续抓取类目...")
        print(f"{'='*60}")
        input("按 Enter 继续...")
        
        # 提取类目
        categories = extract_categories(page)
        
        if not categories:
            print(f"[ERROR] 没有找到类目")
            browser.close()
            return
        
        # 保存类目列表
        categories_file = Path(__file__).parent.parent / "screenshots" / "categories.json"
        categories_file.parent.mkdir(parents=True, exist_ok=True)
        with open(categories_file, "w", encoding="utf-8") as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)
        print(f"[OK] 类目列表已保存: {categories_file}")
        
        # 抓取所有类目
        print(f"\n[步骤 2] 抓取 {len(categories)} 个类目...")
        
        for i, category in enumerate(categories):
            print(f"\n[{i+1}/{len(categories)}] {category['name']}")
            
            products = fetch_category_products(page, category['name'], category['url'])
            
            if products:
                save_category_data(category, products)
            else:
                print(f"[WARN] 该类目没有抓到商品")
            
            if i < len(categories) - 1:
                wait = random.randint(3000, 6000)
                print(f"[INFO] 等待 {wait}ms...")
                time.sleep(wait / 1000)
        
        browser.close()
    
    print(f"\n{'='*60}")
    print(f"[完成] 抓取完成！")
    print(f"{'='*60}")


if __name__ == "__main__":
    fetch_all_categories()
