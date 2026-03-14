#!/usr/bin/env python3
"""
视频生成流程测试脚本 V2
正确流程：
1. Gemini 直接生成一张 3x3 九宫格分镜图（不是9个提示词）
2. Gemini 生成视频提示词
3. Grok 用九宫格图 + 视频提示词生成视频
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from providers.flash_image import FlashImageProvider
from providers.grok_video import GrokVideoProvider
from PIL import Image
import google.generativeai as genai


def generate_video_prompt(image_path: str) -> str:
    """返回固定的英文版视频提示词"""
    return """[Task] Animate the uploaded 3x3 product grid into a seamless 360-degree horizontal rotation video.

[Motion Instructions]
1. SEQUENCE: Interpret the 9 frames from top-left to bottom-right as a continuous chronological sequence.
2. ACTION: Synthesize a smooth, fluid clockwise rotation. The product must transition perfectly from the front view (0°) through each profile to a full 360-degree spin.
3. MOTION TYPE: Use a "Turntable" motion effect. The camera remains static and centered while the object rotates steadily.
4. CONSISTENCY: Maintain 100% visual fidelity of the product's geometry and logo. No morphing or "hallucinating" new parts during the turn.

[Style & Environment]
- Keep the solid white background (#FFFFFF) clean and unmoving.
- Lighting: Maintain the soft studio wrap-around lighting. Reflections on the product surface should slide realistically according to the rotation.
- Output: 6-10 second cinematic product showcase, 720p/1080p, ultra-smooth frame rate.

[Negative]
Choppy transitions, erratic movement, grid lines visible in the final video, background flicker, zooming in/out, shape distortion."""


def generate_storyboard_and_prompt(product_image_path: str, output_dir: Path):
    """
    使用 Flash Image (Gemini) 直接生成 3x3 九宫格分镜图
    同时生成视频提示词
    """
    print("=" * 60)
    print("Step 1: 生成 3x3 九宫格分镜图 + 视频提示词")
    print("=" * 60)

    # 输出路径
    storyboard_path = str(output_dir / "storyboard_9grid.png")

    # 主人提供的英文版提示词
    prompt = """[Instruction] Based strictly on the provided Reference Image, generate a 3x3 structured composite grid (grid of 9 individual images). The output must be a seamless, perfectly consistent horizontal 360-degree rotation sequence of the specific product, optimized for creating a smooth product 360 showcase video.

[Core Requirements]
1. **VISUAL CONSISTENCY (CRITICAL):** Maintain 100% physical and structural consistency across all 9 images. The product's geometry, branding, material textures, colors, and component proportions must remain identical. Absolutely NO shape-shifting or detail distortion is allowed during rotation.

2. **ROTATION SEQUENCE (VISUAL GUIDE):** Arrange a strict clockwise horizontal rotation in a 3x3 grid format, from top-left to bottom-right. The frames sequence must capture:
Frame 1: Pure Front View (0°)
Frame 2: Front-Right profile
Frame 3: Pure Right Side View
Frame 4: Back-Right profile
Frame 5: Pure Back View (180°)
Frame 6: Back-Left profile
Frame 7: Pure Left Side View
Frame 8: Front-Left profile
Frame 9: Centered Front View (or a detailed close-up of the front)
The rotation displacement must be visually progressive and equal between frames.

3. **PERFECT STUDIO ENVIRONMENT:**
* **Background:** Use a solid, absolute white background (Hex #FFFFFF) with no gradients, platforms, or artifacts.
* **Lighting:** Fixed soft wrap-around studio lighting. Highlighting must shift naturally on metal or plastic surfaces as the product rotates, with no flickering.

[Technical Specs]
1. **Style:** Ultra High-Definition (UHD) photography, 8K commercial product rendering.
2. **Composition:** The product must always be perfectly centered within each cell, with identical scaling to ensure the video does not shake when synthesized.
3. **Shot Type:** Clean eye-level view, eliminating any perspective distortion (nearly orthographic).
4. **Format:** Output as a single composite image containing the 3x3 grid.

[Negative Prompt]
Text, watermark, logo changes, shape shifting, inconsistent textures, shadows on floor, blurred details, multiple objects, platform, messy background, dramatic perspective distortion, uneven rotation steps."""

    # 用 Gemini 分析产品图，生成针对性的视频提示词
    print("  分析产品类型，生成视频提示词...")
    video_prompt = generate_video_prompt(product_image_path)

    print("[1/2] 生成九宫格分镜图...")
    print(f"  提示词长度: {len(prompt)} 字符")
    print(f"  要求: 3x3 网格，0°→40°→80°→...→320° 旋转")

    try:
        flash = FlashImageProvider()

        # 使用图生图功能生成九宫格
        print("  调用 Flash Image API...")
        result = flash.generate_image(
            prompt=prompt,
            output_path=storyboard_path,
            input_image=product_image_path,  # 参考图
            aspect_ratio="1:1",  # 正方形
            resolution="2K"  # 高分辨率
        )

        if result['status'] == 'success':
            print(f"  ✓ 九宫格生成成功: {storyboard_path}")
        else:
            print(f"  ✗ 九宫格生成失败: {result.get('error', {}).get('message')}")
            return {
                "status": "error",
                "error": result.get('error', {})
            }

        # 生成视频提示词
        print("[2/2] 生成视频提示词...")
        video_prompt = generate_video_prompt(product_image_path)
        print(f"  ✓ 视频提示词: {video_prompt}")

        return {
            "status": "success",
            "storyboard_path": storyboard_path,
            "video_prompt": video_prompt
        }

    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "error": {"message": str(e)}
        }


def generate_video(storyboard_path: str, video_prompt: str, output_dir: Path):
    """
    使用 Grok 生成视频
    """
    print()
    print("=" * 60)
    print("Step 2: Grok 生成视频 (5秒 480p)")
    print("=" * 60)

    output_video_path = str(output_dir / "video.mp4")

    print(f"输入九宫格: {storyboard_path}")
    print(f"视频提示词: {video_prompt}")
    print(f"输出路径: {output_video_path}")
    print("-" * 60)

    try:
        grok = GrokVideoProvider()

        result = grok.generate_video(
            prompt=video_prompt,
            output_path=output_video_path,
            input_image=storyboard_path,  # 使用九宫格作为参考
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

    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "error": {"message": str(e)}
        }


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

    # 创建输出目录
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    # Step 1: 生成九宫格分镜图 + 视频提示词
    step1_result = generate_storyboard_and_prompt(image_path, output_dir)
    if step1_result['status'] != 'success':
        return 1

    # Step 2: Grok 生成视频
    step2_result = generate_video(
        step1_result['storyboard_path'],
        step1_result['video_prompt'],
        output_dir
    )

    print()
    print("=" * 60)
    if step2_result['status'] == 'success':
        print("✓ 全部流程成功!")
        print(f"  九宫格: {step1_result['storyboard_path']}")
        print(f"  视频: {step2_result['output_path']}")
    else:
        print("✗ 流程失败")
    print("=" * 60)

    return 0 if step2_result['status'] == 'success' else 1


if __name__ == "__main__":
    sys.exit(main())
