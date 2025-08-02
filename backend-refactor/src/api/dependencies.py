"""
API依赖注入模块
"""

from typing import Generator
from sqlalchemy.orm import Session
from ..database.connection import get_db as get_database_session


def get_db() -> Generator[Session, None, None]:
    """获取数据库会话依赖"""
    with get_database_session() as db:
        yield db 