#!/usr/bin/env python3
"""
单独测试九宫格分镜生成
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from providers.flash_image import FlashImageProvider


def generate_storyboard_only(product_image_path: str, output_path: str):
    """只生成九宫格分镜图"""
    print("=" * 60)
    print("生成 3x3 九宫格分镜图")
    print("=" * 60)
    print(f"输入图片: {product_image_path}")
    print(f"输出路径: {output_path}")
    print()

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

    print(f"提示词长度: {len(prompt)} 字符")
    print("调用 Flash Image API...")
    print()

    try:
        flash = FlashImageProvider()

        result = flash.generate_image(
            prompt=prompt,
            output_path=output_path,
            input_image=product_image_path,
            aspect_ratio="1:1",
            resolution="2K"
        )

        if result['status'] == 'success':
            print(f"✓ 九宫格生成成功!")
            print(f"  保存路径: {output_path}")
            return True
        else:
            print(f"✗ 九宫格生成失败")
            print(f"  错误: {result.get('error', {}).get('message')}")
            return False

    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


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

    # 输出路径
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    output_path = str(output_dir / "storyboard_9grid.png")

    success = generate_storyboard_only(image_path, output_path)

    print()
    print("=" * 60)
    if success:
        print("✓ 测试完成，请检查生成的九宫格")
    else:
        print("✗ 测试失败")
    print("=" * 60)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
