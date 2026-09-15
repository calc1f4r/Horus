"""Hunt-card enrichment integration for retrieval builds."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from .writers import file_size, write_json


def enrich_huntcards(huntcards_dir: Path, manifests: dict, emit: Callable[[str], None]) -> None:
    """Run micro-directive enrichment over per-manifest hunt-card files."""
    emit("\n🔬 Enriching hunt cards with micro-directives...")
    try:
        from generate_micro_directives import enrich_huntcard_file

        total_enriched = 0
        all_enriched_cards = []
        for hc_file in sorted(huntcards_dir.glob("*-huntcards.json")):
            if hc_file.name == "all-huntcards.json":
                continue
            stats = enrich_huntcard_file(hc_file, hc_file)
            total_enriched += stats["enriched"]
            with hc_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                all_enriched_cards.extend(data["cards"])
            emit(f"   → {hc_file.name}: {stats['enriched']}/{stats['total']} enriched")

        combined = {
            "meta": {
                "description": "ALL enriched hunt cards — compressed detection rules with verification and triage context for direct bug validation",
                "totalCards": len(all_enriched_cards),
                "enriched": total_enriched,
                "manifests": list(sorted(manifests.keys())),
                "usage": (
                    "Load this single file for all vulnerability detection cards. For each card: "
                    "grep target code for card.grep. On hit: execute card.check steps directly against "
                    "grep hit locations, use validWhen/invalidWhen/impact for rapid triage, and only read "
                    "full DB entry (card.ref + card.lines) for confirmed true/likely positives."
                ),
            },
            "cards": all_enriched_cards,
        }
        combined_path = huntcards_dir / "all-huntcards.json"
        write_json(combined_path, combined)
        combined_size = file_size(combined_path)
        emit(f"   → all-huntcards.json: {len(all_enriched_cards)} cards, {combined_size:,} bytes (enriched)")
    except ImportError:
        emit("   ⚠ Skipping enrichment (scripts/generate_micro_directives.py not found)")
    except Exception as exc:
        emit(f"   ⚠ Enrichment failed: {exc}")
