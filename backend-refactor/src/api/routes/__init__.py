"""
API路由模块
"""

from fastapi import APIRouter
from .members import router as members_router
from .statistics import router as statistics_router
from .search import router as search_router
from .crawler import router as crawler_router
from .test import router as test_router

# 创建主路由
api_router = APIRouter()

# 注册子路由
api_router.include_router(
    members_router,
    prefix="/members",
    tags=["公会成员"]
)

api_router.include_router(
    statistics_router,
    prefix="/statistics",
    tags=["统计数据"]
)

api_router.include_router(
    search_router,
    prefix="/search",
    tags=["搜索功能"]
)

api_router.include_router(
    crawler_router,
    prefix="/crawler",
    tags=["数据爬虫"]
)

api_router.include_router(
    test_router,
    prefix="/test",
    tags=["测试"]
) 