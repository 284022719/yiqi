import pytest
import asyncio
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from src.database.connection import get_db, Base
from src.config.settings import get_settings

# 测试设置
settings = get_settings()

# 创建内存数据库用于测试
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def db_engine():
    """创建测试数据库引擎"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    yield engine
    # 清理
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db_engine):
    """创建数据库会话"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session) -> Generator:
    """创建测试客户端"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_guild_member_data():
    """示例公会成员数据"""
    return {
        "name": "测试玩家",
        "realm": "艾泽拉斯",
        "class_name": "战士",
        "level": 70,
        "faction": "联盟",
        "guild_rank": "成员",
        "achievement_points": 15000,
        "item_level": 450,
        "mythic_plus_score": 2500,
        "online_status": True
    }


@pytest.fixture
def sample_guild_members_data():
    """多个示例公会成员数据"""
    return [
        {
            "name": "战士玩家",
            "realm": "艾泽拉斯",
            "class_name": "战士",
            "level": 70,
            "faction": "联盟",
            "guild_rank": "成员",
            "achievement_points": 15000,
            "item_level": 450,
            "mythic_plus_score": 2500,
            "online_status": True
        },
        {
            "name": "法师玩家",
            "realm": "艾泽拉斯",
            "class_name": "法师",
            "level": 70,
            "faction": "联盟",
            "guild_rank": "官员",
            "achievement_points": 20000,
            "item_level": 460,
            "mythic_plus_score": 3000,
            "online_status": False
        },
        {
            "name": "猎人玩家",
            "realm": "艾泽拉斯",
            "class_name": "猎人",
            "level": 70,
            "faction": "联盟",
            "guild_rank": "成员",
            "achievement_points": 12000,
            "item_level": 440,
            "mythic_plus_score": 2000,
            "online_status": True
        }
    ] 