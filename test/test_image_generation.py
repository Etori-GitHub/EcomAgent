"""测试图片生成功能"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from providers import FlashImageProvider


def test_flash_image():
    """测试 Flash Image Provider"""
    print("=" * 60)
    print("测试 Flash Image 生图")
    print("=" * 60)
    
    provider = FlashImageProvider()
    print(f"使用模型: {provider.model_name}")
    
    prompt = "A beautiful white wireless headphone on clean white background, professional studio lighting, photorealistic"
    output_path = "test/test_output.png"
    
    print(f"\n提示词: {prompt[:60]}...")
    print(f"输出路径: {output_path}")
    print("-" * 60)
    
    result = provider.generate_image(
        prompt=prompt,
        output_path=output_path,
        aspect_ratio="1:1",
        resolution="2K"
    )
    
    if result['status'] == 'success':
        print(f"\n✓ 图片生成成功!")
        print(f"  保存路径: {result['output_path']}")
        return 0
    else:
        print(f"\n✗ 图片生成失败")
        print(f"  错误: {result.get('error', {}).get('message')}")
        return 1


if __name__ == "__main__":
    sys.exit(test_flash_image())
