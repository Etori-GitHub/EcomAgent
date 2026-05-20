#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片处理模块
功能：
1. 下载图片
2. 等比压缩（长宽≤1024px，大小≤300KB）
3. 保存到本地
4. 记录图片变更历史
"""

import hashlib
import httpx
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image
import io


class ImageProcessor:
    """图片处理器"""
    
    MAX_SIZE = 1024  # 最大边长
    MAX_FILE_SIZE = 300 * 1024  # 300KB
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.images_dir = base_dir / "data" / "images"
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建平台子目录
        (self.images_dir / "amazon").mkdir(exist_ok=True)
        (self.images_dir / "tiktok").mkdir(exist_ok=True)
    
    def download_image(self, url: str, timeout: int = 30) -> Optional[bytes]:
        """下载图片"""
        if not url:
            return None
        
        try:
            with httpx.Client(timeout=timeout, follow_redirects=True) as client:
                # 添加 User-Agent 避免被拒绝
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                }
                response = client.get(url, headers=headers)
                if response.status_code == 200:
                    return response.content
        except Exception as e:
            print(f"[WARN] 下载图片失败: {url[:50]}... - {e}")
        
        return None
    
    def compress_image(self, image_data: bytes) -> Optional[bytes]:
        """压缩图片：等比缩放 + 质量压缩"""
        try:
            # 打开图片
            img = Image.open(io.BytesIO(image_data))
            
            # 转换为 RGB（处理 RGBA/P 等模式）
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # 等比缩放
            width, height = img.size
            if width > self.MAX_SIZE or height > self.MAX_SIZE:
                # 计算缩放比例
                ratio = min(self.MAX_SIZE / width, self.MAX_SIZE / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)
                print(f"[INFO] 图片缩放: {width}x{height} -> {new_width}x{new_height}")
            
            # 质量压缩
            output = io.BytesIO()
            quality = 85
            img.save(output, format='JPEG', quality=quality, optimize=True)
            
            # 如果还是太大，继续降低质量
            while output.tell() > self.MAX_FILE_SIZE and quality > 20:
                output = io.BytesIO()
                quality -= 10
                img.save(output, format='JPEG', quality=quality, optimize=True)
            
            print(f"[INFO] 图片压缩: 原始 {len(image_data)//1024}KB -> 压缩后 {output.tell()//1024}KB (质量={quality})")
            
            return output.getvalue()
            
        except Exception as e:
            print(f"[WARN] 压缩图片失败: {e}")
            return None
    
    def save_image(
        self, 
        platform: str, 
        platform_id: str, 
        image_url: str,
        timestamp: Optional[str] = None
    ) -> Optional[str]:
        """
        下载并保存图片
        
        Args:
            platform: 平台名称 (amazon/tiktok)
            platform_id: 平台商品 ID
            image_url: 图片 URL
            timestamp: 时间戳（可选，默认当前时间）
        
        Returns:
            本地图片路径（相对路径），失败返回 None
        """
        if not image_url:
            return None
        
        # 下载图片
        image_data = self.download_image(image_url)
        if not image_data:
            return None
        
        # 压缩图片
        compressed_data = self.compress_image(image_data)
        if not compressed_data:
            return None
        
        # 生成文件名
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        filename = f"{platform}_{platform_id}_{timestamp}.jpg"
        relative_path = f"{platform}/{filename}"
        full_path = self.images_dir / platform / filename
        
        # 保存文件
        with open(full_path, 'wb') as f:
            f.write(compressed_data)
        
        print(f"[OK] 图片已保存: {relative_path}")
        return relative_path
    
    def get_image_url_hash(self, image_url: str) -> str:
        """计算图片 URL 的哈希值（用于快速比较）"""
        if not image_url:
            return ""
        return hashlib.md5(image_url.encode()).hexdigest()


class ImageChangeTracker:
    """图片变更追踪器"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 图片变更记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS image_changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                platform_id TEXT NOT NULL,
                old_image_url TEXT,
                new_image_url TEXT NOT NULL,
                old_local_path TEXT,
                new_local_path TEXT NOT NULL,
                change_date TEXT NOT NULL,
                change_time TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_image_changes_platform_id 
            ON image_changes(platform, platform_id)
        """)
        
        conn.commit()
        conn.close()
    
    def record_change(
        self,
        platform: str,
        platform_id: str,
        old_image_url: Optional[str],
        new_image_url: str,
        old_local_path: Optional[str],
        new_local_path: str,
        change_date: Optional[str] = None,
        change_time: Optional[str] = None
    ):
        """记录图片变更"""
        if change_date is None:
            change_date = datetime.now().strftime("%Y-%m-%d")
        if change_time is None:
            change_time = datetime.now().strftime("%H:%M:%S")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO image_changes 
            (platform, platform_id, old_image_url, new_image_url, old_local_path, new_local_path, change_date, change_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (platform, platform_id, old_image_url, new_image_url, old_local_path, new_local_path, change_date, change_time))
        
        conn.commit()
        conn.close()
        
        print(f"[INFO] 图片变更已记录: {platform}_{platform_id} @ {change_date} {change_time}")
    
    def get_current_image(self, platform: str, platform_id: str) -> Optional[Tuple[str, str]]:
        """
        获取当前图片信息
        
        Returns:
            (image_url, local_path) 或 None
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 从商品表获取当前图片信息
        if platform == 'amazon':
            cursor.execute("""
                SELECT image_url, local_image_path FROM products 
                WHERE asin = ?
            """, (platform_id,))
        elif platform == 'tiktok':
            cursor.execute("""
                SELECT image_url, local_image_path FROM tiktok_products 
                WHERE tiktokshop_id = ?
            """, (platform_id,))
        else:
            conn.close()
            return None
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return (result[0], result[1])
        return None
    
    def get_change_history(self, platform: str, platform_id: str, limit: int = 10) -> list:
        """获取图片变更历史"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT change_date, change_time, old_image_url, new_image_url, old_local_path, new_local_path
            FROM image_changes
            WHERE platform = ? AND platform_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (platform, platform_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'change_date': r[0],
                'change_time': r[1],
                'old_image_url': r[2],
                'new_image_url': r[3],
                'old_local_path': r[4],
                'new_local_path': r[5]
            }
            for r in results
        ]
