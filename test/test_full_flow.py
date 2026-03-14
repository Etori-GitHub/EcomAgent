"""测试完整流程：模拟用户发图 → 生成9张广告图"""
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from generate_images import generate_images


def test_full_flow():
    """测试完整生图流程"""
    print("=" * 60)
    print("测试完整流程：用户发图 → 生成9张广告图")
    print("=" * 60)
    
    # 测试图片路径（尝试多个可能的文件名）
    img_dir = Path(__file__).parent / "img"
    possible_names = ["test.png", "test.jpg", "test_product.png", "test_product.jpg", "product.png", "product.jpg"]
    
    test_image = None
    for name in possible_names:
        candidate = img_dir / name
        if candidate.exists():
            test_image = candidate
            break
    
    # 如果还是找不到，列出目录
    if not test_image.exists():
        img_dir = Path(__file__).parent / "img"
        print(f"\n[Error] 找不到测试图片")
        print(f"目录 {img_dir} 中的文件：")
        if img_dir.exists():
            for f in img_dir.iterdir():
                print(f"  - {f.name}")
        else:
            print("  (目录不存在)")
        return 1
    
    print(f"\n测试图片: {test_image}")
    print(f"图片大小: {test_image.stat().st_size / 1024:.1f} KB")
    print("-" * 60)
    
    # 模拟用户ID
    test_user_id = "ou_test_user_12345"
    
    print("\n开始生成...")
    print("(这可能需要几分钟，请耐心等待)")
    print()
    
    # 执行生图流程
    result = generate_images(
        image_path=str(test_image),
        user_id=test_user_id,
        provider_name="flash_image",
        output_dir=None  # 使用默认时间戳目录
    )
    
    # 显示结果
    print("\n" + "=" * 60)
    print("生成结果:")
    print("=" * 60)
    
    if result['status'] == 'success':
        print(f"✓ 成功生成 {result['success_count']}/{result['total']} 张图片")
        print(f"✓ 输出目录: {result['output_dir']}")
        print("\n生成的图片:")
        for img in result['images']:
            status = "✓" if img['status'] == 'success' else "✗"
            print(f"  {status} [{img['index']}] {img['scene']}")
            if img['status'] == 'success':
                print(f"      → {img['output_path']}")
        return 0
    else:
        print(f"✗ 生成失败")
        print(f"  错误: {result.get('error', {}).get('message', 'Unknown error')}")
        return 1


if __name__ == "__main__":
    sys.exit(test_full_flow())
