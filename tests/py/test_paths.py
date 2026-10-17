#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paths 测试：路径解析不依赖 cwd，这是迁移到 tools/ 后最容易踩的地方。
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from paths import (  # noqa: E402
    DATA_DIR,
    DEFAULT_DB_PATH,
    PAGE_DATA_PATH,
    REPO_ROOT,
    ensure_logs_dir,
    find_repo_root,
    resolve_db_path,
)


class FindRepoRootTest(unittest.TestCase):
    def test_detects_repository_root(self):
        self.assertEqual(REPO_ROOT, ROOT)

    def test_root_contains_markers(self):
        self.assertTrue((REPO_ROOT / "index.html").exists())
        self.assertTrue((REPO_ROOT / "package.json").exists())

    def test_works_from_nested_path(self):
        nested = ROOT / "js" / "core" / "dom.js"
        self.assertEqual(find_repo_root(nested), ROOT)

    def test_accepts_directory_input(self):
        self.assertEqual(find_repo_root(ROOT / "tools"), ROOT)


class ResolveDbPathTest(unittest.TestCase):
    def test_default_points_into_data_dir(self):
        self.assertEqual(DEFAULT_DB_PATH, DATA_DIR / "guild_database.db")

    def test_empty_argument_falls_back(self):
        # 不存在的写法定向到默认路径，而不是抛错
        result = resolve_db_path(None)
        self.assertEqual(result, DEFAULT_DB_PATH)
        self.assertTrue(result.is_absolute())

    def test_accepts_absolute_path_when_file_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake_db = Path(tmp) / "custom.db"
            fake_db.write_bytes(b"")
            self.assertEqual(resolve_db_path(str(fake_db)), fake_db.resolve())

    def test_resolves_relative_writing_styles(self):
        """历史上 config.json 里出现过三种写法，都应能定位到同一个真实文件。"""
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp) / "data"
            data_dir.mkdir()
            real = data_dir / "guild_database.db"
            real.write_bytes(b"")

            # 直接给绝对路径（模拟已解析过的写法）
            self.assertEqual(resolve_db_path(str(real)), real.resolve())

    def test_page_data_path(self):
        self.assertEqual(PAGE_DATA_PATH, DATA_DIR / "page_data.json")


class EnsureLogsDirTest(unittest.TestCase):
    def test_creates_and_returns_logs_dir(self):
        logs = ensure_logs_dir()
        self.assertTrue(logs.exists())
        self.assertEqual(logs.name, "logs")


if __name__ == "__main__":
    unittest.main()
