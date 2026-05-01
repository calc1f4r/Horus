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
"""

import argparse
import json
import os
import sys

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
    args = parser.parse_args()

    if not os.path.isfile(args.hunt_card_hits):
        print(f"Error: '{args.hunt_card_hits}' not found", file=sys.stderr)
        sys.exit(1)

    with open(args.hunt_card_hits, "r", encoding="utf-8") as f:
        data = json.load(f)

    hits = data.get("hits", [])
    shards, critical = partition(hits, args.max_shard_size, args.min_group_size)

    output = {
        "totalSurvivingCards": len(hits),
        "criticalCards": len(critical),
        "criticalCardIds": [c["id"] for c in critical],
        "criticalSet": critical,
        "shardCount": len(shards),
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
