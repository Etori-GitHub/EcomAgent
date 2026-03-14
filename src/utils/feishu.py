"""飞书消息发送工具"""
import subprocess
from pathlib import Path
from typing import Optional, List


class FeishuMessenger:
    """飞书消息发送器"""
    
    def __init__(self):
        pass
    
    def send_text(self, user_id: str, message: str) -> bool:
        """
        发送文本消息
        
        Args:
            user_id: 飞书用户ID (如: ou_xxx)
            message: 消息内容
        
        Returns:
            bool: 是否发送成功
        """
        try:
            escaped_message = message.replace('"', '\\"')
            cmd = f'openclaw message send --channel feishu --target "{user_id}" --message "{escaped_message}"'
            print(f"[FeishuMessenger] 执行命令: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            print(f"[FeishuMessenger] 返回码: {result.returncode}")
            print(f"[FeishuMessenger] stdout: {result.stdout}")
            print(f"[FeishuMessenger] stderr: {result.stderr}")
            return result.returncode == 0
        except Exception as e:
            print(f"[FeishuMessenger] 发送文本失败: {e}")
            return False
    
    def send_image(self, user_id: str, image_path: str, caption: str = "") -> bool:
        """
        发送图片消息
        
        Args:
            user_id: 飞书用户ID
            image_path: 图片文件路径
            caption: 图片说明文字
        
        Returns:
            bool: 是否发送成功
        """
        try:
            if not Path(image_path).exists():
                print(f"[FeishuMessenger] 图片不存在: {image_path}")
                return False
            
            cmd = f'openclaw message send --channel feishu --target "{user_id}" --media "{image_path}"'
            if caption:
                escaped_caption = caption.replace('"', '\\"')
                cmd += f' --message "{escaped_caption}"'
            
            print(f"[FeishuMessenger] 执行命令: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            print(f"[FeishuMessenger] 返回码: {result.returncode}")
            print(f"[FeishuMessenger] stdout: {result.stdout}")
            print(f"[FeishuMessenger] stderr: {result.stderr}")
            return result.returncode == 0
        except Exception as e:
            print(f"[FeishuMessenger] 发送图片失败: {e}")
            return False
    
    def send_images_batch(
        self,
        user_id: str,
        image_paths: List[str],
        caption: str = "",
        progress_callback = None
    ) -> dict:
        """
        批量发送多张图片
        
        Args:
            user_id: 飞书用户ID
            image_paths: 图片路径列表
            caption: 批量发送前的说明文字
            progress_callback: 进度回调函数 (current, total)
        
        Returns:
            {"success": int, "failed": int}
        """
        results = {"success": 0, "failed": 0}
        
        if caption:
            self.send_text(user_id, caption)
        
        for i, path in enumerate(image_paths, 1):
            if progress_callback:
                progress_callback(i, len(image_paths))
            
            print(f"[{i}/{len(image_paths)}] 发送: {path}")
            
            if self.send_image(user_id, path):
                results["success"] += 1
            else:
                results["failed"] += 1
        
        return results
    
    def send_generation_result(
        self,
        user_id: str,
        result: dict,
        send_images: bool = True
    ) -> bool:
        """
        发送生图结果给用户
        
        Args:
            user_id: 飞书用户ID
            result: generate_images 返回的结果字典
            send_images: 是否发送图片文件
        
        Returns:
            bool: 是否发送成功
        """
        try:
            # 发送汇总信息
            total = result.get('total', 0)
            success_count = result.get('success_count', 0)
            
            summary = f"生成完成！共生成 {success_count}/{total} 张图片"
            self.send_text(user_id, summary)
            
            if not send_images:
                return True
            
            # 逐张发送图片
            images = result.get('images', [])
            for img_info in images:
                if img_info['status'] == 'success':
                    scene = img_info.get('scene', f"图片 {img_info['index']}")
                    output_path = img_info.get('output_path')
                    
                    if output_path and Path(output_path).exists():
                        caption = f"[{img_info['index']+1}/{total}] {scene}"
                        self.send_image(user_id, output_path, caption)
            
            return True
            
        except Exception as e:
            print(f"[FeishuMessenger] 发送结果失败: {e}")
            return False


# 便捷函数
def send_text(user_id: str, message: str) -> bool:
    """发送文本消息"""
    return FeishuMessenger().send_text(user_id, message)


def send_image(user_id: str, image_path: str, caption: str = "") -> bool:
    """发送图片消息"""
    return FeishuMessenger().send_image(user_id, image_path, caption)


def send_generation_result(user_id: str, result: dict) -> bool:
    """发送生图结果"""
    return FeishuMessenger().send_generation_result(user_id, result)
