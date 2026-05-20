#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 TikTok Shop 页面内容
"""

from playwright.sync_api import sync_playwright

def check_page_content():
    print("[INFO] 连接到 Chrome...")
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        print(f"[OK] 连接成功！")
        
        context = browser.contexts[0]
        print(f"[INFO] 当前有 {len(context.pages)} 个页面")
        
        # 找到 TikTok 页面
        tiktok_page = None
        for page in context.pages:
            print(f"  - {page.url}")
            if "tiktok.com" in page.url:
                tiktok_page = page
        
        if not tiktok_page:
            print("[ERROR] 没有找到 TikTok 页面")
            return
        
        print(f"\n[INFO] 检查页面: {tiktok_page.url}")
        
        # 检查页面内容
        content = tiktok_page.content()
        print(f"[INFO] 页面内容长度: {len(content)} 字符")
        
        # 检查是否有 /shop/c/ 链接
        has_shop_c = "/shop/c/" in content
        print(f"[INFO] 是否有 /shop/c/ 链接: {has_shop_c}")
        
        # 获取所有链接
        links_js = """
            () => {
                const links = Array.from(document.querySelectorAll('a'));
                return links.map(link => ({
                    href: link.href,
                    text: (link.innerText || link.textContent || '').trim().substring(0, 50)
                })).filter(l => l.href && l.text);
            }
        """
        
        links = tiktok_page.evaluate(links_js)
        print(f"\n[INFO] 找到 {len(links)} 个链接")
        
        # 打印前 20 个链接
        print("\n[前 20 个链接]:")
        for i, link in enumerate(links[:20]):
            print(f"  [{i}] {link['text']} -> {link['href']}")
        
        # 检查是否有包含 shop 的链接
        shop_links = [l for l in links if 'shop' in l['href'].lower()]
        print(f"\n[INFO] 包含 'shop' 的链接: {len(shop_links)}")
        for i, link in enumerate(shop_links[:10]):
            print(f"  [{i}] {link['text']} -> {link['href']}")
        
        # 检查是否有包含 /shop/c/ 的链接
        shop_c_links = [l for l in links if '/shop/c/' in l['href']]
        print(f"\n[INFO] 包含 '/shop/c/' 的链接: {len(shop_c_links)}")
        for i, link in enumerate(shop_c_links[:10]):
            print(f"  [{i}] {link['text']} -> {link['href']}")
        
        # 检查页面标题
        title = tiktok_page.title()
        print(f"\n[INFO] 页面标题: {title}")
        
        # 检查是否有登录状态
        login_js = """
            () => {
                // 检查是否有登录按钮或用户头像
                const loginBtn = document.querySelector('[data-e2e="login-button"]');
                const userAvatar = document.querySelector('[data-e2e="profile-icon"]');
                return {
                    hasLoginBtn: !!loginBtn,
                    hasUserAvatar: !!userAvatar,
                    loginBtnText: loginBtn?.innerText || null,
                    userAvatarAlt: userAvatar?.alt || null
                };
            }
        """
        
        login_status = tiktok_page.evaluate(login_js)
        print(f"\n[INFO] 登录状态: {login_status}")

if __name__ == "__main__":
    check_page_content()