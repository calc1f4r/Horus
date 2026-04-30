#!/usr/bin/env python3
"""Inventory hunt-card quality and map cards to supporting reports.

This is a working artifact for docs/HUNT_CARD_REPORT_ENRICHMENT_PLAN.md.
It does not edit DB markdown or generated manifest files.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from horus_retrieval.documents import DBDocument, split_frontmatter


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HUNTCARDS = ROOT / "DB/manifests/huntcards/all-huntcards.json"
DEFAULT_OUT_DIR = ROOT / "DB/_telemetry/huntcard-enrichment"
DEFAULT_CHECKLIST = DEFAULT_OUT_DIR / "CHECKLIST.md"
PILOT_TERMS = (
    "erc4626",
    "erc-4626",
    "vault",
    "share inflation",
    "first depositor",
    "inflation attack",
    "donation",
    "convertToShares",
    "totalAssets",
)
REPORT_READ_LIMIT = 32768
MAX_REPORT_FILES = 750
MAX_CANDIDATES_PER_CARD = 8
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_]{2,}")
REPORT_PATH_RE = re.compile(r"(?:\.\./)*(reports/[A-Za-z0-9_./-]+\.md)")
URL_RE = re.compile(r"https?://[^\s)>\]\"']+")
SOLODIT_RE = re.compile(r"\bsolodit(?:_id)?\s*[:#]?\s*([0-9]{3,})\b", re.I)

AUDIT_FIRMS = (
    "Code4rena",
    "Sherlock",
    "Cantina",
    "Spearbit",
    "Trail of Bits",
    "OpenZeppelin",
    "Pashov",
    "Pashov Audit Group",
    "SigmaPrime",
    "MixBytes",
    "Zokyo",
    "Cyfrin",
    "Consensys",
    "ChainSecurity",
    "Dedaub",
)


@dataclass(frozen=True)
class ReportDoc:
    path: str
    title: str
    text: str
    metadata: dict[str, Any]
    tokens: set[str]


def ascii_clean(value: Any) -> Any:
    if isinstance(value, str):
        replacements = {
            "\u2018": "'",
            "\u2019": "'",
            "\u201c": '"',
            "\u201d": '"',
            "\u2013": "-",
            "\u2014": "-",
            "\u2192": "->",
            "\u00a0": " ",
        }
        for old, new in replacements.items():
            value = value.replace(old, new)
        return value.encode("ascii", "ignore").decode("ascii")
    if isinstance(value, list):
        return [ascii_clean(v) for v in value]
    if isinstance(value, dict):
        return {ascii_clean(k): ascii_clean(v) for k, v in value.items()}
    return value


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii") as handle:
        json.dump(ascii_clean(data), handle, indent=2, sort_keys=True)
        handle.write("\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(ascii_clean(text), encoding="ascii")


def load_cards(manifest: str | None) -> tuple[list[dict[str, Any]], str]:
    if not manifest or manifest == "all":
        path = DEFAULT_HUNTCARDS
    else:
        name = manifest
        if not name.endswith("-huntcards"):
            name = f"{name}-huntcards"
        path = ROOT / "DB/manifests/huntcards" / f"{name}.json"
    data = load_json(path)
    cards = data.get("cards", data if isinstance(data, list) else [])
    if not isinstance(cards, list):
        raise SystemExit(f"Unsupported hunt-card shape in {path}")
    return cards, rel(path)


def load_manifest_patterns() -> dict[tuple[str, int, int], dict[str, Any]]:
    patterns: dict[tuple[str, int, int], dict[str, Any]] = {}
    for path in sorted((ROOT / "DB/manifests").glob("*.json")):
        if path.name == "keywords.json":
            continue
        data = load_json(path)
        for file_info in data.get("files", []):
            db_ref = file_info.get("file")
            for pattern in file_info.get("patterns", []) or []:
                start = int(pattern.get("lineStart") or 0)
                end = int(pattern.get("lineEnd") or 0)
                patterns[(db_ref, start, end)] = pattern
    return patterns


def pattern_for_card(card: dict[str, Any], patterns: dict[tuple[str, int, int], dict[str, Any]]) -> dict[str, Any]:
    ref_path = card.get("ref")
    lines = card.get("lines") or [0, 0]
    if len(lines) != 2:
        return {}
    start, end = int(lines[0]), int(lines[1])
    best: tuple[int, dict[str, Any]] = (0, {})
    for (ref, p_start, p_end), pattern in patterns.items():
        if ref != ref_path:
            continue
        overlap = max(0, min(end, p_end) - max(start, p_start) + 1)
        if overlap > best[0]:
            best = (overlap, pattern)
    return best[1]


def tokenize(text: str) -> set[str]:
    return {t.lower() for t in WORD_RE.findall(text) if len(t) >= 3}


def code_terms_from_grep(grep: str) -> list[str]:
    terms: list[str] = []
    for raw in re.split(r"[|,\s]+", grep or ""):
        term = raw.strip("`'\"()[]{}")
        if len(term) >= 4 and re.search(r"[A-Za-z_]", term):
            terms.append(term)
    return sorted(set(terms), key=str.lower)


def meaningful_terms(card: dict[str, Any], pattern: dict[str, Any]) -> list[str]:
    terms: list[str] = []
    terms.extend(code_terms_from_grep(card.get("grep", "")))
    terms.extend(pattern.get("codeKeywords") or [])
    terms.extend(pattern.get("searchKeywords") or [])
    terms.extend(card.get("cat") or [])
    for field in ("title", "detect", "antipattern", "validWhen", "impact"):
        terms.extend(WORD_RE.findall(str(card.get(field, ""))))
    stop = {
        "the",
        "and",
        "with",
        "from",
        "this",
        "that",
        "when",
        "can",
        "has",
        "for",
        "not",
        "via",
        "bug",
        "vulnerability",
        "vulnerable",
        "pattern",
        "issue",
        "issues",
        "against",
        "attacker",
        "attack",
        "high",
        "medium",
        "critical",
    }
    filtered = []
    seen = set()
    for term in terms:
        clean = term.strip("`'\"()[]{}").lower()
        if len(clean) < 4 or clean in stop or clean in seen:
            continue
        seen.add(clean)
        filtered.append(term.strip("`'\"()[]{}"))
    return filtered[:80]


def extract_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    frontmatter, body = split_frontmatter(text)
    normalized = {
        str(key).strip().lower().replace(" ", "_"): value
        for key, value in frontmatter.items()
    }
    return normalized, body


def read_db_section(ref_path: str, lines: list[int] | tuple[int, int]) -> tuple[str, dict[str, Any]]:
    path = ROOT / ref_path
    if not path.exists():
        return "", {}
    document = DBDocument.from_path(path)
    frontmatter = {
        str(key).strip().lower().replace(" ", "_"): value
        for key, value in document.frontmatter.items()
    }
    all_lines = document.content.splitlines()
    start = max(1, int(lines[0]) if lines else 1)
    end = min(len(all_lines), int(lines[1]) if len(lines) > 1 else start)
    section = "\n".join(all_lines[start - 1 : end])
    return section, frontmatter


def extract_metadata(text: str, frontmatter: dict[str, Any] | None = None) -> dict[str, Any]:
    frontmatter = frontmatter or {}
    urls = sorted(set(URL_RE.findall(text)))
    report_paths = sorted(set(p.replace("../", "") for p in REPORT_PATH_RE.findall(text)))
    solodit_ids = sorted(set(SOLODIT_RE.findall(text)))
    for key in ("solodit_id", "solodit"):
        value = frontmatter.get(key)
        if isinstance(value, str) and value and value not in solodit_ids:
            solodit_ids.append(value)
    firms = sorted({firm for firm in AUDIT_FIRMS if re.search(rf"\b{re.escape(firm)}\b", text, re.I)})
    audit_firm = frontmatter.get("audit_firm")
    if isinstance(audit_firm, str) and audit_firm and audit_firm not in firms:
        firms.append(audit_firm)
    protocols = []
    protocol = frontmatter.get("protocol")
    if isinstance(protocol, str) and protocol and protocol.lower() not in {"generic", "unknown"}:
        protocols.append(protocol)
    for match in re.finditer(r"\|\s*([^|\n]{3,60})\s*\|\s*`?reports/", text):
        candidate = match.group(1).strip(" -*`")
        if candidate and candidate not in protocols:
            protocols.append(candidate)
    metadata: dict[str, Any] = dict(frontmatter)
    metadata.update({
        "report_paths": report_paths,
        "solodit_ids": sorted(set(solodit_ids)),
        "urls": urls,
        "source_urls": [u for u in urls if "github.com" not in u.lower()],
        "github_urls": [u for u in urls if "github.com" in u.lower()],
        "audit_firms": sorted(set(firms)),
        "protocols": sorted(set(protocols)),
    })
    return metadata


def report_title(text: str, path: Path, frontmatter: dict[str, Any]) -> str:
    for key in ("title", "vulnerability_title"):
        value = frontmatter.get(key)
        if isinstance(value, str) and value:
            return value
    _, body = extract_frontmatter(text)
    lines = body.splitlines()
    for idx, line in enumerate(lines[:120]):
        stripped = line.strip()
        if stripped.lower() == "## vulnerability title":
            for candidate in lines[idx + 1 : idx + 8]:
                candidate = candidate.strip()
                if candidate and not candidate.startswith("#"):
                    return candidate.strip("[]")
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return path.stem.replace("-", " ")


def load_reports(reports_dir: Path | None) -> list[ReportDoc]:
    if not reports_dir:
        return []
    base = reports_dir if reports_dir.is_absolute() else ROOT / reports_dir
    if not base.exists():
        return []
    docs: list[ReportDoc] = []
    for path in sorted(base.rglob("*.md"))[:MAX_REPORT_FILES]:
        text = path.read_text(encoding="utf-8", errors="replace")[:REPORT_READ_LIMIT]
        frontmatter, _ = extract_frontmatter(text)
        metadata = extract_metadata(text, frontmatter)
        title = report_title(text, path, frontmatter)
        docs.append(
            ReportDoc(
                path=rel(path),
                title=title,
                text=text,
                metadata=metadata,
                tokens=tokenize(title + "\n" + path.stem + "\n" + text[:8192]),
            )
        )
    return docs


def score_text_presence(text: str, minimum_words: int, action_words: tuple[str, ...] = ()) -> int:
    stripped = (text or "").strip()
    if not stripped:
        return 0
    words = WORD_RE.findall(stripped)
    if len(words) < minimum_words:
        return 1
    if action_words and not any(word.lower() in stripped.lower() for word in action_words):
        return 2
    return 3


def score_card(card: dict[str, Any], explicit_count: int = 0) -> dict[str, Any]:
    grep_terms = code_terms_from_grep(card.get("grep", ""))
    distinctive = [t for t in grep_terms if len(t) >= 7 or "_" in t or re.search(r"[A-Z]", t[1:])]
    generic = {"transfer", "deposit", "withdraw", "mint", "burn", "update", "execute", "balance", "amount"}
    generic_count = sum(1 for t in grep_terms if t.lower() in generic)
    if not grep_terms:
        grep_score = 0
    elif len(distinctive) >= 3 and generic_count <= max(1, len(grep_terms) // 3):
        grep_score = 3
    elif len(grep_terms) >= 2:
        grep_score = 2
    else:
        grep_score = 1

    checks = card.get("check") or []
    check_text = "\n".join(str(c) for c in checks)
    check_markers = sum(1 for marker in ("VERIFY:", "PROVE:", "FALSIFY:", "IMPACT:", "ANTIPATTERN:") if marker in check_text)
    check_score = 0 if not checks else 1 if check_markers == 0 else 2 if check_markers < 3 else 3

    invalid_when = str(card.get("invalidWhen") or card.get("securePattern") or "")
    guard_score = score_text_presence(invalid_when, 6, ("safe", "prevent", "reject", "enforce", "validate", "neutralize", "only"))

    impact_score = score_text_presence(str(card.get("impact") or ""), 6, ("loss", "drain", "theft", "dos", "insolv", "steal", "freeze"))
    detect_score = score_text_presence(str(card.get("detect") or card.get("validWhen") or ""), 8)
    report_score = 0 if explicit_count == 0 else 1 if explicit_count == 1 else 2 if explicit_count < 4 else 3

    return {
        "grep_specificity": grep_score,
        "detect_correctness": detect_score,
        "check_actionability": check_score,
        "false_positive_guard": guard_score,
        "impact_clarity": impact_score,
        "report_support": report_score,
        "graph_connectivity": 0,
        "notes": {
            "grep_terms": len(grep_terms),
            "explicit_report_refs": explicit_count,
            "graph_connectivity": "placeholder_not_evaluated",
        },
    }


def explicit_report_refs(section_metadata: dict[str, Any], db_metadata: dict[str, Any]) -> list[dict[str, Any]]:
    refs = []
    for path in section_metadata.get("report_paths", []):
        refs.append({"path": path, "confidence": "explicit", "matched_terms": ["db_section_report_path"]})
    for solodit_id in section_metadata.get("solodit_ids", []):
        refs.append({"solodit_id": solodit_id, "confidence": "explicit", "matched_terms": ["db_section_solodit_id"]})
    for key in ("urls", "source_urls", "github_urls"):
        for url in section_metadata.get(key, []):
            refs.append({"url": url, "confidence": "explicit", "matched_terms": [f"db_section_{key}"]})
    if not refs:
        for path in db_metadata.get("report_paths", [])[:5]:
            refs.append({"path": path, "confidence": "weak_keyword", "matched_terms": ["db_file_report_path"]})
    return refs


def enrich_report_ref(ref: dict[str, Any], report_by_path: dict[str, ReportDoc]) -> dict[str, Any]:
    path = ref.get("path")
    if path and path in report_by_path:
        report = report_by_path[path]
        metadata = report.metadata
        ref = dict(ref)
        ref.update(
            {
                "title": report.title,
                "severity": metadata_value(metadata, "severity"),
                "audit_firm": metadata_value(metadata, "audit_firm") or first(metadata.get("audit_firms")),
                "protocol": metadata_value(metadata, "protocol") or first(metadata.get("protocols")),
                "solodit_id": metadata_value(metadata, "solodit_id") or first(metadata.get("solodit_ids")),
                "source_url": metadata_value(metadata, "source_link") or first(metadata.get("source_urls")),
                "github_url": metadata_value(metadata, "github_link") or first(metadata.get("github_urls")),
            }
        )
    return {k: v for k, v in ref.items() if v not in (None, "", [], {})}


def first(values: Any) -> Any:
    if isinstance(values, list) and values:
        return values[0]
    return None


def metadata_value(metadata: dict[str, Any], key: str) -> Any:
    value = metadata.get(key)
    if isinstance(value, list):
        value = value[0] if value else None
    if isinstance(value, str) and value.strip().lower() in {"none", "n/a", "na", "unknown"}:
        return None
    return value


def candidate_reports(card: dict[str, Any], pattern: dict[str, Any], reports: list[ReportDoc]) -> list[dict[str, Any]]:
    if not reports:
        return []
    terms = meaningful_terms(card, pattern)
    weighted_terms: dict[str, int] = {}
    for term in terms:
        clean = term.lower()
        if len(clean) < 4:
            continue
        weight = 3 if re.search(r"[A-Z_()]", term) else 2 if " " in term else 1
        weighted_terms[clean] = max(weighted_terms.get(clean, 0), weight)
    title_tokens = tokenize(str(card.get("title", "")))
    scored = []
    for report in reports:
        haystack = (report.path + "\n" + report.title + "\n" + report.text[:8192]).lower()
        matched = []
        score = 0
        for term, weight in weighted_terms.items():
            if term in haystack:
                matched.append(term)
                score += weight
        token_overlap = title_tokens & report.tokens
        score += min(6, len(token_overlap))
        if score < 4:
            continue
        confidence = "strong_semantic" if score >= 10 and len(matched) >= 3 else "weak_keyword"
        ref = {
            "path": report.path,
            "confidence": confidence,
            "matched_terms": sorted(set(matched + sorted(token_overlap)))[:12],
            "match_score": score,
            "title": report.title,
            "severity": metadata_value(report.metadata, "severity"),
            "audit_firm": metadata_value(report.metadata, "audit_firm") or first(report.metadata.get("audit_firms")),
            "protocol": metadata_value(report.metadata, "protocol") or first(report.metadata.get("protocols")),
            "solodit_id": metadata_value(report.metadata, "solodit_id") or first(report.metadata.get("solodit_ids")),
            "source_url": metadata_value(report.metadata, "source_link") or first(report.metadata.get("source_urls")),
            "github_url": metadata_value(report.metadata, "github_link") or first(report.metadata.get("github_urls")),
        }
        scored.append(ref)
    scored.sort(key=lambda item: (-item["match_score"], item["path"]))
    return [{k: v for k, v in item.items() if v not in (None, "", [], {})} for item in scored[:MAX_CANDIDATES_PER_CARD]]


def pilot_filter(card: dict[str, Any]) -> bool:
    haystack = json.dumps(card, sort_keys=True).lower()
    return any(term.lower() in haystack for term in PILOT_TERMS)


def summarize_quality(rows: list[dict[str, Any]]) -> dict[str, Any]:
    fields = [
        "grep_specificity",
        "detect_correctness",
        "check_actionability",
        "false_positive_guard",
        "impact_clarity",
        "report_support",
        "graph_connectivity",
    ]
    summary = {"card_count": len(rows), "averages": {}, "score_counts": {}}
    for field in fields:
        values = [row["scores"][field] for row in rows]
        summary["averages"][field] = round(sum(values) / len(values), 3) if values else 0
        summary["score_counts"][field] = dict(sorted(Counter(values).items()))
    return summary


def render_report(
    baseline: dict[str, Any],
    mappings: list[dict[str, Any]],
    unresolved: list[dict[str, Any]],
    manifest_source: str,
    reports_dir: str | None,
) -> str:
    confidence_counts = Counter()
    for item in mappings:
        for ref in item.get("report_refs", []):
            confidence_counts[ref.get("confidence", "unknown")] += 1
    lines = [
        "# Hunt Card Enrichment Inventory",
        "",
        f"- Manifest source: `{manifest_source}`",
        f"- Cards processed: {baseline['summary']['card_count']}",
        f"- Reports dir: `{reports_dir or 'not provided'}`",
        f"- Cards with unresolved report map: {len(unresolved)}",
        f"- Report refs by confidence: {dict(sorted(confidence_counts.items()))}",
        "",
        "## Quality Averages",
        "",
    ]
    for key, value in baseline["summary"]["averages"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Lowest Scoring Cards", ""])
    ranked = sorted(
        baseline["cards"],
        key=lambda row: (
            sum(v for k, v in row["scores"].items() if isinstance(v, int)),
            row["id"],
        ),
    )[:20]
    for row in ranked:
        score_sum = sum(v for k, v in row["scores"].items() if isinstance(v, int))
        lines.append(f"- `{row['id']}` ({score_sum}/21): {row['title']}")
    lines.extend(["", "## Unresolved Sample", ""])
    for row in unresolved[:20]:
        lines.append(f"- `{row['card_id']}`: {row['title']} ({row['db_ref']}:{row['lines']})")
    lines.append("")
    return "\n".join(lines)


def render_checklist(
    baseline: dict[str, Any],
    mappings: list[dict[str, Any]],
    unresolved: list[dict[str, Any]],
    manifest_source: str,
    reports_dir: str | None,
) -> str:
    """Render a DB-local progress checklist grouped by canonical source file."""
    unresolved_ids = {row["card_id"] for row in unresolved}
    mapping_by_id = {row["card_id"]: row for row in mappings}
    cards_by_ref: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in baseline["cards"]:
        cards_by_ref[str(row.get("ref") or "UNKNOWN")].append(row)

    lines = [
        "# Hunt Card Enrichment Checklist",
        "",
        "This is the durable DB-local tracker for report-backed hunt-card enrichment.",
        "Generated hunt-card JSON must not be edited by hand; mark work complete only after fixing canonical `DB/**/*.md` source and regenerating manifests.",
        "",
        f"- Manifest source: `{manifest_source}`",
        f"- Reports dir used for latest mapping: `{reports_dir or 'not provided'}`",
        f"- Cards tracked: {baseline['summary']['card_count']}",
        f"- Cards still missing explicit/strong report mapping: {len(unresolved)}",
        "",
        "## Status Legend",
        "",
        "- `[x]` Source has report-backed triage fields and the card has explicit/strong report mapping.",
        "- `[ ]` Source still needs report-backed enrichment or report mapping.",
        "",
        "## Source File Checklist",
        "",
    ]

    for ref in sorted(cards_by_ref):
        rows = sorted(cards_by_ref[ref], key=lambda item: str(item.get("id")))
        done_count = 0
        lines.append(f"### `{ref}`")
        lines.append("")
        for row in rows:
            card_id = row.get("id")
            mapping = mapping_by_id.get(card_id, {})
            has_mapping = card_id not in unresolved_ids
            has_triage = bool(row.get("validWhen") and (row.get("invalidWhen") or row.get("falsePositiveSignals")))
            has_report_evidence = bool(row.get("reportEvidence") or mapping.get("report_refs"))
            done = has_mapping and has_triage and has_report_evidence
            if done:
                done_count += 1
            mark = "x" if done else " "
            score_sum = sum(v for k, v in row["scores"].items() if isinstance(v, int))
            lines.append(
                f"- [{mark}] `{card_id}` ({score_sum}/21) {row.get('title')} "
                f"- lines {row.get('lines')}"
            )
        lines.append("")
        lines.append(f"Progress: {done_count}/{len(rows)} cards source-enriched for this file.")
        lines.append("")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, help="Process at most N cards after filtering.")
    parser.add_argument("--manifest", help="Hunt-card manifest name, for example tokens or all.")
    parser.add_argument("--reports-dir", type=Path, help="Optional reports directory for weak candidate inference.")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR, help="Output directory.")
    parser.add_argument("--checklist", type=Path, default=DEFAULT_CHECKLIST, help="DB-local checklist path.")
    parser.add_argument(
        "--pilot-erc4626",
        action="store_true",
        help="Focus on ERC4626/vault inflation cards and default to reports/erc4626_findings.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.pilot_erc4626:
        args.reports_dir = args.reports_dir or Path("reports/erc4626_findings")
    out_dir = args.out_dir if args.out_dir.is_absolute() else ROOT / args.out_dir

    cards, manifest_source = load_cards(args.manifest)
    if args.pilot_erc4626:
        cards = [card for card in cards if pilot_filter(card)]
    if args.limit:
        cards = cards[: args.limit]

    patterns = load_manifest_patterns()
    reports = load_reports(args.reports_dir)
    report_by_path = {report.path: report for report in reports}

    baseline_rows = []
    mappings = []
    unresolved = []
    for card in cards:
        pattern = pattern_for_card(card, patterns)
        lines = card.get("lines") or [0, 0]
        section, frontmatter = read_db_section(str(card.get("ref", "")), lines)
        section_metadata = extract_metadata(section, frontmatter)
        file_metadata = extract_metadata((ROOT / str(card.get("ref", ""))).read_text(encoding="utf-8", errors="replace")[:20000], frontmatter) if card.get("ref") and (ROOT / str(card.get("ref", ""))).exists() else {}
        refs = explicit_report_refs(section_metadata, file_metadata)
        refs = [enrich_report_ref(ref, report_by_path) for ref in refs]
        explicit_paths = {ref.get("path") for ref in refs if ref.get("path")}
        inferred = [ref for ref in candidate_reports(card, pattern, reports) if ref.get("path") not in explicit_paths]
        refs.extend(inferred)
        explicit_count = sum(1 for ref in refs if ref.get("confidence") == "explicit")
        scores = score_card(card, explicit_count)
        baseline_rows.append(
            {
                "id": card.get("id"),
                "title": card.get("title"),
                "severity": card.get("severity"),
                "grep": card.get("grep"),
                "detect": card.get("detect"),
                "check": card.get("check"),
                "antipattern": card.get("antipattern"),
                "securePattern": card.get("securePattern"),
                "validWhen": card.get("validWhen"),
                "invalidWhen": card.get("invalidWhen"),
                "impact": card.get("impact"),
                "ref": card.get("ref"),
                "lines": lines,
                "cat": card.get("cat"),
                "neverPrune": bool(card.get("neverPrune", False)),
                "matched_manifest_pattern": pattern.get("id"),
                "scores": scores,
            }
        )
        mapping = {
            "card_id": card.get("id"),
            "title": card.get("title"),
            "db_ref": card.get("ref"),
            "lines": lines,
            "section_metadata": section_metadata,
            "report_refs": refs,
            "unresolved": not any(ref.get("confidence") in {"explicit", "strong_semantic"} for ref in refs),
        }
        mappings.append(mapping)
        if mapping["unresolved"]:
            unresolved.append(
                {
                    "card_id": card.get("id"),
                    "title": card.get("title"),
                    "db_ref": card.get("ref"),
                    "lines": lines,
                    "candidate_refs": refs[:3],
                    "reason": "no explicit or strong_semantic report reference found",
                }
            )

    baseline = {
        "meta": {
            "manifest_source": manifest_source,
            "cards_processed": len(cards),
            "reports_dir": rel((args.reports_dir if args.reports_dir and args.reports_dir.is_absolute() else ROOT / args.reports_dir)) if args.reports_dir else None,
            "pilot_erc4626": bool(args.pilot_erc4626),
            "score_scale": {
                "0": "missing or unusable",
                "1": "weak, vague, or mostly structural",
                "2": "usable but incomplete",
                "3": "strong and directly executable",
            },
        },
        "summary": summarize_quality(baseline_rows),
        "cards": baseline_rows,
    }

    card_report_map = {
        "meta": {
            "manifest_source": manifest_source,
            "cards_processed": len(cards),
            "reports_loaded": len(reports),
            "reports_dir": rel((args.reports_dir if args.reports_dir and args.reports_dir.is_absolute() else ROOT / args.reports_dir)) if args.reports_dir else None,
            "max_report_files": MAX_REPORT_FILES,
            "report_read_limit": REPORT_READ_LIMIT,
        },
        "cards": mappings,
    }
    unresolved_map = {
        "meta": {"unresolved_count": len(unresolved), "cards_processed": len(cards)},
        "cards": unresolved,
    }

    write_json(out_dir / "baseline-quality.json", baseline)
    write_json(out_dir / "card-report-map.json", card_report_map)
    write_json(out_dir / "unresolved-report-map.json", unresolved_map)
    write_text(
        out_dir / "ENRICHMENT-REPORT.md",
        render_report(baseline, mappings, unresolved, manifest_source, card_report_map["meta"]["reports_dir"]),
    )
    checklist_path = args.checklist if args.checklist.is_absolute() else ROOT / args.checklist
    write_text(
        checklist_path,
        render_checklist(baseline, mappings, unresolved, manifest_source, card_report_map["meta"]["reports_dir"]),
    )

    print(f"processed_cards={len(cards)}")
    print(f"reports_loaded={len(reports)}")
    print(f"unresolved={len(unresolved)}")
    print(f"out_dir={rel(out_dir)}")
    print(f"checklist={rel(checklist_path)}")


if __name__ == "__main__":
    main()
