"""Partition bundle builders for graph-aware hunt-card fan-out."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Callable

from .protocol_context import bundle_manifest_mapping
from .sharding import partition_hunt_cards
from .taxonomy import GENERAL_SUBCATEGORIES


DEFAULT_DB_DIR = Path(__file__).resolve().parents[2] / "DB"
DEFAULT_MANIFEST_DIR = DEFAULT_DB_DIR / "manifests"
DEFAULT_HUNTCARDS_DIR = DEFAULT_MANIFEST_DIR / "huntcards"
DEFAULT_BUNDLES_DIR = DEFAULT_MANIFEST_DIR / "bundles"


def _manifest_key_for_card(card, general_subcategories):
    ref_parts = card.get("ref", "").split("/")
    if len(ref_parts) < 2:
        return None

    manifest_key = ref_parts[1]
    if manifest_key == "general" and len(ref_parts) >= 3:
        subfolder = ref_parts[2]
        for sub_name, sub_config in general_subcategories.items():
            if subfolder in sub_config["folders"]:
                return sub_name
    return manifest_key


def cards_by_manifest_from_huntcards(all_huntcards, *, general_subcategories=GENERAL_SUBCATEGORIES):
    cards_by_manifest = defaultdict(list)
    for card in all_huntcards["cards"]:
        manifest_key = _manifest_key_for_card(card, general_subcategories)
        if manifest_key:
            cards_by_manifest[manifest_key].append(card)
    return cards_by_manifest


def build_protocol_bundle(protocol_name, manifest_list, cards_by_manifest, *, max_shard_size=80, min_group_size=20):
    protocol_cards = []
    seen_ids = set()
    for manifest_name in manifest_list:
        for card in cards_by_manifest.get(manifest_name, []):
            if card["id"] not in seen_ids:
                protocol_cards.append(card)
                seen_ids.add(card["id"])

    if not protocol_cards:
        return None

    shards, critical_cards = partition_hunt_cards(
        protocol_cards,
        max_shard_size=max_shard_size,
        min_group_size=min_group_size,
    )

    return {
        "meta": {
            "protocol": protocol_name,
            "description": f"Pre-computed shard partition for {protocol_name} audits",
            "totalCards": len(protocol_cards),
            "criticalCards": len(critical_cards),
            "shardCount": len(shards),
            "criticalCardIds": [c["id"] for c in critical_cards],
            "usage": (
                "Load this file to get pre-computed shards for parallel fan-out. "
                "Each shard is assigned to one sub-agent. Critical cards (neverPrune) "
                "must be appended to every shard at spawn time."
            ),
        },
        "shards": shards,
    }


def build_partition_bundles(
    manifests,
    *,
    huntcards_dir=DEFAULT_HUNTCARDS_DIR,
    bundles_dir=DEFAULT_BUNDLES_DIR,
    protocol_mappings=None,
    emit: Callable[[str], None] = print,
):
    """Generate pre-computed shard partition bundles for protocol-context mappings."""
    bundles_dir.mkdir(parents=True, exist_ok=True)

    all_hc_path = huntcards_dir / "all-huntcards.json"
    if not all_hc_path.exists():
        emit("   ⚠ all-huntcards.json not found, skipping partition bundles")
        return None

    with all_hc_path.open("r", encoding="utf-8") as f:
        all_huntcards = json.load(f)

    cards_by_manifest = cards_by_manifest_from_huntcards(all_huntcards)
    protocol_mappings = protocol_mappings or bundle_manifest_mapping()

    for protocol_name, manifest_list in protocol_mappings.items():
        bundle = build_protocol_bundle(protocol_name, manifest_list, cards_by_manifest)
        if not bundle:
            continue

        bundle_path = bundles_dir / f"{protocol_name}-shards.json"
        with bundle_path.open("w", encoding="utf-8") as f:
            json.dump(bundle, f, indent=2, ensure_ascii=False)

        total_shard_cards = sum(s["cardCount"] for s in bundle["shards"])
        emit(
            f"   → {protocol_name}: {len(bundle['shards'])} shards, "
            f"{total_shard_cards} regular + {bundle['meta']['criticalCards']} critical cards"
        )

    return True
