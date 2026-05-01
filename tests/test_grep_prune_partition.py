#!/usr/bin/env python3
"""Regression tests for grep-prune and shard partitioning utilities."""

import os
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from grep_prune import LANGUAGE_PATTERNS, detect_language, grep_card, search_card  # noqa: E402
from partition_shards import partition  # noqa: E402


class TestGrepPrune(unittest.TestCase):

    def test_language_patterns_cover_supported_audit_languages(self):
        self.assertEqual(
            LANGUAGE_PATTERNS,
            {
                "sol": "*.sol",
                "rs": "*.rs",
                "go": "*.go",
                "move": "*.move",
                "cairo": "*.cairo",
                "vy": "*.vy",
            },
        )

    def test_detect_language_includes_cairo_and_vyper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src").mkdir()
            (root / "src" / "vault.cairo").write_text("fn withdraw() {}\n", encoding="utf-8")
            (root / "src" / "pool.vy").write_text("@external\ndef swap(): pass\n", encoding="utf-8")

            detected = detect_language(str(root))

        self.assertEqual(set(detected), {"*.cairo", "*.vy"})

    def test_grep_card_scans_cairo_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "contract.cairo"
            target.write_text("fn update_price() {}\n", encoding="utf-8")

            hits = grep_card({"grep": "update_price"}, str(root), ["*.cairo"])

        self.assertEqual(hits, [f"{target}:1"])

    def test_search_card_reports_invalid_regex_without_hits(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "contract.sol").write_text("contract Vault {}\n", encoding="utf-8")

            result = search_card({"grep": "balanceOf(address(this"}, str(root), ["*.sol"])

        self.assertEqual(result["hits"], [])
        self.assertIsNotNone(result["error"])


class TestPartitionShards(unittest.TestCase):

    def test_critical_only_cards_create_actionable_shard(self):
        shards, critical = partition(
            [
                {"id": "critical-1", "cat": ["oracle"], "neverPrune": True},
                {"id": "critical-2", "cat": ["defi"], "neverPrune": True},
            ]
        )

        self.assertEqual([c["id"] for c in critical], ["critical-1", "critical-2"])
        self.assertEqual(len(shards), 1)
        self.assertEqual(shards[0]["id"], "shard-1-critical")
        self.assertTrue(shards[0]["criticalOnly"])
        self.assertEqual(shards[0]["cardIds"], ["critical-1", "critical-2"])
        self.assertEqual(shards[0]["criticalCardIds"], ["critical-1", "critical-2"])

    def test_regular_shards_reference_critical_cards(self):
        hits = [
            {"id": "regular-1", "cat": ["oracle"]},
            {"id": "regular-2", "cat": ["oracle"]},
            {"id": "critical-1", "cat": ["oracle"], "neverPrune": True},
        ]

        shards, critical = partition(hits, min_group_size=1)

        self.assertEqual([c["id"] for c in critical], ["critical-1"])
        self.assertEqual(shards[0]["cardIds"], ["regular-1", "regular-2"])
        self.assertEqual(shards[0]["criticalCardIds"], ["critical-1"])
        self.assertEqual(shards[0]["effectiveCardCount"], 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
