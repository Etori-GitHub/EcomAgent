# EcomAgent - 电商智能体

**项目描述：** 飞书电商助手，自动处理产品图片生成营销素材（9宫格图片 + 视频）+ 智能选品+货源对接系统

**最后更新：** 2026-03-14  
**状态：** ✅ 生图/生视频功能已重构完成，监听脚本职责分离，日志清晰可读

---

## 更新日志

### 2026-03-14
- ✅ Monitor 职责分离重构完成
  - 监听脚本只做调度（监听→识别→启动脚本）
  - 功能脚本自己负责生成+发送结果
  - 删除 `_parse_result()` 和 `_send_results_to_user()` 方法
  - 所有 `✓` / `✗` / `⚠` 替换为 `[OK]` / `[ERR]` / `[WARN]`
- ✅ 修复飞书消息发送问题
  - `feishu.py` 使用 `subprocess.run` 替代 `os.system`
  - 添加 `--channel feishu` 参数支持多 channel 配置
- ✅ 修复队列消息格式解析，正确提取 `user_id`
- 🚧 智能选品模块开发中（架构设计完成）

### 2026-03-12
- 🚧 新增智能选品模块架构设计（三阶段异步流程）
- 🚧 亚马逊/TikTok热销数据抓取模块
- 🚧 1688货源搜索模块
- 🚧 数据库设计（A库/B库/C库分层架构）
- 🚧 商品聚合去重逻辑（品名+规格）
- 🚧 多货源管理（防断货策略）

### 2026-03-10
- ✅ 场景图/视频/广告词实时发送（生成一个发一个，不等全部完成）
- ✅ 添加 `video_v2` 触发词区分单视频和3视频版本
- ✅ Flash Image Provider 重试机制增强（5次重试，指数退避 5s/10s/15s/20s）
- ✅ 场景图生成重试机制（5次重试 + 图间3秒延迟，防API限流）
- ✅ 修复 monitor 硬编码调用问题，支持根据 triggers.json 配置动态调用

### 2026-03-08
- ✅ 修复 monitor.py 编码错误（Windows GBK 解码问题）
- ✅ 简化视频提示词（删除产品互动描述，保留中心突出展示）
- ✅ 视频生成功能稳定运行

---

## 依赖库安装

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

## 快速开始（生图/生视频）

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

### 测试功能
```bash
# 测试生图
python test\test_full_flow.py

# 测试生视频 V2（3图3视频合成版）
python test\test_video_flow_v2.py
```

---

## 项目状态

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
| **智能选品模块** | 🚧 开发中 | 三阶段异步流程架构设计完成 |
| 亚马逊热销数据抓取 | 🚧 开发中 | 待实现 |
| TikTok热销数据抓取 | 🚧 开发中 | 待实现 |
| 数据库设计 | 🚧 开发中 | A库/B库/C库分层架构 |
| 商品聚合去重 | 🚧 开发中 | 品名+规格聚合逻辑 |
| 1688货源搜索 | 🚧 开发中 | 多商家列表管理 |
| 妙手ERP对接 | 🚧 开发中 | 草稿箱更新接口 |

---

## 智能选品模块核心逻辑（开发中）

### 1. 重复商品聚合
- **标识规则**：【品名+规格】（如：东方树叶茉莉花茶500ml）
- **销量合并**：A库销量 + B库销量 = 聚合销量
- **去重策略**：相同标识的商品合并为一条记录

### 2. 爆品筛选
- **条件**：A库销量高 + B库销量低
- **标记**：在C库中标记为"潜力爆品"
- **用途**：优先寻找货源，快速上架

### 3. 多货源策略
- **1688搜索**：按【品名+规格】搜索
- **商家列表**：保存多个商家信息（价格、库存、信誉）
- **防断货**：至少保存3个商家，避免单卖家断货

