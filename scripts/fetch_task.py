#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据抓取任务脚本 - 任务模式，支持断点续抓
"""

import json
import sqlite3
import subprocess
import sys
import os
import time
import random
from datetime import datetime, date
from pathlib import Path
from typing import Optional, List, Dict, Any

# Windows UTF-8 兼容
if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TASKS_DIR = BASE_DIR / "output" / "tasks"
SCRAPING_DIR = BASE_DIR / "output" / "scraping"

CATEGORIES_DB = DATA_DIR / "categories.db"
DAILY_DB = DATA_DIR / "category_daily.db"
TASKS_DB = DATA_DIR / "tasks.db"

TASKS_DIR.mkdir(parents=True, exist_ok=True)
SCRAPING_DIR.mkdir(parents=True, exist_ok=True)


def random_wait(min_ms=1000, max_ms=3000):
    wait_ms = random.randint(min_ms, max_ms)
    return wait_ms


def get_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


class FetchTask:
    """抓取任务"""
    
    def __init__(self, platform: str, task_id: Optional[str] = None):
        self.platform = platform
        self.task_id = task_id or f"{platform}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.task_file = TASKS_DIR / f"{self.task_id}.json"
        self.status = "running"
        self.started_at = datetime.now().isoformat()
        self.browser = None
        self.page = None
        self.playwright = None
        
    def load_task(self) -> bool:
        """加载已存在的任务"""
        if self.task_file.exists():
            with open(self.task_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.status = data.get('status', 'running')
            self.started_at = data.get('started_at')
            return True
        return False
    
    def save_task(self, categories: List[Dict]):
        """保存任务状态"""
        data = {
            "task_id": self.task_id,
            "platform": self.platform,
            "status": self.status,
            "started_at": self.started_at,
            "total_categories": len(categories),
            "completed_categories": sum(1 for c in categories if c.get('status') == 'done'),
            "categories": categories
        }
        
        with open(self.task_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def update_db_status(self, status: str, error: str = None):
        """更新数据库中的任务状态"""
        conn = get_db(TASKS_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO tasks 
            (task_id, platform, status, started_at, finished_at, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            self.task_id,
            self.platform,
            status,
            self.started_at,
            datetime.now().isoformat() if status in ['completed', 'failed', 'cancelled'] else None,
            error
        ))
        
        conn.commit()
        conn.close()
    
    def get_enabled_categories(self) -> List[Dict]:
        """获取启用的类目列表"""
        conn = get_db(CATEGORIES_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, url
            FROM categories
            WHERE platform = ? AND enabled = 1
            ORDER BY name
        ''', (self.platform,))
        
        categories = []
        today = date.today().isoformat()
        
        for row in cursor.fetchall():
            cat = dict(row)
            cat['status'] = 'pending'
            
            # 检查今日是否已抓
            daily_conn = get_db(DAILY_DB)
            daily_cursor = daily_conn.cursor()
            daily_cursor.execute('''
                SELECT id FROM category_daily
                WHERE category_id = ? AND date = ?
            ''', (cat['id'], today))
            
            if daily_cursor.fetchone():
                cat['status'] = 'skipped'
            
            daily_conn.close()
            categories.append(cat)
        
        conn.close()
        return categories
    
    def init_browser(self):
        """初始化浏览器"""
        from playwright.sync_api import sync_playwright
        
        if self.platform == 'amazon':
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=False)
            self.page = self.browser.new_page()
        else:
            # TikTok 也直接启动浏览器
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=False)
            self.page = self.browser.new_page()
    
    def close_browser(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def fetch_amazon_category(self, category: Dict) -> List[Dict]:
        """抓取 Amazon 类目商品"""
        products = []
        
        try:
            print(f"[INFO] 访问: {category['url']}")
            self.page.goto(category['url'], timeout=60000)
            self.page.wait_for_timeout(random_wait(2000, 4000))
            
            # 提取商品
            product_js = '''
                () => {
                    const products = [];
                    const items = document.querySelectorAll('#gridItemRoot');
                    
                    items.forEach((item, idx) => {
                        const link = item.querySelector('a.a-link-normal');
                        const img = item.querySelector('img');
                        const titleEl = item.querySelector('a > span > div');
                        
                        // 价格 - 更新选择器
                        let price = null;
                        let priceEl = item.querySelector('span._cDEzb_p13n-sc-price_3mJ9Z, span[class*="p13n-sc-price"]');
                        if (priceEl) {
                            const priceMatch = priceEl.innerText.match(/\$?([\d.]+)/);
                            if (priceMatch) price = parseFloat(priceMatch[1]);
                        }
                        // 备用价格选择器
                        if (price === null) {
                            priceEl = item.querySelector('span.a-color-price');
                            if (priceEl) {
                                const priceMatch = priceEl.innerText.match(/\$?([\d.]+)/);
                                if (priceMatch) price = parseFloat(priceMatch[1]);
                            }
                        }
                        
                        // 评分 - 更新选择器
                        let rating = null;
                        const ratingEl = item.querySelector('span.a-icon-alt');
                        if (ratingEl) {
                            const ratingMatch = ratingEl.innerText.match(/([\d.]+)\s*out of/);
                            if (ratingMatch) rating = parseFloat(ratingMatch[1]);
                        }
                        
                        // 评论数 - 更新选择器
                        let ratingCount = null;
                        const ratingLink = item.querySelector('a[aria-label*="stars"]');
                        if (ratingLink) {
                            const ariaLabel = ratingLink.getAttribute('aria-label') || '';
                            const countMatch = ariaLabel.match(/([\d,]+)\s*ratings/);
                            if (countMatch) ratingCount = parseInt(countMatch[1].replace(/,/g, ''));
                        }
                        // 备用评论数选择器
                        if (ratingCount === null) {
                            const countEl = item.querySelector('span.a-size-small');
                            if (countEl) {
                                const countText = countEl.innerText.replace(/[^\d]/g, '');
                                if (countText && parseInt(countText) > 0) {
                                    ratingCount = parseInt(countText);
                                }
                            }
                        }
                        
                        if (link && img) {
                            const asinMatch = link.href.match(/\\/dp\\/([A-Z0-9]+)/);
                            if (asinMatch) {
                                products.push({
                                    asin: asinMatch[1],
                                    name: titleEl ? titleEl.textContent.trim() : '',
                                    image_url: img.src,
                                    product_url: link.href,
                                    rank: idx + 1,
                                    price: price,
                                    rating: rating,
                                    rating_count: ratingCount
                                });
                            }
                        }
                    });
                    
                    return products.slice(0, 20);
                }
            '''
            
            products = self.page.evaluate(product_js)
            
            # 为每个商品添加正确的类目名称
            category_name = category['name']
            for p in products:
                p['category'] = category_name
            
            print(f"[INFO] 提取到 {len(products)} 个商品")
            
        except Exception as e:
            print(f"[ERROR] 抓取失败: {e}")
            
        except Exception as e:
            print(f"[ERROR] 抓取失败: {e}")
        
        return products
    
    def fetch_tiktok_category(self, category: Dict) -> List[Dict]:
        """抓取 TikTok 类目商品"""
        products = []
        
        try:
            # 关键：带上 Google Referer！
            self.page.goto(category['url'], timeout=120000, referer="https://www.google.com/")
            self.page.wait_for_timeout(random_wait(10000, 15000))
            
            for _ in range(3):
                self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                self.page.wait_for_timeout(random_wait(3000, 5000))
            
            product_js = '''
                () => {
                    const products = [];
                    
                    // 从价格元素向上查找商品容器
                    const priceElements = Array.from(document.querySelectorAll('*')).filter(el => {
                        const text = el.innerText || el.textContent || '';
                        return text.includes('$') && /\\$\\d+\\.\\d+/.test(text);
                    });
                    
                    priceElements.forEach((priceEl) => {
                        try {
                            const text = priceEl.innerText.trim();
                            
                            if (text.includes('Orders') || text.includes('销售') || 
                                text.includes('客户支持') || text.includes('TikTok Shop')) {
                                return;
                            }
                            
                            let container = priceEl.parentElement;
                            let depth = 0;
                            
                            while (container && depth < 6) {
                                const nameEl = container.querySelector('h3');
                                const ratingEl = container.querySelector('span');
                                
                                if (nameEl && ratingEl) {
                                    const name = nameEl.innerText.trim();
                                    
                                    if (!name || name.length < 5 || name.includes('Orders')) {
                                        container = container.parentElement;
                                        depth++;
                                        continue;
                                    }
                                    
                                    const ratingMatch = ratingEl.innerText.match(/(\\d+\\.\\d+)/);
                                    const rating = ratingMatch ? parseFloat(ratingMatch[1]) : null;
                                    
                                    const soldEl = Array.from(container.querySelectorAll('span')).find(el => 
                                        el.innerText.includes('已售出')
                                    );
                                    const sold = soldEl ? soldEl.innerText.trim() : null;
                                    
                                    const priceMatch = text.match(/\\$(\\d+\\.\\d+)/);
                                    const price = priceMatch ? parseFloat(priceMatch[1]) : null;
                                    
                                    const linkEl = container.querySelector('a[href*="/pdp/"]');
                                    let tiktokshop_id = null;
                                    let product_url = null;
                                    
                                    if (linkEl && linkEl.href) {
                                        product_url = linkEl.href;
                                        const urlMatch = product_url.match(/\\/pdp\\/[^\\/]+\\/(\\d+)/);
                                        if (urlMatch) {
                                            tiktokshop_id = urlMatch[1];
                                        }
                                    }
                                    
                                    const imgEl = container.querySelector('img');
                                    const imageUrl = imgEl?.src || '';
                                    
                                    products.push({
                                        tiktokshop_id: tiktokshop_id,
                                        name: name,
                                        price: price,
                                        rating: rating,
                                        sold: sold,
                                        image_url: imageUrl,
                                        product_url: product_url
                                    });
                                    
                                    break;
                                }
                                
                                container = container.parentElement;
                                depth++;
                            }
                        } catch (e) {}
                    });
                    
                    const seen = new Set();
                    return products.filter(p => {
                        if (!p.tiktokshop_id || seen.has(p.tiktokshop_id)) return false;
                        seen.add(p.tiktokshop_id);
                        return true;
                    }).slice(0, 20);
                }
            '''
            
            products = self.page.evaluate(product_js)
            
            # 为每个商品添加正确的类目名称
            category_name = category['name']
            for p in products:
                p['category'] = category_name
            
        except Exception as e:
            print(f"[ERROR] 抓取失败: {e}")
        
        return products
    
    def save_products(self, category: Dict, products: List[Dict]) -> str:
        """保存商品数据"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        slug = category['name'].lower().replace(' ', '_').replace('&', 'and')[:30]
        filename = f"{self.platform}_{slug}_{timestamp}.json"
        filepath = SCRAPING_DIR / filename
        
        data = {
            "metadata": {
                "platform": self.platform,
                "category": category['name'],
                "category_id": category['id'],
                "task_id": self.task_id,
                "scraped_at": datetime.now().isoformat()
            },
            "products": products
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] 保存到: {filename}")
        return str(filepath)
    
    def import_to_db(self, json_file: str) -> bool:
        """导入数据到数据库"""
        import_script = BASE_DIR / 'skills' / 'db-importer' / 'src' / 'import_to_db.py'
        
        # 设置 UTF-8 环境
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'
        
        result = subprocess.run(
            ['python', str(import_script), '--file', json_file],
            capture_output=True,
            text=True,
            cwd=str(BASE_DIR),
            env=env,
            timeout=120,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0:
            print(f"[OK] 已导入数据库")
            return True
        else:
            print(f"[ERROR] 导入失败: {result.stderr}")
            return False
    
    def update_category_status(self, category_id: int, products_count: int):
        """更新类目抓取状态"""
        conn = get_db(CATEGORIES_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE categories
            SET last_scraped_at = ?,
                last_products_count = ?,
                total_scrapes = total_scrapes + 1,
                total_products = total_products + ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), products_count, products_count, category_id))
        
        conn.commit()
        conn.close()
        
        # 插入每日记录
        daily_conn = get_db(DAILY_DB)
        daily_cursor = daily_conn.cursor()
        
        daily_cursor.execute('''
            INSERT OR REPLACE INTO category_daily
            (category_id, date, products_count, task_id, scraped_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (category_id, date.today().isoformat(), products_count, self.task_id, datetime.now().isoformat()))
        
        daily_conn.commit()
        daily_conn.close()
    
    def run(self):
        """运行任务"""
        print(f"\n{'='*60}")
        print(f"任务开始: {self.task_id}")
        print(f"平台: {self.platform}")
        print(f"{'='*60}\n")
        
        self.update_db_status('running')
        
        categories = self.get_enabled_categories()
        
        if not categories:
            print("[WARN] 没有启用的类目")
            self.update_db_status('completed')
            return
        
        # 加载已完成的类目（续抓）
        if self.load_task():
            with open(self.task_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for saved_cat in data.get('categories', []):
                for cat in categories:
                    if cat['id'] == saved_cat['id']:
                        cat['status'] = saved_cat.get('status', 'pending')
                        break
        
        # 过滤需要抓取的类目
        to_fetch = [c for c in categories if c['status'] == 'pending']
        print(f"[INFO] 需要抓取 {len(to_fetch)} 个类目（跳过 {len(categories) - len(to_fetch)} 个）")
        
        if not to_fetch:
            print("[OK] 所有类目已完成")
            self.update_db_status('completed')
            return
        
        # 初始化浏览器
        print(f"[INFO] 正在启动浏览器...")
        self.init_browser()
        
        try:
            for i, cat in enumerate(to_fetch):
                print(f"\n[{i+1}/{len(to_fetch)}] {cat['name']}")
                
                if self.platform == 'amazon':
                    products = self.fetch_amazon_category(cat)
                else:
                    products = self.fetch_tiktok_category(cat)
                
                if products:
                    json_file = self.save_products(cat, products)
                    
                    if self.import_to_db(json_file):
                        # 导入脚本已经移动文件到 imported 目录，不需要再移动
                        pass
                    
                    self.update_category_status(cat['id'], len(products))
                    cat['status'] = 'done'
                else:
                    print(f"[WARN] 没有找到商品")
                    cat['status'] = 'failed'
                
                self.save_task(categories)
                
                if i < len(to_fetch) - 1:
                    wait = random_wait(3000, 8000)
                    print(f"[INFO] 等待 {wait}ms...")
                    time.sleep(wait / 1000)
            
            self.status = 'completed'
            self.save_task(categories)
            self.update_db_status('completed')
            
            print(f"\n{'='*60}")
            print(f"任务完成!")
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"[ERROR] 任务失败: {e}")
            self.status = 'failed'
            self.save_task(categories)
            self.update_db_status('failed', str(e))
        
        finally:
            self.close_browser()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='数据抓取任务')
    parser.add_argument('platform', choices=['amazon', 'tiktok'], help='平台名称')
    parser.add_argument('--task-id', help='续抓已有任务')
    args = parser.parse_args()
    
    print("=" * 60)
    print(f"[INFO] 开始 {args.platform} 数据抓取任务")
    print(f"[INFO] 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    task = FetchTask(args.platform, args.task_id)
    task.run()
    
    print("=" * 60)
    print(f"[INFO] 脚本结束")
    print("=" * 60)


if __name__ == "__main__":
    main()