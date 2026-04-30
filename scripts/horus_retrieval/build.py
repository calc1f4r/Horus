"""Retrieval build orchestration for Horus generated artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .bundles import build_partition_bundles
from .enrichment import enrich_huntcards
from .huntcards import build_all_huntcards
from .keywords import build_quick_keywords
from .manifests import (
    build_general_sub_manifests,
    build_manifest,
)
from .router import add_audit_checklist, add_protocol_context, build_lean_router
from .taxonomy import CATEGORY_MAP
from .writers import emit_artifact_summary, file_size, write_json, write_router_index


DEFAULT_DB_DIR = Path(__file__).resolve().parents[2] / "DB"
DEFAULT_MANIFEST_DIR = DEFAULT_DB_DIR / "manifests"
DEFAULT_HUNTCARDS_DIR = DEFAULT_MANIFEST_DIR / "huntcards"


@dataclass(frozen=True)
class RetrievalBuildDeps:
    build_manifest: Callable
    build_general_sub_manifests: Callable
    build_lean_router: Callable
    add_protocol_context: Callable
    add_audit_checklist: Callable
    build_quick_keywords: Callable
    build_all_huntcards: Callable
    build_partition_bundles: Callable


@dataclass(frozen=True)
class RetrievalBuildResult:
    manifests: dict
    router: dict
    keywords: dict
    total_huntcards: int


def standard_build_deps(
    *,
    db_dir: Path = DEFAULT_DB_DIR,
    manifest_dir: Path = DEFAULT_MANIFEST_DIR,
    huntcards_dir: Path = DEFAULT_HUNTCARDS_DIR,
    emit: Callable[[str], None] = print,
) -> RetrievalBuildDeps:
    """Create the standard retrieval-build dependency bundle for the repo DB."""
    return RetrievalBuildDeps(
        build_manifest=lambda category, folders: build_manifest(category, folders, db_root=db_dir),
        build_general_sub_manifests=lambda: build_general_sub_manifests(db_root=db_dir),
        build_lean_router=build_lean_router,
        add_protocol_context=add_protocol_context,
        add_audit_checklist=add_audit_checklist,
        build_quick_keywords=build_quick_keywords,
        build_all_huntcards=lambda manifests: build_all_huntcards(
            manifests,
            huntcards_dir=huntcards_dir,
            db_root=db_dir,
            emit=emit,
        ),
        build_partition_bundles=lambda manifests: build_partition_bundles(
            manifests,
            huntcards_dir=huntcards_dir,
            bundles_dir=manifest_dir / "bundles",
            emit=emit,
        ),
    )


def build_retrieval_db(
    *,
    db_dir: Path = DEFAULT_DB_DIR,
    manifest_dir: Path | None = None,
    huntcards_dir: Path | None = None,
    category_map: dict | None = None,
    deps: RetrievalBuildDeps | None = None,
    enrich: bool = True,
    build_bundles: bool = True,
    emit: Callable[[str], None] = print,
) -> RetrievalBuildResult:
    manifest_dir = manifest_dir or db_dir / "manifests"
    huntcards_dir = huntcards_dir or manifest_dir / "huntcards"
    category_map = category_map or CATEGORY_MAP
    deps = deps or standard_build_deps(
        db_dir=db_dir,
        manifest_dir=manifest_dir,
        huntcards_dir=huntcards_dir,
        emit=emit,
    )
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifests = {}

    emit("=" * 60)
    emit("Horus Manifest Generator")
    emit("=" * 60)

    for category, folders in category_map.items():
        if category == "general":
            emit("\n📁 Processing category: general (split into sub-manifests)")
            sub_manifests = deps.build_general_sub_manifests()
            for sub_name, sub_manifest in sub_manifests.items():
                manifests[sub_name] = sub_manifest
                manifest_path = manifest_dir / f"{sub_name}.json"
                write_json(manifest_path, sub_manifest)
                emit(f"   → {sub_name}: {sub_manifest['meta']['fileCount']} files, {sub_manifest['meta']['totalPatterns']} patterns")
            continue

        emit(f"\n📁 Processing category: {category}")
        manifest = deps.build_manifest(category, folders)
        manifests[category] = manifest

        manifest_path = manifest_dir / f"{category}.json"
        write_json(manifest_path, manifest)

        emit(f"   → {manifest['meta']['fileCount']} files, {manifest['meta']['totalPatterns']} patterns")
        emit(f"   → Written to {manifest_path}")

    emit("\n📋 Building lean router index...")
    router = deps.build_lean_router(manifests)
    deps.add_protocol_context(router)
    deps.add_audit_checklist(router)

    keywords_data = deps.build_quick_keywords(manifests)
    keywords_path = manifest_dir / "keywords.json"
    write_json(keywords_path, keywords_data)
    keywords_size = file_size(keywords_path)
    emit(f"   → Keywords index: {keywords_size:,} bytes ({keywords_data['totalKeywords']} keywords)")
    emit(f"   → Written to {keywords_path}")

    router["keywordIndex"] = {
        "file": "DB/manifests/keywords.json",
        "description": "Keyword → manifest routing. Load this file only when doing keyword-based search.",
        "totalKeywords": keywords_data["totalKeywords"],
    }

    emit("\n🎯 Building hunt cards (Tier 1.5)...")
    huntcard_info, total_huntcards = deps.build_all_huntcards(manifests)

    if enrich:
        enrich_huntcards(huntcards_dir, manifests, emit)

    if build_bundles:
        emit("\n📦 Building partition bundles for parallel fan-out...")
        deps.build_partition_bundles(manifests)

    router["huntcards"] = {
        "description": "Enriched detection cards with grep patterns, micro-directives (check steps, antipattern, securePattern), triage context (validWhen, invalidWhen, impact), and optional reportEvidence/graphHints/proofShape fields. Load all-huntcards.json for ALL patterns. For each card: grep target code → on hit, execute card.check steps directly → use triage context to filter weak matches → only read .md for confirmed positives.",
        "allInOne": "DB/manifests/huntcards/all-huntcards.json",
        "totalCards": total_huntcards,
        "perManifest": huntcard_info,
    }

    write_router_index(db_dir, router, emit)
    emit_artifact_summary(
        manifests=manifests,
        manifest_dir=manifest_dir,
        huntcards_dir=huntcards_dir,
        total_huntcards=total_huntcards,
        emit=emit,
    )

    return RetrievalBuildResult(
        manifests=manifests,
        router=router,
        keywords=keywords_data,
        total_huntcards=total_huntcards,
    )
