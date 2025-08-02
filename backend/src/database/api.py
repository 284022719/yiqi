"""
数据库API接口
提供RESTful API来访问数据库数据
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.models import GuildMemberDB
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DatabaseAPI:
    """数据库API接口类"""
    
    def __init__(self, db_path: str = "data/guild_members.db"):
        """初始化API接口"""
        self.db = GuildMemberDB(db_path)
        self.logger = logger
    
    def get_member_info(self, name: str, realm_name: str) -> Optional[Dict[str, Any]]:
        """获取指定成员信息"""
        try:
            member = self.db.get_member_by_name(name, realm_name)
            if member:
                return {
                    "success": True,
                    "data": member,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": "成员不存在",
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            self.logger.error(f"获取成员信息时出错: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_all_members(self, limit: int = None, offset: int = 0) -> Dict[str, Any]:
        """获取所有成员列表"""
        try:
            members = self.db.get_all_members(limit, offset)
            return {
                "success": True,
                "data": {
                    "members": members,
                    "total": len(members),
                    "limit": limit,
                    "offset": offset
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"获取所有成员时出错: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_members_by_class(self, class_name: str) -> Dict[str, Any]:
        """根据职业获取成员列表"""
        try:
            members = self.db.get_members_by_class(class_name)
            return {
                "success": True,
                "data": {
                    "members": members,
                    "class": class_name,
                    "total": len(members)
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"根据职业获取成员时出错: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_members_by_realm(self, realm_name: str) -> Dict[str, Any]:
        """根据服务器获取成员列表"""
        try:
            members = self.db.get_members_by_realm(realm_name)
            return {
                "success": True,
                "data": {
                    "members": members,
                    "realm": realm_name,
                    "total": len(members)
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"根据服务器获取成员时出错: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_top_mythic_players(self, limit: int = 10) -> Dict[str, Any]:
        """获取Mythic+评分最高的玩家"""
        try:
            players = self.db.get_top_mythic_players(limit)
            return {
                "success": True,
                "data": {
                    "players": players,
                    "limit": limit,
                    "total": len(players)
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"获取Mythic+排行榜时出错: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取公会统计信息"""
        try:
            stats = self.db.get_statistics()
            return {
                "success": True,
                "data": stats,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"获取统计信息时出错: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def search_members(self, query: str, limit: int = 20) -> Dict[str, Any]:
        """搜索成员"""
        try:
            # 这里可以实现更复杂的搜索逻辑
            # 目前简单地在所有成员中搜索包含查询字符串的名称
            all_members = self.db.get_all_members()
            results = []
            
            query_lower = query.lower()
            for member in all_members:
                if query_lower in member['name'].lower():
                    results.append(member)
                    if len(results) >= limit:
                        break
            
            return {
                "success": True,
                "data": {
                    "results": results,
                    "query": query,
                    "total": len(results),
                    "limit": limit
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"搜索成员时出错: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_available_classes(self) -> Dict[str, Any]:
        """获取可用的职业列表"""
        try:
            stats = self.db.get_statistics()
            classes = list(stats.get('class_distribution', {}).keys())
            return {
                "success": True,
                "data": {
                    "classes": classes,
                    "total": len(classes)
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"获取职业列表时出错: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_available_realms(self) -> Dict[str, Any]:
        """获取可用的服务器列表"""
        try:
            stats = self.db.get_statistics()
            realms = list(stats.get('server_distribution', {}).keys())
            return {
                "success": True,
                "data": {
                    "realms": realms,
                    "total": len(realms)
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"获取服务器列表时出错: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def export_data_to_json(self, output_file: str = "data/api_export.json") -> Dict[str, Any]:
        """导出数据到JSON文件"""
        try:
            # 获取所有数据
            stats = self.db.get_statistics()
            top_players = self.db.get_top_mythic_players(50)
            all_members = self.db.get_all_members()
            
            export_data = {
                "statistics": stats,
                "top_mythic_players": top_players,
                "all_members": all_members,
                "export_timestamp": datetime.now().isoformat()
            }
            
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(export_data, file, ensure_ascii=False, indent=2)
            
            return {
                "success": True,
                "data": {
                    "output_file": output_file,
                    "total_members": len(all_members),
                    "top_players_count": len(top_players)
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"导出数据时出错: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


# 创建全局API实例
api = DatabaseAPI()


def handle_api_request(endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """处理API请求的统一接口"""
    try:
        if endpoint == "member":
            name = params.get("name")
            realm = params.get("realm")
            if not name or not realm:
                return {
                    "success": False,
                    "error": "缺少必要参数: name, realm",
                    "timestamp": datetime.now().isoformat()
                }
            return api.get_member_info(name, realm)
        
        elif endpoint == "members":
            limit = params.get("limit") if params else None
            offset = params.get("offset", 0) if params else 0
            return api.get_all_members(limit, offset)
        
        elif endpoint == "class":
            class_name = params.get("class") if params else None
            if not class_name:
                return {
                    "success": False,
                    "error": "缺少必要参数: class",
                    "timestamp": datetime.now().isoformat()
                }
            return api.get_members_by_class(class_name)
        
        elif endpoint == "realm":
            realm_name = params.get("realm") if params else None
            if not realm_name:
                return {
                    "success": False,
                    "error": "缺少必要参数: realm",
                    "timestamp": datetime.now().isoformat()
                }
            return api.get_members_by_realm(realm_name)
        
        elif endpoint == "mythic_ranking":
            limit = params.get("limit", 10) if params else 10
            return api.get_top_mythic_players(limit)
        
        elif endpoint == "statistics":
            return api.get_statistics()
        
        elif endpoint == "search":
            query = params.get("q") if params else ""
            limit = params.get("limit", 20) if params else 20
            return api.search_members(query, limit)
        
        elif endpoint == "classes":
            return api.get_available_classes()
        
        elif endpoint == "realms":
            return api.get_available_realms()
        
        elif endpoint == "export":
            output_file = params.get("output_file", "data/api_export.json") if params else "data/api_export.json"
            return api.export_data_to_json(output_file)
        
        else:
            return {
                "success": False,
                "error": f"未知的API端点: {endpoint}",
                "available_endpoints": [
                    "member", "members", "class", "realm", "mythic_ranking",
                    "statistics", "search", "classes", "realms", "export"
                ],
                "timestamp": datetime.now().isoformat()
            }
    
    except Exception as e:
        logger.error(f"处理API请求时出错: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def main():
    """主函数，支持命令行参数"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='数据库API命令行工具')
    parser.add_argument('action', help='API动作')
    parser.add_argument('--name', help='角色名')
    parser.add_argument('--realm', help='服务器名')
    parser.add_argument('--class', dest='class_name', help='职业名')
    parser.add_argument('--limit', type=int, help='限制数量')
    parser.add_argument('--offset', type=int, help='偏移量')
    parser.add_argument('--q', help='搜索查询')
    parser.add_argument('--output_file', help='输出文件路径')
    
    args = parser.parse_args()
    
    try:
        # 构建参数字典
        params = {}
        if args.name:
            params['name'] = args.name
        if args.realm:
            params['realm'] = args.realm
        if args.class_name:
            params['class'] = args.class_name
        if args.limit:
            params['limit'] = args.limit
        if args.offset:
            params['offset'] = args.offset
        if args.q:
            params['q'] = args.q
        if args.output_file:
            params['output_file'] = args.output_file
        
        # 处理API请求
        result = handle_api_request(args.action, params)
        
        # 输出JSON结果
        print(json.dumps(result, ensure_ascii=False))
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(error_result, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main() 