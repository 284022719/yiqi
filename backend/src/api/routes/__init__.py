"""
API路由模块
统一管理所有API路由
"""

from fastapi import APIRouter

# 创建主路由
api_router = APIRouter()

# 导入子路由（稍后创建）
# from .guild_members import router as guild_members_router
# from .statistics import router as statistics_router
# from .crawler import router as crawler_router
# from .health import router as health_router

# 注册子路由
# api_router.include_router(
#     guild_members_router,
#     prefix="/guild-members",
#     tags=["公会成员"]
# )

# api_router.include_router(
#     statistics_router,
#     prefix="/statistics",
#     tags=["统计数据"]
# )

# api_router.include_router(
#     crawler_router,
#     prefix="/crawler",
#     tags=["数据爬取"]
# )

# api_router.include_router(
#     health_router,
#     prefix="/health",
#     tags=["健康检查"]
# )

# 临时路由用于测试
@api_router.get("/test")
async def test_endpoint():
    """测试端点"""
    return {"message": "API路由工作正常", "status": "success"} 