#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查商品数据提取
"""

from playwright.sync_api import sync_playwright

def check_product_extraction():
    print("[INFO] 连接到 Chrome...")
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        print(f"[OK] 连接成功！")
        
        context = browser.contexts[0]
        
        # 找到 TikTok 页面
        tiktok_page = None
        for page in context.pages:
            if "tiktok.com" in page.url or "shop.tiktok.com" in page.url:
                tiktok_page = page
                break
        
        if not tiktok_page:
            print("[ERROR] 没有找到 TikTok 页面")
            return
        
        print(f"[INFO] 当前页面: {tiktok_page.url}")
        
        # 检查商品链接格式
        product_links_js = """
            () => {
                const links = Array.from(document.querySelectorAll('a'));
                const productLinks = links.filter(l => l.href && l.href.includes('/pdp/'));
                return productLinks.slice(0, 10).map(l => ({
                    href: l.href,
                    text: (l.innerText || l.textContent || '').trim().substring(0, 50)
                }));
            }
        """
        
        product_links = tiktok_page.evaluate(product_links_js)
        print(f"\n[INFO] 找到 {len(product_links)} 个商品链接（前 10 个）:")
        for i, link in enumerate(product_links):
            print(f"  [{i}] {link['text']} -> {link['href']}")
        
        # 检查价格元素
        price_js = """
            () => {
                const priceElements = Array.from(document.querySelectorAll('*')).filter(el => {
                    const text = el.innerText || el.textContent || '';
                    return text.includes('$') && /\\$\\d+\\.\\d+/.test(text);
                });
                return priceElements.slice(0, 10).map(el => el.innerText.trim());
            }
        """
        
        prices = tiktok_page.evaluate(price_js)
        print(f"\n[INFO] 找到 {len(prices)} 个价格元素（前 10 个）:")
        for i, price in enumerate(prices):
            print(f"  [{i}] {price}")
        
        # 检查商品名称
        name_js = """
            () => {
                const nameElements = Array.from(document.querySelectorAll('h3'));
                return nameElements.slice(0, 10).map(el => el.innerText.trim().substring(0, 50));
            }
        """
        
        names = tiktok_page.evaluate(name_js)
        print(f"\n[INFO] 找到 {len(names)} 个商品名称（前 10 个）:")
        for i, name in enumerate(names):
            print(f"  [{i}] {name}")

if __name__ == "__main__":
    check_product_extraction()