"""Manifest builders for Horus DB retrieval artifacts."""

from __future__ import annotations

import re
from pathlib import Path

from horus_retrieval.documents import DBDocument
from horus_retrieval.taxonomy import GENERAL_SUBCATEGORIES


IGNORED_MARKDOWN_FILES = {"README.md", "ARTIFACT_INDEX.md"}
IGNORED_DIRS = {"_drafts", "_telemetry", "graphify-out", "manifests", ".git", "__pycache__"}

STRUCTURAL_H2_TITLES = {
    "table of contents", "references", "references & source reports",
    "keywords for search", "related vulnerabilities", "prevention guidelines",
    "testing requirements", "security research", "technical documentation",
    "external links", "summary", "conclusion", "appendix",
    "development best practices", "reference", "change log",
    "vulnerability categories", "best practices", "agent quick view",
    "contract / boundary map", "valid bug signals", "false positive guards",
    "artifact location", "downloaded artifacts summary", "auditor coverage",
    "protocol coverage",
    "vulnerability description", "vulnerable pattern examples",
    "vulnerable patterns", "attack scenarios",
}

STRUCTURAL_H3_TITLES = STRUCTURAL_H2_TITLES | {
    "overview", "attack categories",
    "secure implementation", "detection patterns", "audit checklist",
    "code patterns to look for", "impact analysis", "technical impact",
    "business impact", "affected scenarios", "known exploits",
    "related cves/reports", "real-world examples", "sub-variant breakdown",
    "complete defihacklabs exploit table", "top poc references",
    "vulnerability description", "vulnerable pattern examples",
    "vulnerable patterns", "attack scenarios",
    "attack scenario / path variants",
}

TITLE_STOP_WORDS = {
    "the", "and", "for", "with", "from", "into", "over", "under",
    "pattern", "patterns", "category", "categories", "vulnerability",
    "vulnerabilities", "attack", "attacks", "example", "examples",
    "description", "secure", "implementation", "real", "world",
    "complete", "table", "references", "reference", "overview",
}

FRONTMATTER_CODE_FIELDS = (
    "code_keywords",
    "primitives",
    "affected_component",
    "bridge_attack_vector",
    "oracle_attack_vector",
)

FRONTMATTER_SEARCH_FIELDS = (
    "code_keywords",
    "primitives",
    "affected_component",
    "vulnerability_type",
    "root_cause_family",
    "pattern_key",
    "attack_type",
    "impact",
    "bridge_attack_vector",
    "oracle_attack_vector",
)


def merge_unique(items, limit=None):
    """Deduplicate strings while preserving order."""
    merged = []
    seen = set()

    for item in items:
        if item is None:
            continue
        cleaned = re.sub(r"\s+", " ", str(item).strip().strip('"').strip("'"))
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        merged.append(cleaned)
        if limit and len(merged) >= limit:
            break

    return merged


def iter_frontmatter_scalars(value):
    """Yield scalar text values from YAML frontmatter structures."""
    if value is None:
        return
    if isinstance(value, dict):
        for nested in value.values():
            yield from iter_frontmatter_scalars(nested)
        return
    if isinstance(value, (list, tuple, set)):
        for nested in value:
            yield from iter_frontmatter_scalars(nested)
        return

    text = str(value).strip().strip('"').strip("'")
    if text:
        yield text


def split_frontmatter_terms(value):
    """Split YAML frontmatter text on list-like separators."""
    for raw in iter_frontmatter_scalars(value):
        for fragment in re.split(r"[|,]", raw):
            cleaned = fragment.strip().strip('"').strip("'")
            if cleaned:
                yield cleaned


def humanize_identifier(text):
    """Convert snake_case / camelCase / namespaced identifiers into readable search terms."""
    if not text:
        return ""
    humanized = str(text)
    humanized = humanized.replace("::", " ").replace("/", " ").replace(".", " ")
    humanized = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", humanized)
    humanized = re.sub(r"[_-]+", " ", humanized)
    humanized = re.sub(r"\s+", " ", humanized)
    return humanized.strip().lower()


def extract_frontmatter_code_keywords(frontmatter):
    """Collect grep-friendly identifiers from structured frontmatter fields."""
    keywords = []
    for field in FRONTMATTER_CODE_FIELDS:
        for term in split_frontmatter_terms(frontmatter.get(field)):
            if len(term) >= 3 and " " not in term:
                keywords.append(term)
    return merge_unique(keywords, limit=24)


def extract_frontmatter_search_keywords(frontmatter):
    """Collect semantic search terms from frontmatter for manifest discovery."""
    keywords = []
    for field in FRONTMATTER_SEARCH_FIELDS:
        for term in split_frontmatter_terms(frontmatter.get(field)):
            if len(term) < 3:
                continue
            keywords.append(term.lower())
            humanized = humanize_identifier(term)
            if humanized and humanized != term.lower():
                keywords.append(humanized)
    return merge_unique(keywords, limit=40)


