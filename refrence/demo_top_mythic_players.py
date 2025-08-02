#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示：获取公会Mythic+ Score最高的10个角色详细信息
"""

import csv
import json
import requests
import time
from typing import List, Dict, Optional

def load_top_players(csv_file: str, limit: int = 10) -> List[Dict]:
    """加载Mythic+ Score最高的角色"""
    members = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # 只处理80级角色且有Mythic+ Score的角色
                if row['레벨'] == '80' and row['Mythic+ Score'] and row['Mythic+ Score'] != '0':
                    try:
                        mythic_score = int(row['Mythic+ Score'])
                        if mythic_score > 0:
                            members.append({
                                'name': row['Name'],
                                'class': row['Class'],
                                'race': row['Race'],
                                'faction': row['Faction'],
                                'rank': row['Rank'],
                                'last_online': row['Last Online (Days)'],
                                'mythic_score': mythic_score
                            })
                    except ValueError:
                        continue
        
        # 按Mythic+ Score降序排序
        members.sort(key=lambda x: x['mythic_score'], reverse=True)
        
        print(f"✅ 找到 {len(members)} 个有Mythic+ Score的80级角色")
        return members[:limit]
        
    except Exception as e:
        print(f"❌ 加载数据失败: {e}")
        return []

def get_character_token(session: requests.Session, realm: str, character: str) -> Optional[str]:
    """获取角色访问令牌"""
    try:
        url = "https://webapi.blizzard.cn/wow-armory-server/api/index"
        params = {
            'realm_slug': realm,
            'role_name': character
        }
        
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('code') == 0:
            return data['data']['token']
        else:
            print(f"获取 {character} token失败: {data.get('message')}")
            return None
            
    except Exception as e:
        print(f"获取 {character} token错误: {e}")
        return None

def get_mythic_data(session: requests.Session, token: str) -> Optional[Dict]:
    """获取大秘境数据"""
    try:
        url = "https://webapi.blizzard.cn/wow-armory-server/api/do"
        params = {
            'api': 'mythic_keystone_season',
            'token': token
        }
        
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('code') == 0:
            return data['data']
        else:
            print(f"获取大秘境数据失败: {data.get('message')}")
            return None
            
    except Exception as e:
        print(f"获取大秘境数据错误: {e}")
        return None

def format_duration(duration_ms: int) -> str:
    """格式化时间显示"""
    total_seconds = duration_ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def analyze_mythic_data(mythic_data: Dict) -> Dict:
    """分析大秘境数据"""
    best_runs = mythic_data['best_runs']
    overall_rating = mythic_data['mythic_rating']['rating']
    season_name = mythic_data['season']['season_str']
    
    if best_runs:
        completed_within_time = sum(1 for run in best_runs if run['is_completed_within_time'])
        completion_rate = (completed_within_time / len(best_runs)) * 100
        highest_level = max(run['keystone_level'] for run in best_runs)
        average_rating = sum(run['mythic_rating']['rating'] for run in best_runs) / len(best_runs)
    else:
        completion_rate = 0
        highest_level = 0
        average_rating = 0
    
    return {
        'overall_rating': overall_rating,
        'season': season_name,
        'best_runs_count': len(best_runs),
        'highest_level': highest_level,
        'completion_rate': completion_rate,
        'average_rating': average_rating,
        'best_runs': best_runs[:3]  # 只取前3条记录
    }

def print_player_info(player: Dict, mythic_data: Optional[Dict]):
    """打印玩家信息"""
    print(f"\n🏆 {player['name']} ({player['class']} - {player['race']})")
    print(f"   职位: {player['rank']} | 阵营: {player['faction']} | 最后在线: {player['last_online']}天")
    print(f"   CSV中的Mythic+ Score: {player['mythic_score']}")
    
    if mythic_data:
        print(f"   API总体评分: {mythic_data['overall_rating']:.2f}")
        print(f"   赛季: {mythic_data['season']}")
        print(f"   最佳记录数: {mythic_data['best_runs_count']}")
        print(f"   最高等级: {mythic_data['highest_level']}层")
        print(f"   限时完成率: {mythic_data['completion_rate']:.1f}%")
        print(f"   平均评分: {mythic_data['average_rating']:.2f}")
        
        if mythic_data['best_runs']:
            print(f"   最佳记录:")
            for i, run in enumerate(mythic_data['best_runs'], 1):
                status = "✅" if run['is_completed_within_time'] else "❌"
                duration = format_duration(run['duration'])
                affixes = [affix['name'] for affix in run['keystone_affixes']]
                print(f"     {i}. {status} {run['dungeon']['name']} {run['keystone_level']}层")
                print(f"        时间: {duration} | 评分: {run['mythic_rating']['rating']:.2f}")
                print(f"        词缀: {', '.join(affixes)}")
    else:
        print(f"   ❌ 无法获取API数据")
    
    print("-" * 80)

def main():
    """主函数"""
    print("🏆 公会Mythic+ Score排行榜分析")
    print("=" * 60)
    
    # 加载前10名角色
    print("\n📊 正在分析CSV数据...")
    top_players = load_top_players("data/guildmember.csv", 10)
    
    if not top_players:
        print("❌ 没有找到有效的角色数据")
        return
    
    # 显示前10名
    print(f"\n📋 CSV中的前10名Mythic+ Score:")
    for i, player in enumerate(top_players, 1):
        print(f"{i:2d}. {player['name']} ({player['class']}) - {player['mythic_score']}分")
    
    # 询问是否获取API数据
    print(f"\n❓ 是否要获取这些角色的详细大秘境数据？")
    print("注意：这需要有效的blizzard_user_info cookie值")
    choice = input("输入 'y' 继续，其他键跳过API获取: ").strip().lower()
    
    if choice != 'y':
        print("\n📋 仅显示CSV数据:")
        for i, player in enumerate(top_players, 1):
            print(f"{i:2d}. {player['name']} ({player['class']} - {player['race']})")
            print(f"    职位: {player['rank']} | 阵营: {player['faction']}")
            print(f"    Mythic+ Score: {player['mythic_score']} | 最后在线: {player['last_online']}天")
            print("-" * 60)
        return
    
    # 获取Cookie Token
    cookie_token = input("\n请输入blizzard_user_info cookie值: ").strip()
    if not cookie_token:
        print("❌ Cookie Token不能为空")
        return
    
    # 创建会话
    session = requests.Session()
    session.headers.update({
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin': 'https://wow.blizzard.cn',
        'referer': 'https://wow.blizzard.cn/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    })
    session.cookies.set('blizzard_user_info', cookie_token, domain='.blizzard.cn')
    
    # 获取详细信息
    print(f"\n🔍 正在获取前10名角色的详细大秘境数据...")
    results = []
    
    for i, player in enumerate(top_players, 1):
        print(f"正在处理 {i}/10: {player['name']}...")
        
        # 获取token
        token = get_character_token(session, "arthas", player['name'])
        if not token:
            print(f"   ❌ 无法获取 {player['name']} 的token")
            results.append((player, None))
            continue
        
        # 获取大秘境数据
        mythic_data = get_mythic_data(session, token)
        if mythic_data:
            analyzed_data = analyze_mythic_data(mythic_data)
            results.append((player, analyzed_data))
            print(f"   ✅ 成功获取 {player['name']} 的数据")
        else:
            results.append((player, None))
            print(f"   ❌ 无法获取 {player['name']} 的大秘境数据")
        
        # 添加延迟避免请求过快
        time.sleep(1)
    
    # 显示结果
    print("\n" + "=" * 100)
    print("🏆 公会Mythic+ Score排行榜详细分析")
    print("=" * 100)
    
    for player, mythic_data in results:
        print_player_info(player, mythic_data)
    
    # 统计信息
    successful_count = sum(1 for _, mythic_data in results if mythic_data is not None)
    print(f"\n📈 统计信息:")
    print(f"成功获取数据: {successful_count}/10")
    print(f"成功率: {successful_count/10*100:.1f}%")
    
    # 保存结果
    try:
        output_data = []
        for player, mythic_data in results:
            result = {
                'name': player['name'],
                'class': player['class'],
                'race': player['race'],
                'faction': player['faction'],
                'rank': player['rank'],
                'last_online': player['last_online'],
                'csv_mythic_score': player['mythic_score'],
                'api_data': mythic_data
            }
            output_data.append(result)
        
        with open('top_mythic_players_demo.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 结果已保存到: top_mythic_players_demo.json")
        
    except Exception as e:
        print(f"保存结果时发生错误: {e}")

if __name__ == "__main__":
    main() 