#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：提取 Amazon Best Sellers 所有分类链接
"""

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


def extract_categories():
    """从 Amazon Best Sellers 首页提取所有分类链接"""
    
    print(f"[INFO] 启动浏览器...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
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
        print(f"[INFO] 访问 Amazon Best Sellers 首页...")
        page.goto("https://www.amazon.com/gp/bestsellers", timeout=60000)
        
        # 等待页面加载
        page.wait_for_timeout(10000)
        
        # 滚动页面
        print(f"[INFO] 滚动页面加载更多内容...")
        for i in range(5):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(3000)
        
        # 提取分类链接
        print(f"[INFO] 正在提取分类链接...")
        
        category_js = """
            () => {
                const categories = [];
                
                // 策略：使用用户提供的精确选择器
                // 1. 找到 Navigation Tree 容器
                const navTree = document.querySelector('div[role="group"][aria-label="Navigation Tree"]');
                
                if (!navTree) {
                    console.log('未找到 Navigation Tree 容器');
                    return [];
                }
                
                console.log('找到 Navigation Tree 容器');
                
                // 2. 找到 ul 列表
                const ul = navTree.querySelector('ul._p13n-zg-nav-tree-all_style_zg-browse-group__88fbz');
                
                if (!ul) {
                    console.log('未找到 ul 列表，尝试其他选择器');
                    // 尝试更宽松的选择器
                    const allUls = navTree.querySelectorAll('ul');
                    console.log('找到 ' + allUls.length + ' 个 ul 元素');
                    
                    // 遍历所有 ul，找到包含分类的
                    allUls.forEach((u, idx) => {
                        const lis = u.querySelectorAll('li');
                        console.log('ul[' + idx + '] 包含 ' + lis.length + ' 个 li');
                    });
                    
                    return [];
                }
                
                console.log('找到 ul 列表');
                
                // 3. 提取所有 li 中的分类
                const lis = ul.querySelectorAll('li');
                console.log('找到 ' + lis.length + ' 个 li 元素');
                
                lis.forEach((li, idx) => {
                    const link = li.querySelector('a');
                    if (link) {
                        const href = link.getAttribute('href') || '';
                        const text = link.innerText.trim();
                        
                        // 提取分类 slug（从 href 中）
                        // 格式：/Best-Sellers-xxx/zgbs/xxx/ref=...
                        const slugMatch = href.match(/\/zgbs\/([^\/]+)/);
                        const slug = slugMatch ? slugMatch[1] : '';
                        
                        // 构建完整 URL
                        const fullUrl = href.startsWith('http') ? href : 'https://www.amazon.com' + href;
                        
                        categories.push({
                            name: text,
                            url: fullUrl,
                            slug: slug,
                            href: href
                        });
                        
                        if (idx < 10) {
                            console.log('[' + idx + '] ' + text + ' -> ' + slug);
                        }
                    }
                });
                
                return categories;
            }
        """
        
        categories = page.evaluate(category_js)
        print(f"[OK] 找到 {len(categories)} 个分类")
        
        # 打印前 20 个分类
        print("\n[分类列表] 前 20 个:")
        for i, cat in enumerate(categories[:20]):
            print(f"  {i+1}. {cat['name']} -> {cat['slug']}")
        
        # 保存到文件
        output_file = Path(__file__).parent / "amazon_categories.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)
        print(f"\n[OK] 分类列表已保存到：{output_file}")
        
        browser.close()
    
    return categories


if __name__ == "__main__":
    extract_categories()
