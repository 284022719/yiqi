"""
坐骑爬虫模块
负责爬取角色坐骑数据
"""

import time
import re
import urllib.parse
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.config.settings import CRAWLER_CONFIG, WEBSITE_CONFIG
from src.utils.logger import create_crawler_logger
from src.utils.browser import BrowserManager
from src.crawler.data_loader import DataLoader


class MountsCrawler:
    """坐骑爬虫"""
    
    def __init__(self, max_workers: int = None):
        """
        初始化爬虫
        
        Args:
            max_workers: 最大并发数
        """
        self.max_workers = max_workers or CRAWLER_CONFIG["max_workers"]
        self.logger = create_crawler_logger()
        self.browser_manager = BrowserManager()
        self.data_loader = DataLoader()
        
        # 线程安全的结果存储
        self.results_lock = Lock()
        self.results = []
    
    def crawl_single_character(self, role_info: Dict[str, Any], thread_id: int) -> Dict[str, Any]:
        """
        爬取单个角色的坐骑数据
        
        Args:
            role_info: 角色信息
            thread_id: 线程ID
            
        Returns:
            爬取结果
        """
        name = role_info['name']
        server = role_info['server']
        full_name = role_info['full_name']
        
        # 创建独立的浏览器实例
        driver = self.browser_manager.create_driver()
        if not driver:
            return self._create_error_result(full_name, "浏览器创建失败")
        
        try:
            # 访问官网并加载Cookie
            driver.get("https://wow.blizzard.cn/")
            self.browser_manager.load_cookies(driver)
            
            # 直接访问坐骑页面
            role_url = WEBSITE_CONFIG["character_url_template"].format(
                server=server, 
                name=urllib.parse.quote(name)
            )
            
            self.logger.info(f"[线程{thread_id}] 处理 {full_name}: {role_url}")
            
            driver.get(role_url)
            time.sleep(CRAWLER_CONFIG["wait_time"])
            
            # 检查页面是否正确加载
            current_url = driver.current_url
            if "search" in current_url:
                self.logger.warning(f"[线程{thread_id}] {full_name} 页面仍在搜索页面，重试...")
                driver.get(role_url)
                time.sleep(CRAWLER_CONFIG["wait_time"])
            
            # 等待页面加载
            try:
                WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/div[3]/div/div'))
                )
            except Exception as e:
                self.logger.error(f"[线程{thread_id}] {full_name} 页面加载超时: {e}")
                return self._create_error_result(full_name, f"页面加载超时: {e}")
            
            # 获取坐骑数量
            mount_count = self._extract_mount_count(driver, thread_id, full_name)
            
            result = {
                "name": full_name,
                "mounts": mount_count,
                "status": "成功" if mount_count != "未知" else "失败"
            }
            
            self.logger.info(f"[线程{thread_id}] {full_name} 处理完成，坐骑数量: {mount_count}")
            return result
            
        except Exception as e:
            self.logger.error(f"[线程{thread_id}] {full_name} 处理失败: {e}")
            return self._create_error_result(full_name, str(e))
        finally:
            self.browser_manager.close_driver(driver)
    
    def _extract_mount_count(self, driver: webdriver.Chrome, thread_id: int, full_name: str) -> str:
        """提取坐骑数量"""
        try:
            mount_count_elem = driver.find_element(
                By.XPATH, 
                "//*[contains(text(),'坐骑') and contains(text(),'个不同的坐骑')]"
            )
            mount_count_text = mount_count_elem.text
            match = re.search(r'(\d+)', mount_count_text)
            if match:
                return match.group(1)
        except Exception as e:
            self.logger.error(f"[线程{thread_id}] {full_name} 无法获取坐骑数量: {e}")
        
        return "未知"
    

    
    def _create_error_result(self, full_name: str, error: str) -> Dict[str, Any]:
        """创建错误结果"""
        return {
            "name": full_name,
            "mounts": "未知",
            "status": "失败",
            "error": error
        }
    
    def crawl_mounts_data(self) -> List[Dict[str, Any]]:
        """
        并发爬取坐骑数据
        
        Returns:
            爬取结果列表
        """
        role_data = self.data_loader.get_filtered_roles()
        
        if not role_data:
            self.logger.error("没有找到需要爬取的角色数据")
            return []
        
        self.logger.info("=" * 60)
        self.logger.info(f"魔兽世界坐骑数量并发爬取系统启动 (最大并发数: {self.max_workers})")
        self.logger.info("=" * 60)
        
        start_time = time.time()
        completed_count = 0
        
        # 使用线程池进行并发处理
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_role = {
                executor.submit(self.crawl_single_character, role_info, i % self.max_workers + 1): role_info 
                for i, role_info in enumerate(role_data)
            }
            
            # 收集结果
            for future in as_completed(future_to_role):
                role_info = future_to_role[future]
                try:
                    result = future.result()
                    with self.results_lock:
                        self.results.append(result)
                        completed_count += 1
                    
                    # 显示进度
                    progress = (completed_count / len(role_data)) * 100
                    self.logger.info(f"进度: {completed_count}/{len(role_data)} ({progress:.1f}%)")
                    
                except Exception as e:
                    self.logger.error(f"处理角色 {role_info['full_name']} 时发生异常: {e}")
                    with self.results_lock:
                        self.results.append(self._create_error_result(role_info['full_name'], str(e)))
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # 统计结果
        success_count = len([r for r in self.results if r['status'] == '成功'])
        failed_count = len([r for r in self.results if r['status'] == '失败'])
        
        self.logger.info("=" * 60)
        self.logger.info("并发爬取完成！")
        self.logger.info(f"总角色数：{len(role_data)}")
        self.logger.info(f"成功获取：{success_count} 个")
        self.logger.info(f"获取失败：{failed_count} 个")
        self.logger.info(f"成功率：{success_count/len(role_data)*100:.1f}%")
        self.logger.info(f"总耗时：{total_time:.1f}秒")
        self.logger.info(f"平均每个角色：{total_time/len(role_data):.1f}秒")
        self.logger.info("=" * 60)
        
        return self.results


def create_mounts_crawler(max_workers: int = None) -> MountsCrawler:
    """创建坐骑爬虫实例"""
    return MountsCrawler(max_workers) 