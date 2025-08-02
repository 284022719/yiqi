"""
数据库连接管理
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
from typing import Generator
import logging

from src.config.settings import get_settings

logger = logging.getLogger(__name__)

# 创建基础模型类
Base = declarative_base()

# 全局变量
_engine = None
_SessionLocal = None


def get_database_url() -> str:
    """获取数据库连接URL"""
    settings = get_settings()
    return settings.database_url


def create_database_engine():
    """创建数据库引擎"""
    global _engine
    
    if _engine is not None:
        return _engine
    
    settings = get_settings()
    database_url = get_database_url()
    
    # SQLite特殊配置
    if database_url.startswith("sqlite"):
        _engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=settings.database_echo
        )
    else:
        _engine = create_engine(
            database_url,
            echo=settings.database_echo
        )
    
    logger.info(f"数据库引擎创建成功: {database_url}")
    return _engine


def get_database() -> Session:
    """获取数据库会话"""
    global _SessionLocal
    
    if _SessionLocal is None:
        engine = create_database_engine()
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    return _SessionLocal()


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """数据库会话上下文管理器"""
    db = get_database()
    try:
        yield db
    except Exception as e:
        logger.error(f"数据库操作出错: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


async def init_database():
    """初始化数据库"""
    try:
        engine = create_database_engine()
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        
        logger.info("数据库初始化完成")
        
        # 检查是否需要导入现有数据
        await check_and_import_existing_data()
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        raise


async def check_and_import_existing_data():
    """检查并导入现有数据"""
    try:
        from .models import GuildMember
        
        with get_db() as db:
            # 检查是否有现有数据
            existing_count = db.query(GuildMember).count()
            
            if existing_count == 0:
                logger.info("数据库为空，准备导入现有数据...")
                await import_existing_data()
            else:
                logger.info(f"数据库已有 {existing_count} 条记录")
                
    except Exception as e:
        logger.error(f"检查现有数据时出错: {str(e)}")


async def import_existing_data():
    """导入现有数据"""
    try:
        import sqlite3
        import json
        from pathlib import Path
        
        # 检查现有数据库文件
        old_db_path = Path("../data/database/guild_members.db")
        
        if old_db_path.exists():
            logger.info("发现现有数据库文件，开始导入...")
            
            # 连接现有数据库
            old_conn = sqlite3.connect(str(old_db_path))
            old_cursor = old_conn.cursor()
            
            # 获取所有数据
            old_cursor.execute("SELECT * FROM guild_members")
            rows = old_cursor.fetchall()
            
            # 获取列名
            columns = [description[0] for description in old_cursor.description]
            
            # 导入到新数据库
            from .models import GuildMember
            
            with get_db() as db:
                for row in rows:
                    try:
                        # 创建数据字典，处理字段映射
                        data_dict = {}
                        
                        # 字段映射：旧数据库字段名 -> 新模型字段名
                        field_mapping = {
                            'class': 'class_name',
                            'race': 'race_name',
                            'mythic_score': 'mythic_plus_score',
                            'rank': 'guild_rank'
                        }
                        
                        for i, column in enumerate(columns):
                            # 获取新模型中的字段名
                            new_column = field_mapping.get(column, column)
                            
                            if hasattr(GuildMember, new_column):
                                value = row[i]
                                
                                # 处理datetime字段的转换
                                if new_column in ['created_at', 'updated_at'] and value is not None:
                                    try:
                                        if isinstance(value, str):
                                            # 尝试解析常见的datetime字符串格式
                                            from datetime import datetime
                                            import re
                                            
                                            # 移除时区信息并解析
                                            value_str = str(value).split('.')[0]  # 移除微秒
                                            value_str = re.sub(r'[+-]\d{2}:\d{2}$', '', value_str)  # 移除时区
                                            
                                            # 尝试多种格式
                                            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d']:
                                                try:
                                                    value = datetime.strptime(value_str, fmt)
                                                    break
                                                except ValueError:
                                                    continue
                                            else:
                                                # 如果所有格式都失败，使用当前时间
                                                value = datetime.now()
                                        elif not isinstance(value, datetime):
                                            value = datetime.now()
                                    except Exception as e:
                                        logger.warning(f"日期转换失败，使用当前时间: {str(e)}")
                                        value = datetime.now()
                                
                                # 处理空值，为必填字段提供默认值
                                if value is None:
                                    if new_column in ['class_name', 'race_name']:
                                        value = '未知'
                                    elif new_column in ['faction']:
                                        value = 'Horde'  # 默认阵营
                                    elif new_column in ['guild_rank']:
                                        value = '成员'
                                
                                data_dict[new_column] = value
                        
                        # 创建新的GuildMember对象
                        member = GuildMember(**data_dict)
                        db.add(member)
                        
                    except Exception as e:
                        logger.warning(f"跳过无效记录: {str(e)}")
                        continue
                
                db.commit()
                logger.info(f"成功导入 {len(rows)} 条记录")
            
            old_conn.close()
        else:
            logger.info("未发现现有数据库文件")
            
    except Exception as e:
        logger.error(f"导入现有数据时出错: {str(e)}")


def close_database():
    """关闭数据库连接"""
    global _engine
    if _engine is not None:
        _engine.dispose()
        logger.info("数据库连接已关闭") 