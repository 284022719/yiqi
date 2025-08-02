"""
浏览器工具模块
提供浏览器实例管理和Cookie处理功能
"""

import pickle
from pathlib import Path
from typing import Optional, Dict, Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException

from src.config.settings import BROWSER_CONFIG
from src.utils.logger import get_logger


class BrowserManager:
    """浏览器管理器"""
    
    def __init__(self):
        self.logger = get_logger('browser')
        self.cookies_file = Path("cookies.pkl")
    
    def create_driver(self, headless: bool = True) -> Optional[webdriver.Chrome]:
        """
        创建Chrome浏览器实例
        
        Args:
            headless: 是否使用无头模式
            
        Returns:
            Chrome浏览器实例或None
        """
        try:
            chrome_options = Options()
            
            # 添加基本配置
            for option in BROWSER_CONFIG["chrome_options"]:
                chrome_options.add_argument(option)
            
            # 设置用户代理
            chrome_options.add_argument(f'--user-agent={BROWSER_CONFIG["user_agent"]}')
            
            # 设置窗口大小
            chrome_options.add_argument(f'--window-size={BROWSER_CONFIG["window_size"]}')
            
            # 无头模式
            if headless:
                chrome_options.add_argument('--headless')
            
            # 创建浏览器实例
            driver = webdriver.Chrome(options=chrome_options)
            
            self.logger.info("浏览器实例创建成功")
            return driver
            
        except WebDriverException as e:
            self.logger.error(f"创建浏览器实例失败: {e}")
            return None
        except Exception as e:
            self.logger.error(f"创建浏览器实例时发生未知错误: {e}")
            return None
    
    def load_cookies(self, driver: webdriver.Chrome) -> bool:
        """
        加载Cookie到浏览器
        
        Args:
            driver: 浏览器实例
            
        Returns:
            是否成功加载Cookie
        """
        try:
            if not self.cookies_file.exists():
                self.logger.warning("Cookie文件不存在，跳过Cookie加载")
                return False
            
            with open(self.cookies_file, "rb") as f:
                cookies = pickle.load(f)
            
            # 添加Cookie到浏览器
            for cookie in cookies:
                # 移除可能导致问题的字段
                if 'sameSite' in cookie:
                    del cookie['sameSite']
                if 'expiry' in cookie:
                    del cookie['expiry']
                
                try:
                    driver.add_cookie(cookie)
                except Exception as e:
                    self.logger.warning(f"添加Cookie失败: {e}")
                    continue
            
            self.logger.info(f"成功加载 {len(cookies)} 个Cookie")
            return True
            
        except FileNotFoundError:
            self.logger.warning("Cookie文件不存在，跳过Cookie加载")
            return False
        except Exception as e:
            self.logger.error(f"加载Cookie失败: {e}")
            return False
    
    def save_cookies(self, driver: webdriver.Chrome) -> bool:
        """
        保存Cookie到文件
        
        Args:
            driver: 浏览器实例
            
        Returns:
            是否成功保存Cookie
        """
        try:
            cookies = driver.get_cookies()
            
            with open(self.cookies_file, "wb") as f:
                pickle.dump(cookies, f)
            
            self.logger.info(f"成功保存 {len(cookies)} 个Cookie")
            return True
            
        except Exception as e:
            self.logger.error(f"保存Cookie失败: {e}")
            return False
    
    def close_driver(self, driver: webdriver.Chrome):
        """
        关闭浏览器实例
        
        Args:
            driver: 浏览器实例
        """
        try:
            if driver:
                driver.quit()
                self.logger.info("浏览器实例已关闭")
        except Exception as e:
            self.logger.error(f"关闭浏览器实例失败: {e}")


class BrowserContext:
    """浏览器上下文管理器"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser_manager = BrowserManager()
        self.driver = None
    
    def __enter__(self):
        """进入上下文"""
        self.driver = self.browser_manager.create_driver(self.headless)
        if self.driver:
            self.browser_manager.load_cookies(self.driver)
        return self.driver
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        if self.driver:
            self.browser_manager.save_cookies(self.driver)
            self.browser_manager.close_driver(self.driver)


def create_browser_context(headless: bool = True) -> BrowserContext:
    """
    创建浏览器上下文
    
    Args:
        headless: 是否使用无头模式
        
    Returns:
        浏览器上下文管理器
    """
    return BrowserContext(headless) 