from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://www.tiktok.com/shop/c/beauty-personal-care/601450', wait_until='networkidle')
    page.wait_for_timeout(10000)
    
    # 提取第一个商品卡片的完整 HTML
    productHTML = page.evaluate('''() => {
        const link = document.querySelector('a[href*="/shop/pdp/"]');
        if (!link) return null;
        
        const parent = link.parentElement;
        const card = parent.closest('[class*="product"]') || parent;
        
        return {
            link: {
                href: link.getAttribute('href'),
                text: link.textContent?.trim(),
                className: link.className
            },
            parent: {
                tag: parent.tagName,
                className: parent.className,
                html: parent.outerHTML.substring(0, 2000)
            },
            card: {
                tag: card.tagName,
                className: card.className,
                html: card.outerHTML.substring(0, 3000)
            },
            // 查找所有子元素
            children: Array.from(card.querySelectorAll('*')).slice(0, 20).map(el => ({
                tag: el.tagName,
                className: el.className?.substring(0, 100),
                text: el.textContent?.trim().substring(0, 50),
                href: el.getAttribute('href')
            }))
        };
    }''')
    
    print('商品卡片结构:')
    print(f'链接：{productHTML["link"]["href"]}')
    print(f'链接文本：{productHTML["link"]["text"]}')
    print(f'\n父元素：{productHTML["parent"]["tag"]} ({productHTML["parent"]["className"]})')
    print(f'\n卡片 HTML 片段:')
    print(productHTML["parent"]["html"])
    
    print(f'\n\n子元素:')
    for i, child in enumerate(productHTML["children"]):
        print(f'{i+1}. [{child["tag"]}] {child["className"][:50]}')
        if child["text"]:
            print(f'   Text: {child["text"]}')
        if child["href"]:
            print(f'   Href: {child["href"]}')
    
    browser.close()
