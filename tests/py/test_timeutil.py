#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
timeutil 测试

重点：毫秒/秒混用是历史 bug 的根因，必须有回归保护。
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from timeutil import format_millis, format_seconds, to_unix_seconds  # noqa: E402


class ToUnixSecondsTest(unittest.TestCase):
    def test_milliseconds_are_converted(self):
        # 数据库里真实的毫秒值
        self.assertEqual(to_unix_seconds(1754329119000), 1754329119)

    def test_seconds_pass_through(self):
        self.assertEqual(to_unix_seconds(1754329119), 1754329119)

    def test_none_stays_none(self):
        self.assertIsNone(to_unix_seconds(None))

    def test_zero_is_preserved(self):
        self.assertEqual(to_unix_seconds(0), 0)

    def test_boundary_just_below_threshold_is_seconds(self):
        # 10_000_000_000 是阈值本身：不大于阈值，视为秒
        self.assertEqual(to_unix_seconds(10_000_000_000), 10_000_000_000)

    def test_boundary_just_above_threshold_is_milliseconds(self):
        self.assertEqual(to_unix_seconds(10_000_000_001), 10_000_000)

    def test_string_input_accepted(self):
        self.assertEqual(to_unix_seconds("1754329119000"), 1754329119)


class FormatTest(unittest.TestCase):
    def test_format_millis_default_is_date_only(self):
        self.assertEqual(format_millis(1754329119000), "2025-08-04")

    def test_format_seconds_carries_time(self):
        # 输出统一为 UTC
        self.assertEqual(format_seconds(1754329119), "2025-08-04 17:38:39")

    def test_format_accepts_seconds_too(self):
        self.assertEqual(format_millis(1754329119), "2025-08-04")

    def test_none_returns_empty_string(self):
        self.assertEqual(format_millis(None), "")
        self.assertEqual(format_seconds(None), "")


if __name__ == "__main__":
    unittest.main()
