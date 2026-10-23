#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公会成员抓取脚本的纯函数测试（不联网）。

重点覆盖两点：职业英文名 → 项目 slug 的映射，以及从 profile_url 里取服务器 slug——
后者用于逐角色补 ilvl/分数，写错就会全量 404。
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import fetch_guild_roster as fgr  # noqa: E402

SAMPLE = {
    "rank": 2,
    "character": {
        "name": "雪蒂凯",
        "realm": "Arthas",
        "class": "Death Knight",
        "active_spec_name": "Frost",
        "active_spec_role": "DPS",
        "race": "Blood Elf",
        "gender": "female",
        "faction": "horde",
        "achievement_points": 20000,
        "last_crawled_at": "2026-10-21T11:24:15.000Z",
        "profile_url": "https://raider.io/characters/cn/arthas/雪蒂凯",
    },
}

# 带空格与撇号的服务器名，slug 规则最容易在这里出错
SAMPLE_ZULDRAK = {
    "rank": 7,
    "character": {
        "name": "Alencetr",
        "realm": "Zul'Drak",
        "class": "Hunter",
        "last_crawled_at": "2026-10-01T00:00:00.000Z",
        "profile_url": "https://raider.io/characters/cn/zuldrak/Alencetr",
    },
}


class NormalizeTest(unittest.TestCase):
    def test_基本字段与职业slug(self):
        member = fgr.normalize_member(SAMPLE)
        self.assertEqual(member["name"], "雪蒂凯")
        self.assertEqual(member["classSlug"], "death-knight")
        self.assertEqual(member["rank"], 2)
        self.assertEqual(member["achievementPoints"], 20000)
        self.assertEqual(member["rioLastCrawled"], "2026-10-21")

    def test_从profile_url取服务器slug(self):
        self.assertEqual(fgr.normalize_member(SAMPLE)["realmSlug"], "arthas")
        self.assertEqual(fgr.normalize_member(SAMPLE_ZULDRAK)["realmSlug"], "zuldrak")

    def test_缺字段不抛异常(self):
        member = fgr.normalize_member({"rank": 7, "character": {"name": "X"}})
        self.assertEqual(member["classSlug"], "")
        self.assertEqual(member["realmSlug"], "")
        self.assertEqual(member["achievementPoints"], 0)


class ClassMapTest(unittest.TestCase):
    def test_十三个职业都有slug(self):
        self.assertEqual(len(fgr.CLASS_SLUGS), 13)
        slugs = sorted(fgr.CLASS_SLUGS.values())
        self.assertEqual(slugs, sorted(set(slugs)), "slug 不应重复")
        for slug in slugs:
            self.assertRegex(slug, r"^[a-z-]+$")


if __name__ == "__main__":
    unittest.main()
