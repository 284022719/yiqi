#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新页面数据脚本
在爬虫完成后自动运行，更新page_data.json
"""

import os
import sys
from generate_page_data import PageDataGenerator

def main():
    """主函数"""
    print("=== 自动更新页面数据 ===")
    
    # 检查数据库文件是否存在
    db_path = "data/guild_database.db"
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        print("请先运行爬虫脚本获取数据")
        return False
    
    # 检查guild_characters表是否有数据
    try:
        import sqlite3
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM guild_characters")
            count = cursor.fetchone()[0]
            
            if count == 0:
                print("❌ 数据库中没有角色数据")
                print("请先运行爬虫脚本获取数据")
                return False
            
            print(f"✅ 数据库中有 {count} 个角色数据")
    except Exception as e:
        print(f"❌ 检查数据库失败: {e}")
        return False
    
    # 生成页面数据
    generator = PageDataGenerator()
    success = generator.run()
    
    if success:
        print("\n✅ 页面数据更新成功！")
        print("现在可以刷新网页查看最新数据。")
        return True
    else:
        print("\n❌ 页面数据更新失败！")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 