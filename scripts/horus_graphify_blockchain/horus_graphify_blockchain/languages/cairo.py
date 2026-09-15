"""
Cairo 1.x (Starknet) AST extractor using tree-sitter-cairo.

Grammar source: https://github.com/starkware-libs/tree-sitter-cairo
Install: pip install tree-sitter-cairo  (if available)

Extracted edges:
  - Module declares Function / Struct / Storage / Event
  - Function calls Function (same-contract resolution)
  - Function reads_var / writes_var on #[storage] fields
  - Function emits Event
  - Contract Component usage → hyperedge
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
            import tree_sitter_cairo as ts_cairo
            lang = Language(ts_cairo.language())
        except (ImportError, AttributeError):
            try:
                import tree_sitter_languages
                lang = tree_sitter_languages.get_language("cairo")
            except (ImportError, Exception):
                return None
        return Parser(lang)
    except Exception as exc:
        print(f"[cairo] tree-sitter unavailable: {exc}", file=sys.stderr)
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

    fn_names: dict[str, str] = {}
    storage_vars: dict[str, str] = {}
    event_names: dict[str, str] = {}
    component_uses: list[str] = []

    # Cairo 1.x: top-level items are mod_item, trait_item, impl_item, function_declaration
    for top in tree.root_node.children:
        ttype = top.type

        # #[starknet::contract] mod
        if ttype in ("mod_item", "module_definition"):
            name_node = _child_by_type(top, "identifier")
            if not name_node:
                continue
            mod_name = _node_text(name_node, src)
            mod_id = make_node_id(rel_path, mod_name)
            result.nodes.append(Node(
                id=mod_id, label=mod_name, node_kind="Module",
                source_file=rel_path, source_location=_loc(top),
            ))

            # Look inside for Storage struct, events, impls, functions
            _walk_cairo_mod(top, mod_id, mod_name, src, rel_path, result,
                            fn_names, storage_vars, event_names, component_uses)

        # Top-level function
        elif ttype in ("function_declaration", "function_definition", "function_item"):
            fn_name_node = _child_by_type(top, "identifier")
            if fn_name_node:
                fn_name = _node_text(fn_name_node, src)
                fn_id = make_node_id(rel_path, fn_name)
                fn_names[fn_name] = fn_id
                result.nodes.append(Node(
                    id=fn_id, label=fn_name, node_kind="Function",
                    source_file=rel_path, source_location=_loc(top),
                ))

    # Component cluster hyperedge
    if len(component_uses) >= 2:
        result.hyperedges.append(Hyperedge(
            id=make_node_id(rel_path, "component_cluster"),
            label="Starknet components used by this contract",
            nodes=component_uses,
            relation="participate_in",
            confidence="INFERRED",
            confidence_score=0.85,
            source_file=rel_path,
        ))

    return result


def _walk_cairo_mod(mod_node, mod_id: str, mod_name: str, src: bytes,
                    rel_path: str, result: ExtractionResult,
                    fn_names: dict, storage_vars: dict, event_names: dict,
                    component_uses: list):
    """Walk inside a Cairo contract module."""
    for child in mod_node.children:
        ctype = child.type

        # Storage struct (#[storage])
        if ctype in ("struct_item", "struct_definition"):
            st_name_node = _child_by_type(child, "type_identifier", "identifier")
            if not st_name_node:
                continue
            st_name = _node_text(st_name_node, src)
            if st_name.lower() == "storage":
                # Extract storage fields as StateVar nodes
                for field in _iter_nodes_by_type(child, "field_declaration", "named_field_definition"):
                    f_name_node = _child_by_type(field, "identifier", "field_identifier")
                    if f_name_node:
                        f_name = _node_text(f_name_node, src)
                        sv_id = make_node_id(rel_path, f"{mod_name}_{f_name}")
                        storage_vars[f_name] = sv_id
                        result.nodes.append(Node(
                            id=sv_id, label=f"{mod_name}.Storage.{f_name}",
                            node_kind="StateVar", source_file=rel_path, source_location=_loc(field),
                        ))
                        result.edges.append(Edge(
                            source=mod_id, target=sv_id, relation="declares",
                            source_file=rel_path, source_location=_loc(field),
                        ))
            else:
                # Regular struct
                st_id = make_node_id(rel_path, f"{mod_name}_{st_name}")
                result.nodes.append(Node(
                    id=st_id, label=f"{mod_name}::{st_name}", node_kind="Struct",
                    source_file=rel_path, source_location=_loc(child),
                ))
                result.edges.append(Edge(
                    source=mod_id, target=st_id, relation="declares",
                    source_file=rel_path, source_location=_loc(child),
                ))

        # Events enum
        elif ctype in ("enum_item", "enum_definition"):
            ev_name_node = _child_by_type(child, "type_identifier", "identifier")
            if ev_name_node:
                ev_name = _node_text(ev_name_node, src)
                ev_id = make_node_id(rel_path, f"{mod_name}_{ev_name}")
                event_names[ev_name] = ev_id
                result.nodes.append(Node(
                    id=ev_id, label=f"{mod_name}::{ev_name}", node_kind="Event",
                    source_file=rel_path, source_location=_loc(child),
                ))
                result.edges.append(Edge(
                    source=mod_id, target=ev_id, relation="declares",
                    source_file=rel_path, source_location=_loc(child),
                ))

        # impl block → extract functions
        elif ctype in ("impl_item", "impl_definition"):
            for item in child.children:
                if item.type in ("function_declaration", "function_definition", "function_item"):
                    _walk_cairo_fn(item, mod_id, mod_name, src, rel_path, result,
                                   fn_names, storage_vars, event_names)

        # Component usage (component!(...)  or  use OZOwnable::*)
        elif ctype == "use_declaration":
            use_text = _node_text(child, src)
            if "component" in use_text.lower() or "::Component" in use_text:
                comp_name = use_text.split("::")[-1].strip().rstrip(";")
                comp_id = make_node_id(rel_path, comp_name)
                component_uses.append(comp_id)
                result.nodes.append(Node(
                    id=comp_id, label=comp_name, node_kind="Module",
                    source_file=rel_path, source_location=_loc(child),
                ))
                result.edges.append(Edge(
                    source=mod_id, target=comp_id, relation="references",
                    confidence="INFERRED", confidence_score=0.8, unresolved=True,
                    source_file=rel_path, source_location=_loc(child),
                ))

        # Recurse for nested mods
        _walk_cairo_mod(child, mod_id, mod_name, src, rel_path, result,
                        fn_names, storage_vars, event_names, component_uses)


def _walk_cairo_fn(fn_node, mod_id: str, mod_name: str, src: bytes,
                   rel_path: str, result: ExtractionResult,
                   fn_names: dict, storage_vars: dict, event_names: dict):
    fn_name_node = _child_by_type(fn_node, "identifier")
    if not fn_name_node:
        return
    fn_name = _node_text(fn_name_node, src)
    fn_id = make_node_id(rel_path, f"{mod_name}_{fn_name}")
    fn_names[fn_name] = fn_id

    result.nodes.append(Node(
        id=fn_id, label=f"{mod_name}::{fn_name}",
        node_kind="Function", source_file=rel_path, source_location=_loc(fn_node),
    ))
    result.edges.append(Edge(
        source=mod_id, target=fn_id, relation="declares",
        source_file=rel_path, source_location=_loc(fn_node),
    ))

    # Body: look for self.storage.<field>.read/write calls and internal calls
    for call_node in _iter_nodes_by_type(fn_node, "call_expression"):
        call_text = _node_text(call_node, src)
        # self.storage.<field>.write/read
        storage_write = re.search(r'self\.storage\.(\w+)\.write', call_text)
        storage_read  = re.search(r'self\.storage\.(\w+)\.read', call_text)
        if storage_write:
            field = storage_write.group(1)
            if field in storage_vars:
                result.edges.append(Edge(
                    source=fn_id, target=storage_vars[field], relation="writes_var",
                    source_file=rel_path, source_location=_loc(call_node),
                ))
        elif storage_read:
            field = storage_read.group(1)
            if field in storage_vars:
                result.edges.append(Edge(
                    source=fn_id, target=storage_vars[field], relation="reads_var",
                    source_file=rel_path, source_location=_loc(call_node),
                ))
        # emit event
        elif "emit" in call_text.lower():
            ev_match = re.search(r'emit\s*\(\s*(\w+)', call_text)
            if ev_match:
                ev_name = ev_match.group(1)
                if ev_name in event_names:
                    result.edges.append(Edge(
                        source=fn_id, target=event_names[ev_name], relation="emits",
                        source_file=rel_path, source_location=_loc(call_node),
                    ))
        else:
            # Internal call
            call_name = call_text.split("(")[0].split("::")[-1].strip()
            if call_name in fn_names:
                result.edges.append(Edge(
                    source=fn_id, target=fn_names[call_name], relation="calls",
                    source_file=rel_path, source_location=_loc(call_node),
                ))


def _regex_fallback(file_path: str) -> ExtractionResult:
    result = ExtractionResult()
    src = Path(file_path).read_text(errors="ignore")
    rel_path = file_path

    for m in re.finditer(r'\bmod\s+(\w+)\s*\{', src):
        mod_name = m.group(1)
        result.nodes.append(Node(
            id=make_node_id(rel_path, mod_name), label=mod_name, node_kind="Module",
            source_file=rel_path,
            source_location={"line": src[:m.start()].count("\n") + 1, "col": 0},
        ))

    for m in re.finditer(r'\bfn\s+(\w+)\s*[<(]', src):
        fn_name = m.group(1)
        result.nodes.append(Node(
            id=make_node_id(rel_path, fn_name), label=fn_name, node_kind="Function",
            source_file=rel_path,
            source_location={"line": src[:m.start()].count("\n") + 1, "col": 0},
        ))

    for m in re.finditer(r'\bstruct\s+(\w+)\b', src):
        st_name = m.group(1)
        result.nodes.append(Node(
            id=make_node_id(rel_path, st_name), label=st_name, node_kind="Struct",
            source_file=rel_path,
            source_location={"line": src[:m.start()].count("\n") + 1, "col": 0},
        ))

    return result
