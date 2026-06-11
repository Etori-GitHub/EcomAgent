"""
TikTok Shop 商品上传自动化模块
将 EcomAgent 货源数据上传到 TikTok Shop 商家后台
"""

import asyncio
import sqlite3
import logging
import subprocess
import socket
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from playwright.async_api import async_playwright, Page, BrowserContext

# 配置
BASE_DIR = Path(__file__).parent.parent
SOURCING_DB = BASE_DIR / "data" / "sourcing.db"
IMAGE_DIR = BASE_DIR / "data" / "images"
SCREENSHOT_DIR = BASE_DIR / "scripts" / "screenshots"

# TikTok Shop URL
PRODUCT_CREATE_URL = "https://seller.tiktokshopglobalselling.com/product/create?shop_region=VN"

# Chrome 配置
import platform

SYSTEM = platform.system()  # Windows / Darwin / Linux

if SYSTEM == "Windows":
    CHROME_PATHS = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        Path.home() / "AppData\\Local\\Google\\Chrome\\Application\\chrome.exe",
    ]
    TIKTOK_CHROME_DIR = Path("C:\\chrome-tiktok")
elif SYSTEM == "Darwin":  # macOS
    CHROME_PATHS = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    TIKTOK_CHROME_DIR = Path.home() / ".chrome-tiktok"
else:  # Linux
    CHROME_PATHS = [
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
    ]
    TIKTOK_CHROME_DIR = Path.home() / ".chrome-tiktok"

WEBUI_URL = "http://127.0.0.1:8000"
TIKTOK_LOGIN_URL = "https://seller.tiktokshopglobalselling.com/"

# 日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SourcingItem:
    """货源数据"""
    ecom_code: str
    offer_id: str
    title: str
    price: float
    local_image_path: str
    image_url: str
    shop_name: str
    description: Optional[str] = None


