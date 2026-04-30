"""Hunt-card builders for Horus retrieval artifacts."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Callable


DEFAULT_DB_DIR = Path(__file__).resolve().parents[2] / "DB"
DEFAULT_MANIFEST_DIR = DEFAULT_DB_DIR / "manifests"
DEFAULT_HUNTCARDS_DIR = DEFAULT_MANIFEST_DIR / "huntcards"


MANIFEST_CATEGORY_MAP = {
    "oracle": ["oracle", "price-feed", "data-freshness"],
    "amm": ["amm", "dex", "liquidity", "swap"],
    "bridge": ["bridge", "cross-chain", "messaging"],
    "cosmos": ["cosmos", "ibc", "appchain"],
    "solana": ["solana", "spl", "anchor"],
    "tokens": ["token", "erc20", "erc721", "erc4626"],
    "general-defi": ["defi", "calculation", "vault", "flash-loan"],
    "general-governance": ["governance", "dao", "voting", "stablecoin", "mev"],
    "general-infrastructure": ["proxy", "reentrancy", "storage", "upgradeable"],
    "general-security": ["access-control", "signature", "validation", "input"],
    "unique": ["protocol-specific", "unique"],
    "account-abstraction": ["account-abstraction", "ERC-4337", "ERC-7579", "smart-wallet", "paymaster", "session-key"],
    "zk-rollup": ["zk-rollup", "circuit", "fraud-proof", "rollup", "sequencer", "batch-processing", "reorg", "zksync", "optimism", "arbitrum"],
}


def truncate_to_sentence(text, max_len=120):
    """Truncate text to the first meaningful sentence or max_len chars."""
    if not text:
        return ""
    cleaned = re.sub(r"^(\d+\.\s*|-\s*|\*\s*)+", "", text.strip())
    if not cleaned or len(cleaned) < 5:
        return ""

    backtick_spans = []

    def _save_backtick(m):
        backtick_spans.append(m.group(0))
        return f"__BT{len(backtick_spans)-1}__"

    safe = re.sub(r"`[^`]+`", _save_backtick, cleaned)

    decimal_spans = []

    def _save_decimal(m):
        decimal_spans.append(m.group(0))
        return f"__DC{len(decimal_spans)-1}__"

    safe = re.sub(r"\d+(?:\.\d+)+", _save_decimal, safe)
    safe = re.sub(r"(?<=\n)(\d+)\.", lambda m: f"_NL{m.group(1)}_", safe)

    for end in [".", "!", "\n\n"]:
        idx = safe.find(end)
        if 0 < idx < max_len:
            result = safe[: idx + 1].strip()
            stripped_result = result.rstrip(".!").strip()
            if stripped_result.endswith(":") and len(stripped_result) < 40:
                continue
            if len(result) < 15:
                continue
            for i, span in enumerate(backtick_spans):
                result = result.replace(f"__BT{i}__", span)
            for i, span in enumerate(decimal_spans):
                result = result.replace(f"__DC{i}__", span)
            result = re.sub(r"_NL(\d+)_", r"\1.", result)
            return result

    result = cleaned
    if len(result) <= max_len:
        return result.strip()
    truncated = result[:max_len].rsplit(" ", 1)[0]
    return truncated.strip() + "..."


def _resolve_db_file(file_path, db_root):
    full_path = Path(file_path)
    if not full_path.is_absolute():
        full_path = db_root.parent / file_path
    return full_path


def extract_identifiers_from_content(file_path, line_start, line_end, max_keywords=6, *, db_root=DEFAULT_DB_DIR):
    """Scan DB Markdown content for Solidity/Rust/Go identifiers to enrich grep patterns."""
    try:
        full_path = _resolve_db_file(file_path, db_root)
        if not full_path.exists():
            return []
        with full_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()
        section = "".join(lines[max(0, line_start - 1):line_end])
    except Exception:
        return []

    identifiers = set()

    for m in re.finditer(r"\b([a-z][a-zA-Z0-9]{4,})\s*\(", section):
        identifiers.add(m.group(1))
    for m in re.finditer(r"\b([A-Z][a-zA-Z0-9]{4,})\s*[\(\{]?", section):
        word = m.group(1)
        if not word.isupper() and any(c.islower() for c in word):
            identifiers.add(word)
    for m in re.finditer(r"\.([a-zA-Z][a-zA-Z0-9]{3,})\s*\(", section):
        identifiers.add(m.group(1))
    for m in re.finditer(r"\b([a-z][a-z0-9]*_[a-z][a-z0-9_]{2,})\b", section):
        identifiers.add(m.group(1))
    for m in re.finditer(r"`([a-zA-Z_][a-zA-Z0-9_\.]{3,})`", section):
        identifiers.add(m.group(1))
    for m in re.finditer(r"\b(msg\.value|msg\.sender|block\.timestamp|tx\.origin|delegatecall|staticcall)\b", section):
        identifiers.add(m.group(1))

    noise = {
        "function", "require", "returns", "return", "memory", "storage",
        "calldata", "pragma", "import", "contract", "library", "interface",
        "modifier", "constructor", "virtual", "override", "public", "private",
        "internal", "external", "view", "pure", "payable", "indexed", "event",
        "emit", "struct", "mapping", "address", "uint256", "uint128", "uint64",
        "uint32", "uint8", "int256", "bool", "bytes32", "bytes", "string",
        "amount", "balance", "value", "owner", "sender", "block", "this",
        "context", "error", "string", "module", "keeper", "query",
        "handler", "types", "params", "genesis", "store",
        "example", "pattern", "vulnerability", "attack", "impact",
        "description", "following", "secure", "implementation", "section",
        "using", "when", "where", "which", "should", "would", "could",
        "above", "below", "ensure", "check", "verify", "validate",
    }
    filtered = [ident for ident in identifiers if ident.lower() not in noise and len(ident) >= 4]

    scored = []
    for ident in filtered:
        score = len(ident)
        if "_" in ident:
            score += 3
        if any(c.isupper() for c in ident[1:]):
            score += 4
        scored.append((score, ident))
    scored.sort(reverse=True)
    return [ident for _, ident in scored[:max_keywords]]


def select_best_grep_keywords(keywords, max_count=6):
    """Select the most specific keywords for grep patterns."""
    if not keywords:
        return []

    generic_terms = {
        "address", "amount", "balance", "bool", "bytes", "data",
        "event", "function", "mapping", "msg.sender", "owner",
        "require", "return", "string", "uint256", "value",
        "true", "false", "public", "private", "internal", "external",
        "swap", "transfer", "token", "call", "emit", "send",
        "block", "memory", "storage", "error", "check", "input",
        "output", "result", "state", "total", "count", "index",
        "length", "type", "name", "code", "hash", "key", "user",
        "contract", "sender", "receiver", "from", "target",
    }
    reject_exact = {"exploit", "exploits", "hack", "hacks", "poc", "test"}

    scored = []
    for kw in keywords:
        kw_clean = kw.strip().rstrip("()")
        kw_lower = kw_clean.lower()
        if kw_lower in generic_terms or kw_lower in reject_exact:
            continue
        if len(kw_clean) < 3:
            continue
        score = len(kw_clean)
        if "(" in kw or "." in kw:
            score += 5
        if any(c.isupper() for c in kw_clean[1:]):
            score += 3
        if "_" in kw_clean:
            score += 3
        scored.append((score, kw_clean))

    scored.sort(reverse=True)
    return [kw for _, kw in scored[:max_count]]


def _extract_detect_from_content(file_path, line_start, line_end, title, *, db_root=DEFAULT_DB_DIR):
    """Extract the first meaningful prose sentence from DB Markdown content."""
    try:
        full_path = _resolve_db_file(file_path, db_root)
        if not full_path.exists():
            return title
        with full_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()
        section_lines = lines[max(0, line_start - 1):min(line_end, len(lines))]
    except Exception:
        return title

    for line in section_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "```", "---", "|", ">", "<!--")):
            continue
        cleaned = re.sub(r"^(\d+\.\s*|-\s*|\*\s*|\*\*[^*]+\*\*:?\s*)+", "", stripped)
        if len(cleaned) < 20:
            continue
        if re.match(r"^[a-z_]+:\s", stripped):
            continue
        return truncate_to_sentence(cleaned, max_len=120) or title

    return title


def build_huntcard(pattern, file_path, manifest_name="", *, db_root=DEFAULT_DB_DIR):
    """Build a compressed hunt card from a manifest pattern entry."""
    title_lower = pattern["title"].lower().strip()

    always_skip = {
        "overview", "secure implementation examples", "secure implementation",
        "secure implementation patterns", "secure patterns",
        "detection patterns", "detection checklist", "audit checklist",
        "summary", "conclusion",
        "references", "prevention guidelines", "testing requirements",
        "code patterns to look for",
        "related cves/reports", "table of contents",
        "keywords for search", "related vulnerabilities",
        "development best practices", "reference", "change log",
        "security research", "technical documentation", "external links",
        "appendix",
        "secure implementation guidelines", "frequency analysis",
        "mitigation strategies", "remediation", "common patterns",
        "impact analysis", "technical impact", "business impact",
        "real-world examples", "known exploits",
        "attack mechanics", "attack vectors", "attack scenario",
        "mathematical proof", "vulnerable architecture",
        "real-world examples summary", "real-world exploits summary",
        "real-world loss summary by category",
        "detection patterns summary", "semgrep detection rules",
        "best practices", "automation best practices",
        "vulnerability categories", "agent quick view",
        "contract / boundary map", "valid bug signals",
        "false positive guards", "artifact location",
        "downloaded artifacts summary", "auditor coverage",
        "protocol coverage",
    }
    if title_lower in always_skip:
        return None

    skip_unless_substantial = {
        "vulnerability description", "vulnerable pattern examples",
        "vulnerable patterns", "attack categories", "attack scenarios",
        "affected scenarios",
    }
    line_count = pattern.get("lineCount", pattern["lineEnd"] - pattern["lineStart"])
    has_severity = bool(pattern.get("severity"))
    if title_lower in skip_unless_substantial and (not has_severity or line_count < 40):
        return None

    if title_lower.startswith("defihacklabs real-world"):
        return None
    if re.match(r"^(category\s+\d+|bsc\s+token\s+exploit)", title_lower):
        return None
    if re.match(r"^(top\s+poc\s+references|complete\s+.*\s+table|sub-variant\s+breakdown)$", title_lower):
        return None
    if line_count < 10:
        return None

    grep_keywords = select_best_grep_keywords(pattern.get("codeKeywords", []))

    if len(grep_keywords) < 2 and pattern.get("subsections"):
        all_sub_keywords = []
        for sub in pattern["subsections"]:
            all_sub_keywords.extend(sub.get("codeKeywords", []))
        sub_kws = select_best_grep_keywords(all_sub_keywords)
        existing = {k.lower() for k in grep_keywords}
        for kw in sub_kws:
            if kw.lower() not in existing:
                grep_keywords.append(kw)
                existing.add(kw.lower())
            if len(grep_keywords) >= 6:
                break

    if len(grep_keywords) < 2:
        content_kws = extract_identifiers_from_content(
            file_path,
            pattern["lineStart"],
            pattern["lineEnd"],
            db_root=db_root,
        )
        existing = {k.lower() for k in grep_keywords}
        for kw in content_kws:
            if kw.lower() not in existing:
                grep_keywords.append(kw)
                existing.add(kw.lower())
            if len(grep_keywords) >= 4:
                break

    if not grep_keywords:
        title_words = re.findall(r"[a-zA-Z][a-zA-Z0-9]{3,}", pattern["title"])
        stop_words = {
            "vulnerability", "vulnerabilities", "pattern", "patterns",
            "attack", "attacks", "example", "examples", "implementation",
            "secure", "vulnerable", "description", "analysis", "impact",
            "overview", "missing", "incorrect", "improper", "issue", "issues",
        }
        grep_keywords = [w for w in title_words if w.lower() not in stop_words][:4]

    grep_pattern = "|".join(grep_keywords) if grep_keywords else ""

    root_cause = pattern.get("rootCause", "")
    detect = truncate_to_sentence(root_cause)
    if not detect or len(detect) < 15:
        if root_cause:
            lines_rc = root_cause.strip().split("\n")
            for line_rc in lines_rc:
                candidate = re.sub(r"^(\d+\.\s*|-\s*|\*\s*)+", "", line_rc).strip()
                if len(candidate) >= 20:
                    detect = truncate_to_sentence(candidate)
                    break
        if not detect or len(detect) < 15:
            detect = _extract_detect_from_content(
                file_path,
                pattern["lineStart"],
                pattern["lineEnd"],
                pattern["title"],
                db_root=db_root,
            )

    severities = pattern.get("severity", [])
    top_severity = severities[0] if severities else "UNKNOWN"
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    if len(severities) > 1:
        severities_sorted = sorted(severities, key=lambda s: severity_order.get(s, 99))
        top_severity = severities_sorted[0]
    if top_severity == "UNKNOWN":
        return None

    card = {
        "id": pattern["id"],
        "title": pattern["title"],
        "severity": top_severity,
        "grep": grep_pattern,
        "detect": detect,
        "cat": MANIFEST_CATEGORY_MAP.get(manifest_name, ["general"]),
        "ref": file_path,
        "lines": [pattern["lineStart"], pattern["lineEnd"]],
    }
    for optional_field in ("reportEvidence", "graphHints"):
        value = pattern.get(optional_field)
        if value:
            card[optional_field] = value
    if top_severity == "CRITICAL":
        card["neverPrune"] = True

    return card


def build_huntcards_for_manifest(manifest_name, manifest_data, *, db_root=DEFAULT_DB_DIR):
    """Generate compressed hunt cards for all patterns in a manifest."""
    cards = []
    skipped = 0
    for file_entry in manifest_data["files"]:
        for pattern in file_entry["patterns"]:
            card = build_huntcard(pattern, file_entry["file"], manifest_name, db_root=db_root)
            if card is not None:
                cards.append(card)
            else:
                skipped += 1
    return {
        "meta": {
            "manifest": manifest_name,
            "description": f"Compressed hunt cards for {manifest_name} — one-line detection rules for bulk scanning",
            "totalCards": len(cards),
            "skipped": skipped,
            "usage": "Load all cards into context. For each card, grep target code for card.grep pattern. On hit, read full DB entry via read_file(card.ref, startLine=card.lines[0], endLine=card.lines[1]).",
        },
        "cards": cards,
    }


def build_all_huntcards(
    manifests,
    *,
    huntcards_dir=DEFAULT_HUNTCARDS_DIR,
    db_root=DEFAULT_DB_DIR,
    emit: Callable[[str], None] = print,
):
    """Generate hunt-card files for all manifests and the combined all-in-one file."""
    huntcards_dir.mkdir(parents=True, exist_ok=True)
    total_cards = 0
    all_cards = []
    per_manifest_info = {}

    for manifest_name, manifest_data in sorted(manifests.items()):
        huntcard_data = build_huntcards_for_manifest(manifest_name, manifest_data, db_root=db_root)
        card_count = huntcard_data["meta"]["totalCards"]
        total_cards += card_count
        all_cards.extend(huntcard_data["cards"])

        path = huntcards_dir / f"{manifest_name}-huntcards.json"
        with path.open("w", encoding="utf-8") as f:
            json.dump(huntcard_data, f, indent=2, ensure_ascii=False)

        per_manifest_info[manifest_name] = {
            "file": f"DB/manifests/huntcards/{manifest_name}-huntcards.json",
            "totalCards": card_count,
        }

        size = os.path.getsize(path)
        emit(f"   → {manifest_name}-huntcards.json: {card_count} cards, {size:,} bytes")

    combined = {
        "meta": {
            "description": "ALL hunt cards from all manifests — compressed detection rules for bulk codebase scanning",
            "totalCards": total_cards,
            "manifests": list(sorted(manifests.keys())),
            "usage": "Load this single file to get all vulnerability detection cards (~15K tokens). For each card: grep target code for card.grep pattern. On hit, read full entry via read_file(card.ref, startLine=card.lines[0], endLine=card.lines[1]).",
        },
        "cards": all_cards,
    }
    combined_path = huntcards_dir / "all-huntcards.json"
    with combined_path.open("w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    combined_size = os.path.getsize(combined_path)
    emit(f"   → all-huntcards.json: {total_cards} cards, {combined_size:,} bytes")

    return per_manifest_info, total_cards
