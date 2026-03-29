# 亚马逊 Best Sellers 抓取开发文档

## 项目概述

本项目用于抓取亚马逊 Best Sellers 榜单数据，支持抓取所有主要分类的热销榜单，并可扩展至子分类。

## 技术方案

### 核心技术栈

- **语言**: Python 3.8+
- **浏览器自动化**: Playwright (Chromium)
- **数据格式**: JSON
- **输出目录**: `code/EcomAgent/output/scraping/`

### 抓取逻辑

#### 1. 榜单结构分析

亚马逊 Best Sellers 页面采用分页结构：
- 每页显示 50 个商品
- 主分类 URL 格式: `https://www.amazon.com/gp/bestsellers/{slug}/ref=zg_bs_{slug}_sm`
- 子分类 URL 格式: `https://www.amazon.com/Best-Sellers-{name}/zgbs/{name}/ref=zg_bs_nav_{name}_0`
- 分页 URL: `?_encoding=UTF8&pg=N` (N 为页码)

#### 2. 数据提取策略

使用 Playwright 的 `evaluate()` 方法执行 JavaScript 代码提取数据：

```javascript
// 核心选择器
const rows = document.querySelectorAll('li.zg-no-numbers');

// 每个商品提取字段：
- rank: 排名（从 .zg-bdg-text 提取）
- name: 商品名称（从链接文本提取）
- asin: 商品唯一标识（从链接 URL 正则匹配）
- price: 价格（从价格链接文本提取）
- rating: 评分（从 .a-icon-alt 提取）
- rating_count: 评论数（从 .a-size-small 提取）
```

#### 3. 动态内容加载

为确保页面完全加载，采用以下策略：
1. 设置大视口高度（1920x5000）一次性加载所有商品
2. 访问页面后等待 5-10 秒（随机）
3. 滚动到底部触发懒加载
4. 再等待 2-5 秒确保内容加载完成

### 反爬措施

- 页面访问前随机等待 5-10 秒
- 滚动后随机等待 2-5 秒
- 分类之间随机等待 3-8 秒
- 使用 Playwright 模拟真实用户行为

### 错误处理

- 单个商品解析失败不影响其他商品
- 某页商品不足 50 个时，按实际数量提取
- 总数据量 = 所有页面实际提取商品之和

## 开发经验总结

### 1. 选择器调试技巧

- 使用浏览器开发者工具（F12）分析页面结构
- 优先使用唯一标识符（ID）或稳定的 class
- 对于动态内容，使用 `querySelectorAll` 遍历所有匹配项

### 2. 页面加载优化

- **视口设置**: 设置足够大的高度避免分页加载
- **等待策略**: 静态等待 + 滚动触发 + 再等待
- **超时设置**: `page.goto()` 设置 60 秒超时

### 3. 数据清洗

- 价格提取：使用正则 `[^\\d.]` 移除非数字字符
- 评分提取：从 `4.5 out of 5 stars` 中提取 `4.5`
- 评论数提取：从 `273,537 ratings` 中提取数字

### 4. URL 构建

- 主分类 URL: `/gp/bestsellers/{slug}/ref=zg_bs_{slug}_sm`
- 子分类 URL: `/Best-Sellers-{name}/zgbs/{name}/ref=zg_bs_nav_{name}_0`
- 分页 URL: `?_encoding=UTF8&pg=N`

## 扩展方案

### 支持所有分类

亚马逊 Best Sellers 主页面包含 6 个主要分类：
- Kitchen & Dining
- Electronics
- Beauty & Personal Care
- Health & Household
- Clothing, Shoes & Jewelry
- Industrial & Scientific

每个主要分类下还有多个子分类。

#### 实现方式

1. **抓取主要分类**
   - 访问主页面 `https://www.amazon.com/gp/bestsellers/`
   - 提取 6 个主要分类的链接

2. **抓取子分类**（待实现）
   - 访问每个主要分类页面
   - 提取子分类列表
   - 循环抓取每个子分类

3. **文件命名规范**
   ```
   amazon_{分类名}_{YYYYMMDD_HHMMSS}.json
   ```

### 代码结构优化

```python
# 主函数：抓取指定分类的前 N 页
def fetch_category_bestsellers(category_url, category_name, subcategory, pages=2):
    """抓取指定分类的热销榜单"""
    # 实现抓取逻辑

# 主函数：抓取所有分类
def fetch_all_categories():
    """抓取所有 Best Sellers 分类"""
    # 1. 获取所有分类链接
    # 2. 循环抓取每个分类
    # 3. 保存到对应文件
```

## 使用说明

### 安装依赖

```bash
cd code/EcomAgent/skills/amazon-fetcher
pip install -r requirements.txt
playwright install chromium
```

### 运行脚本

```bash
# 抓取 6 个主要分类的前2页（共600个商品）
python code/EcomAgent/skills/amazon-fetcher/src/fetch_amazon_main_categories.py

# 或者抓取所有分类（待实现）
python code/EcomAgent/skills/amazon-fetcher/src/fetch_amazon_all_categories.py
```

### 输出格式

```json
[
  {
    "rank": 1,
    "name": "商品名称",
    "asin": "B08JHCVHTY",
    "price": 11.99,
    "rating": 4.4,
    "rating_count": 273537,
    "category": "Electronics",
    "subcategory": "Best Sellers in Electronics"
  }
]
```

## 注意事项

1. **反爬机制**: 已添加随机等待机制，但仍建议在非高峰时段运行
2. **页面结构变化**: 亚马逊可能更新页面结构，需定期检查选择器
3. **网络稳定性**: 确保网络连接稳定，避免因超时导致抓取失败
4. **数据更新频率**: 建议每天或每周运行一次，获取最新榜单

## 后续优化方向

1. 支持抓取所有子分类（目前只支持 6 个主要分类）
2. 添加重试机制（网络失败时自动重试）
3. 支持增量更新（只抓取新增商品）
4. 添加数据去重逻辑
5. 支持导出为 CSV/Excel 格式
6. 添加数据可视化功能
7. 支持自定义分类和页数配置

## 当前进度（2026-03-29）

### 已完成
- ✅ 抓取单个分类（Electronics）第1页数据
- ✅ 数据保存到 JSON 文件
- ✅ 支持多分类批量抓取
- ✅ 支持分页抓取（前2页）
- ✅ 添加反爬机制（随机等待）
- ✅ 6 个主要分类全部抓取成功（共 600 个商品）

### 待实现
- ⏳ 抓取所有子分类（如 Electronics 下的 Amazon Devices, Apps & Games 等）
- ⏳ 动态抓取分类列表（避免硬编码）
- ⏳ 数据合并到一个 JSON 文件
- ⏳ 增量更新支持

## 文件结构

```
amazon-fetcher/
├── SKILL.md                    # 技能说明文档
├── docs/
│   └── AMAZON-BESTSELLER-SCRAPER.md  # 开发文档（本文档）
├── src/
│   ├── fetch_amazon_main_categories.py   # 抓取 6 个主要分类（推荐使用）
│   ├── fetch_amazon_all_categories.py    # 抓取所有分类（待完善）
│   ├── fetch_amazon_categories.py        # 抓取分类列表（调试用）
│   └── fetch_amazon_bestsellers.py       # 抓取单个分类（旧版）
└── requirements.txt
```

---

_Good luck out there. Make it count._
