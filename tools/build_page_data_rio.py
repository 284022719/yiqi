#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 Raider.IO 成员名单生成 data/page_data.json。

为什么不再用 build_page_data.py：
    那套管线读的是英雄榜导出的 SQLite（guild_characters），而英雄榜现在必须登录。
    Raider.IO 公开接口能给出成员身份/会阶/职业/专精/种族/阵营/成就点，
    加 --enrich 还能拿到装备等级与本季大秘境分数，足够支撑首页的全部图表与排行榜。

口径变化（重要）：
    - 「活跃」不再按「最后登录天数」，改成「本季有大秘境记录 或 RIO 最近 30 天更新过」，
      因为最后在线时间只有登录英雄榜才有。label 字段会写清楚，前端直接展示。
    - 「数据完整率」= 成就点数 > 0 且 装备等级 > 0 的占比。
    - 坐骑维度整个下线（RIO 没有这项数据，英雄榜的坐骑数据本来也全是同一个值）。

用法：
    python tools/fetch_guild_roster.py --enrich     # 先抓名单（含 ilvl / 分数）
    python tools/build_page_data_rio.py             # 再生成 data/page_data.json
    python tools/build_page_data_rio.py --check     # 只校验输入，不写文件
"""

from __future__ import annotations

import argparse
import os
import json
import logging
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from paths import PAGE_DATA_PATH, REPO_ROOT
from wow_terms import (
    class_cn,
    class_slug,
    faction_label,
    gender_cn,
    race_cn,
    realm_cn,
    spec_cn,
)

ROSTER_PATH = REPO_ROOT / "data" / "guildmember.rio.json"
# 活跃窗口天数可用环境变量覆盖，与旧管线保持一致的用法
ACTIVE_DAYS = int(os.environ.get("ACTIVE_DAYS", "30"))
RANK_LIMIT = 20
LOG = logging.getLogger("page-data-rio")


# ---------------------------------------------------------------------- 读入


def load_roster(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"未找到 {path}，请先运行 python tools/fetch_guild_roster.py --enrich")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def normalize(roster: dict) -> List[Dict[str, Any]]:
    """把 Raider.IO 的字段翻成页面用的口径（中文名 + 数值缺省 0）。"""
    characters = []
    for member in roster.get("members") or []:
        class_en = member.get("classEn") or ""
        characters.append(
            {
                "name": member.get("name") or "",
                "realm": realm_cn(member.get("realmSlug"), member.get("realm")),
                "class": class_cn(class_en),
                "class_slug": class_slug(class_en),
                "spec": spec_cn(class_en, member.get("specEn")),
                "race": race_cn(member.get("raceEn")),
                "faction": faction_label(member.get("faction")),
                "gender": gender_cn(member.get("gender")),
                "rank": member.get("rank") if member.get("rank") is not None else 99,
                "achievement_points": int(member.get("achievementPoints") or 0),
                "average_item_level": float(member.get("itemLevel") or 0),
                "mythic_score": float(member.get("mplusScore") or 0),
                "mplus_season": member.get("mplusSeason"),
                "rio_last_crawled": member.get("rioLastCrawled") or "",
            }
        )
    return characters


def deduplicate(characters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """按 (名字, 服务器) 去重；跨服同名是两个人，不能合并。

    同一角色偶尔会重复出现，逐字段取「更优值」而不是整条覆盖：
    装备等级/成就点/大秘境分数取最大，最后更新时间取最新——不同接口返回的新旧程度并不一致，
    整条取一条会丢掉另一条里的新分数。
    """
    best: Dict[tuple, Dict[str, Any]] = {}
    for character in characters:
        key = (character["name"], character["realm"])
        current = best.get(key)
        if current is None:
            best[key] = dict(character)
            continue
        current["achievement_points"] = max(current["achievement_points"], character["achievement_points"])
        current["average_item_level"] = max(
            current["average_item_level"], character["average_item_level"]
        )
        current["mythic_score"] = max(current["mythic_score"], character["mythic_score"])
        if character["mplus_season"]:
            current["mplus_season"] = character["mplus_season"]
        if (character["rio_last_crawled"] or "") > (current["rio_last_crawled"] or ""):
            current["rio_last_crawled"] = character["rio_last_crawled"]
    return list(best.values())


# ---------------------------------------------------------------------- 统计


def parse_date(value: str) -> Optional[date]:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def calculate_statistics(characters: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(characters)
    crawl_dates = [d for d in (parse_date(c["rio_last_crawled"]) for c in characters) if d]
    latest_crawl = max(crawl_dates) if crawl_dates else None

    window_start = latest_crawl - timedelta(days=ACTIVE_DAYS) if latest_crawl else None

    # 活跃 = 本季有大秘境记录，或 RIO 在窗口内更新过该角色
    active_window_members = [
        c
        for c in characters
        if c["mythic_score"] > 0
        or (window_start and (parse_date(c["rio_last_crawled"]) or date.min) >= window_start)
    ]
    active = len(active_window_members)
    mplus_active = sum(1 for c in characters if c["mythic_score"] > 0)

    complete = sum(
        1 for c in characters if c["achievement_points"] > 0 and c["average_item_level"] > 0
    )

    return {
        "totalMembers": total,
        "activeMembers": active,
        "activeWindow": {
            "days": ACTIVE_DAYS,
            "since": window_start.isoformat() if window_start else None,
            "latest": latest_crawl.isoformat() if latest_crawl else None,
            "basis": "rio_activity",
            "label": f"近 {ACTIVE_DAYS} 天活跃",
            "note": "本季有大秘境记录，或 Raider.IO 在窗口内更新过该角色",
            "mplusActive": mplus_active,
        },
        "dataCompleteness": {
            "total": total,
            "complete": complete,
            "incomplete": total - complete,
            "percentage": round(complete / total * 100, 1) if total else 0,
        },
    }


# ---------------------------------------------------------------------- 图表


def distribution(characters: List[Dict[str, Any]], field: str, default: str = "未知") -> List[Dict[str, Any]]:
    counts: Dict[str, int] = {}
    for character in characters:
        value = character.get(field) or default
        counts[value] = counts.get(value, 0) + 1
    return [
        {"name": name, "value": count}
        for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def generate_charts(characters: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    return {
        "classDistribution": distribution(characters, "class"),
        "factionDistribution": distribution(characters, "faction"),
        "raceDistribution": distribution(characters, "race"),
        "realmDistribution": distribution(characters, "realm"),
        "genderDistribution": distribution(characters, "gender"),
    }


# ---------------------------------------------------------------------- 排行


def rank(characters: List[Dict[str, Any]], sort_field: str, limit: int = RANK_LIMIT) -> List[Dict[str, Any]]:
    ordered = sorted(
        characters,
        key=lambda c: (-(c.get(sort_field) or 0), -c["achievement_points"], c["name"]),
    )
    return [
        {
            "rank": index,
            "name": character["name"],
            "realm": character["realm"],
            "class": character["class"],
            "spec": character["spec"],
            "achievement_points": character["achievement_points"],
            "average_item_level": character["average_item_level"],
            "mythic_score": character["mythic_score"],
        }
        for index, character in enumerate(ordered[:limit], 1)
    ]


def generate_rankings(characters: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    return {
        "achievementRanking": rank(characters, "achievement_points"),
        "itemLevelRanking": rank(characters, "average_item_level"),
        "mythicScoreRanking": rank(characters, "mythic_score"),
    }


# ---------------------------------------------------------------------- 汇总


def build_page_data(roster: dict) -> Dict[str, Any]:
    raw = normalize(roster)
    characters = deduplicate(raw)
    if not characters:
        raise SystemExit("名单里没有可用角色，已中止生成。")

    stats = calculate_statistics(characters)
    source_rows = len(roster.get("members") or [])
    data_as_of = (roster.get("fetchedAt") or "").replace("/", "-") or stats["activeWindow"]["latest"]

    return {
        "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dataAsOf": data_as_of,
        "stats": stats,
        "charts": generate_charts(characters),
        "rankings": generate_rankings(characters),
        "meta": {
            "source": "raider.io",
            "sourceRows": source_rows,
            "uniqueCharacters": len(characters),
            "duplicatesRemoved": source_rows - len(characters),
            "enriched": roster.get("enriched", 0),
            "guild": roster.get("guild"),
            "generator": "tools/build_page_data_rio.py",
        },
    }


def main(argv: Optional[List[str]] = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if not stream.isatty() and hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="从 Raider.IO 名单生成 data/page_data.json")
    parser.add_argument("--roster", type=Path, default=ROSTER_PATH)
    parser.add_argument("--out", type=Path, default=PAGE_DATA_PATH)
    parser.add_argument("--check", action="store_true", help="只校验输入，不写文件")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    page_data = build_page_data(load_roster(args.roster))
    stats = page_data["stats"]
    LOG.info("成员 %d（活跃 %d，其中本季 M+ %d）", stats["totalMembers"],
             stats["activeMembers"], stats["activeWindow"]["mplusActive"])
    LOG.info("数据完整率 %.1f%% | 数据截至 %s", stats["dataCompleteness"]["percentage"],
             page_data["dataAsOf"])

    if args.check:
        LOG.info("--check：未写文件")
        return 0

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(page_data, ensure_ascii=False, indent=2), encoding="utf-8")
    LOG.info("已写入 %s", args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