### 4. 数据库设计
| 库名 | 用途 | 关键字段 |
|------|------|----------|
| A库 | 亚马逊热销数据 | 商品ID、名称、规格、销量、价格、链接 |
| B库 | TikTok热销数据 | 商品ID、名称、规格、销量、价格、链接 |
| C库 | 主库（状态中心） | 商品ID、聚合销量、货源状态、1688链接列表、上架状态 |

---

## 关键配置

### API Keys - config/api_keys.json
```json
{
    "google": "your-google-api-key",
    "grok": "your-grok-api-key"
}
```

### 模型配置 - config/models.json
```json
{
  "image_providers": {
    "flash_image": {
      "model": "gemini-2.0-flash-exp-image-generation"
    }
  },
  "video_providers": {
    "grok": {
      "model": "grok-2-video"
    }
  },
  "gemini": {
    "model": "gemini-2.5-flash"
  }
}
```

### 触发词配置 - config/triggers.json
```json
{
  "triggers": {
    "image": {
      "name": "生成图片",
      "script": "generate_images.py",
      "keywords": ["作图", "生图", "生9图", "9图", "生成图片"],
      "description": "生成9张电商营销图"
    },
    "video": {
      "name": "生成视频",
      "script": "generate_video_v2.py",
      "keywords": ["生视频", "视频", "生成视频"],
      "description": "生成3图3视频合成版"
    }
  },
  "settings": {
    "cache_expire_minutes": 10,
    "case_sensitive": false
  }
}
```

---

## 项目结构

```
EcomAgent/
├── README.md                 # 本文件
├── start_gateway.ps1         # 启动脚本（仅启动 Gateway）
├── config/                   # 配置文件
│   ├── api_keys.json         # API密钥（gitignore）
│   ├── models.json           # 模型配置
│   ├── templates.json        # 9图模板配置
│   └── triggers.json         # 触发词配置
├── src/                      # 源码
│   ├── monitor.py            # 飞书监听服务（改进版日志）
│   ├── generate_images.py    # 生9图功能
│   ├── generate_video.py     # 生视频功能（单视频版）
│   ├── generate_video_v2.py  # 生视频功能 V2（3图3视频合成版）
│   ├── generate_video_v2_backup.py  # V2备份
│   ├── providers/            # Provider实现
│   │   ├── base.py           # 基础Provider接口
│   │   ├── flash_image.py    # Google Flash Image（带重试机制）
│   │   ├── gemini_prompt.py  # Gemini提示词优化（含比例约束）
│   │   └── grok_video.py     # Grok视频生成
│   └── utils/                # 工具层
│       ├── logger.py         # 日志工具
│       ├── feishu.py         # 飞书消息发送
│       └── video_merger.py   # 视频合并工具
├── ecommerce/                # 智能选品模块
│   ├── config/               # 配置文件
│   │   ├── db_config.json    # 数据库配置
│   │   └── supplier_rules.json  # 货源搜索规则
│   ├── src/                  # 源码
│   │   ├── data_fetcher/     # 数据抓取模块
│   │   │   ├── amazon.py     # 亚马逊热销数据抓取
│   │   │   └── tiktok.py     # TikTok热销数据抓取
│   │   ├── database/         # 数据库模块
│   │   │   ├── base.py       # 数据库基类
│   │   │   ├── a_db.py       # A库（亚马逊）
│   │   │   ├── b_db.py       # B库（TikTok）
│   │   │   └── c_db.py       # C库（主库）
│   │   ├── aggregator.py     # 商品聚合去重
│   │   ├── trending_scorer.py # 爆品评分
│   │   ├── supplier_search.py # 1688货源搜索
│   │   └── erp_sync.py       # 妙手ERP对接
│   └── test/                 # 测试
│       ├── test_data_fetcher.py
│       ├── test_aggregator.py
│       └── test_supplier_search.py
├── test/                     # 测试
│   ├── test_full_flow.py     # 完整流程测试
│   ├── test_video.py         # 视频生成测试
│   └── img/                  # 测试图片
├── output/                   # 输出文件
│   └── YYYYMMDD_HHMMSS/      # 每次执行结果
│       ├── images/           # 生成的9张图
│       ├── scene_01~03.png   # 3张场景图（V2）
│       ├── prompts_01~03.txt # 3套提示词（V2）
│       ├── ad_script.txt     # 广告词文案（V2）
│       ├── video_01~03.mp4   # 3段视频（V2）
│       ├── video_merged.mp4  # 合成视频（V2）
│       └── result.json       # 结果记录
├── logs/                     # 日志
│   └── YYYYMMDD.log          # 运行日志
└── temp/                     # 临时文件
    └── image_cache.json      # 图片缓存
```

