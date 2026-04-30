#!/usr/bin/env python3
"""Regression tests for DB Graphify graph construction."""

import os
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import build_db_graph as graph_builder  # noqa: E402


class TestDbGraphBuilder(unittest.TestCase):

    def test_build_extraction_adds_semantic_nodes_and_related_edges(self):
        cards = [
            {
                "id": "oracle-flash-loan-001",
                "title": "Flash Loan Oracle Manipulation",
                "severity": "HIGH",
                "grep": "latestRoundData|flashLoan",
                "cat": ["oracle"],
                "ref": "DB/oracle/example.md",
                "graphHints": {
                    "variants": ["flash loan oracle manipulation", "spot price manipulation"],
                    "commonlyComposesWith": ["lending liquidation"],
                },
                "reportEvidence": {
                    "severityConsensus": "HIGH",
                    "sampleReports": ["reports/oracle/example.md"],
                },
            },
            {
                "id": "oracle-stale-price-002",
                "title": "Oracle Stale Price",
                "severity": "HIGH",
                "grep": "latestRoundData|updatedAt",
                "cat": ["oracle"],
                "ref": "DB/oracle/example.md",
                "graphHints": {
                    "variants": ["flash loan oracle manipulation", "stale price"],
                    "commonlyComposesWith": ["lending liquidation"],
                },
                "reportEvidence": {
                    "severityConsensus": "HIGH",
                    "sampleReports": ["reports/oracle/example.md"],
                },
            },
        ]

        original_loader = graph_builder._load_manifest_context
        graph_builder._load_manifest_context = lambda: {
            "oracle-flash-loan-001": {
                "manifest": "oracle",
                "file": "DB/oracle/example.md",
                "frontmatter": {
                    "root_cause_family": "oracle_price_manipulation",
                    "attack_type": "flash_loan|economic_exploit",
                    "affected_component": "price_oracle",
                },
                "pattern": {},
            },
            "oracle-stale-price-002": {
                "manifest": "oracle",
                "file": "DB/oracle/example.md",
                "frontmatter": {
                    "root_cause_family": "oracle_price_manipulation",
                    "attack_type": "stale_data|economic_exploit",
                    "affected_component": "price_oracle",
                },
                "pattern": {},
            },
        }
        try:
            extraction = graph_builder.build_extraction(cards)
        finally:
            graph_builder._load_manifest_context = original_loader

        kinds = {node["node_kind"] for node in extraction["nodes"]}
        for expected in {
            "RootCauseFamily",
            "AttackType",
            "AffectedComponent",
            "GraphHint",
            "ReportEvidence",
            "ProtocolContext",
            "Manifest",
            "Severity",
        }:
            self.assertIn(expected, kinds)

        relations = {edge["relation"] for edge in extraction["edges"]}
        self.assertIn("related_variant", relations)
        self.assertIn("has_graph_hint", relations)
        self.assertIn("has_root_cause_family", relations)
        self.assertIn("routes_to_manifest", relations)

    def test_curate_wiki_communities_keeps_largest_named_communities(self):
        communities = {
            1: ["a"],
            2: ["b", "c", "d"],
            3: ["e", "f"],
            4: ["g", "h", "i", "j"],
        }
        labels = {
            1: "DB Community 1",
            2: "oracle",
            3: "bridge",
            4: "amm",
        }
        cohesion = {1: 0.9, 2: 0.2, 3: 0.7, 4: 0.1}

        curated = graph_builder._curate_wiki_communities(communities, labels, cohesion, limit=2)

        self.assertEqual(set(curated), {2, 4})

    def test_curate_wiki_communities_drops_singleton_when_room_remains(self):
        communities = {
            1: ["a"],
            2: ["b", "c"],
            3: ["d"],
        }
        labels = {
            1: "DB Community 1",
            2: "oracle",
            3: "DB Community 3",
        }

        curated = graph_builder._curate_wiki_communities(communities, labels, {}, limit=80)

        self.assertEqual(set(curated), {2})

    def test_reset_wiki_dir_removes_only_markdown_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            wiki_dir = Path(tmpdir)
            (wiki_dir / "index.md").write_text("old", encoding="utf-8")
            (wiki_dir / "oracle.md").write_text("old", encoding="utf-8")
            (wiki_dir / ".keep").write_text("keep", encoding="utf-8")

            graph_builder._reset_wiki_dir(wiki_dir)

            self.assertFalse((wiki_dir / "index.md").exists())
            self.assertFalse((wiki_dir / "oracle.md").exists())
            self.assertTrue((wiki_dir / ".keep").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
