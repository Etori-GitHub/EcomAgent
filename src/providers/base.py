"""Provider 基础接口"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union
from PIL import Image


class ImageProvider(ABC):
    """图像生成 Provider 基类"""
    
    @abstractmethod
    def generate_image(
        self,
        prompt: str,
        output_path: str,
        aspect_ratio: str = "1:1",
        resolution: str = "2K",
        input_image: Optional[Union[str, Image.Image]] = None
    ) -> Dict:
        """生成单张图片"""
        pass
    
    @abstractmethod
    def generate_batch(
        self,
        prompts: List[str],
        output_dir: str,
        aspect_ratio: str = "1:1",
        resolution: str = "2K"
    ) -> List[Dict]:
        """批量生成图片"""
        pass


class VideoProvider(ABC):
    """视频生成 Provider 基类"""
    
    @abstractmethod
    def generate_video(
        self,
        prompt: str,
        output_path: str,
        input_image: Optional[Union[str, Image.Image]] = None,
        duration: int = 5,
        resolution: str = "720p"
    ) -> Dict:
        """
        生成视频
        
        Args:
            prompt: 视频提示词
            output_path: 输出路径
            input_image: 输入图片（图生视频）
            duration: 视频时长（秒）
            resolution: 分辨率
        
        Returns:
            {
                "status": "success|error",
                "output_path": str,
                "provider": str,
                "error": {"message": str}
            }
        """
        pass
