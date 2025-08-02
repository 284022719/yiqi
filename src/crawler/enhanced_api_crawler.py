"""
增强版API爬虫模块
集成更多暴雪官方API数据，包括装备、成就、副本进度等
"""

import time
import requests
import urllib.parse
import csv
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

from src.config.settings import CRAWLER_CONFIG, DATA_FILES
from src.utils.logger import create_crawler_logger


class EnhancedAPICrawler:
    """增强版API爬虫，集成更多游戏数据"""
    
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or CRAWLER_CONFIG["max_workers"]
        self.logger = create_crawler_logger()
        self.results_lock = Lock()
        self.results = []
        self.base_url = "https://webapi.blizzard.cn/wow-armory-server/api"
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://wow.blizzard.cn/',
            'Origin': 'https://wow.blizzard.cn'
        }
        
        self.log_dir = "logs"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"enhanced_api_crawler_{timestamp}.log")
        self._init_log_file()
    
    def _init_log_file(self):
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"增强版魔兽世界API爬虫日志 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
    
    def _write_log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        print(log_message.strip())
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message)
    
    def get_character_data(self, server: str, name: str) -> Optional[Dict[str, Any]]:
        """获取角色完整数据"""
        try:
            encoded_name = urllib.parse.quote(name)
            url = f"{self.base_url}/index?realm_slug={server}&role_name={encoded_name}"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0 and "data" in data:
                    return data["data"]
            
            return None
            
        except Exception as e:
            self._write_log(f"获取角色数据失败 {server}-{name}: {str(e)}")
            return None
    
    def get_equipment_data(self, token: str) -> Optional[Dict[str, Any]]:
        """获取装备数据"""
        try:
            url = f"{self.base_url}/do?api=equipment&token={token}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0 and "data" in data:
                    return data["data"]
            
            return None
            
        except Exception as e:
            self._write_log(f"获取装备数据失败: {str(e)}")
            return None
    
    def crawl_enhanced_data(self) -> List[Dict[str, Any]]:
        """爬取增强版数据"""
        self._write_log("开始爬取增强版游戏数据...")
        
        # 测试数据
        test_characters = [
            {"name": "快来骑我吧", "realm": "arthas", "class": "唤魔师"}
        ]
        
        results = []
        for char in test_characters:
            try:
                # 获取角色基本信息
                char_data = self.get_character_data(char["realm"], char["name"])
                if char_data:
                    # 获取装备数据
                    token = char_data.get("token")
                    if token:
                        equipment_data = self.get_equipment_data(token)
                        char_data["equipment"] = equipment_data
                    
                    results.append({
                        "name": char["name"],
                        "realm": char["realm"],
                        "class": char["class"],
                        "data": char_data,
                        "status": "success"
                    })
                    
                    self._write_log(f"成功获取角色数据: {char['name']}")
                
            except Exception as e:
                self._write_log(f"处理角色失败 {char['name']}: {str(e)}")
        
        # 保存结果
        self.save_results(results)
        return results
    
    def save_results(self, results: List[Dict[str, Any]]):
        """保存结果到文件"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            data_file = os.path.join("data", f"enhanced_api_results_{timestamp}.json")
            
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            self._write_log(f"结果已保存到: {data_file}")
            
        except Exception as e:
            self._write_log(f"保存结果失败: {str(e)}")


def create_enhanced_api_crawler(max_workers: int = None) -> EnhancedAPICrawler:
    return EnhancedAPICrawler(max_workers=max_workers)


if __name__ == "__main__":
    crawler = create_enhanced_api_crawler(max_workers=5)
    results = crawler.crawl_enhanced_data()
    print(f"爬取完成，共获取 {len(results)} 个角色的数据") 