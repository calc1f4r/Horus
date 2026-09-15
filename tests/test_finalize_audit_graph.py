#!/usr/bin/env python3
"""Regression tests for audit graph finalization."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

from networkx.readwrite import json_graph


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import finalize_audit_graph as finalizer  # noqa: E402


class TestFinalizeAuditGraph(unittest.TestCase):

    def test_raw_extraction_is_written_as_queryable_node_link_graph(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            codebase = root / "codebase"
            graphify_out = codebase / "graphify-out"
            graphify_out.mkdir(parents=True)
            out = root / "audit-output" / "graph" / "graph.json"

            extraction = {
                "nodes": [
                    {
                        "id": "oracle_card",
                        "label": "Oracle Stale Price",
                        "node_kind": "HuntCard",
                        "file_type": "document",
                        "source_file": "DB/oracle/example.md",
                    },
                    {
                        "id": "oracle_topic",
                        "label": "oracle",
                        "node_kind": "GraphHint",
                        "file_type": "document",
                        "source_file": "DB/oracle/example.md",
                    },
                ],
                "edges": [
                    {
                        "source": "oracle_card",
                        "target": "oracle_topic",
                        "relation": "has_graph_hint",
                        "confidence": "EXTRACTED",
                        "source_file": "DB/oracle/example.md",
                    }
                ],
                "hyperedges": [],
            }
            (graphify_out / ".graphify_extract.json").write_text(json.dumps(extraction), encoding="utf-8")

            base_file = finalizer.find_base_graph_file(codebase)
            loaded = finalizer.load_graphify_input(base_file)
            finalizer.write_node_link_graph(loaded, out)

            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertIn("links", data)
            self.assertNotIn("edges", data)
            self.assertGreaterEqual(len(data["nodes"]), 2)
            self.assertGreaterEqual(len(data["links"]), 1)
            self.assertEqual(data["links"][0]["confidence_score"], 1.0)
            json_graph.node_link_graph(data, edges="links")

    def test_nested_hyperedges_survive_legacy_node_link_input(self):
        graph_data = {
            "directed": True,
            "multigraph": False,
            "graph": {
                "hyperedges": [
                    {
                        "id": "access_flow",
                        "label": "Access flow",
                        "nodes": ["a", "b"],
                        "relation": "participate_in",
                    }
                ]
            },
            "nodes": [
                {"id": "a", "label": "A", "file_type": "code", "source_file": "src/a.sol"},
                {"id": "b", "label": "B", "file_type": "code", "source_file": "src/b.sol"},
            ],
            "links": [
                {
                    "source": "a",
                    "target": "b",
                    "relation": "calls",
                    "confidence": "EXTRACTED",
                    "source_file": "src/a.sol",
                }
            ],
        }

        loaded = finalizer.normalize_extraction(graph_data)

        self.assertEqual(loaded["hyperedges"][0]["id"], "access_flow")


if __name__ == "__main__":
    unittest.main(verbosity=2)
