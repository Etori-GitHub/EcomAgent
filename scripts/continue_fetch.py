#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""继续抓取剩余分类"""

import json
import random
import sys
from pathlib import Path
from datetime import datetime

from playwright.sync_api import sync_playwright

# 需要抓取的分类（从中断处继续）
REMAINING_CATEGORIES = [
    {"name": "Grocery & Gourmet Food", "slug": "grocery", "url": "https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food/zgbs/grocery/ref=zg_bs_nav_grocery_0"},
    {"name": "Handmade Products", "slug": "handmade", "url": "https://www.amazon.com/Best-Sellers-Handmade-Products/zgbs/handmade/ref=zg_bs_nav_handmade_0"},
    {"name": "Health & Household", "slug": "hpc", "url": "https://www.amazon.com/Best-Sellers-Health-Household/zgbs/hpc/ref=zg_bs_nav_hpc_0"},
    {"name": "Home & Kitchen", "slug": "home-garden", "url": "https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/ref=zg_bs_nav_home-garden_0"},
    {"name": "Industrial & Scientific", "slug": "industrial", "url": "https://www.amazon.com/Best-Sellers-Industrial-Scientific/zgbs/industrial/ref=zg_bs_nav_industrial_0"},
    {"name": "Kindle Store", "slug": "digital-text", "url": "https://www.amazon.com/Best-Sellers-Kindle-Store/zgbs/digital-text/ref=zg_bs_nav_digital-text_0"},
    {"name": "Kitchen & Dining", "slug": "kitchen", "url": "https://www.amazon.com/Best-Sellers-Kitchen-Dining/zgbs/kitchen/ref=zg_bs_nav_kitchen_0"},
    {"name": "Movies & TV", "slug": "movies-tv", "url": "https://www.amazon.com/best-sellers-movies-TV-DVD-Blu-ray/zgbs/movies-tv/ref=zg_bs_nav_movies-tv_0"},
    {"name": "Musical Instruments", "slug": "musical-instruments", "url": "https://www.amazon.com/Best-Sellers-Musical-Instruments/zgbs/musical-instruments/ref=zg_bs_nav_musical-instruments_0"},
    {"name": "Office Products", "slug": "office-products", "url": "https://www.amazon.com/Best-Sellers-Office-Products/zgbs/office-products/ref=zg_bs_nav_office-products_0"},
    {"name": "Patio, Lawn & Garden", "slug": "lawn-garden", "url": "https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden/zgbs/lawn-garden/ref=zg_bs_nav_lawn-garden_0"},
    {"name": "Pet Supplies", "slug": "pet-supplies", "url": "https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_nav_pet-supplies_0"},
    {"name": "Software", "slug": "software", "url": "https://www.amazon.com/best-sellers-software/zgbs/software/ref=zg_bs_nav_software_0"},
    {"name": "Sports & Outdoors", "slug": "sporting-goods", "url": "https://www.amazon.com/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods/ref=zg_bs_nav_sporting-goods_0"},
    {"name": "Sports Collectibles", "slug": "sports-collectibles", "url": "https://www.amazon.com/Best-Sellers-Sports-Collectibles/zgbs/sports-collectibles/ref=zg_bs_nav_sports-collectibles_0"},
    {"name": "Tools & Home Improvement", "slug": "hi", "url": "https://www.amazon.com/Best-Sellers-Tools-Home-Improvement/zgbs/hi/ref=zg_bs_nav_hi_0"},
    {"name": "Toys & Games", "slug": "toys-and-games", "url": "https://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games/ref=zg_bs_nav_toys-and-games_0"},
    {"name": "Unique Finds", "slug": "boost", "url": "https://www.amazon.com/Best-Sellers-Unique-Finds/zgbs/boost/ref=zg_bs_nav_boost_0"},
    {"name": "Video Games", "slug": "videogames", "url": "https://www.amazon.com/best-sellers-video-games/zgbs/videogames/ref=zg_bs_nav_videogames_0"},
]