---

## 核心流程

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

## 3套场景风格（V2版）

| 风格 | 名称 | 场景描述 |
|------|------|----------|
| 1 | 简约现代 | 白色大理石台面，自然日光，北欧极简内饰，专业工作室氛围 |
| 2 | 奢华高端 | 深色胡桃木桌面，温暖环境光，奢华质感，高端产品展示 |
| 3 | 生活化场景 | 温馨家居环境，自然生活化布置，真实使用场景 |

---

## 重试机制说明

### Flash Image Provider（场景图生成）
- **重试次数**: 5次
- **等待时间**: 5s → 10s → 15s → 20s（指数退避）
- **原因**: VPN不稳定，增加冗余时间

### 场景图批量生成
- **单图重试**: 5次
- **图间延迟**: 3秒（防API限流）

---

## 监听服务日志说明

改进后的 `monitor.py` 提供清晰的日志输出：

```
[2026-03-08 02:00:48] [Init] 项目根目录: C:\Users\etori\.openclaw\workspace\code\EcomAgent
[2026-03-08 02:00:48] [Init] 日志文件: logs\gateway.log
[2026-03-08 02:00:48] [Config] 加载配置: 2个触发器, 6个关键词
[2026-03-08 02:00:48] [Cache] 加载缓存: 0个有效
[2026-03-08 02:00:48] [Start] 监听服务启动
[2026-03-08 02:00:48] [Start] 使用编码: utf-8
[2026-03-08 02:00:48] [Start] 文件大小: 1234 bytes，从末尾开始监听
[2026-03-08 02:00:48] [Start] 等待飞书消息...

[2026-03-08 02:01:15] [Raw] Image saved: media/inbound/abc123.png for user ou_xxx...
[2026-03-08 02:01:15] [Parse] 检测到图片: user=ou_xxx
[2026-03-08 02:01:15] [Cache] ✓ 缓存图片: user=ou_xxx, path=media/inbound/abc123.png

[2026-03-08 02:01:30] [Raw] Feishu[default] DM from ou_xxx: 作图
[2026-03-08 02:01:30] [Parse] 检测到消息: user=ou_xxx, content='作图'
[2026-03-08 02:01:30] [Trigger] ✓ 匹配触发词 'image': user=ou_xxx
[2026-03-08 02:01:30] [Exec] 调用脚本: generate_images.py
[2026-03-08 02:01:30] [Exec] 命令: python src/generate_images.py --image ...
[2026-03-08 02:01:30] [Exec] ✓ 进程已启动: PID=12345
[2026-03-08 02:01:30] [Cache] ✗ 清除缓存: user=ou_xxx
[2026-03-08 02:01:30] [Trigger] ✓ 已触发并清除缓存: user=ou_xxx
```

**日志标签说明：**
- `[Init]` - 初始化信息
- `[Config]` - 配置加载
- `[Cache]` - 缓存操作（✓ 设置/✗ 清除/过期）
- `[Start]` - 服务启动
- `[Raw]` - 原始日志行
- `[Parse]` - 解析结果
- `[Trigger]` - 触发词匹配
- `[Exec]` - 脚本执行
- `[Error]` - 错误信息
- `[Heartbeat]` - 心跳（每30秒）

---

## 视频生成参数

### 单视频版（generate_video.py）
- **时长**: 5秒
- **分辨率**: 720p
- **比例**: 9:16（竖屏，适合抖音/小红书）
- **比例约束**: Gemini 自动生成动态比例参照

