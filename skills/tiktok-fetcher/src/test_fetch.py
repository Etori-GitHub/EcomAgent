#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok Shop 抓取测试脚本
使用已保存的类目列表进行测试
"""

import json
import random
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright


def random_wait(min_ms=1000, max_ms=3000):
    """随机等待"""
    wait_ms = random.randint(min_ms, max_ms)
    print(f"[INFO] 等待 {wait_ms}ms...")
    return wait_ms


def fetch_category_products(page, category):
    """抓取单个类目的商品"""
    
    print(f"\n=== 抓取类目：{category['name']} ===")
    print(f"[INFO] URL: {category['url']}")
    
    try:
        page.goto(category['url'], timeout=120000)
    except Exception as e:
        print(f"[ERROR] 访问失败：{e}")
        return None
    
    # 等待页面加载
    page.wait_for_timeout(random_wait(10000, 20000))
    
    # 滚动加载更多
    for i in range(3):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(random_wait(3000, 5000))
    
    # 提取商品数据
    product_js = """
        () => {
            const products = [];
            
            // 找到所有包含价格的元素
            const priceElements = Array.from(document.querySelectorAll('*')).filter(el => {
                const text = el.innerText || '';
                return text.includes('$') && /\\$\\d+\\.\\d+/.test(text);
            });
            
            console.log('找到 ' + priceElements.length + ' 个价格元素');
            
            priceElements.forEach((priceEl, idx) => {
                try {
                    const text = priceEl.innerText.trim();
                    
                    // 跳过导航元素
                    if (text.includes('Orders') || text.includes('销售') || text.includes('TikTok Shop')) {
                        return;
                    }
                    
                    // 向上查找商品容器
                    let container = priceEl.parentElement;
                    let depth = 0;
                    
                    while (container && depth < 6) {
                        const nameEl = container.querySelector('h3');
                        
                        if (nameEl) {
                            const name = nameEl.innerText.trim();
                            
                            if (!name || name.length < 5) {
                                container = container.parentElement;
                                depth++;
                                continue;
                            }
                            
                            // 提取价格
                            const priceMatch = text.match(/\\$(\\d+\\.\\d+)/);
                            const price = priceMatch ? parseFloat(priceMatch[1]) : null;
                            
                            // 提取商品 URL 和 ID
                            const linkEl = container.querySelector('a[href*="/pdp/"]');
                            let tiktokshop_id = null;
                            let product_url = null;
                            
                            if (linkEl && linkEl.href) {
                                product_url = linkEl.href;
                                const urlMatch = product_url.match(/\\/pdp\\/[^/]+\\/(\d+)/);
                                if (urlMatch) {
                                    tiktokshop_id = urlMatch[1];
                                }
                            }
                            
                            // 提取图片
                            const imgEl = container.querySelector('img');
                            const imageUrl = imgEl?.src || '';
                            
                            // 提取销量
                            const soldEl = Array.from(container.querySelectorAll('span')).find(el => 
                                el.innerText.includes('已售出')
                            );
                            const sold = soldEl ? soldEl.innerText.trim() : null;
                            
                            products.push({
                                name: name,
                                price: price,
                                sold: sold,
                                tiktokshop_id: tiktokshop_id,
                                product_url: product_url,
                                image_url: imageUrl,
                                rank: products.length + 1
                            });
                            
                            break;
                        }
                        
                        container = container.parentElement;
                        depth++;
                    }
                } catch (e) {
                    // 忽略错误
                }
            });
            
            return products;
        }
    """
    
    products = page.evaluate(product_js)
    print(f"[OK] 找到 {len(products)} 个商品")
    
    return products


def main():
    """主函数"""
    
    base_dir = Path(__file__).parent.parent.parent.parent
    categories_file = base_dir / "skills" / "tiktok-fetcher" / "screenshots" / "categories.json"
    output_dir = base_dir / "output" / "scraping"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 读取已保存的类目列表
    with open(categories_file, "r", encoding="utf-8") as f:
        categories = json.load(f)
    
    print(f"[INFO] 加载了 {len(categories)} 个类目")
    
    # 测试模式：只抓第一个
    test_categories = categories[:1]
    print(f"[INFO] 测试模式：只抓前 {len(test_categories)} 个类目")
    
    with sync_playwright() as p:
        # 使用 persistent context 复用登录状态
        user_data_dir = r"C:\Users\Etroi\AppData\Local\Google\Chrome\User Data\Profile 1"
        
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            slow_mo=500,
            args=[
                '--disable-blink-features=AutomationControlled',
            ]
        )
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        for category in test_categories:
            products = fetch_category_products(page, category)
            
            if products:
                # 去重
                seen_ids = set()
                unique = []
                for p in products:
                    if p.get('tiktokshop_id') and p['tiktokshop_id'] not in seen_ids:
                        seen_ids.add(p['tiktokshop_id'])
                        unique.append(p)
                        if len(unique) >= 20:
                            break
                
                # 保存
                now = datetime.now()
                timestamp = now.strftime("%Y%m%d_%H%M%S")
                category_slug = category['name'].lower().replace(' ', '_')
                output_file = output_dir / f"tiktok_{category_slug}_{timestamp}.json"
                
                data = {
                    "metadata": {
                        "platform": "tiktok",
                        "category": category['name'],
                        "category_url": category['url'],
                        "scraped_at": now.isoformat(),
                        "total_items": len(unique)
                    },
                    "products": unique
                }
                
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"[OK] 保存到：{output_file}")
                print(f"[OK] 共 {len(unique)} 个商品")
                
                # 打印示例
                for item in unique[:3]:
                    print(f"  - {item['name'][:40]}... ${item.get('price', 'N/A')}")
        
        browser.close()


if __name__ == "__main__":
    main()
