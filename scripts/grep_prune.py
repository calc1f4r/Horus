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
    --language sol|rs|go|move|cairo|vy|all
                               File extension filter (default: auto-detect)
    --output <path>            Output path (default: audit-output/hunt-card-hits.json)

Output: hunt-card-hits.json with surviving cards + grep hit locations.
Cards whose search command errors are retained with `searchError` for manual
review instead of being silently pruned.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


LANGUAGE_PATTERNS = {
    "sol": "*.sol",
    "rs": "*.rs",
    "go": "*.go",
    "move": "*.move",
    "cairo": "*.cairo",
    "vy": "*.vy",
}


def detect_language(target_path):
    """Auto-detect primary language from file extensions."""
    ext_counts = {}
    tracked_exts = {pattern.replace("*", "") for pattern in LANGUAGE_PATTERNS.values()}
    for root, _, files in os.walk(target_path):
        # Skip common non-source dirs
        if any(skip in root for skip in ["/node_modules/", "/lib/", "/.git/", "/test/", "/tests/"]):
            continue
        for f in files:
            ext = Path(f).suffix
            if ext in tracked_exts:
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
    if not ext_counts:
        return list(LANGUAGE_PATTERNS.values())
    # Return top extensions
    sorted_exts = sorted(ext_counts.items(), key=lambda x: -x[1])
    return [f"*{ext}" for ext, _ in sorted_exts[:2]]


def build_search_command(grep_pattern, target_path, include_patterns):
    """Build a regex-capable search command, preferring ripgrep when available."""
    rg_path = shutil.which("rg")
    if rg_path:
        command = [rg_path, "-n", "-e", grep_pattern]
        for pat in include_patterns:
            command.extend(["-g", pat])
        command.append(target_path)
        return command

    command = ["grep", "-Ern", grep_pattern, target_path]
    for pat in include_patterns:
        command.extend(["--include", pat])
    return command


def grep_card(card, target_path, include_patterns):
    """Run grep for a single card's pattern. Returns list of file:line hits."""
    return search_card(card, target_path, include_patterns)["hits"]


def search_card(card, target_path, include_patterns):
    """Run grep for a card and return hit locations plus any execution error."""
    grep_pattern = card.get("grep", "")
    if not grep_pattern:
        return {"hits": [], "error": None}

    try:
        result = subprocess.run(
            build_search_command(grep_pattern, target_path, include_patterns),
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            hits = []
            for line in result.stdout.strip().split("\n")[:20]:  # Cap at 20 hits per card
                # Format: file:line:content → keep file:line
                parts = line.split(":", 2)
                if len(parts) >= 2:
                    hits.append(f"{parts[0]}:{parts[1]}")
            return {"hits": hits, "error": None}
        if result.returncode in (0, 1):
            return {"hits": [], "error": None}
        detail = result.stderr.strip() or result.stdout.strip() or f"search exited with {result.returncode}"
        return {"hits": [], "error": detail}
    except subprocess.TimeoutExpired:
        return {"hits": [], "error": "search timed out after 10 seconds"}
    except FileNotFoundError as exc:
        return {"hits": [], "error": str(exc)}


def main():
    parser = argparse.ArgumentParser(description="Grep-prune hunt cards against a target codebase")
    parser.add_argument("target_path", help="Path to the target codebase")
    parser.add_argument("huntcards_json", help="Path to hunt cards JSON file")
    parser.add_argument("--language", choices=[*LANGUAGE_PATTERNS, "all"], default=None,
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
        include_patterns = list(LANGUAGE_PATTERNS.values())
    elif args.language:
        include_patterns = [LANGUAGE_PATTERNS[args.language]]
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
    search_error_count = 0

    for i, card in enumerate(cards):
        card_id = card.get("id", f"unknown-{i}")
        is_never_prune = card.get("neverPrune", False)

        search_result = search_card(card, args.target_path, include_patterns)
        hits = search_result["hits"]
        search_error = search_result["error"]

        if hits or is_never_prune or search_error:
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
            for field in [
                "grep",
                "detect",
                "check",
                "antipattern",
                "securePattern",
                "validWhen",
                "invalidWhen",
                "impact",
                "cat",
            ]:
                if field in card:
                    entry[field] = card[field]
            if search_error:
                entry["searchError"] = search_error
                search_error_count += 1
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
        "searchErrorCards": search_error_count,
        "targetPath": args.target_path,
        "fileFilter": include_patterns,
        "hits": surviving,
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nResults:")
    print(f"  Surviving: {len(surviving)} cards ({never_prune_count} via neverPrune)")
    if search_error_count:
        print(f"  Search errors: {search_error_count} cards kept for manual review")
    print(f"  Pruned:    {pruned} cards")
    print(f"  Written:   {args.output}")


if __name__ == "__main__":
    main()
