# -*- coding: utf-8 -*-
"""任务队列管理 - 使用内存队列（简化版，无需 Redis）

对于单机部署，使用内存队列足够，避免 Redis 依赖。
如果未来需要多实例部署，可以切换到 RQ + Redis。
"""

import uuid
import threading
import subprocess
import sys
import json
import shutil
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Callable
from queue import Queue
from enum import Enum

# 项目路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = DATA_DIR / "assets"


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class TaskQueue:
    """内存任务队列"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._tasks: Dict[str, dict] = {}
                    cls._instance._queue = Queue()
                    cls._instance._worker_thread = None
                    cls._instance._start_worker()
        return cls._instance
    
    def _start_worker(self):
        """启动工作线程"""
        self._worker_thread = threading.Thread(target=self._worker, daemon=True)
        self._worker_thread.start()
    
    def _worker(self):
        """工作线程，处理队列中的任务"""
        while True:
            try:
                task_func, task_id, params = self._queue.get()
                task_func(task_id, params)
                self._queue.task_done()
            except Exception as e:
                print(f"[TaskQueue] Worker error: {e}")
                import traceback
                traceback.print_exc()
    
    def submit(self, task_func: Callable, task_type: str, params: dict) -> str:
        """
        提交任务到队列
        
        Args:
            task_func: 任务执行函数
            task_type: 任务类型
            params: 任务参数
        
        Returns:
            task_id: 任务ID
        """
        task_id = str(uuid.uuid4())[:8]
        
        self._tasks[task_id] = {
            "task_id": task_id,
            "task_type": task_type,
            "status": TaskStatus.PENDING,
            "progress": 0,
            "message": "等待执行...",
            "result": None,
            "error": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "params": params
        }
        
        self._queue.put((task_func, task_id, params))
        return task_id
    
    def get_task(self, task_id: str) -> Optional[dict]:
        """获取任务信息"""
        return self._tasks.get(task_id)
    
    def update_task(self, task_id: str, **kwargs):
        """更新任务状态"""
        if task_id in self._tasks:
            self._tasks[task_id].update(kwargs)
            self._tasks[task_id]["updated_at"] = datetime.now().isoformat()
    
    def list_tasks(self, limit: int = 20) -> list:
        """列出最近的任务"""
        tasks = list(self._tasks.values())
        tasks.sort(key=lambda x: x["created_at"], reverse=True)
        return tasks[:limit]


# 全局任务队列实例
task_queue = TaskQueue()


# ==================== 任务执行函数 ====================

def execute_generate_video(task_id: str, params: dict):
    """
    执行生成视频任务
    
    Args:
        task_id: 任务ID
        params: {
            "ecom_code": str,
            "image_path": str,
            "duration": int,
            "resolution": str,
            "output_dir": str
        }
    """
    queue = TaskQueue()
    
    try:
        queue.update_task(task_id, status=TaskStatus.RUNNING, message="开始生成视频...")
        
        ecom_code = params["ecom_code"]
        image_path = params["image_path"]
        duration = params.get("duration", 5)
        resolution = params.get("resolution", "480p")
        output_dir = params["output_dir"]
        
        # 确保输出目录存在
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 调用生成脚本
        queue.update_task(task_id, progress=10, message="正在生成首帧模特图...")
        
        cmd = [
            sys.executable,
            str(BASE_DIR / "src" / "generate_video_v3.py"),
            "--image", image_path,
            "--duration", str(duration),
            "--resolution", resolution,
            "--output_dir", output_dir
        ]
        
        print(f"[TaskQueue] 执行命令: {' '.join(cmd)}")
        
        # 设置环境变量禁用 Python 缓冲
        import os
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        
        # 使用 Popen 实时读取输出
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=str(BASE_DIR),
            env=env
        )
        
        # 实时读取输出
        output_lines = []
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            
            if line:
                line = line.rstrip()
                output_lines.append(line)
                print(f"[VideoGen] {line}")
                
                # 更新进度
                if "首帧" in line or "模特图" in line:
                    queue.update_task(task_id, progress=10, message=line)
                elif "上传" in line:
                    queue.update_task(task_id, progress=20, message=line)
                elif "视频 [1/3]" in line or "视频 [1]" in line:
                    queue.update_task(task_id, progress=30, message="生成第1段视频...")
                elif "视频 [2/3]" in line or "视频 [2]" in line:
                    queue.update_task(task_id, progress=50, message="生成第2段视频...")
                elif "视频 [3/3]" in line or "视频 [3]" in line:
                    queue.update_task(task_id, progress=70, message="生成第3段视频...")
                elif "合并" in line:
                    queue.update_task(task_id, progress=90, message="合并视频...")
                elif "OK" in line or "成功" in line:
                    queue.update_task(task_id, message=line)
                elif "Error" in line or "失败" in line or "error" in line:
                    queue.update_task(task_id, message=f"错误: {line}")
        
        returncode = process.wait(timeout=600)
        output = '\n'.join(output_lines)
        
        print(f"[TaskQueue] returncode: {returncode}")
        
        if returncode != 0:
            error_msg = output[-500:] if len(output) > 500 else output
            queue.update_task(
                task_id,
                status=TaskStatus.FAILED,
                error=error_msg
            )
            return
        
        # 解析输出结果
        # 查找 [VIDEO_RESULT] 标记
        if "[VIDEO_RESULT]" in output:
            result_json = output.split("[VIDEO_RESULT]")[-1].strip()
            try:
                task_result = json.loads(result_json)
            except:
                task_result = {"raw_output": output[-1000:]}
        else:
            task_result = {"raw_output": output[-1000:]}
        
        # 读取生成的文件列表
        output_path = Path(output_dir)
        files = []
        for f in output_path.iterdir():
            if f.suffix in [".mp4", ".png", ".jpg"]:
                files.append(str(f.relative_to(ASSETS_DIR.parent)))
        
        queue.update_task(
            task_id,
            status=TaskStatus.SUCCESS,
            progress=100,
            message="视频生成完成",
            result={
                "output_dir": output_dir,
                "files": files,
                "merged_video": str(output_path / "video_merged.mp4") if (output_path / "video_merged.mp4").exists() else None,
                "raw_result": task_result
            }
        )
        
    except subprocess.TimeoutExpired:
        queue.update_task(task_id, status=TaskStatus.FAILED, error="任务超时（10分钟）")
    except Exception as e:
        queue.update_task(task_id, status=TaskStatus.FAILED, error=str(e))


def execute_generate_images(task_id: str, params: dict):
    """
    执行生成图片任务（展示图或详情图）
    
    Args:
        task_id: 任务ID
        params: {
            "ecom_code": str,
            "image_path": str,
            "output_dir": str,
            "task_type": "showcase" | "detail"
        }
    """
    queue = TaskQueue()
    
    try:
        queue.update_task(task_id, status=TaskStatus.RUNNING, message="开始生成图片...")
        
        ecom_code = params["ecom_code"]
        image_path = params["image_path"]
        output_dir = params["output_dir"]
        task_type = params.get("task_type", "detail")
        
        print(f"[TaskQueue] ecom_code={ecom_code}, image_path={image_path}, output_dir={output_dir}")
        
        # 确保输出目录存在
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 调用生成脚本
        cmd = [
            sys.executable,
            str(BASE_DIR / "src" / "generate_images.py"),
            "--image", image_path,
            "--output_dir", output_dir
        ]
        
        print(f"[TaskQueue] 执行命令: {' '.join(cmd)}")
        
        # 使用 Popen 实时读取输出并更新进度
        import re
        import os
        
        # 设置环境变量禁用 Python 缓冲
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=str(BASE_DIR),
            env=env
        )
        
        # 实时读取输出
        output_lines = []
        current_image = 0
        total_images = 9
        
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            
            if line:
                line = line.rstrip()
                output_lines.append(line)
                print(f"[GenerateImages] {line}")
                
                # 解析进度：查找 "生成 [x/9]" 或 "生成 [x/y]"
                match = re.search(r'生成 \[(\d+)/(\d+)\]', line)
                if match:
                    current_image = int(match.group(1))
                    total_images = int(match.group(2))
                    progress = int((current_image / total_images) * 100)
                    queue.update_task(
                        task_id,
                        progress=progress,
                        message=f"正在生成第 {current_image}/{total_images} 张图片..."
                    )
                
                # 解析成功/失败状态
                if "Success!" in line or "[OK]" in line:
                    queue.update_task(
                        task_id,
                        message=f"第 {current_image}/{total_images} 张完成"
                    )
                
                if "Retry" in line or "failed" in line.lower():
                    queue.update_task(
                        task_id,
                        message=f"第 {current_image}/{total_images} 张重试中..."
                    )
        
        # 等待进程完成
        returncode = process.wait(timeout=1200)  # 20分钟超时
        
        output = '\n'.join(output_lines)
        print(f"[TaskQueue] returncode: {returncode}")
        print(f"[TaskQueue] output lines: {len(output_lines)}")
        
        if returncode != 0:
            error_msg = output[-500:] if len(output) > 500 else output
            queue.update_task(
                task_id,
                status=TaskStatus.FAILED,
                error=error_msg
            )
            return
        
        # 解析输出结果
        if "[GENERATION_RESULT]" in output:
            result_json = output.split("[GENERATION_RESULT]")[-1].strip()
            try:
                task_result = json.loads(result_json)
            except:
                task_result = {"raw_output": output[-1000:]}
        else:
            task_result = {"raw_output": output[-1000:]}
        
        # 读取生成的文件列表
        output_path = Path(output_dir)
        files = []
        for f in output_path.iterdir():
            if f.suffix in [".png", ".jpg"]:
                files.append(str(f.relative_to(ASSETS_DIR.parent)))
        
        queue.update_task(
            task_id,
            status=TaskStatus.SUCCESS,
            progress=100,
            message=f"图片生成完成，共 {len(files)} 张",
            result={
                "output_dir": output_dir,
                "files": files,
                "count": len(files),
                "raw_result": task_result
            }
        )
        
    except subprocess.TimeoutExpired:
        queue.update_task(task_id, status=TaskStatus.FAILED, error="任务超时（20分钟）")
    except Exception as e:
        queue.update_task(task_id, status=TaskStatus.FAILED, error=str(e))


# ==================== 便捷函数 ====================

def submit_video_task(ecom_code: str, image_path: str, duration: int = 5, resolution: str = "480p", group_index: int = 1) -> str:
    """
    提交视频生成任务
    
    Returns:
        task_id
    """
    output_dir = ASSETS_DIR / ecom_code / "video" / f"group_{group_index}"
    
    # 如果目录已存在，找下一个可用的组号
    while output_dir.exists() and any(output_dir.iterdir()):
        group_index += 1
        output_dir = ASSETS_DIR / ecom_code / "video" / f"group_{group_index}"
    
    params = {
        "ecom_code": ecom_code,
        "image_path": image_path,
        "duration": duration,
        "resolution": resolution,
        "output_dir": str(output_dir),
        "group_index": group_index
    }
    
    return task_queue.submit(
        execute_generate_video,
        "generate_video",
        params
    )


def submit_image_task(ecom_code: str, image_path: str, task_type: str = "detail", group_index: int = 1) -> str:
    """
    提交图片生成任务
    
    Args:
        task_type: "showcase" | "detail"
    
    Returns:
        task_id
    """
    output_dir = ASSETS_DIR / ecom_code / task_type / f"group_{group_index}"
    
    # 如果目录已存在，找下一个可用的组号
    while output_dir.exists() and any(output_dir.iterdir()):
        group_index += 1
        output_dir = ASSETS_DIR / ecom_code / task_type / f"group_{group_index}"
    
    params = {
        "ecom_code": ecom_code,
        "image_path": image_path,
        "output_dir": str(output_dir),
        "task_type": task_type,
        "group_index": group_index
    }
    
    return task_queue.submit(
        execute_generate_images,
        f"generate_{task_type}",
        params
    )
