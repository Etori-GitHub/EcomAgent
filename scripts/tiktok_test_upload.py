"""
TikTok Shop 商品上传 - 实际测试上传图片
"""

import asyncio
import sys
import sqlite3
from pathlib import Path
from playwright.async_api import async_playwright

# TikTok Shop 商家后台 URL
PRODUCT_CREATE_URL = "https://seller.tiktokshopglobalselling.com/product/create?shop_region=VN"

# 货源数据
BASE_DIR = Path(__file__).parent.parent
SOURCING_DB = BASE_DIR / "data" / "sourcing.db"
IMAGE_DIR = BASE_DIR / "data" / "images"


async def main():
    """测试上传图片"""
    # 获取货源数据
    conn = sqlite3.connect(SOURCING_DB)
    cursor = conn.execute("""
        SELECT ecom_code, offer_id, title, price, local_image_path, image_url, shop_name
        FROM sourcing_1688 
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        print("[错误] 货源数据库为空")
        return
    
    ecom_code, offer_id, title, price, local_image_path, image_url, shop_name = row
    print(f"[货源] ecom_code: {ecom_code}")
    print(f"[货源] 标题: {title}")
    print(f"[货源] 价格: {price}")
    print(f"[货源] 本地图片: {local_image_path}")
    
    # 获取本地图片路径
    if local_image_path:
        image_path = IMAGE_DIR / local_image_path
    else:
        print("[错误] 没有本地图片")
        return
    
    if not image_path.exists():
        print(f"[错误] 图片不存在: {image_path}")
        return
    
    print(f"[货源] 图片路径: {image_path}")
    
    async with async_playwright() as p:
        # 连接到已运行的 Chrome
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            print(f"[错误] 无法连接到 Chrome: {e}")
            return
        
        print(f"[TikTok] 已连接到 Chrome")
        
        # 获取第一个上下文
        context = browser.contexts[0]
        
        # 找到商品创建页面或创建新页面
        target_page = None
        for page in context.pages:
            if "product/create" in page.url:
                target_page = page
                break
        
        if not target_page:
            target_page = await context.new_page()
            await target_page.goto(PRODUCT_CREATE_URL, wait_until="domcontentloaded", timeout=30000)
        
        print(f"[TikTok] 当前页面: {target_page.url}")
        
        # 等待页面加载
        await target_page.wait_for_timeout(3000)
        
        # 截图 - 上传前
        await target_page.screenshot(path=str(BASE_DIR / "scripts" / "before_upload.png"))
        print("[TikTok] 截图: before_upload.png")
        
        # ===== 步骤1: 上传图片 =====
        print("\n[步骤1] 上传商品图片...")
        
        # 找到第一个文件上传 input（商品主图）
        file_input = await target_page.query_selector("input[type='file'][accept*='.jpg']")
        
        if file_input:
            # 上传图片
            await file_input.set_input_files(str(image_path))
            print(f"[TikTok] 已上传图片: {image_path.name}")
            
            # 等待上传完成
            await target_page.wait_for_timeout(3000)
            
            # 截图 - 上传后
            await target_page.screenshot(path=str(BASE_DIR / "scripts" / "after_upload.png"))
            print("[TikTok] 截图: after_upload.png")
        else:
            print("[错误] 找不到文件上传 input")
        
        # ===== 步骤2: 填入商品名称 =====
        print("\n[步骤2] 填入商品名称...")
        
        # 查找商品名称输入框（中文）
        # 通常在页面左侧，有 "请输入中文" 的 placeholder
        name_inputs = await target_page.query_selector_all("input[type='text'], textarea")
        
        for inp in name_inputs:
            try:
                placeholder = await inp.get_attribute("placeholder") or ""
                cls = await inp.get_attribute("class") or ""
                if "中文" in placeholder or "请输入" in placeholder:
                    print(f"[TikTok] 找到名称输入框: placeholder='{placeholder}'")
                    await inp.fill(title[:100])  # 限制长度
                    print(f"[TikTok] 已填入标题: {title[:50]}...")
                    break
            except:
                pass
        
        # 截图 - 填入名称后
        await target_page.screenshot(path=str(BASE_DIR / "scripts" / "after_name.png"))
        print("[TikTok] 截图: after_name.png")
        
        # ===== 步骤3: 查找保存按钮 =====
        print("\n[步骤3] 查找保存草稿按钮...")
        
        buttons = await target_page.query_selector_all("button")
        for btn in buttons:
            try:
                text = await btn.inner_text()
                if "保存" in text or "草稿" in text:
                    print(f"[TikTok] 找到按钮: '{text}'")
            except:
                pass
        
        print("\n[完成] 测试结束。请在浏览器中检查结果。")
        print("[提示] 按 Enter 退出...")
        sys.stdin.readline()


if __name__ == "__main__":
    asyncio.run(main())