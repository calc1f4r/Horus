"""
Move (Sui / Aptos) AST extractor using tree-sitter-move.

Grammar source: varies — try 'tree-sitter-move' on PyPI or build from source.
Falls back to regex if unavailable.

Extracted edges:
  - Module declares Function / Struct / Constant
  - Function calls Function (same-module resolution)
  - Function reads_var / writes_var (local variable use on mutable refs)
  - Module imports (INFERRED reference edges)
  - hot_potato pattern detection → hyperedge
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Optional

from ..schema import Edge, ExtractionResult, Hyperedge, Node, make_node_id


def _load_parser():
    try:
        from tree_sitter import Language, Parser
        try:
            import tree_sitter_move as ts_move
            lang = Language(ts_move.language())
        except (ImportError, AttributeError):
            try:
                import tree_sitter_languages
                lang = tree_sitter_languages.get_language("move")
            except (ImportError, Exception):
                return None
        return Parser(lang)
    except Exception as exc:
        print(f"[move_sui] tree-sitter unavailable: {exc}", file=sys.stderr)
        return None


_PARSER = None


def _get_parser():
    global _PARSER
    if _PARSER is None:
        _PARSER = _load_parser()
    return _PARSER


def _node_text(node, src: bytes) -> str:
    return src[node.start_byte:node.end_byte].decode("utf-8", errors="replace").strip()


def _loc(node) -> dict:
    return {"line": node.start_point[0] + 1, "col": node.start_point[1]}


def _child_by_type(node, *types):
    for child in node.children:
        if child.type in types:
            return child
    return None


def _iter_nodes_by_type(node, target_type: str):
    if node.type == target_type:
        yield node
    for child in node.children:
        yield from _iter_nodes_by_type(child, target_type)


def extract(file_path: str, project_root: Optional[str] = None) -> ExtractionResult:
    parser = _get_parser()
    if parser is None:
        return _regex_fallback(file_path)

    src = Path(file_path).read_bytes()
    tree = parser.parse(src)
    rel_path = file_path
    result = ExtractionResult()

    fn_names: dict[str, str] = {}  # name → node_id

    for module_node in _iter_nodes_by_type(tree.root_node, "module_definition"):
        addr_node = _child_by_type(module_node, "module_identity", "address_literal")
        name_node = _child_by_type(module_node, "identifier")
        if not name_node:
            continue
        module_name = _node_text(name_node, src)
        module_id = make_node_id(rel_path, module_name)

        result.nodes.append(Node(
            id=module_id, label=module_name, node_kind="Module",
            source_file=rel_path, source_location=_loc(module_node),
        ))

        # use declarations → INFERRED references
        for use_node in _iter_nodes_by_type(module_node, "use_declaration"):
            used_text = _node_text(use_node, src).replace("use ", "").strip().rstrip(";")
            if "::" in used_text:
                imported_module = used_text.split("::")[0].split("::")[- 1].strip()
                ref_id = make_node_id(rel_path, imported_module)
                result.edges.append(Edge(
                    source=module_id, target=ref_id, relation="references",
                    confidence="INFERRED", confidence_score=0.9, unresolved=True,
                    source_file=rel_path, source_location=_loc(use_node),
                ))

        # Struct definitions
        for struct_node in _iter_nodes_by_type(module_node, "struct_definition"):
            st_name_node = _child_by_type(struct_node, "identifier")
            if not st_name_node:
                continue
            st_name = _node_text(st_name_node, src)
            st_id = make_node_id(rel_path, f"{module_name}_{st_name}")
            result.nodes.append(Node(
                id=st_id, label=f"{module_name}::{st_name}",
                node_kind="Struct", source_file=rel_path, source_location=_loc(struct_node),
            ))
            result.edges.append(Edge(
                source=module_id, target=st_id, relation="declares",
                source_file=rel_path, source_location=_loc(struct_node),
            ))

        # Function definitions
        for fn_node in _iter_nodes_by_type(module_node, "function_definition"):
            fn_name_node = _child_by_type(fn_node, "identifier")
            if not fn_name_node:
                continue
            fn_name = _node_text(fn_name_node, src)
            fn_id = make_node_id(rel_path, f"{module_name}_{fn_name}")
            fn_names[fn_name] = fn_id

            result.nodes.append(Node(
                id=fn_id, label=f"{module_name}::{fn_name}",
                node_kind="Function", source_file=rel_path, source_location=_loc(fn_node),
            ))
            result.edges.append(Edge(
                source=module_id, target=fn_id, relation="declares",
                source_file=rel_path, source_location=_loc(fn_node),
            ))

            # Calls within function body
            for call_node in _iter_nodes_by_type(fn_node, "call_expression"):
                called = _node_text(call_node, src).split("(")[0].split("::")[-1].strip()
                if called in fn_names:
                    result.edges.append(Edge(
                        source=fn_id, target=fn_names[called], relation="calls",
                        source_file=rel_path, source_location=_loc(call_node),
                    ))
                else:
                    ext_id = make_node_id(rel_path, f"external_{called}")
                    result.edges.append(Edge(
                        source=fn_id, target=ext_id, relation="calls",
                        unresolved=True, confidence_score=0.8,
                        source_file=rel_path, source_location=_loc(call_node),
                    ))

    # Hot-potato detection: structs that have no 'drop' ability
    # These are force-consumed and can be smuggled through interfaces
    _detect_hot_potato(result, src, rel_path)

    return result


def _detect_hot_potato(result: ExtractionResult, src: bytes, rel_path: str):
    """
    Move hot-potato structs have no 'drop' ability.
    Emit a hyperedge grouping them — relevant for capability-bypass patterns.
    """
    src_text = src.decode("utf-8", errors="replace")
    # Look for struct without drop ability
    hot_potato_structs = []
    for node in result.nodes:
        if not hasattr(node, 'node_kind'):
            continue
        if node.node_kind != "Struct":
            continue
        struct_name = node.label.split("::")[-1]
        pattern = re.compile(
            rf'\bstruct\s+{re.escape(struct_name)}\b(?![^{{]*\bdrop\b)', re.S
        )
        if pattern.search(src_text):
            hot_potato_structs.append(node.id)

    if len(hot_potato_structs) >= 2:
        result.hyperedges.append(Hyperedge(
            id=make_node_id(rel_path, "hot_potato_cluster"),
            label="Hot-potato structs (no drop ability)",
            nodes=hot_potato_structs,
            relation="participate_in",
            confidence="INFERRED",
            confidence_score=0.85,
            source_file=rel_path,
        ))


def _regex_fallback(file_path: str) -> ExtractionResult:
    result = ExtractionResult()
    src = Path(file_path).read_text(errors="ignore")
    rel_path = file_path

    for m in re.finditer(r'\bmodule\s+([\w:]+)\s*\{', src):
        mod_name = m.group(1).split("::")[-1]
        mod_id = make_node_id(rel_path, mod_name)
        result.nodes.append(Node(
            id=mod_id, label=mod_name, node_kind="Module",
            source_file=rel_path,
            source_location={"line": src[:m.start()].count("\n") + 1, "col": 0},
        ))

    for m in re.finditer(r'\bpublic\s+(?:entry\s+)?fun\s+(\w+)\s*[<(]', src):
        fn_name = m.group(1)
        fn_id = make_node_id(rel_path, fn_name)
        result.nodes.append(Node(
            id=fn_id, label=fn_name, node_kind="Function",
            source_file=rel_path,
            source_location={"line": src[:m.start()].count("\n") + 1, "col": 0},
        ))

    for m in re.finditer(r'\bstruct\s+(\w+)\b', src):
        st_name = m.group(1)
        st_id = make_node_id(rel_path, st_name)
        result.nodes.append(Node(
            id=st_id, label=st_name, node_kind="Struct",
            source_file=rel_path,
            source_location={"line": src[:m.start()].count("\n") + 1, "col": 0},
        ))

    return result
