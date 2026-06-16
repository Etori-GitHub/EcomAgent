#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
亚马逊 Best Sellers 全分类抓取脚本
功能:
1. 从首页提取所有分类列表
2. 遍历每个分类抓取热销商品
3. 保存到 JSON 文件
"""

import json
import random
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
    """随机等待,避免被反爬"""
    wait_ms = random.randint(min_ms, max_ms)
    print(f"[INFO] 等待 {wait_ms}ms 避免反爬...")
    return wait_ms


def extract_categories(page):
    """从 Amazon Best Sellers 首页提取所有分类链接"""

    print(f"\n[INFO] 正在提取分类列表...")

    category_js = """
        () => {
            const categories = [];

            // 找到 Navigation Tree 容器
            const navTree = document.querySelector('div[role="group"][aria-label="Navigation Tree"]');

            if (!navTree) {
                console.log('未找到 Navigation Tree 容器');
                return [];
            }

            console.log('找到 Navigation Tree 容器');

            // 找到 ul 列表
            const ul = navTree.querySelector('ul._p13n-zg-nav-tree-all_style_zg-browse-group__88fbz');

            if (!ul) {
                console.log('未找到 ul 列表');
                return [];
            }

            console.log('找到 ul 列表');

            // 提取所有 li 中的分类
            const lis = ul.querySelectorAll('li');
            console.log('找到 ' + lis.length + ' 个 li 元素');

            lis.forEach((li, idx) => {
                const link = li.querySelector('a');
                if (link) {
                    const href = link.getAttribute('href') || '';
                    const text = link.innerText.trim();

                    // 提取分类 slug
                    const slugMatch = href.match(/\\/zgbs\\/([^\\/]+)/);
                    const slug = slugMatch ? slugMatch[1] : '';

                    // 构建完整 URL
                    const fullUrl = href.startsWith('http') ? href : 'https://www.amazon.com' + href;

                    categories.push({
                        name: text,
                        url: fullUrl,
                        slug: slug
                    });

                    if (idx < 5) {
                        console.log('[' + idx + '] ' + text + ' -> ' + slug);
                    }
                }
            });

            return categories;
        }
    """

    categories = page.evaluate(category_js)
    print(f"[OK] 找到 {len(categories)} 个分类")

    return categories


def fetch_category_bestsellers_pages(page, category, pages=2):
    """抓取指定分类的 Best Sellers 榜单(前 N 页)"""

    all_items = []

    # 简化的数据提取
    js_code = """
        () => {
            const results = [];
            const rows = document.querySelectorAll('li.zg-no-numbers, div#gridItemRoot > div');

            console.log(`找到 ${rows.length} 个商品行`);

            rows.forEach((row, idx) => {
                try {
                    // 排名
                    const rankEl = row.querySelector('.zg-bdg-text, span.zg-bdg-text');
                    const rank = rankEl ? parseInt(rankEl.innerText.replace('#', '').trim()) : idx + 1;

                    // 商品链接和 ASIN
                    const allLinks = row.querySelectorAll('a.a-link-normal');
                    let link = null;
                    let asin = '';
                    let href = '';
                    
                    // 遍历所有链接找到商品链接
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

                    // 商品名称 - 按可靠性优先级提取
                    let name = '';
                    
                    // 方法1: 从专门的名称容器获取 (最可靠)
                    const nameEl = row.querySelector('div._cDEzb_p13n-sc-css-line-clamp-3_g3dy1, div[class*="line-clamp"], div[class*="p13n-sc-truncate"]');
                    if (nameEl?.innerText?.trim()) {
                        name = nameEl.innerText.trim();
                    }
                    
                    // 方法2: 从图片 alt 属性获取（也很可靠）
                    if (!name) {
                        const imgEl = row.querySelector('img');
                        if (imgEl?.alt?.trim()) {
                            name = imgEl.alt.trim();
                        }
                    }
                    
                    // 方法3: 从链接文字获取
                    if (!name && link?.innerText?.trim()) {
                        name = link.innerText.trim();
                    }
                    
                    // 方法4: 从 title 属性获取
                    if (!name) {
                        const titledEl = row.querySelector('[title]');
                        if (titledEl?.title?.trim()) {
                            name = titledEl.title.trim();
                        }
                    }
                    
                    // 图片URL
                    const imgEl = row.querySelector('img');
                    let imageUrl = imgEl?.src || '';
                    // 清理图片URL，获取高清版本
                    if (imageUrl && imageUrl.includes('._')) {
                        imageUrl = imageUrl.replace(/\\._[^.]+\\./, '.');
                    }
                    
                    // 价格 - 根据实际页面结构更新
                    // <span class="_cDEzb_p13n-sc-price_3mJ9Z">$19.99</span>
                    let price = null;
                    const priceEl = row.querySelector('span._cDEzb_p13n-sc-price_3mJ9Z, span[class*=\"p13n-sc-price\"]');
                    if (priceEl) {
                        const priceText = priceEl.innerText.trim();
                        const priceMatch = priceText.match(/\\$?([\\d.]+)/);
                        if (priceMatch) {
                            price = parseFloat(priceMatch[1]);
                        }
                    }
                    
                    // 备用价格选择器
                    if (price === null) {
                        const priceEl2 = row.querySelector('span.a-color-price');
                        if (priceEl2) {
                            const priceText = priceEl2.innerText.trim();
                            const priceMatch = priceText.match(/\\$?([\\d.]+)/);
                            if (priceMatch) {
                                price = parseFloat(priceMatch[1]);
                            }
                        }
                    }

                    // 评分 - 根据实际页面结构
                    // <span class="a-icon-alt">4.1 out of 5 stars</span>
                    let rating = null;
                    let ratingCount = null;
                    
                    // 方法1: 从 a-icon-alt 获取评分
                    const ratingEl = row.querySelector('span.a-icon-alt');
                    if (ratingEl) {
                        const ratingText = ratingEl.innerText || '';
                        const ratingMatch = ratingText.match(/([\\d.]+)\\s*out of/);
                        if (ratingMatch) {
                            rating = parseFloat(ratingMatch[1]);
                        }
                    }
                    
                    // 方法2: 从 aria-label 获取
                    if (rating === null) {
                        const ratingLink = row.querySelector('a[aria-label*=\"stars\"]');
                        if (ratingLink) {
                            const ariaLabel = ratingLink.getAttribute('aria-label') || '';
                            // 格式: "4.1 out of 5 stars, 14,143 ratings"
                            const ratingMatch = ariaLabel.match(/([\\d.]+)\\s*out of/);
                            if (ratingMatch) {
                                rating = parseFloat(ratingMatch[1]);
                            }
                            // 提取评价数
                            const countMatch = ariaLabel.match(/([\\d,]+)\\s*ratings/);
                            if (countMatch) {
                                ratingCount = parseInt(countMatch[1].replace(/,/g, ''));
                            }
                        }
                    }
                    
                    // 评价数量 - 从 span.a-size-small 获取
                    if (ratingCount === null) {
                        // <span aria-hidden="true" class="a-size-small">14,143</span>
                        const countEl = row.querySelector('span.a-size-small');
                        if (countEl) {
                            const countText = countEl.innerText.replace(/[^\\d]/g, '');
                            if (countText && parseInt(countText) > 0) {
                                ratingCount = parseInt(countText);
                            }
                        }
                    }

                    console.log(`商品 ${idx}: rank=${rank}, asin=${asin}, price=${price}, rating=${rating}, count=${ratingCount}`);

                    if (asin) {
                        const productUrl = `https://www.amazon.com/dp/${asin}`;

                        results.push({
                            rank,
                            name,
                            asin,
                            product_url: productUrl,
                            image_url: imageUrl,
                            price: price,
                            rating: rating,
                            rating_count: ratingCount,
                            category: 'CATEGORY_PLACEHOLDER',
                            subcategory: 'SUBCATEGORY_PLACEHOLDER'
                        });
                        
                        // 详细打印每个商品
                        if (idx < 3) {
                            console.log(`[DEBUG] 商品${idx} 详情: name=${name.substring(0,30)}, price=${price}, rating=${rating}, count=${ratingCount}`);
                        }
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
            url = category['url']
        else:
            # 第2页开始,将 ref=zg_bs_nav_xxx_0 改为 ref=zg_bs_pg_2_xxx_0
            url = category['url'].replace('/ref=zg_bs_nav_', f'/ref=zg_bs_pg_{page_num}_')

        print(f"[INFO] 访问第 {page_num} 页: {url}")
        page.goto(url, timeout=60000)

        # 等待页面加载
        page.wait_for_timeout(random_wait(10000, 20000))
        
        # 滚动页面触发懒加载
        for _ in range(3):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(random_wait(3000, 5000))
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(500)

        # 使用字符串替换注入变量
        page_js_code = js_code.replace('CATEGORY_PLACEHOLDER', category['name']).replace('SUBCATEGORY_PLACEHOLDER', category['name'])
        items = page.evaluate(page_js_code)

        print(f"[INFO] 第 {page_num} 页成功提取 {len(items)} 个商品")
        
        # 打印前3个商品的详细数据
        if items:
            print("[DEBUG] 提取的商品示例:")
            for i, item in enumerate(items[:3]):
                print(f"  [{i}] asin={item.get('asin')}, price={item.get('price')}, rating={item.get('rating')}, count={item.get('rating_count')}")
        
        all_items.extend(items)

    return all_items


def fetch_and_save_category(category, page, pages=2):
    """抓取单个分类并保存到独立文件"""

    base_dir = Path(__file__).parent.parent.parent.parent
    output_dir = base_dir / "output" / "scraping"
    output_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    # 生成文件名
    category_slug = category['slug']
    output_file = output_dir / f"amazon_{category_slug}_{timestamp}.json"

    print(f"\n=== 抓取分类:{category['name']} (前 {pages} 页) ===")
    print(f"[INFO] 文件名:{output_file.name}")

    # 添加重试机制
    max_retries = 3
    retry_count = 0
    last_error = None

    while retry_count < max_retries:
        try:
            data = fetch_category_bestsellers_pages(page, category, pages)

            # 去重处理:使用 asin 作为唯一标识
            print(f"[INFO] 正在去重...")
            seen_asins = set()
            unique_products = []
            duplicates = 0

            for product in data:
                asin = product.get('asin')
                if asin and asin not in seen_asins:
                    seen_asins.add(asin)
                    unique_products.append(product)
                elif asin:
                    duplicates += 1

            if duplicates > 0:
                print(f"[OK] 去重完成:原始 {len(data)} 个商品,去重后 {len(unique_products)} 个,删除 {duplicates} 个重复项")

            data = unique_products

            # 添加元数据
            enriched_data = {
                "metadata": {
                    "platform": "amazon",
                    "category": category['name'],
                    "category_slug": category['slug'],
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

            print(f"[OK] 分类 {category['name']} 抓取完成,共 {len(data)} 个商品")
            print(f"[OK] 数据已保存到:{output_file}")

            # 打印前5条数据作为示例
            if data:
                print("\n[示例数据] 前5条:")
                for item in data[:5]:
                    print(f"  - {item['rank']}. {item['name'][:50]}... (${item['price']}) - {item['rating']}★ ({item['rating_count']}评)")

            return enriched_data
        except Exception as e:
            retry_count += 1
            last_error = e
            print(f"[WARN] 失败 {retry_count}/{max_retries}: {e}")
            if retry_count < max_retries:
                wait_ms = random_wait(10000, 20000)
                print(f"[INFO] 等待 {wait_ms}ms 后重试...")
                import time
                time.sleep(wait_ms / 1000)

    print(f"[ERROR] 分类 {category['name']} 抓取失败(已达最大重试次数)")
    raise last_error


def fetch_all_categories(pages=2, headless=True):
    """抓取所有 Amazon Best Sellers 分类的热销数据"""

    print(f"[INFO] 开始抓取 Amazon Best Sellers 所有分类...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=500)
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

        # 访问 Best Sellers 首页
        print(f"[INFO] 访问 Amazon Best Sellers 首页...")
        page.goto("https://www.amazon.com/gp/bestsellers", timeout=60000)

        # 等待页面加载
        page.wait_for_timeout(random_wait(10000, 15000))

        # 滚动页面
        print(f"[INFO] 滚动页面加载更多内容...")
        for i in range(5):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(random_wait(3000, 5000))

        # 提取分类
        categories = extract_categories(page)

        if not categories:
            print(f"[ERROR] 没有提取到任何分类!")
            browser.close()
            return

        # 保存分类列表
        categories_file = Path(__file__).parent.parent / "screenshots" / "amazon_categories.json"
        categories_file.parent.mkdir(parents=True, exist_ok=True)
        with open(categories_file, "w", encoding="utf-8") as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)
        print(f"[OK] 分类列表已保存到:{categories_file}")

        # 抓取每个分类(复用同一个 page 和 browser)
        # 抓取所有分类
        print(f"[INFO] 开始抓取 {len(categories)} 个分类")
        for i, category in enumerate(categories):
            fetch_and_save_category(category, page, pages)
            if i < len(categories) - 1:
                wait_ms = random_wait(10000, 20000)
                print(f"\n[INFO] 等待 {wait_ms}ms 后开始下一个分类...")
                import time
                time.sleep(wait_ms / 1000)

        browser.close()

    print(f"\n[OK] 所有分类抓取完成!")


if __name__ == "__main__":
    fetch_all_categories()
