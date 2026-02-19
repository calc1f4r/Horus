#!/usr/bin/env python3
"""
Manifest Generator for Vulnerability Database
==============================================
Parses all .md files in DB/ to extract vulnerability patterns at the section level
and generates per-category manifest files with line ranges for surgical agent access.

Architecture:
  DB/index.json (lean router) → DB/manifests/<category>.json (pattern-level detail)

Each pattern entry includes:
  - id, title, severity, file, lineStart, lineEnd
  - keywords, rootCause snippet, attackVector snippet
  - section hierarchy for navigation
"""

import json
import os
import re
import sys
from pathlib import Path
from collections import defaultdict

DB_DIR = Path(__file__).parent / "DB"
MANIFEST_DIR = DB_DIR / "manifests"

# Category mapping: which top-level folder owns which manifest
CATEGORY_MAP = {
    "oracle": ["oracle"],
    "amm": ["amm"],
    "bridge": ["bridge"],
    "tokens": ["tokens"],
    "cosmos": ["cosmos"],
    "solana": ["Solona-chain-specific"],
    "general": ["general"],
    "unique": ["unique"],
}


def extract_severity_from_context(lines, start, end):
    """Extract severity hints from lines near a heading."""
    severities = set()
    text = "\n".join(lines[start:min(end, start + 40)])
    # Match patterns like [MEDIUM], [HIGH], severity: medium, **Severity:** HIGH
    for m in re.finditer(
        r"\[?(CRITICAL|HIGH|MEDIUM|LOW|MID)\]?",
        text,
        re.IGNORECASE,
    ):
        sev = m.group(1).upper()
        if sev == "MID":
            sev = "MEDIUM"
        severities.add(sev)
    return sorted(severities) if severities else []


def extract_keywords_from_context(lines, start, end):
    """Extract code identifiers and key terms from a section's content."""
    text = "\n".join(lines[start:min(end, start + 120)])
    keywords = set()

    # Backtick-wrapped terms (code identifiers)
    for m in re.finditer(r"`([a-zA-Z_][a-zA-Z0-9_.:()]{2,50})`", text):
        keywords.add(m.group(1).rstrip("()"))

    # Solidity function signatures
    for m in re.finditer(r"function\s+(\w+)\s*\(", text):
        keywords.add(m.group(1))

    return sorted(keywords)[:15]  # cap at 15


def extract_root_cause(lines, start, end):
    """Try to extract a root cause snippet from the section."""
    text = "\n".join(lines[start:min(end, len(lines))])
    # Look for "Root Cause" subsection
    m = re.search(
        r"(?:root\s*cause|fundamental\s*issue)[:\s]*\n+(.*?)(?:\n#|\n\*\*|\Z)",
        text,
        re.IGNORECASE | re.DOTALL,
    )
    if m:
        snippet = m.group(1).strip()[:200]
        return snippet if snippet else None
    # Fallback: look for lines right after "❌ VULNERABLE:"
    m = re.search(r"❌\s*VULNERABLE[:\s]*(.*)", text)
    if m:
        return m.group(1).strip()[:200]
    return None


def parse_md_file(filepath):
    """
    Parse a markdown file and extract all headings with line ranges.
    Returns a list of section dicts.
    """
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    sections = []
    heading_stack = []  # (level, title, lineNum)

    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            heading_stack.append((level, title, i + 1))  # 1-based

    # Calculate line ranges
    for idx, (level, title, line_num) in enumerate(heading_stack):
        # End = next heading at same or higher level, or EOF
        end_line = len(lines)
        for next_idx in range(idx + 1, len(heading_stack)):
            if heading_stack[next_idx][0] <= level:
                end_line = heading_stack[next_idx][2] - 1
                break

        # Build hierarchy path
        ancestors = []
        for prev_idx in range(idx - 1, -1, -1):
            if heading_stack[prev_idx][0] < level:
                ancestors.insert(0, heading_stack[prev_idx][1])
                level = heading_stack[prev_idx][0]

        severity = extract_severity_from_context(lines, line_num - 1, end_line)
        code_keywords = extract_keywords_from_context(lines, line_num - 1, end_line)
        root_cause = extract_root_cause(lines, line_num - 1, end_line)

        section_lines = end_line - line_num + 1

        sections.append(
            {
                "title": title,
                "heading_level": len(re.match(r"^(#{1,6})", f"{'#' * heading_stack[idx][0]}").group(1)),
                "lineStart": line_num,
                "lineEnd": end_line,
                "lineCount": section_lines,
                "hierarchy": ancestors,
                "severity": severity,
                "codeKeywords": code_keywords,
                "rootCause": root_cause,
            }
        )

    return sections, lines


