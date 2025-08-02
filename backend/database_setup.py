#!/usr/bin/env python3
"""
数据库设置脚本
用于初始化数据库并导入现有数据
"""

import os
import sys
import json
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(__file__))

from src.database.models import GuildMemberDB
from src.database.importer import DataImporter
from src.database.api import DatabaseAPI
from src.utils.logger import get_logger

logger = get_logger(__name__)


def setup_database():
    """设置数据库"""
    print("=" * 50)
    print("公会成员数据库设置")
    print("=" * 50)
    
    try:
        # 1. 初始化数据库
        print("\n1. 初始化数据库...")
        db = GuildMemberDB()
        print("✓ 数据库初始化完成")
        
        # 2. 导入CSV数据
        print("\n2. 导入CSV数据...")
        importer = DataImporter()
        
        if os.path.exists("data/memberinfo.csv"):
            csv_result = importer.import_csv_data()
            print(f"✓ CSV数据导入完成: 处理 {csv_result['processed']} 条记录")
            print(f"  - 更新: {csv_result['updated']} 条")
            print(f"  - 错误: {csv_result['errors']} 条")
        else:
            print("⚠ CSV文件不存在，跳过CSV导入")
        
        # 3. 导入增强API数据
        print("\n3. 导入增强API数据...")
        try:
            api_result = importer.import_enhanced_api_data()
            print(f"✓ 增强API数据导入完成: 处理 {api_result['processed']} 条记录")
            print(f"  - 更新: {api_result['updated']} 条")
            print(f"  - 错误: {api_result['errors']} 条")
        except FileNotFoundError:
            print("⚠ 增强API数据文件不存在，跳过API数据导入")
        except Exception as e:
            print(f"⚠ 导入增强API数据时出错: {str(e)}")
        
        # 4. 导出统计信息
        print("\n4. 导出统计信息...")
        importer.export_statistics_to_json()
        print("✓ 统计信息已导出到 data/database_stats.json")
        
        # 5. 测试API功能
        print("\n5. 测试API功能...")
        api = DatabaseAPI()
        
        # 获取统计信息
        stats = api.get_statistics()
        if stats['success']:
            data = stats['data']
            print(f"✓ 数据库统计信息:")
            print(f"  - 总成员数: {data['total_members']}")
            print(f"  - 活跃成员数: {data['active_members']}")
            print(f"  - 职业数量: {len(data['class_distribution'])}")
            print(f"  - 服务器数量: {len(data['server_distribution'])}")
        
        # 获取Mythic+排行榜
        ranking = api.get_top_mythic_players(5)
        if ranking['success']:
            print(f"✓ Mythic+排行榜前5名:")
            for i, player in enumerate(ranking['data']['players'], 1):
                print(f"  {i}. {player['name']} ({player['class']}) - {player['mythic_score']}分")
        
        print("\n" + "=" * 50)
        print("数据库设置完成！")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 数据库设置失败: {str(e)}")
        logger.error(f"数据库设置失败: {str(e)}")
        return False


def test_database_operations():
    """测试数据库操作"""
    print("\n" + "=" * 50)
    print("数据库操作测试")
    print("=" * 50)
    
    try:
        api = DatabaseAPI()
        
        # 测试各种API端点
        test_cases = [
            ("statistics", {}, "获取统计信息"),
            ("mythic_ranking", {"limit": 3}, "获取Mythic+排行榜"),
            ("classes", {}, "获取职业列表"),
            ("realms", {}, "获取服务器列表"),
            ("search", {"q": "Dadie", "limit": 5}, "搜索成员"),
            ("members", {"limit": 5}, "获取成员列表")
        ]
        
        for endpoint, params, description in test_cases:
            print(f"\n测试: {description}")
            
            # 根据端点调用相应的API方法
            if endpoint == "statistics":
                result = api.get_statistics()
            elif endpoint == "mythic_ranking":
                limit = params.get("limit", 10)
                result = api.get_top_mythic_players(limit)
            elif endpoint == "classes":
                result = api.get_available_classes()
            elif endpoint == "realms":
                result = api.get_available_realms()
            elif endpoint == "search":
                query = params.get("q", "")
                limit = params.get("limit", 20)
                result = api.search_members(query, limit)
            elif endpoint == "members":
                limit = params.get("limit", 20)
                result = api.get_all_members(limit)
            else:
                result = {"success": False, "error": f"未知的端点: {endpoint}"}
            
            if result['success']:
                print(f"✓ {description} - 成功")
                if 'data' in result and 'total' in result['data']:
                    print(f"  返回 {result['data']['total']} 条记录")
            else:
                print(f"❌ {description} - 失败: {result.get('error', '未知错误')}")
        
        print("\n" + "=" * 50)
        print("数据库操作测试完成！")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 数据库操作测试失败: {str(e)}")
        logger.error(f"数据库操作测试失败: {str(e)}")
        return False


