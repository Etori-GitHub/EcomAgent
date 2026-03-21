# 视频生成脚本 V3 - 链式续接版（首帧模特图）

## 最新进度
- **日期**: 2026-03-21
- **状态**: ✅ 流程设计完成，待测试
- **核心问题**: Grok API 无法从 ImgBB 下载图片（`Failed to fetch response body while downloading image`）

---

## 核心思路
用**首帧模特图 + 链式续接**实现15秒连贯广告视频：
- 第1段：高质量首帧模特图 → 5秒视频
- 第2段：第1段最后一帧 → 5秒视频
- 第3段：第2段最后一帧 → 5秒视频
- 合并：3段 → 15秒完整视频

---

## 技术限制
Grok Imagine Video API **不支持同时传首帧+尾帧**，只支持：
- Text-to-Video（纯文字）
- Image-to-Video（1张起始帧 + prompt）
- Video-to-Video（已有视频 + prompt编辑）

**解决方案**：用 `extract_last_frame` 截取上一段最后一帧，作为下一段的起始帧。

---

## 关键优化点

### 1. 首帧模特图（高质量视觉基础）
- **用途**：第1段视频的起始帧，决定整体视觉质感
- **要求**：
  - 欧洲面孔白人模特（帅哥或美女）
  - 时尚穿搭，专业摄影质感
  - 与产品自然互动（手持、试用、佩戴等）
  - 9:16竖屏，高清细节，无任何失真
- **生成方式**：Gemini Prompt + FlashImage 生成

### 2. 链式续接（保证视觉连贯性）
- **原理**：每段视频的起始帧 = 上一段的最后一帧
- **实现**：用 `extract_last_frame` 截取最后一帧 → 传本地路径给 Grok → Grok 自动上传到图床

---

## 具体流程

### Step 0: 生成高质量首帧模特图
- 用 Gemini 生成**高质量时尚白人模特图**（帅哥/美女）
- 要求：专业摄影级别，高清细节，9:16竖屏
- 输出：`model_frame.png`

### Step 1: 生成3段视频（链式续接）

#### 第1段视频
```
起始帧：model_frame.png（本地路径）
提示词：[VIDEO_PROMPT_TEMPLATE]
输出：video_01.mp4（5秒）
```

#### 第2段视频
```
起始帧：extract_last_frame(video_01.mp4) → frame_end_01.jpg（本地路径）
提示词：[VIDEO_PROMPT_TEMPLATE]
输出：video_02.mp4（5秒）
```

#### 第3段视频
```
起始帧：extract_last_frame(video_02.mp4) → frame_end_02.jpg（本地路径）
提示词：[VIDEO_PROMPT_TEMPLATE]
输出：video_03.mp4（5秒）
```

### Step 2: 合并视频
```
输入：video_01.mp4, video_02.mp4, video_03.mp4
输出：video_merged.mp4（15秒）
```

---

## 代码实现要点

### 1. 所有段都用本地路径
```python
# 第1段：用本地首帧路径
current_frame = model_frame_path

for i in range(1, 4):
    # 生成视频（Grok 会自动上传到图床）
    result = grok.generate_video(
        prompt=video_prompt_with_voice,
        output_path=str(output_dir / f"video_{i:02d}.mp4"),
        input_image=current_frame,  # 本地路径
        ...
    )
    
    # 截取最后一帧（除最后一段外）
    if i < 3:
        next_input_frame = str(output_dir / f"frame_end_{i:02d}.jpg")
        extract_last_frame(video_path, next_input_frame)
        current_frame = next_input_frame  # 下一段用本地路径
```

### 2. Grok 自动上传机制
- Grok 的 `generate_video` 方法会自动：
  1. 检查图片大小（>2MB 自动压缩）
  2. 上传到 ImgBB
  3. 获取 URL 并传给 API

---

## 输出文件结构
```
output/YYYYMMDD_HHMMSS/
├── model_frame.png       # 高质量白人模特图（首帧）
├── video_01.mp4          # 第1段视频
├── video_02.mp4          # 第2段视频
├── video_03.mp4          # 第3段视频
├── frame_end_01.jpg      # 第1段最后一帧（中间文件）
├── frame_end_02.jpg      # 第2段最后一帧（中间文件）
├── video_merged.mp4      # 合成视频（15秒）
└── result.json           # 结果记录
```

---

## 依赖检查
- ✅ `extract_last_frame` 函数（`utils/video_merger.py`）
- ✅ `ffmpeg` 命令行（用于截取帧）
- ✅ `PIL`（图片压缩）

---

## 当前问题
**Grok API 无法从 ImgBB 下载图片**：
```
Image URL could not be fetched: Failed to fetch response body while downloading image.
```

**可能原因**：
1. ImgBB 的 URL 有访问限制（需要特定的 User-Agent 或 Referer）
2. ImgBB 的 URL 有 CDN 重定向，Grok 无法跟随
3. Grok 的 API 有 bug

**待测试**：直接传本地路径给 Grok，让它自己上传到图床。

---

## 后续优化
- 如果连贯性不足，可增加 `prompt` 中的视觉描述一致性
- 可尝试用 `video_01.mp4` 作为 `video_02` 的 `input_video`（Video-to-Video模式）
- 可考虑用 `ffmpeg` 做转场淡入淡出，提升观感
- 如果模特图质感不达标，可尝试调整 Gemini 提示词（增加 "professional photography", "8K detail", "studio lighting" 等关键词）