def generate_pattern_id(category, filename, section_title, idx):
    """Generate a unique pattern ID."""
    slug = re.sub(r"[^a-z0-9]+", "-", section_title.lower()).strip("-")[:40]
    return f"{category}-{slug}-{idx:03d}"


def build_file_manifest(filepath, category):
    """Build manifest entry for a single file."""
    rel_path = str(filepath.relative_to(DB_DIR.parent))
    sections, lines = parse_md_file(filepath)

    if not sections:
        return None

    # Extract frontmatter metadata if present
    frontmatter = {}
    content = "".join(lines)
    fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if fm_match:
        for line in fm_match.group(1).split("\n"):
            kv = line.split(":", 1)
            if len(kv) == 2:
                key = kv[0].strip().lstrip("# ")
                val = kv[1].strip()
                if key and val:
                    frontmatter[key] = val

    # Filter out non-vulnerability structural sections
    SKIP_H2_TITLES = {
        "table of contents", "references", "references & source reports",
        "keywords for search", "related vulnerabilities", "prevention guidelines",
        "testing requirements", "security research", "technical documentation",
        "external links", "summary", "conclusion", "appendix",
        "development best practices", "reference", "change log",
    }
    SKIP_H3_TITLES = SKIP_H2_TITLES | {
        "overview", "attack categories",
        "secure implementation", "detection patterns", "audit checklist",
        "code patterns to look for", "impact analysis", "technical impact",
        "business impact", "affected scenarios", "known exploits",
        "related cves/reports", "real-world examples",
    }

    def is_h2_vulnerability(sec):
        title_lower = sec["title"].lower().strip()
        if title_lower in SKIP_H2_TITLES:
            return False
        if sec["lineCount"] < 8:
            return False
        return True

    def is_h3_vulnerability(sec):
        title_lower = sec["title"].lower().strip()
        if title_lower in SKIP_H3_TITLES:
            return False
        if sec["lineCount"] < 5:
            return False
        return True

    patterns = []
    h2_sections = [s for s in sections if s["heading_level"] == 2 and is_h2_vulnerability(s)]
    h3_all = [s for s in sections if s["heading_level"] == 3 and is_h3_vulnerability(s)]

    # If there are no good H2s but there are H3s (common in cosmos/template-based files),
    # promote H3s to be the primary patterns
    if not h2_sections and h3_all:
        h2_sections = h3_all
        h3_all = [s for s in sections if s["heading_level"] == 4 and s["lineCount"] >= 5]
    # If only a template "Vulnerability Title" H2 wraps everything, use its H3 children instead
    all_h2 = [s for s in sections if s["heading_level"] == 2]
    vuln_title_h2 = [s for s in all_h2 if s["title"].lower().strip() == "vulnerability title"]
    if len(all_h2) <= 2 and len(vuln_title_h2) == 1 and h3_all:
        h2_sections = h3_all
        h3_all = [s for s in sections if s["heading_level"] == 4 and s["lineCount"] >= 5]

    h3_sections = h3_all

    # Use H2 as primary patterns, H3 as sub-patterns
    for idx, sec in enumerate(h2_sections):
        pattern_id = generate_pattern_id(category, filepath.stem, sec["title"], idx)

        # Find child H3 sections
        children = []
        for h3 in h3_sections:
            if h3["lineStart"] > sec["lineStart"] and h3["lineEnd"] <= sec["lineEnd"]:
                children.append(
                    {
                        "title": h3["title"],
                        "lineStart": h3["lineStart"],
                        "lineEnd": h3["lineEnd"],
                        "severity": h3["severity"],
                        "codeKeywords": h3["codeKeywords"][:8],
                    }
                )

        patterns.append(
            {
                "id": pattern_id,
                "title": sec["title"],
                "lineStart": sec["lineStart"],
                "lineEnd": sec["lineEnd"],
                "lineCount": sec["lineCount"],
                "severity": sec["severity"],
                "codeKeywords": sec["codeKeywords"],
                "rootCause": sec["rootCause"],
                "subsections": children if children else None,
            }
        )

    return {
        "file": rel_path,
        "totalLines": len(lines),
        "frontmatter": frontmatter if frontmatter else None,
        "patternCount": len(patterns),
        "patterns": patterns,
    }


