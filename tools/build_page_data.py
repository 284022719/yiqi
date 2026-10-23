#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从数据库生成 data/page_data.json，供前端直接 fetch。

**已不是默认链路**：英雄榜（wow.blizzard.cn）现在要战网登录，这条管线只适合「手里已有登录态导出的
guild_database.db」的场景。首页当前走 tools/build_page_data_rio.py（Raider.IO，公开接口），
两套脚本输出的结构一致但统计口径不同，见 docs/DATA_PIPELINE.md §4。

相对旧版的修正：
1. 不再硬编码 cut-off 时间戳，也不再把毫秒时间戳当秒比较（见 timeutil.py）。
2. 统计口径拆分为三个独立指标：totalMembers / activeMembers / dataCompleteness。
3. 生成前按 (name, realm) 去重，避免重复记录虚增总数与排名。
4. 「活跃」以数据集内最新登录时间为基准，而不是墙上时钟——
   否则数据未及时更新时，页面会显示「0 人活跃」。
5. 输出 meta 字段，便于 validate.py 做数据质量断言。
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from paths import PAGE_DATA_PATH, resolve_db_path
from timeutil import format_millis, to_unix_seconds

ACTIVE_DAYS = int(os.environ.get("ACTIVE_DAYS", "30"))

# 完整性口径：成就点数与平均装等都有值才算「完整」
CORE_FIELDS = ("achievement_points", "average_item_level")


