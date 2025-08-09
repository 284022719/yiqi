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
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT name, level, class, race, faction, realm, guild, 
                           achievement_points, average_item_level, equipped_item_level,
                           mythic_score, last_online_days, mounts_now, mounts_total
                    FROM guild_characters 
                    WHERE name = ? AND realm = ?
                    LIMIT 1
                ''', (character_name, realm))
                
                row = cursor.fetchone()
                if not row:
                    print(f"未找到角色 {character_name} 的数据")
                    return
                
                name, level, class_name, race, faction, realm_name, guild, achievement_points, avg_ilvl, equipped_ilvl, mythic_score, last_online, mounts_now, mounts_total = row
                
                print(f"角色名称: {name}")
                print(f"等级: {level}")
                print(f"职业: {class_name}")
                print(f"种族: {race}")
                print(f"阵营: {faction}")
                print(f"服务器: {realm_name}")
                print(f"公会: {guild}")
                print(f"成就点数: {achievement_points}")
                print(f"平均装等: {avg_ilvl}")
                print(f"装备装等: {equipped_ilvl}")
                print(f"钥石评分: {mythic_score}")
                print(f"离线天数: {last_online}")
                print(f"坐骑数量: {mounts_now}/{mounts_total}")
                
        except Exception as e:
            print(f"查询角色信息失败: {e}")
    
    def show_character_history(self, character_name: str, realm: str = "arthas"):
        """显示角色历史数据"""
        print(f"\n{'='*60}")
        print(f"角色历史数据: {character_name} ({realm})")
        print(f"{'='*60}")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT crawl_timestamp, level, average_item_level, achievement_points, 
                           mythic_score, mounts_now, mounts_total
                    FROM guild_characters 
                    WHERE name = ? AND realm = ?
                    ORDER BY crawl_timestamp DESC
                ''', (character_name, realm))
                
                rows = cursor.fetchall()
                if not rows:
                    print(f"未找到角色 {character_name} 的历史数据")
                    return
                
                print(f"共找到 {len(rows)} 条历史记录:")
                for i, row in enumerate(rows, 1):
                    timestamp, level, avg_ilvl, achievement_points, mythic_score, mounts_now, mounts_total = row
                    print(f"\n--- 记录 {i} ---")
                    print(f"时间: {timestamp}")
                    print(f"等级: {level}")
                    print(f"装等: {avg_ilvl}")
                    print(f"成就点数: {achievement_points}")
                    print(f"钥石评分: {mythic_score}")
                    print(f"坐骑数量: {mounts_now}/{mounts_total}")
                
        except Exception as e:
            print(f"查询角色历史失败: {e}")
    
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
                        SELECT name, class, level, average_item_level, achievement_points
                        FROM guild_characters 
                        WHERE average_item_level > 0
                        ORDER BY average_item_level DESC
                        LIMIT ?
                    ''', (limit,))
                    title = "装等排行榜"
                    value_col = "平均装等"
                elif category == "achievement":
                    cursor.execute('''
                        SELECT name, class, level, achievement_points, average_item_level
                        FROM guild_characters 
                        WHERE achievement_points > 0
                        ORDER BY achievement_points DESC
                        LIMIT ?
                    ''', (limit,))
                    title = "成就点数排行榜"
                    value_col = "成就点数"
                elif category == "mounts":
                    cursor.execute('''
                        SELECT name, class, level, mounts_now, mounts_total, average_item_level
                        FROM guild_characters 
                        WHERE mounts_now > 0
                        ORDER BY mounts_now DESC
                        LIMIT ?
                    ''', (limit,))
                    title = "坐骑数量排行榜"
                    value_col = "坐骑数量"
                else:
                    print(f"未知的排行榜类型: {category}")
                    return
                
                results = cursor.fetchall()
                print(f"{title} (前{limit}名):")
                print(f"{'排名':<4} {'角色名':<15} {'职业':<8} {'等级':<4} {value_col:<10} {'其他信息':<15}")
                print("-" * 70)
                
                for i, row in enumerate(results, 1):
                    if category == "mounts":
                        name, class_name, level, value, mounts_total, other = row
                        other_info = f"装等{other}"
                    else:
                        name, class_name, level, value, other = row
                        other_info = f"成就{other}"
                    
                    print(f"{i:<4} {name:<15} {class_name:<8} {level:<4} {value:<10} {other_info:<15}")
                
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
                    SELECT name, level, class, race, faction, realm, guild, 
                           achievement_points, average_item_level, equipped_item_level,
                           mythic_score, last_online_days, mounts_now, mounts_total,
                           crawl_timestamp, updated_at
                    FROM guild_characters 
                    WHERE name = ? AND realm = ?
                    ORDER BY crawl_timestamp DESC
                    LIMIT 1
                ''', (character_name, realm))
                
                character_data = cursor.fetchone()
                if not character_data:
                    print(f"未找到角色 {character_name} 的数据")
                    return
                
                # 构建导出数据
                export_data = {
                    'character_info': {
                        'name': character_data[0],
                        'level': character_data[1],
                        'class': character_data[2],
                        'race': character_data[3],
                        'faction': character_data[4],
                        'realm': character_data[5],
                        'guild': character_data[6],
                        'achievement_points': character_data[7],
                        'average_item_level': character_data[8],
                        'equipped_item_level': character_data[9],
                        'mythic_score': character_data[10],
                        'last_online_days': character_data[11],
                        'mounts_now': character_data[12],
                        'mounts_total': character_data[13],
                        'crawl_timestamp': character_data[14],
                        'updated_at': character_data[15]
                    }
                }
                
                # 保存到文件
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                
                print(f"数据已导出到: {output_file}")
                print(f"角色名称: {character_data[0]}")
                print(f"等级: {character_data[1]}")
                print(f"职业: {character_data[2]}")
                print(f"装等: {character_data[8]}")
                print(f"成就点数: {character_data[7]}")
                print(f"坐骑数量: {character_data[12]}/{character_data[13]}")
                
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