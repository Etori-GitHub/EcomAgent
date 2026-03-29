# TODO - Amazon Best Sellers 抓取项目

## 当前进度
- ✅ 抓取单个分类的前2页（100个商品）
- ✅ 支持多分类批量抓取
- ✅ 抓取所有主要分类（6个）
- ✅ 添加反爬机制（随机等待）

## 待实现方案

### 方案1：抓取所有子分类
1. 先抓取 6 个主要分类（Kitchen, Electronics, Beauty, HPC, Fashion, Industrial）
2. 每个主要分类下有多个子分类（如 Electronics 下有 Amazon Devices, Apps & Games 等）
3. 需要先抓取每个主要分类页面的子分类列表

### 方案2：动态抓取所有分类
1. 访问 `/gp/bestsellers/` 主页
2. 提取所有分类链接（包括主要分类和子分类）
3. 动态构建 URL 并抓取

### URL 格式
- 主分类 URL: `https://www.amazon.com/gp/bestsellers/{slug}/ref=zg_bs_{slug}_sm`
- 子分类 URL: `https://www.amazon.com/Best-Sellers-{name}/zgbs/{name}/ref=zg_bs_nav_{name}_0`

### 需要解决的问题
1. 如何准确提取所有子分类
2. 如何处理分类名中的特殊字符（如 `&`, `,`, 空格）
3. 如何避免重复抓取（有些子分类可能在多个主要分类下）

## 文件清理建议
- `debug/` 目录下的调试文件可以删除
- `src/` 目录下的旧版脚本可以删除：
  - `fetch_amazon_bestsellers.py`
  - `fetch_amazon_all_categories.py`
  - `fetch_amazon_categories.py`
  - `fetch_amazon_category.py`
  - `debug_page.py`
  - `debug_page_bs4.py`
  - `debug_amazon_page.py`
  - `save_page_html.py`
- `src/__pycache__/` 目录可以删除

## 当前推荐使用
- `src/fetch_amazon_main_categories.py` - 抓取 6 个主要分类（推荐）
