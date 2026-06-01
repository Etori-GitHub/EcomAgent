#!/usr/bin/env python3
"""检查 TikTok 页面 - 不自动关闭浏览器"""
from playwright.sync_api import sync_playwright
import time

print("[INFO] 启动浏览器...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    print("[INFO] 打开 TikTok Shop...")
    page.goto("https://www.tiktok.com/shop", timeout=120000)
    
    print("[INFO] 等待页面加载...如果有验证码请手动完成")
    print("[INFO] 浏览器将保持打开，按 Ctrl+C 退出")
    
    # 无限等待，让用户处理验证
    while True:
        time.sleep(10)
        try:
            links = page.evaluate('''() => {
                return Array.from(document.querySelectorAll('a')).map(a => ({
                    href: a.href,
                    text: a.textContent.trim().substring(0, 40)
                })).filter(l => l.text.length > 0);
            }''')
            if links:
                print(f"\n[INFO] 当前找到 {len(links)} 个链接")
                # 打印类目相关链接
                for link in links[:30]:
                    if any(k in link['text'] for k in ['美妆', '女装', '男装', '手机', '家居', '鞋', '运动']):
                        print(f"  {link['text']} -> {link['href']}")
        except:
            pass
