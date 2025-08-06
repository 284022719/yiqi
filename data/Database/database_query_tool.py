import sqlite3
import json
from datetime import datetime
from database_manager import GuildDatabaseManager

class DatabaseQueryTool:
    def __init__(self, db_path: str = "data/guild_database.db"):
        """初始化数据库查询工具"""
        self.db_path = db_path
        self.db_manager = GuildDatabaseManager(db_path)
    
    def show_database_info(self):
        """显示数据库基本信息"""
        print("=" * 60)
        print("公会数据库信息")
        print("=" * 60)
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 获取表信息
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                print(f"数据库文件: {self.db_path}")
                print(f"表数量: {len(tables)}")
                print("\n表列表:")
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                    count = cursor.fetchone()[0]
                    print(f"  - {table[0]}: {count} 条记录")
                
                # 显示统计信息
                stats = self.db_manager.get_guild_statistics()
                print(f"\n公会统计:")
                print(f"  总成员数: {stats.get('total_members', 0)}")
                print(f"  API数据角色数: {stats.get('api_characters', 0)}")
                print(f"  职业分布: {stats.get('class_distribution', {})}")
                print(f"  等级分布: {stats.get('level_distribution', {})}")
                print(f"  装等统计: {stats.get('item_level_stats', {})}")
                
        except Exception as e:
            print(f"获取数据库信息失败: {e}")
    
    def search_character(self, character_name: str, realm: str = "arthas"):
        """搜索角色信息"""
        print(f"\n{'='*60}")
        print(f"角色信息查询: {character_name} ({realm})")
        print(f"{'='*60}")
        
        # 获取最新数据
        latest_data = self.db_manager.get_latest_character_data(character_name, realm)
        if not latest_data:
            print(f"未找到角色 {character_name} 的数据")
            return
        
        print(f"角色名称: {latest_data.get('name', 'N/A')}")
        print(f"等级: {latest_data.get('level', 'N/A')}")
        print(f"职业: {latest_data.get('class', 'N/A')} - {latest_data.get('spec', 'N/A')}")
        print(f"种族: {latest_data.get('race', 'N/A')}")
        print(f"阵营: {latest_data.get('faction', 'N/A')}")
        print(f"公会: {latest_data.get('guild', 'N/A')}")
        print(f"成就点数: {latest_data.get('achievement_points', 'N/A')}")
        print(f"平均装等: {latest_data.get('average_item_level', 'N/A')}")
        print(f"装备装等: {latest_data.get('equipped_item_level', 'N/A')}")
        print(f"盟约: {latest_data.get('covenant', 'N/A')}")
        print(f"名望等级: {latest_data.get('renown_level', 'N/A')}")
        print(f"装备数量: {latest_data.get('equipment_count', 'N/A')}")
        print(f"坐骑数量: {latest_data.get('mounts_count', 'N/A')}")
        print(f"成就数量: {latest_data.get('achievements_count', 'N/A')}")
        print(f"数据时间: {latest_data.get('crawl_timestamp', 'N/A')}")
    
    def show_character_history(self, character_name: str, realm: str = "arthas"):
        """显示角色历史数据"""
        print(f"\n{'='*60}")
        print(f"角色历史数据: {character_name} ({realm})")
        print(f"{'='*60}")
        
        history = self.db_manager.get_character_history(character_name, realm)
        if not history:
            print(f"未找到角色 {character_name} 的历史数据")
            return
        
        print(f"共找到 {len(history)} 条历史记录:")
        for i, record in enumerate(history, 1):
            print(f"\n--- 记录 {i} ---")
            print(f"时间: {record.get('crawl_timestamp', 'N/A')}")
            print(f"等级: {record.get('level', 'N/A')}")
            print(f"装等: {record.get('average_item_level', 'N/A')}")
            print(f"成就点数: {record.get('achievement_points', 'N/A')}")
            print(f"装备数量: {record.get('equipment_count', 'N/A')}")
            print(f"坐骑数量: {record.get('mounts_count', 'N/A')}")
            print(f"成就数量: {record.get('achievements_count', 'N/A')}")
    
    def show_top_characters(self, category: str = "item_level", limit: int = 10):
        """显示排行榜"""
        print(f"\n{'='*60}")
        print(f"角色排行榜 - {category}")
        print(f"{'='*60}")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if category == "item_level":
                    cursor.execute('''
                        SELECT name, class, spec, average_item_level, achievement_points
                        FROM character_details 
                        WHERE data_source = "api" AND average_item_level > 0
                        ORDER BY average_item_level DESC
                        LIMIT ?
                    ''', (limit,))
                    title = "装等排行榜"
                    value_col = "平均装等"
                elif category == "achievement":
                    cursor.execute('''
                        SELECT name, class, spec, achievement_points, average_item_level
                        FROM character_details 
                        WHERE data_source = "api" AND achievement_points > 0
                        ORDER BY achievement_points DESC
                        LIMIT ?
                    ''', (limit,))
                    title = "成就点数排行榜"
                    value_col = "成就点数"
                elif category == "mounts":
                    cursor.execute('''
                        SELECT cd.name, cd.class, cd.spec, COUNT(cm.id) as mount_count, cd.average_item_level
                        FROM character_details cd
                        LEFT JOIN character_mounts cm ON cd.id = cm.character_detail_id
                        WHERE cd.data_source = "api"
                        GROUP BY cd.id
                        ORDER BY mount_count DESC
                        LIMIT ?
                    ''', (limit,))
                    title = "坐骑数量排行榜"
                    value_col = "坐骑数量"
                else:
                    print(f"未知的排行榜类型: {category}")
                    return
                
                results = cursor.fetchall()
                print(f"{title} (前{limit}名):")
                print(f"{'排名':<4} {'角色名':<15} {'职业':<8} {'专精':<8} {value_col:<10} {'其他信息':<15}")
                print("-" * 70)
                
                for i, row in enumerate(results, 1):
                    if category == "mounts":
                        name, class_name, spec, value, other = row
                        other_info = f"装等{other}"
                    else:
                        name, class_name, spec, value, other = row
                        other_info = f"成就{other}"
                    
                    print(f"{i:<4} {name:<15} {class_name:<8} {spec:<8} {value:<10} {other_info:<15}")
                
        except Exception as e:
            print(f"获取排行榜失败: {e}")
    
    def show_crawl_logs(self, limit: int = 20):
        """显示爬虫日志"""
        print(f"\n{'='*60}")
        print(f"爬虫日志 (最近{limit}条)")
        print(f"{'='*60}")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT crawl_session, character_name, realm, status, message, crawl_timestamp
                    FROM crawl_logs
                    ORDER BY crawl_timestamp DESC
                    LIMIT ?
                ''', (limit,))
                
                results = cursor.fetchall()
                print(f"{'时间':<20} {'会话':<12} {'角色名':<15} {'状态':<10} {'消息':<30}")
                print("-" * 90)
                
                for row in results:
                    session, name, realm, status, message, timestamp = row
                    time_str = timestamp.split('.')[0] if timestamp else 'N/A'
                    print(f"{time_str:<20} {session:<12} {name:<15} {status:<10} {message[:30]:<30}")
                
        except Exception as e:
            print(f"获取爬虫日志失败: {e}")
    
    def export_character_data(self, character_name: str, realm: str = "arthas", output_file: str = None):
        """导出角色数据到JSON文件"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"data/character_export_{character_name}_{timestamp}.json"
        
        print(f"\n{'='*60}")
        print(f"导出角色数据: {character_name}")
        print(f"{'='*60}")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 获取角色详细信息
                cursor.execute('''
                    SELECT * FROM character_details 
                    WHERE name = ? AND realm = ?
                    ORDER BY crawl_timestamp DESC
                    LIMIT 1
                ''', (character_name, realm))
                
                character_data = cursor.fetchone()
                if not character_data:
                    print(f"未找到角色 {character_name} 的数据")
                    return
                
                # 获取装备信息
                cursor.execute('''
                    SELECT slot, item_name, item_level, quality, enchantments, gems, temporary_enchantments
                    FROM character_equipment 
                    WHERE character_detail_id = ?
                ''', (character_data[0],))
                
                equipment = []
                for row in cursor.fetchall():
                    equipment.append({
                        'slot': row[0],
                        'name': row[1],
                        'item_level': row[2],
                        'quality': row[3],
                        'enchantments': json.loads(row[4]) if row[4] else [],
                        'gems': json.loads(row[5]) if row[5] else [],
                        'temporary_enchantments': json.loads(row[6]) if row[6] else []
                    })
                
                # 获取坐骑信息
                cursor.execute('''
                    SELECT mount_name, mount_id, creature_displays
                    FROM character_mounts 
                    WHERE character_detail_id = ?
                ''', (character_data[0],))
                
                mounts = []
                for row in cursor.fetchall():
                    mounts.append({
                        'name': row[0],
                        'id': row[1],
                        'creature_displays': json.loads(row[2]) if row[2] else []
                    })
                
                # 获取成就信息
                cursor.execute('''
                    SELECT achievement_id, achievement_name, description, completed_timestamp, category
                    FROM character_achievements 
                    WHERE character_detail_id = ?
                ''', (character_data[0],))
                
                achievements = []
                for row in cursor.fetchall():
                    achievements.append({
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'completed_timestamp': row[3],
                        'category': row[4]
                    })
                
                # 构建导出数据
                export_data = {
                    'character_info': {
                        'name': character_data[2],
                        'realm': character_data[3],
                        'guild': character_data[4],
                        'level': character_data[5],
                        'faction': character_data[6],
                        'race': character_data[7],
                        'class': character_data[8],
                        'spec': character_data[9],
                        'achievement_points': character_data[10],
                        'average_item_level': character_data[11],
                        'equipped_item_level': character_data[12],
                        'covenant': character_data[14],
                        'renown_level': character_data[15],
                        'crawl_timestamp': character_data[17]
                    },
                    'equipment': equipment,
                    'mounts': mounts,
                    'achievements': achievements
                }
                
                # 保存到文件
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                
                print(f"数据已导出到: {output_file}")
                print(f"装备数量: {len(equipment)}")
                print(f"坐骑数量: {len(mounts)}")
                print(f"成就数量: {len(achievements)}")
                
        except Exception as e:
            print(f"导出数据失败: {e}")

def main():
    """主函数 - 交互式查询工具"""
    tool = DatabaseQueryTool()
    
    while True:
        print("\n" + "="*60)
        print("公会数据库查询工具")
        print("="*60)
        print("1. 显示数据库信息")
        print("2. 搜索角色信息")
        print("3. 显示角色历史")
        print("4. 装等排行榜")
        print("5. 成就排行榜")
        print("6. 坐骑排行榜")
        print("7. 查看爬虫日志")
        print("8. 导出角色数据")
        print("9. 退出")
        print("-"*60)
        
        choice = input("请选择功能 (1-9): ").strip()
        
        if choice == "1":
            tool.show_database_info()
        
        elif choice == "2":
            name = input("请输入角色名: ").strip()
            if name:
                tool.search_character(name)
        
        elif choice == "3":
            name = input("请输入角色名: ").strip()
            if name:
                tool.show_character_history(name)
        
        elif choice == "4":
            limit = input("显示前几名 (默认10): ").strip()
            limit = int(limit) if limit.isdigit() else 10
            tool.show_top_characters("item_level", limit)
        
        elif choice == "5":
            limit = input("显示前几名 (默认10): ").strip()
            limit = int(limit) if limit.isdigit() else 10
            tool.show_top_characters("achievement", limit)
        
        elif choice == "6":
            limit = input("显示前几名 (默认10): ").strip()
            limit = int(limit) if limit.isdigit() else 10
            tool.show_top_characters("mounts", limit)
        
        elif choice == "7":
            limit = input("显示最近几条 (默认20): ").strip()
            limit = int(limit) if limit.isdigit() else 20
            tool.show_crawl_logs(limit)
        
        elif choice == "8":
            name = input("请输入角色名: ").strip()
            if name:
                output_file = input("输出文件名 (可选): ").strip()
                output_file = output_file if output_file else None
                tool.export_character_data(name, output_file=output_file)
        
        elif choice == "9":
            print("感谢使用！")
            break
        
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main() 