def collect_files_for_category(category, folders):
    """Collect all .md files for a category."""
    files = []
    for folder_name in folders:
        folder = DB_DIR / folder_name
        if folder.exists():
            for md_file in sorted(folder.rglob("*.md")):
                if md_file.name == "README.md":
                    continue
                files.append(md_file)
    return files


def build_manifest(category, folders):
    """Build complete manifest for a category."""
    files = collect_files_for_category(category, folders)
    entries = []
    total_patterns = 0

    for f in files:
        entry = build_file_manifest(f, category)
        if entry:
            entries.append(entry)
            total_patterns += entry["patternCount"]

    return {
        "meta": {
            "category": category,
            "description": f"Pattern-level index for {category} vulnerabilities",
            "fileCount": len(entries),
            "totalPatterns": total_patterns,
            "usage": "Use patterns[].lineStart/lineEnd to read exact sections with read_file tool",
        },
        "files": entries,
    }


def build_lean_router(manifests):
    """Build the lean router index.json that points to manifests."""
    router = {
        "meta": {
            "description": "Vulnerability Database Router - lightweight entry point for agents",
            "version": "3.0.0",
            "generated": "2026-02-13",
            "architecture": "Tiered search: router (this file) → manifests (DB/manifests/*.json) → vulnerability files (DB/**/*.md)",
            "usage": "1) Identify category from protocolContext or keywords. 2) Load the relevant manifest. 3) Find specific patterns with line ranges. 4) Read only those lines from the .md file.",
        },
        "searchStrategy": {
            "description": "How agents should search this database for maximum precision",
            "steps": [
                {
                    "step": 1,
                    "action": "Identify category",
                    "detail": "Use protocolContext to match the protocol type being audited, OR use quickKeywords to find the right category",
                },
                {
                    "step": 2,
                    "action": "Load category manifest",
                    "detail": "Read DB/manifests/<category>.json (much smaller than this file). Each manifest has pattern-level entries with exact line ranges.",
                },
                {
                    "step": 3,
                    "action": "Find specific patterns",
                    "detail": "Search manifest patterns by title, severity, codeKeywords. Each pattern has lineStart/lineEnd.",
                },
                {
                    "step": 4,
                    "action": "Read targeted content",
                    "detail": "Use read_file with lineStart/lineEnd to read ONLY the relevant section. Do NOT read entire files.",
                },
            ],
        },
        "manifests": {},
        "protocolContext": {},
        "auditChecklist": {},
    }

    # Build manifests section
    for cat_name, manifest in manifests.items():
        router["manifests"][cat_name] = {
            "file": f"DB/manifests/{cat_name}.json",
            "description": manifest["meta"]["description"],
            "fileCount": manifest["meta"]["fileCount"],
            "totalPatterns": manifest["meta"]["totalPatterns"],
        }

    return router


