"""
日志管理模块
提供统一的日志配置和管理
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from src.config.settings import get_settings


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> None:
    """设置日志配置"""
    settings = get_settings()
    
    # 创建日志目录
    log_dir = Path(settings.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 设置日志级别
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # 创建格式化器
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # 清除现有的处理器
    root_logger.handlers.clear()
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 文件处理器
    if log_file is None:
        log_file = log_dir / "app.log"
    
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # 设置第三方库的日志级别
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """获取指定名称的日志记录器"""
    return logging.getLogger(name)


# 预定义的日志记录器
app_logger = get_logger("app")
api_logger = get_logger("api")
db_logger = get_logger("database")
crawler_logger = get_logger("crawler")
stats_logger = get_logger("statistics") 