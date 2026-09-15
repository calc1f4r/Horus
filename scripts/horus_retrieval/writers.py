"""Filesystem writers and reporting helpers for retrieval artifacts."""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Callable


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def file_size(path: Path) -> int:
    return os.path.getsize(path)


def backup_existing_file(path: Path, backup_path: Path) -> bool:
    if not path.exists():
        return False
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup_path)
    return True


def write_router_index(db_dir: Path, router: dict, emit: Callable[[str], None]) -> None:
    router_path = db_dir / "index.json"
    old_index = db_dir / "index.old.json"
    if backup_existing_file(router_path, old_index):
        emit(f"   → Backed up old index to {old_index}")

    write_json(router_path, router)

    router_size = file_size(router_path)
    old_size = file_size(old_index) if old_index.exists() else 0
    emit(f"   → New index.json: {router_size:,} bytes")
    if old_size:
        emit(f"   → Old index.json: {old_size:,} bytes")
        emit(f"   → Size reduction: {(1 - router_size / old_size) * 100:.1f}%")


def emit_artifact_summary(
    *,
    manifests: dict,
    manifest_dir: Path,
    huntcards_dir: Path,
    total_huntcards: int,
    emit: Callable[[str], None],
) -> None:
    emit(f"\n{'=' * 60}")
    emit("Summary")
    emit(f"{'=' * 60}")
    total_patterns = sum(m["meta"]["totalPatterns"] for m in manifests.values())
    total_files = sum(m["meta"]["fileCount"] for m in manifests.values())
    emit(f"Total files indexed: {total_files}")
    emit(f"Total patterns extracted: {total_patterns}")
    emit(f"Total hunt cards generated: {total_huntcards}")
    emit(f"Manifests generated: {len(manifests)}")

    emit("\nManifest files:")
    for cat in sorted(manifests.keys()):
        mf = manifest_dir / f"{cat}.json"
        size = file_size(mf)
        emit(f"  DB/manifests/{cat}.json - {size:,} bytes ({manifests[cat]['meta']['totalPatterns']} patterns)")

    emit("\nHunt card files:")
    for cat in sorted(manifests.keys()):
        hc = huntcards_dir / f"{cat}-huntcards.json"
        if hc.exists():
            size = file_size(hc)
            emit(f"  DB/manifests/huntcards/{cat}-huntcards.json - {size:,} bytes")
    combined_hc = huntcards_dir / "all-huntcards.json"
    if combined_hc.exists():
        emit(f"  DB/manifests/huntcards/all-huntcards.json - {file_size(combined_hc):,} bytes (ALL)")
