#!/usr/bin/env python3
"""
新流程测试：产品图 → 场景化产品图 → 视频提示词 → 视频
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from providers.flash_image import FlashImageProvider
from providers.gemini_prompt import GeminiPromptProvider
from providers.grok_video import GrokVideoProvider
from utils.imgbb_uploader import upload_image
from PIL import Image


# 主人提供的场景化提示词模板
SCENE_PROMPT_TEMPLATE = """Photorealistic professional e-commerce lifestyle product photography using the exact reference image as the product source -- the product must remain 100% identical in every single detail: precise shape, exact original colors, perfect logo/text/font placement and spelling, identical packaging, materials, textures, labels, proportions, reflections, no alterations, no redesign, no stylization, no improvements, no hallucinations or changes whatsoever to the product itself. Preserve all original features faithfully with maximum fidelity. Integrate the unchanged product naturally and seamlessly into a premium, aspirational real-life usage scene: {scene_description}. High-end commercial advertising style, sophisticated and balanced composition, ideal hero product placement and flattering angle for online store showcase, professional cinematic lighting: soft diffused key light from {light_direction} + gentle natural fill + subtle realistic rim/highlight on product edges, accurate soft shadows falling naturally on surfaces, realistic reflections and caustics where appropriate, shallow to medium depth of field with creamy background blur (f/2.8–f/4 aesthetic), razor-sharp critical focus exclusively on the product, hyper-realistic materials and surfaces, clean aspirational mood that evokes desire and quality, no text overlays, no watermarks, no distracting or obscuring elements on or covering the product. Ultra-high resolution 8K, RAW photo quality, shot on professional full-frame camera like Canon EOS R5 or Sony A1 with 85mm or 100mm prime lens, subtle film-like color grading."""


# 针对不同产品类型的场景描述
SCENE_PRESETS = {
    "food": {
        "scene": "rustic wooden dining table at warm golden hour, soft natural window light from the left, ceramic plate and linen napkin, fresh herbs garnish, cozy home kitchen atmosphere with gentle bokeh",
        "light": "front-left window"
    },
    "electronics": {
        "scene": "minimalist modern workspace with matte black desk, soft diffused daylight from large window, subtle tech accessories in background, clean Scandinavian interior design, premium professional environment",
        "light": "front-right large window"
    },
    "fashion": {
        "scene": "elegant walk-in closet with warm ambient lighting, velvet hanger and marble surface, soft fabric textures in background, luxurious boutique atmosphere, refined lifestyle setting",
        "light": "front-left softbox"
    },
    "cosmetics": {
        "scene": "marble vanity counter with fresh flowers, soft morning light through sheer curtains, rose gold accents, spa-like serene atmosphere, dewy fresh aesthetic",
        "light": "front window with sheer diffusion"
    },
    "default": {
        "scene": "clean modern surface with soft natural lighting, minimal elegant background, professional studio atmosphere with subtle lifestyle elements",
        "light": "front-left window"
    }
}


# 固定的视频提示词（主人提供）
VIDEO_PROMPT_TEMPLATE = """Using the uploaded reference image as the exact product and starting scene, create a premium cinematic product advertisement video. First analyze the product's theme, design style, colors, materials, and surrounding environment in the image, then craft a natural, engaging, story-driven showcase that feels like a high-end commercial. Feature elegant dynamic product showcase with subtle, realistic interactions relevant to the product (such as gentle handling, natural usage, pouring, wearing, or environmental interaction) while keeping the product perfectly centered and heroically highlighted. Showcase the product through dynamic camera movements and professional cinematography techniques. Use smooth, fluid cinematic camera movements — slow push-in, gentle tracking shot, subtle elegant orbit, or graceful dolly — to reveal beautiful details from multiple flattering angles in a seamless, continuous flow. Maintain 100% visual fidelity to the original product in every frame: exact shape, precise colors, perfect logo placement and text, identical materials, textures, reflections, and all details — no morphing, distortion, hallucination, or added parts whatsoever. Enhance the original scene with consistent premium atmosphere, professional soft studio wrap-around lighting plus natural cinematic enhancements, realistic sliding reflections and soft shadows that perfectly match the motion. Output an 8-second ultra-cinematic product advertisement video: ultra-smooth 60fps-like fluid motion, hyper-realistic photorealistic rendering, razor-sharp 720p clarity and ultra-high detail, professional Hollywood color grading, high dynamic range, cinematic depth of field, clean aspirational mood, masterpiece commercial quality, no artifacts, no jitter, no flicker. Negative: choppy transitions, erratic movement, background changes or flicker, excessive zooming, shape distortion, blurry details, low quality, morphing, artifacts, unnatural motion."""


