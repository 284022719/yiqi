"""
爬虫API路由
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any
import asyncio
import aiohttp
import json
from datetime import datetime
from ..dependencies import get_db
from ...models.guild_member import GuildMember
from ...schemas.guild_member import GuildMemberCreate, GuildMemberUpdate

router = APIRouter()

# 模拟的爬虫数据
MOCK_GUILD_DATA = [
    {
        "name": "战士王",
        "realm_name": "艾泽拉斯",
        "level": 70,
        "class_name": "Warrior",
        "race_name": "Human",
        "faction": "Alliance",
        "mythic_plus_score": 2500,
        "achievement_points": 15000,
        "mounts_count": 150,
        "average_item_level": 425.5,
        "last_online_days": 2,
        "is_online": True,
        "guild_rank": "Officer",
        "note": "公会主力坦克"
    },
    {
        "name": "法师小美",
        "realm_name": "艾泽拉斯",
        "level": 70,
        "class_name": "Mage",
        "race_name": "Blood Elf",
        "faction": "Horde",
        "mythic_plus_score": 2800,
        "achievement_points": 18000,
        "mounts_count": 200,
        "average_item_level": 430.2,
        "last_online_days": 0,
        "is_online": True,
        "guild_rank": "Member",
        "note": "高输出法师"
    },
    {
        "name": "猎人阿强",
        "realm_name": "艾泽拉斯",
        "level": 70,
        "class_name": "Hunter",
        "race_name": "Night Elf",
        "faction": "Alliance",
        "mythic_plus_score": 2200,
        "achievement_points": 12000,
        "mounts_count": 180,
        "average_item_level": 420.8,
        "last_online_days": 5,
        "is_online": False,
        "guild_rank": "Member",
        "note": "PVP专家"
    },
    {
        "name": "牧师小丽",
        "realm_name": "艾泽拉斯",
        "level": 70,
        "class_name": "Priest",
        "race_name": "Draenei",
        "faction": "Alliance",
        "mythic_plus_score": 1900,
        "achievement_points": 14000,
        "mounts_count": 120,
        "average_item_level": 415.3,
        "last_online_days": 1,
        "is_online": True,
        "guild_rank": "Officer",
        "note": "主治疗"
    },
    {
        "name": "盗贼影子",
        "realm_name": "艾泽拉斯",
        "level": 70,
        "class_name": "Rogue",
        "race_name": "Undead",
        "faction": "Horde",
        "mythic_plus_score": 2600,
        "achievement_points": 16000,
        "mounts_count": 160,
        "average_item_level": 428.7,
        "last_online_days": 3,
        "is_online": False,
        "guild_rank": "Member",
        "note": "潜行专家"
    }
]

@router.post("/start")
async def start_crawler(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """启动数据爬虫"""
    try:
        # 在后台任务中执行爬虫
        background_tasks.add_task(run_crawler_task, db)
        
        return {
            "message": "爬虫任务已启动",
            "status": "running",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动爬虫失败: {str(e)}")

@router.get("/status")
async def get_crawler_status():
    """获取爬虫状态"""
    return {
        "status": "idle",
        "last_run": datetime.now().isoformat(),
        "total_members_crawled": len(MOCK_GUILD_DATA),
        "next_scheduled_run": None
    }

@router.post("/sync")
async def sync_guild_data(db: Session = Depends(get_db)):
    """同步公会数据"""
    try:
        # 清空现有数据
        db.query(GuildMember).delete()
        db.commit()
        
        # 插入模拟数据
        for member_data in MOCK_GUILD_DATA:
            member = GuildMember(**member_data)
            db.add(member)
        
        db.commit()
        
        return {
            "message": "公会数据同步完成",
            "members_synced": len(MOCK_GUILD_DATA),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"同步数据失败: {str(e)}")

@router.post("/update-member/{member_id}")
async def update_member_data(
    member_id: int, 
    member_update: GuildMemberUpdate, 
    db: Session = Depends(get_db)
):
    """更新单个成员数据"""
    try:
        member = db.query(GuildMember).filter(GuildMember.id == member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="成员不存在")
        
        # 更新成员数据
        for field, value in member_update.dict(exclude_unset=True).items():
            setattr(member, field, value)
        
        member.updated_at = datetime.now()
        db.commit()
        
        return {
            "message": "成员数据更新成功",
            "member_id": member_id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新成员数据失败: {str(e)}")

@router.get("/guild-info")
async def get_guild_info():
    """获取公会基本信息"""
    return {
        "guild_name": "易骑公会",
        "realm": "艾泽拉斯",
        "faction": "Alliance",
        "total_members": len(MOCK_GUILD_DATA),
        "active_members": len([m for m in MOCK_GUILD_DATA if m["last_online_days"] <= 7]),
        "online_members": len([m for m in MOCK_GUILD_DATA if m["is_online"]]),
        "last_updated": datetime.now().isoformat()
    }

async def run_crawler_task(db: Session):
    """后台爬虫任务"""
    try:
        # 模拟爬虫延迟
        await asyncio.sleep(2)
        
        # 这里可以添加实际的数据抓取逻辑
        # 例如：调用WoW API、解析网页等
        
        print("爬虫任务执行完成")
        
    except Exception as e:
        print(f"爬虫任务执行失败: {str(e)}")

@router.post("/test-api")
async def test_external_api():
    """测试外部API连接"""
    try:
        # 模拟API调用
        async with aiohttp.ClientSession() as session:
            # 这里可以添加实际的API调用
            # async with session.get('https://api.example.com/data') as response:
            #     data = await response.json()
            
            # 返回模拟数据
            return {
                "status": "success",
                "message": "外部API连接正常",
                "data": MOCK_GUILD_DATA[:2],  # 只返回前2个成员作为示例
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API测试失败: {str(e)}")

@router.get("/crawl-history")
async def get_crawl_history():
    """获取爬虫历史记录"""
    return {
        "history": [
            {
                "id": 1,
                "started_at": "2024-01-15T10:00:00",
                "completed_at": "2024-01-15T10:05:00",
                "status": "completed",
                "members_processed": len(MOCK_GUILD_DATA),
                "errors": 0
            },
            {
                "id": 2,
                "started_at": "2024-01-14T10:00:00",
                "completed_at": "2024-01-14T10:04:30",
                "status": "completed",
                "members_processed": len(MOCK_GUILD_DATA),
                "errors": 0
            }
        ]
    } 