def export_database_info():
    """导出数据库信息"""
    print("\n" + "=" * 50)
    print("导出数据库信息")
    print("=" * 50)
    
    try:
        api = DatabaseAPI()
        
        # 导出完整数据
        export_result = api.export_data_to_json("data/database_export.json")
        
        if export_result['success']:
            data = export_result['data']
            print(f"✓ 数据库信息已导出到: {data['output_file']}")
            print(f"  - 总成员数: {data['total_members']}")
            print(f"  - 排行榜玩家数: {data['top_players_count']}")
        else:
            print(f"❌ 导出失败: {export_result.get('error', '未知错误')}")
        
        # 导出API文档
        api_docs = {
            "api_version": "1.0",
            "description": "公会成员数据库API",
            "endpoints": {
                "statistics": {
                    "description": "获取公会统计信息",
                    "method": "GET",
                    "parameters": {},
                    "response": "统计信息对象"
                },
                "mythic_ranking": {
                    "description": "获取Mythic+排行榜",
                    "method": "GET",
                    "parameters": {
                        "limit": "返回结果数量限制（可选，默认10）"
                    },
                    "response": "排行榜玩家列表"
                },
                "member": {
                    "description": "获取指定成员信息",
                    "method": "GET",
                    "parameters": {
                        "name": "角色名称（必需）",
                        "realm": "服务器名称（必需）"
                    },
                    "response": "成员详细信息"
                },
                "search": {
                    "description": "搜索成员",
                    "method": "GET",
                    "parameters": {
                        "q": "搜索查询（必需）",
                        "limit": "返回结果数量限制（可选，默认20）"
                    },
                    "response": "搜索结果列表"
                },
                "class": {
                    "description": "根据职业获取成员列表",
                    "method": "GET",
                    "parameters": {
                        "class": "职业名称（必需）"
                    },
                    "response": "该职业的成员列表"
                },
                "realm": {
                    "description": "根据服务器获取成员列表",
                    "method": "GET",
                    "parameters": {
                        "realm": "服务器名称（必需）"
                    },
                    "response": "该服务器的成员列表"
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
        with open("data/api_documentation.json", "w", encoding="utf-8") as f:
            json.dump(api_docs, f, ensure_ascii=False, indent=2)
        
        print(f"✓ API文档已导出到: data/api_documentation.json")
        
        print("\n" + "=" * 50)
        print("数据库信息导出完成！")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 导出数据库信息失败: {str(e)}")
        logger.error(f"导出数据库信息失败: {str(e)}")
        return False


def main():
    """主函数"""
    print("公会成员数据库设置工具")
    print("此工具将帮助您设置数据库并导入现有数据")
    
    # 检查数据目录
    if not os.path.exists("data"):
        os.makedirs("data")
        print("✓ 创建data目录")
    
    # 设置数据库
    if not setup_database():
        print("数据库设置失败，程序退出")
        return
    
    # 测试数据库操作
    if not test_database_operations():
        print("数据库操作测试失败")
        return
    
    # 导出数据库信息
    if not export_database_info():
        print("导出数据库信息失败")
        return
    
    print("\n🎉 所有操作完成！")
    print("\n可用的文件:")
    print("- data/guild_members.db: SQLite数据库文件")
    print("- data/database_stats.json: 数据库统计信息")
    print("- data/database_export.json: 完整数据导出")
    print("- data/api_documentation.json: API文档")
    
    print("\n下一步:")
    print("1. 使用 src/database/api.py 中的API来访问数据")
    print("2. 运行 src/database/importer.py 来更新数据")
    print("3. 在前端页面中集成数据库API")


if __name__ == "__main__":
    main() 