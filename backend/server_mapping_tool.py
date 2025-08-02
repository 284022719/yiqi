#!/usr/bin/env python3
"""
服务器映射管理工具
用于验证、更新和管理服务器英文映射
"""

import json
import os
import requests
import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class ServerMappingTool:
    """服务器映射管理工具"""
    
    def __init__(self):
        self.mapping_file = "data/server_mapping.json"
        self.realm_mapping = self.load_mapping()
        
        # API配置
        self.base_url = "https://webapi.blizzard.cn/wow-armory-server/api"
        self.raider_io_url = "https://raider.io/api/v1/characters/profile"
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://wow.blizzard.cn/',
            'Origin': 'https://wow.blizzard.cn'
        }
    
    def load_mapping(self) -> Dict[str, str]:
        """加载服务器映射"""
        try:
            if os.path.exists(self.mapping_file):
                with open(self.mapping_file, 'r', encoding='utf-8') as f:
                    mapping = json.load(f)
                print(f"成功加载服务器映射，共 {len(mapping)} 个服务器")
                return mapping
            else:
                print(f"映射文件不存在: {self.mapping_file}")
                return {}
        except Exception as e:
            print(f"加载映射文件失败: {e}")
            return {}
    
    def save_mapping(self):
        """保存服务器映射"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.mapping_file), exist_ok=True)
            
            with open(self.mapping_file, 'w', encoding='utf-8') as f:
                json.dump(self.realm_mapping, f, ensure_ascii=False, indent=2)
            print(f"服务器映射已保存到: {self.mapping_file}")
        except Exception as e:
            print(f"保存映射文件失败: {e}")
    
    def test_server_slug(self, realm_name: str, realm_slug: str) -> bool:
        """测试服务器slug是否有效"""
        try:
            # 使用一个测试角色名
            test_name = "TestCharacter"
            encoded_name = urllib.parse.quote(test_name)
            
            # 测试暴雪API
            url = f"{self.base_url}/index?realm_slug={realm_slug}&role_name={encoded_name}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # 即使角色不存在，如果slug正确，API会返回特定的错误码
                if data.get("code") in [0, 30004]:  # 0=成功, 30004=角色不存在
                    return True
            
            # 测试Raider.io API
            raider_url = f"{self.raider_io_url}?region=cn&realm={realm_slug}&name={test_name}"
            raider_response = requests.get(raider_url, timeout=10)
            
            if raider_response.status_code == 200:
                return True
            
            return False
            
        except Exception as e:
            print(f"测试服务器slug失败 {realm_name} ({realm_slug}): {e}")
            return False
    
    def validate_mapping(self) -> List[Tuple[str, str, bool]]:
        """验证所有服务器映射"""
        print("开始验证服务器映射...")
        results = []
        
        for realm_name, realm_slug in self.realm_mapping.items():
            print(f"验证: {realm_name} → {realm_slug}")
            is_valid = self.test_server_slug(realm_name, realm_slug)
            results.append((realm_name, realm_slug, is_valid))
            
            if is_valid:
                print(f"  ✓ 有效")
            else:
                print(f"  ✗ 无效")
        
        return results
    
    def add_mapping(self, realm_name: str, realm_slug: str):
        """添加新的服务器映射"""
        if realm_name in self.realm_mapping:
            print(f"服务器 {realm_name} 已存在映射: {self.realm_mapping[realm_name]}")
            choice = input("是否要更新? (y/n): ").lower()
            if choice != 'y':
                return
        
        # 验证slug是否有效
        print(f"验证映射: {realm_name} → {realm_slug}")
        if self.test_server_slug(realm_name, realm_slug):
            self.realm_mapping[realm_name] = realm_slug
            self.save_mapping()
            print(f"✓ 成功添加映射: {realm_name} → {realm_slug}")
        else:
            print(f"✗ 映射无效，请检查slug是否正确")
    
    def remove_mapping(self, realm_name: str):
        """删除服务器映射"""
        if realm_name in self.realm_mapping:
            removed_slug = self.realm_mapping.pop(realm_name)
            self.save_mapping()
            print(f"✓ 已删除映射: {realm_name} → {removed_slug}")
        else:
            print(f"服务器 {realm_name} 不存在于映射中")
    
    def generate_slug(self, realm_name: str) -> str:
        """生成可能的slug"""
        # 基本转换规则
        slug = realm_name.lower()
        
        # 替换特殊字符
        replacements = {
            '（': '', '）': '',
            '(': '', ')': '',
            ' ': '-',
            '，': '-',
            ',': '-',
            '：': '-',
            ':': '-',
            '·': '-',
            '、': '-'
        }
        
        for old, new in replacements.items():
            slug = slug.replace(old, new)
        
        # 移除多余的连字符
        while '--' in slug:
            slug = slug.replace('--', '-')
        
        # 移除首尾连字符
        slug = slug.strip('-')
        
        return slug
    
    def suggest_mappings(self, realm_names: List[str]) -> Dict[str, List[str]]:
        """为服务器名称建议可能的slug"""
        suggestions = {}
        
        for realm_name in realm_names:
            if realm_name not in self.realm_mapping:
                # 生成多个可能的slug
                possible_slugs = []
                
                # 1. 基本转换
                basic_slug = self.generate_slug(realm_name)
                possible_slugs.append(basic_slug)
                
                # 2. 移除特殊字符
                clean_slug = realm_name.lower().replace('（', '').replace('）', '').replace(' ', '-')
                if clean_slug != basic_slug:
                    possible_slugs.append(clean_slug)
                
                # 3. 音译映射（常见的中文到英文映射）
                transliteration_map = {
                    '阿尔萨斯': 'arthas',
                    '死亡之翼': 'deathwing',
                    '白银之手': 'silver-hand',
                    '罗宁': 'rhonin',
                    '燃烧之刃': 'burning-blade',
                    '祖达克': 'zul-drak',
                    '冬泉谷': 'winterspring',
                    '阿克蒙德': 'archimonde',
                    '凤凰之神': 'phoenix-god',
                    '国王之谷': 'king-valley',
                    '阿古斯': 'argus',
                    '金色平原': 'golden-plain',
                    '斯克提斯': 'skettis',
                    '影之哀伤': 'shadowmourne',
                    '无尽之海': 'endless-sea',
                    '巴瑟拉斯': 'barthilas',
                    '克尔苏加德': 'kel-thuzad',
                    '丽丽（四川）': 'lili-sichuan',
                    '霜狼': 'frostwolf',
                    '苏拉玛': 'suramar',
                    '红龙军团': 'red-dragon-legion',
                    '伊森利恩': 'earthen-ring',
                    '伊利丹': 'illidan',
                    '主宰之剑': 'master-sword',
                    '血色十字军': 'scarlet-crusade',
                    '瓦里安': 'varian',
                    '瓦拉纳': 'varana',
                    '熊猫酒仙': 'panda-brewmaster',
                    '梅尔加尼': 'malganis',
                    '暴风祭坛': 'storm-altar',
                    '安苏': 'anshe',
                    '塞拉摩': 'theramore',
                    '埃德萨拉': 'edessa',
                    '冰风岗': 'icewind-post',
                    '黑铁': 'black-iron',
                    '黑暗魅影': 'dark-shadow',
                    '风暴峭壁': 'storm-peak',
                    '霜之哀伤': 'frostmourne',
                    '贫瘠之地': 'barrens',
                    '诺莫瑞根': 'gnomeregan',
                    '莱索恩': 'lesaune',
                    '符文图腾': 'rune-totem',
                    '甜水绿洲': 'sweetwater-oasis',
                    '玛里苟斯': 'malygos',
                    '烈焰荆棘': 'flame-thorn',
                    '海克泰尔': 'hectar',
                    '洛萨': 'lothar',
                    '格瑞姆巴托': 'grim-batol',
                    '月神殿': 'temple-of-the-moon',
                    '恶魔之翼': 'demon-wing',
                    '布兰卡德': 'brandecard',
                    '奥特兰克': 'alterac',
                    '地狱之石': 'hell-stone',
                    '回音山': 'echo-mountain',
                    '加里索斯': 'garithos'
                }
                
                if realm_name in transliteration_map:
                    possible_slugs.append(transliteration_map[realm_name])
                
                # 去重并保留顺序
                unique_slugs = []
                for slug in possible_slugs:
                    if slug not in unique_slugs:
                        unique_slugs.append(slug)
                
                suggestions[realm_name] = unique_slugs
        
        return suggestions
    
    def auto_discover_mappings(self, realm_names: List[str]):
        """自动发现服务器映射"""
        print("开始自动发现服务器映射...")
        
        suggestions = self.suggest_mappings(realm_names)
        
        for realm_name, possible_slugs in suggestions.items():
            print(f"\n测试服务器: {realm_name}")
            
            for i, slug in enumerate(possible_slugs, 1):
                print(f"  测试 {i}/{len(possible_slugs)}: {slug}")
                
                if self.test_server_slug(realm_name, slug):
                    print(f"  ✓ 发现有效映射: {realm_name} → {slug}")
                    self.realm_mapping[realm_name] = slug
                    break
            else:
                print(f"  ✗ 未找到有效映射")
        
        # 保存发现的映射
        if suggestions:
            self.save_mapping()
            print(f"\n自动发现完成，共发现 {len([r for r in suggestions.keys() if r in self.realm_mapping])} 个新映射")
    
    def export_mapping_report(self):
        """导出映射报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"data/server_mapping_report_{timestamp}.json"
        
        report = {
            'timestamp': timestamp,
            'total_servers': len(self.realm_mapping),
            'mappings': self.realm_mapping,
            'validation_results': self.validate_mapping()
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"映射报告已导出到: {report_file}")
        except Exception as e:
            print(f"导出报告失败: {e}")
    
    def interactive_mode(self):
        """交互模式"""
        while True:
            print("\n" + "="*50)
            print("服务器映射管理工具")
            print("="*50)
            print("1. 查看所有映射")
            print("2. 验证映射")
            print("3. 添加映射")
            print("4. 删除映射")
            print("5. 导出报告")
            print("6. 退出")
            
            choice = input("\n请选择操作 (1-6): ").strip()
            
            if choice == '1':
                print("\n当前服务器映射:")
                for realm_name, realm_slug in self.realm_mapping.items():
                    print(f"  {realm_name} → {realm_slug}")
            
            elif choice == '2':
                results = self.validate_mapping()
                valid_count = sum(1 for _, _, is_valid in results if is_valid)
                print(f"\n验证结果: {valid_count}/{len(results)} 个映射有效")
            
            elif choice == '3':
                realm_name = input("请输入中文服务器名称: ").strip()
                realm_slug = input("请输入英文slug: ").strip()
                if realm_name and realm_slug:
                    self.add_mapping(realm_name, realm_slug)
            
            elif choice == '4':
                realm_name = input("请输入要删除的服务器名称: ").strip()
                if realm_name:
                    self.remove_mapping(realm_name)
            
            elif choice == '5':
                self.export_mapping_report()
            
            elif choice == '6':
                print("退出程序")
                break
            
            else:
                print("无效选择，请重新输入")


def main():
    """主函数"""
    tool = ServerMappingTool()
    
    if len(os.sys.argv) > 1:
        command = os.sys.argv[1]
        
        if command == 'validate':
            tool.validate_mapping()
        
        elif command == 'add':
            if len(os.sys.argv) >= 4:
                realm_name = os.sys.argv[2]
                realm_slug = os.sys.argv[3]
                tool.add_mapping(realm_name, realm_slug)
            else:
                print("用法: python server_mapping_tool.py add <中文名称> <英文slug>")
        
        elif command == 'remove':
            if len(os.sys.argv) >= 3:
                realm_name = os.sys.argv[2]
                tool.remove_mapping(realm_name)
            else:
                print("用法: python server_mapping_tool.py remove <中文名称>")
        
        elif command == 'report':
            tool.export_mapping_report()
        
        else:
            print("未知命令")
            print("可用命令: validate, add, remove, report")
    else:
        tool.interactive_mode()


if __name__ == "__main__":
    main() 