def extract_title_search_keywords(title):
    """Turn section titles into compact semantic search hints."""
    cleaned = re.sub(r"\[[^\]]*\]", "", title)
    cleaned = re.sub(r"\([^\)]*\)", "", cleaned)
    cleaned = re.sub(r"^(?:pattern|category)\s+\d+(?:\.\d+)*\s*:\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^\d+(?:\.\d+)*\s*[:.)-]?\s*", "", cleaned)
    humanized = humanize_identifier(cleaned)
    tokens = [
        token for token in re.findall(r"[a-z][a-z0-9]{2,}", humanized)
        if token not in TITLE_STOP_WORDS
    ]

    keywords = []
    if tokens:
        keywords.extend(tokens)
        if len(tokens) <= 6:
            keywords.append(" ".join(tokens))
            for idx in range(len(tokens) - 1):
                keywords.append(f"{tokens[idx]} {tokens[idx + 1]}")

    return merge_unique(keywords, limit=16)


def build_graph_hints(pattern_title, search_keywords, frontmatter, subsections):
    """Build compact graph expansion hints from semantic DB metadata."""
    variants = []
    composes = []

    for term in search_keywords or []:
        lower = str(term).lower()
        if any(marker in lower for marker in ("variant", "inflation", "donation", "replay", "rounding", "staleness", "manipulation")):
            variants.append(term)
        if any(marker in lower for marker in ("flash loan", "reentrancy", "oracle", "callback", "bridge", "slippage", "liquidation")):
            composes.append(term)

    for field in ("root_cause_family", "attack_type", "pattern_key", "vulnerability_type"):
        for term in split_frontmatter_terms(frontmatter.get(field)):
            humanized = humanize_identifier(term)
            if humanized:
                variants.append(humanized)

    for field in ("primitives", "affected_component"):
        for term in split_frontmatter_terms(frontmatter.get(field)):
            humanized = humanize_identifier(term)
            if humanized:
                composes.append(humanized)

    for child in subsections or []:
        title = child.get("title", "")
        if title:
            variants.extend(extract_title_search_keywords(title)[:2])

    title_terms = extract_title_search_keywords(pattern_title)
    variants.extend(title_terms[:3])

    hints = {}
    variant_values = merge_unique(variants, limit=5)
    compose_values = merge_unique(composes, limit=5)
    if variant_values:
        hints["variants"] = variant_values
    if compose_values:
        hints["commonlyComposesWith"] = compose_values
    return hints or None


def parse_md_file(filepath):
    """Parse a markdown file and extract all headings with line ranges."""
    document = DBDocument.from_path(filepath)
    return document.manifest_sections(), list(document.lines)


def generate_pattern_id(category, filename, section_title, idx):
    """Generate a unique pattern ID."""
    file_slug = re.sub(r"[^a-z0-9]+", "-", filename.lower()).strip("-")[:40]
    title_slug = re.sub(r"[^a-z0-9]+", "-", section_title.lower()).strip("-")[:30]
    return f"{category}-{file_slug}-{title_slug}-{idx:03d}"


