#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试抓取脚本 - 只抓取一个分类验证名称提取
"""

import sys
import io
import json
from pathlib import Path
from datetime import datetime

# Windows UTF-8 兼容
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright

def test_fetch():
    """测试抓取一个分类"""
    
    with sync_playwright() as p:
        user_data_dir = Path.home() / ".openclaw" / "chrome-profile-amazon"
        user_data_dir.mkdir(parents=True, exist_ok=True)
        
        context = p.chromium.launch_persistent_context(
            str(user_data_dir),
            headless=False,
            viewport={"width": 1280, "height": 800}
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        
        # 打开 Electronics Best Sellers
        url = "https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics"
        print(f"打开页面: {url}")
        page.goto(url, timeout=30000)
        
        # 等待页面加载
        page.wait_for_selector('li.zg-no-numbers, div#gridItemRoot', timeout=10000)
        
        # 使用更新后的 JS 提取数据
        js_code = """
            () => {
                const results = [];
                const rows = document.querySelectorAll('li.zg-no-numbers, div#gridItemRoot > div');
                
                rows.forEach((row, idx) => {
                    try {
                        // 排名
                        const rankEl = row.querySelector('.zg-bdg-text, span.zg-bdg-text');
                        const rank = rankEl ? parseInt(rankEl.innerText.replace('#', '').trim()) : idx + 1;

                        // 商品链接和 ASIN
                        const allLinks = row.querySelectorAll('a.a-link-normal');
                        let link = null;
                        let asin = '';
                        
                        for (const a of allLinks) {
                            const h = a.href || '';
                            const match = h.match(/\\/dp\\/([A-Z0-9]{10})/);
                            if (match) {
                                link = a;
                                asin = match[1];
                                break;
                            }
                        }

                        // 商品名称 - 按可靠性优先级提取
                        let name = '';
                        
                        // 方法1: 从专门的名称容器获取
                        const nameEl = row.querySelector('div._cDEzb_p13n-sc-css-line-clamp-3_g3dy1, div[class*="line-clamp"]');
                        if (nameEl?.innerText?.trim()) {
                            name = nameEl.innerText.trim();
                        }
                        
                        // 方法2: 从图片 alt 属性获取
                        if (!name) {
                            const imgEl = row.querySelector('img');
                            if (imgEl?.alt?.trim()) {
                                name = imgEl.alt.trim();
                            }
                        }
                        
                        // 方法3: 从链接文字获取
                        if (!name && link?.innerText?.trim()) {
                            name = link.innerText.trim();
                        }

                        // 价格
                        let price = null;
                        const priceEl = row.querySelector('span._cDEzb_p13n-sc-price_3mJ9Z, span[class*="p13n-sc-price"]');
                        if (priceEl) {
                            const priceText = priceEl.innerText.trim();
                            const priceMatch = priceText.match(/\\$?([\\d.]+)/);
                            if (priceMatch) {
                                price = parseFloat(priceMatch[1]);
                            }
                        }
                        
                        // 备用价格选择器
                        if (price === null) {
                            const priceEl2 = row.querySelector('span.a-color-price');
                            if (priceEl2) {
                                const priceText = priceEl2.innerText.trim();
                                const priceMatch = priceText.match(/\\$?([\\d.]+)/);
                                if (priceMatch) {
                                    price = parseFloat(priceMatch[1]);
                                }
                            }
                        }

                        // 评分
                        let rating = null;
                        const ratingEl = row.querySelector('span.a-icon-alt');
                        if (ratingEl) {
                            const ratingText = ratingEl.innerText || '';
                            const ratingMatch = ratingText.match(/([\\d.]+)\\s*out of/);
                            if (ratingMatch) {
                                rating = parseFloat(ratingMatch[1]);
                            }
                        }
                        
                        // 评价数
                        let ratingCount = null;
                        const countEl = row.querySelector('span.a-size-small');
                        if (countEl) {
                            const countText = countEl.innerText.replace(/[^\\d]/g, '');
                            if (countText && parseInt(countText) > 0) {
                                ratingCount = parseInt(countText);
                            }
                        }

                        if (asin) {
                            results.push({
                                rank,
                                name,
                                asin,
                                product_url: `https://www.amazon.com/dp/${asin}`,
                                price,
                                rating,
                                rating_count: ratingCount
                            });
                        }
                    } catch (e) {
                        console.log(`商品 ${idx} 解析失败:`, e.message);
                    }
                });
                
                return results;
            }
        """
        
        products = page.evaluate(js_code)
        
        print(f"\n=== 测试结果 ===")
        print(f"共提取 {len(products)} 个商品")
        print(f"\n前 10 个商品:")
        for p in products[:10]:
            print(f"  #{p['rank']}: {p['name'][:40] if p['name'] else '(empty)'}... | ${p['price']} | {p['rating']}⭐")
        
        # 统计名称提取成功率
        named = sum(1 for p in products if p['name'])
        print(f"\n名称提取成功率: {named}/{len(products)} ({named/len(products)*100:.1f}%)")
        
        context.close()
        return products

if __name__ == "__main__":
    test_fetch()
