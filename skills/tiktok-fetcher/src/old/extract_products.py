from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://www.tiktok.com/shop/c/beauty-personal-care/601450', wait_until='networkidle')
    page.wait_for_timeout(10000)
    
    # 提取商品卡片信息
    products = page.evaluate('''() => {
        // 查找所有商品链接
        const productLinks = Array.from(document.querySelectorAll('a[href*="/shop/pdp/"]'));
        
        return productLinks.slice(0, 20).map(link => {
            // 获取父元素
            const parent = link.parentElement;
            
            // 查找价格（尝试多种模式）
            let price = null;
            const priceSelectors = [
                '[class*="price"]',
                '[class*="cost"]',
                '[class*="amount"]',
                'span[class*="price"]',
                'div[class*="price"]'
            ];
            
            for (const selector of priceSelectors) {
                const priceEl = link.closest('[class*="product"]')?.querySelector(selector) || 
                               parent?.querySelector(selector);
                if (priceEl) {
                    price = priceEl.textContent.trim();
                    break;
                }
            }
            
            // 查找评分
            let rating = null;
            const ratingEl = link.closest('[class*="product"]')?.querySelector('[class*="rating"]') ||
                            parent?.querySelector('[class*="rating"]');
            if (ratingEl) {
                rating = ratingEl.textContent.trim();
            }
            
            // 查找销量
            let sold = null;
            const soldEl = link.closest('[class*="product"]')?.querySelector('[class*="sold"]') ||
                          parent?.querySelector('[class*="sold"]');
            if (soldEl) {
                sold = soldEl.textContent.trim();
            }
            
            return {
                href: link.getAttribute('href'),
                name: link.textContent.trim().substring(0, 200),
                price: price,
                rating: rating,
                sold: sold,
                parentClass: parent?.className?.substring(0, 100),
                parentTag: parent?.tagName
            };
        });
    }''')
    
    print(f'找到 {len(products)} 个商品')
    # 只打印前 5 个，避免编码问题
    for i, prod in enumerate(products[:5]):
        print(f'\n{i+1}. {prod["name"]}')
        print(f'   URL: {prod["href"]}')
        print(f'   Price: {prod["price"]}')
        print(f'   Rating: {prod["rating"]}')
        print(f'   Sold: {prod["sold"]}')
        print(f'   Parent: {prod["parentTag"]} ({prod["parentClass"][:50]})')
    
    browser.close()
