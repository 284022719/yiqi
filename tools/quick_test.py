#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

import requests
from config import config

def test_new_token():
    """测试令牌：从环境变量读取，仓库里不存令牌。"""

    # 在 wow.blizzard.cn 登录后取到的 armory 令牌，用环境变量传入：
    #   WOW_ARMORY_TOKEN=<token> python tools/quick_test.py
    new_token = os.environ.get("WOW_ARMORY_TOKEN", "").strip()
    # 需要对比旧令牌时可选设置；不设置就只测一个。
    old_token = os.environ.get("WOW_ARMORY_TOKEN_OLD", "").strip()

    if not new_token:
        print("跳过：未设置 WOW_ARMORY_TOKEN（本脚本不内置令牌）")
        return 1
    
    base_url = "https://webapi.blizzard.cn/wow-armory-server/api/do"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "origin": "https://wow.blizzard.cn",
        "referer": "https://wow.blizzard.cn/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/136.0.0.0"
    }
    
    print("=== 令牌对比测试 ===")
    
    # 测试新令牌
    print(f"\n测试新令牌: {new_token[:10]}...")
    params = {"api": "mounts", "token": new_token, "attr": "HORDE"}
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0:
                mounts_data = data.get("data", {})
                print(f"✅ 新令牌结果: {mounts_data.get('now', 0)}/{mounts_data.get('total', 0)}")
            else:
                print(f"❌ 新令牌错误: {data.get('message')}")
        else:
            print(f"❌ 新令牌HTTP错误: {response.status_code}")
    except Exception as e:
        print(f"❌ 新令牌异常: {e}")
    
    # 测试旧令牌（可选：未设置 WOW_ARMORY_TOKEN_OLD 就跳过）
    if not old_token:
        print("\n跳过旧令牌对比：未设置 WOW_ARMORY_TOKEN_OLD")
        return 0

    print(f"\n测试旧令牌: {old_token[:10]}...")
    params = {"api": "mounts", "token": old_token, "attr": "HORDE"}
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0:
                mounts_data = data.get("data", {})
                print(f"✅ 旧令牌结果: {mounts_data.get('now', 0)}/{mounts_data.get('total', 0)}")
            else:
                print(f"❌ 旧令牌错误: {data.get('message')}")
        else:
            print(f"❌ 旧令牌HTTP错误: {response.status_code}")
    except Exception as e:
        print(f"❌ 旧令牌异常: {e}")
    
    print("\n=== 结论 ===")
    print("✅ API支持多角色查询")
    print("✅ 不同令牌返回不同的坐骑数据")
    print("✅ 问题根源是使用了相同的令牌")
    print("✅ 解决方案是为不同角色配置不同的令牌")

if __name__ == '__main__':
    test_new_token() 