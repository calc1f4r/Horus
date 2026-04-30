#!/usr/bin/env python3
"""Unit tests for partition bundle builders."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from horus_retrieval.bundles import (  # noqa: E402
    build_partition_bundles,
    build_protocol_bundle,
    cards_by_manifest_from_huntcards,
)


class TestBundles(unittest.TestCase):

    def test_cards_by_manifest_maps_general_subfolders_to_sub_manifests(self):
        all_huntcards = {
            "cards": [
                {"id": "oracle-1", "ref": "DB/oracle/stale.md"},
                {"id": "access-1", "ref": "DB/general/access-control/owner.md"},
                {"id": "precision-1", "ref": "DB/general/precision/rounding.md"},
            ]
        }

        by_manifest = cards_by_manifest_from_huntcards(all_huntcards)

        self.assertEqual([c["id"] for c in by_manifest["oracle"]], ["oracle-1"])
        self.assertEqual([c["id"] for c in by_manifest["general-security"]], ["access-1"])
        self.assertEqual([c["id"] for c in by_manifest["general-defi"]], ["precision-1"])

    def test_build_protocol_bundle_deduplicates_and_separates_critical_cards(self):
        cards_by_manifest = {
            "oracle": [
                {"id": "shared", "cat": ["oracle"]},
                {"id": "critical", "cat": ["oracle"], "neverPrune": True},
            ],
            "tokens": [
                {"id": "shared", "cat": ["token"]},
                {"id": "token-1", "cat": ["token"]},
            ],
        }

        bundle = build_protocol_bundle(
            "vault_yield",
            ["oracle", "tokens"],
            cards_by_manifest,
        )

        self.assertEqual(bundle["meta"]["totalCards"], 3)
        self.assertEqual(bundle["meta"]["criticalCards"], 1)
        self.assertEqual(bundle["meta"]["criticalCardIds"], ["critical"])
        shard_ids = [card_id for shard in bundle["shards"] for card_id in shard["cardIds"]]
        self.assertEqual(sorted(shard_ids), ["shared", "token-1"])

    def test_build_partition_bundles_writes_protocol_shard_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            huntcards_dir = root / "huntcards"
            bundles_dir = root / "bundles"
            huntcards_dir.mkdir()
            emitted = []
            all_cards = {
                "cards": [
                    {
                        "id": "oracle-1",
                        "ref": "DB/oracle/stale.md",
                        "cat": ["oracle"],
                    },
                    {
                        "id": "access-1",
                        "ref": "DB/general/access-control/owner.md",
                        "cat": ["access-control"],
                        "neverPrune": True,
                    },
                ]
            }
            with (huntcards_dir / "all-huntcards.json").open("w", encoding="utf-8") as f:
                json.dump(all_cards, f)

            result = build_partition_bundles(
                {},
                huntcards_dir=huntcards_dir,
                bundles_dir=bundles_dir,
                protocol_mappings={"custom": ["oracle", "general-security"]},
                emit=emitted.append,
            )

            with (bundles_dir / "custom-shards.json").open("r", encoding="utf-8") as f:
                bundle = json.load(f)

        self.assertTrue(result)
        self.assertEqual(bundle["meta"]["totalCards"], 2)
        self.assertEqual(bundle["meta"]["criticalCards"], 1)
        self.assertEqual(bundle["shards"][0]["cardIds"], ["oracle-1"])
        self.assertTrue(any("custom" in line for line in emitted))


if __name__ == "__main__":
    unittest.main(verbosity=2)
