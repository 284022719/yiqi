"""
数据库模型定义
定义公会成员信息的表结构
"""

import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any
import json


class GuildMemberDB:
    """公会成员数据库管理类"""
    
    def __init__(self, db_path: str = "data/guild_members.db"):
        """初始化数据库连接"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库表结构"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 创建公会成员基本信息表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS guild_members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    realm_name TEXT NOT NULL,
                    realm_slug TEXT,
                    rank TEXT,
                    level INTEGER,
                    class TEXT,
                    race TEXT,
                    sex TEXT,
                    faction TEXT,
                    last_online_days REAL,
                    mythic_score INTEGER DEFAULT 0,
                    achievement_points INTEGER DEFAULT 0,
                    average_item_level REAL DEFAULT 0,
                    equipped_item_level REAL DEFAULT 0,
                    guild_name TEXT,
                    active_spec TEXT,
                    covenant_name TEXT,
                    renown_level INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(name, realm_name)
                )
            ''')
            
            # 创建装备信息表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS member_equipment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id INTEGER,
                    slot_name TEXT,
                    item_id INTEGER,
                    item_name TEXT,
                    item_level INTEGER,
                    quality TEXT,
                    enchant_id INTEGER,
                    enchant_name TEXT,
                    gem_ids TEXT,  -- JSON格式存储宝石ID
                    gem_names TEXT, -- JSON格式存储宝石名称
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (member_id) REFERENCES guild_members (id),
                    UNIQUE(member_id, slot_name)
                )
            ''')
            
            # 创建成就信息表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS member_achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id INTEGER,
                    achievement_id INTEGER,
                    achievement_name TEXT,
                    achievement_description TEXT,
                    completed_at TIMESTAMP,
                    points INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (member_id) REFERENCES guild_members (id),
                    UNIQUE(member_id, achievement_id)
                )
            ''')
            
            # 创建副本进度表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS member_raids (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id INTEGER,
                    raid_name TEXT,
                    raid_expansion TEXT,
                    difficulty TEXT,
                    progress_current INTEGER DEFAULT 0,
                    progress_total INTEGER DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (member_id) REFERENCES guild_members (id),
                    UNIQUE(member_id, raid_name, difficulty)
                )
            ''')
            

            
            # 创建数据同步记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sync_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sync_type TEXT,  -- csv_import, api_update, manual_update
                    records_processed INTEGER,
                    records_updated INTEGER,
                    records_inserted INTEGER,
                    sync_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT,  -- success, error, partial
                    error_message TEXT
                )
            ''')
            
            conn.commit()
    
    def insert_or_update_member(self, member_data: Dict[str, Any]) -> int:
        """插入或更新公会成员信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 检查成员是否已存在
            cursor.execute('''
                SELECT id FROM guild_members 
                WHERE name = ? AND realm_name = ?
            ''', (member_data['name'], member_data['realm_name']))
            
            existing = cursor.fetchone()
            
            if existing:
                # 更新现有记录
                member_id = existing[0]
                cursor.execute('''
                    UPDATE guild_members SET
                        rank = ?, level = ?, class = ?, race = ?, sex = ?,
                        faction = ?, last_online_days = ?, mythic_score = ?,
                        achievement_points = ?, average_item_level = ?,
                        equipped_item_level = ?, guild_name = ?, active_spec = ?,
                        covenant_name = ?, renown_level = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (
                    member_data.get('rank'), member_data.get('level'),
                    member_data.get('class'), member_data.get('race'),
                    member_data.get('sex'), member_data.get('faction'),
                    member_data.get('last_online_days'), member_data.get('mythic_score', 0),
                    member_data.get('achievement_points', 0), member_data.get('average_item_level', 0),
                    member_data.get('equipped_item_level', 0), member_data.get('guild_name'),
                    member_data.get('active_spec'), member_data.get('covenant_name'),
                    member_data.get('renown_level', 0), member_id
                ))
            else:
                # 插入新记录
                cursor.execute('''
                    INSERT INTO guild_members (
                        name, realm_name, realm_slug, rank, level, class, race, sex,
                        faction, last_online_days, mythic_score, achievement_points,
                        average_item_level, equipped_item_level, guild_name, active_spec,
                        covenant_name, renown_level
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    member_data['name'], member_data['realm_name'],
                    member_data.get('realm_slug'), member_data.get('rank'),
                    member_data.get('level'), member_data.get('class'),
                    member_data.get('race'), member_data.get('sex'),
                    member_data.get('faction'), member_data.get('last_online_days'),
                    member_data.get('mythic_score', 0), member_data.get('achievement_points', 0),
                    member_data.get('average_item_level', 0), member_data.get('equipped_item_level', 0),
                    member_data.get('guild_name'), member_data.get('active_spec'),
                    member_data.get('covenant_name'), member_data.get('renown_level', 0)
                ))
                member_id = cursor.lastrowid
            
            conn.commit()
            return member_id
    
    def update_equipment(self, member_id: int, equipment_data: List[Dict[str, Any]]):
        """更新成员装备信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 删除现有装备记录
            cursor.execute('DELETE FROM member_equipment WHERE member_id = ?', (member_id,))
            
            # 插入新装备记录
            for item in equipment_data:
                cursor.execute('''
                    INSERT INTO member_equipment (
                        member_id, slot_name, item_id, item_name, item_level,
                        quality, enchant_id, enchant_name, gem_ids, gem_names
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    member_id, item.get('slot_name'), item.get('item_id'),
                    item.get('item_name'), item.get('item_level'),
                    item.get('quality'), item.get('enchant_id'),
                    item.get('enchant_name'), json.dumps(item.get('gem_ids', [])),
                    json.dumps(item.get('gem_names', []))
                ))
            
            conn.commit()
    
    def update_achievements(self, member_id: int, achievements_data: List[Dict[str, Any]]):
        """更新成员成就信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 删除现有成就记录
            cursor.execute('DELETE FROM member_achievements WHERE member_id = ?', (member_id,))
            
            # 插入新成就记录
            for achievement in achievements_data:
                cursor.execute('''
                    INSERT INTO member_achievements (
                        member_id, achievement_id, achievement_name,
                        achievement_description, completed_at, points
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    member_id, achievement.get('id'), achievement.get('name'),
                    achievement.get('description'), achievement.get('completed_at'),
                    achievement.get('points', 0)
                ))
            
            conn.commit()
    
    def update_raids(self, member_id: int, raids_data: List[Dict[str, Any]]):
        """更新成员副本进度"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 删除现有副本记录
            cursor.execute('DELETE FROM member_raids WHERE member_id = ?', (member_id,))
            
            # 插入新副本记录
            for raid in raids_data:
                cursor.execute('''
                    INSERT INTO member_raids (
                        member_id, raid_name, raid_expansion, difficulty,
                        progress_current, progress_total
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    member_id, raid.get('name'), raid.get('expansion'),
                    raid.get('difficulty'), raid.get('progress_current', 0),
                    raid.get('progress_total', 0)
                ))
            
            conn.commit()
    

    
    def get_member_by_name(self, name: str, realm_name: str) -> Optional[Dict[str, Any]]:
        """根据角色名和服务器名获取成员信息"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM guild_members 
                WHERE name = ? AND realm_name = ?
            ''', (name, realm_name))
            
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    def get_all_members(self, limit: int = None, offset: int = 0) -> List[Dict[str, Any]]:
        """获取所有成员信息"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = 'SELECT * FROM guild_members ORDER BY name'
            if limit:
                query += f' LIMIT {limit} OFFSET {offset}'
            
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_members_by_class(self, class_name: str) -> List[Dict[str, Any]]:
        """根据职业获取成员列表"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM guild_members 
                WHERE class = ? 
                ORDER BY mythic_score DESC, name
            ''', (class_name,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_members_by_realm(self, realm_name: str) -> List[Dict[str, Any]]:
        """根据服务器获取成员列表"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM guild_members 
                WHERE realm_name = ? 
                ORDER BY mythic_score DESC, name
            ''', (realm_name,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_top_mythic_players(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取Mythic+评分最高的玩家"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM guild_members 
                WHERE mythic_score > 0 
                ORDER BY mythic_score DESC 
                LIMIT ?
            ''', (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取公会统计信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 总成员数
            cursor.execute('SELECT COUNT(*) FROM guild_members')
            total_members = cursor.fetchone()[0]
            
            # 活跃成员数（7天内上线）
            cursor.execute('SELECT COUNT(*) FROM guild_members WHERE last_online_days <= 7')
            active_members = cursor.fetchone()[0]
            
            # 职业分布
            cursor.execute('''
                SELECT class, COUNT(*) as count 
                FROM guild_members 
                GROUP BY class 
                ORDER BY count DESC
            ''')
            class_distribution = dict(cursor.fetchall())
            
            # 种族分布
            cursor.execute('''
                SELECT race, COUNT(*) as count 
                FROM guild_members 
                GROUP BY race 
                ORDER BY count DESC
            ''')
            race_distribution = dict(cursor.fetchall())
            
            # 性别分布
            cursor.execute('''
                SELECT sex, COUNT(*) as count 
                FROM guild_members 
                GROUP BY sex 
                ORDER BY count DESC
            ''')
            gender_distribution = dict(cursor.fetchall())
            
            # 阵营分布
            cursor.execute('''
                SELECT faction, COUNT(*) as count 
                FROM guild_members 
                GROUP BY faction 
                ORDER BY count DESC
            ''')
            faction_distribution = dict(cursor.fetchall())
            
            # 服务器分布
            cursor.execute('''
                SELECT realm_name, COUNT(*) as count 
                FROM guild_members 
                GROUP BY realm_name 
                ORDER BY count DESC
            ''')
            server_distribution = dict(cursor.fetchall())
            
            return {
                'total_members': total_members,
                'active_members': active_members,
                'class_distribution': class_distribution,
                'race_distribution': race_distribution,
                'gender_distribution': gender_distribution,
                'faction_distribution': faction_distribution,
                'server_distribution': server_distribution
            }
    
    def log_sync(self, sync_type: str, records_processed: int, 
                 records_updated: int, records_inserted: int, 
                 status: str, error_message: str = None):
        """记录数据同步日志"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO sync_logs (
                    sync_type, records_processed, records_updated,
                    records_inserted, status, error_message
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (sync_type, records_processed, records_updated, 
                  records_inserted, status, error_message))
            
            conn.commit() 