BASE_DIR = Path(__file__).parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output" / "scraping"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def fetch_category(page, category, pages=2):
    """抓取单个分类"""
    
    js_code = """
        () => {
            const results = [];
            const rows = document.querySelectorAll('li.zg-no-numbers, div#gridItemRoot > div');
            rows.forEach((row, idx) => {
                try {
                    const rankEl = row.querySelector('.zg-bdg-text, span.zg-bdg-text');
                    const rank = rankEl ? parseInt(rankEl.innerText.replace('#', '').trim()) : idx + 1;
                    
                    const allLinks = row.querySelectorAll('a.a-link-normal');
                    let link = null;
                    let asin = '';
                    let href = '';
                    
                    for (const a of allLinks) {
                        const h = a.href || '';
                        const match = h.match(/\\/dp\\/([A-Z0-9]{10})/);
                        if (match) {
                            link = a;
                            asin = match[1];
                            href = h;
                            break;
                        }
                    }
                    
                    let name = '';
                    const nameEl = row.querySelector('div._cDEzb_p13n-sc-css-line-clamp-3_g3dy1, div[class*="line-clamp"]');
                    if (nameEl?.innerText?.trim()) name = nameEl.innerText.trim();
                    if (!name) {
                        const imgEl = row.querySelector('img');
                        if (imgEl?.alt?.trim()) name = imgEl.alt.trim();
                    }
                    if (!name && link?.innerText?.trim()) name = link.innerText.trim();
                    
                    const imgEl = row.querySelector('img');
                    let imageUrl = imgEl?.src || '';
                    if (imageUrl && imageUrl.includes('._')) imageUrl = imageUrl.replace(/\\._[^.]+\\./, '.');
                    
                    let price = null;
                    const priceEl = row.querySelector('span._cDEzb_p13n-sc-price_3mJ9Z, span[class*="p13n-sc-price"]');
                    if (priceEl) {
                        const priceText = priceEl.innerText.trim();
                        const priceMatch = priceText.match(/\\$?([\\d.]+)/);
                        if (priceMatch) price = parseFloat(priceMatch[1]);
                    }
                    
                    let rating = null;
                    let ratingCount = null;
                    const ratingEl = row.querySelector('span.a-icon-alt');
                    if (ratingEl) {
                        const ratingText = ratingEl.innerText || '';
                        const ratingMatch = ratingText.match(/([\\d.]+)\\s*out of/);
                        if (ratingMatch) rating = parseFloat(ratingMatch[1]);
                    }
                    
                    if (rating === null) {
                        const ratingLink = row.querySelector('a[aria-label*="stars"]');
                        if (ratingLink) {
                            const ariaLabel = ratingLink.getAttribute('aria-label') || '';
                            const ratingMatch = ariaLabel.match(/([\\d.]+)\\s*out of/);
                            if (ratingMatch) rating = parseFloat(ratingMatch[1]);
                            const countMatch = ariaLabel.match(/([\\d,]+)\\s*ratings/);
                            if (countMatch) ratingCount = parseInt(countMatch[1].replace(/,/g, ''));
                        }
                    }
                    
                    if (ratingCount === null) {
                        const countEl = row.querySelector('span.a-size-small');
                        if (countEl) {
                            const countText = countEl.innerText.replace(/[^\\d]/g, '');
                            if (countText && parseInt(countText) > 0) ratingCount = parseInt(countText);
                        }
                    }
                    
                    if (asin) {
                        results.push({
                            rank, name, asin,
                            product_url: `https://www.amazon.com/dp/${asin}`,
                            image_url: imageUrl,
                            price, rating, rating_count: ratingCount,
                            category: 'CAT_PLACEHOLDER',
                            subcategory: 'CAT_PLACEHOLDER'
                        });
                    }
                } catch (e) {}
            });
            return results;
        }
    """
    
    all_items = []
    
    for page_num in range(1, pages + 1):
        if page_num == 1:
            url = category['url']
        else:
            url = category['url'].replace('/ref=zg_bs_nav_', f'/ref=zg_bs_pg_{page_num}_')
        
        print(f"[INFO] 访问第 {page_num} 页: {url}", flush=True)
        page.goto(url, timeout=60000)
        wait_ms = random.randint(10000, 20000)
        page.wait_for_timeout(wait_ms)
        
        for _ in range(3):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(random.randint(3000, 5000))
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(500)
        
        page_js = js_code.replace('CAT_PLACEHOLDER', category['name'])
        items = page.evaluate(page_js)
        print(f"[INFO] 第 {page_num} 页成功提取 {len(items)} 个商品", flush=True)
        all_items.extend(items)
    
    # 去重
    seen_asins = set()
    unique_products = []
    for product in all_items:
        asin = product.get('asin')
        if asin and asin not in seen_asins:
            seen_asins.add(asin)
            unique_products.append(product)
    
    # 保存
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"amazon_{category['slug']}_{timestamp}.json"
    
    enriched_data = {
        "metadata": {
            "platform": "amazon",
            "category": category['name'],
            "category_slug": category['slug'],
            "category_url": category['url'],
            "scraped_at": now.isoformat(),
            "scraped_date": now.strftime("%Y-%m-%d"),
            "total_items": len(unique_products)
        },
        "products": unique_products
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(enriched_data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 分类 {category['name']} 抓取完成,共 {len(unique_products)} 个商品", flush=True)
    print(f"[OK] 数据已保存到:{output_file}", flush=True)
    
    return enriched_data

def main():
    print(f"[INFO] 继续抓取剩余 {len(REMAINING_CATEGORIES)} 个分类...", flush=True)
    
    total_items = 0
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=500)
        page = browser.new_page()
        
        page.add_init_script("""
            () => {
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                navigator.languages = ['en-US', 'en'];
                navigator.plugins = [1, 2, 3, 4, 5];
            }
        """)
        page.set_viewport_size({"width": 1920, "height": 5000})
        
        for i, category in enumerate(REMAINING_CATEGORIES):
            print(f"\n=== [{i+1}/{len(REMAINING_CATEGORIES)}] 抓取分类:{category['name']} ===", flush=True)
            data = fetch_category(page, category)
            total_items += data['metadata']['total_items']
            
            if i < len(REMAINING_CATEGORIES) - 1:
                wait_ms = random.randint(10000, 20000)
                print(f"[INFO] 等待 {wait_ms}ms 后开始下一个分类...", flush=True)
                import time
                time.sleep(wait_ms / 1000)
        
        browser.close()
    
    print(f"\n[OK] 所有剩余分类抓取完成! 共 {total_items} 个商品", flush=True)

if __name__ == "__main__":
    main()