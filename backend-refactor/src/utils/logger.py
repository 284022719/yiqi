"""
日志管理模块
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.config.settings import get_settings

settings = get_settings()


class CustomFormatter(logging.Formatter):
    """自定义日志格式化器"""
    
    # 颜色代码
    grey = "\x1b[38;21m"
    blue = "\x1b[34;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    
    # 格式字符串
    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 不同级别的格式
    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: blue + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setup_logger(
    name: str = "yiqi",
    level: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称
        level: 日志级别
        log_file: 日志文件路径
    
    Returns:
        配置好的日志记录器
    """
    # 获取日志级别
    log_level = level or settings.log_level or "INFO"
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level_map.get(log_level.upper(), logging.INFO))
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level_map.get(log_level.upper(), logging.INFO))
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)
    
    # 创建文件处理器（如果指定了日志文件）
    if log_file:
        # 确保日志目录存在
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 创建轮转文件处理器
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(level_map.get(log_level.upper(), logging.INFO))
        
        # 文件日志使用简单格式
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "yiqi") -> logging.Logger:
    """
    获取日志记录器
    
    Args:
        name: 日志记录器名称
    
    Returns:
        日志记录器实例
    """
    return logging.getLogger(name)


# 创建默认日志记录器
def get_default_logger():
    """获取默认日志记录器"""
    try:
        settings = get_settings()
        log_file = os.path.join(settings.logs_dir, "app.log") if settings.logs_dir else None
        return setup_logger("yiqi", log_file=log_file)
    except Exception:
        # 如果配置加载失败，使用控制台日志
        return setup_logger("yiqi")

default_logger = get_default_logger()


class LoggerMixin:
    """日志记录器混入类"""
    
    @property
    def logger(self) -> logging.Logger:
        """获取日志记录器"""
        return get_logger(f"{self.__class__.__module__}.{self.__class__.__name__}")


# 使用示例
if __name__ == "__main__":
    logger = get_logger("test")
    logger.debug("这是一条调试信息")
    logger.info("这是一条信息")
    logger.warning("这是一条警告")
    logger.error("这是一条错误")
    logger.critical("这是一条严重错误") 