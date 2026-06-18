# -*- coding: utf-8 -*-
"""Gemini Prompt Provider - 使用 HTTP API 直接调用（绕过 SDK SSL 问题）"""

import json
import base64
import urllib.request
import ssl
import time
import sys
from pathlib import Path
from typing import Dict, List
from PIL import Image

# 强制禁用 stdout 缓冲
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)


class GeminiPromptProviderHTTP:
    """使用 HTTP API 直接调用 Gemini"""
    
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
        
        self.api_key = keys['google']
        self.model_name = config['gemini']['model']
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"
    
    def _call_api(self, image_path: str, prompt_text: str, max_retries: int = 5) -> Dict:
        """调用 Gemini API - 带指数退避重试"""
        
        # 读取图片并转 base64
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # 判断图片类型
        img = Image.open(image_path)
        mime_type = f"image/{img.format.lower()}" if img.format else "image/jpeg"
        
        # 构建请求
        data = {
            "contents": [{
                "parts": [
                    {"text": prompt_text},
                    {"inline_data": {"mime_type": mime_type, "data": image_data}}
                ]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 4096
            }
        }
        
        # SSL 配置
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        last_error = None
        for attempt in range(max_retries):
            try:
                # 指数退避: 2s -> 4s -> 8s -> 16s -> 32s
                if attempt > 0:
                    wait_time = 2 ** attempt
                    print(f"[GeminiHTTP] 等待 {wait_time}s 后重试...")
                    time.sleep(wait_time)
                
                print(f"[GeminiHTTP] 第 {attempt+1}/{max_retries} 次尝试...")
                
                req = urllib.request.Request(
                    f"{self.api_url}?key={self.api_key}",
                    data=json.dumps(data).encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                
                response = urllib.request.urlopen(req, timeout=90, context=ctx)
                result = json.loads(response.read().decode('utf-8'))
                
                # 检查 API 错误
                if 'error' in result:
                    error_msg = result['error'].get('message', str(result['error']))
                    print(f"[GeminiHTTP] API 返回错误: {error_msg}")
                    last_error = error_msg
                    continue
                
                print(f"[GeminiHTTP] API 调用成功!")
                return {"status": "success", "result": result}
                
            except urllib.error.URLError as e:
                last_error = f"网络错误: {e.reason}"
                print(f"[GeminiHTTP] 第 {attempt+1} 次失败 (网络): {e.reason}")
            except Exception as e:
                last_error = str(e)
                print(f"[GeminiHTTP] 第 {attempt+1} 次失败: {e}")
        
        print(f"[GeminiHTTP] 所有重试失败: {last_error}")
        return {"status": "error", "error": last_error or "Unknown error"}
    
    def generate_image_prompts(
        self,
        image_path: str,
        count: int = 9,
        language: str = "english"
    ) -> Dict:
        """分析产品图片，生成营销场景提示词"""
        
        lang_instruction = "Write in English" if language == "english" else "用中文撰写"
        
        prompt_text = f"""Analyze this product image and generate {count} different marketing image descriptions.

Requirements:
1. Each description should be detailed, including scene, lighting, angle, atmosphere
2. Cover these marketing scenarios:
   - Main product shot (white background, professional)
   - Lifestyle scene (real usage context)
   - Detail close-up (texture, material)
   - Feature highlight (key selling points)
   - Comparison/before-after
   - Specifications display
   - Bundle/set showcase
   - Real photo/unfiltered
   - Trust/guarantee elements

3. CRITICAL - PRODUCT FIDELITY CONSTRAINTS:
   - The product in the generated image MUST be IDENTICAL to the reference image
   - Maintain exact same shape, proportions, dimensions, and silhouette
   - Preserve all visible details: colors, textures, materials, logos, text, patterns
   - Keep the same number of components/parts and their arrangement
   - Do NOT add, remove, or alter any design elements

4. {lang_instruction} for AI image generation
5. Each description should be 1-2 sentences, specific and vivid

Return ONLY a JSON object in this format:
{{"prompts": ["description 1", "description 2", ...], "scenes": ["scene name 1", "scene name 2", ...]}}"""
        
        result = self._call_api(image_path, prompt_text)
        
        if result["status"] == "error":
            return {
                "status": "error",
                "error": {"message": result["error"]},
                "prompts": []
            }
        
        # 解析响应
        try:
            content = result["result"]["candidates"][0]["content"]["parts"][0]["text"]
            content = content.strip()
            
            # 去掉 markdown 代码块
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            # 尝试找到 JSON 对象
            start_idx = content.find('{')
            end_idx = content.rfind('}')
            if start_idx >= 0 and end_idx > start_idx:
                json_str = content[start_idx:end_idx+1]
            else:
                json_str = content
            
            data = json.loads(json_str)
            prompts = data.get('prompts', [])
            scenes = data.get('scenes', [])
            
            # 确保数量
            while len(prompts) < count:
                prompts.append("Professional product photography, studio lighting")
            while len(scenes) < count:
                scenes.append(f"Scene {len(scenes)+1}")
            
            return {
                "status": "success",
                "prompts": prompts[:count],
                "scenes": scenes[:count]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": {"message": f"解析响应失败: {e}"},
                "prompts": []
            }
    
    def generate_video_prompt_with_scale(
        self,
        image_path: str,
        scene_description: str = None
    ) -> Dict:
        """生成视频提示词"""
        
        scene_context = f"\nScene context: {scene_description}" if scene_description else ""
        
        prompt_text = f"""Analyze this product image and create a video prompt for AI video generation.

{scene_context}

Requirements:
1. Create a short video scene description (10-15 seconds)
2. Include camera movement, lighting, and product interaction
3. The product MUST remain exactly the same appearance

Return ONLY a JSON:
{{"video_prompt": "...", "scale_reference": "..."}}"""
        
        result = self._call_api(image_path, prompt_text)
        
        if result["status"] == "error":
            return {
                "status": "error",
                "error": {"message": result["error"]}
            }
        
        try:
            content = result["result"]["candidates"][0]["content"]["parts"][0]["text"]
            content = content.strip()
            
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            
            data = json.loads(content.strip())
            
            return {
                "status": "success",
                "video_prompt": data.get("video_prompt", ""),
                "scale_reference": data.get("scale_reference", "")
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": {"message": f"解析响应失败: {e}"}
            }

    def generate_model_frame(self, image_path: str, language: str = "english") -> Dict:
        """分析产品图片，生成高质量首帧模特图提示词"""
        
        lang_instruction = "Write in English" if language == "english" else "用中文撰写"
        
        prompt_text = f"""Analyze this product image and generate a prompt for creating a high-quality model frame image featuring a European model.

Requirements:
1. The prompt should describe a professional e-commerce product photography scene
2. The scene should feature a European model (male or female) presenting the product
3. Include details about: model pose, lighting, background, composition, atmosphere
4. The product MUST remain exactly the same - same shape, color, size, texture, details
5. {lang_instruction}

Return ONLY a JSON:
{{"prompt": "..."}}"""
        
        result = self._call_api(image_path, prompt_text)
        
        if result["status"] == "error":
            return {
                "status": "error",
                "error": {"message": result["error"]}
            }
        
        
        try:
            content = result["result"]["candidates"][0]["content"]["parts"][0]["text"]
            content = content.strip()
            
            # 去掉 markdown 代码块
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            # 尝试找到 JSON 对象
            start_idx = content.find('{')
            end_idx = content.rfind('}')
            if start_idx >= 0 and end_idx > start_idx:
                json_str = content[start_idx:end_idx+1]
            else:
                json_str = content
            
            data = json.loads(json_str)
            
            prompt = data.get("prompt", "")
            if not prompt:
                return {
                    "status": "error",
                    "error": {"message": "未找到有效的提示词"}
                }
            
            return {
                "status": "success",
                "prompt": prompt
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": {"message": f"解析响应失败: {e}"}
            }