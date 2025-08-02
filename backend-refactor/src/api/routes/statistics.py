"""
统计数据API路由
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List
from ..dependencies import get_db
from ...models.guild_member import GuildMember
from ...schemas.statistics import (
    Statistics,
    ClassDistribution,
    RealmDistribution,
    MythicPlusStats,
    ScoreDistribution
)

router = APIRouter()

@router.get("/overview", response_model=Statistics)
def get_overview(db: Session = Depends(get_db)):
    """获取公会统计总览"""
    try:
        # 基础统计
        total_members = db.query(GuildMember).count()
        active_members = db.query(GuildMember).filter(GuildMember.last_online_days <= 7).count()
        online_members = db.query(GuildMember).filter(GuildMember.is_online == True).count()
        classes_count = db.query(func.count(func.distinct(GuildMember.class_name))).scalar()
        realms_count = db.query(func.count(func.distinct(GuildMember.realm_name))).scalar()
        
        # 平均数据
        avg_level = db.query(func.avg(GuildMember.level)).scalar()
        avg_item_level = db.query(func.avg(GuildMember.average_item_level)).scalar()
        avg_mythic_score = db.query(func.avg(GuildMember.mythic_plus_score)).scalar()
        avg_achievement_points = db.query(func.avg(GuildMember.achievement_points)).scalar()
        
        # 最高数据
        max_level = db.query(func.max(GuildMember.level)).scalar()
        max_item_level = db.query(func.max(GuildMember.average_item_level)).scalar()
        max_mythic_score = db.query(func.max(GuildMember.mythic_plus_score)).scalar()
        max_achievement_points = db.query(func.max(GuildMember.achievement_points)).scalar()
        
        # 顶级玩家
        top_mythic_players_raw = db.query(GuildMember).order_by(desc(GuildMember.mythic_plus_score)).limit(5).all()
        top_mount_collectors_raw = db.query(GuildMember).order_by(desc(GuildMember.mounts_count)).limit(5).all()
        top_achievement_players_raw = db.query(GuildMember).order_by(desc(GuildMember.achievement_points)).limit(5).all()
        
        # 转换为Pydantic模型
        from ...schemas.statistics import TopPlayer
        
        def convert_to_top_player(member):
            return TopPlayer(
                id=member.id,
                name=member.name,
                realm_name=member.realm_name,
                level=member.level,
                class_name=member.class_name,
                faction=member.faction,
                mythic_plus_score=member.mythic_plus_score,
                achievement_points=member.achievement_points,
                mounts_count=member.mounts_count,
                average_item_level=member.average_item_level
            )
        
        top_mythic_players = [convert_to_top_player(m) for m in top_mythic_players_raw]
        top_mount_collectors = [convert_to_top_player(m) for m in top_mount_collectors_raw]
        top_achievement_players = [convert_to_top_player(m) for m in top_achievement_players_raw]
        
        return Statistics(
            total_members=total_members,
            active_members=active_members,
            online_members=online_members,
            classes_count=classes_count,
            realms_count=realms_count,
            average_level=float(avg_level) if avg_level else None,
            average_item_level=float(avg_item_level) if avg_item_level else None,
            average_mythic_plus_score=float(avg_mythic_score) if avg_mythic_score else None,
            average_achievement_points=float(avg_achievement_points) if avg_achievement_points else None,
            max_level=max_level,
            max_item_level=float(max_item_level) if max_item_level else None,
            max_mythic_plus_score=float(max_mythic_score) if max_mythic_score else None,
            max_achievement_points=max_achievement_points,
            top_mythic_players=top_mythic_players,
            top_mount_collectors=top_mount_collectors,
            top_achievement_players=top_achievement_players
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")

@router.get("/class-distribution", response_model=List[ClassDistribution])
def get_class_distribution(db: Session = Depends(get_db)):
    """获取职业分布统计"""
    try:
        result = db.query(
            GuildMember.class_name,
            func.count(GuildMember.id).label('count')
        ).group_by(GuildMember.class_name).order_by(desc('count')).all()
        
        total = sum(item.count for item in result)
        
        return [
            ClassDistribution(
                class_name=item.class_name,
                count=item.count,
                percentage=round((item.count / total) * 100, 2) if total > 0 else 0
            )
            for item in result
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取职业分布失败: {str(e)}")

@router.get("/realm-distribution", response_model=List[RealmDistribution])
def get_realm_distribution(db: Session = Depends(get_db)):
    """获取服务器分布统计"""
    try:
        result = db.query(
            GuildMember.realm_name,
            func.count(GuildMember.id).label('count')
        ).group_by(GuildMember.realm_name).order_by(desc('count')).all()
        
        total = sum(item.count for item in result)
        
        return [
            RealmDistribution(
                realm_name=item.realm_name,
                count=item.count,
                percentage=round((item.count / total) * 100, 2) if total > 0 else 0
            )
            for item in result
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取服务器分布失败: {str(e)}")

@router.get("/mythic-plus-stats", response_model=MythicPlusStats)
def get_mythic_plus_stats(db: Session = Depends(get_db)):
    """获取Mythic+统计信息"""
    try:
        # 基础统计
        avg_score = db.query(func.avg(GuildMember.mythic_plus_score)).scalar()
        max_score = db.query(func.max(GuildMember.mythic_plus_score)).scalar()
        active_players = db.query(GuildMember).filter(GuildMember.mythic_plus_score > 0).count()
        
        # 评分分布
        score_ranges = [
            (0, 500, "0-500"),
            (501, 1000, "501-1000"),
            (1001, 1500, "1001-1500"),
            (1501, 2000, "1501-2000"),
            (2001, 2500, "2001-2500"),
            (2501, 3000, "2501-3000"),
            (3001, float('inf'), "3000+")
        ]
        
        score_distribution = []
        for min_score, max_score_range, range_name in score_ranges:
            if max_score_range == float('inf'):
                count = db.query(GuildMember).filter(GuildMember.mythic_plus_score >= min_score).count()
            else:
                count = db.query(GuildMember).filter(
                    GuildMember.mythic_plus_score >= min_score,
                    GuildMember.mythic_plus_score <= max_score_range
                ).count()
            
            score_distribution.append(ScoreDistribution(
                range=range_name,
                count=count
            ))
        
        return MythicPlusStats(
            average_score=float(avg_score) if avg_score else None,
            max_score=float(max_score) if max_score else None,
            active_players=active_players,
            score_distribution=score_distribution
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取Mythic+统计失败: {str(e)}")

@router.get("/faction-distribution")
def get_faction_distribution(db: Session = Depends(get_db)):
    """获取阵营分布统计"""
    try:
        result = db.query(
            GuildMember.faction,
            func.count(GuildMember.id).label('count')
        ).group_by(GuildMember.faction).all()
        
        total = sum(item.count for item in result)
        
        return {
            "factions": [
                {
                    "faction": item.faction,
                    "count": item.count,
                    "percentage": round((item.count / total) * 100, 2) if total > 0 else 0
                }
                for item in result
            ],
            "total": total
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取阵营分布失败: {str(e)}")

@router.get("/level-distribution")
def get_level_distribution(db: Session = Depends(get_db)):
    """获取等级分布统计"""
    try:
        level_ranges = [
            (1, 10, "1-10"),
            (11, 20, "11-20"),
            (21, 30, "21-30"),
            (31, 40, "31-40"),
            (41, 50, "41-50"),
            (51, 60, "51-60"),
            (61, 70, "61-70")
        ]
        
        distribution = []
        for min_level, max_level, range_name in level_ranges:
            count = db.query(GuildMember).filter(
                GuildMember.level >= min_level,
                GuildMember.level <= max_level
            ).count()
            
            distribution.append({
                "range": range_name,
                "count": count
            })
        
        return {"level_distribution": distribution}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取等级分布失败: {str(e)}")

@router.get("/online-status")
def get_online_status(db: Session = Depends(get_db)):
    """获取在线状态统计"""
    try:
        online_count = db.query(GuildMember).filter(GuildMember.is_online == True).count()
        offline_count = db.query(GuildMember).filter(GuildMember.is_online == False).count()
        total = online_count + offline_count
        
        return {
            "online": online_count,
            "offline": offline_count,
            "total": total,
            "online_percentage": round((online_count / total) * 100, 2) if total > 0 else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取在线状态统计失败: {str(e)}") 