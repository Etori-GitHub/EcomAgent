#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok Shop 热销榜单抓取脚本 - undetected-chromedriver 版本
专门绑过反爬检测，效果最强

功能：
1. 使用 undetected_chromedriver 绑过反爬
2. 模拟真实用户行为
3. 从首页提取类目列表
4. 提取商品数据并保存到 JSON 文件

依赖：pip install undetected-chromedriver
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

# 检查依赖
try:
    import undetected_chromedriver as uc
    HAS_UC = True
    print("[OK] undetected-chromedriver 已加载")
except ImportError:
    HAS_UC = False
    print("[ERROR] undetected-chromedriver 未安装！")
    print("[ERROR] 安装命令: pip install undetected-chromedriver")
    sys.exit(1)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def random_wait(min_ms=1000, max_ms=3000):
    """随机等待"""
    wait_ms = random.randint(min_ms, max_ms)
    print(f"[INFO] 等待 {wait_ms}ms...")
    time.sleep(wait_ms / 1000)
    return wait_ms


def human_like_scroll(driver):
    """模拟人类滚动"""
    for _ in range(random.randint(3, 6)):
        scroll_amount = random.randint(300, 800)
        driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
        time.sleep(random.uniform(0.5, 1.5))


def extract_categories(driver):
    """提取类目列表"""
    print(f"\n[INFO] 正在提取类目列表...")
    
    categories = []
    links = driver.find_elements(By.TAG_NAME, "a")
    
    for link in links:
        try:
            href = link.get_attribute("href")
            text = link.text.strip()
            
            if href and text:
                is_category = (
                    'shop.tiktok.com' in href and '/c/' in href
                ) or '/shop/c/' in href
                
                if is_category and 0 < len(text) < 50:
                    categories.append({
                        'name': text,
                        'url': href
                    })
        except:
            continue
    
    # 去重
    seen = set()
    unique = []
    for cat in categories:
        if cat['url'] not in seen:
            seen.add(cat['url'])
            unique.append(cat)
    
    print(f"[OK] 找到 {len(unique)} 个类目")
    return unique


def fetch_category_products(driver, category_name):
    """抓取商品数据"""
    random_wait(8000, 15000)
    
    # 滚动加载
    print(f"[INFO] 滚动页面加载商品...")
    human_like_scroll(driver)
    
    # 点击查看更多
    try:
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for btn in buttons:
            if "查看更多" in btn.text:
                btn.click()
                random_wait(5000, 10000)
                break
    except:
        pass
    
    # 提取商品 - 使用 JavaScript
    print(f"[INFO] 正在提取商品数据...")
    
    product_js = """
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
                            const urlMatch = product_url.match(/\\/shop\\/pdp\\/[^/]+\\/(\\d+)/);
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
    """
    
    products = driver.execute_script(product_js)
    print(f"[OK] 找到 {len(products)} 个商品")
    return products if products else []


def fetch_and_save_category(category, driver):
    """抓取并保存单个分类"""
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
        driver.get(category['url'])
        random_wait(5000, 10000)
    except Exception as e:
        print(f"[ERROR] 访问页面失败：{e}")
        return None
    
    # 检查封禁
    if '{"code":100000}' in driver.page_source:
        print(f"[ERROR] 检测到封禁响应 code:100000")
        return None
    
    data = fetch_category_products(driver, category['name'])
    
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
            "method": "undetected-chromedriver"
        },
        "products": data
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(enriched_data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 分类 {category['name']} 抓取完成，共 {len(data)} 个商品")
    print(f"[OK] 数据已保存到：{output_file}")
    
    return enriched_data


def fetch_all_categories():
    """主函数 - undetected-chromedriver 版本（全新配置模式）"""
    print(f"[INFO] 开始抓取 TikTok Shop (undetected-chromedriver 全新配置版本)...")
    
    # 创建临时 Chrome 配置目录（完全干净的环境）
    temp_profile = Path.home() / ".openclaw" / "chrome-temp-profile"
    if temp_profile.exists():
        print(f"[INFO] 清理旧的临时配置...")
        import shutil
        shutil.rmtree(temp_profile, ignore_errors=True)
    temp_profile.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] 使用全新 Chrome 配置: {temp_profile}")
    
    # 创建 Chrome 实例
    print(f"[INFO] 启动 Chrome 浏览器...")
    
    options = uc.ChromeOptions()
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-infobars')
    options.add_argument(f'--user-data-dir={temp_profile}')  # 使用全新配置
    options.add_argument('--no-first-run')  # 不显示首次运行页面
    options.add_argument('--no-default-browser-check')  # 不检查默认浏览器
    options.add_argument('--disable-extensions')  # 禁用扩展
    options.add_argument('--disable-plugins')  # 禁用插件
    
    # 修改设备指纹
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--lang=en-US')
    options.add_argument('--timezone=America/New_York')
    
    # 模拟不同的 GPU 和屏幕信息
    options.add_argument('--use-gl=swiftshader')  # 使用软件渲染，改变 GPU 指纹
    options.add_argument('--disable-gpu')  # 禁用 GPU 加速
    options.add_argument('--disable-software-rasterizer')
    
    # 添加随机 User-Agent
    import random
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    ]
    options.add_argument(f'--user-agent={random.choice(user_agents)}')
    
    driver = uc.Chrome(
        options=options,
        version_main=149,  # 强制使用 Chrome 149
        use_subprocess=False
    )
    
    print(f"[OK] 浏览器已启动")
    
    # 关键：带上 Google Referer 访问 TikTok Shop
    print(f"[INFO] 访问 TikTok Shop (带 Google Referer)...")
    
    try:
        driver.get("https://shop.tiktok.com/us")
        # 注意：Selenium 不支持直接设置 referer，需要通过其他方式
        # 但我们已经知道问题所在，可以用 Playwright 版本
    except Exception as e:
        print(f"[ERROR] 访问失败：{e}")
        driver.quit()
        return
    
    # 检查封禁
    if '{"code":100000}' in driver.page_source:
        print(f"[ERROR] 检测到封禁响应 code:100000")
        print(f"[INFO] undetected-chromedriver 也无法绑过，建议：")
        print(f"  1. 换 IP（VPN/代理）")
        print(f"  2. 考虑 Android App 抓包方案")
        driver.quit()
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
    human_like_scroll(driver)
    
    # 提取类目
    categories = extract_categories(driver)
    
    if not categories:
        print(f"[ERROR] 没有提取到任何类目！")
        driver.quit()
        return
    
    # 保存类目列表
    categories_file = Path(__file__).parent.parent / "screenshots" / "categories_uc.json"
    categories_file.parent.mkdir(parents=True, exist_ok=True)
    with open(categories_file, "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)
    print(f"[OK] 类目列表已保存")
    
    # 抓取第一个类目（测试）
    test_categories = categories[:1]
    for category in test_categories:
        fetch_and_save_category(category, driver)
    
    driver.quit()
    print(f"\n[OK] 抓取完成！")


if __name__ == "__main__":
    fetch_all_categories()
