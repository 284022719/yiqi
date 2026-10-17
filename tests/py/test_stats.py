#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据管道核心逻辑测试

覆盖三处曾经出过错的地方：
1. 去重规则（同角色多行）
2. 活跃口径（以数据集最新时间为基准，而不是墙上时钟）
3. 排行榜排序与截断
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from build_page_data import PageDataGenerator  # noqa: E402
from timeutil import to_unix_seconds  # noqa: E402

DAY_MS = 86400 * 1000
LATEST_MS = 1754329119000  # 2025-08-04，与数据库中的真实最大值一致


def make_generator(active_days=30):
    """构造实例但不碰数据库：__init__ 只做路径解析。"""
    generator = PageDataGenerator(db_path="does-not-exist.db")
    generator.active_days = active_days
    return generator


def character(name, realm="arthos", login_days_ago=0, **overrides):
    """login_days_ago 以数据集最新时间为基准往前推。"""
    data = {
        "name": name,
        "realm": realm,
        "class": "战士",
        "level": 80,
        "achievement_points": 10000,
        "average_item_level": 600.0,
        "mythic_score": 2000,
        "last_login_timestamp": LATEST_MS - login_days_ago * DAY_MS,
        "updated_at": "2026-01-01 00:00:00",
    }
    data.update(overrides)
    return data


class DeduplicateTest(unittest.TestCase):
    def test_keeps_latest_login_row(self):
        rows = [
            character("Acg", login_days_ago=10),
            character("Acg", login_days_ago=1, **{"class": "法师"}),
        ]
        result = PageDataGenerator.deduplicate(rows)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["class"], "法师")

    def test_same_name_different_realm_are_both_kept(self):
        rows = [character("Acg", realm="arthos"), character("Acg", realm="zuldrak")]
        self.assertEqual(len(PageDataGenerator.deduplicate(rows)), 2)

    def test_millisecond_and_second_mix_is_normalised(self):
        """一行毫秒、一行秒，应被识别为同一角色而不是两条。"""
        rows = [
            character("Acg", login_days_ago=10, last_login_timestamp=LATEST_MS // 1000),
            character("Acg", login_days_ago=10),
        ]
        result = PageDataGenerator.deduplicate(rows)
        self.assertEqual(len(result), 1)
        # 保留的是原始记录，比较时才做单位归一化
        self.assertEqual(to_unix_seconds(result[0]["last_login_timestamp"]), LATEST_MS // 1000)

    def test_null_login_is_kept_when_only_row(self):
        rows = [character("Acg", last_login_timestamp=None)]
        self.assertEqual(len(PageDataGenerator.deduplicate(rows)), 1)

    def test_tie_breaks_on_updated_at(self):
        rows = [
            character("Acg", updated_at="2025-01-01 00:00:00"),
            character("Acg", updated_at="2026-05-05 00:00:00", **{"class": "牧师"}),
        ]
        result = PageDataGenerator.deduplicate(rows)
        self.assertEqual(result[0]["class"], "牧师")


class CalculateStatisticsTest(unittest.TestCase):
    def setUp(self):
        self.generator = make_generator(active_days=30)

    def test_empty_input(self):
        stats = self.generator.calculate_statistics([])
        self.assertEqual(stats["totalMembers"], 0)
        self.assertEqual(stats["activeMembers"], 0)
        self.assertEqual(stats["dataCompleteness"]["percentage"], 0)

    def test_active_window_uses_dataset_latest_not_wall_clock(self):
        """数据整体停在 2025 年，按墙上时钟会算出 0 活跃；这里必须按数据集基准。"""
        rows = [
            character("A", login_days_ago=0),
            character("B", login_days_ago=10),
            character("C", login_days_ago=40),
            character("D", last_login_timestamp=None),
        ]
        stats = self.generator.calculate_statistics(rows)

        self.assertEqual(stats["totalMembers"], 4)
        self.assertEqual(stats["activeMembers"], 2)
        self.assertEqual(stats["activeWindow"]["basis"], "dataset_latest")
        self.assertEqual(stats["activeWindow"]["days"], 30)
        self.assertEqual(stats["activeWindow"]["latest"], "2025-08-04")

    def test_active_days_configurable(self):
        rows = [character("A", login_days_ago=0), character("B", login_days_ago=40)]
        self.assertEqual(self.generator.calculate_statistics(rows)["activeMembers"], 1)

        wide = make_generator(active_days=90)
        self.assertEqual(wide.calculate_statistics(rows)["activeMembers"], 2)

    def test_active_never_exceeds_total(self):
        rows = [character(f"C{i}", login_days_ago=i) for i in range(5)]
        stats = self.generator.calculate_statistics(rows)
        self.assertLessEqual(stats["activeMembers"], stats["totalMembers"])

    def test_completeness_requires_both_fields(self):
        rows = [
            character("A"),
            character("B", average_item_level=0),
            character("C", achievement_points=0),
        ]
        completeness = self.generator.calculate_statistics(rows)["dataCompleteness"]
        self.assertEqual(completeness["total"], 3)
        self.assertEqual(completeness["complete"], 1)
        self.assertEqual(completeness["incomplete"], 2)
        self.assertAlmostEqual(completeness["percentage"], 33.3, places=1)

    def test_all_rows_without_login_time(self):
        rows = [character("A", last_login_timestamp=None)]
        stats = self.generator.calculate_statistics(rows)
        self.assertEqual(stats["activeMembers"], 0)
        self.assertIsNone(stats["activeWindow"]["latest"])


class RankTest(unittest.TestCase):
    def test_sorted_desc_and_rank_continuous(self):
        rows = [
            character("low", achievement_points=100),
            character("high", achievement_points=900),
            character("mid", achievement_points=500),
        ]
        ranked = PageDataGenerator._rank(rows, "achievement_points")
        self.assertEqual([r["name"] for r in ranked], ["high", "mid", "low"])
        self.assertEqual([r["rank"] for r in ranked], [1, 2, 3])

    def test_limit_is_applied(self):
        rows = [character(f"C{i}", achievement_points=i) for i in range(30)]
        self.assertEqual(len(PageDataGenerator._rank(rows, "achievement_points", limit=20)), 20)

    def test_missing_field_treated_as_zero(self):
        rows = [character("A", achievement_points=None), character("B", achievement_points=1)]
        ranked = PageDataGenerator._rank(rows, "achievement_points")
        self.assertEqual(ranked[0]["name"], "B")
        self.assertEqual(ranked[1]["achievement_points"], 0)


class DistributionTest(unittest.TestCase):
    def test_counts_and_sorts_desc(self):
        rows = [
            character("A", realm="arthos"),
            character("B", realm="arthos"),
            character("C", realm="zuldrak"),
        ]
        result = PageDataGenerator._distribution(rows, "realm")
        self.assertEqual(result[0], {"name": "arthos", "value": 2})
        self.assertEqual(result[1], {"name": "zuldrak", "value": 1})

    def test_empty_field_uses_default_label(self):
        rows = [character("A", realm=None), character("B", realm="")]
        result = PageDataGenerator._distribution(rows, "realm")
        self.assertEqual(result[0]["name"], "未知")
        self.assertEqual(result[0]["value"], 2)


if __name__ == "__main__":
    unittest.main()
