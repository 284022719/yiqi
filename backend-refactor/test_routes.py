#!/usr/bin/env python3
"""
测试路由注册
"""

import uvicorn
from fastapi import FastAPI
from src.api.routes import api_router

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")

print("注册的路由:")
for route in app.routes:
    if hasattr(route, 'path'):
        print(f"  {route.path} - {route.methods}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001) 