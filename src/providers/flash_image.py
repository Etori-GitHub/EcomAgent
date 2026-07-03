"""Flash Image Provider - Google Gemini (HTTP API 直接调用，绕过 SDK SSL 问题)"""
import json
import time
import sys
import urllib.request
import ssl
import base64
from pathlib import Path
from typing import Dict, List, Optional, Union
from PIL import Image
from .base import ImageProvider

# 强制禁用 stdout 缓冲
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)


class FlashImageProvider(ImageProvider):
    """Google Flash Image Provider - 使用 HTTP API 直接调用"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config"
        
        # 加载 API Key
        keys_file = config_path / "api_keys.json"
        with open(keys_file, 'r', encoding='utf-8') as f:
            keys = json.load(f)
        
        # 加载模型配置
        models_file = config_path / "models.json"
        with open(models_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        self.api_key = keys['google']
        self.model_name = config['image_providers']['flash_image']['model']
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"
    
    def _encode_image(self, image_path: str) -> tuple:
        """将图片编码为 base64，返回 (data, mime_type)"""
        with open(image_path, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
        
        # 判断图片类型
        img = Image.open(image_path)
        mime_type = f"image/{img.format.lower()}" if img.format else "image/jpeg"
        return data, mime_type
    
    def generate_image(
        self,
        prompt: str,
        output_path: str,
        aspect_ratio: str = "1:1",
        resolution: str = "2K",
        input_image: Optional[Union[str, Image.Image]] = None,
        max_retries: int = 10
    ) -> Dict:
        """生成单张图片，带指数退避重试机制"""
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # 指数退避: 15s -> 30s -> 60s -> 120s（最大）
                if attempt > 0:
                    wait_time = min(15 * (2 ** attempt), 120)
                    print(f"  [FlashImage Retry] Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                
                print(f"  [FlashImage] Attempt {attempt + 1}/{max_retries}...")
                sys.stdout.flush()
                
                # 构建请求体
                parts = [{"text": prompt}]
                
                if input_image:
                    if isinstance(input_image, str):
                        image_data, mime_type = self._encode_image(input_image)
                        # 压缩图片到 100KB 以下
                        original_size = len(image_data)
                        print(f"  [FlashImage] Original image size: {original_size / 1024:.1f} KB")
                        
                        if original_size > 100 * 1024:  # > 100KB
                            print(f"  [FlashImage] Compressing image...")
                            img = Image.open(input_image)
                            # 缩放到最大 1024px
                            max_size = 1024
                            if max(img.size) > max_size:
                                ratio = max_size / max(img.size)
                                new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                                img = img.resize(new_size, Image.Resampling.LANCZOS)
                            # 保存为 JPEG，质量 85
                            import io
                            buffer = io.BytesIO()
                            img = img.convert('RGB')
                            img.save(buffer, format='JPEG', quality=85)
                            image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
                            mime_type = 'image/jpeg'
                            print(f"  [FlashImage] Compressed to: {len(image_data) / 1024:.1f} KB")
                        
                        parts.append({
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": image_data
                            }
                        })
                    elif isinstance(input_image, Image.Image):
                        # PIL Image 对象，转为 base64
                        import io
                        buffer = io.BytesIO()
                        input_image.save(buffer, format='PNG')
                        image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
                        parts.append({
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": image_data
                            }
                        })
                
                data = {
                    "contents": [{"parts": parts}],
                    "generationConfig": {
                        "response_modalities": ["TEXT", "IMAGE"]
                    }
                }
                
                # 添加图片配置（仅在没有输入图片时）
                # 注意：有输入图片时，imageConfig 可能导致 Bad Request
                if not input_image:
                    if aspect_ratio or resolution:
                        image_config = {}
                        if aspect_ratio:
                            image_config["aspectRatio"] = aspect_ratio
                        if resolution:
                            image_config["outputOptions"] = {"mimeType": "image/png"}
                        if image_config:
                            data["generationConfig"]["imageConfig"] = image_config
                        print(f"  [FlashImage] Config: aspect_ratio={aspect_ratio}, resolution={resolution}")
                else:
                    print(f"  [FlashImage] Input image provided, aspect_ratio controlled by prompt")
                
                # SSL 配置 - 从配置文件读取
                ssl_verify = False
                try:
                    settings_file = Path(__file__).parent.parent.parent / "config" / "settings.json"
                    if settings_file.exists():
                        with open(settings_file, 'r', encoding='utf-8') as f:
                            settings = json.load(f)
                            ssl_verify = settings.get('ssl_verify', False)
                            print(f"  [FlashImage] SSL verify from config: {ssl_verify}")
                except Exception as e:
                    print(f"  [FlashImage] Failed to read ssl_verify: {e}")
                
                if ssl_verify:
                    ctx = ssl.create_default_context()
                else:
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                
                # 配置代理（从配置文件读取）
                proxy_url = None
                try:
                    settings_file = Path(__file__).parent.parent.parent / "config" / "settings.json"
                    if settings_file.exists():
                        with open(settings_file, 'r', encoding='utf-8') as f:
                            settings = json.load(f)
                            proxy_config = settings.get('proxy', {})
                            if proxy_config.get('enabled', True):
                                host = proxy_config.get('host', '127.0.0.1')
                                port = proxy_config.get('port', 7890)
                                proxy_url = f"http://{host}:{port}"
                                print(f"  [FlashImage] Proxy from config: {proxy_url}")
                except Exception as e:
                    print(f"  [FlashImage] Failed to read proxy config: {e}")
                
                if not proxy_url:
                    proxy_url = 'http://127.0.0.1:7897'
                
                print(f"  [FlashImage] Using proxy: {proxy_url}")
                
                # 使用代理处理器
                proxy_handler = urllib.request.ProxyHandler({
                    'http': proxy_url,
                    'https': proxy_url
                })
                opener = urllib.request.build_opener(proxy_handler, urllib.request.HTTPSHandler(context=ctx))
                
                req = urllib.request.Request(
                    f"{self.api_url}?key={self.api_key}",
                    data=json.dumps(data).encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                
                request_size_kb = len(json.dumps(data).encode('utf-8')) / 1024
                print(f"  [FlashImage] Request size: {request_size_kb:.1f} KB, timeout: 180s")
                
                response = opener.open(req, timeout=180)
                result = json.loads(response.read().decode('utf-8'))
                
                # 检查 API 错误
                if 'error' in result:
                    error_msg = result['error'].get('message', str(result['error']))
                    last_error = error_msg
                    print(f"  [FlashImage Retry] Attempt {attempt + 1}/{max_retries} failed: {error_msg}")
                    continue
                
                # 解析响应
                candidates = result.get('candidates', [])
                if not candidates:
                    last_error = "No candidates in response"
                    print(f"  [FlashImage] No candidates in response")
                    print(f"  [FlashImage] Response: {json.dumps(result, indent=2)[:500]}")
                    continue
                
                parts = candidates[0].get('content', {}).get('parts', [])
                print(f"  [FlashImage] Got {len(parts)} parts in response")
                
                for part in parts:
                    print(f"  [FlashImage] Part keys: {list(part.keys())}")
                    # 检查是否有图片数据（注意：API 返回的是 inlineData，不是 inline_data）
                    image_data_key = None
                    if 'inlineData' in part:
                        image_data_key = 'inlineData'
                    elif 'inline_data' in part:
                        image_data_key = 'inline_data'
                    
                    if image_data_key:
                        img_data = base64.b64decode(part[image_data_key]['data'])
                        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                        with open(output_path, 'wb') as f:
                            f.write(img_data)
                        print(f"  [FlashImage] Success! Image saved to {output_path}")
                        return {
                            "status": "success",
                            "output_path": output_path,
                            "provider": "flash_image"
                        }
                
                # 没有图片数据
                text_parts = [p.get('text', '') for p in parts if 'text' in p]
                if text_parts:
                    last_error = f"API returned text instead of image: {text_parts[0][:200]}"
                else:
                    last_error = "No image generated in response"
                print(f"  [FlashImage] No image in response")
                    
            except urllib.error.URLError as e:
                last_error = f"网络错误: {e.reason}"
                print(f"  [FlashImage Retry] Attempt {attempt + 1}/{max_retries} failed: {last_error}")
                print(f"  [FlashImage Retry] Full error: {str(e)}")
                print(f"  [FlashImage Retry] URL: {self.api_url}")
                print(f"  [FlashImage Retry] Proxy: {proxy_url}")
            except Exception as e:
                last_error = str(e)
                print(f"  [FlashImage Retry] Attempt {attempt + 1}/{max_retries} failed: {last_error}")
                print(f"  [FlashImage Retry] Exception type: {type(e).__name__}")
                import traceback
                traceback.print_exc()
        
        # 所有重试都失败
        print(f"  [FlashImage] All {max_retries} attempts failed")
        return {
            "status": "error",
            "error": {"message": f"All {max_retries} attempts failed. Last error: {last_error}"},
            "provider": "flash_image"
        }
    
    def generate_batch(
        self,
        prompts: List[str],
        output_dir: str,
        aspect_ratio: str = "1:1",
        resolution: str = "2K",
        input_image: Optional[Union[str, Image.Image]] = None
    ) -> List[Dict]:
        """批量生成图片"""
        results = []
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for i, prompt in enumerate(prompts):
            output_path = str(output_dir / f"{i:02d}_marketing.png")
            result = self.generate_image(prompt, output_path, aspect_ratio, resolution, input_image)
            result['index'] = i
            result['prompt'] = prompt
            results.append(result)
            time.sleep(0.5)
        
        return results


if __name__ == "__main__":
    # 测试
    provider = FlashImageProvider()
    result = provider.generate_image(
        "A white wireless headphone on white background, professional photo",
        "test_output.png"
    )
    print(result)