def add_protocol_context(router):
    """Add protocol context mappings with manifest references."""
    router["protocolContext"] = {
        "description": "Map protocol type → relevant manifests + priority patterns. Load the manifest file, then search for patterns matching your codebase.",
        "mappings": {
            "lending_protocol": {
                "description": "Aave, Compound, lending/borrowing protocols",
                "manifests": ["oracle", "general-defi", "tokens", "general-security"],
                "focusPatterns": [
                    "staleness", "price manipulation", "liquidation",
                    "flash loan", "precision", "rounding", "inflation attack",
                    "reentrancy", "token compatibility"
                ],
            },
            "dex_amm": {
                "description": "Uniswap, SushiSwap, decentralized exchanges",
                "manifests": ["amm", "general-defi", "oracle"],
                "focusPatterns": [
                    "slippage", "sandwich", "MEV", "TWAP", "slot0",
                    "liquidity", "constant product", "fee", "reentrancy"
                ],
            },
            "vault_yield": {
                "description": "ERC4626 vaults, yield aggregators, strategies",
                "manifests": ["tokens", "general-defi", "oracle", "unique"],
                "focusPatterns": [
                    "ERC4626", "inflation attack", "first depositor",
                    "rounding", "share manipulation", "harvest", "strategy"
                ],
            },
            "governance_dao": {
                "description": "DAOs, governance systems, voting contracts",
                "manifests": ["general-governance"],
                "focusPatterns": [
                    "governance", "voting power", "quorum", "timelock",
                    "proposal", "flash loan governance", "delegation"
                ],
            },
            "cross_chain_bridge": {
                "description": "Bridges, LayerZero, Wormhole, cross-chain messaging",
                "manifests": ["bridge", "general-infrastructure"],
                "focusPatterns": [
                    "replay", "message validation", "gas", "trusted remote",
                    "VAA", "lzReceive", "channel blocking"
                ],
            },
            "cosmos_appchain": {
                "description": "Cosmos SDK chains, IBC, app-chains",
                "manifests": ["cosmos"],
                "focusPatterns": [
                    "IBC", "staking", "slashing", "precompile",
                    "chain halt", "governance", "hooks"
                ],
            },
            "solana_program": {
                "description": "Solana programs, Anchor, SPL tokens",
                "manifests": ["solana"],
                "focusPatterns": [
                    "PDA", "CPI", "anchor", "token-2022",
                    "transfer hook", "account validation"
                ],
            },
            "perpetuals_derivatives": {
                "description": "Perpetual DEXes, options, derivatives",
                "manifests": ["oracle", "general-defi", "amm"],
                "focusPatterns": [
                    "oracle staleness", "price manipulation", "liquidation",
                    "flash loan", "precision", "funding rate"
                ],
            },
            "token_launch": {
                "description": "New token launches, meme coins, trading contracts",
                "manifests": ["general-governance", "tokens", "general-security"],
                "focusPatterns": [
                    "rug pull", "honeypot", "backdoor", "hidden mint",
                    "fee extraction", "access control", "proxy hijack"
                ],
            },
            "staking_liquid_staking": {
                "description": "Staking protocols, liquid staking derivatives",
                "manifests": ["general-defi", "tokens", "oracle"],
                "focusPatterns": [
                    "reward calculation", "precision", "rounding",
                    "ERC4626", "reentrancy", "staking"
                ],
            },
            "nft_marketplace": {
                "description": "NFT platforms, ERC721 marketplaces",
                "manifests": ["tokens", "general-infrastructure"],
                "focusPatterns": [
                    "ERC721", "callback", "onERC721Received",
                    "reentrancy", "approval"
                ],
            },
        },
    }


def build_quick_keywords(manifests):
    """Build a compact keyword → manifest mapping, saved as separate file."""
    keyword_to_manifests = defaultdict(set)

    for cat_name, manifest in manifests.items():
        for file_entry in manifest["files"]:
            # Extract keywords from file path components
            path_parts = re.findall(r"[a-zA-Z][a-zA-Z0-9]{2,}", file_entry["file"])
            for part in path_parts:
                if part.lower() not in {"md", "db", "general", "vulnerabilities", "patterns"}:
                    keyword_to_manifests[part.lower()].add(cat_name)

            for pattern in file_entry["patterns"]:
                # Index by code keywords
                for kw in pattern.get("codeKeywords", []):
                    keyword_to_manifests[kw.lower()].add(cat_name)
                # Index by significant title words
                stop_words = {
                    "the", "a", "an", "in", "of", "for", "and", "or", "to",
                    "is", "at", "by", "on", "with", "via", "using", "from",
                    "example", "pattern", "vulnerable", "secure", "implementation",
                    "analysis", "impact", "overview", "description", "fix",
                    "detection", "prevention", "guidelines", "checklist",
                    "references", "keywords", "search", "related", "table",
                    "contents", "vulnerabilities", "vulnerability",
                }
                for word in re.findall(r"[a-zA-Z][a-zA-Z0-9]{2,}", pattern["title"]):
                    if word.lower() not in stop_words:
                        keyword_to_manifests[word.lower()].add(cat_name)

    # Convert sets to sorted lists
    compact = {}
    for kw, cats in sorted(keyword_to_manifests.items()):
        compact[kw] = sorted(cats)

    return {
        "description": "Keyword → manifest names. Load manifest (DB/manifests/<name>.json) then search patterns.",
        "totalKeywords": len(compact),
        "mappings": compact,
    }


