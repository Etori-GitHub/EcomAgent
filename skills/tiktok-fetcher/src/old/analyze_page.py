from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # 显示浏览器窗口
    page = browser.new_page()
    page.goto('https://www.tiktok.com/shop/c/beauty-personal-care/601450', wait_until='networkidle')
    # 额外等待 15 秒让商品加载
    page.wait_for_timeout(15000)
    
    # 截图
    page.screenshot(path='beauty_category.png', full_page=True)
    print('截图已保存：beauty_category.png')
    
    # 获取完整 HTML
    html = page.content()
    with open('category_page.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('HTML 已保存：category_page.html')
    
    # 等待用户按键继续
    print('\n浏览器已打开，请查看页面...')
    print('HTML 已保存到 category_page.html')
    print('按 Enter 键继续分析...')
    input()
    
    # 使用 JavaScript 获取所有商品卡片
    products = page.evaluate('''() => {
        // 查找所有链接，找包含 /product/ 的
        const productLinks = Array.from(document.querySelectorAll('a[href*="/product/"]'));
        console.log(`Found ${productLinks.length} product links`);
        
        if (productLinks.length > 0) {
            return productLinks.slice(0, 5).map(link => ({
                href: link.getAttribute('href'),
                text: link.textContent?.trim().substring(0, 100),
                parentTag: link.parentElement?.tagName,
                parentClass: link.parentElement?.className?.substring(0, 100)
            }));
        }
        
        // 返回所有包含价格的元素
        const priceElements = Array.from(document.querySelectorAll('*'))
            .filter(el => {
                const text = el.textContent?.toLowerCase() || '';
                return text.includes('$') || text.includes('¥') || text.includes('元');
            });
        
        console.log(`Found ${priceElements.length} elements with prices`);
        
        return priceElements.slice(0, 5).map(el => ({
            tag: el.tagName,
            className: el.className?.substring(0, 100),
            text: el.textContent?.trim().substring(0, 50)
        }));
    }''')
    
    print(f'页面标题：{page.title()}')
    print(f'\n商品元素分析:')
    for i, prod in enumerate(products):
        print(f'{i+1}. {prod}')
    
    # 尝试找到商品卡片
    productCards = page.evaluate('''() => {
        // 尝试多种选择器
        const selectors = [
            'a[href*="/product/"]',
            '[class*="product"]',
            '[class*="item"]'
        ];
        
        for (const selector of selectors) {
            const elements = document.querySelectorAll(selector);
            if (elements.length > 0) {
                console.log(`Found ${elements.length} elements with selector: ${selector}`);
                return elements.slice(0, 3).map(el => ({
                    tag: el.tagName,
                    className: el.className,
                    href: el.getAttribute('href'),
                    text: el.textContent?.trim().substring(0, 200),
                    children: Array.from(el.children).map(c => ({
                        tag: c.tagName,
                        className: c.className?.substring(0, 100)
                    }))
                }));
            }
        }
        
        return [];
    }''')
    
    print(f'\n商品卡片分析:')
    for i, card in enumerate(productCards):
        print(f'{i+1}. {card}')
    
    input('\n按 Enter 键关闭浏览器...')
    browser.close()
    
    browser.close()
