# EcomAgent - 电商智能体

电商数据抓取与分析平台，支持 Amazon 和 TikTok Shop 数据抓取、存储、可视化。

**最后更新**：2026-05-20  
**状态**：生产环境可用

---

## 功能概览

| 功能 | 状态 | 说明 |
|------|------|------|
| 数据抓取 | ✅ | Amazon/TikTok Shop 热销数据 |
| 数据导入 | ✅ | JSON → SQLite，自动去重 |
| Web UI | ✅ | 商品总库、追踪、趋势分析 |
| 商品趋势 | ✅ | 销量/价格/评分图表 + 每日数据 |
| 图片存储 | ✅ | 自动下载、压缩、变更追踪 |
| 定时任务 | 🚧 | 待配置 |

---

## 快速开始

### 1. 启动 Web UI

```bash
cd C:\Users\Etroi\.openclaw\workspace\code\EcomAgent
python -m src.data_viewer.main
```

访问 http://localhost:8000

### 2. 数据抓取

```bash
# Amazon 抓取
python skills/amazon-fetcher/src/fetch_amazon_main_categories.py

# TikTok 抓取（需先启动 Chrome 调试端口）
chrome.exe --remote-debugging-port=9222 --user-data-dir="..."
python skills/tiktok-fetcher/src/fetch_tiktok_cdp.py
```

### 3. 数据导入

```bash
python skills/db-importer/src/import_to_db.py
```

---

## Web UI 功能

### 导航菜单

| 页面 | 功能 |
|------|------|
| 数据概览 | Amazon/TikTok 统计、抓取记录 |
| 商品总库 | 搜索、筛选、追踪、趋势分析 |
| 商品追踪 | 追踪商品列表、趋势查看 |
| 今日TOP榜 | 各分类热销排行 |
| 系统设置 | 配置文件查看 |

### 商品总库

- **筛选**：平台（Amazon/TikTok）、分类、关键词搜索
- **排序**：销量、价格、评分（升序/降序）
- **操作**：
  - ☆/★ 添加/取消追踪
  - 趋势 → 进入商品趋势页面
  - 查看 → 打开商品链接

### 商品趋势页面

- **时间选择**：近7天、15天、1月、3月、自定义
- **维度切换**：销量、价格、评分（Tab 切换）
- **图表**：SVG 折线图 + 鼠标悬停 Tooltip
- **数据表格**：每日数据详情（分页）

---

## 更新日志

### 2026-05-20
- ✅ 商品趋势页面开发
  - 时间选择（快速/自定义）
  - 维度切换（销量/价格/评分）
  - SVG 折线图 + Tooltip
  - 每日数据表格（分页）
  - 返回功能（记住来源页面）
- ✅ 商品库排序修复（全局排序后再分页）
- ✅ 追踪页面样式优化（与商品库一致）
- ✅ 文档重构

### 2026-05-19
- ✅ 图片抓取与存储功能
- ✅ 商品名称翻译流水线设计
- ✅ TikTok 数据库 UNIQUE 约束修复

### 2026-05-13
- ✅ Web UI 模块化重构（Lit + TypeScript + Vite）
- ✅ 商品总库、追踪、今日TOP榜页面
- ✅ OpenClaw 风格迁移

### 2026-05-12
- ✅ Web UI Bug 修复
- ✅ 追踪按钮改为星星图标

### 2026-05-11
- ✅ Web UI OpenClaw 风格重构
- ✅ 主题切换、导航折叠

### 2026-04-01
- ✅ TikTok Shop 数据抓取（CDP 连接模式）
- ✅ 28 个分类抓取

### 2026-03-14
- ✅ Amazon 数据抓取
- ✅ DB Importer 技能

---

## 目录结构

```
EcomAgent/
├── ui/                          # 前端（Lit + TypeScript）
│   ├── src/
│   │   ├── app.ts               # 主应用
│   │   ├── components/          # 组件
│   │   ├── pages/               # 页面
│   │   ├── services/api.ts      # API
│   │   └── types/               # 类型定义
│   └── package.json
├── src/
│   └── data_viewer/
│       ├── main.py               # FastAPI 后端
│       └── static/               # 前端构建输出
├── skills/
│   ├── amazon-fetcher/           # Amazon 抓取技能
│   ├── tiktok-fetcher/           # TikTok 抓取技能
│   └── db-importer/              # 数据导入技能
├── data/
│   ├── amazon.db                 # Amazon 数据库
│   ├── tiktok.db                 # TikTok 数据库
│   ├── product_master.db         # 商品主库
│   └── images/                   # 商品图片
├── output/
│   └── scraping/                 # JSON 抓取数据
├── scripts/
│   ├── generate_test_sales_data.py
│   └── generate_pending_names.py
├── docs/                         # 开发文档
│   ├── DEVELOPMENT.md            # 架构设计
│   ├── CHANGELOG.md              # 开发日志
│   ├── STATUS.md                 # 当前状态
│   ├── NOTES.md                  # 开发笔记
│   └── references/               # 参考资料
└── README.md                     # 本文件
```

---

## 数据库说明

### 商品主库 (product_master.db)

统一管理所有平台商品，通过 `ecom_code` 唯一标识。

| 字段 | 说明 |
|------|------|
| ecom_code | 唯一编码（ECAMxxx/ECTKxxx） |
| platform | 平台（amazon/tiktok） |
| name | 商品名称 |
| short_name | 中文简称 |
| category | 分类 |
| price | 价格 |
| rating | 评分 |
| sales_count | 销量 |

### 平台数据库

- `amazon.db`：products + daily_sales
- `tiktok.db`：tiktok_products + tiktok_daily_sales

---

## 常见问题

### Q: 图表 XY 轴标签不显示？

检查浏览器是否强制刷新（Ctrl+Shift+R），SVG 需要足够容器高度。

### Q: 排序只对当前页生效？

已修复。后端改为先排序再分页。

### Q: TikTok 抓取失败？

需先启动 Chrome 调试端口：
```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="..."
```

### Q: 商品趋势页面返回空白？

已修复。使用 `window.ecomagentNavigate()` 返回来源页面。

---

## 开发文档

详见 `docs/` 目录：

- **DEVELOPMENT.md** - 架构设计、API 设计
- **CHANGELOG.md** - 每日开发记录
- **STATUS.md** - 当前进行中的任务
- **NOTES.md** - 技术难点、解决方案