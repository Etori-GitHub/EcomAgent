#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok Shop - 连接真实 Chrome 测试
使用 CDP 连接已打开的 Chrome（真实浏览器）

步骤：
1. 先启动 Chrome（带调试端口）：
   chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/Users/Etroi/AppData/Local/Google/Chrome/User Data"
   
2. 手动从 Google 搜索进入 TikTok Shop

3. 运行此脚本，抓取数据
"""

import sys
import time
import json
from pathlib import Path

if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("[ERROR] 请先安装: pip install playwright")
    sys.exit(1)


def connect_real_chrome():
    """连接真实 Chrome 浏览器"""
    
    print(f"[INFO] 尝试连接到 Chrome (端口 9222)...")
    print(f"[提示] 确保已启动 Chrome:")
    print(f"  chrome.exe --remote-debugging-port=9222")
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222", timeout=10000)
            print(f"[OK] 已连接到真实 Chrome！")
            
            # 获取所有页面
            contexts = browser.contexts
            if not contexts:
                print(f"[ERROR] 没有找到浏览器上下文")
                return
            
            context = contexts[0]
            pages = context.pages
            
            print(f"[INFO] 找到 {len(pages)} 个页面")
            for i, page in enumerate(pages):
                print(f"  [{i}] {page.url}")
            
            # 等待用户确认
            print(f"\n{'='*60}")
            print(f"[重要] 请在浏览器中完成以下操作：")
            print(f"1. 打开 Google (google.com)")
            print(f"2. 搜索 'tiktok shop'")
            print(f"3. 点击搜索结果进入 TikTok Shop")
            print(f"4. 确认页面正常显示商品")
            print(f"5. 按 Enter 继续...")
            print(f"{'='*60}")
            input("按 Enter 继续...")
            
            # 重新获取页面列表（用户可能新开了标签页）
            pages = context.pages
            print(f"\n[INFO] 当前打开的页面 ({len(pages)} 个):")
            for i, page in enumerate(pages):
                try:
                    url = page.url
                    print(f"  [{i}] {url}")
                except Exception as e:
                    print(f"  [{i}] (无法获取URL: {e})")
            
            # 查找 TikTok Shop 页面（放宽条件）
            target_page = None
            for page in pages:
                try:
                    url = page.url
                    # 放宽匹配条件
                    if 'tiktok' in url or 'shop' in url:
                        target_page = page
                        print(f"\n[OK] 找到匹配页面: {url}")
                        break
                except:
                    continue
            
            # 如果还是没找到，让用户选择
            if not target_page and len(pages) > 0:
                print(f"\n[提示] 没有自动匹配到页面，请手动选择")
                print(f"[提示] 输入页面对应的编号 (0-{len(pages)-1})")
                try:
                    idx = int(input("请输入编号: "))
                    if 0 <= idx < len(pages):
                        target_page = pages[idx]
                        print(f"[OK] 已选择页面: {target_page.url}")
                except:
                    print(f"[ERROR] 输入无效")
                    return
            
            if not target_page:
                print(f"[ERROR] 没有找到 TikTok Shop 页面")
                print(f"[提示] 请先打开 TikTok Shop")
                return
            
            print(f"[OK] 找到 TikTok Shop 页面: {target_page.url}")
            
            # 检查是否被封
            content = target_page.content()
            if '{"code":100000}' in content:
                print(f"[ERROR] 页面仍然显示 code:100000")
                return
            
            print(f"[OK] 页面正常！")
            
            # 提取类目
            print(f"\n[INFO] 提取类目链接...")
            categories = target_page.evaluate("""
                () => {
                    const cats = [];
                    document.querySelectorAll('a').forEach(a => {
                        const href = a.href;
                        const text = a.innerText.trim();
                        if (href && href.includes('/c/') && text && text.length < 50 && text.length > 0) {
                            cats.push({name: text, url: href});
                        }
                    });
                    
                    // 去重
                    const seen = new Set();
                    return cats.filter(cat => {
                        if (seen.has(cat.url)) return false;
                        seen.add(cat.url);
                        return true;
                    });
                }
            """)
            
            print(f"[OK] 找到 {len(categories)} 个类目")
            
            if categories:
                print(f"\n[类目列表]")
                for i, cat in enumerate(categories[:10]):
                    print(f"  {i+1}. {cat['name']}")
                
                # 保存类目列表
                output_file = Path(__file__).parent.parent / "screenshots" / "categories_real_chrome.json"
                output_file.parent.mkdir(parents=True, exist_ok=True)
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(categories, f, ensure_ascii=False, indent=2)
                print(f"[OK] 类目列表已保存: {output_file}")
            
            # 测试抓取一个类目
            if categories:
                test_cat = categories[0]
                print(f"\n[测试] 点击类目: {test_cat['name']}")
                print(f"[URL] {test_cat['url']}")
                
                # 点击类目链接
                target_page.evaluate(f"""
                    () => {{
                        const links = document.querySelectorAll('a');
                        for (const link of links) {{
                            if (link.href.includes('/c/')) {{
                                link.click();
                                break;
                            }}
                        }}
                    }}
                """)
                
                time.sleep(5)
                
                # 检查结果
                content = target_page.content()
                if '{"code":100000}' in content:
                    print(f"[类目] ❌ 被封")
                else:
                    print(f"[类目] ✅ 成功！")
                    
                    # 提取商品
                    products = target_page.evaluate("""
                        () => {
                            const items = [];
                            document.querySelectorAll('a[href*="/shop/pdp/"]').forEach(a => {
                                const href = a.href;
                                const text = a.innerText.trim();
                                if (text && text.length > 5) {
                                    items.push({ text: text.substring(0, 50), url: href });
                                }
                            });
                            return items.slice(0, 20);
                        }
                    """)
                    
                    print(f"[商品数量] {len(products)}")
                    if products:
                        print(f"\n[商品示例]")
                        for i, p in enumerate(products[:5]):
                            print(f"  {i+1}. {p['text']}...")
            
            print(f"\n{'='*60}")
            print(f"[完成] 按 Enter 关闭...")
            print(f"{'='*60}")
            input()
            
        except Exception as e:
            print(f"[ERROR] 连接失败: {e}")
            print(f"[提示] 确保已启动 Chrome:")
            print(f"  chrome.exe --remote-debugging-port=9222")


if __name__ == "__main__":
    connect_real_chrome()