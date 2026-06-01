#!/usr/bin/env python3
"""手动提取 TikTok 类目 - 使用已打开的浏览器"""
from playwright.sync_api import sync_playwright
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CATEGORIES_DB = DATA_DIR / "categories.db"

print("[INFO] 连接到 Chrome...")
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    context = browser.contexts[0]
    
    # 找到或创建 TikTok 页面
    page = None
    for pg in context.pages:
        if 'tiktok' in pg.url.lower():
            page = pg
            break
    
    if not page:
        page = context.new_page()
    
    print(f"[INFO] 当前页面: {page.url}")
    
    # 如果不在 TikTok Shop 页面，导航过去
    if 'tiktok.com/shop' not in page.url:
        print("[INFO] 导航到 TikTok Shop...")
        page.goto("https://www.tiktok.com/shop", timeout=60000)
        page.wait_for_timeout(10000)
    
    # 滚动
    print("[INFO] 滚动页面...")
    for i in range(3):
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        page.wait_for_timeout(2000)
    
    # 提取类目 - 从侧边栏类目列表
    print("[INFO] 提取类目...")
    
    # 方法1: 找类目名称对应的链接
    category_names = [
        "美妆个护", "女装与女士内衣", "男装与男士内衣", "手机与数码",
        "时尚配件", "收藏品", "家居用品", "厨房用品", "鞋靴",
        "运动与户外", "箱包", "玩具和爱好", "汽车与摩托车", "儿童时尚",
        "电脑办公", "母婴用品", "五金工具", "家纺布艺", "宠物用品",
        "家装建材", "食品饮料", "穆斯林时尚", "图书、杂志和音频",
        "家电", "保健", "家具", "珠宝与衍生品", "二手"
    ]
    
    categories = []
    
    # 尝试从页面提取链接
    all_links = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a')).map(a => ({
            href: a.href,
            text: a.textContent.trim()
        }));
    }''')
    
    print(f"[INFO] 页面共有 {len(all_links)} 个链接")
    
    # 匹配类目名称和链接
    for name in category_names:
        for link in all_links:
            if link['text'] == name and '/c/' in link['href']:
                categories.append({'name': name, 'url': link['href']})
                print(f"  找到: {name}")
                break
    
    print(f"\n[OK] 共找到 {len(categories)} 个类目")
    
    # 保存到数据库
    if categories:
        conn = sqlite3.connect(CATEGORIES_DB)
        cursor = conn.cursor()
        
        saved = 0
        for cat in categories:
            try:
                cursor.execute(
                    'INSERT OR IGNORE INTO categories (platform, name, url) VALUES (?, ?, ?)',
                    ('tiktok', cat['name'], cat['url'])
                )
                if cursor.rowcount > 0:
                    saved += 1
            except Exception as e:
                print(f"  [ERROR] {cat['name']}: {e}")
        
        conn.commit()
        conn.close()
        print(f"[OK] 保存了 {saved} 个新类目到数据库")
    
    print("\n完成！")
