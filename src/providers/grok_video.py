"""Grok Video Provider - xAI 视频生成"""
import json
import base64
import requests
import time
from pathlib import Path
from typing import Dict, Optional, Union
from PIL import Image
from .base import VideoProvider


class GrokVideoProvider(VideoProvider):
    """Grok (xAI) 视频生成 Provider - 使用 grok-imagine-video 模型"""

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config"

        # 加载 API Key
        keys_file = config_path / "api_keys.json"
        with open(keys_file, 'r', encoding='utf-8') as f:
            keys = json.load(f)

        # 加载配置
        models_file = config_path / "models.json"
        with open(models_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        self.api_key = keys.get('xai', '')
        self.model_name = config['video_providers']['grok']['model']
        self.base_url = "https://api.x.ai/v1"

    def _encode_image(self, image_path: str) -> str:
        """将图片编码为 base64"""
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')

    def _get_mime_type(self, image_path: str) -> str:
        """获取图片 MIME 类型"""
        ext = Path(image_path).suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.webp': 'image/webp'
        }
        return mime_types.get(ext, 'image/jpeg')

    def generate_video(
        self,
        prompt: str,
        output_path: str,
        input_image: Optional[Union[str, Image.Image]] = None,
        duration: int = 5,
        resolution: str = "480p",
        aspect_ratio: str = "16:9",
        max_retries: int = 3
    ) -> Dict:
        """
        生成视频 - 支持文生视频和图生视频（带429重试机制）

        Args:
            prompt: 视频生成提示词
            output_path: 输出视频路径
            input_image: 输入图片路径（图生视频）
            duration: 视频时长（1-15秒）
            resolution: 分辨率（480p 或 720p）
            aspect_ratio: 宽高比（默认 16:9）
            max_retries: 最大重试次数（默认3次，应对429限流）

        Returns:
            Dict: {
                "status": "success" | "error",
                "output_path": str,
                "video_url": str,
                "provider": "grok",
                "error": {...}
            }
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                result = self._generate_video_internal(
                    prompt=prompt,
                    output_path=output_path,
                    input_image=input_image,
                    duration=duration,
                    resolution=resolution,
                    aspect_ratio=aspect_ratio
                )
                
                if result['status'] == 'success':
                    return result
                    
                # 如果是429错误，重试
                error_msg = result.get('error', {}).get('message', '')
                if '429' in error_msg or 'Too Many Requests' in error_msg:
                    last_error = error_msg
                    wait_time = 10 * (attempt + 1)  # 10s, 20s, 30s
                    print(f"[Grok Retry] 429限流，等待 {wait_time}s 后重试 ({attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)
                    continue
                else:
                    # 其他错误直接返回
                    return result
                    
            except Exception as e:
                last_error = str(e)
                if '429' in last_error or 'Too Many Requests' in last_error:
                    wait_time = 10 * (attempt + 1)
                    print(f"[Grok Retry] 429限流，等待 {wait_time}s 后重试 ({attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)
                    continue
                else:
                    return {
                        "status": "error",
                        "error": {"message": last_error},
                        "provider": "grok"
                    }
        
        # 重试耗尽
        return {
            "status": "error",
            "error": {"message": f"Max retries ({max_retries}) exceeded. Last error: {last_error}"},
            "provider": "grok"
        }
    
    def _generate_video_internal(
        self,
        prompt: str,
        output_path: str,
        input_image: Optional[Union[str, Image.Image]] = None,
        duration: int = 5,
        resolution: str = "480p",
        aspect_ratio: str = "16:9"
    ) -> Dict:
        """内部视频生成方法（实际调用API）"""
        try:
            # 构建请求体
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "duration": duration,
                "resolution": resolution,
                "aspect_ratio": aspect_ratio
            }

            # 如果提供了图片，添加 image_url
            # 注意：grok-imagine-video 只支持 public URL，不支持 base64
            if input_image:
                if isinstance(input_image, str):
                    if input_image.startswith('http'):
                        # 已经是 URL，直接使用
                        payload["image"] = {"url": input_image}
                    elif Path(input_image).exists():
                        # 本地文件路径，先压缩再上传到 ImgBB 获取 URL
                        print(f"[Grok] 准备图片...")
                        
                        # 检查并压缩图片（如果太大）
                        image_path = input_image
                        image_size = Path(image_path).stat().st_size / 1024  # KB
                        
                        if image_size > 2000:  # 如果大于 2MB，进行压缩
                            print(f"[Grok] 图片较大 ({image_size:.1f} KB)，正在压缩...")
                            from PIL import Image as PILImage
                            import tempfile
                            
                            # 打开图片并压缩
                            with PILImage.open(image_path) as img:
                                # 转换为 RGB（去除透明通道）
                                if img.mode in ('RGBA', 'P'):
                                    img = img.convert('RGB')
                                
                                # 如果尺寸太大，先缩小
                                max_size = 1024
                                if max(img.size) > max_size:
                                    ratio = max_size / max(img.size)
                                    new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                                    img = img.resize(new_size, PILImage.Resampling.LANCZOS)
                                    print(f"[Grok] 图片已缩放至: {new_size}")
                                
                                # 保存为临时文件，质量 85%
                                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                                    tmp_path = tmp.name
                                img.save(tmp_path, 'JPEG', quality=85, optimize=True)
                                image_path = tmp_path
                                new_size = Path(tmp_path).stat().st_size / 1024
                                print(f"[Grok] 图片已压缩: {image_size:.1f} KB -> {new_size:.1f} KB")
                        
                        from utils.imgbb_uploader import upload_image
                        
                        # 重试3次
                        for attempt in range(3):
                            upload_result = upload_image(image_path, expiration=600)
                            if upload_result['status'] == 'success':
                                break
                            print(f"[Grok] 上传失败，重试 {attempt + 1}/3...")
                        
                        # 如果使用了临时压缩文件，删除它
                        if image_path != input_image and Path(image_path).exists():
                            Path(image_path).unlink()
                        
                        if upload_result['status'] != 'success':
                            return {
                                "status": "error",
                                "error": {"message": f"Failed to upload image: {upload_result.get('error', {}).get('message')}"},
                                "provider": "grok"
                            }
                        
                        payload["image"] = {"url": upload_result['url']}
                        print(f"[Grok] 图片URL: {upload_result['url']}")
                elif isinstance(input_image, Image.Image):
                    # PIL Image 对象，先保存再上传
                    import tempfile
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                        tmp_path = tmp.name
                    input_image.save(tmp_path)
                    
                    print(f"[Grok] 上传图片到图床...")
                    from utils.imgbb_uploader import upload_image
                    upload_result = upload_image(tmp_path, expiration=600)
                    
                    # 删除临时文件
                    Path(tmp_path).unlink()
                    
                    if upload_result['status'] != 'success':
                        return {
                            "status": "error",
                            "error": {"message": f"Failed to upload image: {upload_result.get('error', {}).get('message')}"},
                            "provider": "grok"
                        }
                    
                    payload["image"] = {"url": upload_result['url']}
                    print(f"[Grok] 图片URL: {upload_result['url']}")

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            # 第1步：提交生成请求
            url = f"{self.base_url}/videos/generations"
            print(f"[Grok] 提交视频生成请求...")
            print(f"[Grok] 参数: duration={duration}, resolution={resolution}, aspect_ratio={aspect_ratio}")
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()

            result = response.json()
            request_id = result.get("request_id")

            if not request_id:
                return {
                    "status": "error",
                    "error": {"message": "No request_id in response", "raw": result},
                    "provider": "grok"
                }

            # 第2步：轮询获取结果
            poll_result = self._poll_for_result(request_id, headers)

            if poll_result['status'] != 'success':
                return poll_result

            # 第3步：下载视频
            video_url = poll_result['video_url']
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            if self._download_video(video_url, output_path):
                return {
                    "status": "success",
                    "output_path": output_path,
                    "video_url": video_url,
                    "duration": poll_result.get('duration'),
                    "provider": "grok"
                }
            else:
                return {
                    "status": "error",
                    "error": {"message": "Failed to download video", "video_url": video_url},
                    "provider": "grok"
                }

        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "error": {"message": f"Request failed: {str(e)}"},
                "provider": "grok"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": {"message": str(e)},
                "provider": "grok"
            }

    def _poll_for_result(
        self,
        request_id: str,
        headers: Dict,
        poll_interval: int = 5,
        max_wait_time: int = 600
    ) -> Dict:
        """轮询获取视频生成结果"""
        url = f"{self.base_url}/videos/{request_id}"
        start_time = time.time()

        print(f"[Grok] 开始轮询，Request ID: {request_id}")

        while True:
            try:
                response = requests.get(url, headers=headers, timeout=60)
                response.raise_for_status()

                data = response.json()
                status = data.get("status")

                if status == "done":
                    video_data = data.get("video", {})
                    print(f"[Grok] 视频生成完成！")
                    return {
                        "status": "success",
                        "video_url": video_data.get("url"),
                        "duration": video_data.get("duration"),
                        "respect_moderation": video_data.get("respect_moderation"),
                        "request_id": request_id,
                        "model": data.get("model")
                    }

                elif status == "expired":
                    return {
                        "status": "error",
                        "error": {"message": "Video generation request expired", "request_id": request_id}
                    }

                elif status == "failed":
                    print(f"[Grok] 视频生成失败!")
                    print(f"[Grok] 错误详情: {json.dumps(data, indent=2, ensure_ascii=False)}")
                    # 尝试提取更详细的错误信息
                    error_msg = "Video generation failed"
                    if "error" in data:
                        error_msg = data["error"].get("message", error_msg)
                    elif "message" in data:
                        error_msg = data["message"]
                    return {
                        "status": "error",
                        "error": {"message": error_msg, "request_id": request_id, "raw": data}
                    }

                elif status == "pending":
                    elapsed = time.time() - start_time
                    if elapsed > max_wait_time:
                        return {
                            "status": "error",
                            "error": {"message": f"Timeout after {max_wait_time}s", "request_id": request_id}
                        }

                    print(f"[Grok] 生成中... ({int(elapsed)}s)")
                    time.sleep(poll_interval)
                    continue

                else:
                    return {
                        "status": "error",
                        "error": {"message": f"Unknown status: {status}", "raw": data}
                    }

            except requests.exceptions.ConnectionError as e:
                # 连接被重置，等待后重试
                elapsed = time.time() - start_time
                if elapsed > max_wait_time:
                    return {"status": "error", "error": {"message": f"Connection lost and timeout after {max_wait_time}s"}}
                print(f"[Grok] 连接中断，等待重试...")
                time.sleep(poll_interval)
                continue
            except requests.exceptions.RequestException as e:
                return {"status": "error", "error": {"message": f"Polling failed: {str(e)}"}}
            except Exception as e:
                return {"status": "error", "error": {"message": str(e)}}

    def _download_video(self, video_url: str, output_path: str, max_retries: int = 3) -> bool:
        """下载视频到本地，支持重试"""
        for attempt in range(max_retries):
            try:
                print(f"[Grok] 下载视频... (尝试 {attempt + 1}/{max_retries})")
                
                # 使用更保守的参数，避免连接中断
                response = requests.get(
                    video_url, 
                    stream=True, 
                    timeout=(30, 300),  # (连接超时, 读取超时)
                    headers={
                        'Accept': '*/*',
                        'Accept-Encoding': 'identity',  # 禁用压缩，避免解码问题
                    }
                )
                response.raise_for_status()

                # 获取文件大小
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=65536):  # 增大块大小
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            # 每下载 500KB 打印进度
                            if total_size > 0 and downloaded % (500 * 1024) < 65536:
                                progress = (downloaded / total_size) * 100
                                print(f"[Grok] 下载进度: {progress:.1f}% ({downloaded}/{total_size} bytes)")
                
                # 验证文件大小
                saved_size = Path(output_path).stat().st_size
                if total_size > 0 and saved_size < total_size * 0.9:  # 允许 10% 误差
                    print(f"[Grok] 警告: 文件不完整 ({saved_size}/{total_size} bytes)")
                    if attempt < max_retries - 1:
                        print(f"[Grok] 等待 5 秒后重试...")
                        time.sleep(5)
                        continue
                
                print(f"[Grok] 视频已保存: {output_path} ({saved_size} bytes)")
                return True
                
            except requests.exceptions.ChunkedEncodingError as e:
                print(f"[Grok] 下载中断 (ChunkedEncodingError): {e}")
                if attempt < max_retries - 1:
                    print(f"[Grok] 等待 5 秒后重试...")
                    time.sleep(5)
                    continue
            except requests.exceptions.ConnectionError as e:
                print(f"[Grok] 连接错误: {e}")
                if attempt < max_retries - 1:
                    print(f"[Grok] 等待 5 秒后重试...")
                    time.sleep(5)
                    continue
            except Exception as e:
                print(f"[Grok] 下载失败: {e}")
                if attempt < max_retries - 1:
                    print(f"[Grok] 等待 5 秒后重试...")
                    time.sleep(5)
                    continue
        
        print(f"[Grok] 下载失败，已重试 {max_retries} 次")
        return False


if __name__ == "__main__":
    provider = GrokVideoProvider()
    print(f"Model: {provider.model_name}")