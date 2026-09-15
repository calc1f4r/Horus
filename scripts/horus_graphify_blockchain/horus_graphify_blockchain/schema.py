"""
Common schema for blockchain AST extraction.

All extractors produce graphify-compatible nodes and edges using these types.
The JSON structure matches graphify's intermediate extract format (not the final
graph.json — use graphify merge-graphs to combine with graphify's own output).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional

from graphify.ids import make_id as graphify_make_id

# ── Node kinds ──────────────────────────────────────────────────────────────

NODE_KINDS = {
    "Module",       # contract / module / namespace (Solidity contract, Move module, Cairo contract)
    "Function",     # public/private/internal function or method
    "StateVar",     # storage variable / state field
    "Modifier",     # Solidity modifier, Move attribute, Cairo decorator
    "Event",        # emittable event
    "Struct",       # user-defined struct / type
    "ExternalCall", # call site to external/unknown target
    "Constant",     # top-level constant or enum value
}

# ── Edge relations (Graphify-compatible blockchain vocabulary) ────────────────
# Graphify keeps `relation` open-ended. These domain relations remain metadata
# on canonical node-link records and can be filtered by CLI/MCP consumers.

EDGE_RELATIONS = {
    "calls",          # function A calls function B
    "reads_var",      # function reads state var
    "writes_var",     # function writes state var
    "inherits",       # module inherits / extends another module
    "emits",          # function emits event
    "has_modifier",   # function has modifier / attribute
    "external_call",  # function makes an external call to unknown target
    "declares",       # module declares function / var / event / struct
}


# ── Data classes ─────────────────────────────────────────────────────────────

@dataclass
class Node:
    id: str
    label: str
    node_kind: str = "Function"
    file_type: str = "code"
    source_file: str = ""
    source_location: Optional[str] = None
    source_url: Optional[str] = None
    captured_at: Optional[str] = None
    author: Optional[str] = None
    contributor: Optional[str] = None

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None or k in ("id", "label", "file_type", "source_file")}


@dataclass
class Edge:
    source: str
    target: str
    relation: str
    confidence: str = "EXTRACTED"
    confidence_score: float = 1.0
    source_file: str = ""
    source_location: Optional[str] = None
    weight: float = 1.0
    unresolved: bool = False

    def to_dict(self) -> dict:
        d = asdict(self)
        if not self.unresolved:
            d.pop("unresolved", None)
        return {k: v for k, v in d.items() if v is not None or k in ("source", "target", "relation")}


@dataclass
class Hyperedge:
    id: str
    label: str
    nodes: list
    relation: str = "participate_in"
    confidence: str = "EXTRACTED"
    confidence_score: float = 0.9
    source_file: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ExtractionResult:
    nodes: list = field(default_factory=list)
    edges: list = field(default_factory=list)
    hyperedges: list = field(default_factory=list)
    input_tokens: int = 0
    output_tokens: int = 0

    def merge(self, other: ExtractionResult) -> None:
        self.nodes.extend(other.nodes)
        self.edges.extend(other.edges)
        self.hyperedges.extend(other.hyperedges)

    def to_dict(self) -> dict:
        return {
            "nodes": [n.to_dict() if hasattr(n, "to_dict") else n for n in self.nodes],
            "edges": [e.to_dict() if hasattr(e, "to_dict") else e for e in self.edges],
            "hyperedges": [h.to_dict() if hasattr(h, "to_dict") else h for h in self.hyperedges],
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
        }


# ── ID helpers ───────────────────────────────────────────────────────────────

def make_node_id(file_path: str, entity_name: str) -> str:
    """
    Deterministic node ID matching Graphify 0.9's convention.

    The stem is the full project-relative path with its extension removed, not
    merely the filename. Delegating normalization to Graphify keeps Unicode and
    punctuation behavior identical to the upstream AST extractors.
    """
    path = Path(file_path)
    stem = path.with_suffix("").as_posix() if path.name else ""
    return graphify_make_id(stem, entity_name)


def project_relative_source(file_path: str | Path, project_root: str | Path | None) -> str:
    """Return a portable source path suitable for Graphify IDs and metadata."""
    path = Path(file_path)
    if project_root is None:
        return path.name if path.is_absolute() else path.as_posix()

    root = Path(project_root).resolve()
    resolved = path.resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError as exc:
        raise ValueError(f"{resolved} is outside project root {root}") from exc
