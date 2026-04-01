# TikTok Shop 数据抓取使用指南

## 快速开始

### 方法一：使用启动脚本（推荐）

```powershell
# 在项目根目录下运行
.\start_tiktok_fetch.ps1
```

### 方法二：手动运行脚本

```bash
# 安装依赖（首次运行）
cd code/EcomAgent/skills/tiktok-fetcher
pip install -r requirements.txt
playwright install chromium

# 运行抓取脚本
python code/EcomAgent/skills/tiktok-fetcher/src/fetch_tiktok_categories.py
```

## 数据输出

抓取的数据会自动保存到：

```
code/EcomAgent/output/scraping/
```

文件命名格式：

```
tiktok_分类名_YYYYMMDD_HHMMSS.json
```

例如：

```
tiktok_Electronics_20260401_133000.json
tiktok_Fashion_20260401_133500.json
```

## 数据格式

```json
[
  {
    "rank": 1,
    "name": "商品名称",
    "price": 19.99,
    "rating": 4.8,
    "rating_count": 1234,
    "sold_count": 5678,
    "category": "Electronics",
    "subcategory": "Best Sellers in Electronics"
  }
]
```

## 注意事项

1. **页面结构可能变化**: TikTok Shop 的页面结构可能随时间变化，如抓取失败请检查页面选择器
2. **反爬机制**: 脚本已添加随机等待机制，但仍可能触发反爬
3. **网络问题**: 确保网络连接正常，TikTok Shop 在某些地区可能无法访问
4. **数据准确性**: 抓取的数据准确性取决于页面结构的稳定性

## 故障排查

### 1. 页面加载失败

**解决方案**:
- 检查网络连接
- 尝试在浏览器中手动访问 TikTok Shop
- 增加等待时间

### 2. 数据提取失败

**解决方案**:
- 使用浏览器开发者工具检查实际页面结构
- 调整 `fetch_tiktok_categories.py` 中的 JavaScript 选择器
- 参考开发文档 `docs/TikTok-SHOP-SCRAPER.md`

### 3. 数据不完整

**解决方案**:
- 模拟用户滚动页面
- 增加等待时间
- 多次滚动直到加载完成

## 扩展功能

### 支持更多分类

在 `src/fetch_tiktok_categories.py` 的 `categories` 列表中添加更多 TikTok Shop 分类。

### 支持翻页

如果分类页面有分页，可以添加翻页逻辑。

### 数据库导入

将 JSON 数据导入 SQLite 数据库，支持时间序列分析。

## 相关文档

- [SKILL.md](SKILL.md): 技能说明文档
- [开发文档](docs/TikTok-SHOP-SCRAPER.md): 详细开发文档
- [TODO.md](docs/TODO.md): 待办事项

## 联系方式

如有问题，请参考开发文档或联系项目维护者。
