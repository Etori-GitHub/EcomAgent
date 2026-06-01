#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
类目提取脚本 - 从平台首页提取类目列表并保存到数据库
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CATEGORIES_DB = DATA_DIR / "categories.db"


def save_categories(platform: str, categories: list):
    """保存类目到数据库"""
    conn = sqlite3.connect(CATEGORIES_DB)
    cursor = conn.cursor()
    
    new_count = 0
    update_count = 0
    
    for cat in categories:
        name = cat.get('name')
        url = cat.get('url')
        
        if not name or not url:
            continue
        
        cursor.execute("SELECT id FROM categories WHERE platform = ? AND name = ?", (platform, name))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute("UPDATE categories SET url = ? WHERE platform = ? AND name = ?", (url, platform, name))
            update_count += 1
        else:
            cursor.execute('''
                INSERT INTO categories (platform, name, url, enabled, added_at)
                VALUES (?, ?, ?, 1, ?)
            ''', (platform, name, url, datetime.now().isoformat()))
            new_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"[OK] {platform}: 新增 {new_count} 个类目，更新 {update_count} 个")
    return new_count, update_count


def extract_amazon_categories():
    """从 Amazon Best Sellers 提取类目"""
    from playwright.sync_api import sync_playwright
    
    print("[INFO] 正在提取 Amazon 类目...")
    
    categories = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            print("[INFO] 访问 Amazon Best Sellers...")
            page.goto("https://www.amazon.com/Best-Sellers/zgbsto", timeout=60000)
            page.wait_for_timeout(3000)
            
            print("[INFO] 提取类目...")
            category_js = '''
                () => {
                    const categories = [];
                    const container = document.querySelector('div[role="group"][aria-label="Navigation Tree"]');
                    if (!container) return categories;
                    
                    const ul = container.querySelector('ul');
                    if (!ul) return categories;
                    
                    const items = ul.querySelectorAll('li');
                    items.forEach(li => {
                        const link = li.querySelector('a');
                        if (link && link.href) {
                            const name = link.textContent.trim();
                            const url = link.href;
                            if (name && url && url.includes('/zgbs/')) {
                                categories.push({ name, url });
                            }
                        }
                    });
                    
                    return categories;
                }
            '''
            
            categories = page.evaluate(category_js)
            print(f"[OK] 找到 {len(categories)} 个类目")
            
        except Exception as e:
            print(f"[ERROR] 提取失败: {e}")
        finally:
            browser.close()
    
    return categories


def extract_tiktok_categories():
    """从 TikTok Shop 提取类目"""
    from playwright.sync_api import sync_playwright
    import time
    
    print("=" * 50)
    print("[INFO] 开始提取 TikTok 类目")
    print("=" * 50)
    
    categories = []
    
    print("[INFO] 启动浏览器...")
    from playwright.sync_api import sync_playwright
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    print("[OK] 浏览器已启动")
    
    try:
        print("[INFO] 访问 TikTok Shop...")
        page.goto("https://www.tiktok.com/shop", timeout=60000, wait_until='domcontentloaded')
        print(f"[OK] 页面已加载: {page.url}")
        
        # 等待页面稳定
        print("[INFO] 等待页面稳定...")
        try:
            page.wait_for_load_state('networkidle', timeout=15000)
        except:
            print("[WARN] networkidle 超时，继续...")
        
        # 检查是否被重定向
        current_url = page.url
        print(f"[INFO] 当前 URL: {current_url}")
        
        # 等待人机验证（最多30秒）
        print("[INFO] 检查人机验证...")
        for i in range(15):
            try:
                has_captcha = page.evaluate('''() => {
                    const captcha = document.querySelector('.captcha_verify_container');
                    return captcha && captcha.style.visibility === 'visible';
                }''')
            except:
                has_captcha = False
            
            if has_captcha:
                if i == 0:
                    print("[INFO] 检测到人机验证，请在浏览器中手动完成...")
                time.sleep(2)
                print(f"[INFO] 等待验证... {i*2+2}秒")
            else:
                if i > 0:
                    print("[OK] 人机验证已完成")
                break
        else:
            print("[WARN] 人机验证等待超时，继续尝试提取...")
        
        # 等待页面内容加载
        print("[INFO] 等待页面内容加载...")
        page.wait_for_timeout(5000)
        
        # 等待链接出现（最多等30秒）
        print("[INFO] 等待页面内容渲染...")
        for i in range(30):
            try:
                link_count = page.evaluate("document.querySelectorAll('a').length")
                if link_count > 0:
                    print(f"[OK] 页面已加载，找到 {link_count} 个链接")
                    break
            except:
                pass
            page.wait_for_timeout(1000)
            print(f"[INFO] 等待中... {i+1}秒")
        else:
            print("[WARN] 等待超时，尝试提取...")
        
        # 提取类目链接...
        
        try:
            # 先检查页面有多少链接
            link_count = page.evaluate("document.querySelectorAll('a').length")
            print(f"[INFO] 页面共有 {link_count} 个链接")
        except Exception as e:
            print(f"[WARN] 无法获取链接数量: {e}")
            link_count = 0
        
        if link_count == 0:
            print("[WARN] 页面没有链接，可能内容未加载或被反爬")
            try:
                print(f"[INFO] 页面标题: {page.title()}")
            except:
                pass
            print(f"[INFO] 页面URL: {page.url}")
        
        # 提取所有链接
        try:
            categories = page.evaluate('''() => {
                const categories = [];
                
                // 方法1: 直接找类目容器中的链接
                const categoryLinks = document.querySelectorAll('a[href*="shop.tiktok.com/us/c/"]');
                categoryLinks.forEach(link => {
                    const href = link.href || '';
                    const name = (link.textContent || '').trim();
                    const dataId = link.getAttribute('data-id') || '';
                    
                    if (href && name && dataId) {
                        categories.push({ 
                            name: name, 
                            url: href,
                            id: dataId
                        });
                    }
                });
                
                // 去重
                const seen = new Set();
                return categories.filter(c => {
                    if (seen.has(c.id) || !c.name) return false;
                    seen.add(c.id);
                    return true;
                });
            }''')
        except Exception as e:
            print(f"[ERROR] 提取链接失败: {e}")
            categories = []
        
        print(f"[OK] 找到 {len(categories)} 个类目")
        
        # 如果没找到，打印一些链接用于调试
        if len(categories) == 0 and link_count > 0:
            sample_links = page.evaluate('''() => {
                return Array.from(document.querySelectorAll('a')).slice(0, 30).map(a => ({
                    href: a.href,
                    text: a.textContent.trim().substring(0, 40)
                })).filter(l => l.text.length > 0);
            }''')
            print("[DEBUG] 页面链接示例:")
            for link in sample_links[:15]:
                print(f"  {link['text']} -> {link['href'][:70]}")
        
    except Exception as e:
        print(f"[ERROR] 提取失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("[INFO] 关闭浏览器...")
        browser.close()
        p.stop()
        print("[OK] 完成")
    
    print("=" * 50)
    return categories


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='提取平台类目')
    parser.add_argument('platform', choices=['amazon', 'tiktok'], help='平台名称')
    args = parser.parse_args()
    
    print(f"\n[INFO] 开始提取 {args.platform} 类目...")
    
    if args.platform == 'amazon':
        categories = extract_amazon_categories()
    else:
        categories = extract_tiktok_categories()
    
    if categories:
        save_categories(args.platform, categories)
    else:
        print("[WARN] 没有提取到类目")
    
    print(f"\n[INFO] 脚本结束")


if __name__ == "__main__":
    main()
