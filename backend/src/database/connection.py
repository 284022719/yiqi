"""
数据库连接管理模块
提供数据库连接和初始化功能
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.config.settings import get_settings
from src.utils.logger import get_logger

logger = get_logger("database")

# 获取配置
settings = get_settings()

# 创建数据库引擎
if settings.database_url.startswith("sqlite"):
    # SQLite配置
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.debug
    )
else:
    # 其他数据库配置
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        pool_pre_ping=True
    )

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_database():
    """初始化数据库"""
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("数据库初始化完成")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise


def close_database():
    """关闭数据库连接"""
    try:
        engine.dispose()
        logger.info("数据库连接已关闭")
    except Exception as e:
        logger.error(f"关闭数据库连接失败: {e}") 