#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok Shop 抓取 - 第一步：测试首页加载
"""

import random
from playwright.sync_api import sync_playwright


def random_wait(min_ms=1000, max_ms=3000):
    """随机等待，避免被反爬"""
    wait_ms = random.randint(min_ms, max_ms)
    print(f"[INFO] 等待 {wait_ms}ms 避免反爬...")
    return wait_ms


def test_homepage():
    """测试首页加载"""
    
    with sync_playwright() as p:
        # 连接到已运行的 Chrome 实例
        # 首先需要启动一个带远程调试端口的 Chrome
        # 或者使用已有的调试端口
        
        # 方案 1：连接到已有的 Chrome 调试端口（如果已启动）
        # 方案 2：启动新的 Chrome 实例，但使用你的用户数据目录
        
        user_data_dir = r"C:\Users\Etroi\AppData\Local\Google\Chrome\User Data\Profile 1"
        
        print(f"[INFO] 使用 Chrome 配置文件：{user_data_dir}")
        print(f"[INFO] 启动 persistent context（会复用你的登录状态）...")
        
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            slow_mo=500,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--allow-running-insecure-content',
                '--remote-debugging-port=9222'
            ]
        )
        page = browser.new_page()
        
        # 模拟真实用户
        page.add_init_script("""
            () => {
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                navigator.languages = ['en-US', 'en'];
                navigator.plugins = [1, 2, 3, 4, 5];
            }
        """)
        
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        print(f"[INFO] 访问 TikTok Shop 首页...")
        page.goto("https://www.tiktok.com/shop", timeout=120000)
        
        # 等待初始加载
        print(f"[INFO] 等待初始加载...")
        page.wait_for_selector('body', timeout=60000)
        page.wait_for_timeout(random_wait(10000, 15000))
        
        # 滚动页面加载更多内容
        print(f"[INFO] 开始滚动页面...")
        for i in range(5):
            print(f"[INFO] 滚动 {i+1}/5...")
            try:
                page.evaluate("""
                    () => {
                        if (document.body) {
                            window.scrollTo(0, document.body.scrollHeight);
                        }
                    }
                """)
            except Exception as e:
                print(f"[WARN] 滚动失败：{e}")
            page.wait_for_timeout(random_wait(3000, 5000))
        
        # 最终等待
        print(f"[INFO] 等待最终加载...")
        page.wait_for_timeout(random_wait(10000, 20000))
        
        # 保存页面截图
        page.screenshot(path="C:\\Users\\Etroi\\.openclaw\\workspace\\code\\EcomAgent\\skills\\tiktok-fetcher\\screenshots\\homepage.png")
        print(f"[OK] 截图已保存到：C:\\Users\\Etroi\\.openclaw\\workspace\\code\\EcomAgent\\skills\\tiktok-fetcher\\screenshots\\homepage.png")
        
        # 提取类目信息
        category_js = """
            () => {
                const categories = [];
                
                // 查找类目标题
                const categoryHeader = document.querySelector('h2.mb-20.H2-Bold');
                console.log('=== 类目标题:', categoryHeader ? '找到' : '未找到');
                
                if (categoryHeader) {
                    // 查找标题下面的所有类目 div
                    const parent = categoryHeader.parentElement;
                    const allDivs = parent ? parent.querySelectorAll('div') : [];
                    
                    console.log('=== 标题下面的 div 数:', allDivs.length);
                    
                    // 查找包含 title 属性的类目 div
                    allDivs.forEach((div, idx) => {
                        const title = div.getAttribute('title');
                        const className = div.className;
                        const href = div.querySelector('a') ? div.querySelector('a').href : null;
                        
                        if (title && className.includes('cursor-pointer')) {
                            categories.push({
                                name: title,
                                url: href,
                                className: className.substring(0, 100)
                            });
                            console.log('[' + idx + '] ' + title + ' -> ' + href);
                        }
                    });
                }
                
                return categories;
            }
        """
        
        categories = page.evaluate(category_js)
        print(f"\n[INFO] 找到 {len(categories)} 个类目")
        
        # 保存类目列表
        import json
        with open("C:\\Users\\Etroi\\.openclaw\\workspace\\code\\EcomAgent\\skills\\tiktok-fetcher\\screenshots\\categories.json", "w", encoding="utf-8") as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)
        print(f"[OK] 类目列表已保存到：C:\\Users\\Etroi\\.openclaw\\workspace\\code\\EcomAgent\\skills\\tiktok-fetcher\\screenshots\\categories.json")
        
        # 打印前 10 个类目
        if categories:
            print(f"\n[示例] 前 10 个类目:")
            for i, cat in enumerate(categories[:10]):
                print(f"  {i+1}. {cat['name']} -> {cat['url']}")
        
        # 保持浏览器打开，等待用户检查
        print(f"\n[INFO] 页面加载完成！请检查截图、HTML 和类目列表。")
        print(f"[INFO] 如果类目列表正确，我们将进入下一步：抓取分类页面数据。")
        
        # 保存页面 HTML
        html = page.content()
        with open("C:\\Users\\Etroi\\.openclaw\\workspace\\code\\EcomAgent\\skills\\tiktok-fetcher\\screenshots\\homepage.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[OK] HTML 已保存到：C:\\Users\\Etroi\\.openclaw\\workspace\\code\\EcomAgent\\skills\\tiktok-fetcher\\screenshots\\homepage.html")
        
        print(f"\n[INFO] 页面加载完成！请检查截图和 HTML 文件。")
        print(f"[INFO] 如果看到分类列表，请告诉我分类 URL 的格式。")
        
        # 保持浏览器打开，等待用户检查
        print(f"\n[INFO] 浏览器已打开，按 Ctrl+C 关闭...")
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        
        browser.close()


if __name__ == "__main__":
    test_homepage()
