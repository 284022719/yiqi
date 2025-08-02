"""
配置管理模块
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path


class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用基本信息
    app_name: str = Field(default="易骑公会官方网站", description="应用名称")
    app_version: str = Field(default="3.0.0", description="应用版本")
    api_version: str = Field(default="v1", description="API版本")
    
    # 服务器配置
    host: str = Field(default="127.0.0.1", description="服务器主机")
    port: int = Field(default=8000, description="服务器端口")
    debug: bool = Field(default=True, description="调试模式")
    hot_reload: bool = Field(default=True, description="热重载")
    
    # 环境配置
    environment: str = Field(default="development", description="运行环境")
    log_level: str = Field(default="INFO", description="日志级别")
    
    # 数据库配置
    database_url: str = Field(
        default="sqlite:///./data/guild_members.db",
        description="数据库连接URL"
    )
    database_echo: bool = Field(default=False, description="数据库SQL回显")
    
    # CORS配置
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        description="允许的CORS源"
    )
    allowed_hosts: List[str] = Field(
        default=["*"],
        description="允许的主机"
    )
    
    # 安全配置
    secret_key: str = Field(
        default="your-secret-key-here",
        description="JWT密钥"
    )
    algorithm: str = Field(default="HS256", description="JWT算法")
    access_token_expire_minutes: int = Field(
        default=30,
        description="访问令牌过期时间(分钟)"
    )
    
    # 文件上传配置
    upload_dir: str = Field(default="./data/uploads", description="上传目录")
    max_file_size: int = Field(default=10 * 1024 * 1024, description="最大文件大小(字节)")
    allowed_file_types: List[str] = Field(
        default=[".jpg", ".jpeg", ".png", ".gif", ".webp"],
        description="允许的文件类型"
    )
    
    # 缓存配置
    cache_dir: str = Field(default="./cache", description="缓存目录")
    cache_expire_hours: int = Field(default=12, description="缓存过期时间(小时)")
    
    # 日志配置
    logs_dir: str = Field(default="./logs", description="日志目录")
    
    # 爬虫配置
    crawler_timeout: int = Field(default=15, description="爬虫超时时间(秒)")
    crawler_max_retries: int = Field(default=3, description="最大重试次数")
    crawler_delay: float = Field(default=1.0, description="请求间隔(秒)")
    
    # 暴雪API配置
    blizzard_client_id: Optional[str] = Field(default=None, description="暴雪客户端ID")
    blizzard_client_secret: Optional[str] = Field(default=None, description="暴雪客户端密钥")
    blizzard_region: str = Field(default="cn", description="暴雪区域")
    
    # Raider.io API配置
    raiderio_api_url: str = Field(
        default="https://raider.io/api/v1",
        description="Raider.io API地址"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 全局配置实例
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """获取配置实例"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def create_directories():
    """创建必要的目录"""
    settings = get_settings()
    
    directories = [
        Path(settings.upload_dir),
        Path(settings.cache_dir),
        Path("./data"),
        Path("./logs"),
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True) 