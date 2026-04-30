#!/usr/bin/env python3
"""Run the non-mutating Horus retrieval and graph validation suite."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_step(name: str, cmd: list[str]) -> int:
    print(f"\n== {name} ==", flush=True)
    print(" ".join(cmd), flush=True)
    result = subprocess.run(cmd, cwd=ROOT, check=False)
    if result.returncode:
        print(f"{name} failed with exit code {result.returncode}", file=sys.stderr)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-unittests",
        action="store_true",
        help="Skip unittest discovery and run only artifact/tool checks.",
    )
    args = parser.parse_args()

    steps: list[tuple[str, list[str]]] = [
        ("Python compile", [sys.executable, "-m", "py_compile", "scripts/db_quality_check.py", "scripts/build_db_graph.py", "scripts/finalize_audit_graph.py"]),
        ("DB quality check", [sys.executable, "scripts/db_quality_check.py"]),
        ("Graphify topic query", ["graphify", "query", "oracle flash loan", "--graph", "DB/graphify-out/graph.json", "--budget", "1000"]),
        ("Graphify path query", ["graphify", "path", "oracle", "flash-loan", "--graph", "DB/graphify-out/graph.json"]),
        ("Codex sync check", [sys.executable, "scripts/sync_codex_compat.py", "--check"]),
    ]

    if not args.skip_unittests:
        steps.insert(1, ("Unit tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]))

    with tempfile.TemporaryDirectory() as tmp:
        finalized = str(Path(tmp) / "finalized-graph.json")
        steps.append(
            (
                "Audit graph finalizer",
                [
                    sys.executable,
                    "scripts/finalize_audit_graph.py",
                    "--codebase",
                    "DB",
                    "--out",
                    finalized,
                    "--skip-query-smoke",
                    "--strict",
                ],
            )
        )

        failures = 0
        for name, cmd in steps:
            failures += 1 if run_step(name, cmd) else 0

    if failures:
        print(f"\nValidation failed: {failures} step(s) failed", file=sys.stderr)
        return 1

    print("\nValidation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
