#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公会成员抓取（Raider.IO 公开 API）

为什么不用国服英雄榜：
    wow.blizzard.cn 的英雄榜（角色页 /character/#/… 与公会页 /guild/#/…）现在都要战网登录，
    实测无登录态时页面只发出 OAuth authorize 请求、不加载任何成员数据；
    侧信道接口 webapi.blizzard.cn/wow-armory-server/api/do 也需要 xcxtoken（账号令牌，约 7 天过期）。
    因此本项目历史上只能用登录后的浏览器手工导出 data/guildmember.csv。

Raider.IO 是唯一实测可用的公开来源：无需鉴权，覆盖国服（region=cn），
能给出「谁在会里 + 会阶 + 职业/专精/种族/性别/阵营 + 成就点」，
再加 --enrich 可逐角色补装备等级与本赛季大秘境分数。

拿不到的字段（仍只有英雄榜有，需登录）：
    角色等级、最后在线天数、坐骑数量。

用法：
    python tools/fetch_guild_roster.py                       # 抓成员名单，写 data/guildmember.rio.json
    python tools/fetch_guild_roster.py --compare             # 顺带和旧 CSV 比对覆盖率
    python tools/fetch_guild_roster.py --enrich --limit 50   # 逐角色补 ilvl / 大秘境分数（先小批量试）
    python tools/fetch_guild_roster.py --guild 一起 --realm arthas --region cn
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional

import requests

from paths import REPO_ROOT

BEIJING = timezone(timedelta(hours=8))
CACHE_DIR = REPO_ROOT / ".cache" / "guild-roster"
DEFAULT_OUT = REPO_ROOT / "data" / "guildmember.rio.json"
LEGACY_CSV = REPO_ROOT / "data" / "guildmember.csv"

API_PROFILE = "https://raider.io/api/v1/guilds/profile"
API_CHARACTER = "https://raider.io/api/v1/characters/profile"
USER_AGENT = "yiqi-guild-site/1.0 (+https://github.com/xinming-chenniang/yiqi)"

# 英文职业名 → 项目内职业 slug：表在 wow_terms.py，天梯与成员统计共用
from wow_terms import CLASS_EN_TO_SLUG as CLASS_SLUGS  # noqa: E402

LOG = logging.getLogger("guild-roster")


def today_beijing() -> str:
    return datetime.now(BEIJING).strftime("%Y/%m/%d")


def build_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})
    return session


def get_json(session: requests.Session, url: str, params: Dict[str, str], timeout: int = 40) -> dict:
    """GET + 重试；429/5xx 退避一次再试。"""
    last = "未知错误"
    for attempt in range(3):
        try:
            response = session.get(url, params=params, timeout=timeout)
        except requests.RequestException as exc:
            last = f"{type(exc).__name__}: {exc}"
            time.sleep(2 * (attempt + 1))
            continue
        if response.status_code == 200:
            return response.json()
        last = f"HTTP {response.status_code}"
        if response.status_code == 404:
            break
        time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"{url} → {last}")


def normalize_member(member: dict) -> dict:
    character = member.get("character") or {}
    class_en = character.get("class") or ""
    # profileUrl 形如 https://raider.io/characters/cn/arthas/Acg，从中取服务器 slug 最稳
    realm_slug = ""
    profile_url = character.get("profile_url") or ""
    parts = [part for part in profile_url.split("/") if part]
    if "characters" in parts:
        index = parts.index("characters")
        if len(parts) > index + 2:
            realm_slug = parts[index + 2]
    return {
        "name": character.get("name"),
        "realm": character.get("realm"),
        "realmSlug": realm_slug,
        "classEn": class_en,
        "classSlug": CLASS_SLUGS.get(class_en, ""),
        "specEn": character.get("active_spec_name"),
        "role": character.get("active_spec_role"),
        "raceEn": character.get("race"),
        "gender": character.get("gender"),
        "faction": character.get("faction"),
        "achievementPoints": character.get("achievement_points", 0),
        "rank": member.get("rank"),
        "rioLastCrawled": (character.get("last_crawled_at") or "")[:10],
        "profileUrl": profile_url,
    }


def fetch_guild(session: requests.Session, region: str, realm: str, guild: str) -> dict:
    payload = get_json(
        session,
        API_PROFILE,
        {"region": region, "realm": realm, "name": guild, "fields": "members"},
    )
    members = [normalize_member(item) for item in payload.get("members") or []]
    members.sort(key=lambda m: ((m["rank"] if m["rank"] is not None else 99), m["name"] or ""))
    return {
        "source": "raider.io",
        "fetchedAt": today_beijing(),
        "guild": {
            "name": payload.get("name") or guild,
            "displayName": payload.get("displayName"),
            "region": payload.get("region") or region,
            "realm": (payload.get("realm") or "").strip() or realm,
            "faction": payload.get("faction"),
            "profileUrl": payload.get("profile_url"),
        },
        "memberCount": len(members),
        "members": members,
    }


