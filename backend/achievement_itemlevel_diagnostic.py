#!/usr/bin/env python3
"""
成就和装等数据获取问题诊断工具
专门分析成就和装等数据获取失败的原因
"""

import sqlite3
import requests
import json
import urllib.parse
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

class AchievementItemLevelDiagnostic:
    """成就和装等数据诊断工具"""
    
    def __init__(self):
        self.db_path = "data/guild_members.db"
        self.base_url = "https://webapi.blizzard.cn/wow-armory-server/api"
        self.raider_io_url = "https://raider.io/api/v1/characters/profile"
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://wow.blizzard.cn/',
            'Origin': 'https://wow.blizzard.cn'
        }
        
        # 服务器映射
        self.realm_mapping = {
            '阿尔萨斯': 'arthas', '死亡之翼': 'deathwing', '白银之手': 'silver-hand',
            '罗宁': 'rhonin', '燃烧之刃': 'burning-blade', '祖达克': 'zul-drak',
            '冬泉谷': 'winterspring', '阿克蒙德': 'archimonde', '凤凰之神': 'phoenix-god',
            '国王之谷': 'king-valley', '阿古斯': 'argus', '金色平原': 'golden-plain',
            '斯克提斯': 'skettis', '影之哀伤': 'shadowmourne', '无尽之海': 'endless-sea',
            '巴瑟拉斯': 'barthilas', '克尔苏加德': 'kel-thuzad', '丽丽（四川）': 'lili-sichuan',
            '霜狼': 'frostwolf', '苏拉玛': 'suramar', '红龙军团': 'red-dragon-legion',
            '伊森利恩': 'earthen-ring', '伊利丹': 'illidan', '主宰之剑': 'master-sword',
            '血色十字军': 'scarlet-crusade', '瓦里安': 'varian', '瓦拉纳': 'varana',
            '熊猫酒仙': 'panda-brewmaster', '梅尔加尼': 'malganis', '暴风祭坛': 'storm-altar',
            '安苏': 'anshe', '塞拉摩': 'theramore', '埃德萨拉': 'edessa',
            '冰风岗': 'icewind-post', '黑铁': 'black-iron', '黑暗魅影': 'dark-shadow',
            '风暴峭壁': 'storm-peak', '霜之哀伤': 'frostmourne', '贫瘠之地': 'barrens',
            '诺莫瑞根': 'gnomeregan', '莱索恩': 'lesaune', '符文图腾': 'rune-totem',
            '甜水绿洲': 'sweetwater-oasis', '玛里苟斯': 'malygos', '烈焰荆棘': 'flame-thorn',
            '海克泰尔': 'hectar', '洛萨': 'lothar', '格瑞姆巴托': 'grim-batol',
            '月神殿': 'temple-of-the-moon', '恶魔之翼': 'demon-wing', '布兰卡德': 'brandecard',
            '奥特兰克': 'alterac', '地狱之石': 'hell-stone', '回音山': 'echo-mountain',
            '加里索斯': 'garithos'
        }
    
    def get_test_members(self) -> List[Dict[str, Any]]:
        """获取测试用的成员列表"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 获取有成就数据的成员
            cursor.execute("""
                SELECT name, realm_name, level, class, achievement_points
                FROM guild_members 
                WHERE achievement_points > 0 AND level >= 70
                LIMIT 5
            """)
            achievement_members = [{'name': row[0], 'realm': row[1], 'level': row[2], 
                                   'class': row[3], 'achievement_points': row[4]} 
                                  for row in cursor.fetchall()]
            
            # 获取有装等数据的成员
            cursor.execute("""
                SELECT name, realm_name, level, class, average_item_level
                FROM guild_members 
                WHERE average_item_level > 0 AND level >= 70
                LIMIT 5
            """)
            itemlevel_members = [{'name': row[0], 'realm': row[1], 'level': row[2], 
                                 'class': row[3], 'itemlevel': row[4]} 
                                for row in cursor.fetchall()]
            
            # 获取没有成就数据的成员
            cursor.execute("""
                SELECT name, realm_name, level, class
                FROM guild_members 
                WHERE (achievement_points IS NULL OR achievement_points = 0) 
                AND level >= 70
                LIMIT 5
            """)
            no_achievement_members = [{'name': row[0], 'realm': row[1], 'level': row[2], 
                                      'class': row[3]} 
                                     for row in cursor.fetchall()]
            
            # 获取没有装等数据的成员
            cursor.execute("""
                SELECT name, realm_name, level, class
                FROM guild_members 
                WHERE (average_item_level IS NULL OR average_item_level = 0) 
                AND level >= 70
                LIMIT 5
            """)
            no_itemlevel_members = [{'name': row[0], 'realm': row[1], 'level': row[2], 
                                    'class': row[3]} 
                                   for row in cursor.fetchall()]
            
            conn.close()
            
            return {
                'achievement_members': achievement_members,
                'itemlevel_members': itemlevel_members,
                'no_achievement_members': no_achievement_members,
                'no_itemlevel_members': no_itemlevel_members
            }
            
        except Exception as e:
            print(f"获取测试成员失败: {e}")
            return {}
    
    def test_character_api(self, member: Dict[str, Any]) -> Dict[str, Any]:
        """测试角色API调用"""
        try:
            realm_name = member['realm']
            realm_slug = self.realm_mapping.get(realm_name, realm_name.lower().replace(' ', '-'))
            encoded_name = urllib.parse.quote(member['name'])
            
            url = f"{self.base_url}/index?realm_slug={realm_slug}&role_name={encoded_name}"
            
            print(f"测试API: {member['name']} ({realm_name})")
            print(f"URL: {url}")
            
            response = requests.get(url, headers=self.headers, timeout=15)
            
            result = {
                'member': member,
                'url': url,
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds(),
                'success': False,
                'data': None,
                'error': None
            }
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    result['data'] = data
                    
                    if data.get("code") == 0 and "data" in data:
                        result['success'] = True
                        print(f"  ✅ API调用成功")
                    else:
                        result['error'] = f"API返回错误: {data}"
                        print(f"  ❌ API返回错误: {data}")
                        
                except json.JSONDecodeError as e:
                    result['error'] = f"JSON解析失败: {e}"
                    print(f"  ❌ JSON解析失败: {e}")
            else:
                result['error'] = f"HTTP错误: {response.status_code}"
                print(f"  ❌ HTTP错误: {response.status_code}")
            
            return result
            
        except Exception as e:
            result = {
                'member': member,
                'url': url if 'url' in locals() else 'N/A',
                'status_code': None,
                'response_time': None,
                'success': False,
                'data': None,
                'error': f"请求异常: {str(e)}"
            }
            print(f"  ❌ 请求异常: {str(e)}")
            return result
    
    def test_achievement_api(self, member: Dict[str, Any]) -> Dict[str, Any]:
        """测试成就API调用"""
        try:
            realm_name = member['realm']
            realm_slug = self.realm_mapping.get(realm_name, realm_name.lower().replace(' ', '-'))
            encoded_name = urllib.parse.quote(member['name'])
            
            # 尝试不同的成就API端点
            endpoints = [
                f"{self.base_url}/character-achievement?realm_slug={realm_slug}&role_name={encoded_name}",
                f"{self.base_url}/character-achievements?realm_slug={realm_slug}&role_name={encoded_name}",
                f"{self.base_url}/achievements?realm_slug={realm_slug}&role_name={encoded_name}"
            ]
            
            results = []
            
            for i, url in enumerate(endpoints, 1):
                print(f"  测试成就API端点 {i}: {member['name']}")
                
                try:
                    response = requests.get(url, headers=self.headers, timeout=15)
                    
                    result = {
                        'endpoint': i,
                        'url': url,
                        'status_code': response.status_code,
                        'response_time': response.elapsed.total_seconds(),
                        'success': False,
                        'data': None,
                        'error': None
                    }
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            result['data'] = data
                            
                            if data.get("code") == 0 and "data" in data:
                                result['success'] = True
                                print(f"    ✅ 端点 {i} 成功")
                            else:
                                result['error'] = f"API返回错误: {data}"
                                print(f"    ❌ 端点 {i} 失败: {data}")
                                
                        except json.JSONDecodeError as e:
                            result['error'] = f"JSON解析失败: {e}"
                            print(f"    ❌ 端点 {i} JSON解析失败: {e}")
                    else:
                        result['error'] = f"HTTP错误: {response.status_code}"
                        print(f"    ❌ 端点 {i} HTTP错误: {response.status_code}")
                    
                    results.append(result)
                    
                except Exception as e:
                    result = {
                        'endpoint': i,
                        'url': url,
                        'status_code': None,
                        'response_time': None,
                        'success': False,
                        'data': None,
                        'error': f"请求异常: {str(e)}"
                    }
                    print(f"    ❌ 端点 {i} 请求异常: {str(e)}")
                    results.append(result)
                
                time.sleep(1)  # 避免请求过快
            
            return {
                'member': member,
                'results': results,
                'any_success': any(r['success'] for r in results)
            }
            
        except Exception as e:
            return {
                'member': member,
                'results': [],
                'any_success': False,
                'error': f"测试失败: {str(e)}"
            }
    
    def test_equipment_api(self, member: Dict[str, Any]) -> Dict[str, Any]:
        """测试装备API调用"""
        try:
            realm_name = member['realm']
            realm_slug = self.realm_mapping.get(realm_name, realm_name.lower().replace(' ', '-'))
            encoded_name = urllib.parse.quote(member['name'])
            
            # 尝试不同的装备API端点
            endpoints = [
                f"{self.base_url}/character-equipment?realm_slug={realm_slug}&role_name={encoded_name}",
                f"{self.base_url}/character-equipments?realm_slug={realm_slug}&role_name={encoded_name}",
                f"{self.base_url}/equipment?realm_slug={realm_slug}&role_name={encoded_name}"
            ]
            
            results = []
            
            for i, url in enumerate(endpoints, 1):
                print(f"  测试装备API端点 {i}: {member['name']}")
                
                try:
                    response = requests.get(url, headers=self.headers, timeout=15)
                    
                    result = {
                        'endpoint': i,
                        'url': url,
                        'status_code': response.status_code,
                        'response_time': response.elapsed.total_seconds(),
                        'success': False,
                        'data': None,
                        'error': None
                    }
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            result['data'] = data
                            
                            if data.get("code") == 0 and "data" in data:
                                result['success'] = True
                                print(f"    ✅ 端点 {i} 成功")
                            else:
                                result['error'] = f"API返回错误: {data}"
                                print(f"    ❌ 端点 {i} 失败: {data}")
                                
                        except json.JSONDecodeError as e:
                            result['error'] = f"JSON解析失败: {e}"
                            print(f"    ❌ 端点 {i} JSON解析失败: {e}")
                    else:
                        result['error'] = f"HTTP错误: {response.status_code}"
                        print(f"    ❌ 端点 {i} HTTP错误: {response.status_code}")
                    
                    results.append(result)
                    
                except Exception as e:
                    result = {
                        'endpoint': i,
                        'url': url,
                        'status_code': None,
                        'response_time': None,
                        'success': False,
                        'data': None,
                        'error': f"请求异常: {str(e)}"
                    }
                    print(f"    ❌ 端点 {i} 请求异常: {str(e)}")
                    results.append(result)
                
                time.sleep(1)  # 避免请求过快
            
            return {
                'member': member,
                'results': results,
                'any_success': any(r['success'] for r in results)
            }
            
        except Exception as e:
            return {
                'member': member,
                'results': [],
                'any_success': False,
                'error': f"测试失败: {str(e)}"
            }
    
    def analyze_character_data(self, character_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析角色数据中的成就和装等信息"""
        analysis = {
            'has_achievement_data': False,
            'has_equipment_data': False,
            'achievement_points': None,
            'item_level': None,
            'data_structure': {}
        }
        
        try:
            if character_data and 'data' in character_data:
                data = character_data['data']
                
                # 分析数据结构
                analysis['data_structure'] = {
                    'top_level_keys': list(data.keys()) if isinstance(data, dict) else [],
                    'data_type': type(data).__name__
                }
                
                # 检查character_summary子对象（主要数据源）
                if isinstance(data, dict) and 'character_summary' in data:
                    character_summary = data['character_summary']
                    analysis['data_structure']['character_summary_keys'] = list(character_summary.keys()) if isinstance(character_summary, dict) else []
                    
                    # 检查成就点数
                    if 'achievement_points' in character_summary:
                        analysis['has_achievement_data'] = True
                        analysis['achievement_points'] = character_summary['achievement_points']
                    
                    # 检查装等
                    if 'average_item_level' in character_summary:
                        analysis['has_equipment_data'] = True
                        analysis['item_level'] = character_summary['average_item_level']
                    elif 'equipped_item_level' in character_summary:
                        analysis['has_equipment_data'] = True
                        analysis['item_level'] = character_summary['equipped_item_level']
                
                # 备用检查：直接检查顶层字段
                if not analysis['has_achievement_data'] and isinstance(data, dict):
                    achievement_fields = ['achievement', 'achievements', 'achievement_points', 'points']
                    for field in achievement_fields:
                        if field in data:
                            analysis['has_achievement_data'] = True
                            if isinstance(data[field], (int, float)):
                                analysis['achievement_points'] = data[field]
                            elif isinstance(data[field], dict) and 'points' in data[field]:
                                analysis['achievement_points'] = data[field]['points']
                            break
                
                if not analysis['has_equipment_data'] and isinstance(data, dict):
                    equipment_fields = ['equipment', 'equipments', 'items', 'gear']
                    for field in equipment_fields:
                        if field in data:
                            analysis['has_equipment_data'] = True
                            break
                    
                    itemlevel_fields = ['item_level', 'itemlevel', 'average_item_level', 'ilevel']
                    for field in itemlevel_fields:
                        if field in data:
                            if isinstance(data[field], (int, float)):
                                analysis['item_level'] = data[field]
                            break
                
                print(f"  数据结构分析:")
                print(f"    顶级字段: {analysis['data_structure']['top_level_keys']}")
                if 'character_summary_keys' in analysis['data_structure']:
                    print(f"    character_summary字段: {analysis['data_structure']['character_summary_keys']}")
                print(f"    有成就数据: {analysis['has_achievement_data']}")
                print(f"    有装备数据: {analysis['has_equipment_data']}")
                print(f"    成就点数: {analysis['achievement_points']}")
                print(f"    装等: {analysis['item_level']}")
            
        except Exception as e:
            analysis['error'] = f"数据分析失败: {str(e)}"
            print(f"  数据分析失败: {str(e)}")
        
        return analysis
    
    def run_diagnostic(self):
        """运行完整诊断"""
        print("="*60)
        print("成就和装等数据获取问题诊断")
        print("="*60)
        
        # 获取测试成员
        test_members = self.get_test_members()
        
        if not test_members:
            print("无法获取测试成员数据")
            return
        
        diagnostic_results = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'character_api_tests': [],
            'achievement_api_tests': [],
            'equipment_api_tests': [],
            'data_analysis': []
        }
        
        # 1. 测试基础角色API
        print("\n🔍 1. 测试基础角色API")
        print("-" * 40)
        
        # 测试有成就数据的成员
        for member in test_members.get('achievement_members', []):
            result = self.test_character_api(member)
            diagnostic_results['character_api_tests'].append(result)
            
            if result['success']:
                analysis = self.analyze_character_data(result)
                diagnostic_results['data_analysis'].append({
                    'member': member,
                    'analysis': analysis
                })
        
        # 测试没有成就数据的成员
        for member in test_members.get('no_achievement_members', [])[:2]:
            result = self.test_character_api(member)
            diagnostic_results['character_api_tests'].append(result)
            
            if result['success']:
                analysis = self.analyze_character_data(result)
                diagnostic_results['data_analysis'].append({
                    'member': member,
                    'analysis': analysis
                })
        
        # 2. 测试成就API
        print("\n🏆 2. 测试成就API")
        print("-" * 40)
        
        for member in test_members.get('no_achievement_members', [])[:3]:
            result = self.test_achievement_api(member)
            diagnostic_results['achievement_api_tests'].append(result)
        
        # 3. 测试装备API
        print("\n⚔️ 3. 测试装备API")
        print("-" * 40)
        
        for member in test_members.get('no_itemlevel_members', [])[:3]:
            result = self.test_equipment_api(member)
            diagnostic_results['equipment_api_tests'].append(result)
        
        # 4. 生成诊断报告
        print("\n📊 4. 诊断结果总结")
        print("-" * 40)
        
        # 统计成功率
        character_success = sum(1 for r in diagnostic_results['character_api_tests'] if r['success'])
        character_total = len(diagnostic_results['character_api_tests'])
        
        achievement_success = sum(1 for r in diagnostic_results['achievement_api_tests'] if r['any_success'])
        achievement_total = len(diagnostic_results['achievement_api_tests'])
        
        equipment_success = sum(1 for r in diagnostic_results['equipment_api_tests'] if r['any_success'])
        equipment_total = len(diagnostic_results['equipment_api_tests'])
        
        print(f"基础角色API成功率: {character_success}/{character_total} ({character_success/character_total*100:.1f}%)")
        print(f"成就API成功率: {achievement_success}/{achievement_total} ({achievement_success/achievement_total*100:.1f}%)")
        print(f"装备API成功率: {equipment_success}/{equipment_total} ({equipment_success/equipment_total*100:.1f}%)")
        
        # 分析数据结构
        successful_analyses = [a for a in diagnostic_results['data_analysis'] if a['analysis']['has_achievement_data'] or a['analysis']['has_equipment_data']]
        print(f"有成就/装备数据的角色: {len(successful_analyses)}/{len(diagnostic_results['data_analysis'])}")
        
        # 保存诊断结果
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"data/achievement_itemlevel_diagnostic_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(diagnostic_results, f, ensure_ascii=False, indent=2)
            print(f"\n诊断结果已保存到: {filename}")
        except Exception as e:
            print(f"保存诊断结果失败: {e}")
        
        return diagnostic_results


def main():
    """主函数"""
    diagnostic = AchievementItemLevelDiagnostic()
    diagnostic.run_diagnostic()


if __name__ == "__main__":
    main() 