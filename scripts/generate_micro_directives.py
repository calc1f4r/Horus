#!/usr/bin/env python3
"""
Micro-Directive Extractor
=========================
Enriches hunt cards with structured `check`, `antipattern`, and `securePattern`
fields extracted from the referenced .md vulnerability entries.

Agents can execute micro-directives directly against grep hit locations
without reading the full .md file — cutting context usage by 60-80%.

Usage:
    python3 scripts/generate_micro_directives.py                  # Enrich all hunt cards
    python3 scripts/generate_micro_directives.py --dry-run --sample 10  # Preview 10 random cards
    python3 scripts/generate_micro_directives.py --validate       # Validate enriched cards
"""

import argparse
import json
import os
import random
import re
import sys
from pathlib import Path

# Resolve paths relative to repo root
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DB_DIR = REPO_ROOT / "DB"
HUNTCARDS_DIR = DB_DIR / "manifests" / "huntcards"


# ─── Extraction helpers ───


def _read_section(file_path: str, line_start: int, line_end: int) -> list[str]:
    """Read a specific line range from a .md file."""
    full_path = Path(file_path)
    if not full_path.is_absolute():
        full_path = REPO_ROOT / file_path
    if not full_path.exists():
        return []
    with open(full_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines[max(0, line_start - 1):min(line_end, len(lines))]


def _extract_checklist_items(section_lines: list[str]) -> list[str]:
    """Extract audit checklist items (- [ ] ...) from section lines."""
    items = []
    for line in section_lines:
        stripped = line.strip()
        m = re.match(r"^-\s*\[[ x]\]\s*(.+)$", stripped)
        if m:
            items.append(m.group(1).strip())
    return items


def _extract_code_patterns(section_lines: list[str]) -> list[str]:
    """Extract 'Code Patterns to Look For' bullet points."""
    patterns = []
    in_code_patterns = False
    for line in section_lines:
        stripped = line.strip()
        if "code patterns to look for" in stripped.lower():
            in_code_patterns = True
            continue
        if in_code_patterns:
            if stripped.startswith("```"):
                continue
            if stripped.startswith("#") or stripped.startswith("---"):
                break
            m = re.match(r"^-\s*(.+)$", stripped)
            if m:
                patterns.append(m.group(1).strip())
    return patterns


def _extract_antipattern(section_lines: list[str]) -> str:
    """Extract the most specific vulnerable code pattern indicator.

    Looks for lines with  ❌ VULNERABLE:  comments inside code blocks,
    and extracts the explanation after the marker.
    """
    antipatterns = []
    in_code_block = False
    for line in section_lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        # Look for vulnerability markers in code comments
        if in_code_block and "VULNERABLE:" in stripped:
            m = re.search(r"VULNERABLE:\s*(.+)", stripped)
            if m:
                text = m.group(1).rstrip("*/").strip()
                if len(text) > 10:
                    antipatterns.append(text)
        # Also look for vulnerability markers in prose (bold text)
        if not in_code_block and "❌" in stripped:
            text = re.sub(r"[❌\*`]", "", stripped).strip()
            if len(text) > 10:
                antipatterns.append(text)
    # Return the most specific one (longest, as it's usually the most descriptive)
    if antipatterns:
        return max(antipatterns, key=len)[:200]
    return ""


def _extract_secure_pattern(section_lines: list[str]) -> str:
    """Extract the secure implementation indicator.

    Looks for lines with  ✅ SECURE:  comments inside code blocks.
    """
    secure_patterns = []
    in_code_block = False
    for line in section_lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block and "SECURE:" in stripped:
            m = re.search(r"SECURE:\s*(.+)", stripped)
            if m:
                text = m.group(1).rstrip("*/").strip()
                if len(text) > 10:
                    secure_patterns.append(text)
    if secure_patterns:
        return max(secure_patterns, key=len)[:200]
    return ""


def _extract_vulnerable_code_shape(section_lines: list[str]) -> str:
    """Extract a structural code shape from vulnerable examples.

    Looks for the most distinctive code line in vulnerable examples
    that serves as an antipattern when no explicit VULNERABLE marker exists.
    """
    in_vuln_block = False
    in_code_block = False
    candidates = []

    for line in section_lines:
        stripped = line.strip()
        lower = stripped.lower()
        # Detect vulnerable example headings
        if "vulnerable" in lower and ("example" in lower or "pattern" in lower):
            in_vuln_block = True
            continue
        # Detect secure implementation headings (stop looking)
        if "secure" in lower and ("implementation" in lower or "fix" in lower):
            in_vuln_block = False
            continue
        if in_vuln_block:
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block and stripped and not stripped.startswith("//"):
                # Skip trivial lines
                if len(stripped) > 15 and not stripped.startswith("{") and not stripped.startswith("}"):
                    candidates.append(stripped)

    # Pick the most distinctive line (contains function calls, comparisons, etc.)
    scored = []
    for c in candidates:
        score = 0
        if "(" in c and ")" in c:
            score += 3  # function call
        if any(op in c for op in ["==", ">=", "<=", "<", ">", "!="]):
            score += 2  # comparison
        if "require" in c or "assert" in c:
            score += 2  # validation
        if "//" in c and ("Missing" in c or "Bug" in c or "Problem" in c):
            score += 5  # explicit bug comment
        score += min(len(c), 80) / 20  # prefer moderate length
        scored.append((score, c))

    scored.sort(reverse=True)
    if scored:
        return scored[0][1][:200]
    return ""


def _build_check_from_checklist_and_patterns(
    checklist: list[str],
    code_patterns: list[str],
    antipattern: str,
    root_cause: str,
) -> list[str]:
    """Build the `check` array from extracted components.

    Merges audit checklist items and code pattern descriptions into
    1-5 actionable verification steps.
    """
    checks = []

    # Start with the root cause as the primary check
    if root_cause and len(root_cause) > 20:
        # Convert root cause into an imperative check
        rc = root_cause.strip()
        # Clean up common prefixes
        rc = re.sub(r"^This vulnerability exists because\s+", "", rc, flags=re.I)
        rc = re.sub(r"^The\s+", "", rc, flags=re.I)
        if len(rc) > 20:
            checks.append(f"VERIFY: {rc[:150]}")

    # Add checklist items (most actionable)
    for item in checklist[:3]:
        item = item.strip()
        if item and len(item) > 10:
            # Already imperative from the checklist format
            checks.append(item)

    # Add code patterns (structural indicators)
    for pattern in code_patterns[:2]:
        pattern = pattern.strip()
        if pattern and len(pattern) > 10:
            checks.append(f"LOOK FOR: {pattern}")

    # Add antipattern-based check if we have one and checks are sparse
    if antipattern and len(checks) < 3:
        checks.append(f"ANTIPATTERN: {antipattern}")

    # Deduplicate (fuzzy — avoid very similar checks)
    if len(checks) > 1:
        unique = [checks[0]]
        for c in checks[1:]:
            # Skip if >60% word overlap with any existing check
            c_words = set(c.lower().split())
            is_dup = False
            for existing in unique:
                e_words = set(existing.lower().split())
                overlap = len(c_words & e_words) / max(len(c_words | e_words), 1)
                if overlap > 0.6:
                    is_dup = True
                    break
            if not is_dup:
                unique.append(c)
        checks = unique

    return checks[:5]  # Max 5 checks


# ─── Main enrichment function ───


def enrich_card(card: dict) -> dict:
    """Enrich a single hunt card with micro-directive fields.

    Reads the referenced .md section and extracts:
    - check: 1-5 verification steps
    - antipattern: one-line vulnerable code indicator
    - securePattern: one-line secure code indicator
    """
    ref = card.get("ref", "")
    lines = card.get("lines", [0, 0])
    if not ref or len(lines) < 2:
        return card

    section_lines = _read_section(ref, lines[0], lines[1])
    if not section_lines:
        return card

    # Extract components
    checklist = _extract_checklist_items(section_lines)
    code_patterns = _extract_code_patterns(section_lines)
    antipattern = _extract_antipattern(section_lines)
    secure_pattern = _extract_secure_pattern(section_lines)

    # If no explicit antipattern found, try to extract from code shape
    if not antipattern:
        antipattern = _extract_vulnerable_code_shape(section_lines)

    # Get root cause from detect field (already in the card)
    root_cause = card.get("detect", "")

    # Build check array
    checks = _build_check_from_checklist_and_patterns(
        checklist, code_patterns, antipattern, root_cause
    )

    # Only add fields if we actually extracted something useful
    enriched = dict(card)
    if checks:
        enriched["check"] = checks
    if antipattern:
        enriched["antipattern"] = antipattern
    if secure_pattern:
        enriched["securePattern"] = secure_pattern

    return enriched


def enrich_huntcard_file(input_path: Path, output_path: Path = None) -> dict:
    """Enrich all cards in a hunt card JSON file."""
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cards = data.get("cards", [])
    enriched_cards = []
    stats = {"total": 0, "enriched": 0, "with_check": 0, "with_antipattern": 0, "with_secure": 0}

    for card in cards:
        stats["total"] += 1
        enriched = enrich_card(card)

        has_new = False
        if "check" in enriched and enriched["check"]:
            stats["with_check"] += 1
            has_new = True
        if "antipattern" in enriched and enriched["antipattern"]:
            stats["with_antipattern"] += 1
            has_new = True
        if "securePattern" in enriched and enriched["securePattern"]:
            stats["with_secure"] += 1
            has_new = True
        if has_new:
            stats["enriched"] += 1

        enriched_cards.append(enriched)

    data["cards"] = enriched_cards
    # Update meta
    data["meta"]["enriched"] = stats["enriched"]
    data["meta"]["usage"] = (
        "Load cards into context. For each card, grep target code for card.grep. "
        "On hit: execute card.check steps directly. Only read full DB entry (card.ref + card.lines) "
        "for confirmed true/likely positives."
    )

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    return stats


# ─── CLI ───


def main():
    parser = argparse.ArgumentParser(description="Enrich hunt cards with micro-directives")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    parser.add_argument("--sample", type=int, default=0, help="Process only N random cards (for preview)")
    parser.add_argument("--validate", action="store_true", help="Validate enriched cards")
    parser.add_argument("--file", type=str, help="Process only a specific hunt card file")
    args = parser.parse_args()

    if not HUNTCARDS_DIR.exists():
        print(f"❌ Hunt cards directory not found: {HUNTCARDS_DIR}")
        print("   Run `python3 generate_manifests.py` first to generate hunt cards.")
        sys.exit(1)

    all_cards_path = HUNTCARDS_DIR / "all-huntcards.json"

    if args.validate:
        # Validate existing enriched cards
        if not all_cards_path.exists():
            print("❌ all-huntcards.json not found")
            sys.exit(1)
        with open(all_cards_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        cards = data.get("cards", [])
        total = len(cards)
        with_check = sum(1 for c in cards if c.get("check"))
        with_anti = sum(1 for c in cards if c.get("antipattern"))
        with_secure = sum(1 for c in cards if c.get("securePattern"))
        print(f"✅ Validation Results:")
        print(f"   Total cards:          {total}")
        print(f"   With check array:     {with_check} ({with_check/total*100:.0f}%)")
        print(f"   With antipattern:     {with_anti} ({with_anti/total*100:.0f}%)")
        print(f"   With securePattern:   {with_secure} ({with_secure/total*100:.0f}%)")
        print(f"   File size:            {os.path.getsize(all_cards_path):,} bytes")
        # Token estimate (~4 chars per token)
        tokens = os.path.getsize(all_cards_path) // 4
        print(f"   Estimated tokens:     ~{tokens:,}")
        return

    if args.sample > 0 and args.dry_run:
        # Preview mode: show N random enriched cards
        with open(all_cards_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        cards = data.get("cards", [])
        sample = random.sample(cards, min(args.sample, len(cards)))
        for card in sample:
            enriched = enrich_card(card)
            print(f"\n{'='*70}")
            print(f"  ID: {enriched['id']}")
            print(f"  Title: {enriched['title']}")
            print(f"  Severity: {enriched['severity']}")
            print(f"  Grep: {enriched['grep']}")
            print(f"  Detect: {enriched['detect'][:100]}...")
            if enriched.get("check"):
                print(f"  Check ({len(enriched['check'])} steps):")
                for i, step in enumerate(enriched["check"], 1):
                    print(f"    {i}. {step}")
            else:
                print(f"  Check: (none extracted)")
            if enriched.get("antipattern"):
                print(f"  Antipattern: {enriched['antipattern'][:120]}")
            if enriched.get("securePattern"):
                print(f"  SecurePattern: {enriched['securePattern'][:120]}")
        return

    # Full enrichment
    print("=" * 60)
    print("Micro-Directive Enrichment")
    print("=" * 60)

    if args.file:
        # Process single file
        input_path = Path(args.file)
        if not input_path.exists():
            print(f"❌ File not found: {input_path}")
            sys.exit(1)
        output_path = None if args.dry_run else input_path
        stats = enrich_huntcard_file(input_path, output_path)
        print(f"\n  {input_path.name}:")
        print(f"    Total: {stats['total']}, Enriched: {stats['enriched']}")
        print(f"    With check: {stats['with_check']}, antipattern: {stats['with_antipattern']}, secure: {stats['with_secure']}")
        return

    # Process all per-manifest hunt card files
    total_stats = {"total": 0, "enriched": 0, "with_check": 0, "with_antipattern": 0, "with_secure": 0}
    all_enriched_cards = []

    for hc_file in sorted(HUNTCARDS_DIR.glob("*-huntcards.json")):
        if hc_file.name == "all-huntcards.json":
            continue
        output_path = None if args.dry_run else hc_file
        stats = enrich_huntcard_file(hc_file, output_path)

        for key in total_stats:
            total_stats[key] += stats[key]

        # Collect enriched cards for the combined file
        if not args.dry_run:
            with open(hc_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_enriched_cards.extend(data["cards"])

        prefix = "  [DRY-RUN]" if args.dry_run else "  →"
        print(f"{prefix} {hc_file.name}: {stats['enriched']}/{stats['total']} enriched")

    # Write combined all-huntcards.json
    if not args.dry_run and all_enriched_cards:
        combined = {
            "meta": {
                "description": "ALL enriched hunt cards — compressed detection rules with micro-directives for direct verification",
                "totalCards": len(all_enriched_cards),
                "enriched": total_stats["enriched"],
                "manifests": sorted(set(
                    hc_file.stem.replace("-huntcards", "")
                    for hc_file in HUNTCARDS_DIR.glob("*-huntcards.json")
                    if hc_file.name != "all-huntcards.json"
                )),
                "usage": (
                    "Load this single file for all vulnerability detection cards. For each card: "
                    "grep target code for card.grep. On hit: execute card.check steps directly against "
                    "grep hit locations. Only read full DB entry (card.ref + card.lines) for confirmed "
                    "true/likely positives."
                ),
            },
            "cards": all_enriched_cards,
        }
        with open(all_cards_path, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)
        combined_size = os.path.getsize(all_cards_path)
        print(f"\n  → all-huntcards.json: {len(all_enriched_cards)} cards, {combined_size:,} bytes")
        print(f"     Estimated tokens: ~{combined_size // 4:,}")

    # Summary
    print(f"\n{'='*60}")
    print(f"Summary")
    print(f"{'='*60}")
    t = total_stats
    print(f"  Total cards:          {t['total']}")
    print(f"  Enriched:             {t['enriched']} ({t['enriched']/max(t['total'],1)*100:.0f}%)")
    print(f"  With check array:     {t['with_check']} ({t['with_check']/max(t['total'],1)*100:.0f}%)")
    print(f"  With antipattern:     {t['with_antipattern']} ({t['with_antipattern']/max(t['total'],1)*100:.0f}%)")
    print(f"  With securePattern:   {t['with_secure']} ({t['with_secure']/max(t['total'],1)*100:.0f}%)")
    if args.dry_run:
        print(f"\n  [DRY-RUN] No files were modified.")


if __name__ == "__main__":
    main()
