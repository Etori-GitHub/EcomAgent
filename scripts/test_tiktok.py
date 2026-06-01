#!/usr/bin/env python3
"""快速测试 TikTok 类目提取"""
import sqlite3
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CATEGORIES_DB = DATA_DIR / "categories.db"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    context = browser.contexts[0]
    
    # 找到已打开的 TikTok 页面
    for page in context.pages:
        print(f'[INFO] 页面: {page.url}')
        if 'tiktok' in page.url.lower():
            print('[OK] 找到 TikTok 页面')
            page.wait_for_timeout(3000)
            
            # 滚动
            for i in range(3):
                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                page.wait_for_timeout(2000)
                print(f'[INFO] 滚动 {i+1}/3')
            
            # 提取类目
            cats = page.evaluate('''() => {
                const categories = [];
                const allLinks = Array.from(document.querySelectorAll('a'));
                allLinks.forEach(link => {
                    const href = link.href;
                    const name = link.textContent.trim();
                    if (href && name && href.includes('/c/') && !href.includes('/deals/')) {
                        categories.push({ name, url: href });
                    }
                });
                const seen = new Set();
                return categories.filter(c => {
                    if (seen.has(c.name)) return false;
                    seen.add(c.name);
                    return true;
                });
            }''')
            
            print(f'[OK] 找到 {len(cats)} 个类目')
            
            # 保存到数据库
            conn = sqlite3.connect(CATEGORIES_DB)
            cursor = conn.cursor()
            
            saved = 0
            for c in cats:
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO categories (platform, name, url)
                        VALUES (?, ?, ?)
                    ''', ('tiktok', c['name'], c['url']))
                    if cursor.rowcount > 0:
                        saved += 1
                        print(f'  + {c["name"]}')
                except Exception as e:
                    print(f'  [ERROR] {c["name"]}: {e}')
            
            conn.commit()
            conn.close()
            print(f'[OK] 保存了 {saved} 个新类目')
            break
    else:
        print('[ERROR] 没找到 TikTok 页面')
