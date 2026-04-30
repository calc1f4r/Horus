#!/usr/bin/env python3
"""Unit tests for the shared protocol context taxonomy."""

import os
import json
import sys
import unittest
from pathlib import Path


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from horus_retrieval.protocol_context import (  # noqa: E402
    PROTOCOL_CONTEXTS,
    bundle_manifest_mapping,
    router_protocol_mappings,
)


class TestProtocolContext(unittest.TestCase):

    def test_contexts_have_required_fields(self):
        for name, context in PROTOCOL_CONTEXTS.items():
            with self.subTest(name=name):
                self.assertTrue(name)
                self.assertTrue(context.description)
                self.assertTrue(context.manifests)
                self.assertTrue(context.focus_patterns)

    def test_router_mappings_match_contexts(self):
        mappings = router_protocol_mappings()

        self.assertEqual(list(mappings), list(PROTOCOL_CONTEXTS))
        for name, context in PROTOCOL_CONTEXTS.items():
            with self.subTest(name=name):
                self.assertEqual(mappings[name]["description"], context.description)
                self.assertEqual(mappings[name]["manifests"], list(context.manifests))
                self.assertEqual(mappings[name]["focusPatterns"], list(context.focus_patterns))

    def test_bundle_mapping_reuses_context_manifests(self):
        bundle_mapping = bundle_manifest_mapping()

        self.assertEqual(list(bundle_mapping), list(PROTOCOL_CONTEXTS))
        for name, context in PROTOCOL_CONTEXTS.items():
            with self.subTest(name=name):
                self.assertEqual(bundle_mapping[name], list(context.manifests))

    def test_current_index_protocol_mappings_match_shared_context(self):
        repo_root = Path(__file__).resolve().parents[1]
        index_path = repo_root / "DB" / "index.json"
        with index_path.open(encoding="utf-8") as f:
            index = json.load(f)

        self.assertEqual(
            index["protocolContext"]["mappings"],
            router_protocol_mappings(),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
