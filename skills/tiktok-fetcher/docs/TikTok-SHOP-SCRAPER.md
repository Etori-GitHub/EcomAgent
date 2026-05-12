# TikTok Shop 抓取开发文档

## 项目背景

EcomAgent 项目已经实现了亚马逊热销榜单的数据抓取功能，现在需要扩展支持 TikTok Shop 的数据抓取。

## 技术方案

### 1. 核心架构

**Python + Playwright**：
- Python 负责控制浏览器和数据处理
- Playwright 负责浏览器自动化
- JavaScript 负责 DOM 操作和数据提取

### 2. 关键突破

#### 2.1 反机器人验证解决方案

**问题**：
- 新创建的 Chrome 实例会触发反机器人验证
- 无法自动登录谷歌账号

**解决方案**：
```python
browser = p.chromium.launch_persistent_context(
    user_data_dir=r"C:\Users\Etroi\AppData\Local\Google\Chrome\User Data\Profile 1",
    headless=False,
    slow_mo=500,
    args=[
        '--disable-blink-features=AutomationControlled',
        '--disable-web-security',
        '--allow-running-insecure-content'
    ]
)
```

**原理**：
- 复用已登录的 Chrome 配置文件
- 包含登录状态和 cookies
- 避免触发反机器人验证

#### 2.2 页面结构分析

**类目位置**：
```html
<h2 class="mb-20 H2-Bold">类目</h2>
```

**类目入口**：
```html
<div class="group flex flex-col items-center w-full h-full cursor-pointer" title="美妆个护">
```

**URL 格式**：
```
https://www.tiktok.com/shop/c/{slug}/{id}
```
例如：`https://www.tiktok.com/shop/c/beauty-personal-care/601450`

### 3. 数据提取流程

```
1. 访问首页 (https://www.tiktok.com/shop)
   ↓
2. 等待页面加载（包括图片）
   ↓
3. 滚动页面 5 次，加载更多内容
   ↓
4. 执行 JavaScript 提取类目列表
   ↓
5. 保存类目列表到 categories.json
   ↓
6. 逐个访问分类页面
   ↓
7. 提取商品数据
   ↓
8. 保存到 JSON 文件
```

### 4. 关键技术点

#### 4.1 等待机制

```python
# 初始等待
page.wait_for_timeout(random_wait(10000, 15000))

# 滚动等待
for i in range(5):
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(random_wait(3000, 5000))

# 最终等待
page.wait_for_timeout(random_wait(10000, 20000))
```

#### 4.2 DOM 操作

```javascript
// 提取类目
const categoryHeader = document.querySelector('h2.mb-20.H2-Bold');
const parent = categoryHeader.parentElement;
const allDivs = parent.querySelectorAll('div');

allDivs.forEach((div, idx) => {
    const title = div.getAttribute('title');
    const href = div.querySelector('a')?.href;
    
    if (title && className.includes('cursor-pointer')) {
        categories.push({ name: title, url: href });
    }
});
```

#### 4.3 商品提取

```javascript
// 查找包含价格的元素
const priceElements = Array.from(allElements).filter(el => {
    const text = el.innerText || el.textContent || '';
    return text.includes('$') || text.includes('¥');
});

// 提取商品信息
priceElements.forEach((el, idx) => {
    const text = el.innerText ? el.innerText.trim() : '';
    const priceMatch = text.match(/[$¥](\d+\.?\d*)/);
    const ratingMatch = text.match(/(\d+\.\d+)/);
    
    if (priceMatch) {
        products.push({
            text: text.substring(0, 200),
            price: priceMatch[1],
            rating: ratingMatch ? ratingMatch[1] : null
        });
    }
});
```

## 开发步骤

### 第一步：页面结构分析

1. 访问 TikTok Shop 首页
2. 使用浏览器开发者工具检查 HTML 结构
3. 记录关键元素的类名和选择器

