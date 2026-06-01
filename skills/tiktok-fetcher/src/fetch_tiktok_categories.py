#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok Shop 热销榜单抓取脚本
稳健版本：使用动态选择器和相对定位

功能：
1. 从首页提取类目列表（使用 /shop/c/ 过滤）
2. 点击"查看更多"按钮加载商品
3. 提取商品数据（名称、评分、销量、价格、图片等）
4. 保存到 JSON 文件
"""

import json
import random
import re
import sys
import io
from datetime import datetime
from pathlib import Path

# Windows UTF-8 兼容
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright


def random_wait(min_ms=1000, max_ms=3000):
    """随机等待，避免被反爬"""
    wait_ms = random.randint(min_ms, max_ms)
    print(f"[INFO] 等待 {wait_ms}ms 避免反爬...")
    return wait_ms


def extract_categories(page):
    """从首页提取类目列表（匹配 shop.tiktok.com/us/c/ 或 /c/）"""
    
    print(f"\n[INFO] 正在提取类目列表...")
    
    category_js = """
        () => {
            const categories = [];
            
            // 策略：找到所有包含类目链接的 a 标签
            const allLinks = Array.from(document.querySelectorAll('a'));
            
            console.log('=== 总共找到 ' + allLinks.length + ' 个链接 ===');
            
            allLinks.forEach((link, idx) => {
                const href = link.href;
                const text = (link.innerText || link.textContent || '').trim();
                const dataId = link.getAttribute('data-id');
                
                // 匹配类目链接：shop.tiktok.com/*/c/ 或 /shop/c/ 或 /c/
                const isCategoryLink = href && (
                    href.includes('shop.tiktok.com') && href.includes('/c/') ||
                    href.includes('/shop/c/')
                ) && text && text.length > 0 && text.length < 50;
                
                if (isCategoryLink) {
                    categories.push({
                        name: text,
                        url: href,
                        data_id: dataId || '',
                        className: link.className || ''
                    });
                    
                    if (categories.length <= 5) {
                        console.log('[' + (categories.length-1) + '] ' + text + ' -> ' + href);
                    }
                }
            });
            
            return categories;
        }
    """
    
    categories = page.evaluate(category_js)
    print(f"[OK] 找到 {len(categories)} 个类目")
    
    return categories


def fetch_category_products_from_page(page, category_name):
    """从已打开的页面抓取商品数据（使用稳健的选择器）"""
    
    # 等待页面加载
    page.wait_for_timeout(random_wait(10000, 20000))
    
    # 点击"查看更多"按钮加载更多商品
    print(f"[INFO] 点击'查看更多'按钮加载更多商品...")
    try:
        # 使用 Playwright 的 get_by_role 和 get_by_text
        load_more_btn = page.get_by_role("button", name="查看更多").first
        if load_more_btn.is_enabled():
            load_more_btn.click()
            page.wait_for_timeout(random_wait(5000, 10000))
            print(f"[OK] 已点击'查看更多'按钮")
        else:
            print(f"[WARN] 未找到'查看更多'按钮，继续抓取")
    except Exception as e:
        print(f"[WARN] 点击'查看更多'失败：{e}")
    
    # 滚动页面加载更多内容
    print(f"[INFO] 滚动页面加载更多内容...")
    for i in range(3):
        try:
            page.evaluate("""
                () => {
                    if (document.body) {
                        window.scrollTo(0, document.body.scrollHeight);
                    }
                }
            """)
        except Exception as e:
            print(f"[WARN] 滚动失败：{e}")
        page.wait_for_timeout(random_wait(3000, 5000))
    
    # 最终等待
    page.wait_for_timeout(random_wait(10000, 20000))
    
    # 提取商品数据 - 使用稳健的选择器
    print(f"[INFO] 正在提取商品数据...")
    
    product_js = """
        () => {
            const products = [];
            
            // 策略：从价格元素向上查找商品容器
            // 1. 找到所有包含 $ 价格的元素
            const priceElements = Array.from(document.querySelectorAll('*')).filter(el => {
                const text = el.innerText || el.textContent || '';
                return text.includes('$') && /\\$\\d+\\.\\d+/.test(text);
            });
            
            console.log('=== 找到 ' + priceElements.length + ' 个包含价格的元素 ===');
            
            // 2. 从价格元素向上查找商品容器
            priceElements.forEach((priceEl, idx) => {
                try {
                    const text = priceEl.innerText.trim();
                    
                    // 跳过导航元素和页脚
                    if (text.includes('Orders') || text.includes('销售') || 
                        text.includes('客户支持') || text.includes('TikTok Shop')) {
                        return;
                    }
                    
                    // 向上查找商品容器（最多 6 层）
                    let container = priceEl.parentElement;
                    let depth = 0;
                    const maxDepth = 6;
                    
                    while (container && depth < maxDepth) {
                        // 检查是否是商品容器
                        const nameEl = container.querySelector('h3');
                        const ratingEl = container.querySelector('span');
                        
                        if (nameEl && ratingEl) {
                            const name = nameEl.innerText.trim();
                            
                            // 过滤掉空名称或导航元素
                            if (!name || name.length < 5 || name.includes('Orders') || 
                                name.includes('销售') || name.includes('客户支持')) {
                                container = container.parentElement;
                                depth++;
                                continue;
                            }
                            
                            // 提取评分
                            const ratingText = ratingEl.innerText;
                            const ratingMatch = ratingText.match(/(\\d+\\.\\d+)/);
                            const rating = ratingMatch ? parseFloat(ratingMatch[1]) : null;
                            
                            // 提取销售量（查找包含"已售出"的元素）
                            const soldEl = Array.from(container.querySelectorAll('span')).find(el => 
                                el.innerText.includes('已售出')
                            );
                            const sold = soldEl ? soldEl.innerText.trim() : null;
                            
                            // 提取价格
                            const priceMatch = text.match(/\\$(\\d+\\.\\d+)/);
                            const price = priceMatch ? parseFloat(priceMatch[1]) : null;
                            
                            // 提取原价（查找删除线元素）
                            const originalPriceEl = Array.from(container.querySelectorAll('span')).find(el => 
                                el.innerText.startsWith('$') && el.classList.contains('line-through')
                            );
                            const originalPrice = originalPriceEl ? 
                                parseFloat(originalPriceEl.innerText.replace('$', '')) : null;
                            
                            // 提取商品详情页 URL（关键！用于获取唯一 ID）
                            const linkEl = container.querySelector('a[href*="/shop/pdp/"]');
                            let tiktokshop_id = null;
                            let product_url = null;
                            
                            if (linkEl && linkEl.href) {
                                product_url = linkEl.href;
                                // 从 URL 中提取 ID：https://www.tiktok.com/shop/pdp/xxx/1729641467854885041
                                const urlMatch = product_url.match(/\/shop\/pdp\/[^/]+\/(\d+)/);
                                if (urlMatch) {
                                    tiktokshop_id = urlMatch[1];
                                }
                            }
                            
                            // 提取图片 URL
                            const imgEl = container.querySelector('img');
                            const imageUrl = imgEl?.src || '';
                            
                            products.push({
                                name: name,
                                rating: rating,
                                sold: sold,
                                price: price,
                                original_price: originalPrice,
                                tiktokshop_id: tiktokshop_id,
                                product_url: product_url,
                                image_url: imageUrl,
                                rank: products.length + 1  // 按抓取顺序排名
                            });
                            
                            if (products.length <= 5) {
                                console.log('[' + (products.length-1) + '] ' + name.substring(0, 50));
                                console.log('    Rating: ' + rating + ', Sold: ' + sold);
                                console.log('    Price: $' + price + ', Original: $' + originalPrice);
                                console.log('    TikTokShop ID: ' + tiktokshop_id);
                                console.log('    URL: ' + product_url);
                                console.log('    Image: ' + imageUrl.substring(0, 50));
                            }
                            
                            break; // 找到商品容器，跳出循环
                        }
                        
                        container = container.parentElement;
                        depth++;
                    }
                } catch (e) {
                    console.log('商品 ' + idx + ' 解析失败:', e.message);
                }
            });
            
            return products;
        }
    """
    
    products = page.evaluate(product_js)
    print(f"[OK] 找到 {len(products)} 个商品")
    
    return products


def fetch_and_save_category(category, page):
    """抓取单个分类并保存到独立文件（复用浏览器实例）"""
    
    base_dir = Path(__file__).parent.parent.parent.parent
    output_dir = base_dir / "output" / "scraping"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    
    # 生成文件名
    category_slug = category['name'].lower().replace(' ', '_').replace('&', 'and').replace('/', '_')
    output_file = output_dir / f"tiktok_{category_slug}_{timestamp}.json"
    
    print(f"\n=== 抓取分类：{category['name']} ===")
    print(f"[INFO] 文件名：{output_file.name}")
    
    # 访问分类页面
    print(f"[INFO] 访问分类页面：{category['name']}")
    print(f"[INFO] URL: {category['url']}")
    
    try:
        page.goto(category['url'], timeout=120000)
    except Exception as e:
        print(f"[ERROR] 访问页面失败：{e}")
        return None
    
    # 从页面提取商品数据
    data = fetch_category_products_from_page(page, category['name'])
    
    if not data:
        print(f"[WARN] 没有抓取到商品数据")
        return None
    
    # 去重处理：使用 tiktokshop_id 作为唯一标识
    print(f"[INFO] 正在去重...")
    seen_ids = set()
    unique_products = []
    duplicates = 0
    
    for product in data:
        tiktokshop_id = product.get('tiktokshop_id')
        if tiktokshop_id and tiktokshop_id not in seen_ids:
            seen_ids.add(tiktokshop_id)
            unique_products.append(product)
            # 去重后只保留前 20 个
            if len(unique_products) >= 20:
                print(f"[INFO] 已达到 20 个商品，停止处理")
                break
        elif tiktokshop_id:
            duplicates += 1
    
    if duplicates > 0:
        print(f"[OK] 去重完成：原始 {len(data)} 个商品，去重后 {len(unique_products)} 个，删除 {duplicates} 个重复项")
    
    data = unique_products
    
    # 添加元数据
    enriched_data = {
        "metadata": {
            "platform": "tiktok",
            "category": category['name'],
            "category_slug": category_slug,
            "category_url": category['url'],
            "scraped_at": now.isoformat(),
            "scraped_date": now.strftime("%Y-%m-%d"),
            "scraped_time": now.strftime("%H:%M:%S"),
            "total_items": len(data)
        },
        "products": data
    }
    
    # 保存到 JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(enriched_data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 分类 {category['name']} 抓取完成，共 {len(data)} 个商品")
    print(f"[OK] 数据已保存到：{output_file}")
    
    # 打印前 5 条数据
    if data:
        print("\n[示例数据] 前 5 条:")
        for item in data[:5]:
            sold_info = f" ({item.get('sold', 'N/A')})" if item.get('sold') else ""
            print(f"  - {item.get('name', 'N/A')}${item.get('price', 'N/A')}{sold_info}")
    
    return enriched_data


def fetch_all_categories():
    """抓取所有 TikTok Shop 分类的热销数据（复用浏览器实例）"""
    
    print(f"[INFO] 开始抓取 TikTok Shop 所有分类...")
    
    with sync_playwright() as p:
        # 使用 persistent context 复用登录状态
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
        
        # 访问首页 - 使用正确的域名
        print(f"[INFO] 访问 TikTok Shop 首页...")
        page.goto("https://shop.tiktok.com", timeout=120000)
        
        # 等待页面加载
        page.wait_for_timeout(random_wait(10000, 15000))
        
        # 滚动页面
        print(f"[INFO] 滚动页面加载更多内容...")
        for i in range(5):
            try:
                page.evaluate("""
                    () => {
                        if (document.body) {
                            window.scrollTo(0, document.body.scrollHeight);
                        }
                    }
                """)
            except Exception as e:
                print(f"[WARN] 滚动失败：{e}")
            page.wait_for_timeout(random_wait(3000, 5000))
        
        # 最终等待
        page.wait_for_timeout(random_wait(10000, 20000))
        
        # 提取类目
        categories = extract_categories(page)
        
        if not categories:
            print(f"[ERROR] 没有提取到任何类目！")
            browser.close()
            return
        
        # 保存类目列表
        categories_file = Path(__file__).parent.parent / "screenshots" / "categories.json"
        categories_file.parent.mkdir(parents=True, exist_ok=True)
        with open(categories_file, "w", encoding="utf-8") as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)
        print(f"[OK] 类目列表已保存到：{categories_file}")
        
        # 抓取每个分类（复用同一个 page 和 browser）
        # 测试模式：只抓第一个类目验证逻辑
        test_categories = categories[:1]
        print(f"[INFO] 测试模式：只抓取前 {len(test_categories)} 个类目")
        for i, category in enumerate(test_categories):
            fetch_and_save_category(category, page)
            if i < len(test_categories) - 1:
                wait_ms = random_wait(5000, 10000)
                print(f"\n[INFO] 等待 {wait_ms}ms 后开始下一个分类...")
                import time
                time.sleep(wait_ms / 1000)
        
        browser.close()
    
    print(f"\n[OK] 抓取完成！")


if __name__ == "__main__":
    fetch_all_categories()