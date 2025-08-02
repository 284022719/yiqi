import requests
import time

def simple_test():
    """简单的API测试"""
    base_url = "http://127.0.0.1:8000"
    
    print("🚀 简单API测试...")
    
    # 等待服务启动
    print("等待服务启动...")
    time.sleep(2)
    
    # 测试健康检查
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ 健康检查: {response.status_code}")
        print(f"   响应: {response.json()}")
    except Exception as e:
        print(f"❌ 健康检查失败: {str(e)}")
        return
    
    # 测试根路径
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"✅ 根路径: {response.status_code}")
    except Exception as e:
        print(f"❌ 根路径失败: {str(e)}")
    
    # 测试API文档
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        print(f"✅ API文档: {response.status_code}")
    except Exception as e:
        print(f"❌ API文档失败: {str(e)}")
    
    print("✅ 测试完成！")

if __name__ == "__main__":
    simple_test() 