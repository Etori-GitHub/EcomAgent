# EcomAgent - 电商智能体

**项目描述：** 飞书电商助手，自动处理产品图片生成营销素材（9宫格图片 + 视频）+ 智能选品+货源对接系统

**最后更新：** 2026-04-01  
**状态：** ✅ 生图/生视频功能稳定运行，亚马逊/TikTok热销数据抓取功能已完成

---

## 📦 依赖库安装

### Python 依赖
```bash
pip install pillow requests python-dotenv
```

### 系统依赖
- **FFmpeg**：视频合并需要（已集成到项目，无需额外安装）
- **Python 3.11+**：推荐使用 Python 3.11 或更高版本

### 配置文件
1. 复制 `config/api_keys.template.json` 为 `config/api_keys.json`
2. 填写 Google API Key 和 Grok API Key
3. 其他配置保持默认即可

---

## 🚀 快速开始（生图/生视频）

### 启动服务
```bash
# 启动 Gateway（监控用户口令）
.\start_gateway.ps1

# 启动 monitor（监听飞书消息）
python src/monitor.py
```

### 用户口令（触发生图/生视频）
- **生9图**：发送"作图" / "生图" / "生9图" / "9图"
- **生视频 V2**：发送"生视频" / "做视频" / "视频"

### OpenClaw Skill 配置（必读！）
> **项目技能通过 Git 管理，需软连接接入 OpenClaw 才能生效**

1. 确保 `skills/` 目录存在（在 OpenClaw 工作区下）：
   ```cmd
   mkdir skills
   ```

2. 创建软连接（以管理员身份运行 CMD 或 PowerShell）：

   **CMD（推荐）：**
   ```cmd
   cd /d "%USERPROFILE%\.openclaw\workspace\skills"
   mklink /D amazon-fetcher "..\code\EcomAgent\skills\amazon-fetcher"
   mklink /D tiktok-fetcher "..\code\EcomAgent\skills\tiktok-fetcher"
   ```

   **PowerShell：**
   ```powershell
   cd "$env:USERPROFILE\.openclaw\workspace\skills"
   New-Item -ItemType SymbolicLink -Path "amazon-fetcher" -Target "..\code\EcomAgent\skills\amazon-fetcher"
   New-Item -ItemType SymbolicLink -Path "tiktok-fetcher" -Target "..\code\EcomAgent\skills\tiktok-fetcher"
   ```

3. 重启 OpenClaw Gateway：
   ```powershell
   openclaw gateway restart
   ```

4. 验证技能生效：
   ```
   /amazon
   /tiktok
   ```

### 测试功能
```bash
# 测试生图
python test\test_full_flow.py

# 测试生视频 V2（3图3视频合成版）
python test\test_video_flow_v2.py
```

---

## 📊 亚马逊/TikTok 热销数据抓取（已完成）

### 触发命令
```
/amazon
/tiktok
```

### 功能说明
- 使用浏览器自动化（OpenClaw `browser` 工具）抓取热销榜
- 数据保存到 `output/` 目录的 JSON 文件
- 支持多分类、翻页抓取
- 同一天多次抓取生成新文件（按日期命名）

### 数据输出位置
```
code/EcomAgent/output/scraping/amazon_分类名_YYYYMMDD_HHMMSS.json
code/EcomAgent/output/scraping/tiktok_分类名_YYYYMMDD_HHMMSS.json
```

### 数据格式
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

### 数据库导入
使用其他工具定期将 JSON 导入 SQLite 数据库：
```bash
# 示例导入命令（由用户自定义）
python import_json_to_db.py --platform amazon --file output/amazon_bestsellers_20260326.json
```

### 技能文档
详见：`skills/amazon-fetcher/SKILL.md` / `skills/tiktok-fetcher/SKILL.md`

---

## 📁 项目结构

