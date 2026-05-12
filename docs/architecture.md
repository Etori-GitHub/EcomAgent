# EcomAgent 架构设计

_电商数据抓取与分析平台_

## 项目概述

EcomAgent 是一个电商数据抓取和分析平台，支持 Amazon 和 TikTok Shop 的数据抓取、存储和可视化。

## 核心组件

### 1. Data Fetchers (数据抓取)

**位置**: `skills/`

- **amazon-fetcher**: 亚马逊热销榜单数据抓取
- **tiktok-fetcher**: TikTok Shop 数据抓取

**功能**:
- 定时/手动抓取商品数据
- 保存为 JSON 文件
- 支持多分类/多页面

### 2. DB Importer (数据导入)

**位置**: `skills/db-importer/`

**功能**:
- 扫描 `output/scraping/` 目录
- 解析 JSON 文件
- 导入到 SQLite 数据库
- 去重处理

**数据库**:
- `data/amazon.db`
- `data/tiktok.db`

### 3. Data Viewer (数据展示)

**位置**: `src/data_viewer/`

**功能**:
- Web UI 展示数据库数据
- 搜索/过滤功能
- 数据概览统计

**启动方式**:
```bash
ecomagent serve
```

### 4. CLI Tool (命令行工具)

**位置**: 根目录

**命令**:
- `ecomagent serve` - 启动 Web UI
- `ecomagent status` - 查看系统状态
- `ecomagent import` - 手动触发数据导入

## 数据流向

```
[爬虫] → JSON 文件 → [Importer] → SQLite 数据库 → [Data Viewer] → Web UI
```

## 技术栈

- **语言**: Python 3.10+
- **数据库**: SQLite
- **Web 框架**: FastAPI
- **爬虫**: Playwright
- **部署**: 本地服务 / Docker (未来)

## 目录结构

```
EcomAgent/
├── skills/                    # OpenClaw 技能
│   ├── amazon-fetcher/
│   ├── tiktok-fetcher/
│   └── db-importer/
├── src/                       # 核心代码
│   └── data_viewer/
├── data/                      # 数据库
│   ├── amazon.db
│   └── tiktok.db
├── output/                    # 输出文件
│   └── scraping/
├── docs/                      # 文档
├── run_viewer.py              # 启动脚本
├── ecomagent                  # CLI 工具
└── pyproject.toml             # 项目配置
```

## 开发原则

1. **模块化**: 每个功能独立，易于维护
2. **可扩展**: 支持添加新平台/新功能
3. **文档化**: 所有功能都有详细文档
4. **测试**: 关键功能需要单元测试

## 未来规划

- [ ] 支持更多电商平台 (eBay, Shopify 等)
- [ ] 数据分析和可视化 (图表)
- [ ] 定时任务自动化
- [ ] API 接口开放
- [ ] Docker 容器化部署