### V2版（generate_video_v2.py）
- **单段时长**: 5秒
- **总时长**: 15秒（3段合成）
- **分辨率**: 480p/720p 可选
- **比例**: 9:16（竖屏）
- **语音**: 每段带独立语音朗读（5秒广告词）
- **广告词**: 15秒完整文案，自动分段（每段约5秒）

---

## 提示词模板

### 场景图提示词（V2）
```
Create a premium advertising product photography scene for: {product_desc}

Scene Style: {style_name} - {scene_desc}
Lighting: {light_desc}

CRITICAL REQUIREMENTS:
- Premium advertising aesthetic with world-class photography quality
- Fixed 9:16 vertical aspect ratio composition optimized for mobile viewing
- Subject positioned as the clear focal point commanding viewer attention
- Clean, uncluttered composition with sophisticated depth of field
- Professional color grading with cinematic tonal balance
- No text, watermarks, or UI elements
- Photorealistic rendering with meticulous attention to material textures
```

### 视频提示词（带比例约束）
```
CRITICAL PROPORTION CONSTRAINTS:
- Analyze the product in the reference image and maintain its exact real-world proportions
- Human hands, if shown interacting with the product, must be anatomically correct and proportionally realistic
- The product should never appear unnaturally large or small relative to human scale
- Maintain consistent perspective and depth throughout the video
- NEVER create "tiny hands holding giant objects" or disproportionate scaling effects
- The product and any human elements must coexist in believable, physically accurate scale
```

---

## 故障排查

### Server disconnected without sending a response
- **原因**: Flash Image API 连接断开（VPN不稳定）
- **解决**: 已添加5次重试机制，如仍失败请检查 VPN 稳定性

### 视频生成失败
- **检查**: Grok API Key 是否有效
- **检查**: 输入图片格式是否支持（JPG/PNG）

### 飞书消息未触发
- **检查**: monitor.py 是否正常运行
- **检查**: triggers.json 配置是否正确
- **检查**: 图片缓存是否过期（默认10分钟）

---

## 智能选品模块（开发中）

### 架构设计

**三阶段异步流程：**

```
阶段1：数据抓取
├─ A库（亚马逊热销数据）
└─ B库（TikTok热销数据）

阶段2：智能筛选
├─ 聚合去重（品名+规格）
├─ 销量合并统计
└─ C库（主库，标记爆品+货源状态）

阶段3：货源对接
├─ 1688货源搜索
├─ 多商家列表（防断货）
└─ 妙手ERP对接（草稿箱更新）
```

### 数据库设计

| 库名 | 用途 | 关键字段 |
|------|------|----------|
| A库 | 亚马逊热销数据 | 商品ID、名称、规格、销量、价格、链接 |
| B库 | TikTok热销数据 | 商品ID、名称、规格、销量、价格、链接 |
| C库 | 主库（状态中心） | 商品ID、聚合销量、货源状态、1688链接列表、上架状态 |

### 核心逻辑

1. **重复商品聚合**：以【品名+规格】为唯一标识，合并A库+B库销量
2. **爆品筛选**：A库销量高 + B库销量低 → 标记为"潜力爆品"
3. **多货源策略**：1688搜索结果存为列表，避免单卖家断货风险
4. **状态追踪**：C库记录货源链接、上架状态、最后更新时间

---

## 开发计划

- [ ] 视频生成添加更多时长选项（3秒/10秒）
- [ ] 支持自定义场景风格模板
- [ ] 添加视频背景音乐选项
- [ ] 支持批量产品处理
- [ ] 亚马逊热销数据抓取模块
- [ ] TikTok热销数据抓取模块
- [ ] 数据库设计与实现
- [ ] 商品聚合去重逻辑
- [ ] 1688货源搜索模块
- [ ] 妙手ERP对接模块

---

## 开发规范

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
- **输出格式**：统一输出 `[RESULT_MARKER]` 格式的 JSON 结果（如 `[GENERATION_RESULT]` / `[VIDEO_RESULT]` / `[TEST_MODE_RESULT]`）

