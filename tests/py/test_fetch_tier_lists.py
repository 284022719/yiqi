#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天梯抓取解析测试：编号列表优先、分节结构回退、未知专精必须显式报错。

这里只测纯解析与渲染，不走网络——抓取逻辑由 .github/workflows/tier-list-refresh.yml 兜。
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import fetch_tier_lists as ftl  # noqa: E402

GUIDE = ftl.GUIDES[0]

NUMBERED_PAGE = """Title: DPS Raid Rankings - Test
URL Source: https://example.com/guide
Markdown Content:
## Patch 12.1 DPS Tier List

### Filter Buttons

S

A

1.   Arms Warrior (A Tier)

2.   Devourer Demon Hunter (A+ Tier)

3.   Affliction Warlock (B Tier)
"""

HEADING_PAGE = """Title: Tank Tier List - Test
Markdown Content:
### **S-Tier Specs**
#### Blood Death Knight
### A-Tier Specs
#### Guardian Druid
#### Changelog
*   nothing to see here
### B-Tier Specs
#### Brewmaster Monk
"""

UNKNOWN_PAGE = """Title: 未知专精页
Markdown Content:
1.   Pirate Rogue (S Tier)
2.   Frost Mage (A Tier)
3.   Fire Mage (A Tier)
4.   Arcane Mage (A Tier)
"""

AUTHOR_PAGE = """Title: x
Markdown Content:
I'm not sure this is a good idea.

#### About the Author

Hi, I'm YoDa. I have been tanking since Shadowlands.
"""


class NumberedListTest(unittest.TestCase):
    def test_编号列表优先且支持A_加档(self):
        page = ftl.parse_page(NUMBERED_PAGE, GUIDE)
        self.assertEqual(page.title, "DPS Raid Rankings - Test")
        self.assertEqual(page.tiers["A"], ["warrior|武器"])
        self.assertEqual(page.tiers["A+"], ["demon-hunter|噬灭"])
        self.assertEqual(page.tiers["B"], ["warlock|痛苦"])
        self.assertNotIn("S", page.tiers)

    def test_过滤按钮里的裸字母不会被当成层级(self):
        page = ftl.parse_page(NUMBERED_PAGE, GUIDE)
        self.assertEqual(sum(len(v) for v in page.tiers.values()), 3)


class HeadingFallbackTest(unittest.TestCase):
    def test_没有编号列表时按分节标题取(self):
        page = ftl.parse_page(HEADING_PAGE, GUIDE)
        self.assertEqual(page.tiers["S"], ["death-knight|鲜血"])
        self.assertEqual(page.tiers["A"], ["druid|守护"])
        self.assertEqual(page.tiers["B"], ["monk|酒仙"])

    def test_bold标题也能识别(self):
        page = ftl.parse_page(HEADING_PAGE, GUIDE)
        self.assertIn("S", page.tiers)


class UnknownSpecTest(unittest.TestCase):
    def test_未登记专精要报出来而不是静默丢弃(self):
        page = ftl.parse_page(UNKNOWN_PAGE, GUIDE)
        self.assertTrue(any("Pirate Rogue" in item for item in page.unknowns))
        self.assertEqual(page.tiers["A"], ["mage|冰霜", "mage|火焰", "mage|奥术"])

    def test_一条专精都解析不出时直接失败(self):
        with self.assertRaises(ValueError):
            ftl.parse_page("Title: x\nMarkdown Content:\n没有排名内容\n", GUIDE)


class AuthorTest(unittest.TestCase):
    def test_作者只在About段落里取(self):
        self.assertEqual(ftl.extract_author(AUTHOR_PAGE), "YoDa")

    def test_正文里的I_m不会被当成作者(self):
        self.assertEqual(ftl.extract_author("Markdown Content:\nI'm not sure.\n"), "Wowhead")

    def test_中文署名优先(self):
        text = "Markdown Content:\n[来自 AutomaticJak](https://x) 已更新：  2026/10/13"
        self.assertEqual(ftl.extract_author(text), "AutomaticJak")


class RenderTest(unittest.TestCase):
    def test_渲染出七个层级且导出默认变量(self):
        page = ftl.parse_page(NUMBERED_PAGE, GUIDE)
        content = ftl.render_js(GUIDE, page)
        for tier in ftl.TIER_ORDER:
            self.assertIn(f'"{tier}": {{', content)
        self.assertIn("export default dpsTierList;", content)
        self.assertIn('"sourceUrl": "https://www.wowhead.com/cn/guide/classes/tier-lists/'
                      'dps-rankings-raids"', content)


if __name__ == "__main__":
    unittest.main()
