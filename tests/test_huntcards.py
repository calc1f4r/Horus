#!/usr/bin/env python3
"""Unit tests for hunt-card builders."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from horus_retrieval.huntcards import (  # noqa: E402
    build_all_huntcards,
    build_huntcard,
    build_huntcards_for_manifest,
    extract_identifiers_from_content,
    select_best_grep_keywords,
    truncate_to_sentence,
)


class TestHuntcards(unittest.TestCase):

    def test_truncate_to_sentence_preserves_identifiers_with_periods(self):
        text = "1. `vault.totalAssets()` can return a stale value. Later text is not needed."

        self.assertEqual(
            truncate_to_sentence(text),
            "`vault.totalAssets()` can return a stale value.",
        )

    def test_select_best_grep_keywords_filters_generic_terms(self):
        keywords = ["uint256", "balance", "settleFunding()", "update_mark_price", "swap"]

        selected = select_best_grep_keywords(keywords)

        self.assertEqual(set(selected), {"update_mark_price", "settleFunding"})
        self.assertNotIn("uint256", selected)
        self.assertNotIn("balance", selected)
        self.assertNotIn("swap", selected)

    def test_extract_identifiers_reads_db_relative_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db_root = root / "DB"
            entry = db_root / "oracle" / "sample.md"
            entry.parent.mkdir(parents=True)
            entry.write_text(
                "# Oracle Drift\n\n"
                "The code calls `latestRoundData` and then update_mark_price().\n"
                "It also uses vault.totalAssets() before validating block.timestamp.\n",
                encoding="utf-8",
            )

            identifiers = extract_identifiers_from_content(
                "DB/oracle/sample.md",
                1,
                5,
                db_root=db_root,
            )

        self.assertIn("update_mark_price", identifiers)
        self.assertIn("latestRoundData", identifiers)

    def test_build_huntcard_filters_structural_sections(self):
        pattern = {
            "id": "oracle:overview:1",
            "title": "Overview",
            "lineStart": 1,
            "lineEnd": 50,
            "lineCount": 49,
            "severity": ["HIGH"],
        }

        self.assertIsNone(build_huntcard(pattern, "DB/oracle/sample.md", "oracle"))

    def test_build_huntcard_preserves_key_fields_and_critical_flag(self):
        pattern = {
            "id": "oracle:stale-price:10",
            "title": "Stale Oracle Price Accepted",
            "lineStart": 10,
            "lineEnd": 40,
            "lineCount": 30,
            "severity": ["LOW", "CRITICAL"],
            "codeKeywords": ["uint256", "latestRoundData()", "block.timestamp"],
            "rootCause": "The protocol accepts stale oracle rounds before checking timestamps.",
            "reportEvidence": [{"firm": "Example", "severity": "HIGH"}],
            "graphHints": {"attackPhase": ["oracle-read"]},
        }

        card = build_huntcard(pattern, "DB/oracle/sample.md", "oracle")

        self.assertEqual(card["severity"], "CRITICAL")
        self.assertEqual(card["grep"], "latestRoundData|block.timestamp")
        self.assertEqual(card["cat"], ["oracle", "price-feed", "data-freshness"])
        self.assertTrue(card["neverPrune"])
        self.assertIn("reportEvidence", card)
        self.assertIn("graphHints", card)

    def test_build_huntcards_for_manifest_counts_skipped_patterns(self):
        manifest = {
            "files": [
                {
                    "file": "DB/oracle/sample.md",
                    "patterns": [
                        {
                            "id": "oracle:overview:1",
                            "title": "Overview",
                            "lineStart": 1,
                            "lineEnd": 50,
                            "lineCount": 49,
                            "severity": ["HIGH"],
                        },
                        {
                            "id": "oracle:stale-price:10",
                            "title": "Stale Oracle Price Accepted",
                            "lineStart": 10,
                            "lineEnd": 40,
                            "lineCount": 30,
                            "severity": ["HIGH"],
                            "codeKeywords": ["latestRoundData()"],
                            "rootCause": "The protocol accepts stale oracle rounds.",
                        },
                    ],
                }
            ]
        }

        result = build_huntcards_for_manifest("oracle", manifest)

        self.assertEqual(result["meta"]["totalCards"], 1)
        self.assertEqual(result["meta"]["skipped"], 1)

    def test_build_all_huntcards_writes_per_manifest_and_combined_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            huntcards_dir = Path(tmp) / "huntcards"
            emitted = []
            manifests = {
                "oracle": {
                    "files": [
                        {
                            "file": "DB/oracle/sample.md",
                            "patterns": [
                                {
                                    "id": "oracle:stale-price:10",
                                    "title": "Stale Oracle Price Accepted",
                                    "lineStart": 10,
                                    "lineEnd": 40,
                                    "lineCount": 30,
                                    "severity": ["HIGH"],
                                    "codeKeywords": ["latestRoundData()"],
                                    "rootCause": "The protocol accepts stale oracle rounds.",
                                }
                            ],
                        }
                    ]
                }
            }

            per_manifest, total = build_all_huntcards(
                manifests,
                huntcards_dir=huntcards_dir,
                emit=emitted.append,
            )

            with (huntcards_dir / "all-huntcards.json").open("r", encoding="utf-8") as f:
                combined = json.load(f)

        self.assertEqual(total, 1)
        self.assertEqual(per_manifest["oracle"]["totalCards"], 1)
        self.assertEqual(combined["meta"]["totalCards"], 1)
        self.assertTrue(any("oracle-huntcards.json" in line for line in emitted))


if __name__ == "__main__":
    unittest.main(verbosity=2)
