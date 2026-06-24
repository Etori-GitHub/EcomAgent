"""图片比例调整工具 - 填充到目标比例"""

from PIL import Image
from pathlib import Path
from typing import Union


def pad_to_aspect_ratio(
    image_path: Union[str, Path],
    target_ratio: str = "9:16",
    output_path: Union[str, Path] = None,
    bg_color: tuple = (255, 255, 255)  # 白色背景
) -> dict:
    """
    将图片填充到目标比例（不裁剪，不缩放）
    
    Args:
        image_path: 输入图片路径
        target_ratio: 目标比例，如 "9:16", "1:1", "16:9"
        output_path: 输出路径（默认原地替换）
        bg_color: 填充背景色 RGB
    
    Returns:
        {
            "status": "success" | "error",
            "output_path": str,
            "original_size": tuple,
            "new_size": tuple,
            "error": {...}
        }
    """
    try:
        image_path = Path(image_path)
        if not image_path.exists():
            return {"status": "error", "error": {"message": f"Image not found: {image_path}"}}
        
        # 解析目标比例
        parts = target_ratio.split(":")
        target_w = int(parts[0])
        target_h = int(parts[1])
        target_ratio_value = target_w / target_h
        
        # 加载图片
        img = Image.open(image_path)
        orig_w, orig_h = img.size
        orig_ratio = orig_w / orig_h
        
        # 计算新尺寸
        if orig_ratio > target_ratio_value:
            # 图片太宽，需要增加高度
            new_w = orig_w
            new_h = int(orig_w / target_ratio_value)
            # 原图放在中间
            paste_x = 0
            paste_y = (new_h - orig_h) // 2
        else:
            # 图片太高，需要增加宽度
            new_h = orig_h
            new_w = int(orig_h * target_ratio_value)
            # 原图放在中间
            paste_x = (new_w - orig_w) // 2
            paste_y = 0
        
        # 创建新图片（白底）
        new_img = Image.new("RGB", (new_w, new_h), bg_color)
        
        # 粘贴原图
        new_img.paste(img, (paste_x, paste_y))
        
        # 保存
        if output_path is None:
            output_path = image_path
        else:
            output_path = Path(output_path)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        new_img.save(output_path)
        
        return {
            "status": "success",
            "output_path": str(output_path),
            "original_size": (orig_w, orig_h),
            "new_size": (new_w, new_h),
            "padding": {"top": paste_y, "bottom": new_h - orig_h - paste_y, "left": paste_x, "right": new_w - orig_w - paste_x}
        }
        
    except Exception as e:
        return {"status": "error", "error": {"message": str(e)}}


def check_aspect_ratio(image_path: Union[str, Path], expected_ratio: str = "9:16") -> dict:
    """
    检查图片比例是否符合预期
    
    Args:
        image_path: 图片路径
        expected_ratio: 期望比例
    
    Returns:
        {
            "status": "success",
            "matches": bool,
            "current_size": tuple,
            "current_ratio": float,
            "expected_ratio": float
        }
    """
    try:
        img = Image.open(image_path)
        w, h = img.size
        current_ratio = w / h
        
        parts = expected_ratio.split(":")
        expected_ratio_value = int(parts[0]) / int(parts[1])
        
        # 允许 5% 误差
        matches = abs(current_ratio - expected_ratio_value) < 0.05
        
        return {
            "status": "success",
            "matches": matches,
            "current_size": (w, h),
            "current_ratio": current_ratio,
            "expected_ratio": expected_ratio_value
        }
        
    except Exception as e:
        return {"status": "error", "error": {"message": str(e)}}


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="调整图片比例")
    parser.add_argument("image", help="输入图片路径")
    parser.add_argument("--ratio", default="9:16", help="目标比例")
    parser.add_argument("--output", help="输出路径（默认原地替换）")
    parser.add_argument("--check", action="store_true", help="仅检查比例")
    
    args = parser.parse_args()
    
    if args.check:
        result = check_aspect_ratio(args.image, args.ratio)
        if result["status"] == "success":
            print(f"当前尺寸: {result['current_size']}")
            print(f"当前比例: {result['current_ratio']:.2f}")
            print(f"期望比例: {result['expected_ratio']:.2f}")
            print(f"匹配: {result['matches']}")
        else:
            print(f"错误: {result['error']['message']}")
    else:
        result = pad_to_aspect_ratio(args.image, args.ratio, args.output)
        if result["status"] == "success":
            print(f"✓ 调整成功")
            print(f"  原尺寸: {result['original_size']}")
            print(f"  新尺寸: {result['new_size']}")
            print(f"  填充: {result['padding']}")
            print(f"  输出: {result['output_path']}")
        else:
            print(f"✗ 错误: {result['error']['message']}")