# Phase 2 - 素材生成与管理

## 功能概述

为 EcomAgent 货源库添加素材生成和管理功能，支持生成展示图、宣传视频、详情图，并管理生成的素材用于 TikTok 上传。

## 更新日期

2026-06-17

---

## 一、素材类型

| 类型 | 英文 | 说明 | 生成脚本 |
|------|------|------|----------|
| 展示图 | showcase | 首帧模特图，用于商品主图 | `generate_images.py` |
| 宣传视频 | video | 15秒连续营销视频（3段5秒） | `generate_video_v3.py` |
| 详情图 | detail | 9张电商营销图 | `generate_images.py` |

---

## 二、文件结构

### 新增文件

```
EcomAgent/
├── src/
│   └── data_viewer/
│       ├── asset_service.py      # 素材管理服务
│       ├── task_queue.py         # 任务队列
│       ├── asset_models.py       # 数据模型
│       └── main.py               # 新增素材 API 端点
├── ui/
│   └── src/
│       └── pages/
│           └── asset-manager.ts  # 素材管理前端组件
└── data/
    └── assets/                   # 素材存储目录
        └── {ecom_code}/
            ├── showcase/
            │   └── group_1/
            │       └── *.png
            ├── video/
            │   └── group_1/
            │       ├── model_frame.png
            │       ├── video_01.mp4
            │       ├── video_02.mp4
            │       ├── video_03.mp4
            │       └── video_merged.mp4
            └── detail/
                └── group_1/
                    └── *_marketing.png
```

### 数据库

`data/assets.db` - 素材记录表：

```sql
CREATE TABLE sourcing_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ecom_code TEXT NOT NULL,
    asset_type TEXT NOT NULL,      -- showcase | video | detail
    group_index INTEGER NOT NULL,  -- 分组编号
    files TEXT NOT NULL,           -- JSON 文件列表
    params TEXT,                   -- 生成参数
    task_id TEXT,                  -- 关联任务 ID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ecom_code, asset_type, group_index)
)
```

---

## 三、API 端点

### 素材管理

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/assets/{ecom_code}` | 获取货源的所有素材 |
| GET | `/api/assets/{ecom_code}/stats` | 获取素材统计 |
| DELETE | `/api/assets/{ecom_code}/{asset_type}/{group_index}` | 删除素材组 |
| POST | `/api/assets/scan/{ecom_code}` | 扫描磁盘素材同步到数据库 |

### 生成任务

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/assets/generate/video` | 生成宣传视频 |
| POST | `/api/assets/generate/image` | 生成展示图或详情图 |

**请求参数**：

```json
// 生成视频
{
  "ecom_code": "xxx",
  "image_path": null,      // 可选，不传则用货源图片
  "duration": 5,           // 每段时长（秒）
  "resolution": "480p"     // 480p | 720p
}

// 生成图片
{
  "ecom_code": "xxx",
  "image_path": null,      // 可选
  "asset_type": "detail"   // showcase | detail
}
```

### 任务状态

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/tasks/{task_id}` | 查询任务状态 |
| GET | `/api/tasks` | 任务列表（最近20个） |

**任务状态**：
- `pending` - 等待执行
- `running` - 执行中
- `success` - 成功
- `failed` - 失败

---

## 四、前端界面

### 货源库页面

每行新增「素材」按钮（紫色），点击打开素材管理弹窗。

### 素材管理弹窗

```
┌─────────────────────────────────────┐
│ 📁 素材管理                    [×]  │
├─────────────────────────────────────┤
│ 商品: xxx                           │
│                                     │
│ 展示图 (0组)            [+ 生成]    │
│   暂无素材                          │
│                                     │
│ 宣传视频 (2组)          [+ 生成]    │
│   组1: 5个文件  [预览] [删除]       │
│   组2: 5个文件  [预览] [删除]       │
│                                     │
│ 详情图 (1组)            [+ 生成]    │
│   组1: 9个文件  [预览] [删除]       │
└─────────────────────────────────────┘
```

### 生成弹窗

点击「+ 生成」后弹出：

```
┌─────────────────────────────────────┐
│ 🎬 生成宣传视频                     │
├─────────────────────────────────────┤
│ 图片来源：                          │
│   ○ 使用货源图片                    │
│   ○ 上传自定义图片                  │
│                                     │
│ 视频时长：[5秒/段（共15秒）▼]       │
│ 分辨率：  [480p（更快）▼]           │
│                                     │
│ ████████████░░░░░░ 60%              │
│ 正在生成第2段视频...                │
│                                     │
│         [取消]  [开始生成]          │
└─────────────────────────────────────┘
```

---

## 五、技术实现

### 任务队列

使用内存队列（`task_queue.py`），避免 Redis 依赖：

1. `TaskQueue` 单例类管理任务
2. 后台线程执行生成脚本
3. 轮询 `GET /api/tasks/{task_id}` 获取状态

### 脚本调用

通过 `subprocess` 调用生成脚本：

```python
cmd = [
    sys.executable,
    "src/generate_video_v3.py",
    "--image", image_path,
    "--duration", "5",
    "--resolution", "480p",
    "--output_dir", output_dir
]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
```

### 素材存储

- 生成脚本输出到 `data/assets/{ecom_code}/{type}/group_{n}/`
- 生成完成后保存记录到 `sourcing_assets` 表
- 删除时同时删除数据库记录和磁盘文件

---

## 六、待完成功能

### TikTok 上传集成

上传时检查素材：
- 如果只有一组 → 自动选择
- 如果有多组 → 弹窗让用户选择
- 如果没有 → 不上传

### 自定义图片上传

当前只支持使用货源图片，后续支持：
- 用户上传自定义图片
- 图片预览和裁剪

### 批量生成

- 一键生成所有素材类型
- 批量生成多个货源

---

## 七、测试方法

1. 启动服务：
   ```bash
   cd EcomAgent
   python run_viewer.py
   ```

2. 访问货源库页面：`http://127.0.0.1:8000` → 货源库

3. 点击任意货源的「素材」按钮

4. 在弹窗中点击「+ 生成」测试生成功能

---

## 八、注意事项

1. **生成时间**：视频生成约需 3-5 分钟，图片约 2-3 分钟
2. **API 限制**：Gemini 和 Grok 都有速率限制，生成时需等待
3. **图片来源**：确保货源有 `local_image_path`，否则无法生成
4. **任务超时**：默认 10 分钟超时，可在 `task_queue.py` 调整
