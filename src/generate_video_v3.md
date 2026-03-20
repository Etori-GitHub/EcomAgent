# 视频生成脚本 V3 - 链式续接方案

## 核心思路
用**首尾帧链式续接**实现15秒连贯广告视频：
- 第1段：场景图1 → 5秒视频
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

### 2. 广告词英文朗读（语音同步）
- **要求**：
  - 15秒分3段，每段约5秒
  - 语言自然流畅，适合口语化朗读
  - 无复杂术语，节奏感强
- **实现**：
  - Gemini生成英文广告词
  - Grok视频生成时嵌入语音（`voiceover`参数）
  - 每段视频对应一段广告词

---

## 具体流程

### Step 1: 生成高质量首帧模特图（新增步骤）
- 用Gemini生成**时尚白人模特图**（帅哥/美女，与产品互动）
- 质感要求：专业摄影级别，高清细节，9:16竖屏
- 输出：`model_frame.png`

### Step 2: 生成3套场景描述
- 用Gemini生成3套不同风格的场景描述（简约/奢华/生活化）
- 每套包含场景图生成提示词

### Step 2: 生成3张场景图（可选）
- 用FlashImage生成3张场景图（scene_01.png ~ scene_03.png）
- 每张图对应一种风格

### Step 2.5: 生成广告词（关键优化点）
- 用Gemini生成15秒分3段的广告词（英文）
- 每段约5秒，对应3段视频
- **要求**：广告词需适合英文朗读，节奏自然，无复杂术语

### Step 3.5: 生成首帧模特图（关键优化点）
- 用Gemini生成**高质量时尚白人模特图**（帅哥或美女）
- **要求**：
  - 质感极佳（专业摄影级别）
  - 欧洲面孔，时尚穿搭
  - 与产品自然互动（如手持、试用）
  - 9:16竖屏，高清细节
- **用途**：作为第1段视频的起始帧（替代场景图）

### Step 3: 生成3段视频（链式续接）

#### 第1段视频
```
起始帧：model_frame.png（高质量白人模特图，与产品互动）
提示词：[VIDEO_PROMPT_TEMPLATE] + [ad_segment_1] + "seamlessly continue from this frame..."
输出：video_01.mp4（5秒，带英文语音朗读）
```

#### 第2段视频
```
起始帧：extract_last_frame(video_01.mp4) → frame_end_01.png
提示词：[VIDEO_PROMPT_TEMPLATE] + [ad_segment_2] + "seamlessly continue from the exact last frame..."
输出：video_02.mp4（5秒，带英文语音朗读）
```

#### 第3段视频
```
起始帧：extract_last_frame(video_02.mp4) → frame_end_02.png
提示词：[VIDEO_PROMPT_TEMPLATE] + [ad_segment_3] + "seamlessly continue from the exact last frame..."
输出：video_03.mp4（5秒，带英文语音朗读）
```

### Step 4: 合并视频
```
输入：video_01.mp4, video_02.mp4, video_03.mp4
输出：video_merged.mp4（15秒）
```

---

## 代码修改点

### 1. 导入 `extract_last_frame`
```python
from utils.video_merger import extract_last_frame
```

### 2. 修改视频生成循环（链式续接）
```python
# 第1段：用高质量模特图作为起始帧
input_frame = str(output_dir / "model_frame.png")  # 或输入产品图

for i in range(1, 4):  # 3段视频
    # 生成视频（带英文语音朗读）
    ad_segment = ad_segments[i-1] if i <= len(ad_segments) else ""
    video_prompt_with_voice = f"""{VIDEO_PROMPT_TEMPLATE}

IMPORTANT AUDIO INSTRUCTION:
This video MUST include voiceover narration with the following script (read aloud naturally, no background music):
"{ad_segment}"

IMPORTANT VISUAL INSTRUCTION:
This video MUST seamlessly continue from the exact last frame of the previous video.
Maintain visual continuity: same product, same lighting, same camera angle progression.
No cuts, no jumps, no scene changes.
"""
    
    result = grok.generate_video(
        prompt=video_prompt_with_voice,
        output_path=str(output_dir / f"video_{i:02d}.mp4"),
        input_image=input_frame,
        duration=duration,
        resolution=resolution
    )
    
    # 截取最后一帧（除最后一段外）
    if i < 3:
        next_input_frame = str(output_dir / f"frame_end_{i:02d}.png")
        extract_last_frame(str(output_dir / f"video_{i:02d}.mp4"), next_input_frame)
        input_frame = next_input_frame  # 下一段用这张帧
```

### 3. Prompt增加语音朗读描述
```python
video_prompt_with_voice = f"""{VIDEO_PROMPT_TEMPLATE}

IMPORTANT AUDIO INSTRUCTION:
This video MUST include voiceover narration with the following script (read aloud naturally, no background music):
"{ad_segment}"
"""
```

---

## 输出文件结构
```
output/YYYYMMDD_HHMMSS/
├── model_frame.png       # 高质量白人模特图（首帧）
├── scene_01.png          # 场景图1
├── scene_02.png          # 场景图2
├── scene_03.png          # 场景图3
├── ad_script.txt         # 广告词
├── video_01.mp4          # 第1段视频（带英文语音）
├── video_02.mp4          # 第2段视频（带英文语音）
├── video_03.mp4          # 第3段视频（带英文语音）
├── frame_end_01.png      # 第1段最后一帧（中间文件）
├── frame_end_02.png      # 第2段最后一帧（中间文件）
├── video_merged.mp4      # 合成视频（15秒）
└── result.json           # 结果记录
```

---

## 依赖检查
- ✅ `extract_last_frame` 函数（`utils/video_merger.py`）
- ✅ `ffmpeg` 命令行（用于截取帧）
- ✅ `PIL`（可选，备用截帧方案）

---

## 完整流程图
```
输入产品图
    ↓
[Step 1] 生成高质量白人模特图（Gemini + FlashImage）
    ↓
[Step 2] 生成3套场景描述（Gemini）
    ↓
[Step 2.5] 生成广告词（Gemini，15秒分3段）
    ↓
[Step 3] 生成3段视频（Grok，链式续接）
    ├─ video_01.mp4（起始帧：model_frame.png）
    ├─ video_02.mp4（起始帧：video_01最后一帧）
    └─ video_03.mp4（起始帧：video_02最后一帧）
    ↓
[Step 4] 合并视频（ffmpeg）
    ↓
输出：video_merged.mp4（15秒，带英文语音）
```

---

## 后续优化
- 如果连贯性不足，可增加 `prompt` 中的视觉描述一致性
- 可尝试用 `video_01.mp4` 作为 `video_02` 的 `input_video`（Video-to-Video模式）
- 可考虑用 `ffmpeg` 做转场淡入淡出，提升观感
- 如果模特图质感不达标，可尝试调整Gemini提示词（增加"professional photography", "8K detail", "studio lighting"等关键词）
