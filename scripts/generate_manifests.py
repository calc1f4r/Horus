#!/usr/bin/env python3
"""
Manifest Generator for Horus
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

from horus_retrieval.build import DEFAULT_DB_DIR, build_retrieval_db
from horus_retrieval.huntcards import (
    build_huntcard as _build_huntcard,
    build_huntcards_for_manifest as _build_huntcards_for_manifest,
    extract_identifiers_from_content as _extract_identifiers_from_content,
    select_best_grep_keywords as _select_best_grep_keywords,
    truncate_to_sentence as _truncate_to_sentence,
)
from horus_retrieval.manifests import (
    build_file_manifest as _build_file_manifest,
    build_general_sub_manifests as _build_general_sub_manifests,
    build_manifest as _build_manifest,
    collect_files_for_category as _collect_files_for_category,
)

DB_DIR = DEFAULT_DB_DIR
MANIFEST_DIR = DB_DIR / "manifests"

def build_file_manifest(filepath, category):
    return _build_file_manifest(filepath, category, db_root=DB_DIR)


def collect_files_for_category(category, folders):
    return _collect_files_for_category(category, folders, db_root=DB_DIR)


def build_manifest(category, folders):
    return _build_manifest(category, folders, db_root=DB_DIR)


HUNTCARDS_DIR = MANIFEST_DIR / "huntcards"

def truncate_to_sentence(text, max_len=120):
    return _truncate_to_sentence(text, max_len)


def extract_identifiers_from_content(file_path, line_start, line_end, max_keywords=6):
    return _extract_identifiers_from_content(
        file_path,
        line_start,
        line_end,
        max_keywords,
        db_root=DB_DIR,
    )


def select_best_grep_keywords(keywords, max_count=6):
    return _select_best_grep_keywords(keywords, max_count)


def build_huntcard(pattern, file_path, manifest_name=""):
    return _build_huntcard(pattern, file_path, manifest_name, db_root=DB_DIR)


def build_huntcards_for_manifest(manifest_name, manifest_data):
    return _build_huntcards_for_manifest(manifest_name, manifest_data, db_root=DB_DIR)


def build_general_sub_manifests():
    return _build_general_sub_manifests(db_root=DB_DIR)


def main():
    build_retrieval_db(db_dir=DB_DIR)


if __name__ == "__main__":
    main()
