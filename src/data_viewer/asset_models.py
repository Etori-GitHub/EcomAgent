# -*- coding: utf-8 -*-
"""素材管理数据模型"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class AssetType(str, Enum):
    """素材类型"""
    SHOWCASE = "showcase"      # 展示图（首帧模特图）
    VIDEO = "video"            # 宣传视频
    DETAIL = "detail"          # 详情图


class AssetGroup(BaseModel):
    """素材组"""
    id: int
    ecom_code: str
    asset_type: AssetType
    group_index: int
    files: List[str]              # 文件路径列表
    params: Optional[Dict] = None # 生成参数（时长、分辨率等）
    created_at: datetime


class AssetList(BaseModel):
    """素材列表（按类型分组）"""
    showcase: List[AssetGroup] = []
    video: List[AssetGroup] = []
    detail: List[AssetGroup] = []


class GenerateVideoRequest(BaseModel):
    """生成视频请求"""
    ecom_code: str
    image_path: Optional[str] = None   # 自定义图片路径，不传则用货源图片
    duration: int = 5                   # 每段时长（秒）
    resolution: str = "480p"            # 分辨率


class GenerateShowcaseRequest(BaseModel):
    """生成展示图请求"""
    ecom_code: str
    image_path: Optional[str] = None


class GenerateDetailRequest(BaseModel):
    """生成详情图请求"""
    ecom_code: str
    image_path: Optional[str] = None
    count: int = 9                      # 生成图片数量


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class TaskInfo(BaseModel):
    """任务信息"""
    task_id: str
    task_type: str                     # 'generate_video', 'generate_showcase', 'generate_detail'
    status: TaskStatus
    progress: int = 0                   # 0-100
    message: str = ""
    result: Optional[Dict] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
