# TikTok Shop API 参考

TikTok Shop 数据抓取相关 API 和页面结构参考。

---

## 页面 URL 结构

### 类目页面
- 旧格式：`https://shop.tiktok.com/shop/c/{category_id}`
- 新格式：`https://www.tiktok.com/c/{category_id}`

### 商品详情页
- 旧格式：`https://shop.tiktok.com/shop/pdp/{product_id}`
- 新格式：`https://www.tiktok.com/pdp/{product_id}`

---

## 商品 ID 提取

商品链接格式：`/pdp/{prefix}/{id}`

```python
import re

# 提取商品 ID
match = re.search(r'/pdp/[^/]+/(\d+)/', url)
if match:
    product_id = match.group(1)
```

---

## CDP 连接模式

### 启动 Chrome 调试端口

```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\xxx\chrome-debug-profile"
```

### Playwright 连接

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    context = browser.contexts[0]
    page = context.pages[0]  # 或 context.new_page()
    
    # 操作...
    
    # 不要关闭 browser
    page.close()
```

---

## 注意事项

1. TikTok 页面结构可能变化，需要定期检查选择器
2. 使用 CDP 模式时，不要调用 `browser.close()`
3. 建议使用独立的 Chrome Profile 避免冲突