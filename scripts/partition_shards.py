#!/usr/bin/env python3
"""
Partition Hunt Cards into Shards for Parallel Fan-Out
=====================================================
Takes grep-pruned hunt card hits and partitions into shards of 50-80 cards,
grouped by category tag. neverPrune cards are separated as a critical set
to be duplicated into every regular shard. If only neverPrune cards survive,
the output includes a critical-only shard so the safety-net review still runs.

Usage:
    python3 scripts/partition_shards.py <hunt_card_hits_json> [options]

Options:
    --max-shard-size N   Maximum cards per shard (default: 80)
    --min-group-size N   Minimum cards before merging groups (default: 20)
    --output <path>      Output path (default: audit-output/hunt-card-shards.json)
    --scope-file <path>  00-scope.md whose Machine-Readable Scope block drops
                         hits outside the in-scope set (default: none)

With --scope-file, each card's grepHits are filtered to in-scope files; cards
whose hits are all out of scope (and that are neither neverPrune nor carrying
a searchError) are dropped before partitioning.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from horus_retrieval.scope import build_matcher, filter_file_scope, load_scope_block
from horus_retrieval.sharding import partition_hunt_cards


def partition(hits, max_shard_size=80, min_group_size=20):
    """Partition surviving cards into shards by category tag."""
    return partition_hunt_cards(hits, max_shard_size, min_group_size)


def main():
    parser = argparse.ArgumentParser(description="Partition hunt cards into shards")
    parser.add_argument("hunt_card_hits", help="Path to hunt-card-hits.json")
    parser.add_argument("--max-shard-size", type=int, default=80)
    parser.add_argument("--min-group-size", type=int, default=20)
    parser.add_argument("--output", default="audit-output/hunt-card-shards.json")
    parser.add_argument("--scope-file", default=None,
                        help="00-scope.md whose Machine-Readable Scope block drops out-of-scope hits")
    args = parser.parse_args()

    if not os.path.isfile(args.hunt_card_hits):
        print(f"Error: '{args.hunt_card_hits}' not found", file=sys.stderr)
        sys.exit(1)

    scope_matches = None
    if args.scope_file:
        if not os.path.isfile(args.scope_file):
            print(f"Error: Scope file '{args.scope_file}' not found", file=sys.stderr)
            sys.exit(1)
        try:
            scope_matches = build_matcher(load_scope_block(args.scope_file))
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

    with open(args.hunt_card_hits, "r", encoding="utf-8") as f:
        data = json.load(f)

    hits = data.get("hits", [])
    target_path = data.get("targetPath") or "."

    scope_dropped = 0
    if scope_matches is not None:
        kept_hits = []
        for card in hits:
            grep_hits = card.get("grepHits") or []
            if not grep_hits:
                kept_hits.append(card)
                continue
            kept = [
                hit for hit in grep_hits
                if filter_file_scope(hit.rsplit(":", 1)[0], target_path, scope_matches)
            ]
            card = dict(card, grepHits=kept)
            if kept or card.get("neverPrune") or card.get("searchError"):
                kept_hits.append(card)
            else:
                scope_dropped += 1
        hits = kept_hits
        print(f"Scope: {args.scope_file} dropped {scope_dropped} all-out-of-scope cards")

    shards, critical = partition(hits, args.max_shard_size, args.min_group_size)

    output = {
        "totalSurvivingCards": len(hits),
        "criticalCards": len(critical),
        "criticalCardIds": [c["id"] for c in critical],
        "criticalSet": critical,
        "shardCount": len(shards),
        "scopeFile": args.scope_file,
        "scopeDroppedCards": scope_dropped,
        "shards": shards,
    }

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    total_in_shards = sum(s["cardCount"] for s in shards)
    print(f"Partitioned {len(hits)} cards into {len(shards)} shards:")
    for s in shards:
        print(f"  {s['id']}: {s['cardCount']} cards, cats={s['categories']}")
    print(f"  + {len(critical)} critical (neverPrune) cards → duplicated to every shard")
    print(f"Written: {args.output}")


if __name__ == "__main__":
    main()