def build_file_manifest(filepath, category, *, db_root: Path):
    """Build manifest entry for a single file."""
    rel_path = str(filepath.relative_to(db_root.parent))
    document = DBDocument.from_path(filepath)
    sections = document.manifest_sections()
    lines = list(document.lines)

    if not sections:
        return None

    frontmatter = document.frontmatter
    frontmatter_code_keywords = extract_frontmatter_code_keywords(frontmatter)
    frontmatter_search_keywords = extract_frontmatter_search_keywords(frontmatter)
    file_report_evidence = document.report_references()

    def is_h2_vulnerability(sec):
        title_lower = sec["title"].lower().strip()
        if title_lower in STRUCTURAL_H2_TITLES:
            return False
        if sec["lineCount"] < 8:
            return False
        return True

    def is_h3_vulnerability(sec):
        title_lower = sec["title"].lower().strip()
        if title_lower in STRUCTURAL_H3_TITLES:
            return False
        if sec["lineCount"] < 5:
            return False
        return True

    patterns = []
    h2_sections = [s for s in sections if s["heading_level"] == 2 and is_h2_vulnerability(s)]
    h3_all = [s for s in sections if s["heading_level"] == 3 and is_h3_vulnerability(s)]
    h4_all = [s for s in sections if s["heading_level"] == 4 and s["lineCount"] >= 5]

    primary_sections = h2_sections[:]
    if not h2_sections and h3_all:
        primary_sections = h3_all[:]

    all_h2 = [s for s in sections if s["heading_level"] == 2]
    vuln_title_h2 = [s for s in all_h2 if s["title"].lower().strip() == "vulnerability title"]
    if len(all_h2) <= 2 and len(vuln_title_h2) == 1 and h3_all:
        primary_sections = h3_all[:]
    elif primary_sections:
        expanded_sections = []
        for sec in primary_sections:
            child_h3 = [
                h3 for h3 in h3_all
                if h3["lineStart"] > sec["lineStart"] and h3["lineEnd"] <= sec["lineEnd"]
            ]
            title_lower = sec["title"].lower().strip()
            should_promote_children = (
                len(child_h3) >= 2
                and (
                    title_lower.endswith("vulnerabilities")
                    or "pattern" in title_lower
                    or "categories" in title_lower
                    or "examples" in title_lower
                )
            )
            if should_promote_children:
                expanded_sections.extend(child_h3)
            else:
                expanded_sections.append(sec)
        primary_sections = expanded_sections

    for idx, sec in enumerate(primary_sections):
        pattern_id = generate_pattern_id(category, filepath.stem, sec["title"], idx)
        child_pool = h3_all if sec["heading_level"] == 2 else h4_all

        children = []
        child_title_search_keywords = []
        for child in child_pool:
            if child["lineStart"] > sec["lineStart"] and child["lineEnd"] <= sec["lineEnd"]:
                child_search_keywords = extract_title_search_keywords(child["title"])
                child_title_search_keywords.extend(child_search_keywords)
                children.append(
                    {
                        "title": child["title"],
                        "lineStart": child["lineStart"],
                        "lineEnd": child["lineEnd"],
                        "severity": child["severity"],
                        "codeKeywords": child["codeKeywords"][:8],
                        "searchKeywords": child_search_keywords[:12] if child_search_keywords else None,
                    }
                )

        pattern_code_keywords = merge_unique(sec["codeKeywords"] + frontmatter_code_keywords, limit=20)
        pattern_search_keywords = merge_unique(
            extract_title_search_keywords(sec["title"]) + child_title_search_keywords + frontmatter_search_keywords,
            limit=32,
        )
        section_report_evidence = document.report_references(sec["lineStart"], sec["lineEnd"])
        report_evidence = section_report_evidence or file_report_evidence
        graph_hints = build_graph_hints(sec["title"], pattern_search_keywords, frontmatter, children)

        pattern = {
            "id": pattern_id,
            "title": sec["title"],
            "lineStart": sec["lineStart"],
            "lineEnd": sec["lineEnd"],
            "lineCount": sec["lineCount"],
            "severity": sec["severity"],
            "codeKeywords": pattern_code_keywords,
            "searchKeywords": pattern_search_keywords,
            "rootCause": sec["rootCause"],
            "subsections": children if children else None,
        }
        if report_evidence:
            pattern["reportEvidence"] = report_evidence
        if graph_hints:
            pattern["graphHints"] = graph_hints
        patterns.append(pattern)

    return {
        "file": rel_path,
        "totalLines": len(lines),
        "frontmatter": frontmatter if frontmatter else None,
        "patternCount": len(patterns),
        "patterns": patterns,
    }


def collect_files_for_category(category, folders, *, db_root: Path):
    """Collect all .md files for a category."""
    files = []
    for folder_name in folders:
        folder = db_root / folder_name
        if folder.exists():
            for md_file in sorted(folder.rglob("*.md")):
                if md_file.name in IGNORED_MARKDOWN_FILES:
                    continue
                if any(part in IGNORED_DIRS for part in md_file.parts):
                    continue
                files.append(md_file)
    return files


def build_manifest(category, folders, *, db_root: Path):
    """Build complete manifest for a category."""
    files = collect_files_for_category(category, folders, db_root=db_root)
    entries = []
    total_patterns = 0

    for file_path in files:
        entry = build_file_manifest(file_path, category, db_root=db_root)
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


def build_general_sub_manifests(*, db_root: Path):
    """Split general/ into focused sub-manifests for agent precision."""
    sub_manifests = {}
    general_dir = db_root / "general"

    for sub_name, sub_config in GENERAL_SUBCATEGORIES.items():
        entries = []
        total_patterns = 0

        for subfolder in sub_config["folders"]:
            folder = general_dir / subfolder
            if folder.exists():
                for md_file in sorted(folder.rglob("*.md")):
                    if md_file.name in IGNORED_MARKDOWN_FILES:
                        continue
                    if any(part in IGNORED_DIRS for part in md_file.parts):
                        continue
                    entry = build_file_manifest(md_file, sub_name, db_root=db_root)
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
