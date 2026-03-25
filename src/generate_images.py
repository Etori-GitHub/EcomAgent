# -*- coding: utf-8 -*-
"""生图功能脚本 - 编排生成9张营销图

输入参数：
    --image: 输入产品图片路径（必需）
    --user_id: 飞书用户ID（可选，用于发送结果）
    --provider: 使用的生图provider（默认：flash_image）
    --output_dir: 输出目录（可选，默认按时间创建）

输出：
    - 9张营销图：output/YYYYMMDD_HHMMSS/{00-08}_marketing.png
    - 提示词记录：output/YYYYMMDD_HHMMSS/prompts.json
    - 结果汇总：output/YYYYMMDD_HHMMSS/result.json

过程文件：
    - 日志记录：logs/YYYYMMDD.log
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from providers import FlashImageProvider, GeminiPromptProvider
from utils.logger import get_logger


def generate_images(
    image_path: str,
    user_id: str = None,
    provider_name: str = "flash_image",
    output_dir: str = None
) -> dict:
    """
    完整的生图流程：分析图片 → 生成提示词 → 生成9张图
    
    Args:
        image_path: 输入产品图片路径
        user_id: 飞书用户ID（用于发送结果）
        provider_name: 使用的 provider（flash_image/seedream）
        output_dir: 输出目录（默认按时间创建）
    
    Returns:
        {
            "status": "success|error",
            "output_dir": str,
            "total": int,
            "success_count": int,
            "images": [...],
            "user_id": str
        }
    """
    logger = get_logger()
    
    # 验证输入图片
    if not Path(image_path).exists():
        error_msg = f"输入图片不存在: {image_path}"
        logger.log_error("generate_images", "validate_input", Exception(error_msg))
        return {"status": "error", "error": {"message": error_msg}}
    
    # 创建输出目录
    if output_dir is None:
        output_dir = Path("output") / datetime.now().strftime("%Y%m%d_%H%M%S")
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.log_operation(
        module="generate_images",
        action="start",
        params={"image": image_path, "provider": provider_name, "user_id": user_id},
        result={"output_dir": str(output_dir)}
    )
    
    print(f"开始生成营销图...")
    print(f"输入图片: {image_path}")
    print(f"输出目录: {output_dir}")
    print("-" * 60)
    
    # 第1步：Gemini 生成提示词
    print("[1/2] 正在分析产品图片，生成9个营销场景提示词...")
    
    prompt_provider = GeminiPromptProvider()
    prompt_result = prompt_provider.generate_image_prompts(
        image_path=image_path,
        count=9,
        language="english"
    )
    
    if prompt_result['status'] != 'success':
        error_msg = prompt_result.get('error', {}).get('message', '生成提示词失败')
        logger.log_error("generate_images", "generate_prompts", Exception(error_msg))
        return {"status": "error", "error": {"message": error_msg}}
    
    prompts = prompt_result['prompts']
    scenes = prompt_result['scenes']
    
    print(f"[OK] 提示词生成完成")
    for i, (scene, prompt) in enumerate(zip(scenes, prompts)):
        print(f"  [{i}] {scene}: {prompt[:50]}...")
    
    # 保存提示词
    prompts_file = output_dir / "prompts.json"
    with open(prompts_file, 'w', encoding='utf-8') as f:
        json.dump({
            "scenes": scenes,
            "prompts": prompts,
            "input_image": image_path
        }, f, ensure_ascii=False, indent=2)
    
    # 第2步：选择 Provider 并逐张生成图片（每生成一张就发送一张）
    print(f"\n[2/2] 使用 {provider_name} 生成9张营销图...")
    
    if provider_name == "flash_image":
        image_provider = FlashImageProvider()
    else:
        error_msg = f"未知的 provider: {provider_name}"
        logger.log_error("generate_images", "select_provider", Exception(error_msg))
        return {"status": "error", "error": {"message": error_msg}}
    
    # 导入发送函数
    from utils.feishu import send_text, send_image
    
    # 先发送开始生成的通知
    if user_id:
        send_text(user_id, "开始生成9张营销图，每生成一张会立即发送给您~")
    
    # 逐张生成并发送
    results = []
    for i, (prompt, scene) in enumerate(zip(prompts, scenes)):
        print(f"\n  生成 [{i+1}/9] {scene}...")
        
        output_path = str(output_dir / f"{i:02d}_marketing.png")
        result = image_provider.generate_image(
            prompt=prompt,
            output_path=output_path,
            aspect_ratio="1:1",
            resolution="2K",
            input_image=image_path
        )
        result['index'] = i
        result['prompt'] = prompt
        result['scene'] = scene
        results.append(result)
        
        # 立即发送给用户
        if user_id:
            if result['status'] == 'success':
                caption = f"[{i+1}/9] {scene}"
                print(f"  [OK] 生成完成，立即发送...")
                try:
                    # 检查图片大小，如果超过 7MB 进行压缩（目标 5MB 以内）
                    image_size = Path(output_path).stat().st_size / (1024 * 1024)  # MB
                    send_path = output_path
                    
                    if image_size > 7:
                        print(f"  [WARN] 图片较大 ({image_size:.1f} MB)，正在压缩...")
                        from PIL import Image as PILImage
                        import tempfile
                        
                        with PILImage.open(output_path) as img:
                            # 转换为 RGB
                            if img.mode in ('RGBA', 'P'):
                                img = img.convert('RGB')
                            
                            # 压缩质量
                            quality = 85
                            while True:
                                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                                    tmp_path = tmp.name
                                img.save(tmp_path, 'JPEG', quality=quality, optimize=True)
                                
                                new_size = Path(tmp_path).stat().st_size / (1024 * 1024)
                                print(f"  [INFO] 压缩质量 {quality}% -> {new_size:.1f} MB")
                                
                                if new_size <= 5 or quality <= 50:
                                    send_path = tmp_path
                                    break
                                
                                # 降低质量继续压缩
                                quality -= 10
                                Path(tmp_path).unlink()
                    
                    send_image(user_id, send_path, caption)
                    
                    # 如果使用了临时压缩文件，删除它
                    if send_path != output_path and Path(send_path).exists():
                        Path(send_path).unlink()
                        
                except Exception as e:
                    print(f"  [FAIL] 发送失败: {e}")
                    send_text(user_id, f"[{i+1}/9] {scene} - 图片生成成功但发送失败")
            else:
                error_msg = result.get('error', {}).get('message', '未知错误')
                print(f"  [FAIL] 生成失败: {error_msg}")
                send_text(user_id, f"[{i+1}/9] {scene} - 生成失败: {error_msg}")
        
        # 短暂延迟避免请求过快
        import time
        time.sleep(1.0)
    
    # 统计结果
    success_count = sum(1 for r in results if r['status'] == 'success')
    
    print(f"\n生成完成: {success_count}/9 成功")
    for i, result in enumerate(results):
        status = "[OK]" if result['status'] == 'success' else "[FAIL]"
        print(f"  {status} [{i}] {scenes[i]}")
    
    # 构建返回结果
    result = {
        "status": "success" if success_count > 0 else "error",
        "output_dir": str(output_dir),
        "total": len(prompts),
        "success_count": success_count,
        "failed_count": len(prompts) - success_count,
        "images": [
            {
                "index": i,
                "scene": scenes[i],
                "prompt": prompts[i],
                "status": r['status'],
                "output_path": r.get('output_path'),
                "error": r.get('error')
            }
            for i, r in enumerate(results)
        ],
        "user_id": user_id
    }
    
    # 保存结果
    result_file = output_dir / "result.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    logger.log_operation(
        module="generate_images",
        action="complete",
        params={"image": image_path, "provider": provider_name},
        result={
            "success_count": success_count,
            "total": len(prompts),
            "output_dir": str(output_dir)
        }
    )
    
    print(f"\n结果已保存:")
    print(f"  图片目录: {output_dir}")
    print(f"  结果文件: {result_file}")
    
    # 发送汇总信息
    if user_id:
        print(f"\n发送汇总到飞书用户: {user_id}")
        from utils.feishu import send_text
        summary = f"生成完成！共 {success_count}/9 张成功\n输出目录: {output_dir}"
        send_text(user_id, summary)
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description='生成9张电商营销图',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python src/generate_images.py --image product.jpg
  python src/generate_images.py --image product.jpg --user_id ou_xxx --provider flash_image
        """
    )
    parser.add_argument('--image', required=True, help='输入产品图片路径')
    parser.add_argument('--user_id', help='飞书用户ID（用于发送结果）')
    parser.add_argument('--provider', default='flash_image', 
                        choices=['flash_image'],
                        help='使用的生图provider（默认：flash_image）')
    parser.add_argument('--output_dir', help='输出目录（默认按时间创建）')
    
    args = parser.parse_args()
    
    result = generate_images(
        image_path=args.image,
        user_id=args.user_id,
        provider_name=args.provider,
        output_dir=args.output_dir
    )
    
    # 输出 JSON 结果（供其他脚本解析）
    print("\n" + "=" * 60)
    print("[GENERATION_RESULT] " + json.dumps(result, ensure_ascii=False))
    
    return 0 if result['status'] == 'success' else 1


if __name__ == "__main__":
    sys.exit(main())
