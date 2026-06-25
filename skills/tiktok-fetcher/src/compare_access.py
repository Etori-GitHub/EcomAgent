#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok Shop 访问差异对比脚本
分析直接访问 vs Google搜索进入的差异（Cookie、请求头等）
"""

import json
import sys
import time
from datetime import datetime

if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("[ERROR] 请先安装: pip install playwright")
    sys.exit(1)


def analyze_page(page, label):
    """分析页面状态"""
    print(f"\n{'='*60}")
    print(f"[分析] {label}")
    print(f"{'='*60}")
    
    # 基本信息
    print(f"[URL] {page.url}")
    print(f"[标题] {page.title()}")
    
    # Cookie 分析
    cookies = page.context.cookies()
    tiktok_cookies = [c for c in cookies if 'tiktok' in c.get('domain', '')]
    print(f"\n[Cookie 数量] TikTok 相关: {len(tiktok_cookies)} / 总数: {len(cookies)}")
    
    if tiktok_cookies:
        print(f"\n[TikTok Cookie 详情]")
        for c in tiktok_cookies[:10]:
            print(f"  - {c.get('name')}: {c.get('value')[:50]}...")
            print(f"    Domain: {c.get('domain')}, Path: {c.get('path')}")
            print(f"    Expires: {c.get('expires')}, HttpOnly: {c.get('httpOnly')}")
    
    # LocalStorage 分析
    try:
        local_storage = page.evaluate("""
            () => {
                const items = {};
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    items[key] = localStorage.getItem(key);
                }
                return items;
            }
        """)
        print(f"\n[LocalStorage 数量] {len(local_storage)}")
        if local_storage:
            print(f"[LocalStorage 内容]")
            for key, value in list(local_storage.items())[:5]:
                print(f"  - {key}: {str(value)[:100]}...")
    except Exception as e:
        print(f"[LocalStorage] 无法获取: {e}")
    
    # SessionStorage 分析
    try:
        session_storage = page.evaluate("""
            () => {
                const items = {};
                for (let i = 0; i < sessionStorage.length; i++) {
                    const key = sessionStorage.key(i);
                    items[key] = sessionStorage.getItem(key);
                }
                return items;
            }
        """)
        print(f"\n[SessionStorage 数量] {len(session_storage)}")
        if session_storage:
            print(f"[SessionStorage 内容]")
            for key, value in list(session_storage.items())[:5]:
                print(f"  - {key}: {str(value)[:100]}...")
    except Exception as e:
        print(f"[SessionStorage] 无法获取: {e}")
    
    # 页面内容检查
    content = page.content()
    if '{"code":100000}' in content:
        print(f"\n[结果] ❌ 被封 - code:100000")
        return {"success": False, "cookies": tiktok_cookies, "storage": local_storage}
    else:
        print(f"\n[结果] ✅ 成功 - 页面长度: {len(content)} chars")
        return {"success": True, "cookies": tiktok_cookies, "storage": local_storage}


def compare_access():
    """对比两种访问方式"""
    
    print(f"[INFO] 启动浏览器...")
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        
        # ========== 测试 1: 直接访问 ==========
        print(f"\n{'#'*60}")
        print(f"[测试 1] 直接访问 TikTok Shop")
        print(f"{'#'*60}")
        
        page1 = context.new_page()
        page1.goto("https://shop.tiktok.com/us", timeout=60000)
        time.sleep(5)
        
        result1 = analyze_page(page1, "直接访问")
        
        # ========== 测试 2: 从 Google 搜索进入 ==========
        print(f"\n{'#'*60}")
        print(f"[测试 2] 从 Google 搜索进入")
        print(f"{'#'*60}")
        
        page2 = context.new_page()
        
        # 先访问 Google
        print(f"[INFO] 访问 Google...")
        page2.goto("https://www.google.com", timeout=30000)
        time.sleep(2)
        
        # 搜索 TikTok Shop
        print(f"[INFO] 搜索 tiktok shop...")
        try:
            search_box = page2.locator('textarea[name="q"]').first
            search_box.fill("tiktok shop")
            search_box.press("Enter")
            time.sleep(3)
            
            # 点击搜索结果
            print(f"[INFO] 点击搜索结果...")
            links = page2.locator('a').all()
            for link in links:
                href = link.get_attribute("href")
                if href and "shop.tiktok.com" in href:
                    print(f"[点击] {href}")
                    link.click()
                    break
            
            time.sleep(5)
        except Exception as e:
            print(f"[ERROR] 搜索流程失败: {e}")
            # 手动输入 URL
            page2.goto("https://shop.tiktok.com/us")
            time.sleep(5)
        
        result2 = analyze_page(page2, "从 Google 搜索进入")
        
        # ========== 对比差异 ==========
        print(f"\n{'='*60}")
        print(f"[差异对比]")
        print(f"{'='*60}")
        
        print(f"\n[访问结果]")
        print(f"  直接访问: {'✅ 成功' if result1['success'] else '❌ 失败'}")
        print(f"  Google进入: {'✅ 成功' if result2['success'] else '❌ 失败'}")
        
        # Cookie 差异
        cookies1_names = set(c.get('name') for c in result1.get('cookies', []))
        cookies2_names = set(c.get('name') for c in result2.get('cookies', []))
        
        print(f"\n[Cookie 差异]")
        print(f"  直接访问 Cookie 数: {len(cookies1_names)}")
        print(f"  Google进入 Cookie 数: {len(cookies2_names)}")
        
        new_cookies = cookies2_names - cookies1_names
        missing_cookies = cookies1_names - cookies2_names
        
        if new_cookies:
            print(f"  Google进入 新增的 Cookie: {new_cookies}")
        if missing_cookies:
            print(f"  Google进入 缺少的 Cookie: {missing_cookies}")
        
        # 详细对比新增的 Cookie
        if new_cookies:
            print(f"\n[新增 Cookie 详情]")
            for c in result2.get('cookies', []):
                if c.get('name') in new_cookies:
                    print(f"  {c.get('name')}:")
                    print(f"    Value: {c.get('value')}")
                    print(f"    Domain: {c.get('domain')}")
                    print(f"    Expires: {c.get('expires')}")
        
        # Storage 差异
        storage1_keys = set(result1.get('storage', {}).keys()) if result1.get('storage') else set()
        storage2_keys = set(result2.get('storage', {}).keys()) if result2.get('storage') else set()
        
        print(f"\n[LocalStorage 差异]")
        print(f"  直接访问 Key 数: {len(storage1_keys)}")
        print(f"  Google进入 Key 数: {len(storage2_keys)}")
        
        new_keys = storage2_keys - storage1_keys
        if new_keys:
            print(f"  Google进入 新增的 Key: {new_keys}")
            for key in new_keys:
                value = result2.get('storage', {}).get(key, '')
                print(f"    {key}: {str(value)[:200]}...")
        
        # 保存对比结果
        output = {
            "timestamp": datetime.now().isoformat(),
            "test1_direct": {
                "success": result1['success'],
                "cookies": result1.get('cookies', []),
                "storage_keys": list(storage1_keys)
            },
            "test2_google": {
                "success": result2['success'],
                "cookies": result2.get('cookies', []),
                "storage_keys": list(storage2_keys)
            },
            "differences": {
                "new_cookies": list(new_cookies),
                "new_storage_keys": list(new_keys)
            }
        }
        
        import pathlib
        output_file = pathlib.Path(__file__).parent.parent / "screenshots" / "access_comparison.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\n[OK] 对比结果已保存: {output_file}")
        
        input("\n按 Enter 关闭浏览器...")
        browser.close()


if __name__ == "__main__":
    compare_access()