"""Gemini Prompt Provider - 生成图片提示词"""
import json
import base64
from pathlib import Path
from typing import Dict, List
from PIL import Image
from google import genai
from google.genai import types


class GeminiPromptProvider:
    """使用 Gemini 分析图片并生成提示词"""
    
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
        
        # 配置 Gemini (使用新的 google.genai)
        self.client = genai.Client(api_key=self.api_key)
    
    def generate_image_prompts(
        self,
        image_path: str,
        count: int = 9,
        language: str = "english"
    ) -> Dict:
        """
        分析产品图片，生成营销场景提示词
        
        Args:
            image_path: 产品图片路径
            count: 生成提示词数量
            language: 输出语言 (english/chinese)
        
        Returns:
            {
                "status": "success|error",
                "prompts": [str],
                "scenes": [str]
            }
        """
        try:
            # 读取图片
            image = Image.open(image_path)
            
            # 构建提示词
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
   - Do NOT change the product's form factor or structural details
   - Do NOT simplify or stylize the product appearance
   - The product should look like the exact same item, just in a different scene/lighting

4. {lang_instruction} for AI image generation
5. Each description should be 1-2 sentences, specific and vivid

Return ONLY a JSON object in this format:
{{"prompts": ["description 1", "description 2", ...], "scenes": ["scene name 1", "scene name 2", ...]}}"""

            # 调用 Gemini (使用新的 google.genai API)
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt_text, image],
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=4096
                )
            )
            
            # 解析响应
            content = response.text.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            data = json.loads(content)
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
                "error": {"message": str(e)},
                "prompts": []
            }


    def generate_video_prompt_with_scale(
        self,
        image_path: str,
        scene_description: str = None
    ) -> Dict:
        """
        分析产品图片，生成包含比例约束的视频提示词
        
        Args:
            image_path: 产品图片路径
            scene_description: 可选的场景描述（用于V2的3套场景）
        
        Returns:
            {
                "status": "success|error",
                "video_prompt": str,
                "scale_reference": str
            }
        """
        try:
            # 读取图片
            image = Image.open(image_path)
            
            # 构建提示词
            scene_context = f"\nScene context: {scene_description}" if scene_description else ""
            
            prompt_text = f"""Analyze this product image and generate a video generation prompt with CRITICAL proportion constraints.

Your task:
1. Identify the product type and its realistic size category (small handheld item / medium portable item / large wearable or carry item)
2. Determine the appropriate scale reference relative to human hands, body, or common objects
3. Generate a video prompt that includes strict proportion rules{scene_context}

The video prompt MUST include these CRITICAL PROPORTION RULES:

CRITICAL PROPORTION CONSTRAINTS:
- Maintain the exact size relationship between product and any human elements (hands, fingers, body parts)
- Product scale must match real-world expectations - analyze the image to determine if this is a small/medium/large item
- If hands appear in the video, they must be anatomically correct relative to product size
- No miniaturization or enlargement of the main subject beyond realistic proportions
- Background elements must maintain realistic scale hierarchy with the product
- The product should appear at its true-to-life size, not toy-sized or oversized

DYNAMIC SCALE REFERENCE (analyze the image and fill in):
- Product category: [identify type]
- Size classification: [small/medium/large relative to human hand/body]
- Scale anchor: [e.g., "fits comfortably in one hand", "requires two hands to hold", "worn on the body", etc.]
- Realistic proportion note: [specific constraint for this product type]

PROHIBITED DISTORTIONS:
NEVER make product appear toy-sized when it's a real adult product
NEVER shrink human hands to make product look larger
NEVER enlarge product beyond realistic human scale
NEVER distort the natural size hierarchy of scene elements
NEVER create "chibi" or cartoonish oversized proportions

