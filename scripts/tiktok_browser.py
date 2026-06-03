"""
TikTok Shop 商品上传 - 浏览器自动化 (深度分析版)
分析媒体中心页面的详细结构
"""

import asyncio
import sys
import json
from pathlib import Path
from playwright.async_api import async_playwright

# TikTok Shop 商家后台 URL
MATERIAL_CENTER_URL = "https://seller.tiktokshopglobalselling.com/product/materialSender?shop_region=VN"
PRODUCT_CREATE_URL = "https://seller.tiktokshopglobalselling.com/product/create?shop_region=VN"


async def analyze_page(page, page_name: str):
    """深度分析页面结构"""
    print(f"\n{'='*60}")
    print(f"[分析] {page_name}")
    print(f"{'='*60}")
    
    # 等待页面完全加载
    await page.wait_for_timeout(3000)
    
    # 获取页面 HTML 结构
    html = await page.content()
    html_path = Path(__file__).parent / f"{page_name}_html.txt"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html[:50000])  # 只保存前 50000 字符
    print(f"[分析] HTML 已保存: {html_path}")
    
    # 截图
    screenshot_path = Path(__file__).parent / f"{page_name}_screenshot.png"
    await page.screenshot(path=str(screenshot_path), full_page=False)
    print(f"[分析] 截图已保存: {screenshot_path}")
    
    # 分析所有可交互元素
    print("\n[元素分析]")
    
    # 按钮
    buttons = await page.query_selector_all("button")
    print(f"按钮: {len(buttons)} 个")
    for i, btn in enumerate(buttons[:10]):
        try:
            text = await btn.inner_text()
            cls = await btn.get_attribute("class") or ""
            print(f"  [{i}] '{text[:30]}' - class: {cls[:50]}")
        except:
            pass
    
    # 输入框
    inputs = await page.query_selector_all("input, textarea")
    print(f"\n输入框: {len(inputs)} 个")
    for i, inp in enumerate(inputs[:10]):
        try:
            type_ = await inp.get_attribute("type") or "text"
            placeholder = await inp.get_attribute("placeholder") or ""
            cls = await inp.get_attribute("class") or ""
            print(f"  [{i}] type={type_}, placeholder='{placeholder[:30]}' - class: {cls[:50]}")
        except:
            pass
    
    # 文件上传
    file_inputs = await page.query_selector_all("input[type='file']")
    print(f"\n文件上传: {len(file_inputs)} 个")
    for i, fi in enumerate(file_inputs):
        try:
            accept = await fi.get_attribute("accept") or ""
            name = await fi.get_attribute("name") or ""
            print(f"  [{i}] name='{name}', accept='{accept}'")
        except:
            pass
    
    # 带 upload/uploader 类名的元素
    upload_elems = await page.query_selector_all("[class*='upload'], [class*='Upload'], [class*='uploader']")
    print(f"\nUpload 类元素: {len(upload_elems)} 个")
    for i, el in enumerate(upload_elems[:10]):
        try:
            tag = await el.evaluate("el => el.tagName")
            cls = await el.get_attribute("class") or ""
            print(f"  [{i}] {tag} - class: {cls[:80]}")
        except:
            pass
    
    # 下拉选择框
    selects = await page.query_selector_all("select, [role='listbox'], [role='combobox']")
    print(f"\n选择框: {len(selects)} 个")
    for i, sel in enumerate(selects[:5]):
        try:
            tag = await sel.evaluate("el => el.tagName")
            cls = await sel.get_attribute("class") or ""
            print(f"  [{i}] {tag} - class: {cls[:50]}")
        except:
            pass
    
    # 查找导航菜单
    nav_items = await page.query_selector_all("[class*='menu'], [class*='nav'], [class*='sidebar']")
    print(f"\n导航元素: {len(nav_items)} 个")
    for i, nav in enumerate(nav_items[:5]):
        try:
            tag = await nav.evaluate("el => el.tagName")
            cls = await nav.get_attribute("class") or ""
            print(f"  [{i}] {tag} - class: {cls[:50]}")
        except:
            pass
    
    # 查找表格
    tables = await page.query_selector_all("table, [class*='table'], [class*='grid']")
    print(f"\n表格元素: {len(tables)} 个")
    
    # 查找弹窗/对话框
    modals = await page.query_selector_all("[class*='modal'], [class*='dialog'], [role='dialog']")
    print(f"\n弹窗元素: {len(modals)} 个")
    
    # 分析侧边栏菜单
    print("\n[侧边栏菜单]")
    sidebar_links = await page.query_selector_all("a[href*='/product/'], a[class*='menu']")
    for i, link in enumerate(sidebar_links[:10]):
        try:
            href = await link.get_attribute("href") or ""
            text = await link.inner_text()
            print(f"  [{i}] '{text[:20]}' -> {href[:50]}")
        except:
            pass


async def main():
    """连接到已运行的 Chrome 浏览器"""
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            print(f"[错误] 无法连接到 Chrome: {e}")
            return
        
        print(f"[TikTok] 已连接到 Chrome")
        
        # 获取第一个上下文
        context = browser.contexts[0]
        
        # 找到媒体中心页面或创建新页面
        target_page = None
        for page in context.pages:
            if "materialSender" in page.url:
                target_page = page
                break
        
        if not target_page:
            target_page = await context.new_page()
            await target_page.goto(MATERIAL_CENTER_URL, wait_until="domcontentloaded", timeout=30000)
        
        # 分析媒体中心页面
        await analyze_page(target_page, "material_center")
        
        # 尝试点击"上传"按钮并分析
        print("\n[尝试] 查找并点击上传按钮...")
        
        # 查找可能的创建/上传按钮
        create_buttons = await target_page.query_selector_all("button, [role='button'], a[class*='btn']")
        for btn in create_buttons:
            try:
                text = await btn.inner_text()
                if "上传" in text or "upload" in text.lower() or "create" in text.lower() or "创建" in text:
                    print(f"[发现] 按钮文本: '{text}'")
                    cls = await btn.get_attribute("class") or ""
                    print(f"[发现] class: {cls}")
            except:
                pass
        
        # 查找"添加商品"入口
        print("\n[查找] 商品管理页面入口...")
        
        # 访问商品创建页面
        create_page = await context.new_page()
        print(f"\n[访问] 商品创建页面: {PRODUCT_CREATE_URL}")
        try:
            await create_page.goto(PRODUCT_CREATE_URL, wait_until="domcontentloaded", timeout=30000)
            await analyze_page(create_page, "product_create")
        except Exception as e:
            print(f"[错误] 无法访问商品创建页面: {e}")
        
        print("\n" + "="*60)
        print("[完成] 分析结束。按 Enter 关闭...")
        print("="*60)
        sys.stdin.readline()


if __name__ == "__main__":
    asyncio.run(main())