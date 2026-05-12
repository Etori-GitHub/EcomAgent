#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析 TikTok Shop 首页类目结构
"""

from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.set_viewport_size({'width': 1920, 'height': 1200})
    
    print('访问 TikTok Shop 首页...')
    page.goto('https://www.tiktok.com/shop', timeout=60000)
    page.wait_for_timeout(8000)
    
    # 查找类目链接
    js_code = '''
    () => {
        const results = [];
        
        // 查找所有链接
        const allLinks = document.querySelectorAll('a');
        
        allLinks.forEach((link, idx) => {
            const href = link.href;
            const text = (link.innerText || link.textContent || '').trim();
            const className = (link.className || '').substring(0, 100);
            
            // 查找包含'类目'、'Category'、'美妆'、'Beauty'等关键词的链接
            if (text && (
                text.includes('类目') || 
                text.includes('Category') ||
                text.includes('美妆') ||
                text.includes('Beauty') ||
                text.includes('个护') ||
                text.includes('Personal') ||
                href.includes('/shop/c/')
            )) {
                results.push({
                    index: idx,
                    href: href,
                    text: text,
                    className: className,
                    tag: link.tagName
                });
            }
        });
        
        return results;
    }
    '''
    
    results = page.evaluate(js_code)
    
    print(f'\n找到 {len(results)} 个相关链接:')
    for item in results[:30]:
        print(f"  [{item['index']}] {item['text'][:50]}")
        print(f"      -> {item['href']}")
        print(f"      Class: {item['className'][:80]}")
        print()
    
    browser.close()