Return ONLY a JSON object in this format:
{{"video_prompt": "complete video generation prompt with all constraints integrated", "scale_reference": "one sentence describing the realistic scale of this product"}}"""

            # 调用 Gemini
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt_text, image],
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=4096
                )
            )
            
            # 解析响应
            content = response.text.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            data = json.loads(content)
            video_prompt = data.get('video_prompt', '')
            scale_reference = data.get('scale_reference', '')
            
            return {
                "status": "success",
                "video_prompt": video_prompt,
                "scale_reference": scale_reference
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": {"message": str(e)},
                "video_prompt": "",
                "scale_reference": ""
            }

    def generate_ad_script(
        self,
        image_path: str,
        language: str = "chinese"
    ) -> Dict:
        """
        分析产品图片，生成15秒广告词并分割成3段
        
        Args:
            image_path: 产品图片路径
            language: 语言 (chinese/english)
        
        Returns:
            {
                "status": "success|error",
                "full_script": str,  # 完整15秒广告词
                "segments": [str, str, str],  # 3个5秒段落
                "duration_per_segment": 5
            }
        """
        try:
            # 读取图片
            image = Image.open(image_path)
            
            # 构建提示词
            lang_instruction = "用中文撰写" if language == "chinese" else "Write in English"
            duration_guide = "每段约15-20个汉字，朗读时长约5秒" if language == "chinese" else "Each segment about 25-30 words, reading time ~5 seconds"
            
            prompt_text = f"""Analyze this product image and create a 15-second advertisement script.

Requirements:
1. Create an engaging, persuasive advertisement script for this product
2. Total length: approximately 15 seconds when read aloud
3. Split into 3 segments, each approximately 5 seconds
4. {duration_guide}
5. Each segment should flow naturally and build upon the previous one:
   - Segment 1: Hook/Attention grabber + product introduction
   - Segment 2: Key benefits/features + why it's special
   - Segment 3: Call to action + memorable closing
6. {lang_instruction}
7. Make it sound natural when spoken, not too formal or salesy
8. Include specific product details visible in the image

Return ONLY a JSON object in this format:
{{"full_script": "complete 15-second script", "segments": ["segment 1 (~5s)", "segment 2 (~5s)", "segment 3 (~5s)"]}}"""

            # 调用 Gemini
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt_text, image],
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    max_output_tokens=1024
                )
            )
            
            # 解析响应
            content = response.text.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            data = json.loads(content)
            full_script = data.get('full_script', '')
            segments = data.get('segments', [])
            
            # 确保有3段
            while len(segments) < 3:
                segments.append("")
            
            return {
                "status": "success",
                "full_script": full_script,
                "segments": segments[:3],
                "duration_per_segment": 5
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": {"message": str(e)},
                "full_script": "",
                "segments": ["", "", ""],
                "duration_per_segment": 5
            }

    def generate_model_frame(
        self,
        image_path: str,
        language: str = "english"
    ) -> Dict:
        """
        分析产品图片，生成高质量首帧模特图提示词
        
        Args:
            image_path: 产品图片路径
            language: 输出语言 (english/chinese)
        
        Returns:
            {
                "status": "success|error",
                "prompt": str  # 首帧模特图提示词
            }
        """
        try:
            # 读取图片
            image = Image.open(image_path)
            
            # 构建提示词
            lang_instruction = "Write in English" if language == "english" else "用中文撰写"
            
            prompt_text = f"""Analyze this product image and generate a prompt for creating a high-quality model frame image featuring a European model.

Requirements:
1. The prompt should describe a professional e-commerce product photography scene
2. The scene should feature a European model (male or female) presenting the product
3. Include details about: model pose, lighting, background, composition, atmosphere
4. The product should be the clear focal point, held or presented by the model
5. Premium advertising aesthetic with world-class photography quality
6. Fixed 9:16 vertical aspect ratio composition optimized for mobile viewing
7. Clean, uncluttered composition with sophisticated depth of field
8. Professional color grading with cinematic tonal balance
9. {lang_instruction} for AI image generation

Return ONLY a JSON object in this format:
{{"prompt": "complete prompt for AI image generation"}}"""

            # 调用 Gemini (使用新的 google.genai API)
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt_text, image],
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=4096
                )
            )
            
            # 解析响应
            content = response.text.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            data = json.loads(content)
            prompt = data.get('prompt', '')
            
            return {
                "status": "success",
                "prompt": prompt
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": {"message": str(e)},
                "prompt": ""
            }


if __name__ == "__main__":
    # 测试
    provider = GeminiPromptProvider()
    # 需要测试图片路径
    # result = provider.generate_image_prompts("test_image.jpg")
    # print(json.dumps(result, ensure_ascii=False, indent=2))
