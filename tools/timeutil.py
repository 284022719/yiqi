#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间戳工具

背景：魔兽 API 返回的 last_login_timestamp 是**毫秒**（13 位），
而早期脚本里把它当作**秒**比较，导致日期过滤条件恒为真。
这里做统一收敛。
"""

from datetime import datetime, timezone
from typing import Optional

# 10_000_000_000 秒 ≈ 2286 年；超过该量级一律认为是毫秒
_MILLISECOND_THRESHOLD = 10_000_000_000


def to_unix_seconds(value: Optional[int]) -> Optional[int]:
    """把秒或毫秒时间戳统一为秒；None 原样返回。"""
    if value is None:
        return None
    seconds = int(value)
    if seconds > _MILLISECOND_THRESHOLD:
        seconds //= 1000
    return seconds


def format_seconds(value: Optional[int], fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """秒级时间戳 -> 可读字符串（UTC）。"""
    seconds = to_unix_seconds(value)
    if seconds is None:
        return ""
    return datetime.fromtimestamp(seconds, tz=timezone.utc).strftime(fmt)


def format_millis(value: Optional[int], fmt: str = "%Y-%m-%d") -> str:
    """毫秒级时间戳 -> 可读字符串（UTC）。"""
    return format_seconds(value, fmt)
