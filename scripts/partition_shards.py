#!/usr/bin/env python3
"""
Partition Hunt Cards into Shards for Parallel Fan-Out
=====================================================
Takes grep-pruned hunt card hits and partitions into shards of 50-80 cards,
grouped by category tag. neverPrune cards are separated as a critical set
to be duplicated into every shard.

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
from collections import defaultdict


def partition(hits, max_shard_size=80, min_group_size=20):
    """Partition surviving cards into shards by category tag."""
    # Separate critical (neverPrune) cards
    critical = [h for h in hits if h.get("neverPrune", False)]
    regular = [h for h in hits if not h.get("neverPrune", False)]

    # Group by primary cat tag
    groups = defaultdict(list)
    for card in regular:
        cats = card.get("cat", ["general"])
        primary = cats[0] if cats else "general"
        groups[primary].append(card)

    shards = []
    small_groups = []

    for cat_name, cards in sorted(groups.items(), key=lambda x: -len(x[1])):
        if len(cards) > max_shard_size:
            # Split large groups
            for i in range(0, len(cards), 60):
                chunk = cards[i:i + 60]
                suffix = f"-{i // 60 + 1}" if len(cards) > 60 else ""
                shards.append({
                    "id": f"shard-{len(shards) + 1}-{cat_name}{suffix}",
                    "cardCount": len(chunk),
                    "categories": [cat_name],
                    "cardIds": [c["id"] for c in chunk],
                })
        elif len(cards) < min_group_size:
            small_groups.append((cat_name, cards))
        else:
            shards.append({
                "id": f"shard-{len(shards) + 1}-{cat_name}",
                "cardCount": len(cards),
                "categories": [cat_name],
                "cardIds": [c["id"] for c in cards],
            })

    # Merge small groups
    if small_groups:
        merged_cards, merged_cats = [], []
        for cat_name, cards in small_groups:
            merged_cards.extend(cards)
            merged_cats.append(cat_name)
            if len(merged_cards) >= 50:
                shards.append({
                    "id": f"shard-{len(shards) + 1}-{'_'.join(merged_cats[:3])}",
                    "cardCount": len(merged_cards),
                    "categories": merged_cats[:],
                    "cardIds": [c["id"] for c in merged_cards],
                })
                merged_cards, merged_cats = [], []
        if merged_cards:
            if shards and len(merged_cards) < 15:
                shards[-1]["cardCount"] += len(merged_cards)
                shards[-1]["categories"].extend(merged_cats)
                shards[-1]["cardIds"].extend([c["id"] for c in merged_cards])
            else:
                shards.append({
                    "id": f"shard-{len(shards) + 1}-misc",
                    "cardCount": len(merged_cards),
                    "categories": merged_cats,
                    "cardIds": [c["id"] for c in merged_cards],
                })

    return shards, critical


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
