#!/usr/bin/env python3
"""
Micro-Directive Extractor
=========================
Enriches hunt cards with structured `check`, `antipattern`, `securePattern`,
and compact triage context (`validWhen`, `invalidWhen`, `impact`) extracted
from the referenced .md vulnerability entries.

Agents can execute micro-directives directly against grep hit locations
without reading the full .md file — cutting context usage by 60-80% while
also getting enough reportability context to filter out weak matches earlier.

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


def _clean_text(text: str) -> str:
    """Normalize markdown/prose into a compact plain-text sentence."""
    cleaned = text.strip()
    cleaned = re.sub(r"\[(.*?)\]\([^\)]*\)", r"\1", cleaned)
    cleaned = cleaned.replace("❌", "").replace("✅", "").replace("📖", "")
    cleaned = cleaned.replace("`", "")
    cleaned = cleaned.replace("**", "")
    cleaned = cleaned.replace("__", "")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip(" -:|\"")


def _shorten(text: str, max_len: int = 180) -> str:
    """Collapse text to a readable single sentence capped at max_len."""
    cleaned = _clean_text(text)
    if not cleaned:
        return ""
    sentence_breaks = [". ", "! ", "? "]
    for marker in sentence_breaks:
        idx = cleaned.find(marker)
        if 0 < idx < max_len:
            return cleaned[: idx + 1].strip()
    if len(cleaned) <= max_len:
        return cleaned
    truncated = cleaned[:max_len].rsplit(" ", 1)[0].strip()
    return truncated + "..."


def _is_informative_summary(text: str) -> bool:
    """Return True only for summaries that help triage a bug report."""
    cleaned = _clean_text(text)
    lower = cleaned.lower()
    if len(cleaned) < 20:
        return False
    bad_prefixes = (
        "severity:",
        "source:",
        "sources:",
        "reference:",
        "references:",
        "overview",
        "summary",
        "conclusion",
        "technical impact",
        "business impact",
        "financial impact",
    )
    if lower.startswith(bad_prefixes):
        return False
    if lower in {
        "vulnerability description",
        "vulnerable pattern examples",
        "attack scenario",
        "attack scenarios",
        "secure implementation",
    }:
        return False
    if lower.endswith((" because", " due to", " as", " with", " where")):
        return False
    return True


def _dedupe_keep_order(items: list[str]) -> list[str]:
    """Deduplicate short directives while preserving order."""
    result = []
    seen = set()
    for item in items:
        if not item:
            continue
        key = item.strip().lower()
        key = re.sub(r"^(verify|prove|falsify|impact|look for|antipattern):\s*", "", key)
        key = re.sub(r"\s+", " ", key)
        if key in seen:
            continue
        seen.add(key)
        result.append(item.strip())
    return result


def _extract_checklist_items(section_lines: list[str]) -> list[str]:
    """Extract audit checklist items (- [ ] ...) from section lines."""
    items = []
    for line in section_lines:
        stripped = line.strip()
        m = re.match(r"^-\s*\[[ x]\]\s*(.+)$", stripped)
        if m:
            items.append(m.group(1).strip())
    return items


def _extract_root_cause(section_lines: list[str]) -> str:
    """Extract a concise root-cause sentence from a section."""
    in_root_cause = False
    for line in section_lines:
        stripped = line.strip()
        lower = _clean_text(stripped).lower()
        if re.match(r"^#{1,6}\s+.*root cause", stripped, re.IGNORECASE):
            in_root_cause = True
            continue
        if not in_root_cause and lower.startswith("root cause"):
            parts = stripped.split(":", 1)
            if len(parts) == 2:
                candidate = _shorten(parts[1])
                if _is_informative_summary(candidate):
                    return candidate
            in_root_cause = True
            continue
        if in_root_cause:
            if stripped.startswith("#") or stripped.startswith("---"):
                break
            if not stripped or stripped.startswith(("```", ">")):
                continue
            candidate = _shorten(stripped)
            if _is_informative_summary(candidate):
                return candidate
    return ""


def _extract_attack_steps(section_lines: list[str]) -> list[str]:
    """Extract short attack/precondition steps from attack scenario sections."""
    steps = []
    in_attack_section = False
    for line in section_lines:
        stripped = line.strip()
        lower = _clean_text(stripped).lower()
        if re.match(r"^#{1,6}\s+.*attack scenario", stripped, re.IGNORECASE):
            in_attack_section = True
            continue
        if in_attack_section:
            if stripped.startswith("#") or stripped.startswith("---"):
                break
            if stripped.startswith("```"):
                continue
            match = re.match(r"^(?:\d+[\.)]|[-*])\s*(.+)$", stripped)
            if match:
                candidate = _shorten(match.group(1), max_len=120)
                if len(candidate) >= 12:
                    steps.append(candidate)
            elif steps and stripped.startswith(("  -", "    -")):
                continue
            if len(steps) >= 4:
                break
    return steps


def _extract_guidance_signal(section_lines: list[str], heading_terms: tuple[str, ...]) -> str:
    """Extract one concise bullet or sentence under a guidance heading.

    Used for sections like "Valid Bug Signals" and "False Positive Guards"
    that are optimized for low-context agent triage.
    """
    in_section = False
    collected = []
    heading_regex = "|".join(re.escape(term) for term in heading_terms)

    for line in section_lines:
        stripped = line.strip()
        if re.match(rf"^#{{1,6}}\s+.*(?:{heading_regex})", stripped, re.IGNORECASE):
            in_section = True
            continue
        if in_section:
            if stripped.startswith("#") or stripped.startswith("---"):
                break
            if not stripped or stripped.startswith("```"):
                continue
            match = re.match(r"^(?:\d+[\.)]|[-*])\s*(.+)$", stripped)
            candidate = match.group(1).strip() if match else stripped
            candidate = _shorten(candidate, max_len=170)
            if _is_informative_summary(candidate):
                collected.append(candidate)
            if len(collected) >= 2:
                break

    if not collected:
        return ""
    return _shorten("; ".join(collected), max_len=170)


def _extract_impact_summary(section_lines: list[str]) -> str:
    """Extract one concise impact line useful for triage prioritization."""
    for line in section_lines:
        stripped = line.strip()
        cleaned = _clean_text(stripped)
        lower = cleaned.lower()
        if lower.startswith("impacts:") or lower.startswith("impact:"):
            _, _, remainder = cleaned.partition(":")
            candidate = _shorten(remainder or cleaned, max_len=160)
            if _is_informative_summary(candidate):
                return candidate

    in_impact_section = False
    for line in section_lines:
        stripped = line.strip()
        if re.match(r"^#{1,6}\s+.*(?:technical impact|business impact|financial impact)", stripped, re.IGNORECASE):
            in_impact_section = True
            continue
        if in_impact_section:
            if stripped.startswith("#") or stripped.startswith("---"):
                break
            if not stripped:
                continue
            if stripped.startswith("|"):
                cols = [_clean_text(part) for part in stripped.strip("|").split("|")]
                if len(cols) >= 3 and cols[0].lower() not in {"impact type", "impact category"}:
                    candidate = _shorten(cols[2], max_len=160)
                    if _is_informative_summary(candidate):
                        return candidate
            bullet = re.match(r"^(?:\d+[\.)]|[-*])\s*(.+)$", stripped)
            if bullet:
                candidate = _shorten(bullet.group(1), max_len=160)
                if _is_informative_summary(candidate):
                    return candidate
    return ""


def _extract_fix_signal(section_lines: list[str]) -> str:
    """Extract the first secure/fix heading when no code comment is available."""
    for line in section_lines:
        stripped = line.strip()
        if re.match(r"^#{1,6}\s+.*(?:secure pattern|secure implementation|fix)", stripped, re.IGNORECASE):
            heading = re.sub(r"^#{1,6}\s*", "", stripped)
            candidate = _shorten(heading, max_len=160)
            if _is_informative_summary(candidate):
                return candidate
        cleaned = _clean_text(stripped)
        if cleaned.lower().startswith("fix ") or cleaned.lower().startswith("fix:"):
            candidate = _shorten(cleaned, max_len=160)
            if _is_informative_summary(candidate):
                return candidate
    return ""


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


def _build_valid_when(root_cause: str, attack_steps: list[str], antipattern: str) -> str:
    """Build a compact reportability rule for the bug class."""
    if _is_informative_summary(root_cause):
        return _shorten(root_cause, max_len=170)
    if attack_steps:
        candidate = _shorten("; ".join(attack_steps[:2]), max_len=170)
        if _is_informative_summary(candidate):
            return candidate
    if _is_informative_summary(antipattern):
        return _shorten(antipattern, max_len=170)
    return ""


def _build_invalid_when(secure_pattern: str, fix_signal: str) -> str:
    """Build a compact false-positive invalidator rule."""
    if _is_informative_summary(secure_pattern):
        return _shorten(secure_pattern, max_len=170)
    if _is_informative_summary(fix_signal):
        return _shorten(fix_signal, max_len=170)
    return ""


def _build_proof_hint(
    attack_steps: list[str],
    antipattern: str,
    code_patterns: list[str],
    valid_when: str,
) -> str:
    """Build a proof-oriented directive showing what evidence should exist."""
    if attack_steps:
        candidate = _shorten("; ".join(attack_steps[:2]), max_len=170)
        if _is_informative_summary(candidate):
            return candidate
    if _is_informative_summary(antipattern) and _clean_text(antipattern).lower() != _clean_text(valid_when).lower():
        return _shorten(antipattern, max_len=170)
    if code_patterns:
        candidate = _shorten(code_patterns[0], max_len=170)
        if _is_informative_summary(candidate):
            return candidate
    return ""


def _build_check_from_checklist_and_patterns(
    checklist: list[str],
    code_patterns: list[str],
    antipattern: str,
    root_cause: str,
    proof_hint: str,
    invalid_when: str,
    impact: str,
) -> list[str]:
    """Build the `check` array from extracted components.

    Merges audit checklist items and code pattern descriptions into
    1-6 actionable verification steps.
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
            checks.append(f"VERIFY: {_shorten(rc, max_len=150)}")

    if proof_hint:
        checks.append(f"PROVE: {proof_hint}")

    if invalid_when:
        checks.append(f"FALSIFY: {invalid_when}")

    if impact:
        checks.append(f"IMPACT: {impact}")

    # Add checklist items (most actionable)
    for item in checklist[:2]:
        item = item.strip()
        if item and len(item) > 10:
            # Already imperative from the checklist format
            checks.append(item)

    # Add code patterns (structural indicators)
    for pattern in code_patterns[:1]:
        pattern = pattern.strip()
        if pattern and len(pattern) > 10:
            checks.append(f"LOOK FOR: {pattern}")

    # Add antipattern-based check if we have one and checks are sparse
    if antipattern and len(checks) < 4:
        checks.append(f"ANTIPATTERN: {antipattern}")

    checks = _dedupe_keep_order(checks)
    return checks[:6]  # Max 6 checks


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
    root_cause = _extract_root_cause(section_lines) or card.get("detect", "")
    attack_steps = _extract_attack_steps(section_lines)
    explicit_valid_when = _extract_guidance_signal(
        section_lines,
        ("valid bug signals", "valid when", "reportable when"),
    )
    explicit_invalid_when = _extract_guidance_signal(
        section_lines,
        ("false positive guards", "invalid when", "not this bug when", "safe if"),
    )
    impact = _extract_impact_summary(section_lines)
    antipattern = _extract_antipattern(section_lines)
    secure_pattern = _extract_secure_pattern(section_lines)
    fix_signal = _extract_fix_signal(section_lines)

    # If no explicit antipattern found, try to extract from code shape
    if not antipattern:
        antipattern = _extract_vulnerable_code_shape(section_lines)

    valid_when = explicit_valid_when or _build_valid_when(root_cause, attack_steps, antipattern)
    invalid_when = explicit_invalid_when or _build_invalid_when(secure_pattern, fix_signal)
    proof_hint = _build_proof_hint(attack_steps, antipattern, code_patterns, valid_when)

    # Build check array
    checks = _build_check_from_checklist_and_patterns(
        checklist,
        code_patterns,
        antipattern,
        valid_when or root_cause,
        proof_hint,
        invalid_when,
        impact,
    )

    # Only add fields if we actually extracted something useful
    enriched = dict(card)
    if checks:
        enriched["check"] = checks
    if antipattern:
        enriched["antipattern"] = antipattern
    if secure_pattern:
        enriched["securePattern"] = secure_pattern
    if valid_when:
        enriched["validWhen"] = valid_when
    if invalid_when:
        enriched["invalidWhen"] = invalid_when
    if impact:
        enriched["impact"] = impact

    return enriched


