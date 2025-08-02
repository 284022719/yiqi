"""
数据导入器
用于将现有的CSV和JSON数据导入到数据库中
"""

import csv
import json
import os
from typing import Dict, List, Any
from datetime import datetime
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.models import GuildMemberDB
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataImporter:
    """数据导入器类"""
    
    def __init__(self, db_path: str = "data/guild_members.db"):
        """初始化导入器"""
        self.db = GuildMemberDB(db_path)
        self.logger = logger
    
    def import_csv_data(self, csv_file_path: str = "data/memberinfo.csv") -> Dict[str, int]:
        """从CSV文件导入公会成员数据"""
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"CSV文件不存在: {csv_file_path}")
        
        records_processed = 0
        records_updated = 0
        records_inserted = 0
        errors = []
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        # 转换数据类型
                        member_data = self._convert_csv_row(row)
                        
                        # 插入或更新数据库
                        member_id = self.db.insert_or_update_member(member_data)
                        
                        if member_id:
                            records_processed += 1
                            # 这里可以根据需要判断是更新还是插入
                            # 由于我们的方法会更新现有记录，这里简单统计
                            records_updated += 1
                        
                    except Exception as e:
                        error_msg = f"处理行数据时出错: {row.get('Name', 'Unknown')} - {str(e)}"
                        errors.append(error_msg)
                        self.logger.error(error_msg)
                        continue
            
            # 记录同步日志
            status = "success" if not errors else "partial"
            error_message = "; ".join(errors) if errors else None
            
            self.db.log_sync(
                sync_type="csv_import",
                records_processed=records_processed,
                records_updated=records_updated,
                records_inserted=records_inserted,
                status=status,
                error_message=error_message
            )
            
            self.logger.info(f"CSV导入完成: 处理 {records_processed} 条记录")
            
            return {
                "processed": records_processed,
                "updated": records_updated,
                "inserted": records_inserted,
                "errors": len(errors)
            }
            
        except Exception as e:
            error_msg = f"导入CSV文件时出错: {str(e)}"
            self.logger.error(error_msg)
            
            self.db.log_sync(
                sync_type="csv_import",
                records_processed=records_processed,
                records_updated=records_updated,
                records_inserted=records_inserted,
                status="error",
                error_message=error_msg
            )
            
            raise
    
    def import_enhanced_api_data(self, json_file_path: str = None) -> Dict[str, int]:
        """从增强API JSON文件导入详细数据"""
        if not json_file_path:
            # 查找最新的增强API结果文件
            data_dir = "data"
            json_files = [f for f in os.listdir(data_dir) if f.startswith("enhanced_api_results_") and f.endswith(".json")]
            
            if not json_files:
                raise FileNotFoundError("未找到增强API结果文件")
            
            # 按文件名排序，取最新的
            json_files.sort(reverse=True)
            json_file_path = os.path.join(data_dir, json_files[0])
        
        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"JSON文件不存在: {json_file_path}")
        
        records_processed = 0
        records_updated = 0
        records_inserted = 0
        errors = []
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            for character_data in data:
                try:
                    # 提取基本信息
                    name = character_data.get('name')
                    realm = character_data.get('realm')
                    char_data = character_data.get('data', {})
                    
                    if not name or not realm:
                        continue
                    
                    # 构建成员数据
                    member_data = self._convert_api_data_to_member(char_data, name, realm)
                    
                    # 插入或更新基本信息
                    member_id = self.db.insert_or_update_member(member_data)
                    
                    if member_id:
                        records_processed += 1
                        records_updated += 1
                        
                        # 更新装备信息
                        if 'equipment' in char_data:
                            equipment_data = self._extract_equipment_data(char_data['equipment'])
                            if equipment_data:
                                self.db.update_equipment(member_id, equipment_data)
                        
                        # 更新成就信息（如果有的话）
                        # 这里可以根据API返回的数据结构来提取成就信息
                        
                        # 更新副本进度（如果有的话）
                        # 这里可以根据API返回的数据结构来提取副本进度
                        
                        
                    
                except Exception as e:
                    error_msg = f"处理角色数据时出错: {name} - {str(e)}"
                    errors.append(error_msg)
                    self.logger.error(error_msg)
                    continue
            
            # 记录同步日志
            status = "success" if not errors else "partial"
            error_message = "; ".join(errors) if errors else None
            
            self.db.log_sync(
                sync_type="api_update",
                records_processed=records_processed,
                records_updated=records_updated,
                records_inserted=records_inserted,
                status=status,
                error_message=error_message
            )
            
            self.logger.info(f"增强API数据导入完成: 处理 {records_processed} 条记录")
            
            return {
                "processed": records_processed,
                "updated": records_updated,
                "inserted": records_inserted,
                "errors": len(errors)
            }
            
        except Exception as e:
            error_msg = f"导入增强API数据时出错: {str(e)}"
            self.logger.error(error_msg)
            
            self.db.log_sync(
                sync_type="api_update",
                records_processed=records_processed,
                records_updated=records_updated,
                records_inserted=records_inserted,
                status="error",
                error_message=error_msg
            )
            
            raise
    
    def _convert_csv_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        """转换CSV行数据为数据库格式"""
        return {
            'name': row.get('Name', ''),
            'realm_name': row.get('Realm Name', ''),
            'rank': row.get('Rank', ''),
            'level': int(row.get('Level', 0)) if row.get('Level', '').isdigit() else 0,
            'class': row.get('Class', ''),
            'race': row.get('Race', ''),
            'sex': row.get('Sex', ''),
            'faction': row.get('Faction', ''),
            'last_online_days': float(row.get('Last Online (Days)', 0)) if row.get('Last Online (Days)', '').replace('.', '').isdigit() else 0,
            'mythic_score': int(row.get('Mythic+ Score', 0)) if row.get('Mythic+ Score', '').isdigit() else 0,
            'achievement_points': 0,  # CSV中没有这个字段
            'average_item_level': 0,  # CSV中没有这个字段
            'equipped_item_level': 0,  # CSV中没有这个字段
            'guild_name': '',  # CSV中没有这个字段
            'active_spec': '',  # CSV中没有这个字段
            'covenant_name': '',  # CSV中没有这个字段
            'renown_level': 0  # CSV中没有这个字段
        }
    
    def _convert_api_data_to_member(self, char_data: Dict[str, Any], name: str, realm: str) -> Dict[str, Any]:
        """转换API数据为成员数据格式"""
        summary = char_data.get('character_summary', {})
        
        return {
            'name': name,
            'realm_name': summary.get('realm', {}).get('name', realm),
            'realm_slug': summary.get('realm', {}).get('slug', realm),
            'rank': '',  # API中没有公会职位信息
            'level': summary.get('level', 0),
            'class': summary.get('character_class', {}).get('name', ''),
            'race': summary.get('race', {}).get('name', ''),
            'sex': summary.get('gender', {}).get('name', ''),
            'faction': summary.get('faction', {}).get('name', ''),
            'last_online_days': 0,  # API中没有这个信息
            'mythic_score': 0,  # 需要从其他API获取
            'achievement_points': summary.get('achievement_points', 0),
            'average_item_level': summary.get('average_item_level', 0),
            'equipped_item_level': summary.get('equipped_item_level', 0),
            'guild_name': summary.get('guild', {}).get('name', ''),
            'active_spec': summary.get('active_spec', {}).get('name', ''),
            'covenant_name': summary.get('covenant_progress', {}).get('chosen_covenant', {}).get('name', ''),
            'renown_level': summary.get('covenant_progress', {}).get('renown_level', 0)
        }
    
    def _extract_equipment_data(self, equipment_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """从装备数据中提取装备信息"""
        equipment_list = []
        
        # 这里需要根据实际的API数据结构来解析装备信息
        # 由于API结构可能比较复杂，这里提供一个基础框架
        
        equipped_items = equipment_data.get('equipped_items', [])
        
        for item in equipped_items:
            equipment_item = {
                'slot_name': item.get('slot', {}).get('name', ''),
                'item_id': item.get('item', {}).get('id', 0),
                'item_name': item.get('item', {}).get('name', ''),
                'item_level': item.get('level', {}).get('value', 0),
                'quality': item.get('quality', {}).get('name', ''),
                'enchant_id': 0,  # 需要从enchantments中提取
                'enchant_name': '',  # 需要从enchantments中提取
                'gem_ids': [],  # 需要从sockets中提取
                'gem_names': []  # 需要从sockets中提取
            }
            
            # 处理附魔
            enchantments = item.get('enchantments', [])
            if enchantments:
                enchantment = enchantments[0]  # 假设第一个是主要附魔
                equipment_item['enchant_id'] = enchantment.get('enchantment_id', 0)
                equipment_item['enchant_name'] = enchantment.get('display_string', '')
            
            # 处理宝石
            sockets = item.get('sockets', [])
            for socket in sockets:
                socket_item = socket.get('item', {})
                if socket_item:
                    equipment_item['gem_ids'].append(socket_item.get('id', 0))
                    equipment_item['gem_names'].append(socket_item.get('name', ''))
            
            equipment_list.append(equipment_item)
        
        return equipment_list
    
    def export_statistics_to_json(self, output_file: str = "data/database_stats.json"):
        """导出数据库统计信息到JSON文件"""
        try:
            stats = self.db.get_statistics()
            
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(stats, file, ensure_ascii=False, indent=2)
            
            self.logger.info(f"统计信息已导出到: {output_file}")
            
        except Exception as e:
            self.logger.error(f"导出统计信息时出错: {str(e)}")
            raise


def main():
    """主函数，用于测试数据导入"""
    try:
        importer = DataImporter()
        
        # 导入CSV数据
        print("开始导入CSV数据...")
        csv_result = importer.import_csv_data()
        print(f"CSV导入结果: {csv_result}")
        
        # 导入增强API数据
        print("开始导入增强API数据...")
        api_result = importer.import_enhanced_api_data()
        print(f"API导入结果: {api_result}")
        
        # 导出统计信息
        print("导出统计信息...")
        importer.export_statistics_to_json()
        
        print("数据导入完成！")
        
    except Exception as e:
        print(f"导入过程中出错: {str(e)}")
        logger.error(f"导入过程中出错: {str(e)}")


if __name__ == "__main__":
    main() 