# EcomAgent 开发日志

按日期记录开发进度,方便回溯。

---

## 2026-05-20

### 商品趋势页面开发

**功能**：从商品库点击“趋势”按钮进入独立页面，展示商品各维度数据随时间变化。

**完成内容**：
- 后端 API 扩展 `/api/product-trend/{ecom_code}`
  - 支持时间范围（快速选择/自定义）
  - 支持分页
  - 返回详细数据表格
- 前端商品趋势页面
  - 时间选择（近7天/15天/1月/3月/自定义）
  - 维度切换（销量/评分/价格）Tab
  - SVG 折线图渲染
  - 每日数据表格（分页）
  - 返回按钮（记住来源页面）

**存在问题（待修复）**：
- XY 轴标签不显示
  - SVG 代码中存在 text 元素，但页面上不显示
  - 已尝试调整容器高度、固定颜色值，仍未解决
- 鼠标悬停 Tooltip 不显示
  - 已实现 mousemove 事件处理，但 tooltip 未显示

**问题修复（已完成）**：
- Tab 切换不生效 → 添加 `requestUpdate()`
- 返回按钮跳转到空白页 → 改用 `window.ecomagentNavigate()`

### 商品库排序修复

**问题**：排序只对当前页生效，不是全局排序。

**原因**：后端代码先分页再排序。

**修复**：改为先获取所有数据 → 排序 → 再分页。

### 追踪页面样式优化

- 移除星星按钮，改为“移除”按钮
- 样式与商品库统一

### 文档重构

- README.md：用户指南
- docs/DEVELOPMENT.md：架构设计
- docs/CHANGELOG.md：开发日志
- docs/STATUS.md：当前状态
- docs/NOTES.md：开发笔记

---

## 2026-05-19

### 商品库 UI 重构

**完成内容**:
- 图片显示列
- 销量字段
- 分类筛选(动态加载)
- 排序功能(销量/评分/价格)
- 平台筛选改为顶部按钮
- 默认按销量降序排序

### 测试数据生成

**脚本**:`scripts/generate_test_sales_data.py`

为商品库中 1514 个商品生成近 7 天随机销售趋势数据。

### 数据库修复

**问题**:TikTok 表 `tiktokshop_id` 缺少 UNIQUE 约束导致导入失败。

**修复**:创建 `idx_tiktokshop_unique` 索引,清理 799 条重复记录。

---

## 2026-05-13

### Web UI 模块化重构

**技术栈**:Lit + TypeScript + Vite

**完成内容**:
- 组件化:sidebar、layout、header
- 页面化:dashboard、product-master、tracking、today-top、settings 等
- 构建输出到 `src/data_viewer/static/`

### 核心问题修复

| 问题 | 解决方案 |
|------|----------|
| 侧边栏折叠不生效 | `requestUpdate('collapsed')` |
| 导航切换不生效 | 全局函数 `window.ecomagentNavigate` |
| 异步数据后视图不更新 | 显式 `requestUpdate()` |

### 今日TOP榜

- Amazon/TikTok 分类切换
- 排名变化状态(上升/下降/新入榜)
- 分类置顶功能

---

## 2026-05-12

### Web UI Bug 修复

- 编码修复(191 处未闭合标签)
- 追踪按钮改为星星图标(☆/★)

---

## 2026-05-11

### Web UI OpenClaw 风格重构

- CSS 变量系统
- 深色/浅色主题切换
- 导航折叠功能

---

## 2026-04-10

### 数据抓取技能完成

- Amazon 抓取技能(动态获取分类列表)
- TikTok 抓取技能(CDP 连接模式)
- DB Importer 技能(数据导入 + 去重)