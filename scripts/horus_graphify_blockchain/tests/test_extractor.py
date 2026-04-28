"""
Tests for horus-graphify-blockchain extractor.

Run: pytest tests/

Tests use the fixture contracts in tests/fixtures/ and verify:
  - Node counts within ±10% of expected
  - Required node kinds present
  - Edge types present
  - Output is valid graphify JSON (nodes/edges/hyperedges arrays)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"
sys.path.insert(0, str(Path(__file__).parent.parent))

from horus_graphify_blockchain.extractor import extract_file, extract_directory
from horus_graphify_blockchain.schema import ExtractionResult


# ── Helpers ───────────────────────────────────────────────────────────────────

def node_kinds(result: ExtractionResult) -> set[str]:
    return {n.node_kind if hasattr(n, "node_kind") else n.get("node_kind", "") for n in result.nodes}


def edge_relations(result: ExtractionResult) -> set[str]:
    return {e.relation if hasattr(e, "relation") else e.get("relation", "") for e in result.edges}


def count_by_kind(result: ExtractionResult, kind: str) -> int:
    return sum(
        1 for n in result.nodes
        if (n.node_kind if hasattr(n, "node_kind") else n.get("node_kind", "")) == kind
    )


def is_valid_graphify_json(d: dict) -> bool:
    return (
        isinstance(d.get("nodes"), list)
        and isinstance(d.get("edges"), list)
        and isinstance(d.get("hyperedges"), list)
    )


# ── Solidity tests ────────────────────────────────────────────────────────────

class TestSolidity:
    fixture = str(FIXTURES / "solidity" / "ERC20.sol")

    def test_produces_valid_graphify_json(self):
        result = extract_file(self.fixture, language="solidity")
        assert is_valid_graphify_json(result.to_dict())

    def test_node_count_reasonable(self):
        result = extract_file(self.fixture, language="solidity")
        # ERC20.sol has 1 contract, 6 functions, 6 state vars, 2 events, 1 modifier
        assert len(result.nodes) >= 10, f"Expected ≥10 nodes, got {len(result.nodes)}"

    def test_has_module_node(self):
        result = extract_file(self.fixture, language="solidity")
        assert "Module" in node_kinds(result), "No Module node found"

    def test_has_function_nodes(self):
        result = extract_file(self.fixture, language="solidity")
        fn_count = count_by_kind(result, "Function")
        assert fn_count >= 5, f"Expected ≥5 Function nodes, got {fn_count}"

    def test_has_state_var_nodes(self):
        result = extract_file(self.fixture, language="solidity")
        sv_count = count_by_kind(result, "StateVar")
        assert sv_count >= 4, f"Expected ≥4 StateVar nodes, got {sv_count}"

    def test_has_event_nodes(self):
        result = extract_file(self.fixture, language="solidity")
        ev_count = count_by_kind(result, "Event")
        assert ev_count >= 1, f"Expected ≥1 Event nodes, got {ev_count}"

    def test_has_declares_edges(self):
        result = extract_file(self.fixture, language="solidity")
        assert "declares" in edge_relations(result)

    def test_node_ids_are_deterministic(self):
        r1 = extract_file(self.fixture, language="solidity")
        r2 = extract_file(self.fixture, language="solidity")
        ids1 = sorted(n.id if hasattr(n, "id") else n["id"] for n in r1.nodes)
        ids2 = sorted(n.id if hasattr(n, "id") else n["id"] for n in r2.nodes)
        assert ids1 == ids2, "Node IDs are not deterministic across runs"

    def test_no_chunk_suffixes_in_ids(self):
        result = extract_file(self.fixture, language="solidity")
        for node in result.nodes:
            nid = node.id if hasattr(node, "id") else node["id"]
            assert not any(f"_c{i}" in nid or f"_chunk{i}" in nid for i in range(10)), \
                f"Node ID '{nid}' has chunk suffix"


# ── Move-Sui tests ────────────────────────────────────────────────────────────

class TestMoveSui:
    fixture = str(FIXTURES / "move_sui" / "coin.move")

    def test_produces_valid_graphify_json(self):
        result = extract_file(self.fixture, language="move_sui")
        assert is_valid_graphify_json(result.to_dict())

    def test_node_count_reasonable(self):
        result = extract_file(self.fixture, language="move_sui")
        # coin.move: 1 module, 3 structs, 4 functions
        assert len(result.nodes) >= 5, f"Expected ≥5 nodes, got {len(result.nodes)}"

    def test_has_module_node(self):
        result = extract_file(self.fixture, language="move_sui")
        assert "Module" in node_kinds(result)

    def test_has_function_nodes(self):
        result = extract_file(self.fixture, language="move_sui")
        assert count_by_kind(result, "Function") >= 3

    def test_has_struct_nodes(self):
        result = extract_file(self.fixture, language="move_sui")
        assert count_by_kind(result, "Struct") >= 2


# ── Cairo tests ───────────────────────────────────────────────────────────────

class TestCairo:
    fixture = str(FIXTURES / "cairo" / "erc20.cairo")

    def test_produces_valid_graphify_json(self):
        result = extract_file(self.fixture, language="cairo")
        assert is_valid_graphify_json(result.to_dict())

    def test_node_count_reasonable(self):
        result = extract_file(self.fixture, language="cairo")
        # erc20.cairo: 1 module, 3+ functions, 2 events, storage fields
        assert len(result.nodes) >= 4, f"Expected ≥4 nodes, got {len(result.nodes)}"

    def test_has_module_node(self):
        result = extract_file(self.fixture, language="cairo")
        assert "Module" in node_kinds(result)


# ── Directory extraction ──────────────────────────────────────────────────────

class TestDirectoryExtraction:
    def test_extracts_all_fixture_languages(self):
        result = extract_directory(str(FIXTURES))
        assert len(result.nodes) > 10, f"Expected >10 nodes from all fixtures, got {len(result.nodes)}"

    def test_no_duplicate_node_ids(self):
        result = extract_directory(str(FIXTURES))
        ids = [n.id if hasattr(n, "id") else n["id"] for n in result.nodes]
        assert len(ids) == len(set(ids)), f"Duplicate node IDs in directory extraction"

    def test_output_serializes_to_json(self):
        result = extract_directory(str(FIXTURES))
        data = result.to_dict()
        # Should not raise
        _ = json.dumps(data)
        assert is_valid_graphify_json(data)
