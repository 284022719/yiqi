#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
管理API令牌和其他配置信息
"""

import os
import json
from pathlib import Path
from typing import Dict, Any

from paths import REPO_ROOT


def default_config_path() -> str:
    """按优先级定位配置文件，不依赖调用时的 cwd。

    新位置是 tools/config.json（已在 .gitignore 中），示例见 tools/config.example.json；
    旧位置 data/Database/config.json 只作为兼容回退，仓库里不再跟踪它。
    令牌优先取环境变量 WOW_ARMORY_TOKEN，其次取配置文件的 tokens.default。
    """
    candidates = [
        REPO_ROOT / "tools" / "config.json",
        REPO_ROOT / "data" / "Database" / "config.json",
        REPO_ROOT / "config.json",
        Path.cwd() / "config.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return str(REPO_ROOT / "data" / "Database" / "config.json")


class Config:
    def __init__(self, config_file: str = None):
        """初始化配置"""
        self.config_file = config_file or default_config_path()
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            "api": {
                "base_url": "https://webapi.blizzard.cn/wow-armory-server/api/do",
                "headers": {
                    "accept": "application/json, text/javascript, */*; q=0.01",
                    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                    "priority": "u=1, i",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "xcxtoken": "",
                    "referer": "https://wow.blizzard.cn/"
                },
                "timeout": 30,
                "max_retries": 3
            },
            "crawler": {
                "delay_between_requests": 2,
                "batch_size": 10,
                "max_concurrent": 12
            },
            "database": {
                "path": "../guild_database.db",
                "backup_before_update": True
            },
            "logging": {
                "level": "INFO",
                "file": "logs/mounts_crawler.log",
                "max_size": "10MB",
                "backup_count": 5
            },
            "tokens": {
                # 默认令牌：**不要写进仓库**。用环境变量 WOW_ARMORY_TOKEN 注入，
                # 或放在 tools/config.json（已 gitignore）里。
                "default": "",
                # 角色特定令牌
                "characters": {
                    # "角色名-服务器": "令牌"
                    # "example-arthas": "your_token_here"
                },
                # 服务器级别令牌
                "realms": {
                    # "服务器名": "令牌"
                    # "arthas": "your_token_here"
                }
            }
        }

        token_env = os.environ.get("WOW_ARMORY_TOKEN", "").strip()
        if token_env:
            default_config["tokens"]["default"] = token_env
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # 合并用户配置和默认配置
                    self.merge_config(default_config, user_config)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                print("使用默认配置")
        else:
            # 创建默认配置文件
            self.save_config(default_config)
        
        return default_config
    
    def merge_config(self, default: Dict[str, Any], user: Dict[str, Any]):
        """合并配置"""
        for key, value in user.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                self.merge_config(default[key], value)
            else:
                default[key] = value
    
    def save_config(self, config: Dict[str, Any]):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(f"配置文件已保存到: {self.config_file}")
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_token(self, character_name: str = None, realm_slug: str = None) -> str:
        """获取访问令牌"""
        if character_name and realm_slug:
            # 尝试获取特定角色的令牌
            character_key = f"{character_name}-{realm_slug}"
            specific_token = self.get(f"tokens.characters.{character_key}")
            if specific_token:
                return specific_token
            
            # 如果没有特定角色的令牌，尝试获取服务器级别的令牌
            realm_token = self.get(f"tokens.realms.{realm_slug}")
            if realm_token:
                return realm_token
        
        # 返回默认令牌
        return self.get("tokens.default", "")
    
    def add_character_token(self, character_name: str, realm_slug: str, token: str):
        """添加角色令牌"""
        character_key = f"{character_name}-{realm_slug}"
        self.set(f"tokens.characters.{character_key}", token)
        self.save_config(self.config)
    
    def add_realm_token(self, realm_slug: str, token: str):
        """添加服务器级别令牌"""
        self.set(f"tokens.realms.{realm_slug}", token)
        self.save_config(self.config)
    
    def get_all_tokens(self) -> Dict[str, Any]:
        """获取所有令牌信息"""
        return self.get("tokens", {})
    
    def list_configured_tokens(self):
        """列出所有已配置的令牌"""
        tokens = self.get_all_tokens()
        
        print("=== 已配置的令牌 ===")
        print(f"默认令牌: {tokens.get('default', '未配置')[:10]}..." if tokens.get('default') else "默认令牌: 未配置")
        
        if tokens.get('characters'):
            print("\n角色特定令牌:")
            for char_key, token in tokens['characters'].items():
                print(f"  {char_key}: {token[:10]}...")
        else:
            print("\n角色特定令牌: 无")
        
        if tokens.get('realms'):
            print("\n服务器级别令牌:")
            for realm, token in tokens['realms'].items():
                print(f"  {realm}: {token[:10]}...")
        else:
            print("\n服务器级别令牌: 无")

# 全局配置实例
config = Config()

if __name__ == '__main__':
    # 测试配置
    print("API基础URL:", config.get("api.base_url"))
    print("默认令牌:", config.get("tokens.default"))
    print("请求延迟:", config.get("crawler.delay_between_requests")) 