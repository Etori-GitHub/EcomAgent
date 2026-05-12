# Monitor 重构计划

## 📌 背景

当前 `monitor.py` 混杂了太多职责：监听、缓存、解析结果、发送消息。导致逻辑复杂、难以维护。

目标：**职责分离**，`monitor.py` 只做调度，功能脚本自己负责全流程。

---

## 🏗️ 新架构设计

### 职责划分

| 组件 | 职责 | 不做 |
|------|------|------|
| `monitor.py` | 监听日志 → 识别触发词 → 缓存图片 → 启动脚本 → 清理缓存 | 结果解析、消息发送、复杂逻辑 |
| `generate_video_v2.py` | 接收参数 → 调用工具 → 生成 → 发送结果 | 依赖 monitor 解析 |
| `generate_images.py` | 接收参数 → 生成 → 逐张发送 → 输出结果 | 依赖 monitor 发送 |
| `test_mode.py` | 接收参数 → 测试生成 → 发送结果 | 依赖 monitor 发送 |
| `generate_video.py` | 保持原样（基础样例） | - |

---

## 🔄 消息流程

```
用户发消息（飞书）
    ↓
Gateway 日志记录消息 + 图片下载
    ↓
monitor.py 监听日志 → 提取 user_id + image_path + 消息内容
    ↓
检测触发词（作图/生视频/测试）
    ↓
subprocess.run(对应脚本 --image xxx --user_id xxx)
    ↓
功能脚本执行 → 生成文件 → 发送飞书消息 → 输出 [RESULT_MARKER]
    ↓
monitor.py 记录返回码（不处理结果）
```

---

## 📝 具体修改清单

### 1. `monitor.py`

#### 删除的方法
- `_parse_result()` → 移到各功能脚本
- `_send_results_to_user()` → 移到各功能脚本

#### 简化的方法
- `_process_message()`：只做触发词检测 + 启动脚本
- `_call_script()`：只负责 `subprocess.run()`，不处理返回

#### 保留的方法
- `ImageCache` / `TestModeCache`：缓存管理
- `TriggerConfig`：触发词配置
- `_check_log()` / `parse_line()`：日志监听

#### 新增的方法
- `_sanitize_log()`：统一日志内容清理，替换特殊字符为 ASCII
- `log_simple()`：简单日志输出，只清理特殊字符

#### 已完成修改
- ✅ 删除 `_parse_result()` 和 `_send_results_to_user()`
- ✅ 简化 `_process_message()` 只启动脚本
- ✅ 简化 `_call_script()` 只负责 subprocess.run
- ✅ 删除 `send_text` / `send_image` 导入（功能脚本自己导入）
- ✅ 所有 `✓` / `✗` / `⚠` 替换为 `[OK]` / `[ERR]` / `[WARN]`
- ✅ 修复 `feishu.py` 使用 `subprocess.run` 替代 `os.system`
- ✅ 修复 `feishu.py` 添加 `--channel feishu` 参数
- ✅ 修复队列消息格式解析，正确提取 `user_id`

---

### 2. `generate_video_v2.py`

#### 新增功能
- 接收参数：`--image`, `--user_id`, `--duration`, `--resolution`
- 生成完成后：
  - 解析结果（视频路径、场景图路径）
  - 发送场景图预览（飞书）
  - 发送视频文件（飞书，检查文件大小 ≤9.5MB）
  - 输出 `[VIDEO_RESULT]` 标记

#### 输出格式
```json
[VIDEO_RESULT] {"status": "success", "merged_video": "output/xxx.mp4", "scene_path": "output/xxx.png"}
```

#### 已有功能（保留）
- ✅ 3套场景描述（简约现代/奢华高端/生活化场景）
- ✅ 场景图生成（FlashImage）
- ✅ 广告词生成（Gemini）
- ✅ 视频生成（Grok）
- ✅ 视频合并（video_merger）
- ✅ 逐张发送场景图
- ✅ 实时发送中间视频
- ✅ 保存提示词和广告词

---

### 3. `generate_images.py`

#### 新增功能
- 接收参数：`--image`, `--user_id`
- 生成完成后：
  - 逐张发送图片（飞书）
  - 输出 `[GENERATION_RESULT]` 标记

#### 输出格式
```json
[GENERATION_RESULT] {"status": "success", "success_count": 4, "total": 4}
```

#### 已有功能（保留）
- ✅ Gemini 生成9个提示词
- ✅ FlashImage 生成9张图
- ✅ 每张图生成后立即发送
- ✅ 图片压缩（超过9MB自动压缩）
- ✅ 保存提示词和结果

---

### 4. `test_mode.py`

#### 新增功能
- 接收参数：`--image`, `--user_id`
- 生成完成后：
  - 保存测试图片到 `output/test_mode/`
  - 发送飞书消息
  - 输出 `[TEST_MODE_RESULT]` 标记

#### 输出格式
```json
[TEST_MODE_RESULT] {"status": "success", "output_path": "output/test_mode/xxx.png"}
```

#### 已有功能（保留）
- ✅ 保存图片到 output/test_mode/
- ✅ 发送回飞书

---

### 5. `generate_video.py`

**保持原样**，作为基础功能样例，不删不改。

---

## 📝 Bug 修复

### 2026-03-14 修复
- ✅ 修复 `feishu.py` 使用 `os.system` 导致返回码不准确的问题，改用 `subprocess.run`
- ✅ 修复 `feishu.py` 在多 channel 配置下缺少 `--channel` 参数的问题
- ✅ 修复队列消息格式解析，正确提取 `user_id`
- ✅ 修复日志输出特殊字符显示问题，所有 `✓` / `✗` / `⚠` 替换为 ASCII

---

## ✅ 确认点

1. `monitor.py` 不再处理结果 → 只启动脚本，日志记录返回码
2. 功能脚本自己发消息 → 通过 `feishu.py` 的 `send_text` / `send_image`
3. `generate_video.py` 保留 → 不删，作为基础样例
4. 所有脚本输出统一格式的 `[RESULT_MARKER]` → 方便日志调试
5. 日志不使用特殊字符 → 全部替换为 ASCII

---

## 📋 重构状态

- ✅ `monitor.py` 职责分离完成
  - 删除 `_parse_result()` 和 `_send_results_to_user()`
  - 简化 `_process_message()` 只启动脚本
  - 简化 `_call_script()` 只负责 subprocess.run
  - 删除 `send_text` / `send_image` 导入
  - 所有 `✓` / `✗` / `⚠` 替换为 `[OK]` / `[ERR]` / `[WARN]`
- ✅ `generate_video_v2.py` 无需调整（已有完整功能）
- ✅ `generate_images.py` 无需调整（已有完整功能）
- ✅ `test_mode.py` 无需调整（已有完整功能）
- ✅ `feishu.py` 修复发送问题
- ✅ 队列消息解析修复