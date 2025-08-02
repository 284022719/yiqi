"""
数据库模型定义
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from .connection import Base


class GuildMember(Base):
    """公会成员数据库模型"""
    __tablename__ = "guild_members"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 基础信息
    name = Column(String(50), nullable=False, index=True, comment="角色名称")
    realm_name = Column(String(50), nullable=False, index=True, comment="服务器名称")
    level = Column(Integer, default=1, comment="角色等级")
    class_name = Column(String(20), nullable=False, index=True, comment="职业名称")
    race_name = Column(String(20), nullable=False, comment="种族名称")
    faction = Column(String(10), nullable=False, comment="阵营")
    
    # 统计数据
    mythic_plus_score = Column(Float, default=0.0, comment="Mythic+评分")
    achievement_points = Column(Integer, default=0, comment="成就点数")
    mounts_count = Column(Integer, default=0, comment="坐骑数量")
    average_item_level = Column(Float, default=0.0, comment="平均装等")
    
    # 在线状态
    last_online_days = Column(Integer, default=0, comment="最后在线天数")
    is_online = Column(Boolean, default=False, comment="是否在线")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 额外信息
    guild_rank = Column(String(20), default="成员", comment="公会职位")
    note = Column(Text, comment="备注")
    
    def __repr__(self):
        return f"<GuildMember(name='{self.name}', realm='{self.realm_name}', class='{self.class_name}')>"


# Pydantic模型用于API
class GuildMemberBase(BaseModel):
    """公会成员基础模型"""
    name: str = Field(..., description="角色名称")
    realm_name: str = Field(..., description="服务器名称")
    level: int = Field(default=1, description="角色等级")
    class_name: str = Field(..., description="职业名称")
    race_name: str = Field(..., description="种族名称")
    faction: str = Field(..., description="阵营")
    mythic_plus_score: Optional[float] = Field(default=0.0, description="Mythic+评分")
    achievement_points: Optional[int] = Field(default=0, description="成就点数")
    mounts_count: Optional[int] = Field(default=0, description="坐骑数量")
    average_item_level: Optional[float] = Field(default=0.0, description="平均装等")
    last_online_days: Optional[int] = Field(default=0, description="最后在线天数")
    is_online: Optional[bool] = Field(default=False, description="是否在线")
    guild_rank: Optional[str] = Field(default="成员", description="公会职位")
    note: Optional[str] = Field(default=None, description="备注")


class GuildMemberCreate(GuildMemberBase):
    """创建公会成员模型"""
    pass


class GuildMemberUpdate(BaseModel):
    """更新公会成员模型"""
    name: Optional[str] = Field(default=None, description="角色名称")
    realm_name: Optional[str] = Field(default=None, description="服务器名称")
    level: Optional[int] = Field(default=None, description="角色等级")
    class_name: Optional[str] = Field(default=None, description="职业名称")
    race_name: Optional[str] = Field(default=None, description="种族名称")
    faction: Optional[str] = Field(default=None, description="阵营")
    mythic_plus_score: Optional[float] = Field(default=None, description="Mythic+评分")
    achievement_points: Optional[int] = Field(default=None, description="成就点数")
    mounts_count: Optional[int] = Field(default=None, description="坐骑数量")
    average_item_level: Optional[float] = Field(default=None, description="平均装等")
    last_online_days: Optional[int] = Field(default=None, description="最后在线天数")
    is_online: Optional[bool] = Field(default=None, description="是否在线")
    guild_rank: Optional[str] = Field(default=None, description="公会职位")
    note: Optional[str] = Field(default=None, description="备注")


class GuildMemberResponse(GuildMemberBase):
    """公会成员响应模型"""
    id: int = Field(..., description="成员ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class GuildMemberListResponse(BaseModel):
    """公会成员列表响应模型"""
    members: List[GuildMemberResponse] = Field(..., description="成员列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    size: int = Field(..., description="每页数量")
    pages: int = Field(..., description="总页数")


class StatisticsResponse(BaseModel):
    """统计信息响应模型"""
    total_members: int = Field(..., description="总成员数")
    active_members: int = Field(..., description="活跃成员数")
    classes_count: int = Field(..., description="职业种类数")
    realms_count: int = Field(..., description="服务器数量")
    online_members: int = Field(..., description="在线成员数")
    top_mythic_players: List[GuildMemberResponse] = Field(..., description="Mythic+排行榜")
    top_mount_collectors: List[GuildMemberResponse] = Field(..., description="坐骑收藏排行榜")
    top_achievement_players: List[GuildMemberResponse] = Field(..., description="成就排行榜")


class SearchResponse(BaseModel):
    """搜索响应模型"""
    results: List[GuildMemberResponse] = Field(..., description="搜索结果")
    total: int = Field(..., description="结果总数")
    query: str = Field(..., description="搜索查询") 