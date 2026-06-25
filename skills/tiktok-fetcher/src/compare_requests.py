#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok Shop 请求参数对比脚本（完整版）
对比：首页访问、类目页面访问的请求差异
"""

import json
import sys
import time
from datetime import datetime
from urllib.parse import urlparse, parse_qs

if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("[ERROR] 请先安装: pip install playwright")
    sys.exit(1)


def capture_requests(page, label):
    """捕获所有请求信息"""
    requests_data = []
    
    def on_request(request):
        if 'shop.tiktok.com' in request.url or 'tiktok' in request.url:
            req_info = {
                "url": request.url,
                "method": request.method,
                "headers": dict(request.headers),
                "post_data": request.post_data,
                "resource_type": request.resource_type,
            }
            
            parsed = urlparse(request.url)
            req_info["query_params"] = dict(parse_qs(parsed.query))
            req_info["path"] = parsed.path
            req_info["domain"] = parsed.netloc
            
            requests_data.append(req_info)
            print(f"  [{request.method}] {request.url[:80]}...")
    
    page.on("request", on_request)
    return requests_data


def analyze_request(req, label):
    """分析单个请求"""
    print(f"\n[{label} - 主请求详情]")
    print(f"  URL: {req['url']}")
    print(f"  Method: {req['method']}")
    print(f"  Headers:")
    
    important_keys = ['referer', 'origin', 'accept', 'accept-language', 'accept-encoding',
                     'user-agent', 'sec-ch-ua', 'sec-ch-ua-mobile', 'sec-ch-ua-platform',
                     'sec-fetch-dest', 'sec-fetch-mode', 'sec-fetch-site', 'cookie']
    
    for key in important_keys:
        value = req['headers'].get(key, 'N/A')
        if key == 'cookie' and len(str(value)) > 100:
            value = str(value)[:100] + '...'
        print(f"    {key}: {value}")
    
    if req['query_params']:
        print(f"  Query Params:")
        for k, v in req['query_params'].items():
            print(f"    {k}: {v}")


def compare_two_requests(req1, req2, label1, label2):
    """对比两个请求的差异"""
    print(f"\n[{label1} vs {label2} - 关键差异]")
    
    important_keys = ['referer', 'sec-fetch-site', 'sec-fetch-dest', 'sec-fetch-mode', 
                     'sec-ch-ua', 'sec-ch-ua-mobile', 'sec-ch-ua-platform', 'origin']
    
    for key in important_keys:
        val1 = req1['headers'].get(key, 'N/A')
        val2 = req2['headers'].get(key, 'N/A')
        
        if val1 != val2:
            print(f"  [{key}] ⚠️  有差异")
            print(f"    {label1}: {val1}")
            print(f"    {label2}: {val2}")
        else:
            print(f"  [{key}] 无差异")


def main():
    print(f"[INFO] 启动浏览器...")
    
    all_results = {}
    test_cat_url = None
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        
        # ========== 测试 1: 直接访问首页 ==========
        print(f"\n{'='*60}")
        print(f"[测试 1] 直接访问 TikTok Shop 首页")
        print(f"{'='*60}")
        
        page1 = context.new_page()
        requests1 = capture_requests(page1, "直接访问首页")
        
        page1.goto("https://shop.tiktok.com/us", timeout=60000)
        time.sleep(5)
        
        content1 = page1.content()
        success1 = '{"code":100000}' not in content1
        print(f"\n[结果] {'✅ 成功' if success1 else '❌ 失败'}")
        
        all_results["direct_homepage"] = {"success": success1, "requests": requests1}
        
        # ========== 测试 2: 从 Google 搜索进入首页 ==========
        print(f"\n{'='*60}")
        print(f"[测试 2] 从 Google 搜索进入首页")
        print(f"{'='*60}")
        
        page2 = context.new_page()
        requests2 = capture_requests(page2, "Google进入首页")
        
        print(f"[INFO] 访问 Google...")
        page2.goto("https://www.google.com", timeout=30000)
        time.sleep(2)
        
        print(f"[INFO] 搜索 tiktok shop...")
        search_box = page2.locator('textarea[name="q"]').first
        search_box.fill("tiktok shop")
        search_box.press("Enter")
        time.sleep(3)
        
        print(f"\n{'='*60}")
        print(f"[重要] 如有验证码请手动完成，然后按 Enter 继续...")
        print(f"{'='*60}")
        input("按 Enter 继续...")
        
        print(f"[INFO] 点击 TikTok Shop 搜索结果...")
        h3_elements = page2.locator('h3').all()
        for h3 in h3_elements:
            text = h3.inner_text()
            if 'TikTok Shop' in text:
                print(f"[找到] {text}")
                parent = h3.locator('xpath=..')
                parent.click()
                break
        
        time.sleep(5)
        
        content2 = page2.content()
        success2 = '{"code":100000}' not in content2
        print(f"\n[结果] {'✅ 成功' if success2 else '❌ 失败'}")
        
        all_results["google_homepage"] = {"success": success2, "requests": requests2}
        
        # ========== 测试 3: 从首页点击类目 ==========
        print(f"\n{'='*60}")
        print(f"[测试 3] 从首页点击进入类目页面")
        print(f"{'='*60}")
        
        requests3 = capture_requests(page2, "点击进入类目")
        
        print(f"[INFO] 提取类目链接...")
        categories = page2.evaluate("""
            () => {
                const cats = [];
                document.querySelectorAll('a').forEach(a => {
                    const href = a.href;
                    const text = a.innerText.trim();
                    if (href && href.includes('/c/') && text && text.length < 50) {
                        cats.push({name: text, url: href});
                    }
                });
                return cats.slice(0, 5);
            }
        """)
        
        print(f"[INFO] 找到 {len(categories)} 个类目")
        
        if categories:
            test_cat = categories[0]
            test_cat_url = test_cat['url']
            print(f"[INFO] 点击类目: {test_cat['name']}")
            print(f"[URL] {test_cat_url}")
            
            page2.evaluate("""
                () => {
                    const links = document.querySelectorAll('a');
                    for (const link of links) {
                        if (link.href.includes('/c/')) {
                            link.click();
                            break;
                        }
                    }
                }
            """)
            
            time.sleep(5)
            
            content3 = page2.content()
            success3 = '{"code":100000}' not in content3
            print(f"\n[结果] {'✅ 成功' if success3 else '❌ 失败'}")
            
            all_results["click_category"] = {
                "success": success3, 
                "requests": requests3,
                "category": test_cat
            }
        else:
            print(f"[WARN] 没有找到类目链接，使用默认 URL")
            test_cat_url = "https://shop.tiktok.com/c/beauty-personal-care/601450"
        
        # ========== 测试 4: 直接访问类目页面 ==========
        print(f"\n{'='*60}")
        print(f"[测试 4] 直接访问类目页面（对比）")
        print(f"{'='*60}")
        
        page3 = context.new_page()
        requests4 = capture_requests(page3, "直接访问类目")
        
        print(f"[INFO] 直接访问: {test_cat_url}")
        page3.goto(test_cat_url, timeout=60000)
        time.sleep(5)
        
        content4 = page3.content()
        success4 = '{"code":100000}' not in content4
        print(f"\n[结果] {'✅ 成功' if success4 else '❌ 失败'}")
        
        all_results["direct_category"] = {
            "success": success4,
            "requests": requests4,
            "url": test_cat_url
        }
        
        # ========== 分析对比 ==========
        print(f"\n{'='*60}")
        print(f"[请求对比分析]")
        print(f"{'='*60}")
        
        # 找到各个主页面请求
        def find_main_request(requests, path_pattern):
            for req in requests:
                if req.get("resource_type") == "document" and path_pattern in req.get("url", ""):
                    return req
            return None
        
        req_direct_home = find_main_request(requests1, "/us")
        req_google_home = find_main_request(requests2, "/us")
        req_click_cat = find_main_request(requests3, "/c/")
        req_direct_cat = find_main_request(requests4, "/c/")
        
        # 分析首页请求
        if req_direct_home:
            analyze_request(req_direct_home, "直接访问首页")
        if req_google_home:
            analyze_request(req_google_home, "Google进入首页")
        if req_direct_home and req_google_home:
            compare_two_requests(req_direct_home, req_google_home, "直接访问", "Google进入")
        
        # 分析类目请求
        if req_click_cat:
            analyze_request(req_click_cat, "点击进入类目")
        if req_direct_cat:
            analyze_request(req_direct_cat, "直接访问类目")
        if req_click_cat and req_direct_cat:
            compare_two_requests(req_click_cat, req_direct_cat, "点击进入", "直接访问")
        
        # 保存结果
        output_file = "C:/Users/Etroi/.openclaw/workspace/code/EcomAgent/skills/tiktok-fetcher/screenshots/request_comparison.json"
        import pathlib
        pathlib.Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "results": all_results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n[OK] 完整结果已保存: {output_file}")
        
        input("\n按 Enter 关闭浏览器...")
        browser.close()


if __name__ == "__main__":
    main()