---

## OpenClaw 技能配置（软链接）

### 为什么需要软链接？

OpenClaw 的技能默认从全局目录 `/opt/homebrew/lib/node_modules/openclaw/skills/` 加载，但：
- 全局目录是 npm 包的一部分，升级时会被覆盖
- 你的自定义技能应该用 Git 管理，放在项目里

**解决方案：软链接** - 让 OpenClaw 从项目目录读取技能。

### 设置步骤

1. **确保技能放在项目目录**
   ```
   /Users/etori/.openclaw/workspace/code/EcomAgent/skills/
   └── amazon-fetcher/
       └── SKILL.md
   ```

2. **创建软链接**
   ```bash
   # 进入 OpenClaw 全局技能目录
   cd /opt/homebrew/lib/node_modules/openclaw/skills/
   
   # 创建软链接（指向项目技能目录）
   ln -sf /Users/etori/.openclaw/workspace/code/EcomAgent/skills/amazon-fetcher amazon-fetcher
   ```

3. **验证软链接**
   ```bash
   ls -la amazon-fetcher
   # 应该显示：lrwxr-xr-x ... amazon-fetcher -> /Users/etori/.openclaw/workspace/code/EcomAgent/skills/amazon-fetcher
   ```

4. **测试技能**
   ```bash
   # 在 OpenClaw 中调用技能
   /fetch_amazon_bestsellers
   ```

### 重装系统/换环境时的恢复步骤

```bash
# 1. 克隆项目
git clone https://github.com/your-repo/EcomAgent.git
cd EcomAgent

# 2. 设置技能目录
mkdir -p /Users/etori/.openclaw/workspace/code/EcomAgent/skills
cp -r skills/* /Users/etori/.openclaw/workspace/code/EcomAgent/skills/

# 3. 重新创建软链接
cd /opt/homebrew/lib/node_modules/openclaw/skills/
ln -sf /Users/etori/.openclaw/workspace/code/EcomAgent/skills/amazon-fetcher amazon-fetcher
```

### 注意事项

- ✅ 软链接是安全的，OpenClaw 升级不会删除它
- ✅ 用 Git 管理技能目录，方便团队协作
- ✅ 如果技能目录名不同，软链接名要和目录名一致

---

## 智能选品模块 - 数据库设计

### 数据库方案
- **类型**: SQLite（轻量级，单文件数据库）
- **位置**: `data/amazon.db`
- **跨平台**: ✅ 支持 Windows/macOS/Linux

### 表结构

#### `products` - 商品基础信息表
| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `id` | INTEGER PRIMARY KEY | 主键 |
| `name` | TEXT NOT NULL UNIQUE | 商品名称（唯一） |
| `asin` | TEXT | 亚马逊商品ID |
| `platform` | TEXT DEFAULT 'amazon' | 平台标识 |
| `created_at` | DATETIME | 创建时间 |

#### `daily_sales` - 每日销量快照表
| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `id` | INTEGER PRIMARY KEY | 主键 |
| `product_id` | INTEGER NOT NULL | 商品ID（外键） |
| `date` | DATE NOT NULL | 日期（YYYY-MM-DD） |
| `sales` | INTEGER | 当日销量 |
| `price` | REAL | 价格 |
| `rank` | INTEGER | 排名 |
| `created_at` | DATETIME | 创建时间 |

### 索引
- `idx_sales` - 按销量排序
- `idx_platform` - 按平台过滤
- `idx_date` - 按日期查询
- `idx_product_date` - 按商品+日期复合查询

### 爆品判断逻辑（后续实现）
- **销量趋势**: 7天销量增速
- **波动率**: 销量标准差/平均值
- **综合评分**: 增速权重 70% + 稳定性权重 30%

### 自动化计划
- **频率**: 每天凌晨 2:00
- **数据量**: Top200 商品
- **存储**: 每日快照，长期积累