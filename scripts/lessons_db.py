#!/usr/bin/env python3
"""
Horus cross-audit memory — FTS5-backed lesson storage and retrieval.

Usage:
  python3 scripts/lessons_db.py init
  python3 scripts/lessons_db.py ingest <audit-output-dir> [--client-tag TAG]
  python3 scripts/lessons_db.py query --ecosystem EVM [--protocol-type lending_protocol]
                                      [--topic "oracle staleness"] [--limit 10]
  python3 scripts/lessons_db.py purge --client-tag TAG
  python3 scripts/lessons_db.py stats
"""

import argparse
import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

DB_PATH = Path.home() / ".horus" / "lessons.db"
LESSONS_DIR = Path.home() / ".horus" / "lessons"

SCHEMA = """
CREATE VIRTUAL TABLE IF NOT EXISTS lessons USING fts5(
    audit_id     UNINDEXED,
    date         UNINDEXED,
    client_tag   UNINDEXED,
    ecosystem,
    protocol_type,
    phase,
    category,
    finding_id   UNINDEXED,
    related_hunt_cards,
    severity,
    lesson,
    tokenize='porter unicode61'
);

CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT
);
"""

# Patterns we scrub before saving lessons (privacy guardrail)
_SCRUB_PATTERNS = [
    (re.compile(r'0x[0-9a-fA-F]{40,}', re.I), '<address>'),
    (re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'), '<ip>'),
    (re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'), '<email>'),
    (re.compile(r'(?:sk|pk|api[_-]?key|secret)[_-]?\w{16,}', re.I), '<secret>'),
]

SEVERITY_ORDER = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1, "INFO": 0}

# ──────────────────────────────────────────────────────────────────────────────
# DB helpers
# ──────────────────────────────────────────────────────────────────────────────

def _connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    try:
        conn.execute("INSERT OR IGNORE INTO meta VALUES ('schema_version', '1')")
        conn.commit()
    except Exception:
        pass


def cmd_init(args) -> int:
    conn = _connect()
    _ensure_schema(conn)
    print(f"Initialized lessons DB at {DB_PATH}")
    return 0


# ──────────────────────────────────────────────────────────────────────────────
# Privacy scrubbing
# ──────────────────────────────────────────────────────────────────────────────

def _scrub(text: str) -> str:
    for pattern, replacement in _SCRUB_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


# ──────────────────────────────────────────────────────────────────────────────
# Parsing helpers
# ──────────────────────────────────────────────────────────────────────────────

def _parse_scope(audit_dir: Path) -> dict:
    """Read 00-scope.md and extract ecosystem + protocol_type."""
    scope_file = audit_dir / "00-scope.md"
    result = {"ecosystem": "unknown", "protocol_type": "unknown"}
    if not scope_file.exists():
        return result
    text = scope_file.read_text(errors="ignore")

    # Try to find ecosystem
    eco_match = re.search(
        r'ecosystem[:\s]+([a-zA-Z_]+)', text, re.I
    ) or re.search(
        r'\b(evm|solana|sui|cosmos|aptos|starknet|fuel|ton|near|polkadot)\b', text, re.I
    )
    if eco_match:
        result["ecosystem"] = eco_match.group(1).lower()

    # Try to find protocol_type
    pt_match = re.search(
        r'protocol[_\s]?type[:\s]+([a-zA-Z_]+)', text, re.I
    ) or re.search(
        r'\b(lending_protocol|dex_amm|vault_yield|governance_dao|cross_chain_bridge|'
        r'cosmos_appchain|solana_program|perpetuals_derivatives|token_launch|'
        r'staking_liquid_staking|nft_marketplace)\b', text, re.I
    )
    if pt_match:
        result["protocol_type"] = pt_match.group(1).lower()

    return result


def _parse_confirmed_report(audit_dir: Path) -> list[dict]:
    """
    Parse CONFIRMED-REPORT.md or 10-deep-review.md + 05-findings-triaged.md.
    Returns a list of finding dicts with keys:
      id, title, severity, category, root_cause, code_refs, multi_step
    """
    findings = []

    # Try CONFIRMED-REPORT.md first
    report_file = audit_dir / "CONFIRMED-REPORT.md"
    if not report_file.exists():
        report_file = audit_dir / "10-deep-review.md"
    if not report_file.exists():
        return findings

    text = report_file.read_text(errors="ignore")

    # Split on finding headers: ## F-001 or ### Finding: or ## [HIGH]
    sections = re.split(
        r'\n(?=#{1,3}\s+(?:F-\d+|Finding|##|\[(?:CRITICAL|HIGH|MEDIUM|LOW)))',
        text,
        flags=re.I,
    )

    for i, section in enumerate(sections):
        if not section.strip():
            continue

        finding: dict = {
            "id": f"F-{i:03d}",
            "title": "",
            "severity": "MEDIUM",
            "category": "general",
            "root_cause": "",
            "code_refs": [],
            "multi_step": False,
        }

        # Extract finding ID
        fid_match = re.search(r'F-(\d+)', section)
        if fid_match:
            finding["id"] = f"F-{fid_match.group(1)}"

        # Extract title (first non-empty header line)
        title_match = re.search(r'^#+\s+(.+)', section, re.M)
        if title_match:
            finding["title"] = title_match.group(1).strip()

        # Extract severity
        sev_match = re.search(
            r'\b(CRITICAL|HIGH|MEDIUM|LOW|INFO)\b', section, re.I
        )
        if sev_match:
            finding["severity"] = sev_match.group(1).upper()

        # Detect category from title/content
        finding["category"] = _classify_category(section)

        # Extract root cause paragraph
        rc_match = re.search(
            r'(?:root cause|root-cause|vulnerability)[:\s]+(.+?)(?:\n\n|\Z)',
            section, re.I | re.S
        )
        if rc_match:
            finding["root_cause"] = rc_match.group(1).strip()[:500]

        # Detect multi-step (requires >1 tx / cross-contract)
        if re.search(
            r'cross.contract|multi.step|flash.?loan|multiple.transact|'
            r'two.transact|three.transact|callback|reentr',
            section, re.I
        ):
            finding["multi_step"] = True

        # Extract code references
        finding["code_refs"] = re.findall(r'`([^`]+\.(sol|move|cairo|rs|go|ts):[0-9]+)`', section)

        if finding["title"] or finding["root_cause"]:
            findings.append(finding)

    return findings


def _classify_category(text: str) -> str:
    """Best-effort category classification from finding text."""
    text_lower = text.lower()
    rules = [
        ("oracle", ["oracle", "price feed", "chainlink", "twap", "staleness", "price manipulation"]),
        ("reentrancy", ["reentrancy", "reentrant", "check-effects", "cei"]),
        ("access_control", ["access control", "onlyowner", "authorization", "privilege", "role", "admin"]),
        ("arithmetic", ["overflow", "underflow", "integer", "precision", "rounding", "division"]),
        ("flash_loan", ["flash loan", "flashloan", "flash-loan"]),
        ("signature", ["signature", "ecrecover", "eip712", "replay", "malleability"]),
        ("bridge", ["bridge", "cross-chain", "relayer", "message"]),
        ("dos", ["denial of service", "dos", "griefing", "block gas"]),
        ("logic", ["logic", "invariant", "state inconsistency", "incorrect accounting"]),
        ("validation", ["validation", "missing check", "zero address", "bounds"]),
    ]
    for category, keywords in rules:
        if any(kw in text_lower for kw in keywords):
            return category
    return "general"


def _hunt_card_exists(category: str, severity: str) -> Optional[str]:
    """
    Check if the DB has a hunt card related to this category/severity.
    Returns the nearest card ID or None.
    """
    horus_root = Path(__file__).parent.parent
    all_cards_file = horus_root / "DB" / "manifests" / "huntcards" / "all-huntcards.json"

    if not all_cards_file.exists():
        return None

    try:
        data = json.loads(all_cards_file.read_text())
        cards = data if isinstance(data, list) else data.get("huntCards", [])
        category_lower = category.lower()
        for card in cards:
            cid = card.get("id", "")
            title = card.get("title", "").lower()
            card_cat = card.get("category", "").lower()
            if category_lower in cid or category_lower in title or category_lower in card_cat:
                return cid
    except Exception:
        pass

    return None


def _generate_lesson(finding: dict, scope: dict, has_card: bool) -> str:
    """
    Produce a sanitized, actionable lesson string.
    This is stored in FTS5 and queried by agents at audit start.
    """
    category_verb = {
        "oracle": "watch for oracle manipulation / stale price data",
        "reentrancy": "enforce checks-effects-interactions strictly",
        "access_control": "verify all privilege gates are present and non-bypassable",
        "arithmetic": "audit all arithmetic for overflow, precision loss, and rounding direction",
        "flash_loan": "assume any state can be transiently manipulated by flash loans",
        "signature": "check for replay attacks and signature malleability",
        "bridge": "verify message source and delivery guarantees end-to-end",
        "dos": "audit loops and external calls for gas griefing paths",
        "logic": "cross-check state-update ordering against all protocol invariants",
        "validation": "enforce all input validation at system boundaries",
        "general": "perform deep reasoning on the full call graph",
    }.get(finding["category"], "examine carefully")

    multi_step_note = (
        " This was a multi-step / cross-contract attack vector — "
        "single-contract analysis would not have surfaced it."
        if finding["multi_step"]
        else ""
    )

    db_gap_note = (
        " No existing hunt card covered this pattern — consider adding one."
        if not has_card
        else ""
    )

    lesson = (
        f"When auditing {scope['protocol_type']} on {scope['ecosystem']}, "
        f"{category_verb}. "
        f"Confirmed {finding['severity']} finding: {finding['title']}."
        f"{multi_step_note}{db_gap_note}"
    )

    return _scrub(lesson)


# ──────────────────────────────────────────────────────────────────────────────
# Commands
# ──────────────────────────────────────────────────────────────────────────────

def cmd_ingest(args) -> int:
    audit_dir = Path(args.audit_dir)
    if not audit_dir.exists():
        print(f"Error: {audit_dir} does not exist", file=sys.stderr)
        return 1

    client_tag = args.client_tag or "untagged"
    audit_id = audit_dir.name
    scope = _parse_scope(audit_dir)
    findings = _parse_confirmed_report(audit_dir)

    if not findings:
        print(f"No findings parsed from {audit_dir}. Check that CONFIRMED-REPORT.md or 10-deep-review.md exists.")
        return 0

    conn = _connect()
    _ensure_schema(conn)

    inserted = 0
    lessons_artifact_lines = [
        f"# Lessons — {audit_id}\n",
        f"Ecosystem: {scope['ecosystem']} | Protocol: {scope['protocol_type']}\n",
        f"Ingested: {datetime.now(timezone.utc).isoformat()}\n\n",
    ]

    for finding in findings:
        has_card = bool(_hunt_card_exists(finding["category"], finding["severity"]))
        category = "false_negative" if not has_card else "confirmed_hit"
        if finding["multi_step"]:
            category = "multi_step_attack"
        lesson_text = _generate_lesson(finding, scope, has_card)
        related_cards = _hunt_card_exists(finding["category"], finding["severity"]) or ""

        conn.execute(
            """INSERT INTO lessons
               (audit_id, date, client_tag, ecosystem, protocol_type,
                phase, category, finding_id, related_hunt_cards, severity, lesson)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                audit_id,
                datetime.now(timezone.utc).isoformat(),
                client_tag,
                scope["ecosystem"],
                scope["protocol_type"],
                "discovery",
                category,
                finding["id"],
                related_cards,
                finding["severity"],
                lesson_text,
            ),
        )
        inserted += 1
        lessons_artifact_lines.append(
            f"## {finding['id']} — {finding['title']}\n"
            f"- Severity: {finding['severity']}\n"
            f"- Category: {finding['category']} ({category})\n"
            f"- Lesson: {lesson_text}\n\n"
        )

    conn.commit()

    # Write human-readable artifact
    LESSONS_DIR.mkdir(parents=True, exist_ok=True)
    artifact = LESSONS_DIR / f"{audit_id}.md"
    artifact.write_text("".join(lessons_artifact_lines))

    print(f"Ingested {inserted} lessons from {audit_id}")
    print(f"Artifact: {artifact}")
    return 0


def cmd_query(args) -> int:
    conn = _connect()
    _ensure_schema(conn)

    parts = []
    params = []

    if args.ecosystem:
        parts.append("ecosystem MATCH ?")
        params.append(args.ecosystem)
    if args.protocol_type:
        parts.append("protocol_type MATCH ?")
        params.append(args.protocol_type)
    if args.topic:
        parts.append("lesson MATCH ?")
        params.append(args.topic)

    if not parts:
        print("Error: provide at least one of --ecosystem, --protocol-type, --topic", file=sys.stderr)
        return 1

    where = " AND ".join(parts)
    sql = f"SELECT audit_id, date, severity, category, lesson FROM lessons WHERE {where} LIMIT ?"
    params.append(args.limit)

    rows = conn.execute(sql, params).fetchall()
    if not rows:
        print("No lessons found.")
        return 0

    print(f"Found {len(rows)} lessons:\n")
    for row in rows:
        print(f"[{row['date'][:10]}] {row['severity']} {row['category']} (audit: {row['audit_id']})")
        print(f"  {row['lesson']}\n")

    return 0


def cmd_purge(args) -> int:
    if not args.client_tag:
        print("Error: --client-tag required for purge", file=sys.stderr)
        return 1
    conn = _connect()
    _ensure_schema(conn)
    cur = conn.execute(
        "DELETE FROM lessons WHERE client_tag = ?", (args.client_tag,)
    )
    conn.commit()
    print(f"Purged {cur.rowcount} lessons tagged '{args.client_tag}'")
    return 0


def cmd_stats(args) -> int:
    conn = _connect()
    _ensure_schema(conn)
    total = conn.execute("SELECT COUNT(*) FROM lessons").fetchone()[0]
    ecosystems = conn.execute(
        "SELECT ecosystem, COUNT(*) as n FROM lessons GROUP BY ecosystem ORDER BY n DESC"
    ).fetchall()
    categories = conn.execute(
        "SELECT category, COUNT(*) as n FROM lessons GROUP BY category ORDER BY n DESC"
    ).fetchall()
    print(f"Total lessons: {total}")
    print("\nBy ecosystem:")
    for row in ecosystems:
        print(f"  {row[0]}: {row[1]}")
    print("\nBy category:")
    for row in categories:
        print(f"  {row[0]}: {row[1]}")
    return 0


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Horus cross-audit lesson memory (FTS5-backed SQLite)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="Create ~/.horus/lessons.db")

    p_ingest = sub.add_parser("ingest", help="Extract lessons from an audit-output directory")
    p_ingest.add_argument("audit_dir", help="Path to audit-output/<audit-id>/ directory")
    p_ingest.add_argument("--client-tag", default="", help="Tag for later purge (NDA-safe)")

    p_query = sub.add_parser("query", help="Query lessons")
    p_query.add_argument("--ecosystem", default="", help="e.g. evm, sui, solana, cosmos")
    p_query.add_argument("--protocol-type", default="", dest="protocol_type")
    p_query.add_argument("--topic", default="", help="Free-text FTS5 query")
    p_query.add_argument("--limit", type=int, default=10)

    p_purge = sub.add_parser("purge", help="Remove all lessons with a given client tag")
    p_purge.add_argument("--client-tag", required=True)

    sub.add_parser("stats", help="Show DB statistics")

    args = parser.parse_args()

    dispatch = {
        "init": cmd_init,
        "ingest": cmd_ingest,
        "query": cmd_query,
        "purge": cmd_purge,
        "stats": cmd_stats,
    }
    sys.exit(dispatch[args.cmd](args))


if __name__ == "__main__":
    main()
