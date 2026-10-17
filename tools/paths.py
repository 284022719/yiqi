#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路径解析工具

约定：所有脚本都以「仓库根目录」为基准解析路径，不依赖调用时的 cwd。
这样无论从仓库根、tools/ 还是 data/Database/ 启动，结果都一致。
"""

from pathlib import Path
from typing import Optional


def find_repo_root(start: Optional[Path] = None) -> Path:
    """向上查找仓库根目录（同时包含 index.html 与 package.json 的目录）。"""
    current = (start or Path(__file__)).resolve()
    if current.is_file():
        current = current.parent

    for candidate in (current, *current.parents):
        if (candidate / "index.html").exists() and (candidate / "package.json").exists():
            return candidate

    # 兜底：假定本文件位于 <root>/tools/ 或 <root>/data/Database/
    return current.parent if current.name in {"tools", "Database"} else current


REPO_ROOT = find_repo_root()
DATA_DIR = REPO_ROOT / "data"
DEFAULT_DB_PATH = DATA_DIR / "guild_database.db"
PAGE_DATA_PATH = DATA_DIR / "page_data.json"
LOGS_DIR = REPO_ROOT / "logs"


def resolve_db_path(configured: Optional[str] = None) -> Path:
    """解析数据库路径。

    config.json 中历史上出现过三种写法：
      "guild_database.db" / "../guild_database.db" / "data/guild_database.db"
    这里统一按候选顺序探测，取第一个真实存在的文件，避免依赖 cwd。
    """
    candidates = []
    if configured:
        raw = Path(configured)
        candidates.extend([
            raw if raw.is_absolute() else Path.cwd() / raw,
            REPO_ROOT / raw,
            DATA_DIR / raw.name,
            REPO_ROOT / "data" / "Database" / raw.name,
        ])
    candidates.append(DEFAULT_DB_PATH)

    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()

    return DEFAULT_DB_PATH.resolve()


def ensure_logs_dir() -> Path:
    """确保 logs/ 存在（全新克隆时仓库里没有该目录）。"""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    return LOGS_DIR
