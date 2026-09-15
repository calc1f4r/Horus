#!/usr/bin/env python3
"""Tests for scripts/extract_reasoning_seeds.py — DB hunt cards → reasoning seeds."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "extract_reasoning_seeds.py"


def make_hits(cards):
    return {
        "totalCards": len(cards),
        "survivingCards": len(cards),
        "targetPath": "/tmp/target",
        "hits": cards,
    }


class TestExtractReasoningSeeds(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.hits_path = os.path.join(self.tmp.name, "hunt-card-hits.json")
        self.out_path = os.path.join(self.tmp.name, "reasoning-seeds.md")

    def tearDown(self):
        self.tmp.cleanup()

    def _write_hits(self, cards):
        with open(self.hits_path, "w", encoding="utf-8") as f:
            json.dump(make_hits(cards), f)

    def _run(self, *extra):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), self.hits_path, "--output", self.out_path, *extra],
            capture_output=True, text=True,
        )
        return result

    def _read_out(self):
        with open(self.out_path, "r", encoding="utf-8") as f:
            return f.read()

    def test_script_missing(self):
        """Script must exist — this is the fix under test."""
        self.assertTrue(SCRIPT.is_file(), f"{SCRIPT} not found")

    def test_extraction_layers_ids_and_sources(self):
        self._write_hits([
            {"id": "oracle-staleness-001", "ref": "DB/oracle/x.md", "cat": ["oracle"],
             "detect": "latestRoundData() result used without checking updatedAt staleness",
             "check": "Verify heartbeat elapsed since last update exceeds threshold",
             "impact": "stale price drives liquidations"},
            {"id": "reentrancy-001", "ref": "DB/general/reentrancy/y.md", "cat": ["reentrancy"],
             "detect": "external call before state update in withdraw",
             "check": "Confirm state mutated prior to any external call",
             "impact": "double withdrawal"},
        ])
        result = self._run()
        self.assertEqual(result.returncode, 0, result.stderr)
        out = self._read_out()
        # Layered catalog structure
        self.assertIn("Input Seeds", out)
        self.assertIn("Ordering Seeds", out)
        # Stable IDs
        self.assertRegex(out, r"SEED-I-\d{3}")
        self.assertRegex(out, r"SEED-O-\d{3}")
        # Source citation back to hunt cards
        self.assertIn("oracle-staleness-001", out)
        self.assertIn("reentrancy-001", out)
        # Generalized assumption text present
        self.assertIn("External data consumed without temporal validation", out)

    def test_dedup_identical_detect_fields(self):
        self._write_hits([
            {"id": "a-001", "ref": "a.md", "cat": ["oracle"],
             "detect": "spot price from slot0 used for valuation",
             "check": "check pool depth", "impact": "manipulation"},
            {"id": "b-002", "ref": "b.md", "cat": ["oracle"],
             "detect": "spot price from slot0 used for valuation",
             "check": "check pool depth", "impact": "manipulation"},
        ])
        result = self._run()
        self.assertEqual(result.returncode, 0, result.stderr)
        out = self._read_out()
        self.assertEqual(out.count("spot price from slot0"), 1)
        # Both source cards still cited on the merged seed
        self.assertIn("a-001", out)
        self.assertIn("b-002", out)

    def test_empty_hits_explicit_warning(self):
        self._write_hits([])
        result = self._run()
        self.assertEqual(result.returncode, 0, result.stderr)
        out = self._read_out()
        self.assertIn("ZERO", out)  # explicit zero-seed marker for the Phase A gate

    def test_card_without_detect_is_skipped_not_crashing(self):
        self._write_hits([
            {"id": "np-001", "ref": "n.md", "cat": ["access"], "grepHits": ["x:1"]},
        ])
        result = self._run()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_all_huntcards_direct_input(self):
        """Extractor must accept all-huntcards.json directly (standalone mode
        where grep_prune has not run)."""
        all_cards = os.path.join(self.tmp.name, "all-huntcards.json")
        with open(all_cards, "w", encoding="utf-8") as f:
            json.dump({"cards": [
                {"id": "flashloan-001", "ref": "f.md", "cat": ["flash-loan"],
                 "detect": "function behavior scales with caller balance via flash-loan capital",
                 "check": "test with flash-loan-sized input", "impact": "drain"},
            ]}, f)
        result = subprocess.run(
            [sys.executable, str(SCRIPT), all_cards, "--output", self.out_path],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Economic Seeds", self._read_out())


if __name__ == "__main__":
    unittest.main()