def add_audit_checklist(router):
    """Add the audit checklist (keep from original)."""
    router["auditChecklist"] = {
        "description": "Quick checklist items organized by vulnerability type",
        "general": [
            "Check all external calls for reentrancy",
            "Verify slippage protection on all swaps",
            "Check oracle staleness and manipulation vectors",
            "Verify access control on sensitive functions",
            "Check for first depositor/inflation attacks on vaults",
            "Verify rounding direction favors the protocol",
        ],
        "oracle": [
            "Check staleness validation (updatedAt, publishTime)",
            "Verify L2 sequencer uptime checks",
            "Check circuit breaker bounds (minAnswer/maxAnswer)",
            "Verify decimal handling",
            "Check for same-transaction manipulation (Pyth)",
        ],
        "amm": [
            "Check slippage parameters",
            "Verify deadline enforcement",
            "Check for spot price manipulation (slot0)",
            "Verify MINIMUM_LIQUIDITY or equivalent",
            "Check for sandwich attack vectors",
        ],
        "bridge": [
            "Verify message authentication",
            "Check for replay attack protection",
            "Verify gas limit configuration",
            "Check refund address handling",
            "Verify channel blocking recovery",
        ],
        "vault": [
            "Check first depositor attack protection",
            "Verify rounding direction (favor vault)",
            "Check fee handling consistency",
            "Verify ERC4626 compliance",
            "Check for reentrancy in deposit/withdraw",
        ],
    }


# Sub-categories for the "general" folder — split into smaller manifests
GENERAL_SUBCATEGORIES = {
    "general-security": {
        "folders": [
            "access-control", "arbitrary-call", "missing-validations",
            "validation", "initialization", "signature",
        ],
        "description": "Access control, input validation, signatures, initialization",
    },
    "general-defi": {
        "folders": [
            "flash-loan", "flash-loan-attacks", "slippage-protection",
            "vault-inflation-attack", "yield-strategy-vulnerabilities",
            "fee-on-transfer-tokens", "token-compatibility",
            "precision", "rounding-precision-loss", "calculation",
            "integer-overflow", "business-logic",
        ],
        "description": "DeFi-specific: flash loans, slippage, vaults, precision, calculations",
    },
    "general-infrastructure": {
        "folders": [
            "proxy-vulnerabilities", "uups-proxy", "diamond-proxy",
            "storage-collision", "reentrancy", "bridge",
            "erc7702-integration",
        ],
        "description": "Smart contract infrastructure: proxies, reentrancy, storage, bridges",
    },
    "general-governance": {
        "folders": [
            "dao-governance-vulnerabilities",
            "stablecoin-vulnerabilities",
            "malicious", "mev-bot", "randomness",
        ],
        "description": "Governance, stablecoins, malicious patterns, MEV, randomness",
    },
}


HUNTCARDS_DIR = MANIFEST_DIR / "huntcards"


def truncate_to_sentence(text, max_len=100):
    """Truncate text to the first sentence or max_len chars."""
    if not text:
        return ""
    # First sentence
    for end in [".", "!", "\n\n"]:
        idx = text.find(end)
        if 0 < idx < max_len:
            return text[: idx + 1].strip()
    # Fall back to truncation at word boundary
    if len(text) <= max_len:
        return text.strip()
    truncated = text[:max_len].rsplit(" ", 1)[0]
    return truncated.strip() + "..."


