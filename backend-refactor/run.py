#!/usr/bin/env python3
"""
FastAPI后端启动脚本
"""

import uvicorn
from src.config.settings import get_settings

if __name__ == "__main__":
    settings = get_settings()
    
    print(f"🚀 启动 {settings.app_name} v{settings.app_version}")
    print(f"📊 环境: {settings.environment}")
    print(f"🌐 服务地址: http://{settings.host}:{settings.port}")
    print(f"📚 API文档: http://{settings.host}:{settings.port}/docs")
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.hot_reload,
        log_level=settings.log_level.lower(),
        access_log=True
    ) 