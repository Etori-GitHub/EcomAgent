# -*- coding: utf-8 -*-
"""测试模式脚本 - 保存图片到output，再发回飞书

输入参数：
    --image: 输入产品图片路径（必需）
    --user_id: 飞书用户ID（必需）

输出：
    - 保存图片到 output/test_mode/YYYYMMDD_HHMMSS/
    - 发送回飞书
"""
import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

# 修复 Windows 控制台乱码
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

sys.path.insert(0, str(Path(__file__).parent))

from utils.feishu import send_text, send_image


def handle_test_mode(image_path: str, user_id: str) -> dict:
    """
    处理测试模式：保存图片到output，再发回飞书
    
    Args:
        image_path: 图片路径
        user_id: 飞书用户ID
    
    Returns:
        {
            "status": "success|error",
            "output_path": str,
            "user_id": str
        }
    """
    try:
        # 验证输入图片
        if not Path(image_path).exists():
            error_msg = f"输入图片不存在: {image_path}"
            print(f"[ERROR] {error_msg}")
            return {"status": "error", "error": {"message": error_msg}}
        
        # 创建输出目录
        output_dir = Path("output") / "test_mode" / datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 复制图片到output
        dest_path = output_dir / Path(image_path).name
        shutil.copy2(image_path, dest_path)
        
        print(f"[OK] 图片已保存到: {dest_path}")
        
        # 发送回飞书
        if user_id:
            send_success = send_image(user_id, str(dest_path), "测试模式：图片已保存到output目录")
            if send_success:
                print(f"[OK] 图片已发送回飞书: user={user_id}")
            else:
                print(f"[WARN] 发送图片失败: user={user_id}")
        
        return {
            "status": "success",
            "output_path": str(dest_path),
            "user_id": user_id
        }
        
    except Exception as e:
        error_msg = f"测试模式处理失败: {e}"
        print(f"[ERROR] {error_msg}")
        return {"status": "error", "error": {"message": error_msg}}


def main():
    parser = argparse.ArgumentParser(
        description='测试模式：保存图片到output，再发回飞书',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--image', required=True, help='输入产品图片路径')
    parser.add_argument('--user_id', required=True, help='飞书用户ID')
    
    args = parser.parse_args()
    
    result = handle_test_mode(
        image_path=args.image,
        user_id=args.user_id
    )
    
    # 输出 JSON 结果（供 monitor.py 解析）
    print("\n" + "=" * 60)
    print("[TEST_MODE_RESULT] " + json.dumps(result, ensure_ascii=False))
    
    return 0 if result['status'] == 'success' else 1


if __name__ == "__main__":
    sys.exit(main())
