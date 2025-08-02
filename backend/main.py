#!/usr/bin/env python3
"""
易骑公会官方网站 - 后端服务
现代化重构版本
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging
from pathlib import Path

# 导入配置和路由
from src.config.settings import get_settings
from src.api.routes import api_router
from src.utils.logger import setup_logging
from src.database.connection import init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    settings = get_settings()
    setup_logging(settings.log_level)
    
    # 初始化数据库
    await init_database()
    
    logging.info(f"🚀 {settings.app_name} v{settings.app_version} 启动成功")
    logging.info(f"📊 环境: {settings.environment}")
    logging.info(f"🌐 服务地址: http://{settings.host}:{settings.port}")
    
    yield
    
    # 关闭时执行
    logging.info("🛑 应用正在关闭...")


def create_app() -> FastAPI:
    """创建FastAPI应用"""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="易骑公会官方网站后端API服务",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan
    )
    
    # 中间件配置
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.allowed_hosts
    )
    
    # 路由配置
    app.include_router(api_router, prefix=f"/api/{settings.api_version}")
    
    # 健康检查
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "app": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment
        }
    
    # 根路径
    @app.get("/")
    async def root():
        return {
            "message": f"欢迎使用 {settings.app_name}",
            "version": settings.app_version,
            "docs": "/docs" if settings.debug else "文档已禁用"
        }
    
    return app


app = create_app()


if __name__ == "__main__":
    settings = get_settings()
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.hot_reload,
        log_level=settings.log_level.lower(),
        access_log=True
    ) 