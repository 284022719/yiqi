#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试大秘境数据分析功能
"""

import json
from analyze_mythic_data import analyze_mythic_data

def test_analysis():
    """测试数据分析功能"""
    
    # 读取示例数据
    try:
        with open('mythic_data_example.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("🧪 测试大秘境数据分析功能")
        print("=" * 50)
        
        # 分析数据
        if data.get('code') == 0 and 'data' in data:
            analyze_mythic_data(data['data'])
        else:
            print("❌ 无效的API响应数据")
            
    except FileNotFoundError:
        print("❌ 找不到示例数据文件: mythic_data_example.json")
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
    except Exception as e:
        print(f"❌ 测试错误: {e}")

if __name__ == "__main__":
    test_analysis() 