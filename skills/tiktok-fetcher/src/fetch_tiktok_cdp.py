#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok Shop 热销榜单抓取脚本 - CDP 版本
连接到已打开的 Chrome 实例进行抓取

使用方法：
1. 先启动带调试端口的 Chrome：
   chrome.exe --remote-debugging-port=9222
2. 运行此脚本

功能：
1. 连接到已打开的 Chrome（复用登录状态）
2. 从首页提取类目列表
3. 抓取商品数据
4. 保存到 JSON 文件
"""

import json
import random
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright


def random_wait(min_ms=1000, max_ms=3000):
    """随机等待，避免被反爬"""
    wait_ms = random.randint(min_ms, max_ms)
    print(f"[INFO] 等待 {wait_ms}ms...")
    return wait_ms


def extract_categories(page):
    """从首页提取类目列表（使用 /shop/c/ 过滤）"""
    
    print(f"\n[INFO] 正在提取类目列表...")
    
    category_js = """
        () => {
            const categories = [];
            
            // 策略：找到所有包含 /shop/c/ 的链接
            const allLinks = Array.from(document.querySelectorAll('a'));
            
            console.log('=== 总共找到 ' + allLinks.length + ' 个链接 ===');
            
            allLinks.forEach((link, idx) => {
                const href = link.href;
                const text = (link.innerText || link.textContent || '').trim();
                const dataId = link.getAttribute('data-id');
                
                // 只提取包含 /c/ 的链接（新格式：shop.tiktok.com/us/c/xxx/123）
                // 过滤掉 deals 页面
                if (href && href.includes('/c/') && !href.includes('/deals/') && text) {
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
    """从已打开的页面抓取商品数据"""
    
    # 等待页面加载
    page.wait_for_timeout(random_wait(10000, 20000))
    
    # 点击"查看更多"按钮加载更多商品
    print(f"[INFO] 点击'查看更多'按钮加载更多商品...")
    try:
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
    
    # 提取商品数据
    print(f"[INFO] 正在提取商品数据...")
    
    product_js = """
        () => {
            const products = [];
            
            // 策略：从价格元素向上查找商品容器
            const priceElements = Array.from(document.querySelectorAll('*')).filter(el => {
                const text = el.innerText || el.textContent || '';
                return text.includes('$') && /\\$\\d+\\.\\d+/.test(text);
            });
            
            console.log('=== 找到 ' + priceElements.length + ' 个包含价格的元素 ===');
            
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
                        const nameEl = container.querySelector('h3');
                        const ratingEl = container.querySelector('span');
                        
                        if (nameEl && ratingEl) {
                            const name = nameEl.innerText.trim();
                            
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
                            
                            // 提取销售量
                            const soldEl = Array.from(container.querySelectorAll('span')).find(el => 
                                el.innerText.includes('已售出')
                            );
                            const sold = soldEl ? soldEl.innerText.trim() : null;
                            
                            // 提取价格
                            const priceMatch = text.match(/\\$(\\d+\\.\\d+)/);
                            const price = priceMatch ? parseFloat(priceMatch[1]) : null;
                            
                            // 提取原价
                            const originalPriceEl = Array.from(container.querySelectorAll('span')).find(el => 
                                el.innerText.startsWith('$') && el.classList.contains('line-through')
                            );
                            const originalPrice = originalPriceEl ? 
                                parseFloat(originalPriceEl.innerText.replace('$', '')) : null;
                            
                            // 提取商品详情页 URL（新格式：shop.tiktok.com/us/pdp/xxx/123）
                            const linkEl = container.querySelector('a[href*="/pdp/"]');
                            let tiktokshop_id = null;
                            let product_url = null;
                            
                            if (linkEl && linkEl.href) {
                                product_url = linkEl.href;
                                // 从 URL 中提取 ID：https://shop.tiktok.com/us/pdp/xxx/1732278989017747991
                                const urlMatch = product_url.match(/\/pdp\/[^/]+\/(\d+)/);
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
                                rank: products.length + 1
                            });
                            
                            if (products.length <= 5) {
                                console.log('[' + (products.length-1) + '] ' + name.substring(0, 50));
                                console.log('    Price: $' + price + ', TikTokShop ID: ' + tiktokshop_id);
                            }
                            
                            break;
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
    """抓取单个分类并保存到独立文件"""
    
    base_dir = Path(__file__).parent.parent.parent.parent
    output_dir = base_dir / "output" / "scraping"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    
    category_slug = category['name'].lower().replace(' ', '_').replace('&', 'and').replace('/', '_')
    output_file = output_dir / f"tiktok_{category_slug}_{timestamp}.json"
    
    print(f"\n=== 抓取分类：{category['name']} ===")
    print(f"[INFO] 文件名：{output_file.name}")
    
    print(f"[INFO] 访问分类页面：{category['url']}")
    
    try:
        page.goto(category['url'], timeout=120000)
    except Exception as e:
        print(f"[ERROR] 访问页面失败：{e}")
        return None
    
    data = fetch_category_products_from_page(page, category['name'])
    
    if not data:
        print(f"[WARN] 没有抓取到商品数据")
        return None
    
    # 去重处理
    print(f"[INFO] 正在去重...")
    seen_ids = set()
    unique_products = []
    duplicates = 0
    
    for product in data:
        tiktokshop_id = product.get('tiktokshop_id')
        if tiktokshop_id and tiktokshop_id not in seen_ids:
            seen_ids.add(tiktokshop_id)
            unique_products.append(product)
            if len(unique_products) >= 20:
                print(f"[INFO] 已达到 20 个商品，停止处理")
                break
        elif tiktokshop_id:
            duplicates += 1
    
    if duplicates > 0:
        print(f"[OK] 去重完成：原始 {len(data)} 个，去重后 {len(unique_products)} 个")
    
    data = unique_products
    
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
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(enriched_data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 分类 {category['name']} 抓取完成，共 {len(data)} 个商品")
    print(f"[OK] 数据已保存到：{output_file}")
    
    if data:
        print("\n[示例数据] 前 5 条:")
        for item in data[:5]:
            sold_info = f" ({item.get('sold', 'N/A')})" if item.get('sold') else ""
            print(f"  - {item.get('name', 'N/A')[:40]}... ${item.get('price', 'N/A')}{sold_info}")
    
    return enriched_data


def fetch_all_categories_cdp():
    """抓取所有 TikTok Shop 分类的热销数据（连接到已打开的 Chrome）"""
    
    print(f"[INFO] 开始抓取 TikTok Shop 所有分类（CDP 模式）...")
    print(f"[INFO] 连接到 Chrome (端口 9222)...")
    
    with sync_playwright() as p:
        try:
            # 连接到已运行的 Chrome
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            print(f"[OK] 连接成功！浏览器版本: {browser.version}")
        except Exception as e:
            print(f"[ERROR] 连接失败：{e}")
            print(f"[INFO] 请确保 Chrome 已用以下参数启动：")
            print(f"       chrome.exe --remote-debugging-port=9222 --user-data-dir=\"...\" --profile-directory=\"Profile 1\"")
            return
        
        # 获取上下文
        contexts = browser.contexts
        if not contexts:
            print(f"[ERROR] 没有找到任何上下文")
            return
        
        context = contexts[0]
        print(f"[INFO] 找到上下文，当前有 {len(context.pages)} 个页面")
        
        # 查找 TikTok Shop 页面，或创建新页面
        tiktok_page = None
        for page in context.pages:
            if "tiktok.com" in page.url:
                tiktok_page = page
                print(f"[INFO] 找到 TikTok 页面: {page.url}")
                break
        
        if not tiktok_page:
            tiktok_page = context.new_page()
            print(f"[INFO] 创建新页面")
        
        # 访问 TikTok Shop 首页
        print(f"[INFO] 访问 TikTok Shop 首页...")
        tiktok_page.goto("https://www.tiktok.com/shop", timeout=120000)
        
        # 等待页面加载
        tiktok_page.wait_for_timeout(random_wait(10000, 15000))
        
        # 滚动页面
        print(f"[INFO] 滚动页面加载更多内容...")
        for i in range(5):
            try:
                tiktok_page.evaluate("""
                    () => {
                        if (document.body) {
                            window.scrollTo(0, document.body.scrollHeight);
                        }
                    }
                """)
            except Exception as e:
                print(f"[WARN] 滚动失败：{e}")
            tiktok_page.wait_for_timeout(random_wait(3000, 5000))
        
        # 最终等待
        tiktok_page.wait_for_timeout(random_wait(10000, 20000))
        
        # 提取类目
        categories = extract_categories(tiktok_page)
        
        if not categories:
            print(f"[ERROR] 没有提取到任何类目！")
            return
        
        # 保存类目列表
        categories_file = Path(__file__).parent.parent / "screenshots" / "categories.json"
        categories_file.parent.mkdir(parents=True, exist_ok=True)
        with open(categories_file, "w", encoding="utf-8") as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)
        print(f"[OK] 类目列表已保存到：{categories_file}")
        
        # 抓取每个分类（测试模式：只抓第一个分类）
        for i, category in enumerate(categories[:1]):
            fetch_and_save_category(category, tiktok_page)
            if i < len(categories[:1]) - 1:
                wait_ms = random_wait(5000, 10000)
                print(f"\n[INFO] 等待 {wait_ms}ms 后开始下一个分类...")
                time.sleep(wait_ms / 1000)
        
        # 注意：不关闭 browser，因为它是外部启动的
        print(f"\n[OK] 抓取完成！")
        print(f"[INFO] Chrome 浏览器保持打开状态")


if __name__ == "__main__":
    fetch_all_categories_cdp()
