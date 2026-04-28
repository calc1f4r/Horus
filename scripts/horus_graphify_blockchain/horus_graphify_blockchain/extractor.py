"""
Generic dispatcher and directory walker for blockchain AST extraction.

Usage:
    from horus_graphify_blockchain.extractor import extract_directory, extract_file
    result = extract_directory("/path/to/contracts")
    print(result.to_dict())  # graphify-compatible JSON
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Optional

from .detect import detect_language, iter_blockchain_files
from .schema import ExtractionResult


# Languages that have extractor modules available in this package.
_LANGUAGE_MODULE_MAP = {
    "solidity":   "horus_graphify_blockchain.languages.solidity",
    "move_sui":   "horus_graphify_blockchain.languages.move_sui",
    "move_aptos": "horus_graphify_blockchain.languages.move_sui",  # same grammar
    "move":       "horus_graphify_blockchain.languages.move_sui",
    "cairo":      "horus_graphify_blockchain.languages.cairo",
    # Phase 2b additions (stubs only for now):
    # "vyper":    "horus_graphify_blockchain.languages.vyper",
    # "sway":     "horus_graphify_blockchain.languages.sway",
    # "tact":     "horus_graphify_blockchain.languages.tact",
}


def _load_language_module(language: str):
    """
    Lazily import a language module.
    Returns None (with a stderr warning) if the module is unavailable
    or the grammar package isn't installed.
    """
    module_name = _LANGUAGE_MODULE_MAP.get(language)
    if not module_name:
        return None
    try:
        return importlib.import_module(module_name)
    except ImportError as exc:
        print(
            f"[hgb] Warning: language '{language}' unavailable ({exc}). "
            "Skipping AST extraction; graphify semantic extraction will still run.",
            file=sys.stderr,
        )
        return None


def extract_file(
    file_path: str | Path,
    language: Optional[str] = None,
    project_root: Optional[str | Path] = None,
) -> ExtractionResult:
    """
    Extract nodes and edges from a single blockchain source file.

    Args:
        file_path: Path to the source file.
        language: Override auto-detected language (e.g. "solidity").
        project_root: Root of the project (used for Move.toml dialect detection).

    Returns:
        ExtractionResult — empty if language is unsupported or grammar missing.
    """
    file_path = Path(file_path)
    if language is None:
        language = detect_language(file_path, project_root)
    if language is None:
        return ExtractionResult()

    module = _load_language_module(language)
    if module is None:
        return ExtractionResult()

    try:
        return module.extract(str(file_path), project_root=str(project_root) if project_root else None)
    except Exception as exc:
        print(f"[hgb] Warning: extraction failed for {file_path}: {exc}", file=sys.stderr)
        return ExtractionResult()


def extract_directory(
    directory: str | Path,
    project_root: Optional[str | Path] = None,
) -> ExtractionResult:
    """
    Walk a directory and extract all blockchain source files.

    Deduplicates nodes by ID (first occurrence wins).
    Returns a single merged ExtractionResult.
    """
    directory = Path(directory)
    if project_root is None:
        project_root = directory

    merged = ExtractionResult()
    seen_node_ids: set[str] = set()

    for file_path, language in iter_blockchain_files(directory):
        result = extract_file(file_path, language, project_root)

        for node in result.nodes:
            nid = node.id if hasattr(node, "id") else node.get("id", "")
            if nid and nid not in seen_node_ids:
                seen_node_ids.add(nid)
                merged.nodes.append(node)

        merged.edges.extend(result.edges)
        merged.hyperedges.extend(result.hyperedges)

    return merged