def select_best_grep_keywords(keywords, max_count=6):
    """Select the most specific keywords for grep patterns.
    
    Prefers longer, more unique identifiers over common short words.
    Filters out overly generic terms that cause false positives.
    """
    if not keywords:
        return []

    GENERIC_TERMS = {
        "address", "amount", "balance", "bool", "bytes", "data",
        "event", "function", "mapping", "msg.sender", "owner",
        "require", "return", "string", "uint256", "value",
        "true", "false", "public", "private", "internal", "external",
    }

    # Filter out generic terms and very short keywords
    scored = []
    for kw in keywords:
        kw_lower = kw.lower().rstrip("()")
        if kw_lower in GENERIC_TERMS:
            continue
        if len(kw) < 3:
            continue
        # Score: longer and more specific = better
        score = len(kw)
        if "(" in kw or "." in kw:
            score += 5  # function calls / member access are very specific
        if any(c.isupper() for c in kw[1:]):
            score += 3  # camelCase identifiers are specific
        scored.append((score, kw))

    scored.sort(reverse=True)
    return [kw for _, kw in scored[:max_count]]


def build_huntcard(pattern, file_path):
    """Build a single compressed hunt card from a manifest pattern entry.
    Returns None if the pattern is not suitable for hunting (structural sections, etc.)."""
    # Skip structural/non-vulnerability sections
    title_lower = pattern["title"].lower().strip()
    SKIP_TITLES = {
        "overview", "secure implementation examples", "secure implementation",
        "secure implementation patterns", "secure patterns",
        "detection patterns", "detection checklist", "audit checklist",
        "summary", "conclusion",
        "references", "prevention guidelines", "testing requirements",
        "code patterns to look for", "impact analysis", "technical impact",
        "business impact", "affected scenarios", "known exploits",
        "related cves/reports", "real-world examples", "table of contents",
        "keywords for search", "related vulnerabilities",
        "development best practices", "reference", "change log",
        "security research", "technical documentation", "external links",
        "appendix", "attack categories",
        "vulnerable pattern examples", "vulnerable patterns",
    }
    if title_lower in SKIP_TITLES:
        return None

    # Skip defihacklabs index sections (reference lists, not patterns)
    if title_lower.startswith("defihacklabs real-world"):
        return None

    # Skip sections that are too small to be meaningful vulnerability patterns
    line_count = pattern.get("lineCount", pattern["lineEnd"] - pattern["lineStart"])
    if line_count < 10:
        return None

    # Select best keywords for grep
    grep_keywords = select_best_grep_keywords(pattern.get("codeKeywords", []))

    # If no keywords from the pattern itself, try to extract from subsections
    if not grep_keywords and pattern.get("subsections"):
        all_sub_keywords = []
        for sub in pattern["subsections"]:
            all_sub_keywords.extend(sub.get("codeKeywords", []))
        grep_keywords = select_best_grep_keywords(all_sub_keywords)

    # If still empty, try to extract meaningful terms from the title
    if not grep_keywords:
        title_words = re.findall(r"[a-zA-Z][a-zA-Z0-9]{3,}", pattern["title"])
        stop_words = {
            "vulnerability", "vulnerabilities", "pattern", "patterns",
            "attack", "example", "examples", "implementation", "secure",
            "vulnerable", "description", "analysis", "impact", "overview",
        }
        grep_keywords = [w for w in title_words if w.lower() not in stop_words][:4]

    grep_pattern = "|".join(grep_keywords) if grep_keywords else ""

    # Build detection hint from rootCause or title
    root_cause = pattern.get("rootCause", "")
    detect = truncate_to_sentence(root_cause) if root_cause else pattern["title"]

    # Pick highest severity
    severities = pattern.get("severity", [])
    top_severity = severities[0] if severities else "UNKNOWN"
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    if len(severities) > 1:
        severities_sorted = sorted(severities, key=lambda s: severity_order.get(s, 99))
        top_severity = severities_sorted[0]

    return {
        "id": pattern["id"],
        "title": pattern["title"],
        "severity": top_severity,
        "grep": grep_pattern,
        "detect": detect,
        "ref": file_path,
        "lines": [pattern["lineStart"], pattern["lineEnd"]],
    }


