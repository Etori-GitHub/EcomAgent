# -*- coding: utf-8 -*-
"""生视频功能脚本 V2 - 3图3视频合成版

输入参数：
    --image: 输入产品图片路径（必需）
    --user_id: 飞书用户ID（可选，用于发送结果）
    --duration: 每段视频时长（默认：5秒）
    --resolution: 分辨率（默认：480p，可选：720p）
    --output_dir: 输出目录（可选，默认按时间创建）

输出：
    - 3张场景图：output/YYYYMMDD_HHMMSS/scene_01~03.png
    - 3套提示词：output/YYYYMMDD_HHMMSS/prompts_01~03.txt
    - 3段视频：output/YYYYMMDD_HHMMSS/video_01~03.mp4
    - 1段合成视频：output/YYYYMMDD_HHMMSS/video_merged.mp4
    - 结果记录：output/YYYYMMDD_HHMMSS/result.json
"""
# -*- coding: utf-8 -*-
import argparse
import json
import sys
import time
import io
from datetime import datetime
from pathlib import Path

# 修复 Windows 控制台乱码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent))

from providers.flash_image import FlashImageProvider
from providers.grok_video import GrokVideoProvider
from providers.gemini_prompt import GeminiPromptProvider
from utils.logger import get_logger
from utils.feishu import send_text, send_image
from utils.video_merger import merge_vovies


# 3套不同风格的场景描述模板
SCENE_STYLES = [
    {
        "name": "简约现代",
        "name_en": "Minimalist Modern",
        "scene": "clean white marble surface with soft natural daylight, minimalist Scandinavian interior, subtle shadow play, professional studio atmosphere with modern geometric props, pure and elegant composition",
        "light": "front-left large window"
    },
    {
        "name": "奢华高端",
        "name_en": "Luxury Premium",
        "scene": "premium dark wood surface with gold accents, dramatic cinematic lighting, velvet texture background, luxury boutique atmosphere, sophisticated high-end product showcase with subtle reflections",
        "light": "front-right soft spotlight with rim light"
    },
    {
        "name": "生活化场景",
        "name_en": "Lifestyle Cozy",
        "scene": "warm wooden table at golden hour, cozy home environment with soft bokeh background, natural window light, casual lifestyle setting with complementary everyday objects, inviting and relatable atmosphere",
        "light": "front-left natural window"
    }
]

# 场景图生成提示词模板
SCENE_PROMPT_TEMPLATE = """Photorealistic professional e-commerce lifestyle product photography using the exact reference image as the product source -- the product must remain 100% identical in every single detail: precise shape, exact original colors, perfect logo/text/font placement and spelling, identical packaging, materials, textures, labels, proportions, reflections, no alterations, no redesign, no stylization, no improvements, no hallucinations or changes whatsoever to the product itself. Preserve all original features faithfully with maximum fidelity. Integrate the unchanged product naturally and seamlessly into a premium, aspirational real-life usage scene: {scene_description}. High-end commercial advertising style with premium advertising aesthetic, world-class photography quality, fixed 9:16 vertical aspect ratio composition, subject positioned as the clear focal point commanding viewer attention, sophisticated and balanced composition, ideal hero product placement and flattering angle for online store showcase, professional cinematic lighting: soft diffused key light from {light_direction} + gentle natural fill + subtle realistic rim/highlight on product edges, accurate soft shadows falling naturally on surfaces, realistic reflections and caustics where appropriate, shallow to medium depth of field with creamy background blur (f/2.8-f/4 aesthetic), razor-sharp critical focus exclusively on the product, hyper-realistic materials and surfaces, clean aspirational mood that evokes desire and quality, no text overlays, no watermarks, no distracting or obscuring elements on or covering the product. Ultra-high resolution 8K, RAW photo quality, shot on professional full-frame camera like Canon EOS R5 or Sony A1 with 85mm or 100mm prime lens, subtle film-like color grading."""

