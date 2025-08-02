"""
API爬虫模块
使用魔兽世界官方API获取角色数据
基于memberinfo.csv数据进行爬取
"""

import time
import requests
import urllib.parse
import csv
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

from src.config.settings import CRAWLER_CONFIG, DATA_FILES
from src.utils.logger import create_crawler_logger


class APICrawler:
    """API爬虫"""
    
    def __init__(self, max_workers: int = None):
        """
        初始化API爬虫
        
        Args:
            max_workers: 最大并发数
        """
        self.max_workers = max_workers or CRAWLER_CONFIG["max_workers"]
        self.logger = create_crawler_logger()
        
        # 线程安全的结果存储
        self.results_lock = Lock()
        self.results = []
        
        # API基础URL
        self.base_url = "https://webapi.blizzard.cn/wow-armory-server/api"
        
        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://wow.blizzard.cn/',
            'Origin': 'https://wow.blizzard.cn'
        }
        
        # 创建日志目录
        self.log_dir = "logs"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # 日志文件路径
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"api_crawler_{timestamp}.log")
        
        # 初始化日志文件
        self._init_log_file()
    
    def _init_log_file(self):
        """初始化日志文件"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"魔兽世界API爬虫日志 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
    
    def _write_log(self, message: str):
        """写入日志到文件"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        # 同时输出到控制台和文件
        print(log_message.strip())
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message)
    
    def load_memberinfo_data(self) -> List[Dict[str, Any]]:
        """
        加载memberinfo.csv数据
        
        Returns:
            角色数据列表
        """
        try:
            data = []
            memberinfo_path = DATA_FILES.get("memberinfo")
            
            if not memberinfo_path or not os.path.exists(memberinfo_path):
                self._write_log(f"错误: 找不到memberinfo.csv文件: {memberinfo_path}")
                return []
            
            with open(memberinfo_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # 过滤80级角色
                    try:
                        level = int(row.get('Level', 0))
                        if level == 80:
                            data.append(row)
                    except (ValueError, TypeError):
                        continue
            
            self._write_log(f"成功加载 {len(data)} 个80级角色数据")
            return data
            
        except Exception as e:
            self._write_log(f"加载memberinfo.csv数据失败: {e}")
            return []
    
    def get_server_slug(self, realm_name: str) -> str:
        """
        将中文服务器名转换为英文slug
        
        Args:
            realm_name: 中文服务器名
            
        Returns:
            英文服务器slug
        """
        # 服务器名称映射（可以根据需要扩展）
        server_mapping = {
            '阿尔萨斯': 'arthas',
            '死亡之翼': 'deathwing',
            '白银之手': 'silver-hand',
            '风暴峭壁': 'stormrage',
            '红龙军团': 'red-dragon',
            '祖达克': 'zul-drak',
            '无尽之海': 'endless-sea',
            '布兰卡德': 'blackhand',
            '地狱之石': 'hellscream',
            '安苏': 'anshe',
            '加里索斯': 'garithos',
            '斯克提斯': 'skettis',
            '冰风岗': 'icecrown',
            '格瑞姆巴托': 'grim-batol',
            '塞拉摩': 'theramore',
            '巴瑟拉斯': 'barthilas',
            '伊利丹': 'illidan',
            '苏拉玛': 'suramar',
            '冬泉谷': 'winterspring',
            '主宰之剑': 'dominion',
            '罗宁': 'rhonin',
            '莱索恩': 'leshon',
            '瓦里安': 'varian'
        }
        
        return server_mapping.get(realm_name, realm_name.lower().replace(' ', '-'))
    
    def get_character_token(self, server: str, name: str) -> Optional[str]:
        """
        获取角色token
        
        Args:
            server: 服务器英文名
            name: 角色名
            
        Returns:
            角色token或None
        """
        try:
            url = f"{self.base_url}/index"
            params = {
                'realm_slug': server,
                'role_name': name
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0 and data.get('data'):
                    return data['data'].get('token')
            
            self._write_log(f"警告: 获取角色token失败: {server}-{name}")
            return None
            
        except Exception as e:
            self._write_log(f"错误: 获取角色token异常: {server}-{name}, {e}")
            return None
    
    def get_mounts_data(self, token: str, faction: str = "HORDE") -> Optional[Dict[str, Any]]:
        """
        获取坐骑数据
        
        Args:
            token: 角色token
            faction: 阵营 (HORDE/ALLIANCE)
            
        Returns:
            坐骑数据或None
        """
        try:
            url = f"{self.base_url}/do"
            params = {
                'api': 'mounts',
                'token': token,
                'attr': faction
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    return data.get('data', {})
            
            return None
            
        except Exception as e:
            self._write_log(f"错误: 获取坐骑数据异常: {e}")
            return None
    
    def get_mythic_data(self, token: str) -> Optional[Dict[str, Any]]:
        """
        获取Mythic+数据
        
        Args:
            token: 角色token
            
        Returns:
            Mythic+数据或None
        """
        try:
            url = f"{self.base_url}/do"
            params = {
                'api': 'mythic_keystone_season',
                'token': token
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    return data.get('data', {})
            
            return None
            
        except Exception as e:
            self._write_log(f"错误: 获取Mythic+数据异常: {e}")
            return None
    
    def crawl_single_character(self, role_info: Dict[str, Any], thread_id: int) -> Dict[str, Any]:
        """
        爬取单个角色的数据
        
        Args:
            role_info: 角色信息
            thread_id: 线程ID
            
        Returns:
            爬取结果
        """
        name = role_info['Name']
        realm_name = role_info['Realm Name']
        faction = role_info['Faction']
        full_name = f"{name}-{realm_name}"
        
        self._write_log(f"[线程{thread_id}] 处理 {full_name}")
        
        try:
            # 1. 转换服务器名
            server_slug = self.get_server_slug(realm_name)
            
            # 2. 获取角色token
            token = self.get_character_token(server_slug, name)
            if not token:
                return self._create_error_result(full_name, "无法获取角色token")
            
            # 3. 获取坐骑数据
            mounts_data = self.get_mounts_data(token, faction)
            
            # 4. 获取Mythic+数据
            mythic_data = self.get_mythic_data(token)
            
            # 5. 提取坐骑数量
            mount_count = "未知"
            if mounts_data:
                mount_count = str(mounts_data.get('now', '未知'))
            
            # 6. 提取Mythic+评分
            mythic_score = "未知"
            if mythic_data and mythic_data.get('mythic_rating'):
                mythic_score = str(int(mythic_data['mythic_rating']['rating']))
            
            result = {
                "name": full_name,
                "character_name": name,
                "realm": realm_name,
                "faction": faction,
                "mounts": mount_count,
                "mythic_score": mythic_score,
                "status": "成功",
                "token": token,
                "mounts_data": mounts_data,
                "mythic_data": mythic_data
            }
            
            self._write_log(f"[线程{thread_id}] {full_name} 完成: {mount_count} 坐骑, {mythic_score} 评分")
            return result
            
        except Exception as e:
            self._write_log(f"[线程{thread_id}] {full_name} 处理异常: {e}")
            return self._create_error_result(full_name, str(e))
    
    def _create_error_result(self, full_name: str, error: str) -> Dict[str, Any]:
        """创建错误结果"""
        return {
            "name": full_name,
            "mounts": "未知",
            "mythic_score": "未知",
            "status": "失败",
            "error": error
        }
    
    def save_results(self, results: List[Dict[str, Any]]):
        """
        保存爬取结果到CSV文件
        
        Args:
            results: 爬取结果列表
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.log_dir, f"api_crawler_results_{timestamp}.csv")
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                if results:
                    fieldnames = results[0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(results)
            
            self._write_log(f"结果已保存到: {output_file}")
            
        except Exception as e:
            self._write_log(f"保存结果失败: {e}")
    
    def crawl_mounts_data(self) -> List[Dict[str, Any]]:
        """
        并发爬取坐骑数据
        
        Returns:
            爬取结果列表
        """
        # 加载memberinfo.csv数据
        role_data = self.load_memberinfo_data()
        
        if not role_data:
            self._write_log("错误: 没有找到需要爬取的角色数据")
            return []
        
        self._write_log("=" * 80)
        self._write_log(f"魔兽世界API坐骑数据爬取系统启动 (最大并发数: {self.max_workers})")
        self._write_log(f"数据源: memberinfo.csv")
        self._write_log(f"日志文件: {self.log_file}")
        self._write_log("=" * 80)
        
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
                    self._write_log(f"进度: {completed_count}/{len(role_data)} ({progress:.1f}%)")
                    
                except Exception as e:
                    self._write_log(f"处理角色 {role_info['Name']}-{role_info['Realm Name']} 时发生异常: {e}")
                    with self.results_lock:
                        self.results.append(self._create_error_result(f"{role_info['Name']}-{role_info['Realm Name']}", str(e)))
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # 统计结果
        success_count = len([r for r in self.results if r['status'] == '成功'])
        failed_count = len([r for r in self.results if r['status'] == '失败'])
        
        self._write_log("=" * 80)
        self._write_log("API爬取完成！")
        self._write_log(f"总角色数：{len(role_data)}")
        self._write_log(f"成功获取：{success_count} 个")
        self._write_log(f"获取失败：{failed_count} 个")
        self._write_log(f"成功率：{success_count/len(role_data)*100:.1f}%")
        self._write_log(f"总耗时：{total_time:.1f}秒")
        self._write_log(f"平均每个角色：{total_time/len(role_data):.1f}秒")
        self._write_log("=" * 80)
        
        # 保存结果
        self.save_results(self.results)
        
        return self.results


def create_api_crawler(max_workers: int = None) -> APICrawler:
    """创建API爬虫实例"""
    return APICrawler(max_workers) 