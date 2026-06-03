# TikTok Shop 商品上传自动化开发文档

> 本文档记录了通过 Playwright CDP 协议连接已打开浏览器、自动化上传商品到 TikTok Shop 的完整开发过程。

## 一、技术背景

### 1.1 问题场景
EcomAgent 项目需要将 1688 货源信息一键上传到 TikTok Shop 商家后台。

### 1.2 技术选型决策
**选择浏览器自动化而非 API 调用的原因：**

| 方案 | 优点 | 缺点 |
|------|------|------|
| TikTok Shop API | 官方接口，稳定 | 签名参数复杂，认证流程繁琐，需要申请开发者权限 |
| 浏览器自动化 | 无需 API 权限，直观可控 | 需要处理页面变化，依赖浏览器状态 |

**最终选择：Playwright CDP 协议连接已打开的浏览器**

### 1.3 核心技术点
- **CDP (Chrome DevTools Protocol)**: 通过调试端口远程控制 Chrome
- **CDP 连接优势**:
  - 可以使用已登录的浏览器 session（无需重新登录）
  - 复用已有的 cookies 和认证状态
  - 避免自动化检测（使用真实用户浏览器）

---

## 二、Chrome 启动与 CDP 连接

### 2.1 启动 Chrome 并开启调试端口

**Windows 启动命令：**
```powershell
# 使用独立用户数据目录（避免污染主浏览器）
chrome --remote-debugging-port=9222 --user-data-dir=C:\Users\Etroi\.openclaw\chrome-tiktok

# 或者使用已有的 Chrome 实例
chrome.exe --remote-debugging-port=9222
```

**关键参数说明：**
- `--remote-debugging-port=9222`: 开启调试端口，允许外部程序连接
- `--user-data-dir`: 指定独立的用户数据目录，用于隔离 session

### 2.2 CDP 连接验证

**检查调试端口是否开启：**
```bash
curl http://localhost:9222/json/version
```

**返回示例：**
```json
{
  "Browser": "Chrome/125.0.0.0",
  "webSocketDebuggerUrl": "ws://localhost:9222/devtools/browser/xxx-xxx"
}
```

### 2.3 Playwright CDP 连接代码

```python
from playwright.async_api import async_playwright

async def connect_to_chrome(cdp_port: int = 9222):
    """连接到已运行的 Chrome"""
    p = await async_playwright().start()
    browser = await p.chromium.connect_over_cdp(
        f"http://localhost:{cdp_port}",
        timeout=10000
    )
    
    # 获取已有 context（包含登录状态）
    context = browser.contexts[0]
    
    # 获取已有页面或创建新页面
    pages = context.pages
    # 或创建新页面
    page = await context.new_page()
    
    return browser, context, page
```

**注意事项：**
- `connect_over_cdp()` 不需要启动新浏览器
- `browser.contexts[0]` 获取已有的浏览器上下文（包含 cookies）
- 无需重新登录 TikTok Shop

---

## 三、TikTok Shop 商品创建页面分析

### 3.1 目标页面 URL
```
https://seller.tiktokshopglobalselling.com/product/create?shop_region=VN
```

### 3.2 页面元素分析结果

通过 Playwright 调试脚本分析页面结构：

```python
# 分析脚本示例
async def analyze_page(page):
    """分析页面元素结构"""
    elements = await page.query_selector_all("input, button, [contenteditable]")
    
    for i, el in enumerate(elements):
        tag = await el.evaluate("el => el.tagName")
        placeholder = await el.evaluate("el => el.placeholder || ''")
        text = await el.evaluate("el => el.innerText?.substring(0, 30) || ''")
        
        print(f"[{i}] {tag}: placeholder='{placeholder}', text='{text}'")
```

**关键元素定位结果：**

