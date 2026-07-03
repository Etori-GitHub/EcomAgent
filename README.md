# EcomAgent - 电商智能体

电商数据抓取与分析平台，支持 Amazon 和 TikTok Shop 数据抓取、存储、可视化。

**最后更新**：2026-06-25  
**版本**：v2.2  
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
| 1688 货源采集 | ✅ | Chrome 插件，悬停采集 |
| 跨平台启动 | ✅ | Windows/Mac 免安装启动 |
| OpenClaw 辅助 | ✅ | 自动创建定时任务，Gateway 独立运行 |

---

## 快速开始（傻瓜式）

### Windows

**首次安装**：双击 `setup.bat`
- 自动下载 Python 3.11.9
- 自动安装所有依赖
- 启动服务并打开浏览器

**后续启动**：双击 `start.bat`
- 直接启动服务

### macOS / Linux

**首次安装**：
```bash
chmod +x setup.sh
./setup.sh
```

**后续启动**：
```bash
./start.sh
```

---

启动后会自动打开浏览器访问 http://127.0.0.1:8000

### TikTok 上传功能

首次使用 TikTok 上传功能时：
1. 点击货源库的「TikTok」按钮
2. 系统会自动启动调试 Chrome 并打开登录页
3. 登录 TikTok Shop 后台
4. 再次点击「TikTok」按钮即可上传

---

## 手动启动（开发模式）

```bash
# 方式1：使用启动脚本
python run_viewer.py

# 方式2：模块方式
python -m src.data_viewer.main
```

---

## 数据抓取

推荐使用 `daily_fetch.py` 统一入口：

```bash
# 完整流程（抓取 + 导入 + 图片下载）
python scripts/daily_fetch.py all

# 只抓取 TikTok
python scripts/daily_fetch.py tiktok

# 只抓取 Amazon
python scripts/daily_fetch.py amazon

# 只导入数据（不抓取）
python scripts/daily_fetch.py import

# 只下载图片
python scripts/daily_fetch.py images
```

**注意**：`tiktok` 和 `amazon` 参数**只抓取不导入**，需要单独运行 `import` 或直接用 `all`。

### 技能文档

详细抓取说明请查看各技能的 SKILL.md：
- `skills/amazon-fetcher/SKILL.md` - Amazon 抓取说明
- `skills/tiktok-fetcher/SKILL.md` - TikTok 抓取说明（含反爬对策）

---

## 1688 货源采集插件

Chrome 插件，悬停采集 1688 商品信息。

### 安装

1. Chrome 打开 `chrome://extensions/`
2. 开启「开发者模式」
3. 点击「加载已解压的扩展程序」
4. 选择 `1688-plugin` 目录

### 使用

1. 在商品总库点击「1688」按钮
2. 跳转到 1688 搜索页
3. 鼠标悬停商品卡片，弹出采集窗口
4. 确认采集，数据保存到本地

**注意**：插件跨平台通用（Windows/Mac/Linux）

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

## 目录结构

```
EcomAgent/
├── python/                      # Windows 嵌入式 Python
├── python-mac/                  # macOS Python 压缩包
├── start.bat                    # Windows 启动脚本
├── start.sh                     # macOS 启动脚本
├── setup-mac.sh                 # macOS 安装脚本
├── run_viewer.py                # 启动入口
│
├── ui/                          # 前端（Lit + TypeScript + Vite）
│   ├── src/
│   │   ├── app.ts
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
│
├── src/                         # 后端源码
│   ├── data_viewer/             # FastAPI 服务
│   ├── tiktok_uploader.py       # TikTok 上传模块
│   └── monitor.py               # 监控模块
│
├── skills/                      # 抓取技能
│   ├── amazon-fetcher/          # Amazon 抓取
│   ├── tiktok-fetcher/          # TikTok 抓取
│   └── db-importer/             # 数据导入
│
├── 1688-plugin/                 # Chrome 插件（跨平台）
│   ├── manifest.json
│   ├── content.js
│   └── content.css
│
├── data/                        # 数据库
│   ├── amazon.db
│   ├── tiktok.db
│   ├── product_master.db
│   ├── sourcing.db
│   └── images/
│
├── scripts/                     # 工具脚本
├── test/                        # 测试脚本
├── docs/                        # 开发文档
└── README.md
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
- `sourcing.db`：1688 货源数据

---

## 更新日志

### 2026-06-25
- ✅ **TikTok Shop 反爬突破**
  - 关键发现：访问时需要带 `referer: https://www.google.com/`
  - 修复所有抓取脚本（`fetch_tiktok_categories.py`, `fetch_task.py`, `extract_categories.py`）
  - 抓取间隔调整：TikTok 类目间等待 1-5 分钟，避免被封
