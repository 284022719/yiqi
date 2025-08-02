#!/usr/bin/env python3
"""
调试路由注册情况
"""

from fastapi import FastAPI
from src.api.routes import api_router

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")

print("注册的路由:")
for route in app.routes:
    if hasattr(route, 'path'):
        print(f"  {route.path} - {route.methods}")
    elif hasattr(route, 'routes'):
        print(f"  子路由组: {route.prefix}")
        for sub_route in route.routes:
            if hasattr(sub_route, 'path'):
                print(f"    {sub_route.path} - {sub_route.methods}") 