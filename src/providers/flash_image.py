"""Flash Image Provider - Google Gemini"""
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Union
from PIL import Image
from google import genai
from google.genai import types
from .base import ImageProvider


class FlashImageProvider(ImageProvider):
    """Google Flash Image Provider"""
    
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
        self.client = genai.Client(api_key=self.api_key)
    
    def generate_image(
        self,
        prompt: str,
        output_path: str,
        aspect_ratio: str = "1:1",
        resolution: str = "2K",
        input_image: Optional[Union[str, Image.Image]] = None,
        max_retries: int = 5
    ) -> Dict:
        """生成单张图片，带重试机制 - VPN不稳定，增加冗余"""
        last_error = None
        
        for attempt in range(max_retries):
            try:
                contents = [prompt]
                if input_image:
                    if isinstance(input_image, str):
                        input_image = Image.open(input_image)
                    contents.append(input_image)
                
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_modalities=['TEXT', 'IMAGE'],
                        image_config=types.ImageConfig(
                            aspect_ratio=aspect_ratio,
                            image_size=resolution
                        ),
                    )
                )
                
                for part in response.parts:
                    if image := part.as_image():
                        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                        image.save(output_path)
                        return {
                            "status": "success",
                            "output_path": output_path,
                            "provider": "flash_image"
                        }
                
                return {"status": "error", "error": {"message": "No image generated"}}
                    
            except Exception as e:
                last_error = str(e)
                error_msg = f"Attempt {attempt + 1}/{max_retries} failed: {last_error}"
                print(f"  [FlashImage Retry] {error_msg}")
                
                if attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)
                    print(f"  [FlashImage Retry] Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
        
        # 所有重试都失败
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
