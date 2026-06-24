# -*- coding: utf-8 -*-
"""
生成产品详情图
输入一张产品图片，生成 N 张不同场景的展示图
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# 添加项目根目录到 path
sys.path.insert(0, str(Path(__file__).parent))

from providers.flash_image import FlashImageProvider
from utils.logger import get_logger


# 场景模板（预留，以后可以改）
SCENE_TEMPLATES = [
    {
        "name": "简约现代",
        "prompt": "Professional e-commerce product photography, clean white background, soft studio lighting, minimalist modern style, high-end commercial quality, sharp focus on product"
    },
    {
        "name": "自然阳光",
        "prompt": "Natural lifestyle product photography, soft sunlight through window, warm golden hour lighting, cozy home environment, authentic and inviting atmosphere"
    },
    {
        "name": "奢华高端",
        "prompt": "Premium luxury product photography, dark elegant background, dramatic lighting, sophisticated high-end style, exclusive boutique atmosphere"
    },
    {
        "name": "生活场景",
        "prompt": "Lifestyle product photography in real-life setting, natural environment, casual everyday context, relatable and approachable style"
    },
    {
        "name": "商业广告",
        "prompt": "Professional advertising product photography, dynamic composition, bold lighting, commercial catalog style, eye-catching presentation"
    },
    {
        "name": "极简白底",
        "prompt": "Clean white background product photography, pure white backdrop, professional e-commerce standard, shadowless studio lighting"
    },
    {
        "name": "创意艺术",
        "prompt": "Artistic product photography, creative composition, unique perspective, artistic lighting, gallery-style presentation"
    },
    {
        "name": "节日氛围",
        "prompt": "Festive product photography, holiday atmosphere, seasonal decorations, celebratory mood, gift-ready presentation"
    },
    {
        "name": "科技感",
        "prompt": "Modern tech product photography, sleek futuristic style, blue accent lighting, high-tech atmosphere, innovative presentation"
    }
]


def generate_product_details(
    image_path: str,
    output_dir: str = None,
    count: int = 9,
    aspect_ratio: str = "1:1",
    resolution: str = "2K",
    use_input_image: bool = True,
    custom_prompts: List[str] = None
) -> Dict:
    """
    生成产品详情图
    
    Args:
        image_path: 输入图片路径
        output_dir: 输出目录，默认自动创建
        count: 生成数量，默认 9 张
        aspect_ratio: 宽高比，默认 1:1
        resolution: 分辨率，默认 2K
        use_input_image: 是否使用输入图片作为参考，默认 True
        custom_prompts: 自定义提示词列表，如果提供则使用自定义的
    
    Returns:
        {
            "status": "success" | "error",
            "output_dir": str,
            "images": [
                {
                    "path": str,
                    "scene": str,
                    "prompt": str
                }
            ]
        }
    """
    logger = get_logger()
    
    # 验证输入
    if not Path(image_path).exists():
        error_msg = f"输入图片不存在: {image_path}"
        logger.log_error("generate_product_details", "validate_input", Exception(error_msg))
        return {"status": "error", "error": {"message": error_msg}}
    
    # 创建输出目录
    if output_dir is None:
        output_dir = Path("output") / "product_details" / datetime.now().strftime("%Y%m%d_%H%M%S")
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.log_operation(
        module="generate_product_details",
        action="start",
        details=f"input={image_path}, output={output_dir}, count={count}"
    )
    
    print("=" * 60)
    print("生成产品详情图")
    print("=" * 60)
    print(f"输入: {image_path}")
    print(f"输出: {output_dir}")
    print(f"数量: {count}")
    print(f"比例: {aspect_ratio}")
    print(f"分辨率: {resolution}")
    print(f"参考原图: {use_input_image}")
    print()
    
    # 准备提示词
    if custom_prompts:
        prompts = custom_prompts[:count]
        scenes = [f"Custom {i+1}" for i in range(len(prompts))]
    else:
        # 使用内置模板
        templates = SCENE_TEMPLATES[:count]
        prompts = [t["prompt"] for t in templates]
        scenes = [t["name"] for t in templates]
    
    # 补齐数量
    while len(prompts) < count:
        prompts.append("Professional product photography, studio lighting")
        scenes.append(f"Scene {len(scenes)+1}")
    
    # 初始化 Provider
    flash = FlashImageProvider()
    
    results = []
    success_count = 0
    failed_count = 0
    
    for i, (prompt, scene) in enumerate(zip(prompts, scenes)):
        print(f"[{i+1}/{count}] 生成: {scene}")
        print(f"  提示词: {prompt[:60]}...")
        
        output_path = str(output_dir / f"{i+1:02d}_{scene}.png")
        
        # 调用 API 生成图片
        result = flash.generate_image(
            prompt=prompt,
            output_path=output_path,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            input_image=image_path if use_input_image else None
        )
        
        if result['status'] == 'success':
            print(f"  ✓ 成功: {output_path}")
            results.append({
                "path": output_path,
                "scene": scene,
                "prompt": prompt,
                "status": "success"
            })
            success_count += 1
        else:
            error_msg = result.get('error', {}).get('message', 'Unknown error')
            print(f"  ✗ 失败: {error_msg}")
            results.append({
                "path": output_path,
                "scene": scene,
                "prompt": prompt,
                "status": "error",
                "error": error_msg
            })
            failed_count += 1
        
        # 避免频繁调用
        if i < count - 1:
            time.sleep(2)
    
    print()
    print("=" * 60)
    print(f"完成: 成功 {success_count} 张，失败 {failed_count} 张")
    print(f"输出目录: {output_dir}")
    print("=" * 60)
    
    logger.log_operation(
        module="generate_product_details",
        action="complete",
        details=f"success={success_count}, failed={failed_count}"
    )
    
    return {
        "status": "success" if failed_count == 0 else "partial",
        "output_dir": str(output_dir),
        "total": count,
        "success_count": success_count,
        "failed_count": failed_count,
        "images": results
    }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="生成产品详情图")
    parser.add_argument("image", help="输入图片路径")
    parser.add_argument("--output", "-o", help="输出目录")
    parser.add_argument("--count", "-n", type=int, default=9, help="生成数量，默认 9")
    parser.add_argument("--ratio", "-r", default="1:1", help="宽高比，默认 1:1")
    parser.add_argument("--resolution", default="2K", help="分辨率，默认 2K")
    parser.add_argument("--no-reference", action="store_true", help="不使用输入图片作为参考")
    
    args = parser.parse_args()
    
    result = generate_product_details(
        image_path=args.image,
        output_dir=args.output,
        count=args.count,
        aspect_ratio=args.ratio,
        resolution=args.resolution,
        use_input_image=not args.no_reference
    )
    
    if result['status'] == 'error':
        sys.exit(1)
    
    # 输出 JSON 结果
    print()
    print("RESULT:")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