def build_huntcards_for_manifest(manifest_name, manifest_data):
    """Generate compressed hunt cards for all patterns in a manifest.
    Filters out structural sections that aren't actionable vulnerability patterns."""
    cards = []
    skipped = 0
    for file_entry in manifest_data["files"]:
        for pattern in file_entry["patterns"]:
            card = build_huntcard(pattern, file_entry["file"])
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


def build_all_huntcards(manifests):
    """Generate hunt card files for all manifests + a combined all-in-one file."""
    HUNTCARDS_DIR.mkdir(parents=True, exist_ok=True)
    total_cards = 0
    all_cards = []
    per_manifest_info = {}

    for manifest_name, manifest_data in sorted(manifests.items()):
        huntcard_data = build_huntcards_for_manifest(manifest_name, manifest_data)
        card_count = huntcard_data["meta"]["totalCards"]
        total_cards += card_count
        all_cards.extend(huntcard_data["cards"])

        # Write per-manifest hunt card file
        path = HUNTCARDS_DIR / f"{manifest_name}-huntcards.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(huntcard_data, f, indent=2, ensure_ascii=False)

        per_manifest_info[manifest_name] = {
            "file": f"DB/manifests/huntcards/{manifest_name}-huntcards.json",
            "totalCards": card_count,
        }

        size = os.path.getsize(path)
        print(f"   → {manifest_name}-huntcards.json: {card_count} cards, {size:,} bytes")

    # Write combined all-in-one file
    combined = {
        "meta": {
            "description": "ALL hunt cards from all manifests — compressed detection rules for bulk codebase scanning",
            "totalCards": total_cards,
            "manifests": list(sorted(manifests.keys())),
            "usage": "Load this single file to get all vulnerability detection cards (~15K tokens). For each card: grep target code for card.grep pattern. On hit, read full entry via read_file(card.ref, startLine=card.lines[0], endLine=card.lines[1]).",
        },
        "cards": all_cards,
    }
    combined_path = HUNTCARDS_DIR / "all-huntcards.json"
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    combined_size = os.path.getsize(combined_path)
    print(f"   → all-huntcards.json: {total_cards} cards, {combined_size:,} bytes")

    return per_manifest_info, total_cards


def build_general_sub_manifests():
    """Split general/ into focused sub-manifests for agent precision."""
    sub_manifests = {}
    general_dir = DB_DIR / "general"

    for sub_name, sub_config in GENERAL_SUBCATEGORIES.items():
        entries = []
        total_patterns = 0

        for subfolder in sub_config["folders"]:
            folder = general_dir / subfolder
            if folder.exists():
                for md_file in sorted(folder.rglob("*.md")):
                    if md_file.name == "README.md":
                        continue
                    entry = build_file_manifest(md_file, sub_name)
                    if entry:
                        entries.append(entry)
                        total_patterns += entry["patternCount"]

        manifest = {
            "meta": {
                "category": sub_name,
                "description": sub_config["description"],
                "fileCount": len(entries),
                "totalPatterns": total_patterns,
                "usage": "Use patterns[].lineStart/lineEnd to read exact sections",
            },
            "files": entries,
        }
        sub_manifests[sub_name] = manifest
    return sub_manifests

