#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
魔兽世界公会工具快速启动脚本
提供菜单选择不同的功能
"""

import os
import sys

def show_menu():
    """显示主菜单"""
    print("\n" + "="*60)
    print("魔兽世界公会工具集")
    print("="*60)
    print("1. 测试API连接")
    print("2. 获取公会成员详细信息")
    print("3. 查看使用说明")
    print("4. 退出")
    print("="*60)

def run_api_test():
    """运行API测试"""
    print("\n正在启动API测试工具...")
    try:
        from test_api import main as test_main
        test_main()
    except ImportError:
        print("错误: 找不到 test_api.py 文件")
    except Exception as e:
        print(f"运行API测试时发生错误: {e}")

def run_guild_members():
    """运行公会成员信息获取"""
    print("\n正在启动公会成员信息获取工具...")
    try:
        from get_guild_members_info import main as guild_main
        guild_main()
    except ImportError:
        print("错误: 找不到 get_guild_members_info.py 文件")
    except Exception as e:
        print(f"运行公会成员信息获取时发生错误: {e}")

def show_help():
    """显示使用说明"""
    print("\n" + "="*60)
    print("使用说明")
    print("="*60)
    print("1. 首先确保已安装依赖: pip install -r requirements.txt")
    print("2. 获取您的 blizzard_user_info cookie:")
    print("   - 访问 https://wow.blizzard.cn/")
    print("   - 登录您的账号")
    print("   - 按F12打开开发者工具")
    print("   - 在Application/存储标签中找到Cookies")
    print("   - 复制 blizzard_user_info 的值")
    print("3. 选择相应的功能进行测试或获取信息")
    print("4. 结果会保存到JSON文件中")
    print("\n详细说明请查看 README_guild_members.md 文件")

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import requests
        print("✓ requests 库已安装")
    except ImportError:
        print("✗ requests 库未安装，请运行: pip install -r requirements.txt")
        return False
    
    try:
        import urllib3
        print("✓ urllib3 库已安装")
    except ImportError:
        print("✗ urllib3 库未安装，请运行: pip install -r requirements.txt")
        return False
    
    return True

def check_files():
    """检查必要文件是否存在"""
    required_files = [
        "data/guildmember.csv",
        "get_guild_members_info.py",
        "test_api.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("✗ 缺少必要文件:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✓ 所有必要文件都存在")
    return True

def main():
    """主函数"""
    print("魔兽世界公会工具集启动中...")
    
    # 检查依赖
    print("\n检查依赖...")
    if not check_dependencies():
        print("\n请先安装依赖后再运行此工具")
        return
    
    # 检查文件
    print("\n检查文件...")
    if not check_files():
        print("\n请确保所有必要文件都存在")
        return
    
    print("\n✓ 环境检查完成，可以正常使用")
    
    while True:
        show_menu()
        choice = input("\n请选择功能 (1-4): ").strip()
        
        if choice == '1':
            run_api_test()
        elif choice == '2':
            run_guild_members()
        elif choice == '3':
            show_help()
        elif choice == '4':
            print("\n感谢使用魔兽世界公会工具集！")
            break
        else:
            print("\n无效选择，请输入 1-4 之间的数字")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main() 