"""
数据加载模块
负责从CSV文件读取角色数据
"""

import csv
from pathlib import Path
from typing import List, Dict, Any, Optional

from src.config.settings import DATA_FILES, SERVER_MAPPING, STATS_CONFIG
from src.utils.logger import get_logger


class DataLoader:
    """数据加载器"""
    
    def __init__(self):
        self.logger = get_logger('data_loader')
    
    def load_role_data(self) -> List[Dict[str, Any]]:
        """
        从CSV文件加载角色数据
        
        Returns:
            角色数据列表
        """
        try:
            csv_path = DATA_FILES["csv_primary"]
            
            if not csv_path.exists():
                self.logger.error(f"CSV文件不存在: {csv_path}")
                return []
            
            role_data = []
            
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    try:
                        # 解析数据
                        role_info = self._parse_role_row(row)
                        if role_info:
                            role_data.append(role_info)
                            
                    except (ValueError, KeyError) as e:
                        self.logger.warning(f"解析行数据失败: {e}")
                        continue
            
            self.logger.info(f"成功加载 {len(role_data)} 个角色数据")
            return role_data
            
        except Exception as e:
            self.logger.error(f"加载角色数据失败: {e}")
            return []
    
    def _parse_role_row(self, row: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """
        解析单行角色数据
        
        Args:
            row: CSV行数据
            
        Returns:
            解析后的角色信息或None
        """
        try:
            # 获取基本字段
            last_online_days = float(row['Last Online (Days)'])
            level = int(row['Level'])
            character_name = row['Name']
            server_name_cn = row['Realm Name']
            
            # 过滤条件
            if (last_online_days >= STATS_CONFIG["max_online_days"] or 
                level < STATS_CONFIG["min_level"]):
                return None
            
            # 获取英文服务器名
            server_name_en = self._get_server_english_name(server_name_cn)
            
            return {
                'name': character_name,
                'server': server_name_en,
                'full_name': f"{character_name}-{server_name_cn}",
                'level': level,
                'last_online_days': last_online_days
            }
            
        except (ValueError, KeyError) as e:
            self.logger.warning(f"解析角色行失败: {e}")
            return None
    
    def _get_server_english_name(self, server_name_cn: str) -> str:
        """
        获取服务器的英文名称
        
        Args:
            server_name_cn: 中文服务器名
            
        Returns:
            英文服务器名
        """
        # 从映射表中获取
        if server_name_cn in SERVER_MAPPING:
            return SERVER_MAPPING[server_name_cn]
        
        # 使用通用转换规则
        return self._convert_server_name(server_name_cn)
    
    def _convert_server_name(self, server_name_cn: str) -> str:
        """
        通用服务器名称转换
        
        Args:
            server_name_cn: 中文服务器名
            
        Returns:
            转换后的英文名
        """
        # 移除特殊字符
        name = server_name_cn.replace('（', '').replace('）', '')
        
        # 转换为小写并替换空格
        name = name.lower().replace(' ', '-')
        
        return name
    
    def get_filtered_roles(self, max_online_days: int = None, min_level: int = None) -> List[Dict[str, Any]]:
        """
        获取过滤后的角色数据
        
        Args:
            max_online_days: 最大上线天数
            min_level: 最小等级
            
        Returns:
            过滤后的角色数据
        """
        if max_online_days is None:
            max_online_days = STATS_CONFIG["max_online_days"]
        
        if min_level is None:
            min_level = STATS_CONFIG["min_level"]
        
        all_roles = self.load_role_data()
        
        filtered_roles = [
            role for role in all_roles
            if role['last_online_days'] < max_online_days and role['level'] >= min_level
        ]
        
        self.logger.info(f"过滤后剩余 {len(filtered_roles)} 个角色")
        return filtered_roles


def create_data_loader() -> DataLoader:
    """创建数据加载器实例"""
    return DataLoader() 