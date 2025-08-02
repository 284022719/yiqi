"""
日志工具模块
提供统一的日志记录功能
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.config.settings import LOGS_DIR, LOGGING_CONFIG


class Logger:
    """统一的日志记录器"""
    
    def __init__(self, name: str, log_file: Optional[str] = None):
        """
        初始化日志记录器
        
        Args:
            name: 日志记录器名称
            log_file: 日志文件名（可选）
        """
        self.name = name
        self.logger = logging.getLogger(name)
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            self._setup_logger(log_file)
    
    def _setup_logger(self, log_file: Optional[str] = None):
        """设置日志记录器"""
        self.logger.setLevel(getattr(logging, LOGGING_CONFIG["level"]))
        
        # 创建格式化器
        formatter = logging.Formatter(LOGGING_CONFIG["file_format"])
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 文件处理器
        if log_file:
            log_path = LOGS_DIR / log_file
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        """记录信息日志"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """记录警告日志"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """记录错误日志"""
        self.logger.error(message)
    
    def debug(self, message: str):
        """记录调试日志"""
        self.logger.debug(message)
    
    def critical(self, message: str):
        """记录严重错误日志"""
        self.logger.critical(message)


def get_logger(name: str, log_file: Optional[str] = None) -> Logger:
    """
    获取日志记录器
    
    Args:
        name: 日志记录器名称
        log_file: 日志文件名（可选）
    
    Returns:
        Logger实例
    """
    return Logger(name, log_file)


def create_crawler_logger() -> Logger:
    """创建爬虫专用日志记录器"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'mounts_crawler_{timestamp}.log'
    return get_logger('crawler', log_file)


def create_stats_logger() -> Logger:
    """创建统计专用日志记录器"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'stats_generator_{timestamp}.log'
    return get_logger('stats', log_file) 