#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大秘境数据分析脚本
解析API返回的大秘境数据
"""

import json
from datetime import datetime
from typing import Dict, List

def format_duration(duration_ms: int) -> str:
    """格式化时间显示"""
    total_seconds = duration_ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def format_timestamp(timestamp_ms: int) -> str:
    """格式化时间戳显示"""
    dt = datetime.fromtimestamp(timestamp_ms / 1000)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def analyze_mythic_data(data: Dict):
    """分析大秘境数据"""
    
    # 基本信息
    character = data['character']
    mythic_rating = data['mythic_rating']
    season = data['season']
    best_runs = data['best_runs']
    
    print("=" * 60)
    print(f"角色: {character['name']} ({character['realm']['name']})")
    print(f"赛季: {season['season_str']}")
    print(f"总体评分: {mythic_rating['rating']:.2f}")
    print(f"最佳记录数量: {len(best_runs)}")
    print("=" * 60)
    
    # 分析最佳记录
    print(f"\n📊 最佳记录分析:")
    print("-" * 80)
    
    total_runs = len(best_runs)
    completed_within_time = sum(1 for run in best_runs if run['is_completed_within_time'])
    completion_rate = (completed_within_time / total_runs) * 100
    
    print(f"总记录数: {total_runs}")
    print(f"限时完成: {completed_within_time} ({completion_rate:.1f}%)")
    
    # 等级统计
    levels = [run['keystone_level'] for run in best_runs]
    avg_level = sum(levels) / len(levels)
    max_level = max(levels)
    print(f"平均等级: {avg_level:.1f}")
    print(f"最高等级: {max_level}")
    
    # 地下城统计
    dungeon_stats = {}
    for run in best_runs:
        dungeon_name = run['dungeon']['name']
        if dungeon_name not in dungeon_stats:
            dungeon_stats[dungeon_name] = {
                'count': 0,
                'highest_level': 0,
                'completed_within_time': 0
            }
        
        stats = dungeon_stats[dungeon_name]
        stats['count'] += 1
        stats['highest_level'] = max(stats['highest_level'], run['keystone_level'])
        if run['is_completed_within_time']:
            stats['completed_within_time'] += 1
    
    print(f"\n🏰 地下城统计:")
    for dungeon_name, stats in dungeon_stats.items():
        completion_rate = (stats['completed_within_time'] / stats['count']) * 100
        print(f"  {dungeon_name}: {stats['count']}次, 最高{stats['highest_level']}层, "
              f"完成率{completion_rate:.1f}%")
    
    # 显示详细记录
    print(f"\n📋 详细记录 (前10条):")
    print("-" * 80)
    
    for i, run in enumerate(best_runs[:10], 1):
        status = "✅" if run['is_completed_within_time'] else "❌"
        duration = format_duration(run['duration'])
        date = format_timestamp(run['completed_timestamp'])
        affixes = [affix['name'] for affix in run['keystone_affixes']]
        
        print(f"{i:2d}. {status} {run['dungeon']['name']} {run['keystone_level']}层")
        print(f"    时间: {duration} | 评分: {run['mythic_rating']['rating']:.2f} | 日期: {date}")
        print(f"    词缀: {', '.join(affixes)}")
        print()

def main():
    """主函数"""
    print("大秘境数据分析工具")
    print("请输入API返回的JSON数据 (输入'END'结束):")
    
    # 读取JSON数据
    json_lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        json_lines.append(line)
    
    json_str = '\n'.join(json_lines)
    
    try:
        data = json.loads(json_str)
        
        if data.get('code') == 0 and 'data' in data:
            analyze_mythic_data(data['data'])
        else:
            print("❌ 无效的API响应数据")
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
    except Exception as e:
        print(f"❌ 分析错误: {e}")

if __name__ == "__main__":
    main() 