"""
会员信息统计生成器
处理 memberinfo.csv 数据并生成统计数据
"""

import csv
import json
import os
from typing import Dict, List, Any
from collections import defaultdict

from src.config.settings import DATA_FILES, STATS_CONFIG
from src.utils.logger import create_stats_logger


class MemberInfoGenerator:
    """会员信息统计生成器"""
    
    def __init__(self):
        self.logger = create_stats_logger()
        self.memberinfo_path = DATA_FILES["memberinfo"]
    
    def load_memberinfo_data(self) -> List[Dict[str, Any]]:
        """加载会员信息数据"""
        if not os.path.exists(self.memberinfo_path):
            self.logger.error(f"会员信息文件不存在: {self.memberinfo_path}")
            return []
        
        data = []
        try:
            with open(self.memberinfo_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            
            self.logger.info(f"成功加载 {len(data)} 条会员信息数据")
            return data
        except Exception as e:
            self.logger.error(f"加载会员信息数据失败: {e}")
            return []
    
    def filter_active_members(self, data: List[Dict[str, Any]], max_days: int = 150) -> List[Dict[str, Any]]:
        """过滤活跃会员（最近上线天数小于等于指定天数）"""
        filtered_data = []
        for row in data:
            try:
                last_online_days = float(row.get('Last Online (Days)', 999))
                if last_online_days <= max_days:
                    filtered_data.append(row)
            except (ValueError, TypeError):
                continue
        
        self.logger.info(f"活跃会员（{max_days}天内上线）: {len(filtered_data)} 人")
        return filtered_data
    
    def generate_memberinfo_stats(self) -> Dict[str, Any]:
        """生成会员信息统计数据"""
        data = self.load_memberinfo_data()
        if not data:
            return {}
        
        # 过滤活跃会员
        active_data = self.filter_active_members(data, STATS_CONFIG["active_days_threshold"])
        
        # 生成统计数据
        stats = {
            "total_members": len(data),
            "active_members": len(active_data),
            "class_distribution": self._get_class_distribution(active_data),
            "race_distribution": self._get_race_distribution(active_data),
            "gender_distribution": self._get_gender_distribution(active_data),
            "faction_distribution": self._get_faction_distribution(active_data),
            "server_distribution": self._get_server_distribution(active_data),
            "level_distribution": self._get_level_distribution(active_data),
            "mythic_ranking": self._get_mythic_ranking(active_data),
            "recent_members": self._get_recent_members(active_data)
        }
        
        return stats
    
    def _get_class_distribution(self, data: List[Dict[str, Any]]) -> Dict[str, int]:
        """获取职业分布"""
        distribution = defaultdict(int)
        for row in data:
            class_name = row.get('Class', '未知')
            if class_name and class_name != '未知':
                distribution[class_name] += 1
        return dict(distribution)
    
    def _get_race_distribution(self, data: List[Dict[str, Any]]) -> Dict[str, int]:
        """获取种族分布"""
        distribution = defaultdict(int)
        for row in data:
            race = row.get('Race', '未知')
            if race and race != '未知':
                distribution[race] += 1
        return dict(distribution)
    
    def _get_gender_distribution(self, data: List[Dict[str, Any]]) -> Dict[str, int]:
        """获取性别分布"""
        distribution = defaultdict(int)
        for row in data:
            sex = row.get('Sex', 'Unknown')
            if sex:
                # 转换英文为中文
                if sex == 'Male':
                    distribution['Male'] += 1
                elif sex == 'Female':
                    distribution['Female'] += 1
                else:
                    distribution['Unknown'] += 1
        return dict(distribution)
    
    def _get_faction_distribution(self, data: List[Dict[str, Any]]) -> Dict[str, int]:
        """获取阵营分布"""
        distribution = defaultdict(int)
        for row in data:
            faction = row.get('Faction', 'Unknown')
            if faction:
                distribution[faction] += 1
        return dict(distribution)
    
    def _get_server_distribution(self, data: List[Dict[str, Any]]) -> Dict[str, int]:
        """获取服务器分布"""
        distribution = defaultdict(int)
        for row in data:
            server = row.get('Realm Name', '未知')
            if server and server != '未知':
                distribution[server] += 1
        return dict(distribution)
    
    def _get_level_distribution(self, data: List[Dict[str, Any]]) -> Dict[str, int]:
        """获取等级分布"""
        distribution = defaultdict(int)
        for row in data:
            try:
                level = int(row.get('Level', 0))
                if level > 0:
                    distribution[str(level)] += 1
            except (ValueError, TypeError):
                continue
        return dict(distribution)
    
    def _get_mythic_ranking(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """获取 Mythic+ 评分排行"""
        ranking = []
        for row in data:
            try:
                mythic_score = float(row.get('Mythic+ Score', 0))
                if mythic_score > 0:
                    ranking.append({
                        "name": row.get('Name', '未知'),
                        "class": row.get('Class', '未知'),
                        "mythic_score": mythic_score
                    })
            except (ValueError, TypeError):
                continue
        
        # 按评分排序
        ranking.sort(key=lambda x: x['mythic_score'], reverse=True)
        return ranking[:10]  # 返回前10名
    
    def _get_recent_members(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """获取最近上线的会员"""
        recent_members = []
        for row in data:
            try:
                last_online_days = float(row.get('Last Online (Days)', 999))
                if last_online_days <= 7:  # 最近7天内上线
                    recent_members.append({
                        "name": row.get('Name', '未知'),
                        "class": row.get('Class', '未知'),
                        "level": row.get('Level', '未知'),
                        "last_online_days": last_online_days
                    })
            except (ValueError, TypeError):
                continue
        
        # 按最后上线时间排序
        recent_members.sort(key=lambda x: x['last_online_days'])
        return recent_members[:20]  # 返回最近20个
    
    def save_stats(self, stats: Dict[str, Any], output_path: str = None) -> bool:
        """保存统计数据到文件"""
        if not output_path:
            output_path = os.path.join('data', 'memberinfo_stats.json')
        
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"统计数据已保存到: {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"保存统计数据失败: {e}")
            return False


def create_memberinfo_generator() -> MemberInfoGenerator:
    """创建会员信息生成器实例"""
    return MemberInfoGenerator()


if __name__ == "__main__":
    # 测试生成统计数据
    generator = create_memberinfo_generator()
    stats = generator.generate_memberinfo_stats()
    
    if stats:
        print("生成的统计数据:")
        print(f"总会员数: {stats.get('total_members', 0)}")
        print(f"活跃会员数: {stats.get('active_members', 0)}")
        print(f"职业分布: {len(stats.get('class_distribution', {}))} 个职业")
        print(f"种族分布: {len(stats.get('race_distribution', {}))} 个种族")
        print(f"Mythic+ 排行: {len(stats.get('mythic_ranking', []))} 个角色")
        
        # 保存统计数据
        generator.save_stats(stats)
    else:
        print("生成统计数据失败") 