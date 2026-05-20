#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试连接到已打开的 Chrome 实例
使用 CDP (Chrome DevTools Protocol) 连接
"""

from playwright.sync_api import sync_playwright

def test_connect_to_existing_chrome():
    print("[INFO] 尝试连接到已打开的 Chrome (端口 9222)...")
    
    with sync_playwright() as p:
        # 连接到已运行的 Chrome
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        
        print(f"[OK] 连接成功！")
        print(f"[INFO] 浏览器版本: {browser.version}")
        
        # 获取所有上下文（Context）
        contexts = browser.contexts
        print(f"[INFO] 找到 {len(contexts)} 个上下文")
        
        # 获取所有页面
        for i, context in enumerate(contexts):
            pages = context.pages
            print(f"[INFO] 上下文 {i}: {len(pages)} 个页面")
            
            for j, page in enumerate(pages):
                print(f"  - 页面 {j}: {page.url}")
        
        # 如果有页面，尝试操作
        if contexts and contexts[0].pages:
            page = contexts[0].pages[0]
            print(f"\n[INFO] 当前页面: {page.url}")
            print(f"[INFO] 页面标题: {page.title()}")
            
            # 测试：获取页面内容
            content = page.content()
            print(f"[INFO] 页面内容长度: {len(content)} 字符")
            
            # 测试：执行 JavaScript
            result = page.evaluate("() => document.title")
            print(f"[INFO] JavaScript 执行结果: {result}")
            
            # 测试：打开新页面
            print(f"\n[INFO] 测试打开新页面...")
            new_page = contexts[0].new_page()
            new_page.goto("https://www.tiktok.com/shop")
            print(f"[OK] 新页面已打开: {new_page.url}")
            
            # 等待一下
            new_page.wait_for_timeout(3000)
            
            # 关闭新页面
            new_page.close()
            print(f"[OK] 新页面已关闭")
        else:
            print(f"[WARN] 没有找到任何页面")
        
        # 注意：不要关闭 browser，因为它是外部启动的
        # browser.close()  # 不调用这个
        
    print(f"\n[OK] 测试完成！")

if __name__ == "__main__":
    test_connect_to_existing_chrome()
