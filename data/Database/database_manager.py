import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

class GuildDatabaseManager:
    def __init__(self, db_path: str = "../guild_database.db"):
        """初始化数据库管理器"""
        self.db_path = db_path
        self.setup_logging()
        self.init_database()
    
    def setup_logging(self):
        """设置日志记录"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/database_manager.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def init_database(self):
        """初始化数据库表结构"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 检查并添加坐骑数字段
                cursor.execute("PRAGMA table_info(guild_characters)")
                columns = [row[1] for row in cursor.fetchall()]
                
                if 'mounts_now' not in columns:
                    cursor.execute("ALTER TABLE guild_characters ADD COLUMN mounts_now INTEGER DEFAULT 0")
                    self.logger.info("已添加 mounts_now 字段到 guild_characters 表")
                
                if 'mounts_total' not in columns:
                    cursor.execute("ALTER TABLE guild_characters ADD COLUMN mounts_total INTEGER DEFAULT 0")
                    self.logger.info("已添加 mounts_total 字段到 guild_characters 表")
                
                conn.commit()
                self.logger.info("数据库初始化完成")
                
        except Exception as e:
            self.logger.error(f"数据库初始化失败: {e}")
    
    def get_all_characters(self) -> List[Dict[str, Any]]:
        """获取所有角色信息"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT name, realm_slug, faction, class, level, mounts_now, mounts_total
                    FROM guild_characters
                    ORDER BY name
                """)
                
                columns = [description[0] for description in cursor.description]
                characters = []
                
                for row in cursor.fetchall():
                    character = dict(zip(columns, row))
                    characters.append(character)
                
                return characters
                
        except Exception as e:
            self.logger.error(f"获取角色列表失败: {e}")
            return []
    
    def update_character_mounts(self, character_name: str, realm_slug: str, mounts_data: Dict[str, Any]) -> bool:
        """更新角色的坐骑数据"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                mounts_now = mounts_data.get('now', 0)
                mounts_total = mounts_data.get('total', 0)
                
                cursor.execute("""
                    UPDATE guild_characters 
                    SET mounts_now = ?, mounts_total = ?, updated_at = ?
                    WHERE name = ? AND realm_slug = ?
                """, (mounts_now, mounts_total, datetime.now(), character_name, realm_slug))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    self.logger.info(f"已更新角色 {character_name} 的坐骑数据: {mounts_now}/{mounts_total}")
                    return True
                else:
                    self.logger.warning(f"未找到角色 {character_name} ({realm_slug})")
                    return False
                    
        except Exception as e:
            self.logger.error(f"更新角色坐骑数据失败: {e}")
            return False
    
    def get_character_mounts_info(self, character_name: str, realm_slug: str) -> Optional[Dict[str, Any]]:
        """获取角色的坐骑信息"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT name, realm_slug, faction, mounts_now, mounts_total, updated_at
                    FROM guild_characters
                    WHERE name = ? AND realm_slug = ?
                """, (character_name, realm_slug))
                
                row = cursor.fetchone()
                if row:
                    columns = ['name', 'realm_slug', 'faction', 'mounts_now', 'mounts_total', 'updated_at']
                    return dict(zip(columns, row))
                return None
                
        except Exception as e:
            self.logger.error(f"获取角色坐骑信息失败: {e}")
            return None
    
    def get_mounts_statistics(self) -> Dict[str, Any]:
        """获取坐骑统计信息"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 总角色数
                cursor.execute("SELECT COUNT(*) FROM guild_characters")
                total_characters = cursor.fetchone()[0]
                
                # 有坐骑数据的角色数
                cursor.execute("SELECT COUNT(*) FROM guild_characters WHERE mounts_now > 0")
                characters_with_mounts = cursor.fetchone()[0]
                
                # 坐骑数量统计
                cursor.execute("""
                    SELECT 
                        SUM(mounts_now) as total_mounts_now,
                        SUM(mounts_total) as total_mounts_total,
                        AVG(mounts_now) as avg_mounts_now,
                        MAX(mounts_now) as max_mounts_now,
                        MIN(mounts_now) as min_mounts_now
                    FROM guild_characters 
                    WHERE mounts_now > 0
                """)
                
                mount_stats = cursor.fetchone()
                
                # 按职业统计
                cursor.execute("""
                    SELECT class, 
                           COUNT(*) as character_count,
                           AVG(mounts_now) as avg_mounts,
                           SUM(mounts_now) as total_mounts
                    FROM guild_characters 
                    WHERE mounts_now > 0
                    GROUP BY class
                    ORDER BY avg_mounts DESC
                """)
                
                class_stats = []
                for row in cursor.fetchall():
                    class_stats.append({
                        'class': row[0],
                        'character_count': row[1],
                        'avg_mounts': round(row[2], 1),
                        'total_mounts': row[3]
                    })
                
                return {
                    'total_characters': total_characters,
                    'characters_with_mounts': characters_with_mounts,
                    'mounts_coverage': round(characters_with_mounts / total_characters * 100, 1) if total_characters > 0 else 0,
                    'total_mounts_now': mount_stats[0] or 0,
                    'total_mounts_total': mount_stats[1] or 0,
                    'avg_mounts_now': round(mount_stats[2], 1) if mount_stats[2] else 0,
                    'max_mounts_now': mount_stats[3] or 0,
                    'min_mounts_now': mount_stats[4] or 0,
                    'class_statistics': class_stats
                }
                
        except Exception as e:
            self.logger.error(f"获取坐骑统计信息失败: {e}")
            return {}
    
    def get_top_mounts_characters(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取坐骑数量最多的角色"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT name, realm_slug, class, level, mounts_now, mounts_total, faction
                    FROM guild_characters
                    WHERE mounts_now > 0
                    ORDER BY mounts_now DESC
                    LIMIT ?
                """, (limit,))
                
                columns = ['name', 'realm_slug', 'class', 'level', 'mounts_now', 'mounts_total', 'faction']
                characters = []
                
                for row in cursor.fetchall():
                    character = dict(zip(columns, row))
                    characters.append(character)
                
                return characters
                
        except Exception as e:
            self.logger.error(f"获取坐骑排行榜失败: {e}")
            return []
    
    def get_guild_statistics(self) -> Dict[str, Any]:
        """获取公会统计信息"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 总角色数
                cursor.execute("SELECT COUNT(*) FROM guild_characters")
                total_characters = cursor.fetchone()[0]
                
                # 按职业统计
                cursor.execute("""
                    SELECT class, COUNT(*) as count
                    FROM guild_characters
                    WHERE class IS NOT NULL
                    GROUP BY class
                    ORDER BY count DESC
                """)
                class_distribution = {}
                for row in cursor.fetchall():
                    class_distribution[row[0]] = row[1]
                
                # 按等级统计
                cursor.execute("""
                    SELECT level, COUNT(*) as count
                    FROM guild_characters
                    WHERE level IS NOT NULL
                    GROUP BY level
                    ORDER BY level DESC
                """)
                level_distribution = {}
                for row in cursor.fetchall():
                    level_distribution[row[0]] = row[1]
                
                # 装等统计
                cursor.execute("""
                    SELECT 
                        AVG(average_item_level) as avg_ilvl,
                        MAX(average_item_level) as max_ilvl,
                        MIN(average_item_level) as min_ilvl
                    FROM guild_characters
                    WHERE average_item_level > 0
                """)
                ilvl_stats = cursor.fetchone()
                
                return {
                    'total_characters': total_characters,
                    'class_distribution': class_distribution,
                    'level_distribution': level_distribution,
                    'item_level_stats': {
                        'average': round(ilvl_stats[0], 1) if ilvl_stats[0] else 0,
                        'max': ilvl_stats[1] or 0,
                        'min': ilvl_stats[2] or 0
                    }
                }
                
        except Exception as e:
            self.logger.error(f"获取公会统计信息失败: {e}")
            return {}
    
    def export_mounts_data(self, output_file: str = None) -> str:
        """导出坐骑数据"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"data/mounts_database_export_{timestamp}.json"
        
        try:
            characters = self.get_all_characters()
            statistics = self.get_mounts_statistics()
            top_characters = self.get_top_mounts_characters()
            
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'statistics': statistics,
                'top_characters': top_characters,
                'all_characters': characters
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"坐骑数据已导出到: {output_file}")
            return output_file
            
        except Exception as e:
            self.logger.error(f"导出坐骑数据失败: {e}")
            return ""

def main():
    """测试数据库管理器"""
    db_manager = GuildDatabaseManager()
    
    # 显示数据库信息
    print("=== 数据库管理器测试 ===")
    
    # 获取所有角色
    characters = db_manager.get_all_characters()
    print(f"总角色数: {len(characters)}")
    
    # 获取统计信息
    stats = db_manager.get_mounts_statistics()
    print(f"坐骑统计: {stats}")
    
    # 获取排行榜
    top_characters = db_manager.get_top_mounts_characters(5)
    print(f"坐骑排行榜前5名:")
    for i, char in enumerate(top_characters, 1):
        print(f"{i}. {char['name']} ({char['class']}) - {char['mounts_now']} 坐骑")

if __name__ == "__main__":
    main() 