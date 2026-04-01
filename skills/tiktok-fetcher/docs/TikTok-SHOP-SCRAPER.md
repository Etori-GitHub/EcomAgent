# TikTok Shop 抓取开发文档

## 项目背景

EcomAgent 项目已经实现了亚马逊热销榜单的数据抓取功能，现在需要扩展支持 TikTok Shop 的数据抓取。

## 技术方案

### 1. 抓取工具选择

- **Playwright**: 用于浏览器自动化，支持 headless 模式和真实浏览器模式
- **Python**: 用于编写抓取脚本
- **JSON**: 数据输出格式

### 2. 页面结构分析

TikTok Shop 的页面结构可能与亚马逊不同，需要根据实际页面调整选择器。

#### 可能的页面结构

```html
<!-- 商品卡片 -->
<div class="product-card">
    <div class="product-name">商品名称</div>
    <div class="product-price">$19.99</div>
    <div class="product-rating">4.8 ★</div>
    <div class="product-reviews">(1234)</div>
    <div class="product-sold">5678 sold</div>
</div>
```

#### 选择器策略

1. **类名模糊匹配**: 使用 `[class*="name"]`, `[class*="price"]` 等
2. **多选择器尝试**: 尝试多种可能的选择器组合
3. **降级处理**: 如果主要选择器失败，尝试备用选择器

### 3. 反爬策略

1. **随机等待**: 在页面加载和滚动后添加随机等待时间
2. **模拟真实用户**: 使用真实浏览器模式（headless=False）
3. **User-Agent**: 使用真实的浏览器 User-Agent
4. **滚动加载**: 模拟用户滚动页面触发懒加载

### 4. 数据提取

#### 需要提取的信息

- `rank`: 排名
- `name`: 商品名称
- `price`: 价格
- `rating`: 评分
- `rating_count`: 评价数量
- `sold_count`: 销量
- `category`: 大分类
- `subcategory`: 子分类

## 开发步骤

### 第一步：页面结构分析

1. 打开 TikTok Shop 网站
2. 检查商品列表的 HTML 结构
3. 记录关键元素的类名和选择器

### 第二步：编写抓取脚本

参考 `fetch_tiktok_categories.py` 中的 JavaScript 代码，根据实际页面结构调整选择器。

### 第三步：测试和调试

1. 使用 headless=False 模式运行脚本
2. 观察浏览器操作过程
3. 检查控制台输出，确认数据提取正确

### 第四步：优化

1. 添加更多错误处理
2. 优化选择器以适应不同页面结构
3. 添加重试机制

## 常见问题

### 1. 页面加载失败

**原因**: TikTok Shop 可能有反爬机制

**解决方案**:
- 增加等待时间
- 使用真实浏览器模式
- 添加随机 User-Agent

### 2. 数据提取失败

**原因**: 页面结构与预期不符

**解决方案**:
- 使用浏览器开发者工具检查实际页面结构
- 调整 JavaScript 代码中的选择器
- 添加更多调试输出

### 3. 数据不完整

**原因**: 懒加载导致部分商品未加载

**解决方案**:
- 模拟用户滚动页面
- 增加等待时间
- 多次滚动直到加载完成

## 扩展功能

### 1. 支持更多分类

在 `categories` 列表中添加更多 TikTok Shop 分类。

### 2. 支持翻页

如果分类页面有分页，可以添加翻页逻辑。

### 3. 数据库导入

将 JSON 数据导入 SQLite 数据库，支持时间序列分析。

## 相关文件

- `SKILL.md`: 技能说明文档
- `src/fetch_tiktok_categories.py`: 抓取脚本
- `docs/TODO.md`: 待办事项
