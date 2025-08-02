#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取公会成员中Mythic+ Score最高的10个角色的详细信息
使用mythic-keystone-api获取角色数据
"""

import pandas as pd
import requests
import json
import time
from typing import List, Dict, Any

class MythicKeystoneAPI:
    """Mythic Keystone API 客户端"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://eu.api.blizzard.com"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Battlenet-Namespace": "profile-eu",
            "Accept": "application/json"
        }
    
    def get_character_profile(self, realm: str, character_name: str) -> Dict[str, Any]:
        """获取角色档案信息"""
        url = f"{self.base_url}/profile/wow/character/{realm}/{character_name}"
        params = {
            "locale": "zh_CN",
            "access_token": self.api_key
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"获取角色 {character_name} 信息失败: {e}")
            return {}
    
    def get_character_mythic_keystone_profile(self, realm: str, character_name: str) -> Dict[str, Any]:
        """获取角色的Mythic+ Keystone档案"""
        url = f"{self.base_url}/profile/wow/character/{realm}/{character_name}/mythic-keystone-profile"
        params = {
            "locale": "zh_CN",
            "access_token": self.api_key
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"获取角色 {character_name} Mythic+信息失败: {e}")
            return {}
    
    def get_character_mythic_keystone_seasons(self, realm: str, character_name: str, season_id: int) -> Dict[str, Any]:
        """获取角色特定赛季的Mythic+ Keystone信息"""
        url = f"{self.base_url}/profile/wow/character/{realm}/{character_name}/mythic-keystone-profile/season/{season_id}"
        params = {
            "locale": "zh_CN",
            "access_token": self.api_key
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"获取角色 {character_name} 赛季 {season_id} 信息失败: {e}")
            return {}

def load_guild_members(csv_file: str) -> pd.DataFrame:
    """加载公会成员CSV文件"""
    try:
        df = pd.read_csv(csv_file)
        # 确保Mythic+ Score列是数值类型
        df['Mythic+ Score'] = pd.to_numeric(df['Mythic+ Score'], errors='coerce').fillna(0)
        return df
    except Exception as e:
        print(f"读取CSV文件失败: {e}")
        return pd.DataFrame()

def get_top_mplus_players(df: pd.DataFrame, top_n: int = 10) -> List[Dict[str, Any]]:
    """获取Mythic+ Score最高的玩家"""
    # 按Mythic+ Score降序排序，获取前N名
    top_players = df.nlargest(top_n, 'Mythic+ Score')
    
    result = []
    for _, row in top_players.iterrows():
        player_info = {
            'name': row['Name'],
            'class': row['Class'],
            'race': row['Race'],
            'level': row['레벨'],
            'faction': row['Faction'],
            'mythic_score': row['Mythic+ Score'],
            'rank': row['Rank'],
            'last_online': row['Last Online (Days)']
        }
        result.append(player_info)
    
    return result

def get_detailed_character_info(api: MythicKeystoneAPI, character_name: str, realm: str = "安德麦") -> Dict[str, Any]:
    """获取角色的详细信息"""
    print(f"正在获取角色 {character_name} 的详细信息...")
    
    # 获取基础角色信息
    profile = api.get_character_profile(realm, character_name)
    
    # 获取Mythic+ Keystone档案
    keystone_profile = api.get_character_mythic_keystone_profile(realm, character_name)
    
    # 获取当前赛季信息（假设是第4赛季）
    current_season = api.get_character_mythic_keystone_seasons(realm, character_name, 4)
    
    detailed_info = {
        'name': character_name,
        'realm': realm,
        'profile': profile,
        'keystone_profile': keystone_profile,
        'current_season': current_season
    }
    
    # 添加延迟以避免API限制
    time.sleep(0.1)
    
    return detailed_info

def display_top_players_info(top_players: List[Dict[str, Any]], detailed_info: List[Dict[str, Any]]):
    """显示顶级玩家的信息"""
    print("\n" + "="*80)
    print("🏆 公会Mythic+ Score最高的10个角色")
    print("="*80)
    
    for i, (player, detailed) in enumerate(zip(top_players, detailed_info), 1):
        print(f"\n{i}. {player['name']} ({player['class']} - {player['race']})")
        print(f"   Mythic+ Score: {player['mythic_score']}")
        print(f"   等级: {player['level']} | 阵营: {player['faction']}")
        print(f"   公会职位: {player['rank']} | 离线天数: {player['last_online']}")
        
        # 显示API获取的详细信息
        if detailed.get('profile'):
            profile = detailed['profile']
            if 'level' in profile:
                print(f"   API等级: {profile['level']}")
            if 'character_class' in profile:
                print(f"   API职业: {profile['character_class']['name']}")
            if 'active_spec' in profile:
                print(f"   API专精: {profile['active_spec']['name']}")
        
        if detailed.get('keystone_profile'):
            keystone = detailed['keystone_profile']
            if 'current_period' in keystone:
                current = keystone['current_period']
                if 'best_runs' in current:
                    print(f"   本周最佳记录: {len(current['best_runs'])} 次")
        
        if detailed.get('current_season'):
            season = detailed['current_season']
            if 'best_runs' in season:
                print(f"   本赛季最佳记录: {len(season['best_runs'])} 次")
        
        print("-" * 60)

def main():
    """主函数"""
    # 配置API密钥（需要用户提供）
    api_key = input("请输入您的Battle.net API密钥: ").strip()
    
    if not api_key:
        print("错误: 需要提供API密钥才能继续")
        return
    
    # 初始化API客户端
    api = MythicKeystoneAPI(api_key)
    
    # 加载公会成员数据
    print("正在加载公会成员数据...")
    df = load_guild_members("data/guildmember.csv")
    
    if df.empty:
        print("无法加载公会成员数据")
        return
    
    # 获取Mythic+ Score最高的10个角色
    print("正在分析Mythic+ Score...")
    top_players = get_top_mplus_players(df, 10)
    
    if not top_players:
        print("没有找到有效的Mythic+ Score数据")
        return
    
    # 显示基础信息
    print("\n" + "="*80)
    print("📊 基础排名信息")
    print("="*80)
    
    for i, player in enumerate(top_players, 1):
        print(f"{i:2d}. {player['name']:<15} | {player['class']:<8} | Score: {player['mythic_score']:>6} | {player['faction']}")
    
    # 获取详细信息
    print(f"\n正在通过API获取详细信息...")
    detailed_info = []
    
    for player in top_players:
        detailed = get_detailed_character_info(api, player['name'])
        detailed_info.append(detailed)
    
    # 显示详细信息
    display_top_players_info(top_players, detailed_info)
    
    # 保存结果到JSON文件
    result_data = {
        'timestamp': pd.Timestamp.now().isoformat(),
        'top_players': top_players,
        'detailed_info': detailed_info
    }
    
    with open('top_mplus_players_result.json', 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 结果已保存到 top_mplus_players_result.json")

if __name__ == "__main__":
    main() 