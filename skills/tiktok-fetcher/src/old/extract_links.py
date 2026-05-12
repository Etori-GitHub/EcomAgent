from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://www.tiktok.com/shop/c/beauty-personal-care/601450', wait_until='networkidle')
    page.wait_for_timeout(10000)
    
    # 提取所有链接
    all_links = page.evaluate('''() => {
        const links = Array.from(document.querySelectorAll('a[href]'));
        return links.map(l => ({
            href: l.getAttribute('href'),
            text: l.textContent?.trim().substring(0, 100),
            className: l.className?.substring(0, 100)
        }));
    }''')
    
    print(f'找到 {len(all_links)} 个链接')
    
    # 筛选出包含 /shop/ 的
    shop_links = [l for l in all_links if l['href'] and '/shop/' in l['href']]
    print(f'\n找到 {len(shop_links)} 个 shop 链接')
    
    # 打印前 30 个
    for i, link in enumerate(shop_links[:30]):
        print(f'{i+1}. {link}')
    
    browser.close()