def enrich(session: requests.Session, roster: dict, limit: int, delay: float) -> int:
    """逐角色补装备等级与本赛季大秘境分数。limit=0 表示全部。"""
    done = 0
    for member in roster["members"]:
        if limit and done >= limit:
            break
        try:
            payload = get_json(
                session,
                API_CHARACTER,
                {
                    "region": roster["guild"]["region"],
                    "realm": member["realmSlug"] or (member["realm"] or "").lower().replace(" ", "-"),
                    "name": member["name"],
                    "fields": "gear,mythic_plus_scores_by_season:current",
                },
            )
        except RuntimeError as exc:
            LOG.warning("%s-%s: %s", member["name"], member["realm"], exc)
            continue
        gear = payload.get("gear") or {}
        seasons = payload.get("mythic_plus_scores_by_season") or []
        member["itemLevel"] = gear.get("item_level_equipped")
        member["gearUpdatedAt"] = (gear.get("updated_at") or "")[:10]
        member["mplusSeason"] = seasons[0].get("season") if seasons else None
        member["mplusScore"] = ((seasons[0].get("scores") or {}).get("all") if seasons else None)
        done += 1
        LOG.info("补全 %d/%d: %s %s", done, len(roster["members"]), member["name"], member["realm"])
        time.sleep(delay)
    roster["enriched"] = done
    return done


def compare_with_csv(roster: dict) -> None:
    """和旧的英雄榜导出 CSV 比覆盖率——判断能不能直接替换。"""
    if not LEGACY_CSV.exists():
        LOG.warning("没有 %s，跳过比对", LEGACY_CSV)
        return
    with LEGACY_CSV.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    legacy_names = {row.get("Name", "").strip() for row in rows if row.get("Name")}
    rio_names = {member["name"] for member in roster["members"] if member["name"]}
    only_legacy = sorted(legacy_names - rio_names)
    only_rio = sorted(rio_names - legacy_names)
    LOG.info("旧 CSV 角色数: %d（唯一 %d）", len(rows), len(legacy_names))
    LOG.info("RIO 成员数  : %d（唯一 %d）", roster["memberCount"], len(rio_names))
    LOG.info("名字重合    : %d", len(legacy_names & rio_names))
    LOG.info("只在旧 CSV  : %d（可能是已离会、或 RIO 没爬到）", len(only_legacy))
    LOG.info("只在 RIO    : %d（可能是不在旧导出里的新人）", len(only_rio))
    if only_rio:
        LOG.info("  例如: %s", "、".join(only_rio[:8]))
    if only_legacy:
        LOG.info("  例如: %s", "、".join(only_legacy[:8]))


def summarize(roster: dict) -> None:
    members = roster["members"]
    ranks: Dict[int, int] = {}
    classes: Dict[str, int] = {}
    for member in members:
        ranks[member["rank"]] = ranks.get(member["rank"], 0) + 1
        classes[member["classEn"]] = classes.get(member["classEn"], 0) + 1
    LOG.info("公会: %s (%s-%s)", roster["guild"]["displayName"] or roster["guild"]["name"],
             roster["guild"]["region"], roster["guild"]["realm"])
    LOG.info("成员: %d", roster["memberCount"])
    LOG.info("会阶分布: %s", dict(sorted(ranks.items())))
    LOG.info("职业分布: %s", dict(sorted(classes.items(), key=lambda kv: -kv[1])))


def main(argv: Optional[List[str]] = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if not isatty(stream) and hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="从 Raider.IO 抓取公会成员名单")
    parser.add_argument("--region", default="cn")
    parser.add_argument("--realm", default="arthas", help="服务器 slug，例如 arthas")
    parser.add_argument("--guild", default="一起", help="公会名（中文原样传）")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--cache-dir", type=Path, default=CACHE_DIR)
    parser.add_argument("--compare", action="store_true", help="与 data/guildmember.csv 比对覆盖率")
    parser.add_argument("--enrich", action="store_true", help="逐角色补装备等级与大秘境分数")
    parser.add_argument("--limit", type=int, default=0, help="--enrich 时最多补几个角色，0=全部")
    parser.add_argument("--delay", type=float, default=0.3, help="--enrich 的请求间隔秒数")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args.cache_dir.mkdir(parents=True, exist_ok=True)

    session = build_session()
    try:
        roster = fetch_guild(session, args.region, args.realm, args.guild)
    except RuntimeError as exc:
        LOG.error("抓取失败: %s", exc)
        return 2

    (args.cache_dir / "guild.json").write_text(
        json.dumps(roster, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    if args.enrich:
        enrich(session, roster, args.limit, args.delay)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(roster, ensure_ascii=False, indent=2), encoding="utf-8")
    LOG.info("已写入 %s", args.out)

    summarize(roster)
    if args.compare:
        compare_with_csv(roster)
    LOG.info("拿不到（英雄榜登录才有）: 角色等级、最后在线天数、坐骑数量")
    return 0


def isatty(stream) -> bool:
    try:
        return stream.isatty()
    except Exception:  # 探测式，取不到就按“非终端”处理
        return False


if __name__ == "__main__":
    sys.exit(main())
