#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
魔兽世界API令牌管理工具
基于官方API文档规范
"""

import os
import sys
import requests
import json
from config import config

class TokenManager:
    def __init__(self):
        self.base_url = "https://webapi.blizzard.cn/wow-armory-server/api/do"
        self.headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "origin": "https://wow.blizzard.cn",
            "referer": "https://wow.blizzard.cn/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/136.0.0.0"
        }
    
    def test_token(self, token: str, faction: str = "HORDE") -> dict:
        """测试令牌有效性"""
        params = {
            "api": "mounts",
            "token": token,
            "attr": faction
        }
        
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("code") == 0:
                    mounts_data = data.get("data", {})
                    return {
                        "valid": True,
                        "mounts_now": mounts_data.get('now', 0),
                        "mounts_total": mounts_data.get('total', 0),
                        "message": "令牌有效"
                    }
                else:
                    return {
                        "valid": False,
                        "error": data.get('message', '未知错误'),
                        "code": data.get('code', -1)
                    }
            else:
                return {
                    "valid": False,
                    "error": f"HTTP错误: {response.status_code}",
                    "code": response.status_code
                }
                
        except Exception as e:
            return {
                "valid": False,
                "error": f"请求异常: {e}",
                "code": -1
            }
    
    def add_realm_token(self, realm: str, token: str) -> bool:
        """添加服务器级别令牌"""
        # 先测试令牌
        test_result = self.test_token(token)
        if not test_result["valid"]:
            print(f"❌ 令牌无效: {test_result['error']}")
            return False
        
        try:
            config.add_realm_token(realm, token)
            print(f"✅ 成功添加服务器 {realm} 的令牌")
            print(f"   坐骑数据: {test_result['mounts_now']}/{test_result['mounts_total']}")
            return True
        except Exception as e:
            print(f"❌ 添加令牌失败: {e}")
            return False
    
    def add_character_token(self, character: str, realm: str, token: str) -> bool:
        """添加角色特定令牌"""
        # 先测试令牌
        test_result = self.test_token(token)
        if not test_result["valid"]:
            print(f"❌ 令牌无效: {test_result['error']}")
            return False
        
        try:
            config.add_character_token(character, realm, token)
            print(f"✅ 成功添加角色 {character}-{realm} 的令牌")
            print(f"   坐骑数据: {test_result['mounts_now']}/{test_result['mounts_total']}")
            return True
        except Exception as e:
            print(f"❌ 添加令牌失败: {e}")
            return False
    
    def set_default_token(self, token: str) -> bool:
        """设置默认令牌"""
        # 先测试令牌
        test_result = self.test_token(token)
        if not test_result["valid"]:
            print(f"❌ 令牌无效: {test_result['error']}")
            return False
        
        try:
            config.set("tokens.default", token)
            config.save_config(config.config)
            print(f"✅ 成功设置默认令牌")
            print(f"   坐骑数据: {test_result['mounts_now']}/{test_result['mounts_total']}")
            return True
        except Exception as e:
            print(f"❌ 设置令牌失败: {e}")
            return False
    
    def list_tokens(self):
        """列出所有已配置的令牌"""
        tokens = config.get_all_tokens()
        
        print("=== 已配置的令牌 ===")
        
        # 默认令牌
        default_token = tokens.get('default', '')
        if default_token:
            test_result = self.test_token(default_token)
            status = "✅" if test_result["valid"] else "❌"
            print(f"{status} 默认令牌: {default_token[:10]}...")
            if test_result["valid"]:
                print(f"   坐骑数据: {test_result['mounts_now']}/{test_result['mounts_total']}")
        else:
            print("❌ 默认令牌: 未配置")
        
        # 服务器级别令牌
        realm_tokens = tokens.get('realms', {})
        if realm_tokens:
            print("\n服务器级别令牌:")
            for realm, token in realm_tokens.items():
                test_result = self.test_token(token)
                status = "✅" if test_result["valid"] else "❌"
                print(f"{status} {realm}: {token[:10]}...")
                if test_result["valid"]:
                    print(f"   坐骑数据: {test_result['mounts_now']}/{test_result['mounts_total']}")
        else:
            print("\n服务器级别令牌: 无")
        
        # 角色特定令牌
        char_tokens = tokens.get('characters', {})
        if char_tokens:
            print("\n角色特定令牌:")
            for char_key, token in char_tokens.items():
                test_result = self.test_token(token)
                status = "✅" if test_result["valid"] else "❌"
                print(f"{status} {char_key}: {token[:10]}...")
                if test_result["valid"]:
                    print(f"   坐骑数据: {test_result['mounts_now']}/{test_result['mounts_total']}")
        else:
            print("\n角色特定令牌: 无")

def main():
    """主函数"""
    print("=== 魔兽世界API令牌管理工具 ===")
    print("基于官方API文档规范")
    
    manager = TokenManager()
    
    while True:
        print("\n请选择操作:")
        print("1. 显示当前令牌配置")
        print("2. 设置默认令牌")
        print("3. 添加服务器级别令牌")
        print("4. 添加角色特定令牌")
        print("5. 测试令牌")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-5): ").strip()
        
        if choice == '0':
            print("👋 再见！")
            break
        elif choice == '1':
            manager.list_tokens()
        elif choice == '2':
            token = input("请输入默认API令牌: ").strip()
            if token:
                manager.set_default_token(token)
            else:
                print("❌ 令牌不能为空")
        elif choice == '3':
            realm = input("请输入服务器名称: ").strip()
            token = input("请输入API令牌: ").strip()
            if realm and token:
                manager.add_realm_token(realm, token)
            else:
                print("❌ 服务器名称和令牌都不能为空")
        elif choice == '4':
            character = input("请输入角色名称: ").strip()
            realm = input("请输入服务器名称: ").strip()
            token = input("请输入API令牌: ").strip()
            if character and realm and token:
                manager.add_character_token(character, realm, token)
            else:
                print("❌ 角色名称、服务器名称和令牌都不能为空")
        elif choice == '5':
            token = input("请输入要测试的API令牌: ").strip()
            faction = input("请输入阵营 (HORDE/ALLIANCE，默认HORDE): ").strip().upper() or "HORDE"
            if token:
                result = manager.test_token(token, faction)
                if result["valid"]:
                    print(f"✅ 令牌有效！")
                    print(f"   坐骑数据: {result['mounts_now']}/{result['mounts_total']}")
                else:
                    print(f"❌ 令牌无效: {result['error']}")
            else:
                print("❌ 令牌不能为空")
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == '__main__':
    main() 