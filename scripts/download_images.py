#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片下载脚本 - 后台异步下载商品图片到本地
"""

import sqlite3
import urllib.request
import time
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = DATA_DIR / "images"

# 图片保存目录
AMAZON_IMG_DIR = IMAGES_DIR / "amazon"
TIKTOK_IMG_DIR = IMAGES_DIR / "tiktok"
AMAZON_IMG_DIR.mkdir(parents=True, exist_ok=True)
TIKTOK_IMG_DIR.mkdir(parents=True, exist_ok=True)


def download_image(url: str, save_path: Path, referer: str = 'https://www.amazon.com/') -> bool:
    """下载单张图片"""
    if save_path.exists():
        return True
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': referer,
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
        
        with open(save_path, 'wb') as f:
            f.write(data)
        
        return True
    except Exception as e:
        print(f"  下载失败: {e}")
        return False


def download_amazon_images(limit: int = 0):
    """下载 Amazon 商品图片"""
    db_path = DATA_DIR / "amazon.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查询需要下载图片的商品
    if limit > 0:
        cursor.execute('''
            SELECT id, asin, image_url 
            FROM products 
            WHERE image_url IS NOT NULL AND image_url != ''
              AND (local_image_path IS NULL OR local_image_path = '')
            LIMIT ?
        ''', (limit,))
    else:
        cursor.execute('''
            SELECT id, asin, image_url 
            FROM products 
            WHERE image_url IS NOT NULL AND image_url != ''
              AND (local_image_path IS NULL OR local_image_path = '')
        ''')
    
    items = cursor.fetchall()
    total = len(items)
    
    if total == 0:
        print("[OK] Amazon 没有需要下载的图片")
        conn.close()
        return 0, 0
    
    print(f"[INFO] Amazon: 找到 {total} 个商品需要下载图片")
    
    success = 0
    failed = 0
    
    for i, (item_id, asin, image_url) in enumerate(items):
        if not image_url:
            continue
        
        # 从 URL 获取扩展名
        ext = '.jpg'
        url_lower = image_url.lower()
        if '.png' in url_lower:
            ext = '.png'
        elif '.webp' in url_lower:
            ext = '.webp'
        elif '.gif' in url_lower:
            ext = '.gif'
        
        filename = f"amazon_{asin}{ext}"
        save_path = AMAZON_IMG_DIR / filename
        relative_path = f"amazon/{filename}"
        
        print(f"[{i+1}/{total}] {asin}...", end='', flush=True)
        
        if download_image(image_url, save_path, 'https://www.amazon.com/'):
            cursor.execute('UPDATE products SET local_image_path = ? WHERE id = ?', (relative_path, item_id))
            conn.commit()
            print(" OK")
            success += 1
        else:
            failed += 1
        
        time.sleep(0.3)
    
    conn.close()
    print(f"[OK] Amazon 完成: 成功 {success}, 失败 {failed}")
    return success, failed


def download_tiktok_images(limit: int = 0):
    """下载 TikTok 商品图片"""
    db_path = DATA_DIR / "tiktok.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    if limit > 0:
        cursor.execute('''
            SELECT id, tiktokshop_id, image_url 
            FROM tiktok_products 
            WHERE image_url IS NOT NULL AND image_url != ''
              AND (local_image_path IS NULL OR local_image_path = '')
            LIMIT ?
        ''', (limit,))
    else:
        cursor.execute('''
            SELECT id, tiktokshop_id, image_url 
            FROM tiktok_products 
            WHERE image_url IS NOT NULL AND image_url != ''
              AND (local_image_path IS NULL OR local_image_path = '')
        ''')
    
    items = cursor.fetchall()
    total = len(items)
    
    if total == 0:
        print("[OK] TikTok 没有需要下载的图片")
        conn.close()
        return 0, 0
    
    print(f"[INFO] TikTok: 找到 {total} 个商品需要下载图片")
    
    success = 0
    failed = 0
    
    for i, (item_id, tiktok_id, image_url) in enumerate(items):
        if not image_url:
            continue
        
        ext = '.jpg'
        url_lower = image_url.lower()
        if '.png' in url_lower:
            ext = '.png'
        elif '.webp' in url_lower:
            ext = '.webp'
        
        filename = f"tiktok_{tiktok_id}{ext}"
        save_path = TIKTOK_IMG_DIR / filename
        relative_path = f"tiktok/{filename}"
        
        print(f"[{i+1}/{total}] {tiktok_id}...", end='', flush=True)
        
        if download_image(image_url, save_path, 'https://www.tiktok.com/'):
            cursor.execute('UPDATE tiktok_products SET local_image_path = ? WHERE id = ?', (relative_path, item_id))
            conn.commit()
            print(" OK")
            success += 1
        else:
            failed += 1
        
        time.sleep(0.3)
    
    conn.close()
    print(f"[OK] TikTok 完成: 成功 {success}, 失败 {failed}")
    return success, failed


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='下载商品图片')
    parser.add_argument('platform', nargs='?', default='all', choices=['amazon', 'tiktok', 'all'], help='平台')
    parser.add_argument('--limit', type=int, default=0, help='下载数量限制（0=全部）')
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"图片下载脚本")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    if args.platform in ['amazon', 'all']:
        download_amazon_images(args.limit)
    
    if args.platform in ['tiktok', 'all']:
        download_tiktok_images(args.limit)
    
    print(f"\n{'='*60}")
    print(f"全部完成")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
