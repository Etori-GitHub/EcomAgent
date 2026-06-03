# TikTok Shop 自动化开发指南

## 项目概述

**目标**: 将 EcomAgent 货源数据自动上传到 TikTok Shop 商家后台，保存为草稿商品。

**核心流程**:
```
EcomAgent 货源 (sourcing_1688) → 自动化填入 TikTok Shop → 保存草稿
```

---

## 页面分析方法

### 概述

使用 Playwright 连接到已运行的 Chrome 浏览器（CDP 协议），深度分析页面结构。

### 准备工作

1. **启动带调试端口的 Chrome**
   ```powershell
   # 关闭所有 Chrome 进程
   Stop-Process -Name chrome -Force
   
   # 启动带调试端口的新 Chrome
   Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--remote-debugging-port=9222", "--user-data-dir=C:\Users\Etroi\.openclaw\chrome-tiktok"
   ```

2. **验证端口**
   ```powershell
   netstat -ano | Select-String "9222"
   # 应显示: TCP 127.0.0.1:9222 ... LISTENING
   ```

3. **在 Chrome 中登录目标网站并进入要分析的页面**

### 执行过程

1. **运行分析脚本**
   ```powershell
   cd C:\Users\Etroi\.openclaw\workspace\code\EcomAgent
   python scripts/tiktok_browser.py
   ```

2. **脚本输出**
   - `xxx_html.txt` - 页面 HTML 结构
   - `xxx_screenshot.png` - 页面截图
   - 终端输出元素详情

---

## TikTok Shop 页面结构分析结果

### 商品创建页面 (`/product/create`)

**URL**: `https://seller.tiktokshopglobalselling.com/product/create?shop_region=VN`

**文件上传元素** (共4个):
| 索引 | accept | 用途推测 |
|------|--------|----------|
| 0 | `.jpg,.png,.jpeg` | 商品主图 |
| 1 | `image/*` | 图片上传 |
| 2 | `image/*` | 图片上传 |
| 3 | `.mp4,.avi,.mkv,.mov` | 视频上传 |

**主要 Upload 类名**:
- `pulse-upload`
- `core-upload`
- `_uploadContainer_by3vm_401`

**输入框** (共12个):
- 商品名称输入框：支持中文输入，自动翻译越南语
- 类目选择：`core-select` 类

### 媒体中心页面 (`/product/materialSender`)

**URL**: `https://seller.tiktokshopglobalselling.com/product/materialSender?shop_region=VN`

**用途**: 上传图片/视频到媒体库

**发现**:
- 页面动态渲染，初始只有少量元素
- 侧边栏菜单包含商品管理、添加商品、媒体中心等

---

## 字段映射设计

### 当前映射

| TikTok 字段 | 货源字段 | 状态 |
|-------------|----------|------|
| 基本信息-图片(1张) | `sourcing_1688.image_url` | ✅ 已确认 |
| 基本信息-商品名称 | `sourcing_1688.title` | ✅ 已确认 |
| 类目 | - | 空着不填 |
| 商品详情-描述 | `sourcing_1688.description` | ⏳ 待开发（需修改1688插件） |
| 商品详情-图片 | - | ⏳ 待开发（生图功能） |
| 商品详情-视频 | - | 🔬 预研（本地视频上传） |

### 输入语言

- 顶部输入语言：中文
- 自动翻译：越南语

---

## 技术方案讨论

### 方案 A: 直接创建商品草稿

在 `/product/create` 页面直接上传图片并填入信息。

**优点**: 一条流程完成
**缺点**: 上传逻辑可能复杂

### 方案 B: 先上传到媒体库

先在 `/product/materialSender` 上传图片，然后在商品创建时从媒体库选择。

**优点**: 媒体库上传简单，后续插入方便
**缺点**: 需要两步流程

**决策**: 先研究方案 A 的可行性，如果直接上传不难则采用 A。

---

## 实施进度

| 阶段 | 状态 | 说明 |
|------|------|------|
| 页面分析方法 | ✅ 完成 | CDP 连接 + Playwright 分析脚本 |
| 媒体中心页面分析 | ✅ 完成 | HTML + 截图已保存 |
| 商品创建页面分析 | ✅ 完成 | 发现4个文件上传 input |
| 字段映射设计 | ✅ 完成 | 基本字段已确认 |
| 直接上传可行性研究 | ✅ 完成 | input[type=file] 上传成功 |
| 自动化脚本开发 | 🔜 待开始 | 填入名称 + 上传图片 |
| 1688 描述抓取 | 🔜 待开始 | 修改 1688 插件 |
| 生图/生视频集成 | 🔜 待开始 | 多图上传功能 |

---

## 测试结果

### 2026-06-04 测试

**测试货源**: ECTK26000401 - QIC新款双头二叉眉笔

**结果**:
- ✅ 图片上传成功（使用 `input[type=file][accept*='.jpg']`）
- ✅ 商品名称填入成功
- ✅ 找到「另存为草稿」按钮

**关键技术点**:
```python
# 1. 找到文件上传 input
file_input = await page.query_selector("input[type='file'][accept*='.jpg']")

# 2. 上传本地图片
await file_input.set_input_files(str(image_path))

# 3. 填入商品名称
await name_input.fill(title[:100])
```

**决策**: 采用方案 A（直接在商品创建页面上传图片），无需预上传到媒体库。

## 下一步行动

1. ✅ **测试直接上传图片** - 已完成
2. ✅ **实现基本字段填入** - 商品名称 + 图片上传已完成
3. 🔜 **完善自动化脚本** - 添加保存草稿逻辑、错误处理
4. 🔜 **修改 1688 插件** - 抓取商品详情页描述
5. 🔜 **集成生图功能** - 多图上传

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `scripts/tiktok_browser.py` | 页面分析脚本 |
| `scripts/material_center_html.txt` | 媒体中心 HTML |
| `scripts/product_create_html.txt` | 商品创建 HTML |
| `scripts/*.png` | 页面截图 |
| `docs/TikTok-Automation.md` | 本文档 |