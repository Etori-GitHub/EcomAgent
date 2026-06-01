#!/usr/bin/env python3
"""检查 TikTok 页面链接格式"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    print("[INFO] 打开 TikTok Shop...")
    page.goto("https://www.tiktok.com/shop", timeout=120000)
    page.wait_for_timeout(10000)
    
    # 滚动
    for i in range(3):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)
    
    # 检查所有链接
    print("\n[INFO] 检查页面链接...")
    links = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a')).map(a => ({
            href: a.href,
            text: a.textContent.trim().substring(0, 30)
        })).filter(l => l.text.length > 0);
    }''')
    
    print(f"找到 {len(links)} 个链接")
    
    # 找类目相关的链接
    print("\n类目相关链接:")
    for link in links:
        href = link['href']
        text = link['text']
        # 检查类目名称
        if any(k in text for k in ['美妆', '女装', '男装', '手机', '数码', '配件', '家居', '厨房', '鞋靴', '运动', '箱包', '玩具', '母婴', '宠物', '家电', '家具', '珠宝', '二手', '图书', '穆斯林', '五金', '家纺', '食品', '保健', '汽车']):
            print(f"  {text} -> {href}")
    
    # 保持浏览器打开
    print("\n[INFO] 浏览器保持打开，30秒后关闭...")
    page.wait_for_timeout(30000)
    browser.close()
