import sqlite3
import json
from pathlib import Path

def check_old_database():
    """检查旧数据库的结构和数据"""
    old_db_path = Path("../data/database/guild_members.db")
    
    if not old_db_path.exists():
        print("旧数据库文件不存在")
        return
    
    conn = sqlite3.connect(str(old_db_path))
    cursor = conn.cursor()
    
    # 获取表结构
    cursor.execute("PRAGMA table_info(guild_members)")
    columns = cursor.fetchall()
    print("=== 旧数据库表结构 ===")
    for col in columns:
        print(f"列名: {col[1]}, 类型: {col[2]}, 非空: {col[3]}, 默认值: {col[4]}")
    
    # 获取前几条数据
    cursor.execute("SELECT * FROM guild_members LIMIT 5")
    rows = cursor.fetchall()
    
    # 获取列名
    cursor.execute("SELECT * FROM guild_members LIMIT 0")
    column_names = [description[0] for description in cursor.description]
    
    print("\n=== 前5条数据 ===")
    for i, row in enumerate(rows):
        print(f"\n记录 {i+1}:")
        for j, value in enumerate(row):
            print(f"  {column_names[j]}: {value} (类型: {type(value).__name__})")
    
    # 检查空值情况
    print("\n=== 空值统计 ===")
    for col_name in column_names:
        cursor.execute(f"SELECT COUNT(*) FROM guild_members WHERE {col_name} IS NULL")
        null_count = cursor.fetchone()[0]
        cursor.execute(f"SELECT COUNT(*) FROM guild_members")
        total_count = cursor.fetchone()[0]
        print(f"{col_name}: {null_count}/{total_count} 为空 ({null_count/total_count*100:.1f}%)")
    
    conn.close()

if __name__ == "__main__":
    check_old_database() 