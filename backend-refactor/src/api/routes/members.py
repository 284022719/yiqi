"""
公会成员API路由
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import math

from src.database.connection import get_db
from src.database.models import (
    GuildMember, 
    GuildMemberCreate, 
    GuildMemberUpdate, 
    GuildMemberResponse,
    GuildMemberListResponse
)
from src.utils.exceptions import NotFoundException, DatabaseException
from src.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=GuildMemberListResponse)
async def get_members(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词（成员姓名）"),
    class_name: Optional[str] = Query(None, description="职业筛选"),
    realm_name: Optional[str] = Query(None, description="服务器筛选"),
    faction: Optional[str] = Query(None, description="阵营筛选"),
    min_level: Optional[int] = Query(None, ge=1, le=70, description="最低等级"),
    sort_by: Optional[str] = Query("name", description="排序字段"),
    sort_order: Optional[str] = Query("asc", description="排序方向（asc/desc）"),
    db: Session = Depends(get_db)
):
    """获取公会成员列表"""
    try:
        # 构建查询
        query = db.query(GuildMember)
        
        # 应用筛选条件
        if search:
            query = query.filter(GuildMember.name.ilike(f"%{search}%"))
        if class_name:
            query = query.filter(GuildMember.class_name == class_name)
        if realm_name:
            query = query.filter(GuildMember.realm_name == realm_name)
        if faction:
            query = query.filter(GuildMember.faction == faction)
        if min_level:
            query = query.filter(GuildMember.level >= min_level)
        
        # 排序
        if sort_by and hasattr(GuildMember, sort_by):
            order_column = getattr(GuildMember, sort_by)
            if sort_order.lower() == 'desc':
                query = query.order_by(order_column.desc())
            else:
                query = query.order_by(order_column.asc())
        else:
            # 默认按名称排序
            query = query.order_by(GuildMember.name.asc())
        
        # 计算总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * size
        members = query.offset(offset).limit(size).all()
        
        # 计算总页数
        pages = math.ceil(total / size)
        
        return GuildMemberListResponse(
            members=members,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
        
    except Exception as e:
        logger.error(f"获取成员列表时出错: {str(e)}")
        raise DatabaseException("获取成员列表失败")


@router.get("/{member_id}", response_model=GuildMemberResponse)
async def get_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    """获取指定成员信息"""
    try:
        member = db.query(GuildMember).filter(GuildMember.id == member_id).first()
        if not member:
            raise NotFoundException("公会成员", str(member_id))
        
        return member
        
    except NotFoundException:
        raise
    except Exception as e:
        logger.error(f"获取成员信息时出错: {str(e)}")
        raise DatabaseException("获取成员信息失败")


@router.get("/name/{name}/realm/{realm_name}", response_model=GuildMemberResponse)
async def get_member_by_name(
    name: str,
    realm_name: str,
    db: Session = Depends(get_db)
):
    """根据角色名称和服务器获取成员信息"""
    try:
        member = db.query(GuildMember).filter(
            GuildMember.name == name,
            GuildMember.realm_name == realm_name
        ).first()
        
        if not member:
            raise NotFoundException("公会成员", f"{name}@{realm_name}")
        
        return member
        
    except NotFoundException:
        raise
    except Exception as e:
        logger.error(f"根据名称获取成员时出错: {str(e)}")
        raise DatabaseException("获取成员信息失败")


@router.post("/", response_model=GuildMemberResponse, status_code=status.HTTP_201_CREATED)
async def create_member(
    member: GuildMemberCreate,
    db: Session = Depends(get_db)
):
    """创建新成员"""
    try:
        # 检查是否已存在
        existing = db.query(GuildMember).filter(
            GuildMember.name == member.name,
            GuildMember.realm_name == member.realm_name
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="成员已存在"
            )
        
        # 创建新成员
        db_member = GuildMember(**member.dict())
        db.add(db_member)
        db.commit()
        db.refresh(db_member)
        
        logger.info(f"创建新成员: {member.name}@{member.realm_name}")
        return db_member
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建成员时出错: {str(e)}")
        db.rollback()
        raise DatabaseException("创建成员失败")


@router.put("/{member_id}", response_model=GuildMemberResponse)
async def update_member(
    member_id: int,
    member_update: GuildMemberUpdate,
    db: Session = Depends(get_db)
):
    """更新成员信息"""
    try:
        db_member = db.query(GuildMember).filter(GuildMember.id == member_id).first()
        if not db_member:
            raise NotFoundException("公会成员", str(member_id))
        
        # 更新字段
        update_data = member_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_member, field, value)
        
        db.commit()
        db.refresh(db_member)
        
        logger.info(f"更新成员信息: {db_member.name}@{db_member.realm_name}")
        return db_member
        
    except NotFoundException:
        raise
    except Exception as e:
        logger.error(f"更新成员时出错: {str(e)}")
        db.rollback()
        raise DatabaseException("更新成员失败")


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    """删除成员"""
    try:
        db_member = db.query(GuildMember).filter(GuildMember.id == member_id).first()
        if not db_member:
            raise NotFoundException("公会成员", str(member_id))
        
        db.delete(db_member)
        db.commit()
        
        logger.info(f"删除成员: {db_member.name}@{db_member.realm_name}")
        
    except NotFoundException:
        raise
    except Exception as e:
        logger.error(f"删除成员时出错: {str(e)}")
        db.rollback()
        raise DatabaseException("删除成员失败")


@router.get("/classes/available")
async def get_available_classes(db: Session = Depends(get_db)):
    """获取可用的职业列表"""
    try:
        classes = db.query(GuildMember.class_name).distinct().all()
        return {
            "classes": [cls[0] for cls in classes],
            "count": len(classes)
        }
    except Exception as e:
        logger.error(f"获取职业列表时出错: {str(e)}")
        raise DatabaseException("获取职业列表失败")


@router.get("/realms/available")
async def get_available_realms(db: Session = Depends(get_db)):
    """获取可用的服务器列表"""
    try:
        realms = db.query(GuildMember.realm_name).distinct().all()
        return {
            "realms": [realm[0] for realm in realms],
            "count": len(realms)
        }
    except Exception as e:
        logger.error(f"获取服务器列表时出错: {str(e)}")
        raise DatabaseException("获取服务器列表失败") 