def enrich_huntcard_file(input_path: Path, output_path: Path = None) -> dict:
    """Enrich all cards in a hunt card JSON file."""
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cards = data.get("cards", [])
    enriched_cards = []
    stats = {
        "total": 0,
        "enriched": 0,
        "with_check": 0,
        "with_antipattern": 0,
        "with_secure": 0,
        "with_valid": 0,
        "with_invalid": 0,
        "with_impact": 0,
    }

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
        if "validWhen" in enriched and enriched["validWhen"]:
            stats["with_valid"] += 1
            has_new = True
        if "invalidWhen" in enriched and enriched["invalidWhen"]:
            stats["with_invalid"] += 1
            has_new = True
        if "impact" in enriched and enriched["impact"]:
            stats["with_impact"] += 1
            has_new = True
        if has_new:
            stats["enriched"] += 1

        enriched_cards.append(enriched)

    data["cards"] = enriched_cards
    # Update meta
    data["meta"]["enriched"] = stats["enriched"]
    data["meta"]["usage"] = (
        "Load cards into context. For each card, grep target code for card.grep. "
        "On hit: execute card.check steps directly, use validWhen/invalidWhen/impact for rapid triage, "
        "and only read full DB entry (card.ref + card.lines) for confirmed true/likely positives."
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
        with_valid = sum(1 for c in cards if c.get("validWhen"))
        with_invalid = sum(1 for c in cards if c.get("invalidWhen"))
        with_impact = sum(1 for c in cards if c.get("impact"))
        print(f"✅ Validation Results:")
        print(f"   Total cards:          {total}")
        print(f"   With check array:     {with_check} ({with_check/total*100:.0f}%)")
        print(f"   With antipattern:     {with_anti} ({with_anti/total*100:.0f}%)")
        print(f"   With securePattern:   {with_secure} ({with_secure/total*100:.0f}%)")
        print(f"   With validWhen:       {with_valid} ({with_valid/total*100:.0f}%)")
        print(f"   With invalidWhen:     {with_invalid} ({with_invalid/total*100:.0f}%)")
        print(f"   With impact:          {with_impact} ({with_impact/total*100:.0f}%)")
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
            if enriched.get("validWhen"):
                print(f"  validWhen: {enriched['validWhen'][:140]}")
            if enriched.get("invalidWhen"):
                print(f"  invalidWhen: {enriched['invalidWhen'][:140]}")
            if enriched.get("impact"):
                print(f"  impact: {enriched['impact'][:140]}")
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
    total_stats = {
        "total": 0,
        "enriched": 0,
        "with_check": 0,
        "with_antipattern": 0,
        "with_secure": 0,
        "with_valid": 0,
        "with_invalid": 0,
        "with_impact": 0,
    }
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
                    "grep hit locations, use validWhen/invalidWhen/impact for rapid triage, and only read "
                    "full DB entry (card.ref + card.lines) for confirmed true/likely positives."
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
    print(f"  With validWhen:       {t['with_valid']} ({t['with_valid']/max(t['total'],1)*100:.0f}%)")
    print(f"  With invalidWhen:     {t['with_invalid']} ({t['with_invalid']/max(t['total'],1)*100:.0f}%)")
    print(f"  With impact:          {t['with_impact']} ({t['with_impact']/max(t['total'],1)*100:.0f}%)")
    if args.dry_run:
        print(f"\n  [DRY-RUN] No files were modified.")


if __name__ == "__main__":
    main()
