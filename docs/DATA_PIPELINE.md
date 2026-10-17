# 数据管道说明

## 1. 总览

```
Blizzard API ──crawl──▶ SQLite ──build──▶ data/page_data.json ──fetch──▶ 首页
```

- 抓取脚本：`tools/mounts_crawler.py`（坐骑等角色数据）
- 生成脚本：`tools/build_page_data.py`
- 校验脚本：`tools/validate.py`
- 输出文件：`data/page_data.json`（**不要手改**）

运行环境：Python 3.9+。第三方依赖见 `requirements.txt`。

## 2. 常用命令

```bash
# 生成页面数据（默认 cwd 任意，脚本内部按仓库根解析路径）
python tools/build_page_data.py

# 调整活跃窗口（默认 30 天）
ACTIVE_DAYS=14 python tools/build_page_data.py

# 校验产物：结构/口径断言，数据过期仅告警
python tools/validate.py

# CI 模式：数据过期也失败
python tools/validate.py --strict

# 爬取坐骑数据（需要令牌与网络）
python tools/mounts_crawler.py

# 数据库巡检
python tools/database_query_tool.py
```

## 3. 数据库

默认位置：`data/guild_database.db`（**不入版本库**）。

主表 `guild_characters` 共 24 列：

```
id, name, rank, level, class, race, sex,
last_online_days, mythic_score, faction, realm, guild, spec,
achievement_points, average_item_level, equipped_item_level,
last_login_timestamp, data_source, created_at, updated_at, crawl_timestamp,
realm_slug, mounts_now, mounts_total
```

关键点：

- `last_login_timestamp` 是**毫秒**（13 位）。直接与秒级阈值比较会恒为真，历史 bug 见 §6。
- 一个角色可能有多行（多次抓取），需按 `(name, realm)` 去重。
- `264` 行的 `last_login_timestamp` 为 `NULL`，这些记录不会进入活跃统计。

## 4. 统计口径

| 指标 | 定义 | 计算位置 |
|---|---|---|
| `totalMembers` | 按 `(name, realm)` 去重后的角色数 | `calculate_statistics` |
| `activeMembers` | 去重后，登录时间落在「数据集最新登录时间往前 N 天」内的角色数 | 同上 |
| `dataCompleteness` | `achievement_points > 0` 且 `average_item_level > 0` 的占比 | 同上 |
| `activeWindow.basis` | 固定为 `dataset_latest`，表示以数据集中最新时间为基准 | 同上 |

**为什么不用系统时间当基准**：数据若长期未更新，按墙上时钟计算会得到「0 人活跃」，把「数据陈旧」误报成「公会没人」。以数据集最新时间为基准，指标始终描述「这批数据内部的活跃度」，同时通过 `dataAsOf` 字段暴露数据真实截至时间。

## 5. 输出结构

`data/page_data.json`：

```jsonc
{
  "lastUpdated": "2026-10-18 02:05:16",  // 生成时间
  "dataAsOf": "2025-08-04",              // 数据截至（最新登录日）
  "stats": {
    "totalMembers": 965,
    "activeMembers": 356,
    "activeWindow": { "days": 30, "since": "2025-07-05", "latest": "2025-08-04", "basis": "dataset_latest" },
    "dataCompleteness": { "total": 965, "complete": 702, "incomplete": 263, "percentage": 72.7 }
  },
  "charts": {
    "classDistribution":  [{ "name": "圣骑士", "value": 120 }],
    "factionDistribution":[{ "name": "Horde", "value": 900 }],
    "raceDistribution":   [{ "name": "血精灵", "value": 300 }],
    "realmDistribution":  [{ "name": "白银之手", "value": 200 }],
    "genderDistribution": [{ "name": "男", "value": 600 }]
  },
  "rankings": {
    "achievementRanking": [{ "rank": 1, "name": "…", "realm": "…", "class": "…",
                            "spec": "…", "achievement_points": 0, "average_item_level": 0,
                            "mythic_score": 0, "mounts_now": 0 }],
    "itemLevelRanking":  [],
    "mythicScoreRanking":[]
  },
  "meta": {
    "sourceRows": 967, "uniqueCharacters": 965, "duplicatesRemoved": 2,
    "rowsWithoutLoginTime": 264, "generator": "tools/build_page_data.py"
  }
}
```

下游消费方：`js/modules/GuildStatsLoader.js`（概览）与 `js/components/Chart.js`（图表渲染）。

## 6. 时间戳陷阱（历史 bug 复盘）

旧实现同时存在两个错误，导致日期过滤完全失效：

1. 阈值硬编码为 `1706313600`，注释写「2025-02-27」，实际是 **2024-01-27**（差 397 天）。
2. 数据库存的是毫秒（如 `1754329119000`），与秒级阈值比较恒为真。

结果：`WHERE last_login_timestamp >= ?` 实际只等价于 `IS NOT NULL`。

现在统一由 `tools/timeutil.py` 处理：

```python
to_unix_seconds(1754329119000)  # -> 1754329119
```

## 7. 去重规则

按 `(name, realm)` 聚合，保留「登录时间更晚 → 更新时间更晚 → 原始顺序靠前」的一条。当前数据：

| 项 | 数量 |
|---|---|
| 原始行数 | 967 |
| 去重后 | 965 |
| 移除 | 2 |
| 无登录时间 | 264 |

> 同名但不同服务器的角色是合法的，不会被合并。

## 8. 校验

`tools/validate.py` 的断言：

- `totalMembers` 在 `(0, 5000]`
- `0 <= activeMembers <= totalMembers`
- `dataCompleteness.percentage` ∈ [0, 100]
- 5 组图表数据非空且 `value >= 0`
- 3 张排行榜非空、无重复 `(name, realm)`、`rank` 连续
- `meta.uniqueCharacters == totalMembers`，`duplicatesRemoved` 自洽
- `dataAsOf` 超过 7 天则告警（`--strict` 时失败）

## 9. 已知数据问题

| 问题 | 现状 | 影响 | 建议 |
|---|---|---|---|
| 数据停滞 | `dataAsOf = 2025-08-04`，距 2026-10 已 440 天 | 页面数字反映的是一年多前的状态 | 重跑爬虫；长期方案是排定时任务 |
| 坐骑数全部相同 | 277 个有坐骑数据的角色 `mounts_now` 均为 369 | 坐骑维度无区分度 | 排查令牌复用问题，见 `docs/archive/API_ISSUE_ANALYSIS.md` |
| 爬虫令牌未外置 | `tools/config.py` 与 `data/Database/config.json` 仍硬编码令牌 | 安全风险 | 见 §10 |
| 配置文件重复 | `data/config.json` 与 `data/Database/config.json` 两份 | 易改错 | 合并为一份 |

## 10. 待办

1. **令牌外置**：改为读取环境变量（如 `BLIZZARD_API_TOKEN`），移除 `config.py` 内置常量与文档中的明文令牌，随后轮换令牌。
2. **配置合一**：合并两份 `config.json`，迁移到 `tools/config.json`（已被 `.gitignore` 覆盖），仓库只保留 `config.example.json`。
3. **数据出库**：`data/guild_database.db`、`data/guildmember.csv` 仍在 git 跟踪中，需用 `git rm --cached` 停止跟踪（本地文件保留）。
4. **自动化**：定时执行 `build_page_data.py` + `validate.py --strict`，避免再次出现 400 天停滞。
