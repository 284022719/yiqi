#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据校验：对 data/page_data.json 做结构与合理性断言。

用法:
    python tools/validate.py            # 失败返回 1，数据过旧仅告警
    python tools/validate.py --strict   # 数据过旧也视为失败（适合 CI）
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

from paths import PAGE_DATA_PATH

MAX_AGE_DAYS = 7
MAX_MEMBERS = 5000


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    strict = "--strict" in sys.argv

    if not PAGE_DATA_PATH.exists():
        fail(f"未找到 {PAGE_DATA_PATH}，请先运行 tools/build_page_data.py")

    with open(PAGE_DATA_PATH, encoding="utf-8") as handle:
        data = json.load(handle)

    # ---- 统计口径 ----
    stats = data.get("stats") or {}
    total = stats.get("totalMembers")
    active = stats.get("activeMembers")

    if not isinstance(total, int) or total <= 0:
        fail(f"totalMembers 异常: {total!r}")
    if total > MAX_MEMBERS:
        fail(f"totalMembers 超出合理范围: {total}")
    if not isinstance(active, int) or active < 0:
        fail(f"activeMembers 异常: {active!r}")
    if active > total:
        fail(f"activeMembers({active}) > totalMembers({total})")

    completeness = stats.get("dataCompleteness") or {}
    percentage = completeness.get("percentage")
    if not isinstance(percentage, (int, float)) or not 0 <= percentage <= 100:
        fail(f"dataCompleteness.percentage 异常: {percentage!r}")

    window = stats.get("activeWindow") or {}
    if not window.get("days"):
        fail("缺少 activeWindow.days，无法解释活跃口径")

    # ---- 图表数据 ----
    charts = data.get("charts") or {}
    for key in (
        "classDistribution",
        "factionDistribution",
        "raceDistribution",
        "realmDistribution",
        "genderDistribution",
    ):
        series = charts.get(key)
        if not isinstance(series, list) or not series:
            fail(f"charts.{key} 为空")
        for item in series:
            if not isinstance(item.get("value"), int) or item["value"] < 0:
                fail(f"charts.{key} 存在非法 value: {item!r}")

    # ---- 排行榜 ----
    rankings = data.get("rankings") or {}
    for key in ("achievementRanking", "itemLevelRanking", "mythicScoreRanking"):
        rows = rankings.get(key)
        if not isinstance(rows, list) or not rows:
            fail(f"rankings.{key} 为空")
        pairs = [(row.get("name"), row.get("realm")) for row in rows]
        if len(pairs) != len(set(pairs)):
            fail(f"rankings.{key} 存在重复角色 (name, realm)")
        ranks = [row.get("rank") for row in rows]
        if ranks != list(range(1, len(rows) + 1)):
            fail(f"rankings.{key} 排名不连续: {ranks}")

    # ---- 元信息 ----
    meta = data.get("meta") or {}
    source_rows = meta.get("sourceRows")
    unique = meta.get("uniqueCharacters")
    if not isinstance(source_rows, int) or not isinstance(unique, int):
        fail("meta.sourceRows / meta.uniqueCharacters 缺失")
    if unique != total:
        fail(f"meta.uniqueCharacters({unique}) 与 totalMembers({total}) 不一致")
    if source_rows < unique:
        fail("meta.sourceRows 小于 uniqueCharacters")
    if meta.get("duplicatesRemoved") != source_rows - unique:
        fail("meta.duplicatesRemoved 与记录数不匹配")

    # ---- 新鲜度 ----
    # 优先用 dataAsOf（数据本身截至的时间）；缺失时退回 lastUpdated（生成时间）
    last_updated = data.get("lastUpdated")
    data_as_of = data.get("dataAsOf")
    freshness_text = data_as_of or last_updated

    if data_as_of:
        try:
            generated_at = datetime.strptime(data_as_of, "%Y-%m-%d")
        except (TypeError, ValueError):
            fail(f"dataAsOf 格式异常: {data_as_of!r}")
    else:
        try:
            generated_at = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
        except (TypeError, ValueError):
            fail(f"lastUpdated 格式异常: {last_updated!r}")

    age = datetime.now() - generated_at
    if age > timedelta(days=MAX_AGE_DAYS):
        message = f"数据截至 {freshness_text}，已过期 {age.days} 天"
        if strict:
            fail(message)
        print(f"WARN: {message}", file=sys.stderr)

    print(
        "OK  total={total} active={active} window={days}d "
        "completeness={percentage}% source={source} unique={unique}".format(
            total=total,
            active=active,
            days=window.get("days"),
            percentage=percentage,
            source=source_rows,
            unique=unique,
        )
    )


if __name__ == "__main__":
    main()
