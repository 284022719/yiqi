"""
公会成员Pydantic Schema
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class GuildMemberCreate(BaseModel):
    """创建公会成员的请求模型"""
    name: str = Field(..., min_length=1, max_length=50, description="角色名称")
    realm_name: str = Field(..., min_length=1, max_length=50, description="服务器名称")
    level: Optional[int] = Field(None, ge=1, le=70, description="角色等级")
    class_name: Optional[str] = Field(None, max_length=30, description="职业")
    race_name: Optional[str] = Field(None, max_length=30, description="种族")
    faction: str = Field(..., pattern="^(alliance|horde)$", description="阵营")
    mythic_plus_score: Optional[float] = Field(None, ge=0, description="Mythic+评分")
    achievement_points: Optional[int] = Field(None, ge=0, description="成就点数")
    mounts_count: Optional[int] = Field(None, ge=0, description="坐骑数量")
    average_item_level: Optional[float] = Field(None, ge=0, description="平均装等")
    last_online_days: Optional[int] = Field(None, ge=0, description="最后在线天数")
    is_online: Optional[bool] = Field(False, description="是否在线")
    guild_rank: Optional[str] = Field(None, max_length=50, description="公会职位")
    note: Optional[str] = Field(None, description="备注")


class GuildMemberUpdate(BaseModel):
    """更新公会成员的请求模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    realm_name: Optional[str] = Field(None, min_length=1, max_length=50)
    level: Optional[int] = Field(None, ge=1, le=70)
    class_name: Optional[str] = Field(None, max_length=30)
    race_name: Optional[str] = Field(None, max_length=30)
    faction: Optional[str] = Field(None, pattern="^(alliance|horde)$")
    mythic_plus_score: Optional[float] = Field(None, ge=0)
    achievement_points: Optional[int] = Field(None, ge=0)
    mounts_count: Optional[int] = Field(None, ge=0)
    average_item_level: Optional[float] = Field(None, ge=0)
    last_online_days: Optional[int] = Field(None, ge=0)
    is_online: Optional[bool] = None
    guild_rank: Optional[str] = Field(None, max_length=50)
    note: Optional[str] = None


class GuildMemberResponse(BaseModel):
    """公会成员响应模型"""
    id: int
    name: str
    realm_name: str
    level: Optional[int]
    class_name: Optional[str]
    race_name: Optional[str]
    faction: str
    mythic_plus_score: Optional[float]
    achievement_points: Optional[int]
    mounts_count: Optional[int]
    average_item_level: Optional[float]
    last_online_days: Optional[int]
    is_online: bool
    guild_rank: Optional[str]
    note: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class GuildMemberListResponse(BaseModel):
    """公会成员列表响应模型"""
    members: List[GuildMemberResponse]
    total: int
    page: int
    size: int
    pages: int


class GuildMemberSearchParams(BaseModel):
    """公会成员搜索参数"""
    name: Optional[str] = Field(None, description="角色名称搜索")
    realm_name: Optional[str] = Field(None, description="服务器筛选")
    faction: Optional[str] = Field(None, pattern="^(alliance|horde)$", description="阵营筛选")
    class_name: Optional[str] = Field(None, description="职业筛选")
    guild_rank: Optional[str] = Field(None, description="公会职位筛选")
    is_online: Optional[bool] = Field(None, description="在线状态筛选")
    page: int = Field(1, ge=1, description="页码")
    size: int = Field(20, ge=1, le=100, description="每页数量")
    sort_by: str = Field("name", description="排序字段")
    sort_order: str = Field("asc", pattern="^(asc|desc)$", description="排序方向") 