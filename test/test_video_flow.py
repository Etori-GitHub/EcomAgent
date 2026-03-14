#!/usr/bin/env python3
"""
视频生成流程测试脚本
测试完整流程：Gemini 生成分镜 → Flash Image 生成图片 → Grok 生成视频
"""

import sys
import json
import base64
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from providers.gemini_prompt import GeminiPromptProvider
from providers.flash_image import FlashImageProvider
from providers.grok_video import GrokVideoProvider


def test_gemini_prompts(image_path: str):
    """测试 Gemini 生成分镜提示词"""
    print("=" * 60)
    print("测试 1: Gemini 生成分镜提示词")
    print("=" * 60)

    # 读取图片
    with open(image_path, 'rb') as f:
        image_base64 = base64.b64encode(f.read()).decode('utf-8')

    # 提示词模板（简化版）
    prompt_template = """Analyze this product image and create a 360-degree rotation video plan.

Generate:
1. 9 image prompts for a 3x3 grid showing the product rotating 40° each step (0°, 40°, 80°, 120°, 160°, 200°, 240°, 280°, 320°)
2. 1 video generation prompt

Requirements:
- Consistent product shape, color, material across all angles
- Pure white background (#FFFFFF)
- Soft studio lighting, fixed light source
- Product centered, eye-level view, no distortion
- Each prompt: 1 short sentence, under 20 words
- Video prompt: describe smooth 360° rotation, professional lighting

Return compact JSON:
{"storyboard_prompts":["...","...",...],"video_prompt":"..."}"""

    try:
        from PIL import Image
        import io

        gemini = GeminiPromptProvider()

        # 加载图片
        image = Image.open(image_path)

        print("调用 Gemini API...")

        # 使用 Gemini 的 generate_content 方法
        response = gemini.model.generate_content(
            [prompt_template, image],
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 8192  # 增加 token 限制
            }
        )

        # 解析 JSON
        content = response.text.strip()
        print(f"原始响应:\n{content[:1000]}...")
        print("-" * 60)

        # 尝试提取 JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        # 清理可能的特殊字符
        content = content.strip()
        if content.startswith('{'):
            # 找到最后一个 }
            last_brace = content.rfind('}')
            if last_brace > 0:
                content = content[:last_brace+1]

        print(f"提取的 JSON:\n{content[:500]}...")

        result = json.loads(content)

        if "storyboard_prompts" in result and "video_prompt" in result:
            print(f"✓ 成功生成 {len(result['storyboard_prompts'])} 个分镜提示词")
            print(f"✓ 视频提示词: {result['video_prompt'][:100]}...")
            return result
        else:
            print("✗ 响应格式错误")
            print(f"响应内容: {content[:500]}")
            return None

    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_grok_video(image_path: str, video_prompt: str):
    """测试 Grok 视频生成"""
    print()
    print("=" * 60)
    print("测试 2: Grok 视频生成 (5秒 480p)")
    print("=" * 60)

    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    output_path = str(output_dir / "test_video.mp4")

    grok = GrokVideoProvider()

    print(f"输入图片: {image_path}")
    print(f"视频提示词: {video_prompt[:100]}...")
    print(f"输出路径: {output_path}")
    print("-" * 60)

    result = grok.generate_video(
        prompt=video_prompt,
        output_path=output_path,
        input_image=image_path,
        duration=5,
        resolution="480p",
        aspect_ratio="16:9"
    )

    if result['status'] == 'success':
        print(f"✓ 视频生成成功!")
        print(f"  保存路径: {result['output_path']}")
    else:
        print(f"✗ 视频生成失败")
        print(f"  错误: {result.get('error', {}).get('message')}")

    return result


def main():
    # 查找测试图片
    test_img_dir = Path(__file__).parent / "img"
    if not test_img_dir.exists():
        print(f"请创建测试图片目录: {test_img_dir}")
        return 1

    test_images = list(test_img_dir.glob("*.jpg")) + list(test_img_dir.glob("*.png"))
    if not test_images:
        print(f"请在 {test_img_dir} 目录下放置测试图片")
        return 1

    image_path = str(test_images[0])
    print(f"使用测试图片: {image_path}")
    print()

    # 测试 1: Gemini 生成提示词
    prompts_result = test_gemini_prompts(image_path)
    if not prompts_result:
        return 1

    # 测试 2: Grok 生成视频（直接用产品图，跳过生成分镜步骤）
    video_result = test_grok_video(image_path, prompts_result['video_prompt'])

    print()
    print("=" * 60)
    print("测试完成")
    print("=" * 60)

    return 0 if video_result['status'] == 'success' else 1


if __name__ == "__main__":
    sys.exit(main())
