#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证 Amazon 页面结构
"""

from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        page.set_viewport_size({'width': 1920, 'height': 1080})
        
        print("[INFO] 访问 Amazon 主页面...")
        page.goto('https://www.amazon.com/gp/bestsellers/', timeout=60000)
        page.wait_for_timeout(10000)
        
        nav_js = """
        () => {
            const result = {
                found: false,
                parent: null,
                ul: null,
                links: []
            };
            
            const parent = document.querySelector('[data-card-metrics-id="p13n-zg-nav-tree-all_zeitgeist-lists_1"]');
            if (parent) {
                result.found = true;
                result.parent = {
                    id: parent.id,
                    class: parent.className,
                    role: parent.getAttribute('role')
                };
                
                const ul = parent.querySelector('ul.a-unordered-list.a-nostyle.a-vertical');
                if (ul) {
                    result.ul = { class: ul.className };
                    
                    const links = ul.querySelectorAll('a[href*="/Best-Sellers-"][href*="/zgbs/"]');
                    result.links = Array.from(links).map(link => ({
                        text: link.innerText.trim(),
                        href: link.getAttribute('href'),
                        full_url: 'https://www.amazon.com' + link.getAttribute('href')
                    }));
                }
            }
            
            return result;
        }
        """
        
        result = page.evaluate(nav_js)
        
        print('\n=== 页面结构确认 ===')
        print(f'找到导航树元素：{result["found"]}')
        
        if result['parent']:
            print(f'父元素 ID: {result["parent"]["id"]}')
            print(f'父元素 Class: {result["parent"]["class"]}')
        
        if result['ul']:
            print(f'列表 Class: {result["ul"]["class"]}')
        
        if result['links']:
            print(f'\n找到 {len(result["links"])} 个分类链接:')
            for i, link in enumerate(result['links'][:15]):
                print(f'  {i+1}. {link["text"]}')
                print(f'     URL: {link["href"]}')
        
        browser.close()

if __name__ == "__main__":
    main()
