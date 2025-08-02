"""
测试API路由
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_endpoint():
    """测试端点"""
    return {"message": "API路由工作正常", "status": "success"} 