**发现**：
- 类目标题：`h2.mb-20.H2-Bold`
- 类目入口：`div.cursor-pointer[title="xxx"]`
- URL 格式：`/shop/c/{slug}/{id}`

### 第二步：实现类目提取

使用 JavaScript 执行：
```python
categories = page.evaluate(category_js)
```

**结果**：成功提取 28 个类目

### 第三步：实现商品提取

访问分类页面，提取商品数据：
```python
products = page.evaluate(product_js)
```

**当前状态**：提取基础信息（名称、价格、评分）

### 第四步：优化和改进

**待优化**：
1. 优化商品选择器，提取更详细数据
2. 添加错误重试机制
3. 添加进度显示和日志记录
4. 支持翻页抓取

## 已知问题

### 1. 商品数据提取不完整

**原因**：
- TikTok Shop 的商品卡片结构复杂
- 当前选择器只提取基础信息

**解决方案**：
- 使用浏览器开发者工具检查实际商品卡片结构
- 调整 JavaScript 选择器
- 提取更详细的数据（销量、评论数等）

### 2. 页面加载时间

**原因**：
- TikTok Shop 页面包含大量图片
- 懒加载导致部分内容需要滚动后才加载

**解决方案**：
- 增加滚动次数
- 延长等待时间
- 使用 `page.wait_for_load_state('networkidle')`

### 3. 反爬机制

**原因**：
- TikTok Shop 有反爬虫机制
- 频繁访问可能触发限制

**解决方案**：
- 已添加随机等待
- 复用登录状态
- 建议在非高峰时段运行

## 扩展功能

### 1. 支持更多数据字段

当前提取：
- `tag`: HTML 标签名
- `className`: CSS 类名
- `text`: 文本内容
- `price`: 价格
- `rating`: 评分

**可扩展**：
- `name`: 商品名称
- `sold_count`: 销量
- `review_count`: 评论数
- `image_url`: 图片 URL
- `product_url`: 商品链接

### 2. 数据库导入

将 JSON 数据导入 SQLite 数据库：
```python
import sqlite3

conn = sqlite3.connect('tiktok_products.db')
cursor = conn.cursor()

# 创建表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        name TEXT,
        price REAL,
        rating REAL,
        scraped_at TIMESTAMP
    )
''')

# 插入数据
for product in products:
    cursor.execute('''
        INSERT INTO products (category, name, price, rating, scraped_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (category, product['name'], product['price'], product['rating'], datetime.now()))

conn.commit()
conn.close()
```

### 3. 定时任务

使用 OpenClaw cron 设置定时抓取：
```python
cron.add(job={
    "name": "TikTok Shop Daily Scrape",
    "schedule": {"kind": "cron", "expr": "0 9 * * *"},  # 每天 9 点
    "payload": {
        "kind": "agentTurn",
        "message": "运行 TikTok Shop 数据抓取"
    }
})
```

## 相关文件

- `SKILL.md`: 技能说明文档
- `src/fetch_tiktok_categories.py`: 主抓取脚本（重构版）
- `src/old/`: 旧代码参考
- `screenshots/categories.json`: 类目列表

## 经验教训

### 1. 选择合适的工具

- **Playwright** > Selenium：更快、更稳定
- **JavaScript** > Python DOM：直接操作浏览器 DOM
- **Persistent Context** > 新浏览器实例：复用登录状态

### 2. 理解页面结构

- 不要假设 URL 格式
- 使用浏览器开发者工具检查实际结构
- 动态调整选择器

### 3. 处理反爬机制

- 复用登录状态
- 添加随机等待
- 模拟真实用户行为

### 4. 分步测试

- 先测试首页加载
- 再测试类目提取
- 最后测试商品抓取
- 每一步都验证结果

## 数据格式规范

### 文件命名规则

```
tiktok_{category_slug}_{YYYYMMDD}_{HHMMSS}.json
```