class PageDataGenerator:
    def __init__(self, db_path: Optional[str] = None, output_path: Optional[str] = None):
        self.db_path = resolve_db_path(db_path)
        self.output_path = PAGE_DATA_PATH if output_path is None else output_path
        self.active_days = ACTIVE_DAYS

    # ------------------------------------------------------------------ 读取

    def get_database_connection(self) -> sqlite3.Connection:
        if not self.db_path.exists():
            raise FileNotFoundError(
                f"未找到数据库: {self.db_path}\n"
                f"请先运行爬虫（tools/mounts_crawler.py）生成数据。"
            )
        return sqlite3.connect(self.db_path)

    def get_character_data(self) -> List[Dict[str, Any]]:
        """读取全部角色记录（不做日期过滤，过滤逻辑在 Python 侧统一处理）。"""
        with self.get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, class, level, achievement_points, average_item_level,
                       faction, realm, spec, guild, mythic_score, race, sex,
                       mounts_now, mounts_total, last_login_timestamp, updated_at
                FROM guild_characters
            """)
            columns = [description[0] for description in cursor.description]
            characters = []
            for row in cursor.fetchall():
                character = dict(zip(columns, row))
                character["achievement_points"] = character.get("achievement_points") or 0
                character["average_item_level"] = character.get("average_item_level") or 0
                character["level"] = character.get("level") or 0
                character["mythic_score"] = character.get("mythic_score") or 0
                character["mounts_now"] = character.get("mounts_now") or 0
                character["mounts_total"] = character.get("mounts_total") or 0
                characters.append(character)
            return characters

    # ------------------------------------------------------------------ 清洗

    @staticmethod
    def deduplicate(characters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """按 (name, realm) 去重，保留信息最完整的一条。

        同一角色可能因多次抓取产生多行；保留规则：
        登录时间更晚 > 更新时间更晚 > 原始顺序靠前。
        """
        best: Dict[tuple, Dict[str, Any]] = {}
        for character in characters:
            key = (character.get("name"), character.get("realm"))
            login = to_unix_seconds(character.get("last_login_timestamp")) or 0
            previous = best.get(key)
            if previous is None:
                best[key] = character
                continue

            previous_login = to_unix_seconds(previous.get("last_login_timestamp")) or 0
            if login > previous_login:
                best[key] = character
            elif login == previous_login:
                if str(character.get("updated_at") or "") > str(previous.get("updated_at") or ""):
                    best[key] = character

        return list(best.values())

    # ------------------------------------------------------------------ 统计

    def calculate_statistics(self, characters: List[Dict[str, Any]]) -> Dict[str, Any]:
        total = len(characters)
        if total == 0:
            return {
                "totalMembers": 0,
                "activeMembers": 0,
                "activeWindow": {"days": self.active_days, "since": None, "basis": "dataset_latest"},
                "dataCompleteness": {"total": 0, "complete": 0, "incomplete": 0, "percentage": 0},
            }

        logins = [
            to_unix_seconds(c.get("last_login_timestamp"))
            for c in characters
            if c.get("last_login_timestamp")
        ]
        dataset_latest = max(logins) if logins else None

        if dataset_latest:
            window_start = dataset_latest - self.active_days * 86400
            active = sum(
                1
                for c in characters
                if (to_unix_seconds(c.get("last_login_timestamp")) or 0) >= window_start
            )
        else:
            window_start = None
            active = 0

        complete = sum(
            1 for c in characters if all(c.get(field, 0) > 0 for field in CORE_FIELDS)
        )
        incomplete = total - complete

        assert 0 <= active <= total, f"activeMembers({active}) 不应超过 totalMembers({total})"

        return {
            "totalMembers": total,
            "activeMembers": active,
            "activeWindow": {
                "days": self.active_days,
                "since": format_millis(window_start, "%Y-%m-%d") if window_start else None,
                "latest": format_millis(dataset_latest, "%Y-%m-%d") if dataset_latest else None,
                "basis": "dataset_latest",
            },
            "dataCompleteness": {
                "total": total,
                "complete": complete,
                "incomplete": incomplete,
                "percentage": round(complete / total * 100, 1),
            },
        }

    # ------------------------------------------------------------------ 图表

    @staticmethod
    def _distribution(characters: List[Dict[str, Any]], field: str, default: str = "未知") -> List[Dict[str, Any]]:
        counts: Dict[str, int] = {}
        for character in characters:
            value = character.get(field) or default
            counts[value] = counts.get(value, 0) + 1
        return [
            {"name": name, "value": count}
            for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        ]

    def generate_chart_data(self, characters: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        gender_counts: Dict[str, int] = {}
        for character in characters:
            sex = character.get("sex")
            label = "男" if sex == "Male" else "女" if sex == "Female" else "未知"
            gender_counts[label] = gender_counts.get(label, 0) + 1

        return {
            "classDistribution": self._distribution(characters, "class"),
            "factionDistribution": self._distribution(characters, "faction"),
            "raceDistribution": self._distribution(characters, "race"),
            "realmDistribution": self._distribution(characters, "realm"),
            "genderDistribution": [
                {"name": name, "value": count} for name, count in gender_counts.items()
            ],
        }

    # ------------------------------------------------------------------ 排名

    @staticmethod
    def _rank(characters: List[Dict[str, Any]], sort_field: str, limit: int = 20) -> List[Dict[str, Any]]:
        ordered = sorted(
            characters,
            key=lambda c: (
                -(c.get(sort_field) or 0),
                -(c.get("achievement_points") or 0),
                str(c.get("name") or ""),
            ),
        )
        return [
            {
                "rank": index,
                "name": character.get("name") or "",
                "realm": character.get("realm") or "",
                "class": character.get("class") or "",
                "spec": character.get("spec") or "",
                # 注意用 `or 0`：字段存在但值为 None 时，dict.get 的默认值不生效
                "achievement_points": character.get("achievement_points") or 0,
                "average_item_level": character.get("average_item_level") or 0,
                "mythic_score": character.get("mythic_score") or 0,
                "mounts_now": character.get("mounts_now") or 0,
            }
            for index, character in enumerate(ordered[:limit], 1)
        ]

    def generate_rankings(self, characters: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        return {
            "achievementRanking": self._rank(characters, "achievement_points"),
            "itemLevelRanking": self._rank(characters, "average_item_level"),
            "mythicScoreRanking": self._rank(characters, "mythic_score"),
        }

    # ------------------------------------------------------------------ 汇总

    def generate_page_data(self) -> Dict[str, Any]:
        print(f"[1/4] 读取数据库: {self.db_path}")
        raw_characters = self.get_character_data()
        print(f"      原始记录: {len(raw_characters)}")

        characters = self.deduplicate(raw_characters)
        removed = len(raw_characters) - len(characters)
        print(f"[2/4] 去重后:   {len(characters)}（移除重复 {removed} 条）")

        if not characters:
            raise SystemExit("数据库中没有可用角色数据，已中止生成。")

        stats = self.calculate_statistics(characters)
        window = stats["activeWindow"]
        print(
            f"      活跃口径: 最近 {window['days']} 天内登录，"
            f"基准={window['latest']}，下界={window['since']}，命中={stats['activeMembers']}/{stats['totalMembers']}"
        )

        print("[3/4] 生成图表与排行榜数据")
        charts = self.generate_chart_data(characters)
        rankings = self.generate_rankings(characters)

        null_logins = sum(1 for c in raw_characters if not c.get("last_login_timestamp"))

        # lastUpdated 是「本次生成时间」，dataAsOf 是「数据本身截至的时间」。
        # 两者分开，避免数据长期不更新时页面显示成新鲜数据。
        data_as_of = stats.get("activeWindow", {}).get("latest")

        return {
            "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dataAsOf": data_as_of,
            "stats": stats,
            "charts": charts,
            "rankings": rankings,
            "meta": {
                "sourceRows": len(raw_characters),
                "uniqueCharacters": len(characters),
                "duplicatesRemoved": removed,
                "rowsWithoutLoginTime": null_logins,
                "generator": "tools/build_page_data.py",
            },
        }

    def save_page_data(self, page_data: Dict[str, Any]) -> bool:
        try:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.output_path, "w", encoding="utf-8") as handle:
                json.dump(page_data, handle, ensure_ascii=False, indent=2)
            print(f"[4/4] 写入: {self.output_path}")
            return True
        except Exception as error:  # noqa: BLE001 - 生成脚本顶层需要兜底
            print(f"保存页面数据失败: {error}", file=sys.stderr)
            return False

    def run(self) -> bool:
        try:
            print("=== 生成 page_data.json ===")
            page_data = self.generate_page_data()
            if not self.save_page_data(page_data):
                return False

            stats = page_data["stats"]
            print("=== 完成 ===")
            print(f"总成员      : {stats['totalMembers']}")
            print(f"近 {self.active_days} 天活跃 : {stats['activeMembers']}")
            print(f"数据完整率  : {stats['dataCompleteness']['percentage']}%")
            print(f"更新时间    : {page_data['lastUpdated']}")
            return True
        except Exception as error:  # noqa: BLE001
            print(f"生成页面数据失败: {error}", file=sys.stderr)
            return False


def main() -> None:
    success = PageDataGenerator().run()
    raise SystemExit(0 if success else 1)


if __name__ == "__main__":
    main()
