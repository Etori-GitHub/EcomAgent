# Google AI Studio 可用模型清单

**最后更新：** 2026-03-07  
**API Key：** `AIzaSyCWnjr0Ff-kW_VGh5sd2r6YN1F_qPnkBdQ`（有 $300 额度）

---

## 图像生成模型

| 模型名称 | 描述 | 版本 | 状态 |
|---------|------|------|------|
| `gemini-2.0-flash-exp-image-generation` | Gemini 2.0 Flash 图像生成实验版 | 2.0 | 待测试 |
| `gemini-2.5-flash-image` | Gemini 2.5 Flash 图像版 | 2.0 | 待测试 |
| `gemini-3-pro-image-preview` | Gemini 3 Pro 图像预览版 | 3.0 | 待测试 |
| `nano-banana-pro-preview` | Nano Banana Pro 预览版 | 3.0 | 待测试 |
| `gemini-3.1-flash-image-preview` | Gemini 3.1 Flash 图像预览版 | 3.1 | ✅ 已测试通过 |
| `imagen-4.0-generate-001` | Imagen 4.0 标准版 | 001 | 待测试 |
| `imagen-4.0-ultra-generate-001` | Imagen 4.0 Ultra版 | 001 | 待测试 |
| `imagen-4.0-fast-generate-001` | Imagen 4.0 快速版 | 001 | 待测试 |

### 测试记录

| 模型名称 | 测试时间 | 结果 | 备注 |
|---------|---------|------|------|
| `gemini-2.5-flash-image` | 2026-03-07 | ❌ 404 | 旧 API Key |
| `gemini-2.0-flash-exp` | 2026-03-07 | ❌ 404 | 缺少 `-image-generation` 后缀 |
| `gemini-3-pro-image-preview` | 2026-03-07 | ❌ 404 | 旧 API Key |
| `gemini-3.1-flash-image-preview` | 2026-03-07 | ✅ 成功 | 使用 `response_modalities=['TEXT', 'IMAGE']` 方式 |

---

## 视频生成模型

| 模型名称 | 描述 | 版本 |
|---------|------|------|
| `veo-2.0-generate-001` | Veo 2 | 2.0 |
| `veo-3.0-generate-001` | Veo 3 | 3.0 |
| `veo-3.0-fast-generate-001` | Veo 3 快速版 | 3.0 |
| `veo-3.1-generate-preview` | Veo 3.1 预览版 | 3.1 |
| `veo-3.1-fast-generate-preview` | Veo 3.1 快速预览版 | 3.1 |

---

## 文本/多模态模型

| 模型名称 | 描述 | 版本 |
|---------|------|------|
| `gemini-2.5-flash` | Gemini 2.5 Flash 稳定版（支持 1M tokens） | 001 |
| `gemini-2.5-pro` | Gemini 2.5 Pro 稳定版 | 2.5 |
| `gemini-2.0-flash` | Gemini 2.0 Flash | 2.0 |
| `gemini-2.0-flash-001` | Gemini 2.0 Flash 稳定版 | 2.0 |
| `gemini-2.0-flash-lite-001` | Gemini 2.0 Flash-Lite 稳定版 | 2.0 |
| `gemini-2.5-flash-lite` | Gemini 2.5 Flash-Lite 稳定版 | 001 |
| `gemini-flash-latest` | Gemini Flash 最新版 | - |
| `gemini-pro-latest` | Gemini Pro 最新版 | - |

---

## TTS (文本转语音) 模型

| 模型名称 | 描述 | 版本 |
|---------|------|------|
| `gemini-2.5-flash-preview-tts` | Gemini 2.5 Flash TTS 预览版 | gemini-2.5-flash-exp-tts-2025-05-19 |
| `gemini-2.5-pro-preview-tts` | Gemini 2.5 Pro TTS 预览版 | gemini-2.5-pro-preview-tts-2025-05-19 |

---

## 原生音频模型

| 模型名称 | 描述 | 版本 |
|---------|------|------|
| `gemini-2.5-flash-native-audio-latest` | Gemini 2.5 Flash 原生音频最新版 | - |
| `gemini-2.5-flash-native-audio-preview-09-2025` | Gemini 2.5 Flash 原生音频预览版 09-2025 | gemini-2.5-flash-preview-native-audio-dialog-2025-05-19 |
| `gemini-2.5-flash-native-audio-preview-12-2025` | Gemini 2.5 Flash 原生音频预览版 12-2025 | 12-2025 |

---

## 常见问题

### 404 错误原因

1. **模型名称拼写错误** - 必须完全匹配 API 返回的模型名称
2. **API Key 权限不足** - 某些模型需要特定权限或额度
3. **地区限制** - 图像生成功能在某些地区不可用
4. **API 版本不匹配** - 预览版功能只在 `v1beta` 接口开放

### 如何查询可用模型

```python
from google import genai

client = genai.Client(api_key="你的API_KEY")
models = client.models.list()

for model in models:
    print(model.name)
    if hasattr(model, 'supported_generation_methods'):
        print(f"  支持的方法: {model.supported_generation_methods}")
```

---

## 配置位置

- **Flash Image 配置：** `config/flash_image_config.json`
- **Gemini 配置：** `config/gemini_config.json`
- **当前使用模型：** `gemini-3-pro-image-preview`（待测试）
