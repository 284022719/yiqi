"""
搜索功能API路由
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional

from src.database.connection import get_db
from src.database.models import GuildMember, SearchResponse, GuildMemberResponse
from src.utils.exceptions import DatabaseException
from src.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/members", response_model=SearchResponse)
async def search_members(
    q: str = Query(..., description="搜索关键词"),
    limit: int = Query(20, ge=1, le=100, description="结果数量限制"),
    class_name: Optional[str] = Query(None, description="职业筛选"),
    realm_name: Optional[str] = Query(None, description="服务器筛选"),
    min_level: Optional[int] = Query(None, ge=1, le=70, description="最低等级"),
    db: Session = Depends(get_db)
):
    """搜索公会成员"""
    try:
        # 构建基础查询
        query = db.query(GuildMember)
        
        # 搜索条件
        search_conditions = or_(
            GuildMember.name.ilike(f"%{q}%"),
            GuildMember.realm_name.ilike(f"%{q}%"),
            GuildMember.class_name.ilike(f"%{q}%"),
            GuildMember.race_name.ilike(f"%{q}%")
        )
        
        query = query.filter(search_conditions)
        
        # 应用筛选条件
        if class_name:
            query = query.filter(GuildMember.class_name == class_name)
        if realm_name:
            query = query.filter(GuildMember.realm_name == realm_name)
        if min_level:
            query = query.filter(GuildMember.level >= min_level)
        
        # 获取结果
        results = query.limit(limit).all()
        total = query.count()
        
        return SearchResponse(
            results=results,
            total=total,
            query=q
        )
        
    except Exception as e:
        logger.error(f"搜索成员时出错: {str(e)}")
        raise DatabaseException("搜索成员失败")


@router.get("/advanced")
async def advanced_search(
    name: Optional[str] = Query(None, description="角色名称"),
    realm_name: Optional[str] = Query(None, description="服务器名称"),
    class_name: Optional[str] = Query(None, description="职业"),
    race_name: Optional[str] = Query(None, description="种族"),
    faction: Optional[str] = Query(None, description="阵营"),
    min_level: Optional[int] = Query(None, ge=1, le=70, description="最低等级"),
    max_level: Optional[int] = Query(None, ge=1, le=70, description="最高等级"),
    min_mythic_score: Optional[float] = Query(None, ge=0, description="最低Mythic+评分"),
    max_mythic_score: Optional[float] = Query(None, ge=0, description="最高Mythic+评分"),
    min_mounts: Optional[int] = Query(None, ge=0, description="最少坐骑数量"),
    max_mounts: Optional[int] = Query(None, ge=0, description="最多坐骑数量"),
    min_achievement_points: Optional[int] = Query(None, ge=0, description="最少成就点数"),
    max_achievement_points: Optional[int] = Query(None, ge=0, description="最多成就点数"),
    is_online: Optional[bool] = Query(None, description="是否在线"),
    max_last_online_days: Optional[int] = Query(None, ge=0, description="最大离线天数"),
    limit: int = Query(20, ge=1, le=100, description="结果数量限制"),
    db: Session = Depends(get_db)
):
    """高级搜索"""
    try:
        query = db.query(GuildMember)
        
        # 构建筛选条件
        filters = []
        
        if name:
            filters.append(GuildMember.name.ilike(f"%{name}%"))
        if realm_name:
            filters.append(GuildMember.realm_name.ilike(f"%{realm_name}%"))
        if class_name:
            filters.append(GuildMember.class_name == class_name)
        if race_name:
            filters.append(GuildMember.race_name == race_name)
        if faction:
            filters.append(GuildMember.faction == faction)
        if min_level:
            filters.append(GuildMember.level >= min_level)
        if max_level:
            filters.append(GuildMember.level <= max_level)
        if min_mythic_score is not None:
            filters.append(GuildMember.mythic_plus_score >= min_mythic_score)
        if max_mythic_score is not None:
            filters.append(GuildMember.mythic_plus_score <= max_mythic_score)
        if min_mounts is not None:
            filters.append(GuildMember.mounts_count >= min_mounts)
        if max_mounts is not None:
            filters.append(GuildMember.mounts_count <= max_mounts)
        if min_achievement_points is not None:
            filters.append(GuildMember.achievement_points >= min_achievement_points)
        if max_achievement_points is not None:
            filters.append(GuildMember.achievement_points <= max_achievement_points)
        if is_online is not None:
            filters.append(GuildMember.is_online == is_online)
        if max_last_online_days is not None:
            filters.append(GuildMember.last_online_days <= max_last_online_days)
        
        # 应用筛选条件
        if filters:
            query = query.filter(and_(*filters))
        
        # 获取结果
        results = query.limit(limit).all()
        total = query.count()
        
        return {
            "results": results,
            "total": total,
            "filters_applied": len(filters)
        }
        
    except Exception as e:
        logger.error(f"高级搜索时出错: {str(e)}")
        raise DatabaseException("高级搜索失败")


@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., description="搜索关键词"),
    limit: int = Query(10, ge=1, le=50, description="建议数量"),
    db: Session = Depends(get_db)
):
    """获取搜索建议"""
    try:
        # 角色名称建议
        name_suggestions = db.query(GuildMember.name).filter(
            GuildMember.name.ilike(f"{q}%")
        ).distinct().limit(limit).all()
        
        # 服务器名称建议
        realm_suggestions = db.query(GuildMember.realm_name).filter(
            GuildMember.realm_name.ilike(f"{q}%")
        ).distinct().limit(limit).all()
        
        # 职业建议
        class_suggestions = db.query(GuildMember.class_name).filter(
            GuildMember.class_name.ilike(f"{q}%")
        ).distinct().limit(limit).all()
        
        return {
            "name_suggestions": [s[0] for s in name_suggestions],
            "realm_suggestions": [s[0] for s in realm_suggestions],
            "class_suggestions": [s[0] for s in class_suggestions]
        }
        
    except Exception as e:
        logger.error(f"获取搜索建议时出错: {str(e)}")
        raise DatabaseException("获取搜索建议失败")


@router.get("/popular-searches")
async def get_popular_searches(db: Session = Depends(get_db)):
    """获取热门搜索"""
    try:
        # 这里可以实现热门搜索逻辑
        # 暂时返回一些示例数据
        return {
            "popular_searches": [
                "法师",
                "战士", 
                "艾泽拉斯",
                "70级",
                "联盟"
            ]
        }
        
    except Exception as e:
        logger.error(f"获取热门搜索时出错: {str(e)}")
        raise DatabaseException("获取热门搜索失败") 