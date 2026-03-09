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
    "account-abstraction": ["account-abstraction"],
    "zk-rollup": ["zk-rollup"],
    "sui-move": ["Sui-Move-specific"],
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
    file_slug = re.sub(r"[^a-z0-9]+", "-", filename.lower()).strip("-")[:40]
    title_slug = re.sub(r"[^a-z0-9]+", "-", section_title.lower()).strip("-")[:30]
    return f"{category}-{file_slug}-{title_slug}-{idx:03d}"


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
            "sui_move": {
                "description": "Sui Move programs, DeFi on Sui, Sui object model",
                "manifests": ["sui-move", "general-defi", "general-security"],
                "focusPatterns": [
                    "UID", "object_id", "dynamic_field", "kiosk",
                    "overflow", "share_price", "package_upgrade",
                    "public_package", "capability", "flash_receipt",
                    "sui_bridge", "zetachain", "snap_rpc"
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
            "bonding-curve", "restaking",
        ],
        "description": "DeFi-specific: flash loans, slippage, vaults, precision, calculations, bonding curves, restaking",
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

# ── Category mapping for hunt card tags ──
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
    """Truncate text to the first *meaningful* sentence or max_len chars.
    Skips numbered list prefixes like '1.', '- ', bullet stubs.
    Handles backtick-wrapped identifiers (won't break on periods inside backticks)."""
    if not text:
        return ""
    # Strip leading numbered/bullet prefixes: "1. ", "2. ", "- ", "* "
    cleaned = re.sub(r"^(\d+\.\s*|-\s*|\*\s*)+", "", text.strip())
    if not cleaned or len(cleaned) < 5:
        return ""  # Signal caller to use fallback
    # Replace backtick-wrapped content with placeholders to avoid breaking on internal periods
    backtick_spans = []
    def _save_backtick(m):
        backtick_spans.append(m.group(0))
        return f"__BT{len(backtick_spans)-1}__"
    safe = re.sub(r"`[^`]+`", _save_backtick, cleaned)
    # Also protect version/decimal numbers from triggering sentence-end (e.g. "0.8.0", "2.5")
    decimal_spans = []
    def _save_decimal(m):
        decimal_spans.append(m.group(0))
        return f"__DC{len(decimal_spans)-1}__"
    safe = re.sub(r"\d+(?:\.\d+)+", _save_decimal, safe)
    # Also protect numbered list items (e.g. "\n1.", "\n2.") from being treated as sentence ends
    safe = re.sub(r"(?<=\n)(\d+)\.", lambda m: f"_NL{m.group(1)}_", safe)
    # First sentence (on cleaned text without backtick/decimal/list-item internals)
    for end in [".", "!", "\n\n"]:
        idx = safe.find(end)
        if 0 < idx < max_len:
            result = safe[: idx + 1].strip()
            # Skip results that are just preambles ending in colon ("Protocols may:")
            stripped_result = result.rstrip(".!").strip()
            if stripped_result.endswith(":") and len(stripped_result) < 40:
                continue
            # Skip results that are too short to be meaningful
            if len(result) < 15:
                continue
            # Restore backtick content
            for i, span in enumerate(backtick_spans):
                result = result.replace(f"__BT{i}__", span)
            # Restore decimal numbers
            for i, span in enumerate(decimal_spans):
                result = result.replace(f"__DC{i}__", span)
            # Restore numbered list items
            result = re.sub(r"_NL(\d+)_", r"\1.", result)
            return result
    # Fall back to truncation at word boundary
    result = cleaned  # use original with backticks
    if len(result) <= max_len:
        return result.strip()
    truncated = result[:max_len].rsplit(" ", 1)[0]
    return truncated.strip() + "..."


def extract_identifiers_from_content(file_path, line_start, line_end, max_keywords=6):
    """Scan the actual .md content for Solidity/Rust identifiers to enrich grep patterns.
    
    Looks for camelCase function names, function calls with parens, snake_case identifiers,
    and well-known DeFi function signatures in code blocks.
    """
    try:
        full_path = Path(file_path)
        if not full_path.is_absolute():
            full_path = DB_DIR.parent / file_path
        if not full_path.exists():
            return []
        with open(full_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        section = "".join(lines[max(0, line_start - 1):line_end])
    except Exception:
        return []

    # Extract identifiers from code blocks and inline code
    identifiers = set()

    # camelCase function-like: word(  or .word(
    for m in re.finditer(r"\b([a-z][a-zA-Z0-9]{4,})\s*\(", section):
        identifiers.add(m.group(1))
    # PascalCase identifiers (Go/Cosmos): Word(  or .Word(
    for m in re.finditer(r"\b([A-Z][a-zA-Z0-9]{4,})\s*[\(\{]?", section):
        word = m.group(1)
        # Skip markdown/prose words (all-caps or common English)
        if not word.isupper() and any(c.islower() for c in word):
            identifiers.add(word)
    # Member access patterns: object.method (camelCase or PascalCase)
    for m in re.finditer(r"\.([a-zA-Z][a-zA-Z0-9]{3,})\s*\(", section):
        identifiers.add(m.group(1))
    # snake_case identifiers (Rust/Solana): word_word
    for m in re.finditer(r"\b([a-z][a-z0-9]*_[a-z][a-z0-9_]{2,})\b", section):
        identifiers.add(m.group(1))
    # Inline code backtick identifiers: `something`
    for m in re.finditer(r"`([a-zA-Z_][a-zA-Z0-9_\.]{3,})`", section):
        identifiers.add(m.group(1))
    # Well-known Solidity patterns
    for m in re.finditer(r"\b(msg\.value|msg\.sender|block\.timestamp|tx\.origin|delegatecall|staticcall)\b", section):
        identifiers.add(m.group(1))

    # Filter noise
    NOISE = {
        "function", "require", "returns", "return", "memory", "storage",
        "calldata", "pragma", "import", "contract", "library", "interface",
        "modifier", "constructor", "virtual", "override", "public", "private",
        "internal", "external", "view", "pure", "payable", "indexed", "event",
        "emit", "struct", "mapping", "address", "uint256", "uint128", "uint64",
        "uint32", "uint8", "int256", "bool", "bytes32", "bytes", "string",
        "amount", "balance", "value", "owner", "sender", "block", "this",
        # Go/Cosmos noise
        "context", "error", "string", "module", "keeper", "query",
        "handler", "types", "params", "genesis", "store",
        # Markdown/prose noise
        "example", "pattern", "vulnerability", "attack", "impact",
        "description", "following", "secure", "implementation", "section",
        "using", "when", "where", "which", "should", "would", "could",
        "above", "below", "ensure", "check", "verify", "validate",
    }
    filtered = [ident for ident in identifiers if ident.lower() not in NOISE and len(ident) >= 4]

    # Score by specificity (longer + more structure = better)
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
        "swap", "transfer", "token", "call", "emit", "send",
        "block", "memory", "storage", "error", "check", "input",
        "output", "result", "state", "total", "count", "index",
        "length", "type", "name", "code", "hash", "key", "user",
        "contract", "sender", "receiver", "from", "target",
    }

    # Also reject keywords that are just "exploit" — these are DeFiHackLabs markers
    REJECT_EXACT = {"exploit", "exploits", "hack", "hacks", "poc", "test"}

    # Filter out generic terms and very short keywords
    scored = []
    for kw in keywords:
        kw_clean = kw.strip().rstrip("()")
        kw_lower = kw_clean.lower()
        if kw_lower in GENERIC_TERMS or kw_lower in REJECT_EXACT:
            continue
        if len(kw_clean) < 3:
            continue
        # Score: longer and more specific = better
        score = len(kw_clean)
        if "(" in kw or "." in kw:
            score += 5  # function calls / member access are very specific
        if any(c.isupper() for c in kw_clean[1:]):
            score += 3  # camelCase identifiers are specific
        if "_" in kw_clean:
            score += 3  # snake_case identifiers are specific
        scored.append((score, kw_clean))

    scored.sort(reverse=True)
    return [kw for _, kw in scored[:max_count]]


def _extract_detect_from_content(file_path, line_start, line_end, title):
    """Extract the first meaningful prose sentence from .md content for the detect field.
    Falls back to title if nothing meaningful is found."""
    try:
        full_path = Path(file_path)
        if not full_path.is_absolute():
            full_path = DB_DIR.parent / file_path
        if not full_path.exists():
            return title
        with open(full_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        section_lines = lines[max(0, line_start - 1):min(line_end, len(lines))]
    except Exception:
        return title

    # Scan for first meaningful prose line (not heading, not code, not empty, not bullet-only)
    for line in section_lines:
        stripped = line.strip()
        # Skip headings, code fences, empty lines, short lines
        if not stripped or stripped.startswith(("#", "```", "---", "|", ">", "<!--")):
            continue
        # Skip pure bullet/number lines that are just labels
        cleaned = re.sub(r"^(\d+\.\s*|-\s*|\*\s*|\*\*[^*]+\*\*:?\s*)+", "", stripped)
        if len(cleaned) < 20:
            continue
        # Skip YAML frontmatter lines (key: value)
        if re.match(r"^[a-z_]+:\s", stripped):
            continue
        # Found a meaningful sentence
        return truncate_to_sentence(cleaned, max_len=120) or title

    return title


def build_huntcard(pattern, file_path, manifest_name=""):
    """Build a single compressed hunt card from a manifest pattern entry.
    Returns None if the pattern is not suitable for hunting (structural sections, etc.)."""
    # Skip structural/non-vulnerability sections
    title_lower = pattern["title"].lower().strip()

    # Titles that are ALWAYS structural (never contain vulnerability content)
    ALWAYS_SKIP = {
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
        # Analysis/example sections that are meta-content not patterns
        "impact analysis", "technical impact", "business impact",
        "real-world examples", "known exploits",
        "attack mechanics", "attack vectors", "attack scenario",
        "mathematical proof", "vulnerable architecture",
        # Summary/reference/detection meta sections
        "real-world examples summary", "real-world exploits summary",
        "real-world loss summary by category",
        "detection patterns summary", "semgrep detection rules",
    }
    if title_lower in ALWAYS_SKIP:
        return None

    # Titles that are structural UNLESS they have severity and substantial content
    SKIP_UNLESS_SUBSTANTIAL = {
        "vulnerability description", "vulnerable pattern examples",
        "vulnerable patterns", "attack categories", "attack scenarios",
        "affected scenarios",
    }
    line_count = pattern.get("lineCount", pattern["lineEnd"] - pattern["lineStart"])
    has_severity = bool(pattern.get("severity"))
    if title_lower in SKIP_UNLESS_SUBSTANTIAL:
        # Keep only if it has severity AND is substantial (>= 40 lines)
        if not has_severity or line_count < 40:
            return None

    # Skip defihacklabs index sections (reference lists, not patterns)
    if title_lower.startswith("defihacklabs real-world"):
        return None
    # Skip category index headers ("Category N: ...", "BSC Token Exploit Patterns")
    if re.match(r"^(category\s+\d+|bsc\s+token\s+exploit)", title_lower):
        return None

    # Skip sections that are too small to be meaningful vulnerability patterns
    if line_count < 10:
        return None

    # ── Grep keyword assembly (multi-source enrichment) ──
    grep_keywords = select_best_grep_keywords(pattern.get("codeKeywords", []))

    # Enrich from subsections if sparse
    if len(grep_keywords) < 2 and pattern.get("subsections"):
        all_sub_keywords = []
        for sub in pattern["subsections"]:
            all_sub_keywords.extend(sub.get("codeKeywords", []))
        sub_kws = select_best_grep_keywords(all_sub_keywords)
        # Merge without duplicating
        existing = {k.lower() for k in grep_keywords}
        for kw in sub_kws:
            if kw.lower() not in existing:
                grep_keywords.append(kw)
                existing.add(kw.lower())
            if len(grep_keywords) >= 6:
                break

    # If still < 2 keywords, scan actual .md content for identifiers
    if len(grep_keywords) < 2:
        content_kws = extract_identifiers_from_content(
            file_path, pattern["lineStart"], pattern["lineEnd"]
        )
        existing = {k.lower() for k in grep_keywords}
        for kw in content_kws:
            if kw.lower() not in existing:
                grep_keywords.append(kw)
                existing.add(kw.lower())
            if len(grep_keywords) >= 4:
                break

    # Last resort: extract from title
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

    # ── Detect field (multi-fallback for quality) ──
    root_cause = pattern.get("rootCause", "")
    detect = truncate_to_sentence(root_cause)
    # If truncate returned empty (numbered list stub), build from title + rootCause
    if not detect or len(detect) < 15:
        # Try to find a real sentence in rootCause after stripping bullets
        if root_cause:
            lines_rc = root_cause.strip().split("\n")
            for line_rc in lines_rc:
                candidate = re.sub(r"^(\d+\.\s*|-\s*|\*\s*)+", "", line_rc).strip()
                if len(candidate) >= 20:
                    detect = truncate_to_sentence(candidate)
                    break
        # Still bad? Try extracting first meaningful sentence from the .md content
        if not detect or len(detect) < 15:
            detect = _extract_detect_from_content(
                file_path, pattern["lineStart"], pattern["lineEnd"], pattern["title"]
            )

    # ── Severity ──
    severities = pattern.get("severity", [])
    top_severity = severities[0] if severities else "UNKNOWN"
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    if len(severities) > 1:
        severities_sorted = sorted(severities, key=lambda s: severity_order.get(s, 99))
        top_severity = severities_sorted[0]

    # ── Category tags ──
    categories = MANIFEST_CATEGORY_MAP.get(manifest_name, ["general"])

    # ── Never-prune flag for CRITICAL patterns ──
    never_prune = top_severity == "CRITICAL"

    card = {
        "id": pattern["id"],
        "title": pattern["title"],
        "severity": top_severity,
        "grep": grep_pattern,
        "detect": detect,
        "cat": categories,  # category tags for grouping
        "ref": file_path,
        "lines": [pattern["lineStart"], pattern["lineEnd"]],
    }
    if never_prune:
        card["neverPrune"] = True

    return card


def build_huntcards_for_manifest(manifest_name, manifest_data):
    """Generate compressed hunt cards for all patterns in a manifest.
    Filters out structural sections that aren't actionable vulnerability patterns."""
    cards = []
    skipped = 0
    for file_entry in manifest_data["files"]:
        for pattern in file_entry["patterns"]:
            card = build_huntcard(pattern, file_entry["file"], manifest_name)
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


def build_partition_bundles(manifests):
    """Generate pre-computed shard partition bundles for each protocolContext mapping.
    
    For each protocol type (e.g., vault_yield, lending_protocol), collects all hunt cards
    from the protocol's relevant manifests, then partitions them into shards of 50-80 cards
    grouped by category tag. neverPrune cards are separated into a critical set that gets
    duplicated into every shard.
    
    Outputs: DB/manifests/bundles/<protocol>-shards.json
    """
    BUNDLES_DIR = MANIFEST_DIR / "bundles"
    BUNDLES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load all enriched hunt cards
    all_hc_path = HUNTCARDS_DIR / "all-huntcards.json"
    if not all_hc_path.exists():
        print("   ⚠ all-huntcards.json not found, skipping partition bundles")
        return
    
    with open(all_hc_path, "r", encoding="utf-8") as f:
        all_huntcards = json.load(f)
    
    # Build card lookup by manifest name (from ref path: DB/<manifest>/...)
    cards_by_manifest = defaultdict(list)
    for card in all_huntcards["cards"]:
        # Extract manifest name from ref path: "DB/oracle/..." → "oracle"
        ref_parts = card.get("ref", "").split("/")
        if len(ref_parts) >= 2:
            manifest_key = ref_parts[1]
            # Map "general" subfolder to sub-manifest names
            if manifest_key == "general" and len(ref_parts) >= 3:
                subfolder = ref_parts[2]
                # Find which general-* sub-manifest this belongs to
                for sub_name, sub_config in GENERAL_SUBCATEGORIES.items():
                    if subfolder in sub_config["folders"]:
                        manifest_key = sub_name
                        break
            cards_by_manifest[manifest_key].append(card)
    
    # Protocol context mappings (same as add_protocol_context)
    protocol_mappings = {
        "lending_protocol": ["oracle", "general-defi", "tokens", "general-security"],
        "dex_amm": ["amm", "general-defi", "oracle"],
        "vault_yield": ["tokens", "general-defi", "oracle", "unique"],
        "governance_dao": ["general-governance"],
        "cross_chain_bridge": ["bridge", "general-infrastructure"],
        "cosmos_appchain": ["cosmos"],
        "solana_program": ["solana"],
        "perpetuals_derivatives": ["oracle", "general-defi", "amm"],
        "token_launch": ["general-governance", "tokens", "general-security"],
        "staking_liquid_staking": ["general-defi", "tokens", "oracle"],
        "nft_marketplace": ["tokens", "general-infrastructure"],
        "sui_move": ["sui-move", "general-defi", "general-security"],
    }
    
    MAX_SHARD_SIZE = 80
    MIN_GROUP_SIZE = 20
    
    for protocol_name, manifest_list in protocol_mappings.items():
        # Collect all cards for this protocol's manifests
        protocol_cards = []
        seen_ids = set()
        for manifest_name in manifest_list:
            for card in cards_by_manifest.get(manifest_name, []):
                if card["id"] not in seen_ids:
                    protocol_cards.append(card)
                    seen_ids.add(card["id"])
        
        if not protocol_cards:
            continue
        
        # Separate neverPrune cards (critical set)
        critical_cards = [c for c in protocol_cards if c.get("neverPrune", False)]
        regular_cards = [c for c in protocol_cards if not c.get("neverPrune", False)]
        
        # Group regular cards by primary cat tag
        groups = defaultdict(list)
        for card in regular_cards:
            primary_cat = card.get("cat", ["general"])[0] if card.get("cat") else "general"
            groups[primary_cat].append(card)
        
        # Build shards: split large groups, merge small groups
        shards = []
        small_groups = []
        
        for cat_name, cards in sorted(groups.items(), key=lambda x: -len(x[1])):
            if len(cards) > MAX_SHARD_SIZE:
                # Split into sub-shards of ~60
                for i in range(0, len(cards), 60):
                    chunk = cards[i:i + 60]
                    suffix = f"-{i // 60 + 1}" if len(cards) > 60 else ""
                    shards.append({
                        "id": f"shard-{len(shards) + 1}-{cat_name}{suffix}",
                        "cardCount": len(chunk),
                        "categories": [cat_name],
                        "cardIds": [c["id"] for c in chunk],
                    })
            elif len(cards) < MIN_GROUP_SIZE:
                small_groups.append((cat_name, cards))
            else:
                shards.append({
                    "id": f"shard-{len(shards) + 1}-{cat_name}",
                    "cardCount": len(cards),
                    "categories": [cat_name],
                    "cardIds": [c["id"] for c in cards],
                })
        
        # Merge small groups into combined shards
        if small_groups:
            merged_cards = []
            merged_cats = []
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
                    merged_cards = []
                    merged_cats = []
            # Remaining small groups
            if merged_cards:
                if shards and len(merged_cards) < 15:
                    # Append to the last shard if very small
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
        
        # Write bundle
        bundle = {
            "meta": {
                "protocol": protocol_name,
                "description": f"Pre-computed shard partition for {protocol_name} audits",
                "totalCards": len(protocol_cards),
                "criticalCards": len(critical_cards),
                "shardCount": len(shards),
                "criticalCardIds": [c["id"] for c in critical_cards],
                "usage": (
                    "Load this file to get pre-computed shards for parallel fan-out. "
                    "Each shard is assigned to one sub-agent. Critical cards (neverPrune) "
                    "must be appended to every shard at spawn time."
                ),
            },
            "shards": shards,
        }
        
        bundle_path = BUNDLES_DIR / f"{protocol_name}-shards.json"
        with open(bundle_path, "w", encoding="utf-8") as f:
            json.dump(bundle, f, indent=2, ensure_ascii=False)
        
        total_shard_cards = sum(s["cardCount"] for s in shards)
        print(f"   → {protocol_name}: {len(shards)} shards, "
              f"{total_shard_cards} regular + {len(critical_cards)} critical cards")
    
    return True


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

    # Enrich hunt cards with micro-directives
    print(f"\n🔬 Enriching hunt cards with micro-directives...")
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
        from generate_micro_directives import enrich_huntcard_file
        total_enriched = 0
        all_enriched_cards = []
        for hc_file in sorted(HUNTCARDS_DIR.glob("*-huntcards.json")):
            if hc_file.name == "all-huntcards.json":
                continue
            stats = enrich_huntcard_file(hc_file, hc_file)
            total_enriched += stats["enriched"]
            with open(hc_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_enriched_cards.extend(data["cards"])
            print(f"   → {hc_file.name}: {stats['enriched']}/{stats['total']} enriched")
        # Write combined enriched all-huntcards.json
        combined = {
            "meta": {
                "description": "ALL enriched hunt cards — compressed detection rules with micro-directives for direct verification",
                "totalCards": len(all_enriched_cards),
                "enriched": total_enriched,
                "manifests": list(sorted(manifests.keys())),
                "usage": (
                    "Load this single file for all vulnerability detection cards. For each card: "
                    "grep target code for card.grep. On hit: execute card.check steps directly against "
                    "grep hit locations. Only read full DB entry (card.ref + card.lines) for confirmed "
                    "true/likely positives."
                ),
            },
            "cards": all_enriched_cards,
        }
        combined_path = HUNTCARDS_DIR / "all-huntcards.json"
        with open(combined_path, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)
        combined_size = os.path.getsize(combined_path)
        print(f"   → all-huntcards.json: {len(all_enriched_cards)} cards, {combined_size:,} bytes (enriched)")
    except ImportError:
        print("   ⚠ Skipping enrichment (scripts/generate_micro_directives.py not found)")
    except Exception as e:
        print(f"   ⚠ Enrichment failed: {e}")

    # Build partition bundles for parallel fan-out
    print(f"\n📦 Building partition bundles for parallel fan-out...")
    build_partition_bundles(manifests)

    # Add hunt card references to router
    router["huntcards"] = {
        "description": "Enriched detection cards with grep patterns, micro-directives (check steps, antipattern, securePattern), and one-line detection rules. Load all-huntcards.json for ALL patterns. For each card: grep target code → on hit, execute card.check steps directly → only read .md for confirmed positives.",
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
