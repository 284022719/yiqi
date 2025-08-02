"""
改进的API爬虫 - 使用server_mapping.json
"""

import time
import requests
import csv
import os
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

class APICrawler:
    def __init__(self, max_workers=5):
        self.max_workers = max_workers
        self.results_lock = Lock()
        self.results = []
        
        # API基础URL
        self.base_url = "https://webapi.blizzard.cn/wow-armory-server/api"
        
        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
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
        
        # 加载服务器映射
        self.server_mapping = self.load_server_mapping()
    
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
    
    def load_server_mapping(self):
        """加载服务器名称映射"""
        try:
            mapping_file = "data/server_mapping.json"
            if os.path.exists(mapping_file):
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    mapping = json.load(f)
                self._write_log(f"成功加载服务器映射，共 {len(mapping)} 个服务器")
                return mapping
            else:
                self._write_log(f"警告: 服务器映射文件不存在: {mapping_file}")
                return {}
        except Exception as e:
            self._write_log(f"加载服务器映射失败: {e}")
            return {}
    
    def load_memberinfo_data(self):
        """加载memberinfo.csv数据"""
        try:
            data = []
            with open('data/memberinfo.csv', 'r', encoding='utf-8') as f:
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
        """将中文服务器名转换为英文slug"""
        # 优先使用server_mapping.json中的映射
        if realm_name in self.server_mapping:
            return self.server_mapping[realm_name]
        
        # 如果没有找到映射，使用默认转换规则
        self._write_log(f"警告: 未找到服务器映射: {realm_name}，使用默认转换")
        return realm_name.lower().replace(' ', '-')
    
    def get_character_token(self, server: str, name: str):
        """获取角色token"""
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
            
            return None
            
        except Exception as e:
            self._write_log(f"获取角色token异常: {server}-{name}, {e}")
            return None
    
    def get_mounts_data(self, token: str, faction: str = "HORDE"):
        """获取坐骑数据"""
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
            self._write_log(f"获取坐骑数据异常: {e}")
            return None
    
    def get_mythic_data(self, token: str):
        """获取Mythic+数据"""
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
            self._write_log(f"获取Mythic+数据异常: {e}")
            return None
    
    def crawl_single_character(self, role_info, thread_id: int):
        """爬取单个角色的数据"""
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
                return {
                    "name": full_name,
                    "character_name": name,
                    "realm": realm_name,
                    "faction": faction,
                    "mounts": "未知",
                    "mythic_score": "未知",
                    "status": "失败",
                    "error": "无法获取角色token"
                }
            
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
                "status": "成功"
            }
            
            self._write_log(f"[线程{thread_id}] {full_name} 完成: {mount_count} 坐骑, {mythic_score} 评分")
            return result
            
        except Exception as e:
            self._write_log(f"[线程{thread_id}] {full_name} 处理异常: {e}")
            return {
                "name": full_name,
                "character_name": name,
                "realm": realm_name,
                "faction": faction,
                "mounts": "未知",
                "mythic_score": "未知",
                "status": "失败",
                "error": str(e)
            }
    
    def save_results(self, results):
        """保存爬取结果到CSV文件"""
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
    
    def crawl_mounts_data(self):
        """并发爬取坐骑数据"""
        # 加载memberinfo.csv数据
        role_data = self.load_memberinfo_data()
        
        if not role_data:
            self._write_log("错误: 没有找到需要爬取的角色数据")
            return []
        
        self._write_log("=" * 80)
        self._write_log(f"魔兽世界API坐骑数据爬取系统启动 (最大并发数: {self.max_workers})")
        self._write_log(f"数据源: memberinfo.csv")
        self._write_log(f"服务器映射: {len(self.server_mapping)} 个服务器")
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
                        self.results.append({
                            "name": f"{role_info['Name']}-{role_info['Realm Name']}",
                            "character_name": role_info['Name'],
                            "realm": role_info['Realm Name'],
                            "faction": role_info['Faction'],
                            "mounts": "未知",
                            "mythic_score": "未知",
                            "status": "失败",
                            "error": str(e)
                        })
        
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

if __name__ == "__main__":
    # 创建爬虫实例并开始爬取
    crawler = APICrawler(max_workers=5)
    results = crawler.crawl_mounts_data()
    print(f"爬取完成，共处理 {len(results)} 个角色") 