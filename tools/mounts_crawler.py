#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
魔兽世界坐骑数据爬虫
爬取数据库中每个角色的坐骑数量信息
"""

import os
import sys
import time
import json
import requests
import sqlite3
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, List, Optional, Any
from database_manager import GuildDatabaseManager
from config import config
from paths import resolve_db_path

class MountsCrawler:
    def __init__(self, db_path: str = None):
        """初始化坐骑爬虫"""
        self.db_path = str(resolve_db_path(db_path or config.get("database.path")))
        self.db_manager = GuildDatabaseManager(self.db_path)
        self.setup_logging()
        
        # API配置
        self.base_url = config.get("api.base_url")
        self.headers = config.get("api.headers")
        
        # 爬取配置
        self.delay_between_requests = config.get("crawler.delay_between_requests", 2)
        self.max_retries = config.get("api.max_retries", 3)
        self.timeout = config.get("api.timeout", 30)
        self.max_concurrent = config.get("crawler.max_concurrent", 12)  # 并发数
        
        # 线程锁
        self.lock = threading.Lock()
        
        # 统计信息
        self.stats = {
            "total_characters": 0,
            "successful_crawls": 0,
            "failed_crawls": 0,
            "start_time": None,
            "end_time": None
        }
    
    def setup_logging(self):
        """设置日志记录"""
        # 创建logs目录
        os.makedirs("logs", exist_ok=True)
        
        log_level = getattr(logging, config.get("logging.level", "INFO"))
        log_file = config.get("logging.file", "logs/mounts_crawler.log")
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_character_token(self, character_name: str, realm_slug: str) -> Optional[str]:
        """获取角色的访问令牌"""
        return config.get_token(character_name, realm_slug)
    
    def get_mounts_data(self, character_name: str, realm_slug: str, faction: str) -> Optional[Dict[str, Any]]:
        """获取角色的坐骑数据"""
        try:
            # 获取访问令牌
            token = self.get_character_token(character_name, realm_slug)
            if not token:
                self.logger.error(f"无法获取角色 {character_name} 的访问令牌")
                return None
            
            # 构建请求参数
            params = {
                "api": "mounts",
                "token": token,
                "attr": faction.upper(),
                "character": character_name,
                "realm": realm_slug
            }
            
            # 记录请求信息用于调试
            self.logger.debug(f"请求参数: {params}")
            
            # 发送请求
            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("code") == 0:
                    mounts_data = data.get("data", {})
                    now_count = mounts_data.get('now', 0)
                    total_count = mounts_data.get('total', 0)
                    
                    # 检查数据是否合理
                    if now_count == 0 and total_count == 0:
                        self.logger.warning(f"角色 {character_name} 返回了空的坐骑数据，可能API不支持该角色")
                        return None
                    
                    self.logger.info(f"成功获取角色 {character_name} 的坐骑数据: {now_count}/{total_count}")
                    
                    # 添加角色信息到返回数据中
                    mounts_data['character_name'] = character_name
                    mounts_data['realm_slug'] = realm_slug
                    mounts_data['faction'] = faction
                    
                    return mounts_data
                else:
                    error_msg = data.get('message', '未知错误')
                    self.logger.error(f"API返回错误 (角色 {character_name}): {error_msg}")
                    
                    # 如果是服务繁忙错误，记录详细信息
                    if "繁忙" in error_msg or "busy" in error_msg.lower():
                        self.logger.warning(f"API服务繁忙，角色 {character_name} 的请求可能需要重试")
                    
                    return None
            else:
                self.logger.error(f"HTTP请求失败 (角色 {character_name}): {response.status_code}")
                self.logger.debug(f"响应内容: {response.text[:200]}")
                return None
                
        except requests.exceptions.Timeout:
            self.logger.error(f"请求超时: {character_name}")
            return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"请求异常: {character_name} - {e}")
            return None
        except Exception as e:
            self.logger.error(f"获取坐骑数据失败: {character_name} - {e}")
            return None
    
    def crawl_character_mounts(self, character: Dict[str, Any]) -> bool:
        """爬取单个角色的坐骑数据"""
        character_name = character.get("name")
        realm_slug = character.get("realm_slug")
        faction = character.get("faction")
        
        if not all([character_name, realm_slug, faction]):
            self.logger.error(f"角色信息不完整: {character}")
            return False
        
        # 获取坐骑数据
        mounts_data = self.get_mounts_data(character_name, realm_slug, faction)
        
        if mounts_data:
            # 更新数据库（使用线程锁保护）
            with self.lock:
                success = self.db_manager.update_character_mounts(character_name, realm_slug, mounts_data)
                if success:
                    self.stats["successful_crawls"] += 1
                    return True
                else:
                    self.stats["failed_crawls"] += 1
                    return False
        else:
            with self.lock:
                self.stats["failed_crawls"] += 1
            return False
    
    def crawl_all_characters(self) -> bool:
        """爬取所有角色的坐骑数据（并发版本）"""
        self.stats["start_time"] = datetime.now()
        self.logger.info("开始爬取所有角色的坐骑数据...")
        
        # 获取所有角色
        characters = self.db_manager.get_all_characters()
        self.stats["total_characters"] = len(characters)
        
        if not characters:
            self.logger.error("数据库中没有找到角色数据")
            return False
        
        self.logger.info(f"找到 {len(characters)} 个角色，使用 {self.max_concurrent} 个并发线程开始爬取...")
        
        # 使用线程池进行并发爬取
        completed_count = 0
        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            # 提交所有任务
            future_to_character = {
                executor.submit(self.crawl_character_mounts, character): character 
                for character in characters
            }
            
            # 处理完成的任务
            for future in as_completed(future_to_character):
                character = future_to_character[future]
                completed_count += 1
                
                try:
                    success = future.result()
                    character_name = character.get('name', 'Unknown')
                    
                    # 显示进度
                    progress = (completed_count / len(characters)) * 100
                    status = "✅" if success else "❌"
                    self.logger.info(f"{status} 进度: {progress:.1f}% ({completed_count}/{len(characters)}) - {character_name}")
                    
                except Exception as e:
                    self.logger.error(f"处理角色 {character.get('name', 'Unknown')} 时发生异常: {e}")
                    with self.lock:
                        self.stats["failed_crawls"] += 1
        
        self.stats["end_time"] = datetime.now()
        self.logger.info("坐骑数据爬取完成！")
        self.print_statistics()
        
        return True
    
    def print_statistics(self):
        """打印统计信息"""
        duration = self.stats["end_time"] - self.stats["start_time"]
        
        print("\n" + "="*60)
        print("坐骑数据爬取统计")
        print("="*60)
        print(f"总角色数: {self.stats['total_characters']}")
        print(f"成功爬取: {self.stats['successful_crawls']}")
        print(f"失败爬取: {self.stats['failed_crawls']}")
        print(f"成功率: {(self.stats['successful_crawls'] / self.stats['total_characters'] * 100):.1f}%")
        print(f"总耗时: {duration}")
        print(f"平均耗时: {duration / self.stats['total_characters'] if self.stats['total_characters'] > 0 else 0}")
        
        # 添加问题诊断信息
        if self.stats['successful_crawls'] > 0:
            print("\n⚠️  问题诊断:")
            print("如果所有角色都返回相同的坐骑数据，可能的原因:")
            print("1. API不支持角色参数，只返回令牌对应角色的数据")
            print("2. 需要为每个角色获取独立的API令牌")
            print("3. 当前API设计限制，无法查询其他角色的数据")
            print("\n建议解决方案:")
            print("1. 检查API文档，确认是否支持多角色查询")
            print("2. 为每个角色获取独立的访问令牌")
            print("3. 考虑使用其他数据源或API")
        
        print("="*60)
    
    def export_mounts_report(self, output_file: str = None) -> str:
        """导出坐骑数据报告"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"mounts_report_{timestamp}.json"
        
        try:
            # 获取所有角色的坐骑数据
            characters = self.db_manager.get_all_characters()
            
            # 生成报告数据
            report_data = {
                "generated_at": datetime.now().isoformat(),
                "statistics": self.stats,
                "characters": []
            }
            
            for character in characters:
                char_data = {
                    "name": character.get("name"),
                    "realm": character.get("realm_slug"),
                    "faction": character.get("faction"),
                    "class": character.get("class"),
                    "level": character.get("level"),
                    "mounts_now": character.get("mounts_now", 0),
                    "mounts_total": character.get("mounts_total", 0)
                }
                report_data["characters"].append(char_data)
            
            # 按坐骑数量排序
            report_data["characters"].sort(key=lambda x: x["mounts_now"], reverse=True)
            
            # 保存报告
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"坐骑数据报告已保存到: {output_file}")
            return output_file
            
        except Exception as e:
            self.logger.error(f"导出报告失败: {e}")
            return None

def main():
    """主函数"""
    print("=== 魔兽世界坐骑数据爬虫 ===")
    
    # 检查数据库文件
    db_path = resolve_db_path()
    if not db_path.exists():
        print(f"❌ 数据库文件不存在: {db_path}")
        print("请先运行其他爬虫脚本获取角色数据")
        return False
    
    # 创建爬虫实例
    crawler = MountsCrawler(str(db_path))
    
    # 开始爬取
    success = crawler.crawl_all_characters()
    
    if success:
        # 导出报告
        report_file = crawler.export_mounts_report()
        if report_file:
            print(f"\n✅ 坐骑数据爬取完成！")
            print(f"📊 报告文件: {report_file}")
        return True
    else:
        print("\n❌ 坐骑数据爬取失败！")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 