#!/usr/bin/env python3
"""
Grep-Prune Utility for Hunt Card Scanning
==========================================
Runs each hunt card's grep pattern against a target codebase, recording
which cards have hits and at which file:line locations. Cards with zero
hits are pruned. Cards with neverPrune=true always survive.

Usage:
    python3 scripts/grep_prune.py <target_path> <huntcards_json> [options]

Options:
    --language sol|rs|go|all   File extension filter (default: auto-detect)
    --output <path>            Output path (default: audit-output/hunt-card-hits.json)

Output: hunt-card-hits.json with surviving cards + grep hit locations.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def detect_language(target_path):
    """Auto-detect primary language from file extensions."""
    ext_counts = {}
    for root, _, files in os.walk(target_path):
        # Skip common non-source dirs
        if any(skip in root for skip in ["/node_modules/", "/lib/", "/.git/", "/test/", "/tests/"]):
            continue
        for f in files:
            ext = Path(f).suffix
            if ext in {".sol", ".rs", ".go", ".move"}:
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
    if not ext_counts:
        return ["*.sol", "*.rs", "*.go"]  # fallback: all
    # Return top extensions
    sorted_exts = sorted(ext_counts.items(), key=lambda x: -x[1])
    return [f"*{ext}" for ext, _ in sorted_exts[:2]]


def grep_card(card, target_path, include_patterns):
    """Run grep for a single card's pattern. Returns list of file:line hits."""
    grep_pattern = card.get("grep", "")
    if not grep_pattern:
        return []

    include_args = []
    for pat in include_patterns:
        include_args.extend(["--include", pat])

    try:
        result = subprocess.run(
            ["grep", "-rn", grep_pattern, target_path] + include_args,
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            hits = []
            for line in result.stdout.strip().split("\n")[:20]:  # Cap at 20 hits per card
                # Format: file:line:content → keep file:line
                parts = line.split(":", 2)
                if len(parts) >= 2:
                    hits.append(f"{parts[0]}:{parts[1]}")
            return hits
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return []


def main():
    parser = argparse.ArgumentParser(description="Grep-prune hunt cards against a target codebase")
    parser.add_argument("target_path", help="Path to the target codebase")
    parser.add_argument("huntcards_json", help="Path to hunt cards JSON file")
    parser.add_argument("--language", choices=["sol", "rs", "go", "all"], default=None,
                        help="File extension filter (default: auto-detect)")
    parser.add_argument("--output", default="audit-output/hunt-card-hits.json",
                        help="Output path (default: audit-output/hunt-card-hits.json)")
    args = parser.parse_args()

    # Validate inputs
    if not os.path.isdir(args.target_path):
        print(f"Error: Target path '{args.target_path}' is not a directory", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(args.huntcards_json):
        print(f"Error: Hunt cards file '{args.huntcards_json}' not found", file=sys.stderr)
        sys.exit(1)

    # Determine file extensions
    if args.language == "all":
        include_patterns = ["*.sol", "*.rs", "*.go", "*.move"]
    elif args.language:
        include_patterns = [f"*.{args.language}"]
    else:
        include_patterns = detect_language(args.target_path)

    print(f"Target: {args.target_path}")
    print(f"File filter: {', '.join(include_patterns)}")

    # Load hunt cards
    with open(args.huntcards_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    cards = data.get("cards", [])
    print(f"Cards loaded: {len(cards)}")

    # Grep-prune
    surviving = []
    pruned = 0
    never_prune_count = 0

    for i, card in enumerate(cards):
        card_id = card.get("id", f"unknown-{i}")
        is_never_prune = card.get("neverPrune", False)

        hits = grep_card(card, args.target_path, include_patterns)

        if hits or is_never_prune:
            entry = {
                "id": card_id,
                "title": card.get("title", ""),
                "severity": card.get("severity", "UNKNOWN"),
                "ref": card.get("ref", ""),
                "lines": card.get("lines", []),
                "grepHits": hits,
                "neverPrune": is_never_prune,
            }
            # Carry through micro-directive fields
            for field in ["grep", "detect", "check", "antipattern", "securePattern", "cat"]:
                if field in card:
                    entry[field] = card[field]
            surviving.append(entry)
            if is_never_prune and not hits:
                never_prune_count += 1
        else:
            pruned += 1

        # Progress
        if (i + 1) % 50 == 0:
            print(f"  Processed {i + 1}/{len(cards)}...")

    # Write output
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    output = {
        "totalCards": len(cards),
        "survivingCards": len(surviving),
        "prunedCards": pruned,
        "neverPruneCards": never_prune_count,
        "targetPath": args.target_path,
        "fileFilter": include_patterns,
        "hits": surviving,
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nResults:")
    print(f"  Surviving: {len(surviving)} cards ({never_prune_count} via neverPrune)")
    print(f"  Pruned:    {pruned} cards")
    print(f"  Written:   {args.output}")


if __name__ == "__main__":
    main()
