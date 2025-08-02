import requests
import json
from datetime import datetime

def test_api():
    """测试FastAPI后端API"""
    base_url = "http://127.0.0.1:8000"
    
    print("🚀 开始测试FastAPI后端API...")
    print("=" * 50)
    
    # 测试健康检查
    print("1. 测试健康检查...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.json()}")
    except Exception as e:
        print(f"   错误: {str(e)}")
    
    print("\n" + "=" * 50)
    
    # 测试获取所有成员
    print("2. 测试获取所有成员...")
    try:
        response = requests.get(f"{base_url}/api/members")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   总成员数: {data.get('total', 0)}")
            print(f"   当前页成员数: {len(data.get('members', []))}")
            if data.get('members'):
                print(f"   第一个成员: {data['members'][0]['name']} - {data['members'][0]['class_name']}")
        else:
            print(f"   错误响应: {response.text}")
    except Exception as e:
        print(f"   错误: {str(e)}")
    
    print("\n" + "=" * 50)
    
    # 测试获取统计信息
    print("3. 测试获取统计信息...")
    try:
        response = requests.get(f"{base_url}/api/statistics/overview")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   总成员数: {data.get('total_members', 0)}")
            print(f"   活跃成员数: {data.get('active_members', 0)}")
            print(f"   在线成员数: {data.get('online_members', 0)}")
            print(f"   职业种类数: {data.get('classes_count', 0)}")
            print(f"   服务器数量: {data.get('realms_count', 0)}")
        else:
            print(f"   错误响应: {response.text}")
    except Exception as e:
        print(f"   错误: {str(e)}")
    
    print("\n" + "=" * 50)
    
    # 测试搜索功能
    print("4. 测试搜索功能...")
    try:
        response = requests.get(f"{base_url}/api/search/members?q=法师")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   搜索结果数: {data.get('total', 0)}")
            print(f"   查询: {data.get('query', '')}")
        else:
            print(f"   错误响应: {response.text}")
    except Exception as e:
        print(f"   错误: {str(e)}")
    
    print("\n" + "=" * 50)
    
    # 测试获取职业分布
    print("5. 测试获取职业分布...")
    try:
        response = requests.get(f"{base_url}/api/statistics/class-distribution")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   职业分布数据: {len(data)} 个职业")
            for class_info in data[:5]:  # 显示前5个职业
                print(f"   {class_info.get('class_name', '')}: {class_info.get('count', 0)} 人")
        else:
            print(f"   错误响应: {response.text}")
    except Exception as e:
        print(f"   错误: {str(e)}")
    
    print("\n" + "=" * 50)
    
    # 测试获取服务器分布
    print("6. 测试获取服务器分布...")
    try:
        response = requests.get(f"{base_url}/api/statistics/realm-distribution")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   服务器分布数据: {len(data)} 个服务器")
            for realm_info in data[:5]:  # 显示前5个服务器
                print(f"   {realm_info.get('realm_name', '')}: {realm_info.get('count', 0)} 人")
        else:
            print(f"   错误响应: {response.text}")
    except Exception as e:
        print(f"   错误: {str(e)}")
    
    print("\n" + "=" * 50)
    
    # 测试获取Mythic+统计
    print("7. 测试获取Mythic+统计...")
    try:
        response = requests.get(f"{base_url}/api/statistics/mythic-plus-stats")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Mythic+统计: {data}")
        else:
            print(f"   错误响应: {response.text}")
    except Exception as e:
        print(f"   错误: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ API测试完成！")

if __name__ == "__main__":
    test_api() 