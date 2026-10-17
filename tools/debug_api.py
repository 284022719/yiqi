#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API调试脚本
测试不同的API调用方式和参数组合
"""

import requests
import json
import time
from config import config

def test_api_variations():
    """测试不同的API调用方式"""
    
    base_url = config.get("api.base_url")
    headers = config.get("api.headers")
    token = config.get_token()
    
    print("=== API调试测试 ===")
    print(f"基础URL: {base_url}")
    print(f"令牌: {token[:10]}..." if token else "无令牌")
    print()
    
    # 测试用例
    test_cases = [
        {
            "name": "原始方式（无角色参数）",
            "params": {
                "api": "mounts",
                "token": token,
                "attr": "ALLIANCE"
            }
        },
        {
            "name": "添加角色参数",
            "params": {
                "api": "mounts",
                "token": token,
                "attr": "ALLIANCE",
                "character": "Acg",
                "realm": "arthas"
            }
        },
        {
            "name": "使用character-mounts API",
            "params": {
                "api": "character-mounts",
                "token": token,
                "attr": "ALLIANCE",
                "character": "Acg",
                "realm": "arthas"
            }
        },
        {
            "name": "使用profile API",
            "params": {
                "api": "profile",
                "token": token,
                "attr": "ALLIANCE",
                "character": "Acg",
                "realm": "arthas"
            }
        },
        {
            "name": "使用character API",
            "params": {
                "api": "character",
                "token": token,
                "attr": "ALLIANCE",
                "character": "Acg",
                "realm": "arthas"
            }
        },
        {
            "name": "添加更多参数",
            "params": {
                "api": "mounts",
                "token": token,
                "attr": "ALLIANCE",
                "character": "Acg",
                "realm": "arthas",
                "region": "cn",
                "locale": "zh_CN"
            }
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"测试 {i}: {case['name']}")
        print(f"参数: {case['params']}")
        
        try:
            response = requests.get(
                base_url,
                params=case['params'],
                headers=headers,
                timeout=30
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"响应代码: {data.get('code', 'N/A')}")
                
                if data.get("code") == 0:
                    mounts_data = data.get("data", {})
                    print(f"✅ 坐骑数据: {mounts_data.get('now', 0)}/{mounts_data.get('total', 0)}")
                else:
                    print(f"❌ 错误信息: {data.get('message', '未知错误')}")
            else:
                print(f"❌ HTTP错误: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
        
        print("-" * 50)
        time.sleep(1)  # 避免请求过快

def test_different_tokens():
    """测试不同令牌的效果"""
    
    base_url = config.get("api.base_url")
    headers = config.get("api.headers")
    
    print("\n=== 测试不同令牌 ===")
    
    # 获取配置中的所有令牌
    tokens = config.config.get("tokens", {})
    
    if "default" in tokens:
        print(f"测试默认令牌: {tokens['default'][:10]}...")
        test_with_token(base_url, headers, tokens["default"], "默认令牌")
    
    if "characters" in tokens:
        for char_key, token in tokens["characters"].items():
            print(f"测试角色令牌 {char_key}: {token[:10]}...")
            test_with_token(base_url, headers, token, f"角色令牌 {char_key}")

def test_with_token(base_url, headers, token, token_name):
    """使用指定令牌测试API"""
    
    params = {
        "api": "mounts",
        "token": token,
        "attr": "ALLIANCE"
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0:
                mounts_data = data.get("data", {})
                print(f"  ✅ {token_name}: {mounts_data.get('now', 0)}/{mounts_data.get('total', 0)}")
            else:
                print(f"  ❌ {token_name}: {data.get('message', '未知错误')}")
        else:
            print(f"  ❌ {token_name}: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ {token_name}: {e}")

def analyze_response_data():
    """分析API响应数据的结构"""
    
    base_url = config.get("api.base_url")
    headers = config.get("api.headers")
    token = config.get_token()
    
    print("\n=== 分析响应数据结构 ===")
    
    params = {
        "api": "mounts",
        "token": token,
        "attr": "ALLIANCE"
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("code") == 0:
                mounts_data = data.get("data", {})
                
                print("响应数据结构分析:")
                print(f"- 当前坐骑数: {mounts_data.get('now')}")
                print(f"- 总坐骑数: {mounts_data.get('total')}")
                
                mounts_list = mounts_data.get("mounts", [])
                print(f"- 坐骑列表长度: {len(mounts_list)}")
                
                # 统计拥有的坐骑
                owned_mounts = [m for m in mounts_list if m.get("is_owned", False)]
                print(f"- 拥有的坐骑数: {len(owned_mounts)}")
                
                # 检查是否有角色信息
                if "character" in mounts_data:
                    print(f"- 角色信息: {mounts_data['character']}")
                else:
                    print("- 响应中未包含角色信息")
                    
                # 检查是否有其他标识信息
                print(f"- 响应键: {list(mounts_data.keys())}")
                
            else:
                print(f"API错误: {data.get('message')}")
        else:
            print(f"HTTP错误: {response.status_code}")
            
    except Exception as e:
        print(f"请求异常: {e}")

if __name__ == '__main__':
    test_api_variations()
    test_different_tokens()
    analyze_response_data()
    
    print("\n=== 调试完成 ===")
    print("\n结论:")
    print("1. 如果所有API调用都返回相同的数据，说明API可能不支持角色参数")
    print("2. 可能需要为每个角色获取独立的令牌")
    print("3. 或者API设计上只返回令牌对应角色的数据") 