"""ImgBB 图床上传工具"""

import base64
import time
import requests
from pathlib import Path
from typing import Union


IMGBB_API_KEY = "6d2e4a6a74c5ac763e101836277ace4a"
IMGBB_UPLOAD_URL = "https://api.imgbb.com/1/upload"


def upload_image(
    image_path: Union[str, Path],
    expiration: int = 600,  # 默认10分钟后删除
    max_size_kb: int = 500  # 最大尺寸 KB，超过会压缩
) -> dict:
    """
    上传图片到 ImgBB 图床

    Args:
        image_path: 本地图片路径
        expiration: 过期时间（秒），60-15552000，默认600秒（10分钟）
        max_size_kb: 最大尺寸 KB，超过会自动压缩

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

        # 检查图片大小，如果超过限制则压缩
        from PIL import Image
        import io
        
        img = Image.open(image_path)
        original_size_kb = image_path.stat().st_size / 1024
        
        print(f"[ImgBB] 上传图片: {image_path.name} ({original_size_kb:.1f} KB)...")
        
        # 如果图片太大，压缩到 max_size_kb
        if original_size_kb > max_size_kb:
            print(f"[ImgBB] 图片太大，正在压缩到 {max_size_kb} KB...")
            
            # 尝试不同的压缩质量
            quality = 85
            while quality >= 50:
                buffer = io.BytesIO()
                # 如果是 PNG，转为 JPEG 压缩
                if img.format == 'PNG' and img.mode in ('RGBA', 'LA', 'P'):
                    # 保持透明度，转为 RGB（白色背景）
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    background.save(buffer, format='JPEG', quality=quality, optimize=True)
                else:
                    img.save(buffer, format='JPEG', quality=quality, optimize=True)
                
                compressed_size_kb = len(buffer.getvalue()) / 1024
                if compressed_size_kb <= max_size_kb:
                    print(f"[ImgBB] 压缩成功: {compressed_size_kb:.1f} KB (quality={quality})")
                    image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    break
                
                quality -= 5
            else:
                # 如果还是太大，使用最低质量
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=50, optimize=True)
                image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
                print(f"[ImgBB] 使用最低质量: {len(buffer.getvalue()) / 1024:.1f} KB")
        else:
            # 图片大小合适，直接读取
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')

        # 上传参数
        payload = {
            "key": IMGBB_API_KEY,
            "image": image_data,
            "expiration": expiration
        }

        # 发送请求，禁用代理，增加超时时间
        # 读取代理配置
        proxy_url = None
        try:
            settings_file = Path(__file__).parent.parent.parent / "config" / "settings.json"
            if settings_file.exists():
                import json as json_module
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json_module.load(f)
                    proxy_config = settings.get('proxy', {})
                    if proxy_config.get('enabled', True):
                        host = proxy_config.get('host', '127.0.0.1')
                        port = proxy_config.get('port', 7890)
                        proxy_url = f"http://{host}:{port}"
        except:
            pass
        
        if not proxy_url:
            proxy_url = 'http://127.0.0.1:7890'
        
        print(f"[ImgBB] Using proxy: {proxy_url}")
        
        # 重试机制：最多3次
        for retry_attempt in range(3):
            try:
                if retry_attempt > 0:
                    wait_time = 10 * retry_attempt  # 10s, 20s
                    print(f"[ImgBB] Retry {retry_attempt}/3, waiting {wait_time}s...")
                    time.sleep(wait_time)
                
                # 先尝试用代理
                try:
                    response = requests.post(
                        IMGBB_UPLOAD_URL, 
                        data=payload, 
                        timeout=120,
                        proxies={"http": proxy_url, "https": proxy_url}
                    )
                except requests.exceptions.ProxyError:
                    # 代理失败，直连尝试
                    print(f"[ImgBB] Proxy failed, trying direct connection...")
                    response = requests.post(
                        IMGBB_UPLOAD_URL, 
                        data=payload, 
                        timeout=120,
                        proxies={"http": None, "https": None}
                    )
                
                response.raise_for_status()
                break  # 成功则跳出重试循环
                
            except (requests.exceptions.RequestException, requests.exceptions.ProxyError) as e:
                print(f"[ImgBB] Upload attempt {retry_attempt + 1}/3 failed: {str(e)}")
                if retry_attempt == 2:
                    # 最后一次重试也失败
                    return {
                        "status": "error",
                        "error": {"message": f"Request failed after 3 retries: {str(e)}"}
                    }
                continue
        
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