| 功能 | 选择器 | 说明 |
|------|--------|------|
| 图片上传 | `input[type='file'][accept*='.jpg']` | 隐藏的 file input |
| 商品名称(中文) | `input[placeholder*='请输入中文']` | 中文输入框，自动翻译 |
| 商品名称(越南语) | `input[placeholder*='翻译为越南语']` | 翻译结果展示 |
| 商品详情 | `div.ProseMirror` (contenteditable) | 富文本编辑器 |
| 保存草稿 | `button` (innerText: '另存为草稿') | 草稿按钮 |

### 3.3 图片上传机制

**TikTok Shop 图片上传方式：**

方式 A：直接在商品创建页面上传
```python
# 直接上传（推荐）
file_input = await page.query_selector("input[type='file'][accept*='.jpg']")
await file_input.set_input_files(str(image_path))
```

方式 B：先上传到媒体中心，再引用
```python
# 需要先访问媒体中心页面
await page.goto("https://seller.tiktokshopglobalselling.com/media")
# 上传到媒体库后再引用
```

**测试结论：方式 A 可行，无需预上传到媒体库**

---

## 四、完整实现代码

### 4.1 数据结构定义

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class SourcingItem:
    """货源商品数据"""
    ecom_code: str          # 商品编码 (ECTK26000401)
    offer_id: str           # 1688 商品ID
    title: str              # 商品标题
    price: float            # 价格
    local_image_path: Optional[Path]  # 本地图片路径
    image_url: str          # 原始图片URL
    shop_name: str          # 店铺名称
```

### 4.2 TikTokUploader 类

```python
import sqlite3
import asyncio
from playwright.async_api import Page, Browser, BrowserContext

class TikTokUploader:
    """TikTok Shop 商品上传器"""
    
    CDP_PORT = 9222
    PRODUCT_CREATE_URL = "https://seller.tiktokshopglobalselling.com/product/create?shop_region=VN"
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    async def connect(self) -> bool:
        """连接到已运行的 Chrome"""
        try:
            from playwright.async_api import async_playwright
            p = await async_playwright().start()
            self.browser = await p.chromium.connect_over_cdp(
                f"http://localhost:{self.CDP_PORT}",
                timeout=10000
            )
            self.context = self.browser.contexts[0]
            logger.info(f"[TikTok] 已连接到 Chrome (端口 {self.CDP_PORT})")
            return True
        except Exception as e:
            logger.error(f"[TikTok] 连接失败: {e}")
            return False
    
    async def get_or_create_page(self) -> Optional[Page]:
        """获取或创建商品创建页面"""
        if not self.context:
            return None
        
        # 查找现有页面（复用已打开的页面）
        for page in self.context.pages:
            if "product/create" in page.url:
                self.page = page
                return page
        
        # 创建新页面
        self.page = await self.context.new_page()
        await self.page.goto(self.PRODUCT_CREATE_URL, wait_until="domcontentloaded")
        return self.page
    
    async def upload_image(self, image_path: Path) -> bool:
        """上传商品图片"""
        if not self.page:
            return False
        
        try:
            file_input = await self.page.query_selector("input[type='file'][accept*='.jpg']")
            if not file_input:
                file_input = await self.page.query_selector("input[type='file']")
            
            if file_input:
                await file_input.set_input_files(str(image_path))
                await self.page.wait_for_timeout(2000)  # 等待上传完成
                return True
        except Exception as e:
            logger.error(f"[TikTok] 图片上传失败: {e}")
            return False
    
    async def fill_name(self, name: str) -> bool:
        """填入商品名称（中文，自动翻译为越南语）"""
        if not self.page:
            return False
        
        try:
            name_input = await self.page.query_selector("input[placeholder*='请输入中文']")
            if name_input:
                await name_input.click()
                await name_input.fill("")
                await name_input.fill(name[:100])  # 限制长度
                await self.page.wait_for_timeout(1000)  # 等待翻译
                return True
        except Exception as e:
            logger.error(f"[TikTok] 填入名称失败: {e}")
            return False
    
    async def save_as_draft(self) -> bool:
        """保存为草稿"""
        if not self.page:
            return False
        
        try:
            buttons = await self.page.query_selector_all("button")
            for btn in buttons:
                text = await btn.inner_text()
                if "另存为草稿" in text:
                    await btn.click()
                    await self.page.wait_for_timeout(3000)
                    return True
        except Exception as e:
            logger.error(f"[TikTok] 保存失败: {e}")
            return False
    
    async def upload_item(self, item: SourcingItem) -> dict:
        """上传单个商品"""
        result = {
            "success": False,
            "ecom_code": item.ecom_code,
            "title": item.title,
            "message": ""
        }
        
        try:
            # 1. 获取页面
            page = await self.get_or_create_page()
            if not page:
                result["message"] = "无法获取页面"
                return result
            
            # 2. 上传图片
            if item.local_image_path:
                image_path = Path(item.local_image_path)
                if image_path.exists():
                    if not await self.upload_image(image_path):
                        result["message"] = "图片上传失败"
                        return result
            
            # 3. 填入名称
            if not await self.fill_name(item.title):
                result["message"] = "名称填入失败"
                return result
            
            # 4. 保存草稿
            if not await self.save_as_draft():
                result["message"] = "保存草稿失败"
                return result
            
            result["success"] = True
            result["message"] = "上传成功"
            return result
            
        except Exception as e:
            result["message"] = str(e)
            return result