def main():
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    manifests = {}

    print("=" * 60)
    print("Vulnerability Database Manifest Generator")
    print("=" * 60)

    for category, folders in CATEGORY_MAP.items():
        if category == "general":
            # Split general into focused sub-manifests
            print(f"\n📁 Processing category: general (split into sub-manifests)")
            sub_manifests = build_general_sub_manifests()
            for sub_name, sub_manifest in sub_manifests.items():
                manifests[sub_name] = sub_manifest
                manifest_path = MANIFEST_DIR / f"{sub_name}.json"
                with open(manifest_path, "w", encoding="utf-8") as f:
                    json.dump(sub_manifest, f, indent=2, ensure_ascii=False)
                print(f"   → {sub_name}: {sub_manifest['meta']['fileCount']} files, {sub_manifest['meta']['totalPatterns']} patterns")
            continue

        print(f"\n📁 Processing category: {category}")
        manifest = build_manifest(category, folders)
        manifests[category] = manifest

        # Write manifest
        manifest_path = MANIFEST_DIR / f"{category}.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        print(f"   → {manifest['meta']['fileCount']} files, {manifest['meta']['totalPatterns']} patterns")
        print(f"   → Written to {manifest_path}")

    # Build lean router
    print(f"\n📋 Building lean router index...")
    router = build_lean_router(manifests)
    add_protocol_context(router)
    add_audit_checklist(router)

    # Write quickKeywords to a separate file (keeps router lean)
    keywords_data = build_quick_keywords(manifests)
    keywords_path = DB_DIR / "manifests" / "keywords.json"
    with open(keywords_path, "w", encoding="utf-8") as f:
        json.dump(keywords_data, f, indent=2, ensure_ascii=False)
    keywords_size = os.path.getsize(keywords_path)
    print(f"   → Keywords index: {keywords_size:,} bytes ({keywords_data['totalKeywords']} keywords)")
    print(f"   → Written to {keywords_path}")

    # Add reference in router
    router["keywordIndex"] = {
        "file": "DB/manifests/keywords.json",
        "description": "Keyword → manifest routing. Load this file only when doing keyword-based search.",
        "totalKeywords": keywords_data["totalKeywords"],
    }

    # Build hunt cards (Tier 1.5 — compressed detection cards)
    print(f"\n🎯 Building hunt cards (Tier 1.5)...")
    huntcard_info, total_huntcards = build_all_huntcards(manifests)

    # Add hunt card references to router
    router["huntcards"] = {
        "description": "Compressed pattern cards for bulk scanning. Each card has a grep pattern + one-line detection rule. Load all-huntcards.json to fit ALL patterns (~15K tokens) in context simultaneously.",
        "allInOne": "DB/manifests/huntcards/all-huntcards.json",
        "totalCards": total_huntcards,
        "perManifest": huntcard_info,
    }

    # Write router
    router_path = DB_DIR / "index.json"
    # Backup old index
    old_index = DB_DIR / "index.old.json"
    if router_path.exists():
        import shutil
        shutil.copy2(router_path, old_index)
        print(f"   → Backed up old index to {old_index}")

    with open(router_path, "w", encoding="utf-8") as f:
        json.dump(router, f, indent=2, ensure_ascii=False)

    router_size = os.path.getsize(router_path)
    old_size = os.path.getsize(old_index) if old_index.exists() else 0
    print(f"   → New index.json: {router_size:,} bytes")
    if old_size:
        print(f"   → Old index.json: {old_size:,} bytes")
        print(f"   → Size reduction: {(1 - router_size/old_size)*100:.1f}%")

    # Summary
    print(f"\n{'=' * 60}")
    print("Summary")
    print(f"{'=' * 60}")
    total_patterns = sum(m["meta"]["totalPatterns"] for m in manifests.values())
    total_files = sum(m["meta"]["fileCount"] for m in manifests.values())
    print(f"Total files indexed: {total_files}")
    print(f"Total patterns extracted: {total_patterns}")
    print(f"Total hunt cards generated: {total_huntcards}")
    print(f"Manifests generated: {len(manifests)}")
    print(f"\nManifest files:")
    for cat in sorted(manifests.keys()):
        mf = MANIFEST_DIR / f"{cat}.json"
        size = os.path.getsize(mf)
        print(f"  DB/manifests/{cat}.json - {size:,} bytes ({manifests[cat]['meta']['totalPatterns']} patterns)")
    print(f"\nHunt card files:")
    for cat in sorted(manifests.keys()):
        hc = HUNTCARDS_DIR / f"{cat}-huntcards.json"
        if hc.exists():
            size = os.path.getsize(hc)
            print(f"  DB/manifests/huntcards/{cat}-huntcards.json - {size:,} bytes")
    combined_hc = HUNTCARDS_DIR / "all-huntcards.json"
    if combined_hc.exists():
        print(f"  DB/manifests/huntcards/all-huntcards.json - {os.path.getsize(combined_hc):,} bytes (ALL)")


if __name__ == "__main__":
    main()
