#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试脚本：检查 Amazon Best Sellers 页面结构
"""

import sys
import io
from pathlib import Path

# Windows UTF-8 兼容
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright

def debug_page_structure(page):
    """检查页面结构，找出名称元素的正确选择器"""
    
    # 等待页面加载
    page.wait_for_selector('li.zg-no-numbers, div#gridItemRoot', timeout=10000)
    
    # 检查商品行结构
    debug_js = """
        () => {
            const results = [];
            
            // 找到第一个商品行
            const row = document.querySelector('li.zg-no-numbers, div#gridItemRoot > div');
            
            if (!row) {
                return { error: '找不到商品行' };
            }
            
            // 打印整个行的 HTML（简化版）
            const rowHtml = row.innerHTML.substring(0, 500);
            
            // 尝试各种方式提取名称
            const methods = {};
            
            // 方法1: 链接文字
            const link = row.querySelector('a.a-link-normal[href*="/dp/"]');
            methods['link_text'] = link?.innerText?.trim() || '(empty)';
            
            // 方法2: 图片 alt
            const img = row.querySelector('img');
            methods['img_alt'] = img?.alt || '(empty)';
            
            // 方法3: 图片 title
            methods['img_title'] = img?.title || '(empty)';
            
            // 方法4: 所有带文字的元素
            const textElements = [];
            row.querySelectorAll('span, div, a').forEach(el => {
                const text = el.innerText?.trim();
                if (text && text.length > 5 && text.length < 200) {
                    textElements.push({
                        tag: el.tagName,
                        class: el.className?.substring(0, 50),
                        text: text.substring(0, 50)
                    });
                }
            });
            methods['text_elements'] = textElements;
            
            // 方法5: 检查是否有专门的名称容器
            const nameContainers = [
                'div._cDEzb_p13n-sc-css-line-clamp-3_g3dy1',
                'div[class*="p13n-sc-truncate"]',
                'div[class*="line-clamp"]',
                'span.a-size-base-plus',
                'div.zg-item-title',
                'a.a-link-normal[href*="/dp/"]'
            ];
            
            const foundContainers = {};
            nameContainers.forEach(selector => {
                const el = row.querySelector(selector);
                if (el) {
                    foundContainers[selector] = {
                        text: el.innerText?.trim()?.substring(0, 50) || '(empty)',
                        html: el.outerHTML?.substring(0, 100) || '(no html)'
                    };
                }
            });
            methods['name_containers'] = foundContainers;
            
            return methods;
        }
    """
    
    result = page.evaluate(debug_js)
    return result

def main():
    print("=== Amazon Best Sellers 页面结构调试 ===")
    
    with sync_playwright() as p:
        # 使用持久化上下文（复用登录状态）
        user_data_dir = Path.home() / ".openclaw" / "chrome-profile-amazon"
        user_data_dir.mkdir(parents=True, exist_ok=True)
        
        context = p.chromium.launch_persistent_context(
            str(user_data_dir),
            headless=False,  # 显示浏览器方便调试
            viewport={"width": 1280, "height": 800}
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        
        # 打开 Electronics Best Sellers
        url = "https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics"
        print(f"\n打开页面: {url}")
        page.goto(url, timeout=30000)
        
        # 调试页面结构
        print("\n检查第一个商品的结构...")
        result = debug_page_structure(page)
        
        print("\n=== 调试结果 ===")
        if 'error' in result:
            print(f"错误: {result['error']}")
        else:
            print(f"\n方法1 (link_text): {result['link_text']}")
            print(f"\n方法2 (img_alt): {result['img_alt']}")
            print(f"\n方法3 (img_title): {result['img_title']}")
            
            print(f"\n方法4 (text_elements):")
            for el in result.get('text_elements', []):
                print(f"  {el['tag']}.{el['class']}: {el['text']}")
            
            print(f"\n方法5 (name_containers):")
            for selector, info in result.get('name_containers', {}).items():
                print(f"  {selector}:")
                print(f"    text: {info['text']}")
                print(f"    html: {info['html']}")
        
        # 保持浏览器打开，方便手动检查
        print("\n浏览器保持打开，按 Ctrl+C 关闭...")
        try:
            input()
        except KeyboardInterrupt:
            pass
        
        context.close()

if __name__ == "__main__":
    main()