**示例**：
- `tiktok_beauty_personal_care_20260509_104700.json`
- `tiktok_electronics_20260509_104730.json`
- `tiktok_womenswear_underwear_20260509_104800.json`

**命名规则**：
1. 前缀：`tiktok_`（平台标识）
2. 分类名：转小写，空格和特殊字符替换为下划线
3. 日期：`YYYYMMDD`（抓取日期）
4. 时间：`HHMMSS`（抓取时间）

### JSON 数据结构

```json
{
  "metadata": {
    "platform": "tiktok",
    "category": "美妆个护",
    "category_slug": "beauty_personal_care",
    "category_url": "https://www.tiktok.com/shop/c/beauty-personal-care/601450",
    "scraped_at": "2026-05-09T10:47:00.123456",
    "scraped_date": "2026-05-09",
    "scraped_time": "10:47:00",
    "total_items": 150
  },
  "products": [
    {
      "tag": "DIV",
      "className": "product-card-classname...",
      "text": "商品名称 $19.99",
      "price": "19.99",
      "rating": "4.8"
    }
  ]
}
```

**字段说明**：
- `metadata.platform`: 平台标识（"tiktok"）
- `metadata.category`: 分类中文名
- `metadata.category_slug`: 分类英文名（用于文件名和数据库索引）
- `metadata.category_url`: 分类页面 URL
- `metadata.scraped_at`: 抓取时间（ISO 8601 格式）
- `metadata.scraped_date`: 抓取日期（用于数据库分组查询）
- `metadata.scraped_time`: 抓取时间（用于数据库分组查询）
- `metadata.total_items`: 商品总数
- `products`: 商品列表数组

### 数据库导入示例

```python
import sqlite3
import json
from pathlib import Path
from datetime import datetime

# 连接数据库
conn = sqlite3.connect('tiktok_products.db')
cursor = conn.cursor()

# 创建表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT NOT NULL,
        category TEXT NOT NULL,
        category_slug TEXT NOT NULL,
        category_url TEXT,
        product_tag TEXT,
        product_text TEXT,
        price REAL,
        rating REAL,
        scraped_date TEXT,
        scraped_time TEXT,
        scraped_at TIMESTAMP,
        INDEX idx_platform (platform),
        INDEX idx_category (category),
        INDEX idx_scraped_date (scraped_date)
    )
''')

# 读取 JSON 文件
json_file = Path('output/scraping/tiktok_beauty_personal_care_20260509_104700.json')
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 插入数据
metadata = data['metadata']
products = data['products']

for product in products:
    cursor.execute('''
        INSERT INTO products 
        (platform, category, category_slug, category_url, product_tag, 
         product_text, price, rating, scraped_date, scraped_time, scraped_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        metadata['platform'],
        metadata['category'],
        metadata['category_slug'],
        metadata['category_url'],
        product.get('tag'),
        product.get('text'),
        float(product.get('price', 0)) if product.get('price') else None,
        float(product.get('rating', 0)) if product.get('rating') else None,
        metadata['scraped_date'],
        metadata['scraped_time'],
        datetime.fromisoformat(metadata['scraped_at'])
    ))

conn.commit()
conn.close()
print(f"[OK] 成功导入 {len(products)} 条数据")
```

### 查询示例

```sql
-- 查询某天的所有商品
SELECT * FROM products WHERE scraped_date = '2026-05-09';

-- 查询某个分类的所有商品
SELECT * FROM products WHERE category_slug = 'beauty_personal_care';

-- 查询某天的某个分类
SELECT * FROM products WHERE scraped_date = '2026-05-09' AND category_slug = 'beauty_personal_care';

-- 统计每天的商品数量
SELECT scraped_date, COUNT(*) as total FROM products GROUP BY scraped_date ORDER BY scraped_date;

-- 统计每个分类的商品数量
SELECT category, COUNT(*) as total FROM products GROUP BY category ORDER BY total DESC;
```

---

_这文档由你进化。随着项目发展，更新它。_
