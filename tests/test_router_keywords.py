#!/usr/bin/env python3
"""Unit tests for router and keyword artifact builders."""

import os
import sys
import unittest


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from horus_retrieval.keywords import build_quick_keywords  # noqa: E402
from horus_retrieval.protocol_context import router_protocol_mappings  # noqa: E402
from horus_retrieval.router import add_audit_checklist, add_protocol_context, build_lean_router  # noqa: E402


class TestRouterAndKeywords(unittest.TestCase):

    def test_build_lean_router_uses_manifest_meta(self):
        manifests = {
            "oracle": {
                "meta": {
                    "description": "oracle patterns",
                    "fileCount": 2,
                    "totalPatterns": 3,
                },
                "files": [],
            }
        }

        router = build_lean_router(manifests)

        self.assertEqual(router["manifests"]["oracle"]["file"], "DB/manifests/oracle.json")
        self.assertEqual(router["manifests"]["oracle"]["fileCount"], 2)
        self.assertEqual(router["manifests"]["oracle"]["totalPatterns"], 3)

    def test_add_protocol_context_uses_shared_taxonomy(self):
        router = {}

        add_protocol_context(router)

        self.assertEqual(router["protocolContext"]["mappings"], router_protocol_mappings())

    def test_add_audit_checklist_preserves_core_categories(self):
        router = {}

        add_audit_checklist(router)

        self.assertIn("general", router["auditChecklist"])
        self.assertIn("oracle", router["auditChecklist"])
        self.assertIn("amm", router["auditChecklist"])

    def test_build_quick_keywords_indexes_paths_code_keywords_search_keywords_and_titles(self):
        manifests = {
            "oracle": {
                "files": [
                    {
                        "file": "DB/oracle/price-manipulation/example.md",
                        "patterns": [
                            {
                                "title": "Stale Oracle Price",
                                "codeKeywords": ["getPrice"],
                                "searchKeywords": ["staleness"],
                            }
                        ],
                    }
                ],
            }
        }

        keywords = build_quick_keywords(manifests)
        mappings = keywords["mappings"]

        self.assertEqual(mappings["oracle"], ["oracle"])
        self.assertEqual(mappings["getprice"], ["oracle"])
        self.assertEqual(mappings["staleness"], ["oracle"])
        self.assertEqual(mappings["stale"], ["oracle"])
        self.assertEqual(mappings["price"], ["oracle"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
