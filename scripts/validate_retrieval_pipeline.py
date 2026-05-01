#!/usr/bin/env python3
"""Run the non-mutating Horus retrieval and graph validation suite."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED_DB_COPY_DIRS = {"graphify-out", "manifests", "_telemetry"}


def run_step(name: str, cmd: list[str]) -> int:
    print(f"\n== {name} ==", flush=True)
    print(" ".join(cmd), flush=True)
    result = subprocess.run(cmd, cwd=ROOT, check=False)
    if result.returncode:
        print(f"{name} failed with exit code {result.returncode}", file=sys.stderr)
    return result.returncode


def run_callable_step(name: str, fn) -> int:
    print(f"\n== {name} ==", flush=True)
    try:
        fn()
    except Exception as exc:
        print(f"{name} failed: {exc}", file=sys.stderr)
        return 1
    return 0


def validate_generated_huntcard_regexes() -> None:
    path = ROOT / "DB/manifests/huntcards/all-huntcards.json"
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    invalid = []
    for card in data.get("cards", []):
        try:
            re.compile(card.get("grep", ""))
        except re.error as exc:
            invalid.append((card.get("id", "<unknown>"), str(exc)))

    if invalid:
        sample = "\n".join(f"- {card_id}: {error}" for card_id, error in invalid[:10])
        raise RuntimeError(f"{len(invalid)} invalid hunt-card regexes\n{sample}")

    print(f"Validated {len(data.get('cards', []))} hunt-card regexes.", flush=True)


def validate_grep_prune_partition_smoke() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        target = tmp_path / "target"
        target.mkdir()
        (target / "vault.cairo").write_text("fn update_price() {}\n", encoding="utf-8")

        cards_path = tmp_path / "huntcards.json"
        hits_path = tmp_path / "hits.json"
        shards_path = tmp_path / "shards.json"
        cards_path.write_text(
            json.dumps(
                {
                    "cards": [
                        {
                            "id": "cairo-card",
                            "title": "Cairo price update",
                            "severity": "HIGH",
                            "grep": "update_price",
                            "cat": ["cairo"],
                        },
                        {
                            "id": "critical-card",
                            "title": "Critical safety card",
                            "severity": "CRITICAL",
                            "grep": "missing_critical_sink",
                            "cat": ["critical"],
                            "neverPrune": True,
                        },
                        {
                            "id": "invalid-regex-card",
                            "title": "Invalid regex custom card",
                            "severity": "HIGH",
                            "grep": "balanceOf(address(this",
                            "cat": ["custom"],
                        },
                    ]
                }
            ),
            encoding="utf-8",
        )

        grep_result = subprocess.run(
            [
                sys.executable,
                "scripts/grep_prune.py",
                str(target),
                str(cards_path),
                "--language",
                "all",
                "--output",
                str(hits_path),
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if grep_result.returncode:
            raise RuntimeError(grep_result.stderr.strip() or grep_result.stdout.strip())

        partition_result = subprocess.run(
            [
                sys.executable,
                "scripts/partition_shards.py",
                str(hits_path),
                "--output",
                str(shards_path),
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if partition_result.returncode:
            raise RuntimeError(partition_result.stderr.strip() or partition_result.stdout.strip())

        hits = json.loads(hits_path.read_text(encoding="utf-8"))
        shards = json.loads(shards_path.read_text(encoding="utf-8"))
        if "*.cairo" not in hits.get("fileFilter", []) or "*.vy" not in hits.get("fileFilter", []):
            raise RuntimeError(f"language filter missing cairo/vy support: {hits.get('fileFilter')}")
        if hits.get("survivingCards") != 3:
            raise RuntimeError(f"expected 3 surviving cards, got {hits.get('survivingCards')}")
        if hits.get("searchErrorCards") != 1:
            raise RuntimeError(f"expected 1 search-error card, got {hits.get('searchErrorCards')}")
        if shards.get("shardCount", 0) < 1:
            raise RuntimeError("partition output has no actionable shards")
        if "critical-card" not in shards.get("criticalCardIds", []):
            raise RuntimeError("partition output lost critical card")
        errored = [card for card in hits.get("hits", []) if card.get("id") == "invalid-regex-card"]
        if not errored or "searchError" not in errored[0]:
            raise RuntimeError("grep-prune lost invalid-regex card instead of preserving searchError")

    print("grep-prune and partition smoke test OK.", flush=True)


def copy_db_sources(source_db: Path, target_db: Path) -> None:
    """Copy DB sources needed for regeneration, excluding generated artifacts."""
    target_db.mkdir(parents=True, exist_ok=True)
    for source_path in source_db.iterdir():
        if source_path.name in IGNORED_DB_COPY_DIRS:
            continue
        target_path = target_db / source_path.name
        if source_path.is_dir():
            shutil.copytree(source_path, target_path)
        else:
            shutil.copy2(source_path, target_path)


def file_hashes(root: Path) -> dict[str, str]:
    import hashlib

    hashes = {}
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        hashes[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def graph_artifact_hashes(root: Path) -> dict[str, str]:
    import hashlib

    selected = []
    for relative in ("graph.json", "GRAPH_REPORT.md", ".graphify_version"):
        path = root / relative
        if path.is_file():
            selected.append(path)
    wiki_dir = root / "wiki"
    if wiki_dir.is_dir():
        selected.extend(sorted(path for path in wiki_dir.rglob("*.md") if path.is_file()))

    hashes = {}
    for path in sorted(selected):
        rel = path.relative_to(root).as_posix()
        hashes[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def validate_generated_artifacts_current() -> None:
    from horus_retrieval.build import build_retrieval_db

    with tempfile.TemporaryDirectory() as tmp:
        temp_db = Path(tmp) / "DB"
        copy_db_sources(ROOT / "DB", temp_db)
        build_retrieval_db(db_dir=temp_db, emit=lambda _line: None)

        current_index = (ROOT / "DB/index.json").read_bytes()
        expected_index = (temp_db / "index.json").read_bytes()
        if current_index != expected_index:
            raise RuntimeError(
                "DB/index.json is stale; run `python3 scripts/generate_manifests.py` and commit the result"
            )

        current_hashes = file_hashes(ROOT / "DB/manifests")
        expected_hashes = file_hashes(temp_db / "manifests")
        if current_hashes != expected_hashes:
            missing = sorted(expected_hashes.keys() - current_hashes.keys())
            extra = sorted(current_hashes.keys() - expected_hashes.keys())
            changed = sorted(
                key for key in current_hashes.keys() & expected_hashes.keys()
                if current_hashes[key] != expected_hashes[key]
            )
            detail_parts = []
            if missing:
                detail_parts.append(f"missing={missing[:5]}")
            if extra:
                detail_parts.append(f"extra={extra[:5]}")
            if changed:
                detail_parts.append(f"changed={changed[:5]}")
            detail = "; ".join(detail_parts) or "manifest hash mismatch"
            raise RuntimeError(
                "DB/manifests artifacts are stale; run `python3 scripts/generate_manifests.py` "
                f"and commit the result ({detail})"
            )

    print("Generated retrieval artifacts are current.", flush=True)


def validate_graph_artifacts_current() -> None:
    from build_db_graph import build_db_graph

    with tempfile.TemporaryDirectory() as tmp:
        temp_root = Path(tmp)
        temp_out = temp_root / "graphify-out"
        build_db_graph(db=ROOT / "DB", out=temp_out, root=temp_root, emit=lambda _line: None)

        current_hashes = graph_artifact_hashes(ROOT / "DB/graphify-out")
        expected_hashes = graph_artifact_hashes(temp_out)
        if current_hashes != expected_hashes:
            missing = sorted(expected_hashes.keys() - current_hashes.keys())
            extra = sorted(current_hashes.keys() - expected_hashes.keys())
            changed = sorted(
                key for key in current_hashes.keys() & expected_hashes.keys()
                if current_hashes[key] != expected_hashes[key]
            )
            detail_parts = []
            if missing:
                detail_parts.append(f"missing={missing[:5]}")
            if extra:
                detail_parts.append(f"extra={extra[:5]}")
            if changed:
                detail_parts.append(f"changed={changed[:5]}")
            detail = "; ".join(detail_parts) or "graph artifact hash mismatch"
            raise RuntimeError(
                "DB graph artifacts are stale; run `python3 scripts/build_db_graph.py` "
                f"and commit DB/graphify-out ({detail})"
            )

    print("DB graph artifacts are current.", flush=True)


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

    failures += run_callable_step("Generated artifact freshness", validate_generated_artifacts_current)
    failures += run_callable_step("DB graph artifact freshness", validate_graph_artifacts_current)
    failures += run_callable_step("Generated hunt-card regex validation", validate_generated_huntcard_regexes)
    failures += run_callable_step("Grep-prune partition smoke", validate_grep_prune_partition_smoke)

    if failures:
        print(f"\nValidation failed: {failures} step(s) failed", file=sys.stderr)
        return 1

    print("\nValidation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
