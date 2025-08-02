"""
统计生成器模块
负责生成各种统计数据
"""

import json
from collections import Counter, defaultdict
from typing import Dict, Any, List
from pathlib import Path

from src.config.settings import DATA_FILES, STATS_CONFIG
from src.utils.logger import create_stats_logger


class StatsGenerator:
    """统计生成器"""
    
    def __init__(self):
        self.logger = create_stats_logger()
    
    def generate_basic_stats(self) -> Dict[str, Any]:
        """生成基础统计数据"""
        try:
            # 加载CSV数据
            csv_path = DATA_FILES["csv_primary"]
            if not csv_path.exists():
                self.logger.error(f"CSV文件不存在: {csv_path}")
                return {}
            
            import csv
            role_data = []
            
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        last_online_days = int(row['最后上线天数'])
                        level = int(row['等级'])
                        
                        if (last_online_days < STATS_CONFIG["max_online_days"] and 
                            level >= STATS_CONFIG["min_level"]):
                            role_data.append(row)
                    except (ValueError, KeyError):
                        continue
            
            # 生成统计数据
            stats = {
                "total_roles": len(role_data),
                "class_distribution": self._get_class_distribution(role_data),
                "server_distribution": self._get_server_distribution(role_data),
                "recent_roles": self._get_recent_roles(role_data)
            }
            
            # 保存到文件
            with open(DATA_FILES["json_stats"], 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"基础统计数据生成完成，共 {len(role_data)} 个角色")
            return stats
            
        except Exception as e:
            self.logger.error(f"生成基础统计数据失败: {e}")
            return {}
    
    def generate_extended_stats(self) -> Dict[str, Any]:
        """生成扩展统计数据"""
        try:
            # 加载扩展CSV数据
            csv_path = DATA_FILES["csv_extended"]
            if not csv_path.exists():
                self.logger.error(f"扩展CSV文件不存在: {csv_path}")
                return {}
            
            import csv
            role_data = []
            
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        last_online_days = int(row['Last Online (Days)'])
                        if last_online_days < STATS_CONFIG["max_online_days"]:
                            role_data.append(row)
                    except (ValueError, KeyError):
                        continue
            
            # 生成扩展统计数据
            stats = {
                "race_distribution": self._get_race_distribution(role_data),
                "gender_distribution": self._get_gender_distribution(role_data),
                "faction_distribution": self._get_faction_distribution(role_data),
                "mythic_ranking": self._get_mythic_ranking(role_data)
            }
            
            # 保存到文件
            with open(DATA_FILES["json_extended_stats"], 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"扩展统计数据生成完成，共 {len(role_data)} 个角色")
            return stats
            
        except Exception as e:
            self.logger.error(f"生成扩展统计数据失败: {e}")
            return {}
    
    def _get_class_distribution(self, role_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """获取职业分布"""
        class_counter = Counter()
        for role in role_data:
            class_name = role.get('职业', '未知')
            class_counter[class_name] += 1
        return dict(class_counter)
    
    def _get_server_distribution(self, role_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """获取服务器分布"""
        server_counter = Counter()
        for role in role_data:
            full_name = role.get('名字', '')
            if '-' in full_name:
                server_name = full_name.split('-', 1)[1]
                server_counter[server_name] += 1
        return dict(server_counter)
    
    def _get_recent_roles(self, role_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """获取最近角色"""
        recent_roles = []
        for role in role_data:
            try:
                recent_roles.append({
                    "name": role.get('名字', ''),
                    "class": role.get('职业', ''),
                    "level": int(role.get('等级', 0)),
                    "last_online_days": int(role.get('最后上线天数', 0))
                })
            except (ValueError, KeyError):
                continue
        
        # 按上线天数排序
        recent_roles.sort(key=lambda x: x['last_online_days'])
        return recent_roles[:STATS_CONFIG["top_ranking_count"]]
    
    def _get_race_distribution(self, role_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """获取种族分布"""
        race_counter = Counter()
        for role in role_data:
            race_name = role.get('Race', '未知')
            race_counter[race_name] += 1
        return dict(race_counter)
    
    def _get_gender_distribution(self, role_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """获取性别分布"""
        gender_counter = Counter()
        for role in role_data:
            gender = role.get('Sex', '未知')
            gender_counter[gender] += 1
        return dict(gender_counter)
    
    def _get_faction_distribution(self, role_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """获取阵营分布"""
        faction_counter = Counter()
        for role in role_data:
            faction = role.get('Faction', '未知')
            faction_counter[faction] += 1
        return dict(faction_counter)
    
    def _get_mythic_ranking(self, role_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """获取史诗钥石评分排行"""
        mythic_roles = []
        for role in role_data:
            try:
                mythic_score = float(role.get('Mythic+ Score', 0))
                if mythic_score > 0:
                    mythic_roles.append({
                        "name": role.get('Name', ''),
                        "class": role.get('Class', ''),
                        "mythic_score": mythic_score
                    })
            except (ValueError, KeyError):
                continue
        
        # 按评分排序
        mythic_roles.sort(key=lambda x: x['mythic_score'], reverse=True)
        return mythic_roles[:STATS_CONFIG["top_ranking_count"]]


def create_stats_generator() -> StatsGenerator:
    """创建统计生成器实例"""
    return StatsGenerator() 