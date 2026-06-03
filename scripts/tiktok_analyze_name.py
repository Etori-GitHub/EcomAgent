"""
TikTok Shop 商品上传 - 深度分析名称输入框
"""

import asyncio
import sys
import sqlite3
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).parent.parent
SOURCING_DB = BASE_DIR / "data" / "sourcing.db"
IMAGE_DIR = BASE_DIR / "data" / "images"


async def main():
    # 获取货源数据
    conn = sqlite3.connect(SOURCING_DB)
    cursor = conn.execute("""
        SELECT ecom_code, offer_id, title, price, local_image_path, image_url, shop_name
        FROM sourcing_1688 LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        print("[错误] 货源数据库为空")
        return
    
    ecom_code, offer_id, title, price, local_image_path, image_url, shop_name = row
    print(f"[货源] 标题: {title}")
    
    image_path = IMAGE_DIR / local_image_path
    if not image_path.exists():
        print(f"[错误] 图片不存在: {image_path}")
        return
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        print(f"[TikTok] 已连接到 Chrome")
        
        context = browser.contexts[0]
        
        # 找到商品创建页面
        target_page = None
        for page in context.pages:
            if "product/create" in page.url:
                target_page = page
                break
        
        if not target_page:
            print("[错误] 找不到商品创建页面")
            return
        
        print(f"[TikTok] 当前页面: {target_page.url}")
        await target_page.wait_for_timeout(2000)
        
        # 深度分析所有输入框
        print("\n" + "="*60)
        print("[分析] 所有 input 和 textarea 元素")
        print("="*60)
        
        all_inputs = await target_page.query_selector_all("input, textarea")
        for i, inp in enumerate(all_inputs):
            try:
                tag = await inp.evaluate("el => el.tagName")
                inp_type = await inp.get_attribute("type") or ""
                placeholder = await inp.get_attribute("placeholder") or ""
                name = await inp.get_attribute("name") or ""
                cls = await inp.get_attribute("class") or ""
                value = await inp.input_value() if tag == "INPUT" else ""
                
                print(f"\n[{i}] <{tag.lower()}>")
                print(f"    type: {inp_type}")
                print(f"    placeholder: {placeholder[:50]}")
                print(f"    name: {name}")
                print(f"    class: {cls[:60]}...")
                print(f"    value: {value[:30]}")
            except Exception as e:
                print(f"\n[{i}] 读取失败: {e}")
        
        # 查找商品名称区域
        print("\n" + "="*60)
        print("[分析] 查找商品名称输入区域")
        print("="*60)
        
        # 方法1: 查找包含 "商品名称" 文本的标签
        labels = await target_page.query_selector_all("label, .label, .title")
        for label in labels:
            try:
                text = await label.inner_text()
                if "名称" in text or "商品" in text:
                    print(f"[标签] '{text}'")
            except:
                pass
        
        # 方法2: 查找可编辑的 div（富文本编辑器）
        editable_divs = await target_page.query_selector_all("div[contenteditable='true']")
        print(f"\n[发现] {len(editable_divs)} 个可编辑 div")
        for i, div in enumerate(editable_divs[:5]):
            try:
                inner_text = await div.inner_text()
                placeholder_attr = await div.get_attribute("data-placeholder") or ""
                cls = await div.get_attribute("class") or ""
                print(f"  [{i}] inner_text: '{inner_text[:30]}'")
                print(f"      data-placeholder: '{placeholder_attr}'")
                print(f"      class: '{cls[:50]}'")
            except:
                pass
        
        # 方法3: 尝试直接点击并输入
        print("\n" + "="*60)
        print("[测试] 尝试填入商品名称")
        print("="*60)
        
        # 截图 - 当前状态
        await target_page.screenshot(path=str(BASE_DIR / "scripts" / "name_before.png"))
        
        # 尝试找到名称输入框（通过 placeholder 或 aria-label）
        name_input = await target_page.query_selector("input[placeholder*='名称'], input[placeholder*='中文'], input[aria-label*='名称']")
        
        if name_input:
            print("[找到] 名称输入框")
            await name_input.click()
            await target_page.wait_for_timeout(500)
            await name_input.fill("")  # 清空
            await name_input.fill(title[:80])
            print(f"[填入] {title[:50]}...")
        else:
            print("[尝试] 通过坐标点击...")
            # 根据截图，名称输入框大约在左上角区域
            # 点击可能的位置
            await target_page.mouse.click(400, 300)
            await target_page.wait_for_timeout(500)
            await target_page.keyboard.type(title[:50], delay=50)
            print(f"[输入] {title[:50]}...")
        
        await target_page.wait_for_timeout(2000)
        await target_page.screenshot(path=str(BASE_DIR / "scripts" / "name_after.png"))
        print("\n[截图] name_before.png, name_after.png")
        
        print("\n[完成] 按Enter退出")
        sys.stdin.readline()


if __name__ == "__main__":
    asyncio.run(main())