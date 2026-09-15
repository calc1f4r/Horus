"""Shared hunt-card sharding logic for runtime scans and prebuilt bundles."""

from __future__ import annotations

from collections import defaultdict


def partition_hunt_cards(hits, max_shard_size=80, min_group_size=20):
    """Partition cards by category while preserving critical cards for every shard."""
    critical = [h for h in hits if h.get("neverPrune", False)]
    regular = [h for h in hits if not h.get("neverPrune", False)]
    critical_ids = [c["id"] for c in critical]

    groups = defaultdict(list)
    for card in regular:
        cats = card.get("cat", ["general"])
        primary = cats[0] if cats else "general"
        groups[primary].append(card)

    shards = []
    small_groups = []

    def append_shard(shard_id, cards, categories):
        shards.append(
            {
                "id": shard_id,
                "cardCount": len(cards),
                "regularCardCount": len(cards),
                "criticalCardCount": len(critical),
                "effectiveCardCount": len(cards) + len(critical),
                "categories": categories,
                "cardIds": [c["id"] for c in cards],
                "criticalCardIds": critical_ids,
            }
        )

    for cat_name, cards in sorted(groups.items(), key=lambda x: -len(x[1])):
        if len(cards) > max_shard_size:
            for i in range(0, len(cards), 60):
                chunk = cards[i:i + 60]
                suffix = f"-{i // 60 + 1}" if len(cards) > 60 else ""
                append_shard(f"shard-{len(shards) + 1}-{cat_name}{suffix}", chunk, [cat_name])
        elif len(cards) < min_group_size:
            small_groups.append((cat_name, cards))
        else:
            append_shard(f"shard-{len(shards) + 1}-{cat_name}", cards, [cat_name])

    if small_groups:
        merged_cards, merged_cats = [], []
        for cat_name, cards in small_groups:
            merged_cards.extend(cards)
            merged_cats.append(cat_name)
            if len(merged_cards) >= 50:
                append_shard(
                    f"shard-{len(shards) + 1}-{'_'.join(merged_cats[:3])}",
                    merged_cards,
                    merged_cats[:],
                )
                merged_cards, merged_cats = [], []
        if merged_cards:
            if shards and len(merged_cards) < 15:
                shards[-1]["cardCount"] += len(merged_cards)
                shards[-1]["regularCardCount"] += len(merged_cards)
                shards[-1]["effectiveCardCount"] += len(merged_cards)
                shards[-1]["categories"].extend(merged_cats)
                shards[-1]["cardIds"].extend([c["id"] for c in merged_cards])
            else:
                append_shard(f"shard-{len(shards) + 1}-misc", merged_cards, merged_cats)

    if critical and not shards:
        append_shard("shard-1-critical", critical, ["critical"])
        shards[-1]["criticalOnly"] = True

    return shards, critical
