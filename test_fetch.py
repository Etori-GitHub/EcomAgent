#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试脚本 - 诊断 Playwright 输出问题"""

import sys
import random
from pathlib import Path
from datetime import datetime

# 不重定向 stdout/stderr
print(f"[{datetime.now()}] 开始测试...", flush=True)

from playwright.sync_api import sync_playwright

print(f"[{datetime.now()}] Playwright 导入成功", flush=True)

def test_fetch():
    with sync_playwright() as p:
        print(f"[{datetime.now()}] 启动浏览器...", flush=True)
        browser = p.chromium.launch(headless=True, slow_mo=500)
        
        print(f"[{datetime.now()}] 创建页面...", flush=True)
        page = browser.new_page()
        
        # 模拟真实用户
        page.add_init_script("""
            () => {
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                navigator.languages = ['en-US', 'en'];
                navigator.plugins = [1, 2, 3, 4, 5];
            }
        """)
        
        page.set_viewport_size({"width": 1920, "height": 5000})
        
        # 访问 Best Sellers 首页
        print(f"[{datetime.now()}] 访问 Amazon Best Sellers...", flush=True)
        page.goto("https://www.amazon.com/gp/bestsellers", timeout=60000)
        
        print(f"[{datetime.now()}] 等待页面加载...", flush=True)
        wait_ms = random.randint(5000, 10000)
        page.wait_for_timeout(wait_ms)
        
        print(f"[{datetime.now()}] 获取页面标题...", flush=True)
        title = page.title()
        print(f"[{datetime.now()}] 页面标题: {title}", flush=True)
        
        # 提取分类
        print(f"[{datetime.now()}] 提取分类列表...", flush=True)
        category_js = """
            () => {
                const categories = [];
                const navTree = document.querySelector('div[role="group"][aria-label="Navigation Tree"]');
                if (!navTree) return [];
                const ul = navTree.querySelector('ul._p13n-zg-nav-tree-all_style_zg-browse-group__88fbz');
                if (!ul) return [];
                const lis = ul.querySelectorAll('li');
                lis.forEach((li) => {
                    const link = li.querySelector('a');
                    if (link) {
                        const href = link.getAttribute('href') || '';
                        const text = link.innerText.trim();
                        const slugMatch = href.match(/\\/zgbs\\/([^\\/]+)/);
                        const slug = slugMatch ? slugMatch[1] : '';
                        const fullUrl = href.startsWith('http') ? href : 'https://www.amazon.com' + href;
                        categories.push({ name: text, url: fullUrl, slug: slug });
                    }
                });
                return categories;
            }
        """
        
        categories = page.evaluate(category_js)
        print(f"[{datetime.now()}] 找到 {len(categories)} 个分类", flush=True)
        
        # 打印前5个分类
        for i, cat in enumerate(categories[:5]):
            print(f"  [{i}] {cat['name']} -> {cat['slug']}", flush=True)
        
        browser.close()
        
    print(f"[{datetime.now()}] 测试完成!", flush=True)
    return categories

if __name__ == "__main__":
    test_fetch()
