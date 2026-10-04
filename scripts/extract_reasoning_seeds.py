#!/usr/bin/env python3
"""
Reasoning Seed Extractor
========================
Turns hunt cards (grep_prune output or all-huntcards.json) into generalized
assumption seeds for `protocol-reasoning` Phase A. This makes DB-seed loading
a one-command, deterministic step instead of per-run prose.

Usage:
    python3 scripts/extract_reasoning_seeds.py <hunt-card-hits.json|all-huntcards.json> [options]

Options:
    --output <path>    Output path (default: audit-output/reasoning-seeds.md)

Input formats accepted:
    - grep_prune.py output: {"hits": [cards...]} (surviving cards only)
    - DB/manifests/huntcards/all-huntcards.json: {"cards": [cards...]}

Each card's `detect` field is mapped through a canonical assumption-rule table
(5 layers: Input, State, Ordering, Economic, Environmental). Cards matching no
rule keep their `detect` text verbatim with a best-effort layer. Identical
(layer, seed) pairs merge with all source cards cited.
"""

import argparse
import json
import os
import re
import sys

LAYER_NAMES = [
    ("Input", "I"),
    ("State", "S"),
    ("Ordering", "O"),
    ("Economic", "E"),
    ("Environmental", "V"),
]

# (regex on detect+check text, layer, canonical generalized assumption)
# First matching rule wins; rules are evaluated in listed order.
ASSUMPTION_RULES = [
    (re.compile(r"oracle|chainlink|pyth|price.?feed|latestRoundData|updatedAt|staleness|stale|twap|\bfeed\b", re.I),
     "Input", "External data consumed without temporal validation"),
    (re.compile(r"calldata|user.?input|unvalidated|arbitrary (call|input|address)|signature|permit|callback payload", re.I),
     "Input", "Unvalidated external input reaches state-changing logic"),
    (re.compile(r"share|ratio|denominator|accumulat|snapshot|accounting|precision|rounding|first depositor|inflation attack", re.I),
     "State", "Share/asset accounting breaks when denominators approach zero or round adversarially"),
    (re.compile(r"reentr|external call .*(before|prior)|callback|hook|\bCEI\b|state (update|change)d? after", re.I),
     "Ordering", "State updated after external call"),
    (re.compile(r"flash.?loan|caller.?s? balance|\bmev\b|sandwich|slippage|reward|incentive|\bfee\b|manipulat", re.I),
     "Economic", "Function behavior scales with caller's balance"),
    (re.compile(r"\beoa\b|chainid|chain id|block number|blockhash|timestamp|\bgas\b|\bfork\b|randomness|\brandom\b", re.I),
     "Environmental", "Contract assumes environmental properties it cannot enforce"),
]

# Fallback layer guess for cards matching no canonical rule.
FALLBACK_LAYER_KEYWORDS = [
    (re.compile(r"owner|admin|role|access|auth|privileg", re.I), "State"),
    (re.compile(r"profit|cost|capital|liquidit|arbitrage|price", re.I), "Economic"),
    (re.compile(r"call|invoke|execute|bridge|message", re.I), "Ordering"),
    (re.compile(r"input|parameter|argument|data", re.I), "Input"),
    (re.compile(r"time|delay|deadline|window", re.I), "Environmental"),
]


def classify(detect_text, check_text):
    """Return (layer, canonical_seed) for a card's detect+check text."""
    text = f"{detect_text} {check_text}"
    for rule, layer, canonical in ASSUMPTION_RULES:
        if rule.search(text):
            return layer, canonical
    for rule, layer in FALLBACK_LAYER_KEYWORDS:
        if rule.search(text):
            return layer, detect_text.strip()
    return "State", detect_text.strip()


def load_cards(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data.get("hits"), list):
        return data["hits"], len(data.get("hits", []))
    if isinstance(data.get("cards"), list):
        return data["cards"], len(data["cards"])
    raise ValueError(f"{path}: expected 'hits' or 'cards' list")


def _as_text(value):
    """Coerce a card field that may be a string or a list of strings."""
    if isinstance(value, list):
        return "; ".join(str(v) for v in value if v).strip()
    return str(value or "").strip()


def build_seeds(cards):
    """Group cards into deduplicated (layer, seed) buckets with sources."""
    merged = {}
    order = []
    raw_count = 0
    for card in cards:
        if not isinstance(card, dict):
            continue
        detect = _as_text(card.get("detect"))
        check = _as_text(card.get("check"))
        if not detect and not check:
            continue
        raw_count += 1
        layer, seed = classify(detect, check)
        key = (layer, seed.lower())
        if key not in merged:
            merged[key] = {
                "layer": layer,
                "seed": seed,
                "verify": check or detect,
                "sources": [],
            }
            order.append(key)
        merged[key]["sources"].append((card.get("id", "?"), card.get("ref", "")))
    return [merged[k] for k in order], raw_count


def main():
    parser = argparse.ArgumentParser(description="Extract reasoning seeds from hunt cards")
    parser.add_argument("huntcards", help="grep_prune hits JSON or all-huntcards.json")
    parser.add_argument("--output", default="audit-output/reasoning-seeds.md")
    args = parser.parse_args()

    if not os.path.isfile(args.huntcards):
        print(f"Error: '{args.huntcards}' not found", file=sys.stderr)
        sys.exit(1)

    try:
        cards, total = load_cards(args.huntcards)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    seeds, raw_count = build_seeds(cards)

    counters = {code: 0 for _, code in LAYER_NAMES}
    lines = [
        "# Reasoning Seeds",
        "",
        f"> Generated by `scripts/extract_reasoning_seeds.py` from `{args.huntcards}`",
        f"> Cards: {total} — seeds: {len(seeds)} (deduplicated from {raw_count} card-level matches)",
    ]
    if not seeds:
        lines.append(">")
        lines.append("> **ZERO seeds extracted** — protocol-reasoning Phase A must log this in")
        lines.append("> memory-state and proceed with memory HYPOTHESIS seeds only. Do not")
        lines.append("> silently reason without seeds.")
    lines += ["", "## Reasoning Seed Catalog", ""]

    for layer, code in LAYER_NAMES:
        layer_seeds = [s for s in seeds if s["layer"] == layer]
        lines.append(f"### {layer} Seeds")
        if not layer_seeds:
            lines.append("")
            lines.append(f"_(no {layer.lower()}-layer seeds from this corpus)_")
            lines.append("")
            continue
        for seed in layer_seeds:
            counters[code] += 1
            sid = f"SEED-{code}-{counters[code]:03d}"
            lines.append(f"- **{sid}** — {seed['seed']}")
            lines.append(f"  - verify: {seed['verify']}")
            src = ", ".join(f"`{cid}`{f' ({ref})' if ref else ''}" for cid, ref in seed["sources"][:6])
            more = "" if len(seed["sources"]) <= 6 else f" +{len(seed['sources']) - 6} more"
            lines.append(f"  - sources: {src}{more}")
        lines.append("")

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Extracted {len(seeds)} seeds from {raw_count} card matches ({total} cards in input)")
    for layer, _ in LAYER_NAMES:
        n = sum(1 for s in seeds if s["layer"] == layer)
        print(f"  {layer}: {n}")
    print(f"Written: {args.output}")


if __name__ == "__main__":
    main()
