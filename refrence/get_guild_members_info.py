#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
魔兽世界公会成员信息获取脚本
使用魔兽世界角色信息API获取公会成员详细信息
"""

import csv
import json
import time
import urllib.parse
import requests
from typing import List, Dict, Optional

class WoWCharacterAPI:
    """魔兽世界角色信息API客户端"""
    
    def __init__(self, cookie_token: str):
        """
        初始化API客户端
        
        Args:
            cookie_token: blizzard_user_info cookie值
        """
        self.base_url = "https://webapi.blizzard.cn/wow-armory-server/api/index"
        self.cookie_token = cookie_token
        self.session = requests.Session()
        
        # 设置请求头
        self.session.headers.update({
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'origin': 'https://wow.blizzard.cn',
            'referer': 'https://wow.blizzard.cn/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
        })
        
        # 设置cookie
        self.session.cookies.set('blizzard_user_info', cookie_token, domain='.blizzard.cn')
    
    def get_character_info(self, realm_slug: str, character_name: str) -> Optional[Dict]:
        """
        获取角色信息
        
        Args:
            realm_slug: 服务器标识符
            character_name: 角色名称
            
        Returns:
            角色信息字典或None
        """
        try:
            # URL编码角色名称
            encoded_name = urllib.parse.quote(character_name)
            
            # 构建请求URL
            url = f"{self.base_url}?realm_slug={realm_slug}&role_name={encoded_name}"
            
            # 发送请求
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # 解析响应
            data = response.json()
            
            if data.get('code') == 0:
                return data.get('data')
            else:
                print(f"获取角色 {character_name} 信息失败: {data.get('message', '未知错误')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"请求角色 {character_name} 信息时发生错误: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"解析角色 {character_name} 响应时发生错误: {e}")
            return None
        except Exception as e:
            print(f"获取角色 {character_name} 信息时发生未知错误: {e}")
            return None

def load_guild_members(csv_file: str, limit: int = 10) -> List[Dict]:
    """
    从CSV文件加载公会成员信息
    
    Args:
        csv_file: CSV文件路径
        limit: 限制返回的成员数量
        
    Returns:
        公会成员列表
    """
    members = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # 只处理80级角色
                if row.get('레벨') == '80':
                    members.append({
                        'name': row['Name'],
                        'rank': row['Rank'],
                        'level': row['레벨'],
                        'class': row['Class'],
                        'race': row['Race'],
                        'sex': row['Sex'],
                        'last_online': row['Last Online (Days)'],
                        'faction': row['Faction']
                    })
                    
                    if len(members) >= limit:
                        break
                        
    except FileNotFoundError:
        print(f"找不到文件: {csv_file}")
    except Exception as e:
        print(f"读取CSV文件时发生错误: {e}")
    
    return members

def get_detailed_member_info(api_client: WoWCharacterAPI, members: List[Dict], realm_slug: str = "arthas") -> List[Dict]:
    """
    获取公会成员的详细信息
    
    Args:
        api_client: API客户端
        members: 公会成员列表
        realm_slug: 服务器标识符
        
    Returns:
        包含详细信息的成员列表
    """
    detailed_members = []
    
    for i, member in enumerate(members, 1):
        print(f"正在获取第 {i}/{len(members)} 个成员信息: {member['name']}")
        
        # 获取详细信息
        character_info = api_client.get_character_info(realm_slug, member['name'])
        
        if character_info:
            # 合并基本信息和详细信息
            detailed_member = {
                **member,
                'detailed_info': character_info
            }
            detailed_members.append(detailed_member)
            print(f"✓ 成功获取 {member['name']} 的详细信息")
        else:
            print(f"✗ 获取 {member['name']} 详细信息失败")
        
        # 添加延迟避免请求过于频繁
        time.sleep(1)
    
    return detailed_members

def save_results(members: List[Dict], output_file: str):
    """
    保存结果到JSON文件
    
    Args:
        members: 成员列表
        output_file: 输出文件路径
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(members, file, ensure_ascii=False, indent=2)
        print(f"结果已保存到: {output_file}")
    except Exception as e:
        print(f"保存结果时发生错误: {e}")

def print_summary(members: List[Dict]):
    """
    打印成员信息摘要
    
    Args:
        members: 成员列表
    """
    print("\n" + "="*80)
    print("公会成员详细信息摘要")
    print("="*80)
    
    for i, member in enumerate(members, 1):
        print(f"\n{i}. {member['name']} ({member['class']} - {member['race']})")
        print(f"   等级: {member['level']} | 阵营: {member['faction']} | 最后在线: {member['last_online']}天前")
        
        if 'detailed_info' in member:
            char_info = member['detailed_info'].get('character_summary', {})
            
            # 装备等级
            avg_ilvl = char_info.get('average_item_level', 'N/A')
            equipped_ilvl = char_info.get('equipped_item_level', 'N/A')
            print(f"   平均装等: {avg_ilvl} | 已装备装等: {equipped_ilvl}")
            
            # 成就点数
            achievement_points = char_info.get('achievement_points', 'N/A')
            print(f"   成就点数: {achievement_points}")
            
            # 公会信息
            guild_info = char_info.get('guild', {})
            if guild_info:
                guild_name = guild_info.get('name', 'N/A')
                print(f"   公会: {guild_name}")
            
            # 专精信息
            active_spec = char_info.get('active_spec', {})
            if active_spec:
                spec_name = active_spec.get('name', 'N/A')
                print(f"   当前专精: {spec_name}")
        else:
            print("   详细信息获取失败")

def main():
    """主函数"""
    print("魔兽世界公会成员信息获取工具")
    print("="*50)
    
    # 配置参数
    CSV_FILE = "data/guildmember.csv"
    OUTPUT_FILE = "guild_members_detailed.json"
    REALM_SLUG = "arthas"  # 阿尔萨斯服务器
    MEMBER_LIMIT = 10
    
    # 获取用户输入的cookie token
    print("请输入您的 blizzard_user_info cookie 值:")
    print("(可以从浏览器开发者工具中获取)")
    cookie_token = input("Cookie Token: ").strip()
    
    if not cookie_token:
        print("错误: 必须提供cookie token")
        return
    
    # 创建API客户端
    api_client = WoWCharacterAPI(cookie_token)
    
    # 加载公会成员
    print(f"\n正在从 {CSV_FILE} 加载公会成员信息...")
    members = load_guild_members(CSV_FILE, MEMBER_LIMIT)
    
    if not members:
        print("没有找到符合条件的公会成员")
        return
    
    print(f"找到 {len(members)} 个80级公会成员")
    
    # 获取详细信息
    print(f"\n正在获取前 {len(members)} 个成员的详细信息...")
    detailed_members = get_detailed_member_info(api_client, members, REALM_SLUG)
    
    # 保存结果
    if detailed_members:
        save_results(detailed_members, OUTPUT_FILE)
        
        # 打印摘要
        print_summary(detailed_members)
        
        print(f"\n成功获取了 {len(detailed_members)} 个成员的详细信息")
    else:
        print("没有成功获取任何成员的详细信息")

if __name__ == "__main__":
    main() 