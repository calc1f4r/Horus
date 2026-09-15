#!/usr/bin/env python3
"""Unit tests for the horus CLI python modules (scripts/horus_cli/)."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from horus_cli import common, db  # noqa: E402


class TestDbGraphArgParsing(unittest.TestCase):
    def test_no_args_prints_usage_and_succeeds(self):
        self.assertEqual(db.main([]), 0)

    def test_help_succeeds(self):
        self.assertEqual(db.main(["--help"]), 0)
        self.assertEqual(db.main(["-h"]), 0)

    def test_unknown_subcommand_is_usage_error(self):
        self.assertEqual(db.main(["frobnicate"]), 2)

    def test_unknown_flag_is_usage_error(self):
        self.assertEqual(db.main(["graph", "--nope"]), 2)


class TestValidateGraph(unittest.TestCase):
    def _write(self, payload) -> Path:
        tmp = Path(tempfile.mkdtemp()) / "graph.json"
        tmp.write_text(json.dumps(payload), encoding="utf-8")
        return tmp

    def test_missing_file_fails(self):
        missing = Path(tempfile.mkdtemp()) / "absent.json"
        self.assertEqual(db.validate_graph(missing), 1)

    def test_invalid_json_fails(self):
        tmp = Path(tempfile.mkdtemp()) / "graph.json"
        tmp.write_text("{not json", encoding="utf-8")
        self.assertEqual(db.validate_graph(tmp), 1)

    def test_empty_nodes_fails(self):
        self.assertEqual(db.validate_graph(self._write({"nodes": [], "links": []})), 1)

    def test_dangling_edge_fails(self):
        payload = {
            "nodes": [{"id": "a"}],
            "links": [{"source": "a", "target": "ghost"}],
        }
        self.assertEqual(db.validate_graph(self._write(payload)), 1)

    def test_valid_node_link_graph_passes(self):
        payload = {
            "nodes": [{"id": "a"}, {"id": "b"}],
            "links": [{"source": "a", "target": "b"}],
        }
        self.assertEqual(db.validate_graph(self._write(payload)), 0)

    def test_legacy_edges_key_accepted(self):
        """Older exports used 'edges' rather than node-link's 'links'."""
        payload = {
            "nodes": [{"id": "a"}, {"id": "b"}],
            "edges": [{"source": "a", "target": "b"}],
        }
        self.assertEqual(db.validate_graph(self._write(payload)), 0)

    def test_inlined_node_objects_accepted(self):
        """node-link JSON may inline the node object instead of its id."""
        payload = {
            "nodes": [{"id": "a"}, {"id": "b"}],
            "links": [{"source": {"id": "a"}, "target": {"id": "b"}}],
        }
        self.assertEqual(db.validate_graph(self._write(payload)), 0)


class TestCommonState(unittest.TestCase):
    def test_read_state_missing_returns_empty(self):
        original = common.state_path
        try:
            common.state_path = lambda: Path(tempfile.mkdtemp()) / "state.json"
            self.assertEqual(common.read_state(), {})
        finally:
            common.state_path = original

    def test_read_state_corrupt_returns_empty(self):
        original = common.state_path
        try:
            p = Path(tempfile.mkdtemp()) / "state.json"
            p.write_text("garbage", encoding="utf-8")
            common.state_path = lambda: p
            self.assertEqual(common.read_state(), {})
        finally:
            common.state_path = original

    def test_write_then_read_roundtrip(self):
        original = common.state_path
        try:
            p = Path(tempfile.mkdtemp()) / "state.json"
            common.state_path = lambda: p
            common.write_state({"repo_path": "/tmp/x", "schema_version": 1})
            self.assertEqual(common.read_state()["repo_path"], "/tmp/x")
        finally:
            common.state_path = original


class TestDispatcherRouting(unittest.TestCase):
    """The bash dispatcher must route every documented command to a module."""

    def test_every_dispatched_module_exists(self):
        dispatcher = (
            Path(__file__).resolve().parent.parent / "scripts" / "horus"
        ).read_text(encoding="utf-8")
        import re

        # only real dispatch lines, not the `-m horus_cli.X` placeholder in comments
        modules = set(re.findall(r'exec "\$PY" -m horus_cli\.(\w+)', dispatcher))
        self.assertTrue(modules, "dispatcher routes to no modules")
        pkg = Path(__file__).resolve().parent.parent / "scripts" / "horus_cli"
        for mod in sorted(modules):
            with self.subTest(module=mod):
                self.assertTrue(
                    (pkg / f"{mod}.py").is_file(), f"horus_cli/{mod}.py missing"
                )


if __name__ == "__main__":
    unittest.main()