def check_port_in_use(port: int) -> bool:
    """检查端口是否在监听"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    except:
        return False


def find_chrome_path() -> Optional[Path]:
    """查找 Chrome 安装路径"""
    for path in CHROME_PATHS:
        p = Path(path) if isinstance(path, str) else path
        if p.exists():
            return p
    return None


def start_debug_chrome(port: int = 9222, open_webui: bool = True) -> bool:
    """启动调试 Chrome"""
    if check_port_in_use(port):
        logger.info(f"[TikTok] Chrome already running on port {port}")
        return True
    
    chrome_path = find_chrome_path()
    if not chrome_path:
        logger.error("[TikTok] Chrome not found")
        return False
    
    # 创建数据目录
    TIKTOK_CHROME_DIR.mkdir(parents=True, exist_ok=True)
    
    # 启动 Chrome，同时打开 WebUI
    try:
        args = [
            str(chrome_path),
            f"--remote-debugging-port={port}",
            f"--user-data-dir={TIKTOK_CHROME_DIR}",
        ]
        if open_webui:
            args.append(WEBUI_URL)
        
        subprocess.Popen(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        logger.info(f"[TikTok] Chrome started on port {port}, opened {WEBUI_URL}")
        # 等待启动
        import time
        for _ in range(10):
            if check_port_in_use(port):
                return True
            time.sleep(1)
        return False
    except Exception as e:
        logger.error(f"[TikTok] Failed to start Chrome: {e}")
        return False


class TikTokUploader:
    """TikTok Shop 商品上传器"""
    
    def __init__(self, cdp_port: int = 9222):
        self.cdp_port = cdp_port
        self.browser = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    async def connect(self, auto_start: bool = True) -> bool:
        """连接到 Chrome，可选自动启动"""
        # 先检测端口
        if not check_port_in_use(self.cdp_port):
            if auto_start:
                logger.info(f"[TikTok] Port {self.cdp_port} not in use, starting Chrome...")
                if not start_debug_chrome(self.cdp_port):
                    return False
            else:
                return False
        
        # 连接
        try:
            p = await async_playwright().start()
            self.browser = await p.chromium.connect_over_cdp(
                f"http://localhost:{self.cdp_port}",
                timeout=10000
            )
            self.context = self.browser.contexts[0]
            logger.info(f"[TikTok] Connected to Chrome (port {self.cdp_port})")
            return True
        except Exception as e:
            logger.error(f"[TikTok] Connection failed: {e}")
            return False
    
    async def get_or_create_page(self) -> Optional[Page]:
        """获取或创建商品创建页面"""
        if not self.context:
            return None
        
        # 查找现有页面
        for page in self.context.pages:
            if "product/create" in page.url:
                self.page = page
                return page
        
        # 创建新页面
        self.page = await self.context.new_page()
        await self.page.goto(PRODUCT_CREATE_URL, wait_until="domcontentloaded", timeout=30000)
        return self.page
    
    def get_sourcing_items(self, limit: int = 10) -> List[SourcingItem]:
        """获取货源数据"""
        if not SOURCING_DB.exists():
            logger.error(f"[TikTok] 货源数据库不存在: {SOURCING_DB}")
            return []
        
        conn = sqlite3.connect(SOURCING_DB)
        cursor = conn.execute("""
            SELECT ecom_code, offer_id, title, price, local_image_path, image_url, shop_name
            FROM sourcing_1688
            ORDER BY collected_at DESC
            LIMIT ?
        """, (limit,))
        
        items = []
        for row in cursor.fetchall():
            items.append(SourcingItem(
                ecom_code=row[0],
                offer_id=row[1],
                title=row[2],
                price=row[3],
                local_image_path=row[4],
                image_url=row[5],
                shop_name=row[6]
            ))
        
        conn.close()
        return items
    
    async def upload_image(self, image_path: Path) -> bool:
        """上传商品图片"""
        if not self.page:
            return False
        
        try:
            # 找到文件上传 input
            file_input = await self.page.query_selector("input[type='file'][accept*='.jpg']")
            if not file_input:
                file_input = await self.page.query_selector("input[type='file']")
            
            if file_input:
                await file_input.set_input_files(str(image_path))
                logger.info(f"[TikTok] 图片上传成功: {image_path.name}")
                await self.page.wait_for_timeout(2000)  # 等待上传完成
                return True
            else:
                logger.error("[TikTok] 找不到文件上传 input")
                return False
        except Exception as e:
            logger.error(f"[TikTok] 图片上传失败: {e}")
            return False
    
    async def fill_name(self, name: str) -> bool:
        """填入商品名称"""
        if not self.page:
            return False
        
        try:
            # 找到中文输入框
            name_input = await self.page.query_selector("input[placeholder*='请输入中文']")
            
            if name_input:
                # 清空并填入
                await name_input.click()
                await name_input.fill("")
                await name_input.fill(name[:100])
                logger.info(f"[TikTok] 商品名称已填入: {name[:30]}...")
                await self.page.wait_for_timeout(1000)  # 等待翻译
                return True
            else:
                logger.error("[TikTok] 找不到商品名称输入框")
                return False
        except Exception as e:
            logger.error(f"[TikTok] 填入名称失败: {e}")
            return False
    
    async def save_as_draft(self) -> bool:
        """保存为草稿"""
        if not self.page:
            return False
        
        try:
            # 查找保存草稿按钮
            buttons = await self.page.query_selector_all("button")
            for btn in buttons:
                text = await btn.inner_text()
                if "另存为草稿" in text or "保存" in text:
                    await btn.click()
                    logger.info("[TikTok] 已点击保存草稿")
                    await self.page.wait_for_timeout(3000)
                    return True
            
            logger.error("[TikTok] 找不到保存按钮")
            return False
        except Exception as e:
            logger.error(f"[TikTok] 保存失败: {e}")
            return False
    
    async def upload_item(self, item: SourcingItem) -> Dict[str, Any]:
        """上传单个商品"""
        result = {
            "ecom_code": item.ecom_code,
            "title": item.title,
            "success": False,
            "message": ""
        }
        
        # 检查图片
        image_path = IMAGE_DIR / item.local_image_path
        if not image_path.exists():
            result["message"] = f"图片不存在: {image_path}"
            return result
        
        # 获取页面
        page = await self.get_or_create_page()
        if not page:
            result["message"] = "无法获取页面"
            return result
        
        # 刷新页面（清除之前的数据）
        await page.reload(wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)
        
        # 上传图片
        if not await self.upload_image(image_path):
            result["message"] = "图片上传失败"
            return result
        
        # 填入名称
        if not await self.fill_name(item.title):
            result["message"] = "名称填入失败"
            return result
        
        # 保存草稿
        if not await self.save_as_draft():
            result["message"] = "保存草稿失败"
            return result
        
        result["success"] = True
        result["message"] = "上传成功"
        return result
    
    async def upload_batch(self, items: List[SourcingItem]) -> List[Dict[str, Any]]:
        """批量上传商品"""
        results = []
        for item in items:
            result = await self.upload_item(item)
            results.append(result)
            await asyncio.sleep(2)  # 间隔
        return results


# FastAPI 接口
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/tiktok", tags=["tiktok"])


@router.get("/status")
async def get_tiktok_status():
    """获取 TikTok Shop 连接状态"""
    uploader = TikTokUploader()
    connected = await uploader.connect(auto_start=True)
    return {
        "connected": connected,
        "cdp_port": uploader.cdp_port
    }


@router.post("/ensure-chrome")
async def ensure_chrome_running():
    """确保 Chrome 调试浏览器已启动"""
    if check_port_in_use(9222):
        return {"status": "already_running", "port": 9222}
    
    if start_debug_chrome(9222):
        return {"status": "started", "port": 9222}
    
    raise HTTPException(500, "Failed to start Chrome")


@router.post("/open-login")
async def open_tiktok_login():
    """打开 TikTok Shop 登录页面"""
    uploader = TikTokUploader()
    
    if not await uploader.connect(auto_start=True):
        raise HTTPException(500, "无法启动或连接 Chrome")
    
    # 打开登录页面
    page = await uploader.context.new_page()
    await page.goto("https://seller.tiktokshopglobalselling.com/", wait_until="domcontentloaded")
    
    return {"status": "opened", "url": "https://seller.tiktokshopglobalselling.com/"}


@router.get("/sourcing")
async def get_sourcing_list(limit: int = 10):
    """获取待上传的货源列表"""
    uploader = TikTokUploader()
    items = uploader.get_sourcing_items(limit)
    return {
        "total": len(items),
        "items": [
            {
                "ecom_code": item.ecom_code,
                "title": item.title,
                "price": item.price,
                "shop_name": item.shop_name,
                "has_image": bool(item.local_image_path)
            }
            for item in items
        ]
    }


@router.post("/upload/{ecom_code}")
async def upload_single_item(ecom_code: str):
    """上传单个商品"""
    uploader = TikTokUploader()
    
    if not await uploader.connect():
        raise HTTPException(500, "无法连接到 Chrome")
    
    items = uploader.get_sourcing_items(limit=100)
    target = next((item for item in items if item.ecom_code == ecom_code), None)
    
    if not target:
        raise HTTPException(404, f"货源不存在: {ecom_code}")
    
    result = await uploader.upload_item(target)
    return result


@router.post("/upload-batch")
async def upload_batch_items(limit: int = 5):
    """批量上传商品"""
    uploader = TikTokUploader()
    
    if not await uploader.connect():
        raise HTTPException(500, "无法连接到 Chrome")
    
    items = uploader.get_sourcing_items(limit)
    if not items:
        raise HTTPException(404, "没有待上传的货源")
    
    results = await uploader.upload_batch(items)
    return {
        "total": len(results),
        "success": sum(1 for r in results if r["success"]),
        "failed": sum(1 for r in results if not r["success"]),
        "results": results
    }


if __name__ == "__main__":
    # 测试
    async def test():
        uploader = TikTokUploader()
        if await uploader.connect():
            items = uploader.get_sourcing_items(1)
            if items:
                result = await uploader.upload_item(items[0])
                print(result)
    
    asyncio.run(test())