#!/usr/bin/env python3
"""
数据库完整性检查工具
分析数据库中的数据完整性和缺失情况
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Any

class DatabaseIntegrityChecker:
    """数据库完整性检查器"""
    
    def __init__(self, db_path: str = "data/guild_members.db"):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """连接数据库"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            print(f"成功连接到数据库: {self.db_path}")
        except Exception as e:
            print(f"连接数据库失败: {e}")
            return False
        return True
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            print("数据库连接已关闭")
    
    def get_table_info(self) -> Dict[str, Any]:
        """获取表结构信息"""
        try:
            self.cursor.execute("PRAGMA table_info(guild_members)")
            columns = self.cursor.fetchall()
            
            table_info = {
                'table_name': 'guild_members',
                'columns': [],
                'total_columns': len(columns)
            }
            
            for col in columns:
                column_info = {
                    'name': col[1],
                    'type': col[2],
                    'not_null': bool(col[3]),
                    'default_value': col[4],
                    'primary_key': bool(col[5])
                }
                table_info['columns'].append(column_info)
            
            return table_info
        except Exception as e:
            print(f"获取表结构失败: {e}")
            return {}
    
    def get_basic_stats(self) -> Dict[str, Any]:
        """获取基本统计信息"""
        try:
            # 总记录数
            self.cursor.execute("SELECT COUNT(*) FROM guild_members")
            total_members = self.cursor.fetchone()[0]
            
            # 活跃成员数（70级以上）
            self.cursor.execute("SELECT COUNT(*) FROM guild_members WHERE level >= 70")
            active_members = self.cursor.fetchone()[0]
            
            # 不同职业数量
            self.cursor.execute("SELECT COUNT(DISTINCT class) FROM guild_members")
            class_count = self.cursor.fetchone()[0]
            
            # 不同服务器数量
            self.cursor.execute("SELECT COUNT(DISTINCT realm_name) FROM guild_members")
            server_count = self.cursor.fetchone()[0]
            
            # 不同种族数量
            self.cursor.execute("SELECT COUNT(DISTINCT race) FROM guild_members")
            race_count = self.cursor.fetchone()[0]
            
            return {
                'total_members': total_members,
                'active_members': active_members,
                'class_count': class_count,
                'server_count': server_count,
                'race_count': race_count
            }
        except Exception as e:
            print(f"获取基本统计失败: {e}")
            return {}
    
    def check_missing_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """检查缺失数据"""
        missing_data = {}
        
        try:
            # 检查缺失Mythic+评分
            self.cursor.execute("""
                SELECT name, realm_name, level, class 
                FROM guild_members 
                WHERE (mythic_score IS NULL OR mythic_score = 0) 
                AND level >= 70 
                ORDER BY level DESC 
                LIMIT 50
            """)
            missing_mythic = [{'name': row[0], 'realm': row[1], 'level': row[2], 'class': row[3]} 
                             for row in self.cursor.fetchall()]
            missing_data['missing_mythic_score'] = missing_mythic
            
            # 检查缺失成就点数
            self.cursor.execute("""
                SELECT name, realm_name, level, class 
                FROM guild_members 
                WHERE (achievement_points IS NULL OR achievement_points = 0) 
                AND level >= 70 
                ORDER BY level DESC 
                LIMIT 50
            """)
            missing_achievement = [{'name': row[0], 'realm': row[1], 'level': row[2], 'class': row[3]} 
                                  for row in self.cursor.fetchall()]
            missing_data['missing_achievement_points'] = missing_achievement
            
            # 检查缺失坐骑数量
            self.cursor.execute("""
                SELECT name, realm_name, level, class 
                FROM guild_members 
                WHERE (mounts_count IS NULL OR mounts_count = 0) 
                AND level >= 70 
                ORDER BY level DESC 
                LIMIT 50
            """)
            missing_mounts = [{'name': row[0], 'realm': row[1], 'level': row[2], 'class': row[3]} 
                             for row in self.cursor.fetchall()]
            missing_data['missing_mounts_count'] = missing_mounts
            
            # 检查缺失装等
            self.cursor.execute("""
                SELECT name, realm_name, level, class 
                FROM guild_members 
                WHERE (average_item_level IS NULL OR average_item_level = 0) 
                AND level >= 70 
                ORDER BY level DESC 
                LIMIT 50
            """)
            missing_itemlevel = [{'name': row[0], 'realm': row[1], 'level': row[2], 'class': row[3]} 
                                for row in self.cursor.fetchall()]
            missing_data['missing_item_level'] = missing_itemlevel
            
            # 检查低等级成员
            self.cursor.execute("""
                SELECT name, realm_name, level, class 
                FROM guild_members 
                WHERE level < 70 
                ORDER BY level DESC 
                LIMIT 50
            """)
            low_level = [{'name': row[0], 'realm': row[1], 'level': row[2], 'class': row[3]} 
                        for row in self.cursor.fetchall()]
            missing_data['low_level_members'] = low_level
            
            # 检查长期未上线成员
            self.cursor.execute("""
                SELECT name, realm_name, level, class, last_online_days 
                FROM guild_members 
                WHERE last_online_days > 30 
                ORDER BY last_online_days DESC 
                LIMIT 50
            """)
            inactive = [{'name': row[0], 'realm': row[1], 'level': row[2], 'class': row[3], 'days_offline': row[4]} 
                       for row in self.cursor.fetchall()]
            missing_data['inactive_members'] = inactive
            
        except Exception as e:
            print(f"检查缺失数据失败: {e}")
        
        return missing_data
    
    def get_data_distribution(self) -> Dict[str, Any]:
        """获取数据分布情况"""
        distribution = {}
        
        try:
            # 职业分布
            self.cursor.execute("""
                SELECT class, COUNT(*) as count 
                FROM guild_members 
                GROUP BY class 
                ORDER BY count DESC
            """)
            class_dist = {row[0]: row[1] for row in self.cursor.fetchall()}
            distribution['class_distribution'] = class_dist
            
            # 服务器分布
            self.cursor.execute("""
                SELECT realm_name, COUNT(*) as count 
                FROM guild_members 
                GROUP BY realm_name 
                ORDER BY count DESC
            """)
            server_dist = {row[0]: row[1] for row in self.cursor.fetchall()}
            distribution['server_distribution'] = server_dist
            
            # 种族分布
            self.cursor.execute("""
                SELECT race, COUNT(*) as count 
                FROM guild_members 
                GROUP BY race 
                ORDER BY count DESC
            """)
            race_dist = {row[0]: row[1] for row in self.cursor.fetchall()}
            distribution['race_distribution'] = race_dist
            
            # 等级分布
            self.cursor.execute("""
                SELECT 
                    CASE 
                        WHEN level >= 80 THEN '80+'
                        WHEN level >= 70 THEN '70-79'
                        WHEN level >= 60 THEN '60-69'
                        WHEN level >= 50 THEN '50-59'
                        WHEN level >= 40 THEN '40-49'
                        WHEN level >= 30 THEN '30-39'
                        WHEN level >= 20 THEN '20-29'
                        WHEN level >= 10 THEN '10-19'
                        ELSE '1-9'
                    END as level_range,
                    COUNT(*) as count
                FROM guild_members 
                GROUP BY level_range
                ORDER BY count DESC
            """)
            level_dist = {row[0]: row[1] for row in self.cursor.fetchall()}
            distribution['level_distribution'] = level_dist
            
            # 阵营分布
            self.cursor.execute("""
                SELECT faction, COUNT(*) as count 
                FROM guild_members 
                GROUP BY faction 
                ORDER BY count DESC
            """)
            faction_dist = {row[0]: row[1] for row in self.cursor.fetchall()}
            distribution['faction_distribution'] = faction_dist
            
        except Exception as e:
            print(f"获取数据分布失败: {e}")
        
        return distribution
    
    def get_data_quality_metrics(self) -> Dict[str, Any]:
        """获取数据质量指标"""
        metrics = {}
        
        try:
            # 计算各字段的完整性
            total_members = self.get_basic_stats()['total_members']
            
            # Mythic+评分完整性
            self.cursor.execute("SELECT COUNT(*) FROM guild_members WHERE mythic_score IS NOT NULL AND mythic_score > 0")
            mythic_complete = self.cursor.fetchone()[0]
            metrics['mythic_score_completeness'] = {
                'complete': mythic_complete,
                'total': total_members,
                'percentage': round(mythic_complete / total_members * 100, 2) if total_members > 0 else 0
            }
            
            # 成就点数完整性
            self.cursor.execute("SELECT COUNT(*) FROM guild_members WHERE achievement_points IS NOT NULL AND achievement_points > 0")
            achievement_complete = self.cursor.fetchone()[0]
            metrics['achievement_points_completeness'] = {
                'complete': achievement_complete,
                'total': total_members,
                'percentage': round(achievement_complete / total_members * 100, 2) if total_members > 0 else 0
            }
            
            # 坐骑数量完整性
            self.cursor.execute("SELECT COUNT(*) FROM guild_members WHERE mounts_count IS NOT NULL AND mounts_count > 0")
            mounts_complete = self.cursor.fetchone()[0]
            metrics['mounts_count_completeness'] = {
                'complete': mounts_complete,
                'total': total_members,
                'percentage': round(mounts_complete / total_members * 100, 2) if total_members > 0 else 0
            }
            
            # 装等完整性
            self.cursor.execute("SELECT COUNT(*) FROM guild_members WHERE average_item_level IS NOT NULL AND average_item_level > 0")
            itemlevel_complete = self.cursor.fetchone()[0]
            metrics['item_level_completeness'] = {
                'complete': itemlevel_complete,
                'total': total_members,
                'percentage': round(itemlevel_complete / total_members * 100, 2) if total_members > 0 else 0
            }
            
            # 在线天数完整性
            self.cursor.execute("SELECT COUNT(*) FROM guild_members WHERE last_online_days IS NOT NULL")
            online_days_complete = self.cursor.fetchone()[0]
            metrics['online_days_completeness'] = {
                'complete': online_days_complete,
                'total': total_members,
                'percentage': round(online_days_complete / total_members * 100, 2) if total_members > 0 else 0
            }
            
        except Exception as e:
            print(f"获取数据质量指标失败: {e}")
        
        return metrics
    
    def get_top_rankings(self) -> Dict[str, List[Dict[str, Any]]]:
        """获取排行榜数据"""
        rankings = {}
        
        try:
            # Mythic+排行榜
            self.cursor.execute("""
                SELECT name, realm_name, class, mythic_score, level
                FROM guild_members 
                WHERE mythic_score > 0 AND level >= 70
                ORDER BY mythic_score DESC 
                LIMIT 20
            """)
            mythic_ranking = [{'name': row[0], 'realm': row[1], 'class': row[2], 'score': row[3], 'level': row[4]} 
                             for row in self.cursor.fetchall()]
            rankings['mythic_ranking'] = mythic_ranking
            
            # 成就排行榜
            self.cursor.execute("""
                SELECT name, realm_name, class, achievement_points, level
                FROM guild_members 
                WHERE achievement_points > 0 AND level >= 70
                ORDER BY achievement_points DESC 
                LIMIT 20
            """)
            achievement_ranking = [{'name': row[0], 'realm': row[1], 'class': row[2], 'points': row[3], 'level': row[4]} 
                                  for row in self.cursor.fetchall()]
            rankings['achievement_ranking'] = achievement_ranking
            
            # 坐骑排行榜
            self.cursor.execute("""
                SELECT name, realm_name, class, mounts_count, level
                FROM guild_members 
                WHERE mounts_count > 0 AND level >= 70
                ORDER BY mounts_count DESC 
                LIMIT 20
            """)
            mounts_ranking = [{'name': row[0], 'realm': row[1], 'class': row[2], 'count': row[3], 'level': row[4]} 
                             for row in self.cursor.fetchall()]
            rankings['mounts_ranking'] = mounts_ranking
            
            # 装等排行榜
            self.cursor.execute("""
                SELECT name, realm_name, class, average_item_level, level
                FROM guild_members 
                WHERE average_item_level > 0 AND level >= 70
                ORDER BY average_item_level DESC 
                LIMIT 20
            """)
            itemlevel_ranking = [{'name': row[0], 'realm': row[1], 'class': row[2], 'itemlevel': row[3], 'level': row[4]} 
                                for row in self.cursor.fetchall()]
            rankings['itemlevel_ranking'] = itemlevel_ranking
            
        except Exception as e:
            print(f"获取排行榜数据失败: {e}")
        
        return rankings
    
    def generate_integrity_report(self) -> Dict[str, Any]:
        """生成完整性报告"""
        if not self.connect():
            return {}
        
        try:
            report = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'database_path': self.db_path,
                'table_info': self.get_table_info(),
                'basic_stats': self.get_basic_stats(),
                'data_distribution': self.get_data_distribution(),
                'data_quality': self.get_data_quality_metrics(),
                'missing_data': self.check_missing_data(),
                'rankings': self.get_top_rankings()
            }
            
            return report
            
        except Exception as e:
            print(f"生成完整性报告失败: {e}")
            return {}
        finally:
            self.disconnect()
    
    def save_report(self, report: Dict[str, Any], filename: str = None):
        """保存报告到文件"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"data/database_integrity_report_{timestamp}.json"
        
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"完整性报告已保存到: {filename}")
        except Exception as e:
            print(f"保存报告失败: {e}")
    
    def print_summary(self, report: Dict[str, Any]):
        """打印摘要信息"""
        if not report:
            print("无法生成报告")
            return
        
        print("\n" + "="*60)
        print("数据库完整性检查报告")
        print("="*60)
        print(f"检查时间: {report.get('timestamp', 'N/A')}")
        print(f"数据库路径: {report.get('database_path', 'N/A')}")
        
        # 基本统计
        basic_stats = report.get('basic_stats', {})
        print(f"\n📊 基本统计:")
        print(f"  总成员数: {basic_stats.get('total_members', 0):,}")
        print(f"  活跃成员数: {basic_stats.get('active_members', 0):,}")
        print(f"  职业种类: {basic_stats.get('class_count', 0)}")
        print(f"  服务器数量: {basic_stats.get('server_count', 0)}")
        print(f"  种族种类: {basic_stats.get('race_count', 0)}")
        
        # 数据质量
        data_quality = report.get('data_quality', {})
        print(f"\n🔍 数据质量:")
        for field, metrics in data_quality.items():
            field_name = field.replace('_', ' ').title()
            percentage = metrics.get('percentage', 0)
            complete = metrics.get('complete', 0)
            total = metrics.get('total', 0)
            print(f"  {field_name}: {complete:,}/{total:,} ({percentage}%)")
        
        # 缺失数据统计
        missing_data = report.get('missing_data', {})
        print(f"\n❌ 缺失数据统计:")
        for data_type, members in missing_data.items():
            data_name = data_type.replace('_', ' ').title()
            print(f"  {data_name}: {len(members)} 个成员")
        
        # 排行榜统计
        rankings = report.get('rankings', {})
        print(f"\n🏆 排行榜统计:")
        for ranking_type, members in rankings.items():
            ranking_name = ranking_type.replace('_', ' ').title()
            print(f"  {ranking_name}: {len(members)} 个成员")
        
        print("\n" + "="*60)


def main():
    """主函数"""
    checker = DatabaseIntegrityChecker()
    
    # 生成完整性报告
    report = checker.generate_integrity_report()
    
    if report:
        # 打印摘要
        checker.print_summary(report)
        
        # 保存详细报告
        checker.save_report(report)
        
        # 保存摘要报告
        summary = {
            'timestamp': report.get('timestamp'),
            'basic_stats': report.get('basic_stats'),
            'data_quality': report.get('data_quality'),
            'missing_data_summary': {
                data_type: len(members) 
                for data_type, members in report.get('missing_data', {}).items()
            }
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        summary_filename = f"data/database_integrity_summary_{timestamp}.json"
        checker.save_report(summary, summary_filename)
        
    else:
        print("数据库完整性检查失败")


if __name__ == "__main__":
    main() 