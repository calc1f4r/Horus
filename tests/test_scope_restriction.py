#!/usr/bin/env python3
"""Tests for 00-scope.md restriction in grep_prune.py / partition_shards.py."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from horus_retrieval.scope import build_matcher, filter_file_scope, load_scope_block  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]

SCOPE_MD = """# Scope

Prose section that must be ignored.

## Machine-Readable Scope

```json
{
  "schema_version": 1,
  "in_scope": ["src/Pool.sol", "src/vault/"],
  "diff_set": ["src/OracleAdapter.sol"],
  "blast_set": [],
  "out_of_scope": [{"path": "lib/", "rule": "vendored"}]
}
```
"""


class TestScopeModule(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.scope_path = os.path.join(self.tmp.name, "00-scope.md")
        with open(self.scope_path, "w", encoding="utf-8") as f:
            f.write(SCOPE_MD)

    def tearDown(self):
        self.tmp.cleanup()

    def test_load_scope_block_extracts_json_after_heading(self):
        scope = load_scope_block(self.scope_path)
        self.assertEqual(scope["schema_version"], 1)
        self.assertIn("src/Pool.sol", scope["in_scope"])

    def test_load_scope_block_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_scope_block(os.path.join(self.tmp.name, "nope.md"))

    def test_load_scope_block_invalid_json_raises(self):
        bad = os.path.join(self.tmp.name, "bad-scope.md")
        with open(bad, "w", encoding="utf-8") as f:
            f.write("## Machine-Readable Scope\n\n```json\n{not json\n```\n")
        with self.assertRaises(ValueError):
            load_scope_block(bad)

    def test_matcher_file_dir_diff_rules(self):
        matches = build_matcher(load_scope_block(self.scope_path))
        self.assertTrue(matches("src/Pool.sol"))
        self.assertTrue(matches("src/vault/Vault.sol"))
        self.assertTrue(matches("src/vault/deep/Escrow.sol"))
        self.assertTrue(matches("src/OracleAdapter.sol"))  # via diff_set
        self.assertFalse(matches("lib/openzeppelin/token/ERC20.sol"))
        self.assertFalse(matches("src/Other.sol"))

    def test_matcher_globs(self):
        matches = build_matcher({"in_scope": ["src/**/*.sol"]})
        self.assertTrue(matches("src/a/b/C.sol"))
        self.assertFalse(matches("test/a/b/C.sol"))

    def test_matcher_empty_scope_fails_open(self):
        matches = build_matcher({"in_scope": [], "diff_set": [], "blast_set": []})
        self.assertTrue(matches("anything/anywhere.sol"))

    def test_filter_file_scope_absolute_and_relative(self):
        matches = build_matcher(load_scope_block(self.scope_path))
        base = "/tmp/target-repo"
        self.assertTrue(filter_file_scope(f"{base}/src/Pool.sol", base, matches))
        self.assertTrue(filter_file_scope("src/Pool.sol", base, matches))
        self.assertFalse(filter_file_scope(f"{base}/lib/x.sol", base, matches))


class TestGrepPruneScopeCLI(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.target = os.path.join(self.tmp.name, "target")
        os.makedirs(os.path.join(self.target, "src"))
        os.makedirs(os.path.join(self.target, "lib"))
        with open(os.path.join(self.target, "src", "Pool.sol"), "w", encoding="utf-8") as f:
            f.write("contract Pool { function liquidate() external {} }\n")
        with open(os.path.join(self.target, "lib", "Dep.sol"), "w", encoding="utf-8") as f:
            f.write("contract Dep { function liquidate() external {} }\n")

        self.cards_path = os.path.join(self.tmp.name, "cards.json")
        cards = {"cards": [
            {"id": "liq-001", "title": "liquidation", "severity": "HIGH", "ref": "x.md",
             "lines": [], "neverPrune": False,
             "grep": "function\\s+liquidate"},
            {"id": "np-001", "title": "never prune", "severity": "LOW", "ref": "y.md",
             "lines": [], "neverPrune": True,
             "grep": "nomatchpatternxyz"},
        ]}
        with open(self.cards_path, "w", encoding="utf-8") as f:
            json.dump(cards, f)

        self.scope_path = os.path.join(self.tmp.name, "00-scope.md")
        with open(self.scope_path, "w", encoding="utf-8") as f:
            f.write(SCOPE_MD)

        self.out_path = os.path.join(self.tmp.name, "hits.json")

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self, *extra):
        cmd = [
            sys.executable, str(REPO_ROOT / "scripts" / "grep_prune.py"),
            self.target, self.cards_path,
            "--language", "sol",
            "--output", self.out_path,
            *extra,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        with open(self.out_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_without_scope_both_files_hit(self):
        data = self._run()
        hits = {h["id"]: h["grepHits"] for h in data["hits"]}
        self.assertEqual(len(hits["liq-001"]), 2)

    def test_with_scope_only_in_scope_file_hits(self):
        data = self._run("--scope-file", self.scope_path)
        self.assertEqual(data["scopeFile"], self.scope_path)
        hits = {h["id"]: h["grepHits"] for h in data["hits"]}
        self.assertEqual(len(hits["liq-001"]), 1)
        self.assertIn("src/Pool.sol", hits["liq-001"][0])
        self.assertIn("np-001", hits)  # neverPrune survives

    def test_all_out_of_scope_card_pruned(self):
        # Scope out everything except src/, then remove the src hit
        with open(os.path.join(self.target, "src", "Pool.sol"), "w", encoding="utf-8") as f:
            f.write("contract Pool {}\n")  # pattern no longer matches in scope
        data = self._run("--scope-file", self.scope_path)
        ids = {h["id"] for h in data["hits"]}
        self.assertNotIn("liq-001", ids)
        self.assertIn("np-001", ids)


class TestPartitionShardsScopeCLI(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.hits_path = os.path.join(self.tmp.name, "hits.json")
        hits = {
            "targetPath": "/tmp/target-repo",
            "hits": [
                {"id": "in-001", "cat": "oracle", "grepHits": ["/tmp/target-repo/src/Pool.sol:10"],
                 "neverPrune": False},
                {"id": "out-001", "cat": "oracle", "grepHits": ["/tmp/target-repo/lib/Dep.sol:3"],
                 "neverPrune": False},
                {"id": "np-001", "cat": "access", "grepHits": ["/tmp/target-repo/lib/Dep.sol:4"],
                 "neverPrune": True},
                {"id": "err-001", "cat": "bridge", "grepHits": [], "searchError": "boom",
                 "neverPrune": False},
            ],
        }
        with open(self.hits_path, "w", encoding="utf-8") as f:
            json.dump(hits, f)

        self.scope_path = os.path.join(self.tmp.name, "00-scope.md")
        with open(self.scope_path, "w", encoding="utf-8") as f:
            f.write(SCOPE_MD)

        self.out_path = os.path.join(self.tmp.name, "shards.json")

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self, *extra):
        cmd = [
            sys.executable, str(REPO_ROOT / "scripts" / "partition_shards.py"),
            self.hits_path,
            "--output", self.out_path,
            *extra,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        with open(self.out_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_without_scope_all_cards_partitioned(self):
        data = self._run()
        self.assertEqual(data["totalSurvivingCards"], 4)

    def test_with_scope_out_of_scope_card_dropped(self):
        data = self._run("--scope-file", self.scope_path)
        self.assertEqual(data["scopeDroppedCards"], 1)
        self.assertEqual(data["totalSurvivingCards"], 3)
        critical_ids = {c["id"] for c in data["criticalSet"]}
        all_ids = set()
        for shard in data["shards"]:
            all_ids.update(shard.get("cardIds", []))
        self.assertIn("in-001", all_ids)
        self.assertNotIn("out-001", all_ids)
        # neverPrune survives even out of scope
        self.assertIn("np-001", critical_ids)
        # searchError card has no hits to filter — kept for manual review
        self.assertIn("err-001", all_ids)


if __name__ == "__main__":
    unittest.main()
