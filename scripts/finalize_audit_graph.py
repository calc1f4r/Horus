#!/usr/bin/env python3
"""Finalize audit-time Graphify artifacts into a queryable graph.json.

Graphify produces two different JSON shapes:

- .graphify_extract.json: extraction JSON with nodes/edges.
- graph.json: NetworkX node-link JSON with nodes/links.

Audit agents and Graphify CLI/MCP expect the second shape whenever a file is
named graph.json. This script converts and merges inputs so Phase 0 cannot
accidentally publish raw extraction JSON as the final audit graph.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from graphify import build, cluster, export
from networkx.readwrite import json_graph


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def edge_list(data: dict[str, Any]) -> list[dict[str, Any]]:
    edges = data.get("links") if "links" in data else data.get("edges")
    if edges is None:
        return []
    if not isinstance(edges, list):
        raise ValueError("graph edges/links must be a list")
    return [edge for edge in edges if isinstance(edge, dict)]


def is_node_link_graph(data: dict[str, Any]) -> bool:
    return isinstance(data.get("nodes"), list) and isinstance(data.get("links"), list)


def normalize_node(node: dict[str, Any]) -> dict[str, Any]:
    node_id = str(node.get("id") or node.get("label") or "")
    if not node_id:
        raise ValueError("node is missing id")
    return {
        **node,
        "id": node_id,
        "label": str(node.get("label") or node_id),
        "file_type": str(node.get("file_type") or "document"),
        "source_file": str(node.get("source_file") or "unknown"),
    }


def normalize_edge(edge: dict[str, Any]) -> dict[str, Any]:
    source = edge.get("source")
    target = edge.get("target")
    if source is None or target is None:
        raise ValueError("edge is missing source or target")
    return {
        **edge,
        "source": str(source),
        "target": str(target),
        "relation": str(edge.get("relation") or edge.get("type") or "references"),
        "confidence": str(edge.get("confidence") or "EXTRACTED"),
        "source_file": str(edge.get("source_file") or "unknown"),
    }


def normalize_extraction(data: dict[str, Any]) -> dict[str, Any]:
    nodes = data.get("nodes")
    if not isinstance(nodes, list):
        raise ValueError("input graph/extraction is missing nodes list")

    normalized_nodes = []
    for node in nodes:
        if isinstance(node, dict):
            normalized_nodes.append(normalize_node(node))

    normalized_edges = []
    for edge in edge_list(data):
        normalized_edges.append(normalize_edge(edge))

    return {
        "nodes": normalized_nodes,
        "edges": normalized_edges,
        "hyperedges": data.get("hyperedges", []) if isinstance(data.get("hyperedges", []), list) else [],
        "input_tokens": data.get("input_tokens", 0),
        "output_tokens": data.get("output_tokens", 0),
    }


def load_graphify_input(path: Path) -> dict[str, Any]:
    data = load_json(path)
    if is_node_link_graph(data):
        # NetworkX validates the node-link shape and normalizes any graph-level
        # quirks before we convert back into graphify extraction input.
        json_graph.node_link_graph(data, edges="links")
    return normalize_extraction(data)


def find_base_graph_file(codebase: Path) -> Path:
    graph = codebase / "graphify-out" / "graph.json"
    extract = codebase / "graphify-out" / ".graphify_extract.json"
    if graph.exists():
        return graph
    if extract.exists():
        return extract
    raise FileNotFoundError(
        f"No Graphify output found under {codebase}/graphify-out "
        "(expected graph.json or .graphify_extract.json)"
    )


def merge_extractions(base: dict[str, Any], extra: dict[str, Any] | None) -> dict[str, Any]:
    if extra is None:
        return base

    nodes_by_id: dict[str, dict[str, Any]] = {}
    for node in [*base["nodes"], *extra["nodes"]]:
        nodes_by_id.setdefault(node["id"], node)

    edge_keys = set()
    merged_edges = []
    for edge in [*base["edges"], *extra["edges"]]:
        key = (
            edge.get("source"),
            edge.get("target"),
            edge.get("relation"),
            edge.get("source_file"),
        )
        if key in edge_keys:
            continue
        edge_keys.add(key)
        if edge["source"] in nodes_by_id and edge["target"] in nodes_by_id:
            merged_edges.append(edge)

    hyperedges = []
    seen_hyperedges = set()
    for hyperedge in [*base.get("hyperedges", []), *extra.get("hyperedges", [])]:
        marker = json.dumps(hyperedge, sort_keys=True)
        if marker not in seen_hyperedges:
            seen_hyperedges.add(marker)
            hyperedges.append(hyperedge)

    return {
        "nodes": list(nodes_by_id.values()),
        "edges": merged_edges,
        "hyperedges": hyperedges,
        "input_tokens": int(base.get("input_tokens", 0)) + int(extra.get("input_tokens", 0)),
        "output_tokens": int(base.get("output_tokens", 0)) + int(extra.get("output_tokens", 0)),
    }


def write_node_link_graph(extraction: dict[str, Any], out: Path) -> None:
    graph = build.build([extraction], directed=True)
    communities = cluster.cluster(graph)
    out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_out = Path(tmp) / "graph.json"
        export.to_json(graph, communities, str(tmp_out), force=True)
        graph_data = load_json(tmp_out)

    if "links" not in graph_data and "edges" in graph_data:
        graph_data["links"] = graph_data["edges"]
    if "edges" not in graph_data and "links" in graph_data:
        graph_data["edges"] = graph_data["links"]

    validate_node_link_graph(graph_data)
    out.write_text(json.dumps(graph_data, indent=2), encoding="utf-8")


def validate_node_link_graph(data: dict[str, Any]) -> None:
    if not isinstance(data.get("nodes"), list) or not data["nodes"]:
        raise ValueError("final graph has no nodes")
    if not isinstance(data.get("links"), list) or not data["links"]:
        raise ValueError("final graph has no links")

    json_graph.node_link_graph(data, edges="links")

    node_ids = {node.get("id") for node in data["nodes"] if isinstance(node, dict)}
    missing = 0
    for edge in data["links"]:
        if not isinstance(edge, dict):
            missing += 1
            continue
        if edge.get("source") not in node_ids or edge.get("target") not in node_ids:
            missing += 1
    if missing:
        raise ValueError(f"final graph has {missing} links with missing endpoints")


def run_query_smoke(out: Path, query: str) -> tuple[bool, str]:
    graphify_bin = shutil.which("graphify")
    if not graphify_bin:
        return True, "graphify CLI not found; skipped query smoke test"

    result = subprocess.run(
        [graphify_bin, "query", query, "--graph", str(out), "--budget", "200"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        timeout=20,
        check=False,
    )
    if result.returncode != 0:
        return False, result.stderr.strip() or f"graphify query exited {result.returncode}"
    return True, "graphify query smoke test OK"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codebase", required=True, help="Target codebase path containing graphify-out/")
    parser.add_argument("--out", default="audit-output/graph/graph.json", help="Final graph.json output path")
    parser.add_argument("--blockchain-ast", help="Optional horus-graphify-blockchain extraction JSON")
    parser.add_argument("--query", default="security", help="Query used for optional Graphify CLI smoke test")
    parser.add_argument("--strict", action="store_true", help="Return nonzero when optional validation fails")
    parser.add_argument("--skip-query-smoke", action="store_true", help="Skip Graphify CLI smoke query")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    codebase = Path(args.codebase)
    out = Path(args.out)

    try:
        base_file = find_base_graph_file(codebase)
        base = load_graphify_input(base_file)

        blockchain = None
        if args.blockchain_ast:
            blockchain_path = Path(args.blockchain_ast)
            if blockchain_path.exists():
                blockchain = load_graphify_input(blockchain_path)

        merged = merge_extractions(base, blockchain)
        write_node_link_graph(merged, out)

        print(f"Base graph source: {base_file}")
        if blockchain is not None:
            print(f"Merged blockchain AST: {args.blockchain_ast}")
        print(f"Written: {out}")

        if not args.skip_query_smoke:
            ok, message = run_query_smoke(out, args.query)
            print(message)
            if not ok and args.strict:
                return 1

        return 0
    except Exception as exc:
        print(f"WARNING: audit graph finalization failed: {exc}", file=sys.stderr)
        return 1 if args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
