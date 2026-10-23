#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
魔兽世界名词表：英文（Raider.IO / Wowhead 写法）↔ 项目内的中文名与 slug。

单一来源：天梯抓取（fetch_tier_lists.py）与公会成员抓取（fetch_guild_roster.py → build_page_data_rio.py）
都从这里取映射，避免同一张表维护两遍。

约定：
    CLASS_EN_TO_SLUG  英文职业名 → 项目职业 slug（与 js/data/wow-classes.js 的 slug 一致）
    CLASS_EN_TO_CN    英文职业名 → 中文名（与 wow-classes.js 的 name 一致）
    SPEC_BY_EN        "专精 职业"（Wowhead 写法）→ specs.js 的 id（'slug|专精中文'）
    RACE_EN_TO_CN     英文种族名 → 中文名（与 js/data/palettes.js 的 RACE_COLORS 键一致）
    REALM_SLUG_TO_CN  Raider.IO 服务器 slug → 中文服务器名

维护提示：
    - 新的专精/种族/服务器出现时，只在这里补一行；抓取脚本会校验 specs.js 里有没有对应 id。
    - REALM_SLUG_TO_CN 只收录能确证的映射（来源：旧英雄榜导出的 CN/EN 成对列，剔除了自相矛盾的条目）。
      查不到的服务器会回退成 Raider.IO 的英文显示名，图表配色用默认色——宁可显示英文，也不猜中文名。
