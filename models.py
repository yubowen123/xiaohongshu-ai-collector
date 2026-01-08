"""
数据模型
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Author(BaseModel):
    """博主模型"""
    id: Optional[int] = None
    user_id: str = Field(..., description="小红书用户 ID")
    nickname: str = Field(..., description="昵称")
    homepage_url: str = Field(..., description="主页链接")
    category: str = Field(default="AI", description="分类")
    is_active: bool = Field(default=True, description="是否启用采集")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Note(BaseModel):
    """笔记模型"""
    id: Optional[int] = None
    note_id: str = Field(..., description="小红书笔记 ID")
    author_user_id: str = Field(..., description="作者用户 ID")
    title: str = Field(..., description="标题")
    content: str = Field(default="", description="内容摘要")
    note_url: str = Field(..., description="笔记链接")
    cover_image: str = Field(default="", description="封面图片")
    publish_time: Optional[str] = Field(None, description="发布时间")
    likes_count: int = Field(default=0, description="点赞数")
    collected: bool = Field(default=False, description="是否已采集")
    synced_to_feishu: bool = Field(default=False, description="是否已同步到飞书")
    feishu_record_id: str = Field(default="", description="飞书记录 ID")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CollectionTask(BaseModel):
    """采集任务模型"""
    id: Optional[int] = None
    task_type: str = Field(..., description="任务类型: auto/manual")
    status: str = Field(default="pending", description="状态: pending/running/completed/failed")
    total_authors: int = Field(default=0, description="总博主数")
    total_notes: int = Field(default=0, description="总笔记数")
    new_notes: int = Field(default=0, description="新采集笔记数")
    synced_notes: int = Field(default=0, description="已同步笔记数")
    error_message: str = Field(default="", description="错误信息")
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
