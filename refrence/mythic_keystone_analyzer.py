#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
魔兽世界大秘境数据分析工具
解析和分析大秘境赛季API返回的数据
"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class DungeonRun:
    """大秘境记录数据类"""
    dungeon_name: str
    dungeon_id: int
    keystone_level: int
    duration: int
    completed_timestamp: int
    is_completed_within_time: bool
    mythic_rating: float
    map_rating: float
    affixes: List[str]
    members: List[Dict]

@dataclass
class CharacterInfo:
    """角色信息数据类"""
    name: str
    realm_name: str
    realm_slug: str
    character_id: int
    overall_rating: float
    season_name: str
    best_runs_count: int

class MythicKeystoneAnalyzer:
    """大秘境数据分析器"""
    
    def __init__(self, token: str):
        """
        初始化分析器
        
        Args:
            token: 访问令牌
        """
        self.token = token
        self.base_url = "https://webapi.blizzard.cn/wow-armory-server/api/do"
        self.session = requests.Session()
        
        # 设置请求头
        self.session.headers.update({
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site'
        })
    
    def get_mythic_data(self) -> Optional[Dict]:
        """
        获取大秘境数据
        
        Returns:
            大秘境数据字典或None
        """
        try:
            params = {
                'api': 'mythic_keystone_season',
                'token': self.token
            }
            
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('code') == 0:
                return data.get('data')
            else:
                print(f"API错误: {data.get('message', '未知错误')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return None
        except Exception as e:
            print(f"未知错误: {e}")
            return None
    
    def parse_character_info(self, data: Dict) -> CharacterInfo:
        """
        解析角色基本信息
        
        Args:
            data: API返回的数据
            
        Returns:
            角色信息对象
        """
        character = data['character']
        mythic_rating = data['mythic_rating']
        season = data['season']
        
        return CharacterInfo(
            name=character['name'],
            realm_name=character['realm']['name'],
            realm_slug=character['realm']['slug'],
            character_id=character['id'],
            overall_rating=mythic_rating['rating'],
            season_name=season['season_str'],
            best_runs_count=len(data['best_runs'])
        )
    
    def parse_dungeon_runs(self, data: Dict) -> List[DungeonRun]:
        """
        解析大秘境记录
        
        Args:
            data: API返回的数据
            
        Returns:
            大秘境记录列表
        """
        runs = []
        
        for run_data in data['best_runs']:
            # 解析词缀
            affixes = [affix['name'] for affix in run_data['keystone_affixes']]
            
            # 创建记录对象
            run = DungeonRun(
                dungeon_name=run_data['dungeon']['name'],
                dungeon_id=run_data['dungeon']['id'],
                keystone_level=run_data['keystone_level'],
                duration=run_data['duration'],
                completed_timestamp=run_data['completed_timestamp'],
                is_completed_within_time=run_data['is_completed_within_time'],
                mythic_rating=run_data['mythic_rating']['rating'],
                map_rating=run_data['map_rating']['rating'],
                affixes=affixes,
                members=run_data['members']
            )
            
            runs.append(run)
        
        return runs
    
    def format_duration(self, duration_ms: int) -> str:
        """
        格式化时间显示
        
        Args:
            duration_ms: 毫秒时间
            
        Returns:
            格式化的时间字符串
        """
        total_seconds = duration_ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        
        return f"{minutes:02d}:{seconds:02d}"
    
    def format_timestamp(self, timestamp_ms: int) -> str:
        """
        格式化时间戳显示
        
        Args:
            timestamp_ms: 毫秒时间戳
            
        Returns:
            格式化的时间字符串
        """
        dt = datetime.fromtimestamp(timestamp_ms / 1000)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    def analyze_dungeon_performance(self, runs: List[DungeonRun]) -> Dict:
        """
        分析地下城表现
        
        Args:
            runs: 大秘境记录列表
            
        Returns:
            分析结果字典
        """
        analysis = {
            'total_runs': len(runs),
            'completed_within_time': sum(1 for run in runs if run.is_completed_within_time),
            'average_level': sum(run.keystone_level for run in runs) / len(runs) if runs else 0,
            'highest_level': max(run.keystone_level for run in runs) if runs else 0,
            'average_rating': sum(run.mythic_rating for run in runs) / len(runs) if runs else 0,
            'dungeon_stats': {},
            'level_distribution': {},
            'affix_combinations': {}
        }
        
        # 按地下城统计
        for run in runs:
            dungeon_name = run.dungeon_name
            if dungeon_name not in analysis['dungeon_stats']:
                analysis['dungeon_stats'][dungeon_name] = {
                    'count': 0,
                    'highest_level': 0,
                    'average_rating': 0,
                    'completed_within_time': 0
                }
            
            stats = analysis['dungeon_stats'][dungeon_name]
            stats['count'] += 1
            stats['highest_level'] = max(stats['highest_level'], run.keystone_level)
            if run.is_completed_within_time:
                stats['completed_within_time'] += 1
        
        # 计算平均评分
        for dungeon_name, stats in analysis['dungeon_stats'].items():
            dungeon_runs = [run for run in runs if run.dungeon_name == dungeon_name]
            stats['average_rating'] = sum(run.mythic_rating for run in dungeon_runs) / len(dungeon_runs)
        
        # 等级分布
        for run in runs:
            level = run.keystone_level
            analysis['level_distribution'][level] = analysis['level_distribution'].get(level, 0) + 1
        
        # 词缀组合统计
        for run in runs:
            affix_key = tuple(sorted(run.affixes))
            analysis['affix_combinations'][affix_key] = analysis['affix_combinations'].get(affix_key, 0) + 1
        
        return analysis
    
    def print_character_summary(self, character: CharacterInfo):
        """
        打印角色摘要信息
        
        Args:
            character: 角色信息对象
        """
        print("=" * 60)
        print(f"角色信息: {character.name} ({character.realm_name})")
        print(f"赛季: {character.season_name}")
        print(f"总体评分: {character.overall_rating:.2f}")
        print(f"最佳记录数量: {character.best_runs_count}")
        print("=" * 60)
    
    def print_dungeon_runs(self, runs: List[DungeonRun], limit: int = 10):
        """
        打印大秘境记录
        
        Args:
            runs: 大秘境记录列表
            limit: 显示数量限制
        """
        print(f"\n📊 最佳记录 (显示前{limit}条):")
        print("-" * 80)
        
        for i, run in enumerate(runs[:limit], 1):
            status = "✅" if run.is_completed_within_time else "❌"
            duration = self.format_duration(run.duration)
            date = self.format_timestamp(run.completed_timestamp)
            
            print(f"{i:2d}. {status} {run.dungeon_name} {run.keystone_level}层")
            print(f"    时间: {duration} | 评分: {run.mythic_rating:.2f} | 日期: {date}")
            print(f"    词缀: {', '.join(run.affixes)}")
            print()
    
    def print_analysis(self, analysis: Dict):
        """
        打印分析结果
        
        Args:
            analysis: 分析结果字典
        """
        print("\n📈 数据分析:")
        print("-" * 40)
        
        # 总体统计
        completion_rate = (analysis['completed_within_time'] / analysis['total_runs']) * 100
        print(f"总记录数: {analysis['total_runs']}")
        print(f"限时完成: {analysis['completed_within_time']} ({completion_rate:.1f}%)")
        print(f"平均等级: {analysis['average_level']:.1f}")
        print(f"最高等级: {analysis['highest_level']}")
        print(f"平均评分: {analysis['average_rating']:.2f}")
        
        # 地下城统计
        print(f"\n🏰 地下城统计:")
        for dungeon_name, stats in analysis['dungeon_stats'].items():
            completion_rate = (stats['completed_within_time'] / stats['count']) * 100
            print(f"  {dungeon_name}: {stats['count']}次, 最高{stats['highest_level']}层, "
                  f"平均评分{stats['average_rating']:.2f}, 完成率{completion_rate:.1f}%")
        
        # 等级分布
        print(f"\n📊 等级分布:")
        for level in sorted(analysis['level_distribution'].keys()):
            count = analysis['level_distribution'][level]
            print(f"  {level}层: {count}次")
    
    def export_to_json(self, data: Dict, filename: str):
        """
        导出数据到JSON文件
        
        Args:
            data: 要导出的数据
            filename: 文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\n💾 数据已导出到: {filename}")
        except Exception as e:
            print(f"导出失败: {e}")
    
    def run_analysis(self, export_json: bool = False):
        """
        运行完整分析
        
        Args:
            export_json: 是否导出JSON文件
        """
        print("🔍 正在获取大秘境数据...")
        
        # 获取数据
        data = self.get_mythic_data()
        if not data:
            print("❌ 获取数据失败")
            return
        
        # 解析角色信息
        character = self.parse_character_info(data)
        self.print_character_summary(character)
        
        # 解析大秘境记录
        runs = self.parse_dungeon_runs(data)
        self.print_dungeon_runs(runs)
        
        # 分析数据
        analysis = self.analyze_dungeon_performance(runs)
        self.print_analysis(analysis)
        
        # 导出数据
        if export_json:
            export_data = {
                'character': {
                    'name': character.name,
                    'realm': character.realm_name,
                    'overall_rating': character.overall_rating,
                    'season': character.season_name
                },
                'runs': [
                    {
                        'dungeon': run.dungeon_name,
                        'level': run.keystone_level,
                        'duration': run.duration,
                        'completed_within_time': run.is_completed_within_time,
                        'rating': run.mythic_rating,
                        'affixes': run.affixes,
                        'date': self.format_timestamp(run.completed_timestamp)
                    }
                    for run in runs
                ],
                'analysis': analysis
            }
            
            filename = f"mythic_data_{character.name}_{character.realm_slug}.json"
            self.export_to_json(export_data, filename)

def main():
    """主函数"""
    print("魔兽世界大秘境数据分析工具")
    print("=" * 40)
    
    # 获取令牌
    token = input("请输入访问令牌: ").strip()
    if not token:
        print("❌ 令牌不能为空")
        return
    
    # 创建分析器
    analyzer = MythicKeystoneAnalyzer(token)
    
    # 询问是否导出JSON
    export_choice = input("是否导出JSON文件? (y/N): ").strip().lower()
    export_json = export_choice in ['y', 'yes', '是']
    
    # 运行分析
    analyzer.run_analysis(export_json)

if __name__ == "__main__":
    main() 