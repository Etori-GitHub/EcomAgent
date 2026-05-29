"""
研究 1688 商品详情页可获取的数据
"""
from playwright.sync_api import sync_playwright
import json
import re

def analyze_1688_detail():
    with sync_playwright() as p:
        # 启动浏览器
        print("启动浏览器...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # 先搜索获取真实商品链接
        search_url = 'https://s.1688.com/selloffer/offer_search.htm?keywords=手机壳'
        print(f"打开搜索页: {search_url}")
        
        try:
            page.goto(search_url, wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(3000)
        except Exception as e:
            print(f"页面加载超时，继续尝试: {e}")
        
        print(f"页面标题: {page.title()}")
        
        # 获取商品链接
        print("\n=== 查找商品链接 ===")
        
        # 尝试多种选择器
        link_selectors = [
            'a[href*="detail.1688.com/offer"]',
            'a[href*="offer"]',
            '.offer-item a',
            '.list-item a',
            '[class*="offer"] a',
        ]
        
        found_links = []
        for sel in link_selectors:
            links = page.query_selector_all(sel)
            if links:
                print(f"选择器 '{sel}' 找到 {len(links)} 个链接")
                for link in links[:5]:
                    href = link.get_attribute('href')
                    if href and 'detail.1688.com' in href:
                        found_links.append(href)
                        print(f"  - {href}")
                if found_links:
                    break
        
        if not found_links:
            # 保存搜索页面 HTML 用于分析
            html = page.content()
            with open('1688_search.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print("\n未找到商品链接，已保存搜索页面 HTML: 1688_search.html")
            
            # 截图
            page.screenshot(path='1688_search.png', full_page=False)
            print("已保存截图: 1688_search.png")
        else:
            # 进入第一个商品详情页
            detail_url = found_links[0]
            print(f"\n=== 进入商品详情页 ===")
            print(f"URL: {detail_url}")
            
            try:
                page.goto(detail_url, wait_until='networkidle', timeout=30000)
                page.wait_for_timeout(3000)
            except Exception as e:
                print(f"详情页加载超时: {e}")
                page.wait_for_timeout(5000)
            
            print(f"页面标题: {page.title()}")
            
            # 保存详情页 HTML
            html = page.content()
            with open('1688_detail.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print("已保存详情页 HTML: 1688_detail.html")
            
            # 截图
            page.screenshot(path='1688_detail.png', full_page=False)
            print("已保存截图: 1688_detail.png")
            
            # 提取商品信息
            print("\n=== 商品信息提取 ===")
            
            # 从 HTML 中提取数据
            # 1. 标题
            title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
            if title_match:
                title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
                print(f"标题: {title[:100]}")
            
            # 2. 价格
            price_match = re.search(r'price[^>]*>.*?(\d+\.?\d*)', html, re.DOTALL | re.IGNORECASE)
            if price_match:
                print(f"价格: {price_match.group(1)}")
            
            # 3. 图片
            img_matches = re.findall(r'<img[^>]*src=["\']([^"\']+)["\']', html)
            print(f"\n找到 {len(img_matches)} 个图片")
            for i, img in enumerate(img_matches[:10]):
                if 'cbu' in img or '1688' in img or 'alicdn' in img:
                    print(f"  图片 {i+1}: {img[:80]}...")
        
        # 关闭浏览器
        browser.close()
        print("\n分析完成！")

if __name__ == '__main__':
    analyze_1688_detail()