def generate_scene_image(product_image_path: str, output_path: str, scene_type: str = "default"):
    """
    Step 1: 生成场景化产品图
    """
    print("=" * 60)
    print("Step 1: 生成场景化产品图")
    print("=" * 60)

    # 获取场景预设
    preset = SCENE_PRESETS.get(scene_type, SCENE_PRESETS["default"])

    # 填充提示词模板
    prompt = SCENE_PROMPT_TEMPLATE.format(
        scene_description=preset["scene"],
        light_direction=preset["light"]
    )

    print(f"场景类型: {scene_type}")
    print(f"场景描述: {preset['scene'][:60]}...")
    print(f"输出路径: {output_path}")
    print()

    try:
        flash = FlashImageProvider()

        result = flash.generate_image(
            prompt=prompt,
            output_path=output_path,
            input_image=product_image_path,
            aspect_ratio="3:4",  # 竖版，适合电商
            resolution="2K"
        )

        if result['status'] == 'success':
            print(f"✓ 场景图生成成功: {output_path}")
            return True
        else:
            print(f"✗ 场景图生成失败: {result.get('error', {}).get('message')}")
            return False

    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def generate_video(scene_image_path: str, output_path: str, duration: int = 5, resolution: str = "480p"):
    """
    Step 2: 用 Grok 生成视频
    """
    print()
    print("=" * 60)
    print("Step 2: Grok 生成视频")
    print("=" * 60)

    video_prompt = VIDEO_PROMPT_TEMPLATE

    print(f"输入场景图: {scene_image_path}")
    print(f"视频时长: {duration}s")
    print(f"分辨率: {resolution}")
    print(f"输出路径: {output_path}")
    print()
    print("-" * 60)
    print("Grok 视频提示词:")
    print("-" * 60)
    print(video_prompt)
    print("-" * 60)
    print()

    try:
        grok = GrokVideoProvider()

        result = grok.generate_video(
            prompt=video_prompt,
            output_path=output_path,
            input_image=scene_image_path,
            duration=duration,
            resolution=resolution,
            aspect_ratio="9:16"  # 竖版视频
        )

        if result['status'] == 'success':
            print(f"✓ 视频生成成功: {output_path}")
            return True
        else:
            print(f"✗ 视频生成失败: {result.get('error', {}).get('message')}")
            return False

    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description='测试新流程：产品图→场景图→视频')
    parser.add_argument('--image', required=True, help='输入产品图片路径')
    parser.add_argument('--scene', default='default', choices=list(SCENE_PRESETS.keys()),
                        help='场景类型')
    parser.add_argument('--duration', type=int, default=5, help='视频时长（秒）')
    parser.add_argument('--resolution', default='480p', choices=['480p', '720p'])

    args = parser.parse_args()

    if not Path(args.image).exists():
        print(f"图片不存在: {args.image}")
        return 1

    # 创建输出目录
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    scene_path = str(output_dir / "scene_product.png")
    video_path = str(output_dir / "scene_video.mp4")

    print(f"使用测试图片: {args.image}")
    print(f"场景类型: {args.scene}")
    print()

    # Step 1: 生成场景图
    if not generate_scene_image(args.image, scene_path, args.scene):
        return 1

    # Step 2: 生成视频
    if not generate_video(scene_path, video_path, args.duration, args.resolution):
        return 1

    print()
    print("=" * 60)
    print("✓ 全部流程成功!")
    print(f"  场景图: {scene_path}")
    print(f"  视频: {video_path}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())