"""

from __future__ import annotations

from typing import Dict, Optional

CLASS_EN_TO_SLUG: Dict[str, str] = {
    "Death Knight": "death-knight",
    "Demon Hunter": "demon-hunter",
    "Druid": "druid",
    "Evoker": "evoker",
    "Hunter": "hunter",
    "Mage": "mage",
    "Monk": "monk",
    "Paladin": "paladin",
    "Priest": "priest",
    "Rogue": "rogue",
    "Shaman": "shaman",
    "Warlock": "warlock",
    "Warrior": "warrior",
}

CLASS_EN_TO_CN: Dict[str, str] = {
    "Death Knight": "死亡骑士",
    "Demon Hunter": "恶魔猎手",
    "Druid": "德鲁伊",
    "Evoker": "唤魔师",
    "Hunter": "猎人",
    "Mage": "法师",
    "Monk": "武僧",
    "Paladin": "圣骑士",
    "Priest": "牧师",
    "Rogue": "潜行者",
    "Shaman": "萨满祭司",
    "Warlock": "术士",
    "Warrior": "战士",
}

# 英文专精名（Wowhead 的 "专精 职业" 写法）→ specs.js 的 id。
# 新增专精时：先在 specs.js 登记 id 与图标，再在这里补一行；fetch_tier_lists.py 会校验两边一致。
SPEC_BY_EN: Dict[str, str] = {
    "Arms Warrior": "warrior|武器",
    "Fury Warrior": "warrior|狂怒",
    "Protection Warrior": "warrior|防护",
    "Holy Paladin": "paladin|神圣",
    "Protection Paladin": "paladin|防护",
    "Retribution Paladin": "paladin|惩戒",
    "Beast Mastery Hunter": "hunter|野兽控制",
    "Marksmanship Hunter": "hunter|射击",
    "Survival Hunter": "hunter|生存",
    "Assassination Rogue": "rogue|奇袭",
    "Outlaw Rogue": "rogue|狂徒",
    "Subtlety Rogue": "rogue|敏锐",
    "Discipline Priest": "priest|戒律",
    "Holy Priest": "priest|神圣",
    "Shadow Priest": "priest|暗影",
    "Affliction Warlock": "warlock|痛苦",
    "Demonology Warlock": "warlock|恶魔学识",
    "Destruction Warlock": "warlock|毁灭",
    "Arcane Mage": "mage|奥术",
    "Fire Mage": "mage|火焰",
    "Frost Mage": "mage|冰霜",
    "Brewmaster Monk": "monk|酒仙",
    "Mistweaver Monk": "monk|织雾",
    "Windwalker Monk": "monk|踏风",
    "Balance Druid": "druid|平衡",
    "Feral Druid": "druid|野性",
    "Guardian Druid": "druid|守护",
    "Restoration Druid": "druid|恢复",
    "Elemental Shaman": "shaman|元素",
    "Enhancement Shaman": "shaman|增强",
    "Restoration Shaman": "shaman|恢复",
    "Blood Death Knight": "death-knight|鲜血",
    "Frost Death Knight": "death-knight|冰霜",
    "Unholy Death Knight": "death-knight|邪恶",
    "Havoc Demon Hunter": "demon-hunter|浩劫",
    "Vengeance Demon Hunter": "demon-hunter|复仇",
    "Devourer Demon Hunter": "demon-hunter|噬灭",
    "Devastation Evoker": "evoker|湮灭",
    "Preservation Evoker": "evoker|恩护",
    "Augmentation Evoker": "evoker|增辉",
}

RACE_EN_TO_CN: Dict[str, str] = {
    "Blood Elf": "血精灵",
    "Dark Iron Dwarf": "黑铁矮人",
    "Dracthyr": "龙希尔",
    "Draenei": "德莱尼",
    "Dwarf": "矮人",
    "Earthen": "土灵",
    "Gnome": "侏儒",
    "Goblin": "地精",
    "Haranir": "哈拉尼尔",
    "Highmountain Tauren": "至高岭牛头人",
    "Human": "人类",
    "Kul Tiran": "库尔提拉斯人",
    "Lightforged Draenei": "光铸德莱尼",
    "Mag'har Orc": "玛格汉兽人",
    "Mechagnome": "机械侏儒",
    "Night Elf": "暗夜精灵",
    "Nightborne": "夜之子",
    "Orc": "兽人",
    "Pandaren": "熊猫人",
    "Tauren": "牛头人",
    "Troll": "巨魔",
    "Undead": "亡灵",
    "Void Elf": "虚空精灵",
    "Vulpera": "狐人",
    "Worgen": "狼人",
    "Zandalari Troll": "赞达拉巨魔",
}

# 来源与核对：
#   1) data/guildmember.csv（旧英雄榜导出）里 CN/EN 成对的服务器列；
#   2) 人工核对的译名：lothar / alexstrasza / silverpine-forest / skywall / storm-eye /
#      sylvanas / voljin / zulaman；
#   3) 剩下 10 条取自 warcraft.wiki.gg 的「中文 (English)」对照，并用国服服务器名单做交叉核对
#      （arygos=亚雷戈斯、deathwhisper=亡语者、dreamwalker=踏梦者、gothik=戈提克、
#        holy-chanter=神圣之歌、lushwater-oasis=甜水绿洲、northrend=诺森德、
#        temple-of-elune=月神殿、zealot-blade=狂热之刃、algalon=奥尔加隆）。
#   其中 holy-chanter / dreamwalker 已标注「待游戏内核实」：两者的中文名在 wiki 的成对链接与
#   国服正式服名单里都能对上，但人工复核后仍存疑，等有人打开游戏服务器列表确认再摘掉标记。
# 旧导出里 arygos / lothar / lushwater-oasis / temple-of-elune 被错写成「阿尔萨斯」，已按上面修正。
# 以后遇到新服务器：查不到就留空，代码会回退成英文显示名，不猜。
REALM_SLUG_TO_CN: Dict[str, str] = {
    "alar": "凤凰之神",
    "alexstrasza": "阿莱克斯塔萨",
    "algalon": "奥尔加隆",
    "altar-of-storms": "暴风祭坛",
    "alterac-mountains": "奥特兰克",
    "anzu": "安苏",
    "archimonde": "阿克蒙德",
    "argus": "阿古斯",
    "arthas": "阿尔萨斯",
    "arygos": "亚雷戈斯",
    "barrens": "贫瘠之地",
    "barthilas": "巴瑟拉斯",
    "blanchard": "布兰卡德",
    "burning-blade": "燃烧之刃",
    "chillwind-point": "冰风岗",
    "dark-iron": "黑铁",
    "deathwhisper": "亡语者",
    "deathwing": "死亡之翼",
    "direwing": "恶魔之翼",
    "dreamwalker": "踏梦者",        # 待游戏内核实
    "echo-ridge": "回音山",
    "eldrethalas": "埃德萨拉",
    "fel-rock": "地狱之石",
    "frostmourne": "霜之哀伤",
    "frostwolf": "霜狼",
    "garithos": "加里索斯",
    "gnomeregan": "诺莫瑞根",
    "gothik": "戈提克",
    "grim-batol": "格瑞姆巴托",
    "hectae": "海克泰尔",
    "holy-chanter": "神圣之歌",      # 待游戏内核实
    "illidan": "伊利丹",
    "isillien": "伊森利恩",
    "kelthuzad": "克尔苏加德",
    "lethon": "莱索恩",
    "li-li": "丽丽（四川）",
    "lothar": "洛萨",
    "lushwater-oasis": "甜水绿洲",
    "malganis": "梅尔加尼",
    "malygos": "玛里苟斯",
    "northrend": "诺森德",
    "pandaren": "熊猫酒仙",
    "red-dragonflight": "红龙军团",
    "rhonin": "罗宁",
    "runetotem": "符文图腾",
    "scarlet-crusade": "血色十字军",
    "shadowmourne": "影之哀伤",
    "silver-hand": "白银之手",
    "silverpine-forest": "银松森林",
    "skettis": "斯克提斯",
    "skywall": "天空之墙",
    "smolderthorn": "烈焰荆棘",
    "storm-eye": "风暴之眼",
    "storm-peaks": "风暴峭壁",
    "suramar": "苏拉玛",
    "sylvanas": "希尔瓦娜斯",
    "temple-of-elune": "月神殿",
    "the-golden-plains": "金色平原",
    "the-great-sea": "无尽之海",
    "the-masters-glaive": "主宰之剑",
    "theramore": "塞拉摩",
    "valanar": "瓦拉纳",
    "valley-of-kings": "国王之谷",
    "varian": "瓦里安",
    "voljin": "沃金",
    "winterspring": "冬泉谷",
    "zealot-blade": "狂热之刃",
    "zulaman": "祖阿曼",
    "zuldrak": "祖达克",
}

# 阵营与性别：图表按英文键取色（js/data/palettes.js），显示名由前端映射，所以这里只给分类值
FACTION_LABELS = {"horde": "Horde", "alliance": "Alliance"}
GENDER_EN_TO_CN = {"male": "男", "female": "女"}


def class_slug(class_en: Optional[str]) -> str:
    return CLASS_EN_TO_SLUG.get((class_en or "").strip(), "")


def class_cn(class_en: Optional[str]) -> str:
    return CLASS_EN_TO_CN.get((class_en or "").strip(), (class_en or "").strip())


def race_cn(race_en: Optional[str]) -> str:
    value = (race_en or "").strip()
    return RACE_EN_TO_CN.get(value, value or "未知")


def realm_cn(realm_slug: Optional[str], display_name: Optional[str] = None) -> str:
    """优先按 slug 查中文名；查不到就回退 Raider.IO 的英文显示名。"""
    mapped = REALM_SLUG_TO_CN.get((realm_slug or "").strip())
    if mapped:
        return mapped
    return (display_name or realm_slug or "未知").strip()


def faction_label(faction: Optional[str]) -> str:
    value = (faction or "").strip().lower()
    if value in FACTION_LABELS:
        return FACTION_LABELS[value]
    return (faction or "未知").strip() or "未知"


def gender_cn(gender: Optional[str]) -> str:
    return GENDER_EN_TO_CN.get((gender or "").strip().lower(), "未知")


def spec_cn(class_en: Optional[str], spec_en: Optional[str]) -> str:
    """由「职业英文名 + 专精英文名」拼回 specs.js 的 id，再取其中的中文专精名。"""
    key = f"{(spec_en or '').strip()} {(class_en or '').strip()}".strip()
    spec_id = SPEC_BY_EN.get(key)
    if not spec_id:
        return (spec_en or "").strip()
    return spec_id.split("|", 1)[1]
