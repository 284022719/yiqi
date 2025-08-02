#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取公会成员中Mythic+ Score最高的10个角色的基础信息
基于CSV文件数据，无需API密钥
"""

import pandas as pd
from typing import List, Dict, Any

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
            'last_online': row['Last Online (Days)'],
            'guild': row.get('Rank', '未知'),  # 使用Rank列作为公会信息
            'sex': row['Sex']
        }
        result.append(player_info)
    
    return result

def display_top_players_info(top_players: List[Dict[str, Any]]):
    """显示顶级玩家的信息"""
    print("\n" + "="*100)
    print("🏆 公会Mythic+ Score最高的10个角色")
    print("="*100)
    
    print(f"{'排名':<4} {'角色名':<15} {'职业':<8} {'种族':<10} {'等级':<4} {'分数':<8} {'阵营':<8} {'公会职位':<12} {'离线天数':<8}")
    print("-" * 100)
    
    for i, player in enumerate(top_players, 1):
        print(f"{i:<4} {player['name']:<15} {player['class']:<8} {player['race']:<10} "
              f"{player['level']:<4} {player['mythic_score']:<8} {player['faction']:<8} "
              f"{player['rank']:<12} {player['last_online']:<8}")
    
    print("\n" + "="*100)
    print("📊 详细角色信息")
    print("="*100)
    
    for i, player in enumerate(top_players, 1):
        print(f"\n{i}. {player['name']} ({player['class']} - {player['race']})")
        print(f"   Mythic+ Score: {player['mythic_score']}")
        print(f"   等级: {player['level']} | 阵营: {player['faction']}")
        print(f"   公会职位: {player['rank']} | 离线天数: {player['last_online']} 天")
        print(f"   性别: {player['sex']}")
        print("-" * 60)

def analyze_statistics(df: pd.DataFrame, top_players: List[Dict[str, Any]]):
    """分析统计数据"""
    print("\n" + "="*100)
    print("📈 统计分析")
    print("="*100)
    
    # 总体统计
    total_members = len(df)
    members_with_score = len(df[df['Mythic+ Score'] > 0])
    avg_score = df['Mythic+ Score'].mean()
    max_score = df['Mythic+ Score'].max()
    
    print(f"公会总成员数: {total_members}")
    print(f"有Mythic+ Score的成员: {members_with_score}")
    print(f"平均Mythic+ Score: {avg_score:.2f}")
    print(f"最高Mythic+ Score: {max_score}")
    
    # 职业分布
    print(f"\n🏆 前10名职业分布:")
    class_counts = {}
    for player in top_players:
        class_name = player['class']
        class_counts[class_name] = class_counts.get(class_name, 0) + 1
    
    for class_name, count in sorted(class_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {class_name}: {count} 人")
    
    # 阵营分布
    print(f"\n🏆 前10名阵营分布:")
    faction_counts = {}
    for player in top_players:
        faction = player['faction']
        faction_counts[faction] = faction_counts.get(faction, 0) + 1
    
    for faction, count in sorted(faction_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {faction}: {count} 人")

def main():
    """主函数"""
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
    display_top_players_info(top_players)
    
    # 分析统计数据
    analyze_statistics(df, top_players)
    
    # 保存结果到CSV文件
    result_df = pd.DataFrame(top_players)
    result_df.to_csv('top_mplus_players_result.csv', index=False, encoding='utf-8-sig')
    
    print(f"\n✅ 结果已保存到 top_mplus_players_result.csv")
    print("\n💡 提示: 如需获取更详细的角色信息，请运行 get_top_mplus_players.py 并提供Battle.net API密钥")

if __name__ == "__main__":
    main() 