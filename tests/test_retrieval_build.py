#!/usr/bin/env python3
"""Unit tests for retrieval build orchestration."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from horus_retrieval.build import RetrievalBuildDeps, build_retrieval_db  # noqa: E402


class TestRetrievalBuild(unittest.TestCase):

    def test_build_retrieval_db_orchestrates_writes_without_real_db(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db_dir = root / "DB"
            manifest_dir = db_dir / "manifests"
            huntcards_dir = manifest_dir / "huntcards"
            db_dir.mkdir(parents=True)

            def build_manifest(category, folders):
                return {
                    "meta": {
                        "category": category,
                        "description": f"{category} manifest",
                        "fileCount": len(folders),
                        "totalPatterns": 1,
                    },
                    "files": [],
                }

            def build_general_sub_manifests():
                return {
                    "general-security": {
                        "meta": {
                            "category": "general-security",
                            "description": "general security",
                            "fileCount": 1,
                            "totalPatterns": 2,
                        },
                        "files": [],
                    }
                }

            def build_lean_router(manifests):
                return {
                    "meta": {},
                    "manifests": {
                        name: {"fileCount": data["meta"]["fileCount"]}
                        for name, data in manifests.items()
                    },
                }

            def add_protocol_context(router):
                router["protocolContext"] = {"mappings": {}}

            def add_audit_checklist(router):
                router["auditChecklist"] = {}

            def build_quick_keywords(manifests):
                return {"totalKeywords": len(manifests), "mappings": {}}

            def build_all_huntcards(manifests):
                huntcards_dir.mkdir(parents=True)
                all_cards = {
                    "meta": {"totalCards": len(manifests)},
                    "cards": [],
                }
                with (huntcards_dir / "all-huntcards.json").open("w", encoding="utf-8") as f:
                    json.dump(all_cards, f)
                return {}, len(manifests)

            bundle_calls = []

            def build_partition_bundles(manifests):
                bundle_calls.append(sorted(manifests))

            deps = RetrievalBuildDeps(
                build_manifest=build_manifest,
                build_general_sub_manifests=build_general_sub_manifests,
                build_lean_router=build_lean_router,
                add_protocol_context=add_protocol_context,
                add_audit_checklist=add_audit_checklist,
                build_quick_keywords=build_quick_keywords,
                build_all_huntcards=build_all_huntcards,
                build_partition_bundles=build_partition_bundles,
            )

            emitted = []
            result = build_retrieval_db(
                db_dir=db_dir,
                manifest_dir=manifest_dir,
                huntcards_dir=huntcards_dir,
                category_map={"oracle": ["oracle"], "general": ["general"]},
                deps=deps,
                enrich=False,
                build_bundles=True,
                emit=emitted.append,
            )

            self.assertEqual(sorted(result.manifests), ["general-security", "oracle"])
            self.assertEqual(result.total_huntcards, 2)
            self.assertTrue((manifest_dir / "oracle.json").exists())
            self.assertTrue((manifest_dir / "general-security.json").exists())
            self.assertTrue((manifest_dir / "keywords.json").exists())
            self.assertTrue((db_dir / "index.json").exists())
            self.assertEqual(bundle_calls, [["general-security", "oracle"]])
            self.assertIn("Horus Manifest Generator", emitted)

    def test_build_retrieval_db_has_standard_defaults_for_temp_db(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db_dir = root / "DB"
            entry = db_dir / "oracle" / "sample.md"
            entry.parent.mkdir(parents=True)
            entry.write_text(
                "---\n"
                "protocol: ethereum\n"
                "category: oracle\n"
                "severity: high\n"
                "---\n"
                "# Oracle Sample\n\n"
                "## Stale Oracle Price [HIGH]\n\n"
                "Root Cause:\n\n"
                "The protocol accepts stale `latestRoundData()` values.\n\n"
                "```solidity\n"
                "oracle.latestRoundData();\n"
                "```\n"
                + "\n".join(f"Validation detail {i}." for i in range(12))
                + "\n",
                encoding="utf-8",
            )

            emitted = []
            result = build_retrieval_db(
                db_dir=db_dir,
                category_map={"oracle": ["oracle"]},
                enrich=False,
                build_bundles=False,
                emit=emitted.append,
            )

            manifest_dir = db_dir / "manifests"
            self.assertEqual(sorted(result.manifests), ["oracle"])
            self.assertTrue((manifest_dir / "oracle.json").exists())
            self.assertTrue((manifest_dir / "keywords.json").exists())
            self.assertTrue((manifest_dir / "huntcards" / "all-huntcards.json").exists())
            self.assertTrue((db_dir / "index.json").exists())
            self.assertGreaterEqual(result.total_huntcards, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
