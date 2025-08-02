"""
配置管理模块
使用Pydantic Settings进行类型安全的配置管理
"""

from typing import List, Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings
from pathlib import Path
import os


class Settings(BaseSettings):
    """应用配置类"""
    
    # 基础配置
    app_name: str = Field(default="易骑公会官方网站", env="APP_NAME")
    app_version: str = Field(default="3.0.0", env="APP_VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    
    # 服务器配置
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    frontend_port: int = Field(default=3000, env="FRONTEND_PORT")
    
    # 数据库配置
    database_url: str = Field(
        default="sqlite:///./data/database/guild.db",
        env="DATABASE_URL"
    )
    
    # Redis配置
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    redis_password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    
    # 缓存配置
    cache_dir: str = Field(default="./data/cache", env="CACHE_DIR")
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")
    
    # 日志配置
    log_dir: str = Field(default="./data/logs", env="LOG_DIR")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # API配置
    api_base_url: str = Field(default="http://localhost:8000", env="API_BASE_URL")
    api_version: str = Field(default="v1", env="API_VERSION")
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"]
    )
    
    # 安全配置
    secret_key: str = Field(default="your_secret_key_here", env="SECRET_KEY")
    jwt_secret_key: str = Field(default="your_jwt_secret_key", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expiration: int = Field(default=3600, env="JWT_EXPIRATION")
    
    # 暴雪API配置
    blizzard_client_id: Optional[str] = Field(default=None, env="BLIZZARD_CLIENT_ID")
    blizzard_client_secret: Optional[str] = Field(default=None, env="BLIZZARD_CLIENT_SECRET")
    blizzard_region: str = Field(default="cn", env="BLIZZARD_REGION")
    
    # WarcraftLogs配置
    wcl_client_id: Optional[str] = Field(default=None, env="WCL_CLIENT_ID")
    wcl_client_secret: Optional[str] = Field(default=None, env="WCL_CLIENT_SECRET")
    
    # 文件上传配置
    upload_dir: str = Field(default="./data/uploads", env="UPLOAD_DIR")
    max_file_size: int = Field(default=10485760, env="MAX_FILE_SIZE")  # 10MB
    allowed_extensions: List[str] = Field(
        default=["jpg", "jpeg", "png", "gif", "webp"],
        env="ALLOWED_EXTENSIONS"
    )
    
    # 开发工具配置
    hot_reload: bool = Field(default=True, env="HOT_RELOAD")
    auto_migrate: bool = Field(default=True, env="AUTO_MIGRATE")
    seed_data: bool = Field(default=True, env="SEED_DATA")
    
    # 公会配置
    guild_name: str = Field(default="一起公会", env="GUILD_NAME")
    guild_realm: str = Field(default="艾泽拉斯", env="GUILD_REALM")
    guild_region: str = Field(default="cn", env="GUILD_REGION")
    guild_faction: str = Field(default="alliance", env="GUILD_FACTION")
    
    # 爬虫配置
    crawler_delay: float = Field(default=1.0, env="CRAWLER_DELAY")
    crawler_timeout: int = Field(default=30, env="CRAWLER_TIMEOUT")
    crawler_retries: int = Field(default=3, env="CRAWLER_RETRIES")
    crawler_max_workers: int = Field(default=4, env="CRAWLER_MAX_WORKERS")
    crawler_headless: bool = Field(default=True, env="CRAWLER_HEADLESS")
    
    # 统计配置
    stats_update_interval: int = Field(default=3600, env="STATS_UPDATE_INTERVAL")
    stats_cache_ttl: int = Field(default=1800, env="STATS_CACHE_TTL")
    
    # 监控配置
    prometheus_enabled: bool = Field(default=True, env="PROMETHEUS_ENABLED")
    prometheus_port: int = Field(default=9090, env="PROMETHEUS_PORT")
    
    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        """解析CORS origins配置"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        elif isinstance(v, list):
            return v
        return []
    
    @validator("allowed_extensions", pre=True)
    def parse_allowed_extensions(cls, v):
        """解析允许的文件扩展名"""
        if isinstance(v, str):
            return [ext.strip().lower() for ext in v.split(",")]
        return v
    
    @property
    def allowed_hosts(self) -> List[str]:
        """获取允许的主机列表"""
        if self.environment == "development":
            return ["*"]
        return ["localhost", "127.0.0.1", "0.0.0.0"]
    
    @property
    def is_development(self) -> bool:
        """是否为开发环境"""
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        """是否为生产环境"""
        return self.environment == "production"
    
    def ensure_directories(self):
        """确保必要的目录存在"""
        directories = [
            self.log_dir,
            self.cache_dir,
            self.upload_dir,
            Path(self.database_url.replace("sqlite:///", "")).parent
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 全局设置实例
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """获取全局设置实例"""
    global _settings
    if _settings is None:
        _settings = Settings()
        _settings.ensure_directories()
    return _settings


def reload_settings() -> Settings:
    """重新加载设置"""
    global _settings
    _settings = None
    return get_settings() 