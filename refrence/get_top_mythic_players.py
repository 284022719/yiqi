#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取公会成员中Mythic+ Score最高的10个角色的详细信息
"""

import csv
import json
import requests
import time
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class GuildMember:
    """公会成员信息"""
    name: str
    rank: str
    level: str
    class_name: str
    race: str
    sex: str
    last_online: str
    mythic_score: int
    faction: str
    realm: str = "arthas"  # 默认服务器

@dataclass
class MythicData:
    """大秘境数据"""
    character_name: str
    overall_rating: float
    season_name: str
    best_runs_count: int
    highest_level: int
    completion_rate: float
    average_rating: float
    best_runs: List[Dict]

class MythicKeystoneAPI:
    """大秘境API客户端"""
    
    def __init__(self, cookie_token: str):
        self.cookie_token = cookie_token
        self.session = requests.Session()
        
        # 设置请求头
        self.session.headers.update({
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'origin': 'https://wow.blizzard.cn',
            'referer': 'https://wow.blizzard.cn/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        
        # 设置cookie
        self.session.cookies.set('blizzard_user_info', cookie_token, domain='.blizzard.cn')
    
    def get_character_token(self, realm_slug: str, character_name: str) -> Optional[str]:
        """获取角色访问令牌"""
        try:
            url = "https://webapi.blizzard.cn/wow-armory-server/api/index"
            params = {
                'realm_slug': realm_slug,
                'role_name': character_name
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('code') == 0:
                return data['data']['token']
            else:
                print(f"获取角色 {character_name} token失败: {data.get('message')}")
                return None
                
        except Exception as e:
            print(f"获取角色 {character_name} token时发生错误: {e}")
            return None
    
    def get_mythic_data(self, token: str) -> Optional[Dict]:
        """获取大秘境数据"""
        try:
            url = "https://webapi.blizzard.cn/wow-armory-server/api/do"
            params = {
                'api': 'mythic_keystone_season',
                'token': token
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('code') == 0:
                return data['data']
            else:
                print(f"获取大秘境数据失败: {data.get('message')}")
                return None
                
        except Exception as e:
            print(f"获取大秘境数据时发生错误: {e}")
            return None

def load_guild_members(csv_file: str) -> List[GuildMember]:
    """从CSV文件加载公会成员信息"""
    members = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # 只处理80级角色且有Mythic+ Score的角色
                if row['레벨'] == '80' and row['Mythic+ Score'] and row['Mythic+ Score'] != '0':
                    try:
                        mythic_score = int(row['Mythic+ Score'])
                        if mythic_score > 0:  # 只处理有分数的角色
                            member = GuildMember(
                                name=row['Name'],
                                rank=row['Rank'],
                                level=row['레벨'],
                                class_name=row['Class'],
                                race=row['Race'],
                                sex=row['Sex'],
                                last_online=row['Last Online (Days)'],
                                mythic_score=mythic_score,
                                faction=row['Faction']
                            )
                            members.append(member)
                    except ValueError:
                        continue  # 跳过无法解析分数的行
        
        # 按Mythic+ Score降序排序
        members.sort(key=lambda x: x.mythic_score, reverse=True)
        
        print(f"加载了 {len(members)} 个有Mythic+ Score的80级角色")
        return members
        
    except Exception as e:
        print(f"加载公会成员数据时发生错误: {e}")
        return []

def get_mythic_details(api_client: MythicKeystoneAPI, member: GuildMember) -> Optional[MythicData]:
    """获取角色的大秘境详细信息"""
    try:
        # 获取token
        token = api_client.get_character_token(member.realm, member.name)
        if not token:
            return None
        
        # 获取大秘境数据
        mythic_data = api_client.get_mythic_data(token)
        if not mythic_data:
            return None
        
        # 解析数据
        best_runs = mythic_data['best_runs']
        overall_rating = mythic_data['mythic_rating']['rating']
        season_name = mythic_data['season']['season_str']
        
        # 计算统计信息
        if best_runs:
            completed_within_time = sum(1 for run in best_runs if run['is_completed_within_time'])
            completion_rate = (completed_within_time / len(best_runs)) * 100
            highest_level = max(run['keystone_level'] for run in best_runs)
            average_rating = sum(run['mythic_rating']['rating'] for run in best_runs) / len(best_runs)
        else:
            completion_rate = 0
            highest_level = 0
            average_rating = 0
        
        return MythicData(
            character_name=member.name,
            overall_rating=overall_rating,
            season_name=season_name,
            best_runs_count=len(best_runs),
            highest_level=highest_level,
            completion_rate=completion_rate,
            average_rating=average_rating,
            best_runs=best_runs
        )
        
    except Exception as e:
        print(f"获取角色 {member.name} 大秘境数据时发生错误: {e}")
        return None

def format_duration(duration_ms: int) -> str:
    """格式化时间显示"""
    total_seconds = duration_ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def print_top_players(members: List[GuildMember], mythic_details: List[MythicData]):
    """打印前10名玩家的详细信息"""
    print("\n" + "=" * 100)
    print("🏆 公会Mythic+ Score排行榜 (前10名)")
    print("=" * 100)
    
    for i, (member, detail) in enumerate(zip(members[:10], mythic_details[:10]), 1):
        print(f"\n{i:2d}. {member.name} ({member.class_name} - {member.race})")
        print(f"    职位: {member.rank} | 阵营: {member.faction} | 最后在线: {member.last_online}天")
        print(f"    CSV中的Mythic+ Score: {member.mythic_score}")
        
        if detail:
            print(f"    API总体评分: {detail.overall_rating:.2f}")
            print(f"    赛季: {detail.season_name}")
            print(f"    最佳记录数: {detail.best_runs_count}")
            print(f"    最高等级: {detail.highest_level}层")
            print(f"    限时完成率: {detail.completion_rate:.1f}%")
            print(f"    平均评分: {detail.average_rating:.2f}")
            
            # 显示最佳记录
            if detail.best_runs:
                print(f"    最佳记录:")
                for j, run in enumerate(detail.best_runs[:3], 1):  # 只显示前3条
                    status = "✅" if run['is_completed_within_time'] else "❌"
                    duration = format_duration(run['duration'])
                    print(f"      {j}. {status} {run['dungeon']['name']} {run['keystone_level']}层 "
                          f"({duration}) - 评分: {run['mythic_rating']['rating']:.2f}")
        else:
            print(f"    ❌ 无法获取API数据")
        
        print("-" * 80)

def save_results(members: List[GuildMember], mythic_details: List[MythicData], filename: str):
    """保存结果到JSON文件"""
    try:
        results = []
        
        for member, detail in zip(members[:10], mythic_details[:10]):
            result = {
                'name': member.name,
                'rank': member.rank,
                'class': member.class_name,
                'race': member.race,
                'faction': member.faction,
                'last_online': member.last_online,
                'csv_mythic_score': member.mythic_score,
                'api_data': None
            }
            
            if detail:
                result['api_data'] = {
                    'overall_rating': detail.overall_rating,
                    'season': detail.season_name,
                    'best_runs_count': detail.best_runs_count,
                    'highest_level': detail.highest_level,
                    'completion_rate': detail.completion_rate,
                    'average_rating': detail.average_rating,
                    'best_runs': [
                        {
                            'dungeon': run['dungeon']['name'],
                            'level': run['keystone_level'],
                            'duration': run['duration'],
                            'completed_within_time': run['is_completed_within_time'],
                            'rating': run['mythic_rating']['rating'],
                            'affixes': [affix['name'] for affix in run['keystone_affixes']]
                        }
                        for run in detail.best_runs[:5]  # 只保存前5条记录
                    ]
                }
            
            results.append(result)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 结果已保存到: {filename}")
        
    except Exception as e:
        print(f"保存结果时发生错误: {e}")

def main():
    """主函数"""
    print("🏆 获取公会Mythic+ Score最高的10个角色详细信息")
    print("=" * 60)
    
    # 获取Cookie Token
    cookie_token = input("请输入blizzard_user_info cookie值: ").strip()
    if not cookie_token:
        print("❌ Cookie Token不能为空")
        return
    
    # 创建API客户端
    api_client = MythicKeystoneAPI(cookie_token)
    
    # 加载公会成员数据
    print("\n📊 正在加载公会成员数据...")
    members = load_guild_members("data/guildmember.csv")
    
    if not members:
        print("❌ 没有找到有效的公会成员数据")
        return
    
    # 显示前10名
    print(f"\n📋 CSV中的前10名Mythic+ Score:")
    for i, member in enumerate(members[:10], 1):
        print(f"{i:2d}. {member.name} ({member.class_name}) - {member.mythic_score}分")
    
    # 获取详细信息
    print(f"\n🔍 正在获取前10名角色的详细大秘境数据...")
    mythic_details = []
    
    for i, member in enumerate(members[:10], 1):
        print(f"正在处理 {i}/10: {member.name}...")
        
        detail = get_mythic_details(api_client, member)
        mythic_details.append(detail)
        
        # 添加延迟避免请求过快
        time.sleep(1)
    
    # 显示结果
    print_top_players(members, mythic_details)
    
    # 保存结果
    save_results(members, mythic_details, "top_mythic_players.json")
    
    # 统计信息
    successful_count = sum(1 for detail in mythic_details if detail is not None)
    print(f"\n📈 统计信息:")
    print(f"成功获取数据: {successful_count}/10")
    print(f"成功率: {successful_count/10*100:.1f}%")

if __name__ == "__main__":
    main() 