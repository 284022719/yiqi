#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新页面数据脚本（旧链路）

在英雄榜爬虫完成后运行，重新生成 data/page_data.json。
当前默认链路是 tools/fetch_guild_roster.py + tools/build_page_data_rio.py，见 docs/DATA_PIPELINE.md §12。
路径解析统一走 paths.py，不依赖调用时的 cwd。
"""

import sys

from build_page_data import PageDataGenerator
from paths import resolve_db_path


def main() -> bool:
    print("=== 自动更新页面数据 ===")

    db_path = resolve_db_path()
    if not db_path.exists():
        print(f"❌ 数据库文件不存在: {db_path}")
        print("请先运行爬虫脚本获取数据")
        return False

    try:
        import sqlite3

        with sqlite3.connect(db_path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM guild_characters").fetchone()[0]

        if count == 0:
            print("❌ 数据库中没有角色数据")
            print("请先运行爬虫脚本获取数据")
            return False

        print(f"✅ 数据库中有 {count} 条角色记录")
    except Exception as error:  # noqa: BLE001
        print(f"❌ 检查数据库失败: {error}")
        return False

    success = PageDataGenerator(db_path=str(db_path)).run()

    if success:
        print("\n✅ 页面数据更新成功！")
    else:
        print("\n❌ 页面数据更新失败！")
    return success


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
