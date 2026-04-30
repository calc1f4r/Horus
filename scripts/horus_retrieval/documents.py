"""Markdown document parsing for Horus DB entries."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class DBSection:
    title: str
    heading_level: int
    line_start: int
    line_end: int
    line_count: int
    hierarchy: tuple[str, ...]
    severity: tuple[str, ...]
    code_keywords: tuple[str, ...]
    root_cause: str | None

    def as_manifest_section(self) -> dict:
        return {
            "title": self.title,
            "heading_level": self.heading_level,
            "lineStart": self.line_start,
            "lineEnd": self.line_end,
            "lineCount": self.line_count,
            "hierarchy": list(self.hierarchy),
            "severity": list(self.severity),
            "codeKeywords": list(self.code_keywords),
            "rootCause": self.root_cause,
        }


@dataclass(frozen=True)
class DBDocument:
    path: Path
    lines: tuple[str, ...]
    frontmatter: dict
    sections: tuple[DBSection, ...]

    @classmethod
    def from_path(cls, path: Path) -> "DBDocument":
        lines = tuple(path.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True))
        content = "".join(lines)
        return cls(
            path=path,
            lines=lines,
            frontmatter=parse_frontmatter(content),
            sections=tuple(parse_sections(lines)),
        )

    @property
    def content(self) -> str:
        return "".join(self.lines)

    def manifest_sections(self) -> list[dict]:
        return [section.as_manifest_section() for section in self.sections]

    def report_references(self, line_start: int | None = None, line_end: int | None = None) -> dict | None:
        start = line_start - 1 if line_start is not None else None
        end = line_end if line_end is not None else None
        return extract_report_references(self.lines, start, end)


def extract_severity_from_context(lines, start, end):
    """Extract severity hints from lines near a heading."""
    severities = set()
    text = "\n".join(lines[start:min(end, start + 40)])
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

    for m in re.finditer(r"`([a-zA-Z_][a-zA-Z0-9_.:()]{2,50})`", text):
        keywords.add(m.group(1).rstrip("()"))

    for m in re.finditer(r"function\s+(\w+)\s*\(", text):
        keywords.add(m.group(1))

    return sorted(keywords)[:15]


def extract_root_cause(lines, start, end):
    """Try to extract a root cause snippet from the section."""
    text = "\n".join(lines[start:min(end, len(lines))])
    m = re.search(
        r"(?:root\s*cause|fundamental\s*issue)[:\s]*\n+(.*?)(?:\n#|\n\*\*|\Z)",
        text,
        re.IGNORECASE | re.DOTALL,
    )
    if m:
        snippet = m.group(1).strip()[:200]
        return snippet if snippet else None

    m = re.search(r"❌\s*VULNERABLE[:\s]*(.*)", text)
    if m:
        return m.group(1).strip()[:200]
    return None


def parse_frontmatter(content):
    """Parse YAML frontmatter from a markdown document."""
    data, _errors = parse_frontmatter_with_errors(content)
    return data or {}


def split_frontmatter(content):
    """Return parsed frontmatter plus body text without the frontmatter block."""
    fm_match = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", content, re.DOTALL)
    if not fm_match:
        return {}, content
    return parse_frontmatter(content), content[fm_match.end():]


def parse_frontmatter_with_errors(content):
    """Parse YAML frontmatter and return `(data, errors)` for quality tooling."""
    fm_match = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", content, re.DOTALL)
    if not fm_match:
        return None, []
    try:
        data = yaml.safe_load(fm_match.group(1)) or {}
    except yaml.YAMLError as exc:
        return None, [f"YAML parse error: {str(exc)[:80]}"]
    return data if isinstance(data, dict) else {}, []


def extract_report_references(lines, start=None, end=None):
    """Extract compact local report references from markdown lines."""
    selected = lines[slice(start, end)] if start is not None or end is not None else lines
    refs = []
    severity_counts = {}

    for line in selected:
        report_paths = re.findall(r"`?(reports/[^`\s|)]+\.md)`?", line)
        if not report_paths:
            continue

        severity = ""
        m = re.search(r"\b(CRITICAL|HIGH|MEDIUM|LOW|MID)\b", line, re.IGNORECASE)
        if m:
            severity = m.group(1).upper()
            if severity == "MID":
                severity = "MEDIUM"
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        for path in report_paths:
            refs.append(
                {
                    "path": path,
                    "severity": severity or None,
                }
            )

    deduped = []
    seen = set()
    for ref in refs:
        path = ref["path"]
        if path in seen:
            continue
        seen.add(path)
        deduped.append(ref)

    if not deduped:
        return None

    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    severity_consensus = ""
    if severity_counts:
        severity_consensus = sorted(
            severity_counts,
            key=lambda sev: (-severity_counts[sev], severity_order.get(sev, 99)),
        )[0]

    evidence = {
        "count": len(deduped),
        "sampleReports": [ref["path"] for ref in deduped[:5]],
    }
    if severity_consensus:
        evidence["severityConsensus"] = severity_consensus
    return evidence


def parse_sections(lines) -> list[DBSection]:
    sections = []
    heading_stack = []

    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            heading_stack.append((level, title, i + 1))

    for idx, (level, title, line_num) in enumerate(heading_stack):
        end_line = len(lines)
        for next_idx in range(idx + 1, len(heading_stack)):
            if heading_stack[next_idx][0] <= level:
                end_line = heading_stack[next_idx][2] - 1
                break

        ancestors = []
        current_level = level
        for prev_idx in range(idx - 1, -1, -1):
            if heading_stack[prev_idx][0] < current_level:
                ancestors.insert(0, heading_stack[prev_idx][1])
                current_level = heading_stack[prev_idx][0]

        sections.append(
            DBSection(
                title=title,
                heading_level=level,
                line_start=line_num,
                line_end=end_line,
                line_count=end_line - line_num + 1,
                hierarchy=tuple(ancestors),
                severity=tuple(extract_severity_from_context(lines, line_num - 1, end_line)),
                code_keywords=tuple(extract_keywords_from_context(lines, line_num - 1, end_line)),
                root_cause=extract_root_cause(lines, line_num - 1, end_line),
            )
        )

    return sections
