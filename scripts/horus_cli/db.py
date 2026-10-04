"""horus db graph — rebuild and validate the Horus DB knowledge graph.

Wraps scripts/build_db_graph.py, then validates the emitted node-link JSON.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from . import common

USAGE = """Usage: horus db graph [--no-validate]

Rebuilds DB/graphify-out/graph.json from the DB entries and manifests, then
validates the result (node/edge counts, endpoint resolution, node-link schema).

Options:
  --no-validate   Skip the post-build validation step
  -h, --help      Show this help
"""


def _graph_path(repo: Path) -> Path:
    return repo / "DB" / "graphify-out" / "graph.json"


def _interpreter() -> str:
    """Prefer the bootstrapped venv python; fall back to the current one."""
    venv = common.venv_python()
    return str(venv) if venv else sys.executable


def build_graph(repo: Path) -> int:
    script = repo / "scripts" / "build_db_graph.py"
    if not script.is_file():
        common.log_error(f"missing generator: {script}")
        return 1

    common.log_info(f"building DB graph via {script.name}")
    proc = subprocess.run(
        [_interpreter(), str(script)],
        cwd=str(repo),
        env={**os.environ, "PYTHONPATH": str(repo / "scripts")},
    )
    if proc.returncode != 0:
        common.log_error(f"build_db_graph.py exited {proc.returncode}")
        return proc.returncode
    return 0


def validate_graph(path: Path) -> int:
    """Validate the node-link graph. Returns 0 on success, 1 on failure."""
    if not path.is_file():
        common.log_error(f"graph not found after build: {path}")
        return 1

    try:
        with path.open("r", encoding="utf-8") as f:
            graph = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        common.log_error(f"{path}: invalid JSON: {exc}")
        return 1

    nodes = graph.get("nodes") or []
    # graphify exports node-link with "links"; older exports used "edges"
    links = graph.get("links") or graph.get("edges") or []
    hyperedges = graph.get("hyperedges") or []
    communities = graph.get("communities") or []

    failures: list[str] = []
    if not nodes:
        failures.append("graph has no nodes")
    if not links:
        failures.append("graph has no links/edges")

    node_ids = {n.get("id") for n in nodes if isinstance(n, dict)}
    dangling = 0
    for link in links:
        if not isinstance(link, dict):
            continue
        src = link.get("source")
        tgt = link.get("target")
        # node-link JSON may inline the node object rather than its id
        if isinstance(src, dict):
            src = src.get("id")
        if isinstance(tgt, dict):
            tgt = tgt.get("id")
        if src not in node_ids or tgt not in node_ids:
            dangling += 1
    if dangling:
        failures.append(f"{dangling} edges have endpoints missing from nodes")

    print(
        f"graph: {len(nodes)} nodes, {len(links)} edges, "
        f"{len(hyperedges)} hyperedges, {len(communities)} communities"
    )

    if failures:
        for f in failures:
            common.log_error(f)
        return 1

    common.log_pass(f"graph validated: {path}")
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(USAGE)
        return 0

    sub = argv[0]
    if sub != "graph":
        print(f"horus db: unknown subcommand: {sub}", file=sys.stderr)
        print(USAGE, file=sys.stderr)
        return 2

    flags = argv[1:]
    unknown = [f for f in flags if f != "--no-validate"]
    if unknown:
        print(f"horus db graph: unknown option(s): {' '.join(unknown)}", file=sys.stderr)
        print(USAGE, file=sys.stderr)
        return 2

    try:
        repo = common.horus_home()
    except RuntimeError as exc:
        common.log_error(str(exc))
        return 1

    rc = build_graph(repo)
    if rc != 0:
        return rc

    if "--no-validate" in flags:
        common.log_info("validation skipped (--no-validate)")
        return 0

    return validate_graph(_graph_path(repo))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
