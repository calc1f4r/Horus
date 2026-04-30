"""Keyword index builders for Horus retrieval generation."""

from __future__ import annotations

import re
from collections import defaultdict


KEYWORD_TITLE_STOP_WORDS = {
    "the", "a", "an", "in", "of", "for", "and", "or", "to",
    "is", "at", "by", "on", "with", "via", "using", "from",
    "example", "pattern", "vulnerable", "secure", "implementation",
    "analysis", "impact", "overview", "description", "fix",
    "detection", "prevention", "guidelines", "checklist",
    "references", "keywords", "search", "related", "table",
    "contents", "vulnerabilities", "vulnerability",
}


def build_quick_keywords(manifests):
    """Build a compact keyword → manifest mapping, saved as separate file."""
    keyword_to_manifests = defaultdict(set)

    for cat_name, manifest in manifests.items():
        for file_entry in manifest["files"]:
            path_parts = re.findall(r"[a-zA-Z][a-zA-Z0-9]{2,}", file_entry["file"])
            for part in path_parts:
                if part.lower() not in {"md", "db", "general", "vulnerabilities", "patterns"}:
                    keyword_to_manifests[part.lower()].add(cat_name)

            for pattern in file_entry["patterns"]:
                for kw in pattern.get("codeKeywords", []):
                    keyword_to_manifests[kw.lower()].add(cat_name)
                for kw in pattern.get("searchKeywords", []):
                    keyword_to_manifests[kw.lower()].add(cat_name)
                for word in re.findall(r"[a-zA-Z][a-zA-Z0-9]{2,}", pattern["title"]):
                    if word.lower() not in KEYWORD_TITLE_STOP_WORDS:
                        keyword_to_manifests[word.lower()].add(cat_name)

    compact = {}
    for kw, cats in sorted(keyword_to_manifests.items()):
        compact[kw] = sorted(cats)

    return {
        "description": "Keyword → manifest names. Load manifest (DB/manifests/<name>.json) then search patterns.",
        "totalKeywords": len(compact),
        "mappings": compact,
    }
