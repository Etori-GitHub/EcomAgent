#!/usr/bin/env python3
"""检查 TikTok 页面链接"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    context = browser.contexts[0]
    
    for page in context.pages:
        if 'tiktok' in page.url.lower():
            print(f'[OK] 页面: {page.url}')
            
            # 滚动
            for i in range(3):
                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                page.wait_for_timeout(2000)
            
            # 检查页面上的所有链接
            links = page.evaluate('''() => {
                const allLinks = Array.from(document.querySelectorAll('a'));
                return allLinks.map(link => ({
                    href: link.href,
                    text: link.textContent.trim().substring(0, 50)
                })).filter(l => l.text && l.text.length > 2);
            }''')
            
            print(f'\n找到 {len(links)} 个链接')
            
            # 找包含 /c/ 的链接
            cat_links = [l for l in links if '/c/' in l['href']]
            print(f'\n包含 /c/ 的链接: {len(cat_links)} 个')
            for l in cat_links[:20]:
                print(f'  {l["text"]} -> {l["href"]}')
            
            # 找包含 shop.tiktok 的链接
            shop_links = [l for l in links if 'shop.tiktok' in l['href'] and 'pdp' not in l['href']]
            print(f'\n包含 shop.tiktok 的链接: {len(shop_links)} 个')
            for l in shop_links[:20]:
                print(f'  {l["text"]} -> {l["href"]}')
            
            # 直接从类目文本提取
            categories_text = page.evaluate('''() => {
                const catElements = Array.from(document.querySelectorAll('*'));
                const categories = [];
                catElements.forEach(el => {
                    const text = el.textContent.trim();
                    if (text === '美妆个护' || text === '女装与女士内衣' || text === '男装与男士内衣') {
                        // 找到类目元素
                    }
                });
                return categories;
            }''')
            
            break