- ✅ **类目管理优化**
  - 新增全选/取消全选功能
  - 修复类目卡片展开后无法关闭的问题
- ✅ **素材路径修复**
  - 修复数据库中素材路径与实际文件夹不一致的问题
  - 创建 `scripts/fix_assets_paths.py` 自动修复工具
- ✅ **项目清理**
  - 删除测试脚本（test_*.py, compare_*.py, connect_*.py）
  - 创建 `test/` 目录用于临时测试脚本

### 2026-06-16
- ✅ **趋势图表修复**
  - 修复 XY 轴标签不显示问题（字体增大、颜色调整）
  - 修复鼠标悬停 Tooltip 不显示问题
  - Amazon/TikTok 默认指标适配（Amazon 显示排名，TikTok 显示销量）
  - API 字段兼容性修复（timestamp → created_at）
- 🔄 开发规划调整
  - Phase 1：修复已知 Bug ✅ 已完成
  - Phase 2：生图/生视频/详情页功能 ⏳ 待开发
  - Phase 3：TikTok 商品自动填充 ⏳ 待开发
  - Phase 4：Mac/Windows 跨平台兼容 ⏳ 待开发

### 2026-06-10
- ✅ 嵌入式 Python 配置（跨平台免安装）
  - Windows: python/ 目录（已配置好）
  - macOS: python-mac/ 压缩包 + setup-mac.sh
- ✅ 启动脚本
  - Windows: start.bat（双击启动）
  - macOS: start.sh + setup-mac.sh
- ✅ 项目结构整理
  - 脚本移到 scripts/ 和 test/
  - 根目录只保留启动文件

### 2026-05-20
- ✅ 商品趋势页面开发
- ✅ 商品库排序修复
- ✅ 追踪页面样式优化

### 2026-05-19
- ✅ 图片抓取与存储功能
- ✅ 商品名称翻译流水线设计

### 2026-05-13
- ✅ Web UI 模块化重构（Lit + TypeScript + Vite）
- ✅ OpenClaw 风格迁移

### 2026-04-01
- ✅ TikTok Shop 数据抓取（CDP 连接模式）
- ✅ 1688 货源采集插件

### 2026-03-14
- ✅ Amazon 数据抓取
- ✅ DB Importer 技能

---

## 常见问题

### Q: Windows 启动报错 "No module named xxx"？

依赖已内置，如果报错请重新运行安装：
```bash
python\python.exe -m pip install fastapi uvicorn sqlalchemy click pydantic playwright --target python\Lib\site-packages
```

### Q: macOS 首次启动？

先运行 `setup-mac.sh` 解压 Python 和安装依赖，然后运行 `start.sh`。

### Q: TikTok 抓取失败？

需先启动 Chrome 调试端口，见上方说明。

### Q: 1688 插件安装后没反应？

刷新 1688 页面，确保 URL 带有 `ecom_code` 参数。

---

## 开发文档

详见 `docs/` 目录：

- **DEVELOPMENT.md** - 架构设计、API 设计
- **CHANGELOG.md** - 每日开发记录
- **STATUS.md** - 当前进行中的任务
- **NOTES.md** - 技术难点、解决方案
