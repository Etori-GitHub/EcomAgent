"""ImgBB 图床上传工具"""

import base64
import requests
from pathlib import Path
from typing import Union


IMGBB_API_KEY = "6d2e4a6a74c5ac763e101836277ace4a"
IMGBB_UPLOAD_URL = "https://api.imgbb.com/1/upload"


def upload_image(
    image_path: Union[str, Path],
    expiration: int = 600  # 默认10分钟后删除
) -> dict:
    """
    上传图片到 ImgBB 图床

    Args:
        image_path: 本地图片路径
        expiration: 过期时间（秒），60-15552000，默认600秒（10分钟）

    Returns:
        {
            "status": "success" | "error",
            "url": str,  # 直接图片URL
            "display_url": str,
            "delete_url": str,
            "error": {...}
        }
    """
    try:
        image_path = Path(image_path)
        if not image_path.exists():
            return {
                "status": "error",
                "error": {"message": f"Image not found: {image_path}"}
            }

        # 读取图片并转为 base64
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

        # 上传参数
        payload = {
            "key": IMGBB_API_KEY,
            "image": image_data,
            "expiration": expiration
        }

        print(f"[ImgBB] 上传图片: {image_path.name} ({image_path.stat().st_size / 1024:.1f} KB)...")

        # 发送请求，增加超时时间
        response = requests.post(IMGBB_UPLOAD_URL, data=payload, timeout=120)
        response.raise_for_status()

        result = response.json()

        if result.get("success"):
            data = result["data"]
            print(f"[ImgBB] 上传成功!")
            print(f"  URL: {data['url']}")
            return {
                "status": "success",
                "url": data["url"],
                "display_url": data["display_url"],
                "delete_url": data["delete_url"],
                "expiration": expiration
            }
        else:
            return {
                "status": "error",
                "error": {"message": "Upload failed", "response": result}
            }

    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error": {"message": f"Request failed: {str(e)}"}
        }
    except Exception as e:
        return {
            "status": "error",
            "error": {"message": str(e)}
        }


def delete_image(delete_url: str) -> bool:
    """
    删除已上传的图片

    Args:
        delete_url: 上传时返回的 delete_url

    Returns:
        bool: 是否删除成功
    """
    try:
        response = requests.get(delete_url, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"[ImgBB] 删除失败: {e}")
        return False


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='上传图片到 ImgBB')
    parser.add_argument('image', help='本地图片路径')
    parser.add_argument('--expiration', type=int, default=600, help='过期时间（秒），默认600')

    args = parser.parse_args()

    result = upload_image(args.image, args.expiration)

    if result['status'] == 'success':
        print(f"\n✓ 上传成功")
        print(f"  图片URL: {result['url']}")
        print(f"  删除URL: {result['delete_url']}")
    else:
        print(f"\n✗ 上传失败: {result['error']['message']}")
        sys.exit(1)