# 视频生成提示词模板
VIDEO_PROMPT_TEMPLATE = """Using the uploaded reference image as the exact product and starting scene, create a premium cinematic product advertisement video. First analyze the product's theme, design style, colors, materials, and surrounding environment in the image, then craft a natural, engaging, story-driven showcase that feels like a high-end commercial. Feature elegant dynamic product showcase with subtle, realistic interactions relevant to the product (such as gentle handling, natural usage, pouring, wearing, or environmental interaction) while keeping the product perfectly centered and heroically highlighted. Showcase the product through dynamic camera movements and professional cinematography techniques. Use smooth, fluid cinematic camera movements -- slow push-in, gentle tracking shot, subtle elegant orbit, or graceful dolly -- to reveal beautiful details from multiple flattering angles in a seamless, continuous flow. Maintain 100% visual fidelity to the original product in every frame: exact shape, precise colors, perfect logo placement and text, identical materials, textures, reflections, and all details -- no morphing, distortion, hallucination, or added parts whatsoever. CRITICAL: Maintain the exact aspect ratio and proportions of the original product image, strictly prohibit any stretching, squeezing, or distortion of the product shape. Preserve the original width-to-height ratio of all items in the image. Enhance the original scene with consistent premium atmosphere, professional soft studio wrap-around lighting plus natural cinematic enhancements, realistic sliding reflections and soft shadows that perfectly match the motion. Output an ultra-cinematic product advertisement video: ultra-smooth 60fps-like fluid motion, hyper-realistic photorealistic rendering, razor-sharp clarity and ultra-high detail, professional Hollywood color grading, high dynamic range, cinematic depth of field, clean aspirational mood, masterpiece commercial quality, no artifacts, no jitter, no flicker. Negative: choppy transitions, erratic movement, background changes or flicker, excessive zooming, shape distortion, blurry details, low quality, morphing, artifacts, unnatural motion, stretching, squeezing, aspect ratio changes."""


def generate_scene_prompts(image_path: str, styles: list) -> list:
    """
    生成3套场景描述
    
    Args:
        image_path: 产品图片路径
        styles: 风格配置列表
    
    Returns:
        list: 3套场景提示词和元数据
    """
    print("=" * 60)
    print("生成3套场景描述")
    print("=" * 60)
    
    prompts = []
    for i, style in enumerate(styles, 1):
        scene_prompt = SCENE_PROMPT_TEMPLATE.format(
            scene_description=style["scene"],
            light_direction=style["light"]
        )
        prompts.append({
            "index": i,
            "name": style["name"],
            "name_en": style["name_en"],
            "scene": style["scene"],
            "light": style["light"],
            "prompt": scene_prompt
        })
        print(f"  [{i}] {style['name']}: {style['scene'][:50]}...")
    
    return prompts