```

### 4.3 FastAPI 路由集成

```python
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/tiktok", tags=["TikTok"])

@router.get("/status")
async def get_tiktok_status():
    """检查 Chrome 连接状态"""
    uploader = TikTokUploader()
    connected = await uploader.connect()
    return {
        "connected": connected,
        "cdp_port": uploader.CDP_PORT
    }

@router.post("/upload/{ecom_code}")
async def upload_single_item(ecom_code: str):
    """上传单个商品"""
    uploader = TikTokUploader()
    
    if not await uploader.connect():
        raise HTTPException(500, "无法连接到 Chrome")
    
    # 从数据库获取货源信息
    items = uploader.get_sourcing_items(limit=100)
    target = next((item for item in items if item.ecom_code == ecom_code), None)
    
    if not target:
        raise HTTPException(404, f"货源不存在: {ecom_code}")
    
    result = await uploader.upload_item(target)
    return result
```

---

## 五、前端集成

### 5.1 货源库页面按钮

```typescript
// ui/src/pages/sourcing.ts

private async _uploadToTikTok(item: any) {
    console.log('[Sourcing] 开始上传到 TikTok:', item.ecom_code);
    
    // 检查连接状态
    const statusRes = await fetch('/api/tiktok/status');
    const status = await statusRes.json();
    
    if (!status.connected) {
        alert('未连接到 TikTok Shop\n请确保 Chrome 已启动并使用 --remote-debugging-port=9222 参数');
        return;
    }
    
    // 调用上传 API
    const response = await fetch(`/api/tiktok/upload/${item.ecom_code}`, { 
        method: 'POST' 
    });
    const result = await response.json();
    
    if (result.success) {
        alert('上传成功!\n请在 TikTok Shop 后台检查草稿商品');
    } else {
        alert(`上传失败: ${result.message}`);
    }
}
```

### 5.2 按钮样式

```css
.action-btn-tiktok {
    background: #ff0050;  /* TikTok 红色 */
    color: white;
    border: none;
}

