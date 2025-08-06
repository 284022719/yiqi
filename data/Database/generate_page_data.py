#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从数据库生成page_data.json文件
用于前端页面数据展示
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Any

class PageDataGenerator:
    def __init__(self, db_path: str = "data/guild_database.db"):
        """初始化页面数据生成器"""
        self.db_path = db_path
        self.output_path = "data/page_data.json"
    
    def get_database_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)
    
    def get_character_data(self) -> List[Dict]:
        """从guild_character表获取角色数据"""
        with self.get_database_connection() as conn:
            cursor = conn.cursor()
            
            # 获取2025年2月27日之后登录的角色数据
            # 2025-02-27 00:00:00 转换为Unix时间戳
            cutoff_timestamp = 1706313600  # 2025年2月27日 00:00:00 UTC
            
            cursor.execute("""
                SELECT name, class, level, achievement_points, average_item_level, 
                       faction, realm, spec, guild, mythic_score, race, sex
                FROM guild_characters 
                WHERE last_login_timestamp >= ?
                ORDER BY COALESCE(achievement_points, 0) DESC
            """, (cutoff_timestamp,))
            
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            characters = []
            for row in rows:
                character = dict(zip(columns, row))
                # 处理空值
                character['achievement_points'] = character.get('achievement_points') or 0
                character['average_item_level'] = character.get('average_item_level') or 0
                character['level'] = character.get('level') or 0
                character['mythic_score'] = character.get('mythic_score') or 0
                characters.append(character)
            
            return characters
    
    def calculate_statistics(self, characters: List[Dict]) -> Dict[str, Any]:
        """计算统计数据"""
        if not characters:
            return {
                "totalMembers": 0,
                "activeMembers": 0,
                "dataCompleteness": {
                    "total": 0,
                    "complete": 0,
                    "incomplete": 0,
                    "percentage": 0
                }
            }
        
        total = len(characters)
        complete = sum(1 for c in characters if c.get('achievement_points', 0) > 0)
        incomplete = total - complete
        percentage = round((complete / total) * 100, 1) if total > 0 else 0
        
        return {
            "totalMembers": total,
            "activeMembers": complete,
            "dataCompleteness": {
                "total": total,
                "complete": complete,
                "incomplete": incomplete,
                "percentage": percentage
            }
        }
    
    def generate_chart_data(self, characters: List[Dict]) -> Dict[str, List[Dict]]:
        """生成图表数据"""
        # 职业分布
        class_distribution = {}
        for char in characters:
            class_name = char.get('class', '未知')
            class_distribution[class_name] = class_distribution.get(class_name, 0) + 1
        
        class_chart = [
            {"name": class_name, "value": count}
            for class_name, count in sorted(class_distribution.items(), key=lambda x: x[1], reverse=True)
        ]
        
        # 阵营分布（饼图数据）
        faction_distribution = {}
        for char in characters:
            faction = char.get('faction', '未知')
            faction_distribution[faction] = faction_distribution.get(faction, 0) + 1
        
        faction_chart = [
            {"name": faction, "value": count}
            for faction, count in faction_distribution.items()
        ]
        
        # 种族分布
        race_distribution = {}
        for char in characters:
            race = char.get('race', '未知')
            race_distribution[race] = race_distribution.get(race, 0) + 1
        
        race_chart = [
            {"name": race, "value": count}
            for race, count in sorted(race_distribution.items(), key=lambda x: x[1], reverse=True)
        ]
        
        # 服务器分布
        realm_distribution = {}
        for char in characters:
            realm = char.get('realm', '未知')
            realm_distribution[realm] = realm_distribution.get(realm, 0) + 1
        
        realm_chart = [
            {"name": realm, "value": count}
            for realm, count in sorted(realm_distribution.items(), key=lambda x: x[1], reverse=True)
        ]
        
        # 性别分布
        gender_distribution = {}
        for char in characters:
            sex = char.get('sex', '未知')
            # 将英文性别转换为中文
            if sex == 'Male':
                gender = '男'
            elif sex == 'Female':
                gender = '女'
            else:
                gender = '未知'
            gender_distribution[gender] = gender_distribution.get(gender, 0) + 1
        
        gender_chart = [
            {"name": gender, "value": count}
            for gender, count in gender_distribution.items()
        ]
        
        return {
            "classDistribution": class_chart,
            "factionDistribution": faction_chart,
            "raceDistribution": race_chart,
            "realmDistribution": realm_chart,
            "genderDistribution": gender_chart
        }
    
    def generate_rankings(self, characters: List[Dict]) -> Dict[str, List[Dict]]:
        """生成排行榜数据"""
        # 成就点数排行榜
        achievement_ranking = []
        for i, char in enumerate(characters[:20], 1):  # 前20名
            achievement_ranking.append({
                "rank": i,
                "name": char.get('name', ''),
                "realm": char.get('realm', ''),
                "class": char.get('class', ''),
                "spec": char.get('spec', ''),
                "achievement_points": char.get('achievement_points', 0),
                "average_item_level": char.get('average_item_level', 0),
                "mythic_score": char.get('mythic_score', 0)
            })
        
        # 装等排行榜
        item_level_ranking = []
        sorted_by_ilvl = sorted(characters, key=lambda x: x.get('average_item_level', 0), reverse=True)
        for i, char in enumerate(sorted_by_ilvl[:20], 1):
            item_level_ranking.append({
                "rank": i,
                "name": char.get('name', ''),
                "realm": char.get('realm', ''),
                "class": char.get('class', ''),
                "spec": char.get('spec', ''),
                "achievement_points": char.get('achievement_points', 0),
                "average_item_level": char.get('average_item_level', 0),
                "mythic_score": char.get('mythic_score', 0)
            })
        
        # 史诗钥石评分排行榜
        mythic_score_ranking = []
        sorted_by_mythic = sorted(characters, key=lambda x: x.get('mythic_score', 0), reverse=True)
        for i, char in enumerate(sorted_by_mythic[:20], 1):
            mythic_score_ranking.append({
                "rank": i,
                "name": char.get('name', ''),
                "realm": char.get('realm', ''),
                "class": char.get('class', ''),
                "spec": char.get('spec', ''),
                "achievement_points": char.get('achievement_points', 0),
                "average_item_level": char.get('average_item_level', 0),
                "mythic_score": char.get('mythic_score', 0)
            })
        
        return {
            "achievementRanking": achievement_ranking,
            "itemLevelRanking": item_level_ranking,
            "mythicScoreRanking": mythic_score_ranking
        }
    
    def generate_page_data(self) -> Dict[str, Any]:
        """生成完整的页面数据"""
        print("正在从数据库获取角色数据...")
        characters = self.get_character_data()
        print(f"获取到 {len(characters)} 个角色数据")
        
        print("正在计算统计数据...")
        stats = self.calculate_statistics(characters)
        
        print("正在生成图表数据...")
        charts = self.generate_chart_data(characters)
        
        print("正在生成排行榜数据...")
        rankings = self.generate_rankings(characters)
        
        page_data = {
            "lastUpdated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "stats": stats,
            "charts": charts,
            "rankings": rankings
        }
        
        return page_data
    
    def save_page_data(self, page_data: Dict[str, Any]) -> bool:
        """保存页面数据到JSON文件"""
        try:
            # 确保输出目录存在
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(page_data, f, ensure_ascii=False, indent=2)
            
            print(f"页面数据已保存到: {self.output_path}")
            return True
        except Exception as e:
            print(f"保存页面数据失败: {e}")
            return False
    
    def run(self) -> bool:
        """运行数据生成流程"""
        try:
            print("=== 开始生成页面数据 ===")
            
            # 生成页面数据
            page_data = self.generate_page_data()
            
            # 保存到文件
            success = self.save_page_data(page_data)
            
            if success:
                print("=== 页面数据生成完成 ===")
                print(f"总成员数: {page_data['stats']['totalMembers']}")
                print(f"活跃成员: {page_data['stats']['activeMembers']}")
                print(f"数据完整率: {page_data['stats']['dataCompleteness']['percentage']}%")
                print(f"最后更新: {page_data['lastUpdated']}")
            
            return success
            
        except Exception as e:
            print(f"生成页面数据失败: {e}")
            return False

def main():
    """主函数"""
    generator = PageDataGenerator()
    success = generator.run()
    
    if success:
        print("\n✅ 页面数据生成成功！")
        print("现在可以刷新网页查看最新数据。")
    else:
        print("\n❌ 页面数据生成失败！")
        print("请检查数据库连接和文件权限。")

if __name__ == '__main__':
    main() 