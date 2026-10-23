#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Raider.IO 版 page_data 生成器的单元测试（不联网）。

钉住三件容易出错的事：
1. 跨服同名是两个人，不能被当成重复；
2. 中文名词表走 wow_terms（服务器查不到时回退英文，不能瞎猜）；
3. 活跃口径 = 本季有 M+ 记录 ∪ 窗口内被 RIO 更新过。
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import build_page_data_rio as builder  # noqa: E402

ROSTER = {
    "source": "raider.io",
    "fetchedAt": "2026/10/24",
    "guild": {"name": "一起", "region": "cn", "realm": "Arthas", "faction": "horde"},
    "memberCount": 4,
    "enriched": 4,
    "members": [
        {
            "name": "甲", "realm": "Arthas", "realmSlug": "arthas",
            "classEn": "Paladin", "specEn": "Holy", "raceEn": "Blood Elf",
            "gender": "female", "faction": "horde", "rank": 1,
            "achievementPoints": 100, "itemLevel": 300, "mplusScore": 1000,
            "mplusSeason": "season-mn-2", "rioLastCrawled": "2026-10-23",
        },
        # 同一角色被抓了两次：去重时保留装备更好的那条
        {
            "name": "甲", "realm": "Arthas", "realmSlug": "arthas",
            "classEn": "Paladin", "specEn": "Holy", "raceEn": "Blood Elf",
            "gender": "female", "faction": "horde", "rank": 1,
            "achievementPoints": 120, "itemLevel": 310, "mplusScore": 0,
            "mplusSeason": None, "rioLastCrawled": "2026-10-22",
        },
        {
            "name": "乙", "realm": "Unknown Realm", "realmSlug": "unknown-realm",
            "classEn": "Mage", "specEn": "Frost", "raceEn": "Human",
            "gender": "male", "faction": "alliance", "rank": 7,
            "achievementPoints": 0, "itemLevel": 0, "mplusScore": 0,
            "mplusSeason": None, "rioLastCrawled": "2026-07-01",
        },
        # 跨服同名，必须保留
        {
            "name": "甲", "realm": "Deathwing", "realmSlug": "deathwing",
            "classEn": "Demon Hunter", "specEn": "Devourer", "raceEn": "Haranir",
            "gender": "male", "faction": "horde", "rank": 7,
            "achievementPoints": 50, "itemLevel": 250, "mplusScore": 200,
            "mplusSeason": "season-mn-2", "rioLastCrawled": "2026-09-01",
        },
    ],
}


class NormalizeTest(unittest.TestCase):
    def test_中文名词表(self):
        characters = builder.normalize(ROSTER)
        first = characters[0]
        self.assertEqual(first["realm"], "阿尔萨斯")
        self.assertEqual(first["class"], "圣骑士")
        self.assertEqual(first["spec"], "神圣")
        self.assertEqual(first["race"], "血精灵")
        self.assertEqual(first["gender"], "女")
        self.assertEqual(first["faction"], "Horde")

    def test_未收录服务器回退英文名(self):
        characters = builder.normalize(ROSTER)
        self.assertEqual(characters[2]["realm"], "Unknown Realm")

    def test_新种族与新专精(self):
        characters = builder.normalize(ROSTER)
        demon_hunter = characters[3]
        self.assertEqual(demon_hunter["race"], "哈拉尼尔")
        self.assertEqual(demon_hunter["spec"], "噬灭")
        self.assertEqual(demon_hunter["class"], "恶魔猎手")


class DeduplicateTest(unittest.TestCase):
    def test_同名不同服保留为两个角色(self):
        characters = builder.deduplicate(builder.normalize(ROSTER))
        self.assertEqual(len(characters), 3)
        realms = sorted(c["realm"] for c in characters)
        self.assertEqual(realms, ["Unknown Realm", "死亡之翼", "阿尔萨斯"])

    def test_同服重复保留信息更完整的一条(self):
        characters = builder.deduplicate(builder.normalize(ROSTER))
        same = [c for c in characters if c["name"] == "甲" and c["realm"] == "阿尔萨斯"][0]
        self.assertEqual(same["average_item_level"], 310)
        self.assertEqual(same["achievement_points"], 120)


class StatisticsTest(unittest.TestCase):
    def setUp(self):
        self.characters = builder.deduplicate(builder.normalize(ROSTER))
        self.stats = builder.calculate_statistics(self.characters)

    def test_活跃口径是并集(self):
        self.assertEqual(self.stats["totalMembers"], 3)
        # 甲@阿尔萨斯 本季 M+ > 0；甲@死亡之翼 分数 200 也算；乙 既没分数、更新时间又在窗口外
        self.assertEqual(self.stats["activeMembers"], 2)
        self.assertEqual(self.stats["activeWindow"]["mplusActive"], 2)
        self.assertEqual(self.stats["activeWindow"]["latest"], "2026-10-23")

    def test_数据完整率(self):
        completeness = self.stats["dataCompleteness"]
        self.assertEqual(completeness["complete"], 2)
        self.assertEqual(completeness["percentage"], 66.7)


class BuildTest(unittest.TestCase):
    def test_输出结构与元信息自洽(self):
        page = builder.build_page_data(ROSTER)
        self.assertEqual(page["stats"]["totalMembers"], 3)
        self.assertEqual(page["meta"]["sourceRows"], 4)
        self.assertEqual(page["meta"]["uniqueCharacters"], 3)
        self.assertEqual(page["meta"]["duplicatesRemoved"], 1)
        self.assertEqual(page["meta"]["source"], "raider.io")
        for series in page["charts"].values():
            self.assertTrue(series)

    def test_排行榜非空且名次连续(self):
        page = builder.build_page_data(ROSTER)
        for key in ("achievementRanking", "itemLevelRanking", "mythicScoreRanking"):
            rows = page["rankings"][key]
            self.assertTrue(rows, key)
            self.assertEqual([row["rank"] for row in rows], list(range(1, len(rows) + 1)))
        self.assertNotIn("mounts_now", page["rankings"]["achievementRanking"][0])


if __name__ == "__main__":
    unittest.main()
