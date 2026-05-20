# EcomAgent 分阶段开发计划

_项目进度的阶段性规划_

## 当前阶段

### ✅ Phase 1: 基础数据抓取 (已完成)

**目标**: 实现 Amazon 和 TikTok Shop 数据抓取

**完成内容**:
- ✅ Amazon 抓取技能 (动态获取分类列表)
- ✅ TikTok Shop 抓取技能 (多分类)
- ✅ JSON 数据保存
- ✅ 唯一 ID 提取 (ASIN + tiktokshop_id)
- ✅ 图片 URL 抓取
- ✅ OpenClaw 技能集成
- ✅ 使用 Chrome Profile 复用登录状态

**状态**: 生产环境可用

**待优化**:
- [ ] Amazon 销量字段（需进入详情页抓取）
- [ ] TikTok 抓取稳定性（Chrome Profile 冲突问题）

---

### ✅ Phase 2: 数据导入 (已完成)

**目标**: 将 JSON 数据导入数据库

**完成内容**:
- ✅ DB Importer 技能开发
- ✅ Amazon 数据导入
- ✅ TikTok 数据导入
- ✅ 去重处理
- ✅ 错误容错
- ✅ 唯一 ID 支持 (ASIN + tiktokshop_id)
- ✅ 图片下载与存储
- ✅ 图片变更追踪

**状态**: 生产环境可用

**新增功能** (2026-05-19):
- 图片处理模块 `image_processor.py`
- 图片压缩（≤1024px，≤300KB）
- 图片变更历史记录

---

### ✅ Phase 3: 数据可视化 (已完成)

**目标**: 开发 Web UI 展示数据

**完成内容**:
1. **Phase 3.1: 基础框架** ✅
   - [x] 创建 Data Viewer 模块
   - [x] 搭建 FastAPI 服务
   - [x] 实现基础 HTML 页面
   - [x] 创建 CLI 工具 (`ecomagent serve`)

2. **Phase 3.2: 数据展示** ✅
   - [x] Amazon 产品列表页
   - [x] TikTok 产品列表页
   - [x] 数据概览统计
   - [x] 搜索/过滤功能
   - [x] 分页功能
   - [x] 图片显示列

3. **Phase 3.3: UI 优化** ✅
   - [x] OpenClaw 风格样式迁移
   - [x] 主题切换功能 (深色/浅色)
   - [x] 导航折叠功能
   - [x] 响应式布局

**状态**: 生产环境可用

---

### 🚧 Phase 4: 商品名称翻译流水线 (进行中)

**目标**: AI 自动翻译商品名称为中文简称

**设计流程**:
```
3:30  EcomAgent 生成 pending_names.json (10条)
3:40  OpenClaw AI 翻译 → processed_names.json  
3:50  EcomAgent 导入数据库
循环 03:30-08:30，每小时约 60 条
```

**完成内容**:
- ✅ `scripts/generate_pending_names.py` - 生成待翻译 JSON
- ✅ `scripts/import_processed_names.py` - 导入翻译结果
- ✅ 安全机制（超时删除、文件检查）
- ✅ OpenClaw cron 任务配置

**待完成**:
- [ ] 实际运行测试
- [ ] 翻译质量验证

---

### 📅 Phase 5: 自动化 (待配置)

**目标**: 实现定时任务和自动化流程

**计划内容**:
- [ ] **定时抓取任务**
  - [ ] 凌晨 0:00 启动爬虫
  - [ ] Amazon 和 TikTok 分开运行（避免 Chrome Profile 冲突）
  - [ ] 抓取完成后自动导入数据库
- [ ] **商品名称翻译流水线**
  - [ ] 凌晨 3:30-8:30 自动运行
- [ ] **异常告警**
  - [ ] 抓取失败通知
  - [ ] 数据异常检测

---

## 遗留问题

### 1. TikTok 抓取失败

**问题**: TikTok 抓取脚本运行失败，没有生成数据文件

**原因**: Chrome Profile 冲突（和 Amazon 同时使用 Profile 1）

**解决方案**:
- 方案A: Amazon 和 TikTok 定时任务错开运行
- 方案B: 使用不同的 Chrome Profile

### 2. Amazon 销量字段未实现

**问题**: Amazon 商品详情页有销量数据，但抓取脚本未进入详情页抓取

**原因**: 进入详情页会大幅增加请求次数，反爬风险高

**待决定**:
- 保守方案：只抓前 5 个商品的详情页
- 激进方案：全部进详情页，增加等待时间

### 3. 抓取数量控制

**当前设置**:
- Amazon: 每分类 1 页（约 25 个商品）
- TikTok: 每分类 20 个商品（去重后）

**待验证**: 实际抓取数量是否符合预期

---

## 文件结构

```
EcomAgent/
├── data/
│   ├── images/                    # 商品图片
│   │   ├── amazon/
│   │   └── tiktok/
│   ├── name_processing/           # 名称翻译流水线
│   │   ├── pending_names.json
│   │   └── processed_names.json
│   ├── image_changes.db           # 图片变更记录
│   ├── amazon.db
│   ├── tiktok.db
│   └── product_master.db
├── scripts/
│   ├── generate_pending_names.py  # 生成待翻译
│   ├── import_processed_names.py  # 导入翻译结果
│   └── migrate_image_fields.py    # 数据库迁移
├── skills/
│   ├── amazon-fetcher/
│   ├── tiktok-fetcher/
│   └── db-importer/
│       └── src/image_processor.py
├── output/
│   ├── scraping/                  # 抓取数据
│   └── amazon_categories.json     # 分类列表
└── ui/                            # Web UI (Lit + TypeScript)
```

---

## 里程碑

| 阶段 | 状态 | 完成日期 |
|------|------|----------|
| Phase 1 | ✅ 完成 | 2026-04-10 |
| Phase 2 | ✅ 完成 | 2026-05-09 |
| Phase 3 | ✅ 完成 | 2026-05-19 |
| Phase 4 | 🚧 进行中 | - |
| Phase 5 | 📅 待配置 | - |

---

## 下一步

1. 解决 TikTok 抓取 Chrome Profile 冲突问题
2. 配置定时任务（凌晨抓取 + 翻译流水线）
3. 决定 Amazon 销量抓取方案