```
EcomAgent/
├── README.md                 # 本文件
├── start_gateway.ps1         # 启动脚本（仅启动 Gateway）
├── config/                   # 配置文件
│   ├── api_keys.json         # API密钥（gitignore）
│   ├── models.json           # 模型配置
│   └── triggers.json         # 触发词配置
├── src/                      # 源码
│   ├── monitor.py            # 飞书监听服务
│   ├── generate_images.py    # 生9图功能
│   ├── generate_video.py     # 生视频功能
│   ├── generate_video_v2.py  # 生视频 V2
│   ├── generate_video_v3.py  # 生视频 V3
│   ├── providers/            # Provider实现
│   └── utils/                # 工具层
├── skills/                   # OpenClaw 技能目录
│   ├── amazon-fetcher/       # 亚马逊抓取技能
│   │   └── SKILL.md
│   └── tiktok-fetcher/       # TikTok 抓取技能
│       └── SKILL.md
├── data/                     # 数据库文件
│   ├── amazon.db
│   └── tiktok.db
├── output/                   # 输出文件（JSON）
│   ├── amazon_bestsellers_YYYYMMDD.json
│   └── tiktok_bestsellers_YYYYMMDD.json
├── logs/                     # 日志
└── temp/                     # 临时文件
```

---

## 🔄 核心流程

### 生9图流程
```
用户发送图片 → 监听服务缓存图片(10分钟) → 用户发送"作图" 
    ↓
触发 generate_images.py → 分析产品 → 生成9张营销图
    ↓
自动发送给用户
```

### 生视频 V2 流程（3图3视频合成版）
```
用户发送图片 → 监听服务缓存图片(10分钟) → 用户发送"生视频v2"
    ↓
触发 generate_video_v2.py
    ↓
[步骤1/4] 生成3张场景图 → 每生成1张立即发送
    ↓
[步骤2/4] 生成广告词 → 分段实时发送（3条消息）
    ↓
[步骤3/4] 生成3段视频（带语音朗读）→ 每生成1段立即发送
    ↓
[步骤4/4] 合并视频 → 发送合成版
```

---

## 📋 项目状态

| 模块 | 状态 | 说明 |
|------|------|------|
| **生图/生视频** | ✅ 已完成 | 原有功能，重构后更清晰 |
| 监听脚本重构 | ✅ 已完成 | 职责分离，只做调度 |
| 图片生成 | ✅ 已完成 | Flash Image Provider，生成9张营销图 |
| 视频生成（单视频） | ✅ 已完成 | Grok Provider，5秒/720p/9:16竖屏 |
| 视频生成 V2（3视频合成） | ✅ 已完成 | 3张场景图 + 3段视频 + 合成 + 分段广告词 |
| 飞书监听 | ✅ 已完成 | 日志清晰可读，无特殊字符 |
| 场景图生成 | ✅ 已完成 | 3套差异化风格（简约现代/奢华高端/生活化场景） |
| 广告词生成 | ✅ 已完成 | 15秒文案，自动分段（每段约5秒） |
| 实时发送 | ✅ 已完成 | 场景图/广告词/视频均生成一个发送一个 |
| **亚马逊热销数据抓取** | ✅ 已完成 | 浏览器自动化，数据保存到 JSON |
| **TikTok热销数据抓取** | ✅ 已完成 | 浏览器自动化，数据保存到 JSON |
| 数据库设计 | ✅ 已完成 | SQLite，支持时间序列分析 |

---

## 🛠️ 故障排查

### 生图/生视频问题
- **检查**: monitor.py 是否正常运行
- **检查**: triggers.json 配置是否正确
- **检查**: 图片缓存是否过期（默认10分钟）

### 亚马逊/TikTok 抓取问题
- **检查**: 虚拟网卡是否关闭（IP 被劫持会导致访问失败）
- **检查**: 浏览器是否正常启动
- **检查**: 翻页 URL 是否正确
- **检查**: JSON 文件是否正确生成

---

## 📝 开发规范