def generate_video_v2(image_path: str, user_id: str = None, duration: int = 5,
                      resolution: str = "480p", output_dir: Path = None) -> dict:
    """
    生成产品营销视频 V2 - 3图3视频合成版
    
    流程：
        Step 1: 生成3套场景描述
        Step 2: 生成3张场景图 (FlashImage)
        Step 3: 生成3段视频 (Grok)
        Step 4: 合并视频
    
    Args:
        image_path: 输入产品图片路径
        user_id: 飞书用户ID（用于发送结果）
        duration: 每段视频时长（秒）
        resolution: 分辨率 (480p/720p)
        output_dir: 输出目录（默认按时间创建）
    
    Returns:
        {
            "status": "success|error",
            "output_dir": str,
            "scenes": [...],
            "videos": [...],
            "merged_video": str,
            "user_id": str
        }
    """
    logger = get_logger()
    
    # 验证输入图片
    if not Path(image_path).exists():
        error_msg = f"输入图片不存在: {image_path}"
        logger.log_error("generate_video_v2", "validate_input", Exception(error_msg))
        return {"status": "error", "error": {"message": error_msg}}
    
    # 创建输出目录
    if output_dir is None:
        output_dir = Path("output") / datetime.now().strftime("%Y%m%d_%H%M%S")
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.log_operation(
        module="generate_video_v2",
        action="start",
        params={"image": image_path, "duration": duration, "resolution": resolution, "user_id": user_id},
        result={"output_dir": str(output_dir)}
    )
    
    print("=" * 60)
    print("生成产品营销视频 V2 - 3图3视频合成版")
    print("=" * 60)
    print(f"输入: {image_path}")
    print(f"时长: {duration}s/段 | 分辨率: {resolution}")
    print(f"输出: {output_dir}")
    print()
    
    # 通知用户开始生成
    if user_id:
        send_text(user_id, "开始生成视频...\n第1步：生成3套场景描述和场景图")
    
    # Step 1 & 2: 生成3套场景描述和3张场景图
    print("[步骤1/4] 生成3套场景描述和场景图...")
    
    scene_prompts = generate_scene_prompts(image_path, SCENE_STYLES)
    flash = FlashImageProvider()
    
    scenes = []
    for i, scene_data in enumerate(scene_prompts, 1):
        print(f"\n  生成场景图 [{i}/3] - {scene_data['name']}...")
        
        scene_path = str(output_dir / f"scene_{i:02d}.png")
        
        # 重试机制 - VPN不稳定，增加冗余时间
        max_retries = 5
        result = None
        for attempt in range(max_retries):
            try:
                result = flash.generate_image(
                    prompt=scene_data["prompt"],
                    output_path=scene_path,
                    input_image=image_path,
                    aspect_ratio="9:16",
                    resolution="2K"
                )
                if result['status'] == 'success':
                    break
                # 失败时等待后重试 - 指数退避
                if attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)
                    print(f"  [Retry] 场景图{i}生成失败，{wait_time}秒后重试 ({attempt+1}/{max_retries-1})...")
                    time.sleep(wait_time)
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)
                    print(f"  [Retry] 场景图{i}异常，{wait_time}秒后重试 ({attempt+1}/{max_retries-1}): {e}")
                    time.sleep(wait_time)
                else:
                    result = {"status": "error", "error": {"message": str(e)}}
        
        if result is None or result['status'] != 'success':
            error_msg = result.get('error', {}).get('message', f'场景图{i}生成失败') if result else f'场景图{i}生成失败'
            logger.log_error("generate_video_v2", f"generate_scene_{i}", Exception(error_msg))
            if user_id:
                send_text(user_id, f"场景图{i}生成失败: {error_msg}")
            return {"status": "error", "error": {"message": error_msg}}
        
        # 每张图生成后等待，避免API限流 - VPN不稳定多留冗余
        if i < len(scene_prompts):
            print(f"  [Wait] 等待3秒后继续生成下一张...")
            time.sleep(3)
        
        print(f"  [OK] 场景图{i}生成成功: {scene_path}")
        
        # 保存提示词
        prompt_file = output_dir / f"prompts_{i:02d}.txt"
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(f"场景 {i}: {scene_data['name']}\n")
            f.write(f"Scene EN: {scene_data['name_en']}\n")
            f.write(f"描述: {scene_data['scene']}\n")
            f.write(f"光照: {scene_data['light']}\n\n")
            f.write("完整提示词:\n")
            f.write("-" * 60 + "\n")
            f.write(scene_data["prompt"])
        print(f"  [OK] 提示词已保存: {prompt_file}")
        
        # 发送给用户
        if user_id:
            caption = f"场景图 [{i}/3] - {scene_data['name']}"
            send_image(user_id, scene_path, caption)
        
        scenes.append({
            "index": i,
            "name": scene_data["name"],
            "scene_path": scene_path,
            "prompt_file": str(prompt_file)
        })
    
    # 通知用户场景图完成
    if user_id:
        send_text(user_id, "3张场景图生成完成！\n第2步：生成3段视频...")
    
    # Step 3: 生成3段视频
    print("\n[步骤2/4] 生成3段视频...")
    
    grok = GrokVideoProvider()
    videos = []
    
    for i, scene in enumerate(scenes, 1):
        print(f"\n  生成视频 [{i}/3] - {scene['name']}...")
        
        video_path = str(output_dir / f"video_{i:02d}.mp4")
        
        result = grok.generate_video(
            prompt=VIDEO_PROMPT_TEMPLATE,
            output_path=video_path,
            input_image=scene["scene_path"],
            duration=duration,
            resolution=resolution,
            aspect_ratio="9:16"
        )
        
        if result['status'] != 'success':
            error_msg = result.get('error', {}).get('message', f'视频{i}生成失败')
            logger.log_error("generate_video_v2", f"generate_video_{i}", Exception(error_msg))
            if user_id:
                send_text(user_id, f"视频{i}生成失败: {error_msg}")
            return {"status": "error", "error": {"message": error_msg}}
        
        print(f"  [OK] 视频{i}生成成功: {video_path}")
        
        # 发送给用户
        if user_id:
            caption = f"视频 [{i}/3] - {scene['name']}"
            send_image(user_id, video_path, caption)
        
        videos.append({
            "index": i,
            "name": scene["name"],
            "video_path": video_path
        })
    
    # 通知用户视频生成完成
    if user_id:
        send_text(user_id, "3段视频生成完成！\n第3步：合并视频...")
    
    # Step 4: 合并视频
    print("\n[步骤3/4] 合并3段视频...")
    
    video_paths = [v["video_path"] for v in videos]
    merged_path = str(output_dir / "video_merged.mp4")
    
    merge_result = merge_vovies(video_paths, merged_path)
    
    if merge_result['status'] != 'success':
        error_msg = merge_result.get('error', {}).get('message', '视频合并失败')
        logger.log_error("generate_video_v2", "merge_videos", Exception(error_msg))
        if user_id:
            send_text(user_id, f"视频合并失败: {error_msg}")
        return {"status": "error", "error": {"message": error_msg}}
    
    print(f"  [OK] 视频合并成功: {merged_path}")
    
    # 发送合成视频给用户
    if user_id:
        caption = "合成视频完成！🎬\n3段视频已合并为1段完整视频"
        send_image(user_id, merged_path, caption)
    
    # 完成
    print("\n" + "=" * 60)
    print("[OK] 所有步骤完成!")
    print(f"  场景图: {len(scenes)} 张")
    print(f"  视频: {len(videos)} 段")
    print(f"  合成视频: {merged_path}")
    print("=" * 60)
    
    # 构建返回结果
    result = {
        "status": "success",
        "output_dir": str(output_dir),
        "scenes": scenes,
        "videos": videos,
        "merged_video": merged_path,
        "user_id": user_id
    }
    
    # 保存结果
    result_file = output_dir / "result.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    logger.log_operation(
        module="generate_video_v2",
        action="complete",
        params={"image": image_path, "duration": duration, "resolution": resolution},
        result={"scenes": len(scenes), "videos": len(videos), "merged": merged_path}
    )
    
    print(f"\n结果已保存: {result_file}")
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description='生成产品营销视频 V2 - 3图3视频合成版',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python src/generate_video_v2.py --image product.jpg
  python src/generate_video_v2.py --image product.jpg --user_id ou_xxx --duration 5 --resolution 720p
        """
    )
    parser.add_argument('--image', required=True, help='输入产品图片路径')
    parser.add_argument('--user_id', help='飞书用户ID（用于发送结果）')
    parser.add_argument('--duration', type=int, default=5, help='每段视频时长（秒，默认：5）')
    parser.add_argument('--resolution', default='480p', choices=['480p', '720p'],
                        help='分辨率（默认：480p）')
    parser.add_argument('--output_dir', help='输出目录（默认按时间创建）')
    
    args = parser.parse_args()
    
    result = generate_video_v2(
        image_path=args.image,
        user_id=args.user_id,
        duration=args.duration,
        resolution=args.resolution,
        output_dir=Path(args.output_dir) if args.output_dir else None
    )
    
    # 输出 JSON 结果（供其他脚本解析）
    print("\n" + "=" * 60)
    print("[VIDEO_RESULT] " + json.dumps(result, ensure_ascii=False))
    
    return 0 if result['status'] == 'success' else 1


if __name__ == "__main__":
    sys.exit(main())
