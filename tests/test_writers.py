#!/usr/bin/env python3
"""Unit tests for retrieval artifact writers."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from horus_retrieval.writers import (  # noqa: E402
    backup_existing_file,
    emit_artifact_summary,
    write_json,
    write_router_index,
)


class TestWriters(unittest.TestCase):

    def test_write_json_creates_parent_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nested" / "data.json"

            write_json(path, {"ok": True})

            with path.open(encoding="utf-8") as f:
                data = json.load(f)
        self.assertEqual(data, {"ok": True})

    def test_backup_existing_file_returns_false_when_source_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            copied = backup_existing_file(root / "missing.json", root / "backup.json")

        self.assertFalse(copied)

    def test_write_router_index_backs_up_existing_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_dir = Path(tmp) / "DB"
            db_dir.mkdir()
            (db_dir / "index.json").write_text('{"old": true}', encoding="utf-8")
            emitted = []

            write_router_index(db_dir, {"new": True}, emitted.append)

            with (db_dir / "index.json").open(encoding="utf-8") as f:
                new_data = json.load(f)
            with (db_dir / "index.old.json").open(encoding="utf-8") as f:
                old_data = json.load(f)

        self.assertEqual(new_data, {"new": True})
        self.assertEqual(old_data, {"old": True})
        self.assertTrue(any("Backed up old index" in line for line in emitted))

    def test_emit_artifact_summary_reports_manifest_and_huntcard_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_dir = root / "manifests"
            huntcards_dir = manifest_dir / "huntcards"
            write_json(
                manifest_dir / "oracle.json",
                {"meta": {"totalPatterns": 2, "fileCount": 1}, "files": []},
            )
            write_json(
                huntcards_dir / "oracle-huntcards.json",
                {"meta": {"totalCards": 1}, "cards": []},
            )
            write_json(
                huntcards_dir / "all-huntcards.json",
                {"meta": {"totalCards": 1}, "cards": []},
            )
            emitted = []

            emit_artifact_summary(
                manifests={"oracle": {"meta": {"totalPatterns": 2, "fileCount": 1}}},
                manifest_dir=manifest_dir,
                huntcards_dir=huntcards_dir,
                total_huntcards=1,
                emit=emitted.append,
            )

        self.assertIn("Total patterns extracted: 2", emitted)
        self.assertTrue(any("DB/manifests/oracle.json" in line for line in emitted))
        self.assertTrue(any("all-huntcards.json" in line for line in emitted))


if __name__ == "__main__":
    unittest.main(verbosity=2)