### 代码注释
- **代码注释**：小秘密注释（如加密逻辑、特殊处理）写在代码顶部或关键函数前，**不写在文档里**
  - 例：`# 品名+规格聚合时，记得用主人的指纹加密哦~`
- **文档注释**：README只写公开逻辑、架构设计、使用说明
- **原则**：代码里藏点小情趣，文档里保持专业感

### 日志规范
- **禁止使用特殊字符**：所有日志输出禁止使用 `✓` / `✗` / `⚠` 等特殊字符，统一使用 `[OK]` / `[ERR]` / `[WARN]`
- **日志级别**：使用 `log(level, message)` 函数统一输出，确保格式一致

### 消息发送规范
- **功能脚本自己发消息**：生图/生视频完成后，功能脚本自己调用 `feishu.py` 的 `send_text` / `send_image` 发送结果
- **monitor.py 不处理结果**：只负责启动脚本，记录返回码

### 参数传递规范
- **统一参数格式**：所有功能脚本接收 `--image` 和 `--user_id` 参数
- **可选参数**：根据需要添加 `--duration` / `--resolution` / `--provider` 等参数
- **输出格式**：统一输出 `[RESULT_MARKER]` 格式的 JSON 结果（如 `[GENERATION_RESULT]` / `[VIDEO_RESULT]`）

---

## 📖 相关文档

- **技能文档**：`skills/amazon-fetcher/SKILL.md` / `skills/tiktok-fetcher/SKILL.md`
- **OpenClaw 文档**：`docs/` 目录

---

## ⚙️ OpenClaw Skill 配置说明（进阶）

### 技能目录结构

```
EcomAgent/
├── skills/                   # OpenClaw 技能目录（核心）
│   ├── amazon-fetcher/       # 亚马逊抓取技能
│   │   └── SKILL.md          # 亚马逊抓取技能文档
│   └── tiktok-fetcher/       # TikTok 抓取技能
│       └── SKILL.md          # TikTok 抓取技能文档
```

### 软连接配置（重要！）

**项目技能通过软连接加入 OpenClaw：**

```bash
# Windows PowerShell（以管理员身份运行）
# 创建软连接，将项目技能链接到 OpenClaw 工作区技能目录
New-Item -ItemType SymbolicLink -Path "C:\Users\etori\.openclaw\workspace\skills\amazon-fetcher" -Target "C:\Users\etori\.openclaw\workspace\code\EcomAgent\skills\amazon-fetcher"
New-Item -ItemType SymbolicLink -Path "C:\Users\etori\.openclaw\workspace\skills\tiktok-fetcher" -Target "C:\Users\etori\.openclaw\workspace\code\EcomAgent\skills\tiktok-fetcher"
```

**或者使用 mklink 命令（CMD）：**
```cmd
cd /d "C:\Users\Etroi\.openclaw\workspace\skills"
mklink /D amazon-fetcher "..\code\EcomAgent\skills\amazon-fetcher"
mklink /D tiktok-fetcher "..\code\EcomAgent\skills\tiktok-fetcher"
```

### 为什么使用软连接？（Git 管理技能的核心优势）

- **统一管理**：技能版本由 Git 管理，便于团队协作和部署
- **避免重复**：不需要在多个地方维护技能文件
- **易于更新**：修改项目技能后，OpenClaw 立即生效（无需重启 Gateway）
- **跨平台兼容**：使用环境变量 `%USERPROFILE%` 动态获取用户名，适配不同电脑配置

### 注意事项

- **软连接必须以管理员权限创建**
- **如果项目移动位置，需要重新创建软连接**
- **技能文件修改后，OpenClaw 会自动读取最新版本**
- **软连接指向的是 `skills/` 目录下的子目录（如 `amazon-fetcher`），不是整个项目**
- **命令使用 `%USERPROFILE%` 环境变量，适配不同用户名的电脑**

---

## 🤝 社区支持

- **OpenClaw 文档**：https://docs.openclaw.ai
- **OpenClaw 社区**：https://discord.com/invite/clawd