.action-btn-tiktok:hover {
    opacity: 0.9;
}
```

---

## 六、关键问题解决记录

### 6.1 问题：confirm() 对话框不弹出

**现象：** 点击按钮后 `confirm()` 没有弹窗，直接被当作取消

**原因：** 浏览器可能阻止了原生 confirm 对话框，或 Playwright CDP 连接干扰

**解决：** 前端去掉 `confirm()` 确认，直接调用 API

### 6.2 问题：数据库列名错误

**现象：** `sqlite3.OperationalError: no such column: created_at`

**原因：** 数据库实际列名是 `collected_at`

**解决：** 修正 SQL 查询语句

### 6.3 问题：Playwright dialog 错误

**现象：** `Protocol error (Page.handleJavaScriptDialog): No dialog is showing`

**原因：** Playwright 在 CDP 连接时尝试处理不存在的前端 dialog

**影响：** 警告性错误，不影响功能，可忽略

---

## 七、使用流程

### 7.1 准备步骤

1. **启动 Chrome（带调试端口）：**
   ```powershell
   chrome --remote-debugging-port=9222 --user-data-dir=C:\Users\Etroi\.openclaw\chrome-tiktok
   ```

2. **在 Chrome 中登录 TikTok Shop：**
   - 打开 `https://seller.tiktokshopglobalselling.com`
   - 使用商家账号登录
   - 进入商品管理页面

3. **启动 EcomAgent 服务：**
   ```bash
   cd EcomAgent
   python run_viewer.py
   ```

### 7.2 操作流程

1. 打开 EcomAgent WebUI: `http://127.0.0.1:8000`
2. 进入「货源库」页面
3. 找到要上传的货源记录
4. 点击「TikTok」按钮
5. 等待上传完成提示
6. 在 TikTok Shop 后台检查草稿商品

---

## 八、扩展方向

### 8.1 待开发功能

- [ ] 商品详情描述填入（ProseMirror 编辑器）
- [ ] 多图片上传
- [ ] 视频上传
- [ ] 批量上传
- [ ] 类目自动选择

### 8.2 1688 插件增强

需要修改 1688 插件抓取商品详情描述：

```javascript
// content.js 增强版
const detailDesc = await page.evaluate(() => {
    // 抓取商品详情页的描述内容
    const descEl = document.querySelector('.desc-content');
    return descEl?.innerText || '';
});
```

---

## 九、技术要点总结

### 9.1 CDP 连接核心优势

| 优势 | 说明 |
|------|------|
| 复用登录状态 | 无需重新登录，使用已有 session |
| 避免检测 | 使用真实用户浏览器，不易被检测 |
| 调试方便 | 可以在浏览器中实时观察自动化过程 |
| 稳定可靠 | 页面结构变化时可以人工干预 |

### 9.2 元素定位策略

```python
# 优先使用 placeholder 属性定位
input[placeholder*='请输入中文']

# 其次使用 type 属性
input[type='file']

# 最后使用文本内容
button[contains(text(), '另存为草稿')]
```

### 9.3 等待策略

```python
# 等待上传完成
await page.wait_for_timeout(2000)

# 等待翻译完成
await page.wait_for_timeout(1000)

# 等待页面加载
await page.goto(url, wait_until="domcontentloaded")
```

---

## 十、文件结构

```
EcomAgent/
├── src/
│   ├── tiktok_uploader.py          # TikTok 上传核心模块
│   └── data_viewer/
│       └── main.py                 # FastAPI 路由集成
├── ui/
│   └── src/
│       └── pages/
│           └── sourcing.ts         # 货源库前端页面
├── data/
│   └── sourcing.db                 # 货源数据库
└── docs/
    └── TIKTOK-UPLOAD-DEVELOPMENT.md # 本文档
```

---

## 附录：Playwright CDP 调试技巧

### A.1 查看所有已连接页面

```python
pages = context.pages
for page in pages:
    print(f"Page URL: {page.url}")
```

### A.2 截图调试

```python
await page.screenshot(path="debug.png")
```

### A.3 执行 JavaScript

```python
result = await page.evaluate("""
    () => {
        return {
            title: document.title,
            url: window.location.href
        }
    }
""")
```

### A.4 监听网络请求

```python
page.on("response", lambda response: 
    print(f"Response: {response.url} - {response.status}")
)
```

---

**文档版本:** v1.0
**更新日期:** 2026-06-04
**开发者:** Kurisu (EcomAgent Team)