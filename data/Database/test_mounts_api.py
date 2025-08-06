#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试魔兽世界坐骑API
验证API调用是否正常工作
"""

import requests
import json
from config import config

def test_mounts_api():
    """测试坐骑API调用"""
    print("=== 测试魔兽世界坐骑API ===")
    
    # 获取配置
    base_url = config.get("api.base_url")
    headers = config.get("api.headers")
    token = config.get("tokens.default")
    
    print(f"API地址: {base_url}")
    print(f"使用令牌: {token[:10]}...")
    
    # 测试参数
    test_params = {
        "api": "mounts",
        "token": token,
        "attr": "HORDE"  # 测试部落阵营
    }
    
    try:
        print("\n正在发送请求...")
        response = requests.get(
            base_url,
            params=test_params,
            headers=headers,
            timeout=30
        )
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            if data.get("code") == 0:
                mounts_data = data.get("data", {})
                print(f"\n✅ API调用成功！")
                print(f"当前坐骑数量: {mounts_data.get('now', 0)}")
                print(f"总坐骑数量: {mounts_data.get('total', 0)}")
                print(f"坐骑列表长度: {len(mounts_data.get('mounts', []))}")
                
                # 显示前几个坐骑
                mounts = mounts_data.get('mounts', [])
                if mounts:
                    print(f"\n前5个坐骑:")
                    for i, mount_info in enumerate(mounts[:5], 1):
                        mount = mount_info.get('mount', {})
                        print(f"  {i}. {mount.get('name', 'N/A')} - {mount.get('description', 'N/A')}")
                
                return True
            else:
                print(f"❌ API返回错误: {data.get('message', '未知错误')}")
                return False
        else:
            print(f"❌ HTTP请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def test_alliance_mounts():
    """测试联盟阵营坐骑"""
    print("\n=== 测试联盟阵营坐骑 ===")
    
    base_url = config.get("api.base_url")
    headers = config.get("api.headers")
    token = config.get("tokens.default")
    
    test_params = {
        "api": "mounts",
        "token": token,
        "attr": "ALLIANCE"
    }
    
    try:
        response = requests.get(
            base_url,
            params=test_params,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0:
                mounts_data = data.get("data", {})
                print(f"✅ 联盟坐骑API调用成功！")
                print(f"当前坐骑数量: {mounts_data.get('now', 0)}")
                print(f"总坐骑数量: {mounts_data.get('total', 0)}")
                return True
            else:
                print(f"❌ 联盟API返回错误: {data.get('message', '未知错误')}")
                return False
        else:
            print(f"❌ 联盟HTTP请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 联盟API测试失败: {e}")
        return False

def main():
    """主函数"""
    print("开始测试魔兽世界坐骑API...")
    
    # 测试部落坐骑
    horde_success = test_mounts_api()
    
    # 测试联盟坐骑
    alliance_success = test_alliance_mounts()
    
    print("\n" + "="*50)
    print("测试结果总结:")
    print(f"部落API: {'✅ 成功' if horde_success else '❌ 失败'}")
    print(f"联盟API: {'✅ 成功' if alliance_success else '❌ 失败'}")
    
    if horde_success and alliance_success:
        print("\n🎉 所有测试通过！API可以正常使用。")
        return True
    else:
        print("\n⚠️  部分测试失败，请检查配置和网络连接。")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1) 