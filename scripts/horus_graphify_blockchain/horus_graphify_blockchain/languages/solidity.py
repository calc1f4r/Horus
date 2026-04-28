"""
Solidity AST extractor using tree-sitter-solidity.

Grammar source: https://github.com/JoranHonig/tree-sitter-solidity
Install: pip install tree-sitter-solidity  (or pip install tree-sitter-languages)

Extracted edges (all EXTRACTED, confidence_score=1.0):
  - Module declares Function / StateVar / Event / Struct / Modifier / Constant
  - Module inherits Module
  - Function calls Function (same-file resolution; unresolved=True for external)
  - Function reads_var / writes_var StateVar
  - Function emits Event
  - Function has_modifier Modifier
  - Function external_call (low-level / interface calls)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Optional

from ..schema import Edge, ExtractionResult, Hyperedge, Node, make_node_id

# ── Grammar bootstrap ─────────────────────────────────────────────────────────

def _load_parser():
    """Return a tree-sitter Parser for Solidity, or None if unavailable."""
    try:
        from tree_sitter import Language, Parser
        try:
            import tree_sitter_solidity as ts_sol
            lang = Language(ts_sol.language())
        except (ImportError, AttributeError):
            # Fallback: try tree_sitter_languages bundle
            try:
                import tree_sitter_languages
                lang = tree_sitter_languages.get_language("solidity")
            except (ImportError, Exception):
                return None
        parser = Parser(lang)
        return parser
    except Exception as exc:
        print(f"[solidity] tree-sitter unavailable: {exc}", file=sys.stderr)
        return None


_PARSER = None   # lazy-loaded


def _get_parser():
    global _PARSER
    if _PARSER is None:
        _PARSER = _load_parser()
    return _PARSER


# ── Helpers ───────────────────────────────────────────────────────────────────

def _node_text(node, src: bytes) -> str:
    return src[node.start_byte:node.end_byte].decode("utf-8", errors="replace").strip()


def _loc(node) -> dict:
    return {"line": node.start_point[0] + 1, "col": node.start_point[1]}


def _child_by_type(node, *types):
    for child in node.children:
        if child.type in types:
            return child
    return None


def _children_by_type(node, *types):
    return [c for c in node.children if c.type in types]


def _collect_identifiers(node, src: bytes) -> list[str]:
    """Collect all identifier text nodes under a subtree."""
    results = []
    if node.type == "identifier":
        results.append(_node_text(node, src))
    for child in node.children:
        results.extend(_collect_identifiers(child, src))
    return results


# ── Main extractor ────────────────────────────────────────────────────────────

def extract(file_path: str, project_root: Optional[str] = None) -> ExtractionResult:
    """Extract nodes + edges from a Solidity source file."""
    parser = _get_parser()
    result = ExtractionResult()

    if parser is None:
        # Graceful fallback: emit nodes only via regex (no edges)
        return _regex_fallback(file_path)

    src = Path(file_path).read_bytes()
    tree = parser.parse(src)
    rel_path = file_path

    # Track top-level names for same-file call resolution
    module_names: dict[str, str] = {}    # name → node_id
    state_vars: dict[str, str] = {}      # name → node_id
    function_names: dict[str, str] = {}  # name → node_id
    event_names: dict[str, str] = {}
    modifier_names: dict[str, str] = {}

    def _walk_contract(contract_node, contract_id: str, contract_name: str):
        """Walk inside a contract/interface/library and extract members."""
        contract_body = _child_by_type(contract_node, "contract_body") or contract_node
        for child in contract_body.children:
            ctype = child.type

            # ── State variable ──────────────────────────────────────────────
            if ctype == "state_variable_declaration":
                var_name_node = _child_by_type(child, "identifier")
                if not var_name_node:
                    continue
                var_name = _node_text(var_name_node, src)
                var_id = make_node_id(rel_path, f"{contract_name}_{var_name}")
                state_vars[var_name] = var_id
                result.nodes.append(Node(
                    id=var_id,
                    label=f"{contract_name}.{var_name}",
                    node_kind="StateVar",
                    source_file=rel_path,
                    source_location=_loc(child),
                ))
                result.edges.append(Edge(
                    source=contract_id,
                    target=var_id,
                    relation="declares",
                    source_file=rel_path,
                    source_location=_loc(child),
                ))

            # ── Event ───────────────────────────────────────────────────────
            elif ctype == "event_definition":
                ev_name_node = _child_by_type(child, "identifier")
                if not ev_name_node:
                    continue
                ev_name = _node_text(ev_name_node, src)
                ev_id = make_node_id(rel_path, f"{contract_name}_{ev_name}")
                event_names[ev_name] = ev_id
                result.nodes.append(Node(
                    id=ev_id,
                    label=f"{contract_name}.{ev_name}",
                    node_kind="Event",
                    source_file=rel_path,
                    source_location=_loc(child),
                ))
                result.edges.append(Edge(
                    source=contract_id, target=ev_id, relation="declares",
                    source_file=rel_path, source_location=_loc(child),
                ))

            # ── Struct ──────────────────────────────────────────────────────
            elif ctype == "struct_definition":
                st_name_node = _child_by_type(child, "identifier")
                if not st_name_node:
                    continue
                st_name = _node_text(st_name_node, src)
                st_id = make_node_id(rel_path, f"{contract_name}_{st_name}")
                result.nodes.append(Node(
                    id=st_id, label=f"{contract_name}.{st_name}",
                    node_kind="Struct", source_file=rel_path, source_location=_loc(child),
                ))
                result.edges.append(Edge(
                    source=contract_id, target=st_id, relation="declares",
                    source_file=rel_path, source_location=_loc(child),
                ))

            # ── Modifier ────────────────────────────────────────────────────
            elif ctype == "modifier_definition":
                mod_name_node = _child_by_type(child, "identifier")
                if not mod_name_node:
                    continue
                mod_name = _node_text(mod_name_node, src)
                mod_id = make_node_id(rel_path, f"{contract_name}_{mod_name}")
                modifier_names[mod_name] = mod_id
                result.nodes.append(Node(
                    id=mod_id, label=f"{contract_name}.{mod_name}",
                    node_kind="Modifier", source_file=rel_path, source_location=_loc(child),
                ))
                result.edges.append(Edge(
                    source=contract_id, target=mod_id, relation="declares",
                    source_file=rel_path, source_location=_loc(child),
                ))

            # ── Function ────────────────────────────────────────────────────
            elif ctype in ("function_definition", "constructor_definition",
                           "fallback_receive_definition", "receive_definition"):
                _walk_function(child, contract_id, contract_name)

    def _walk_function(fn_node, contract_id: str, contract_name: str):
        """Extract function node + all edges originating from it."""
        fn_name_node = _child_by_type(fn_node, "identifier")
        fn_name = _node_text(fn_name_node, src) if fn_name_node else (
            "constructor" if fn_node.type == "constructor_definition" else
            "fallback" if "fallback" in fn_node.type else "receive"
        )
        fn_id = make_node_id(rel_path, f"{contract_name}_{fn_name}")
        function_names[fn_name] = fn_id

        result.nodes.append(Node(
            id=fn_id,
            label=f"{contract_name}.{fn_name}",
            node_kind="Function",
            source_file=rel_path,
            source_location=_loc(fn_node),
        ))
        result.edges.append(Edge(
            source=contract_id, target=fn_id, relation="declares",
            source_file=rel_path, source_location=_loc(fn_node),
        ))

        # Modifier references on the function signature
        for mod_inv in _iter_nodes_by_type(fn_node, "modifier_invocation"):
            mod_name_node = _child_by_type(mod_inv, "identifier")
            if mod_name_node:
                mod_name = _node_text(mod_name_node, src)
                mod_id = modifier_names.get(mod_name, make_node_id(rel_path, f"{contract_name}_{mod_name}"))
                result.edges.append(Edge(
                    source=fn_id, target=mod_id, relation="has_modifier",
                    source_file=rel_path, source_location=_loc(mod_inv),
                ))

        # Walk function body
        body = _child_by_type(fn_node, "block", "function_body")
        if body:
            _walk_body(body, fn_id, contract_name, rel_path)

    def _walk_body(node, fn_id: str, contract_name: str, rel_path: str):
        """Recursively walk statement nodes extracting calls/reads/writes/emits."""
        for child in node.children:
            ctype = child.type

            # emit Statement
            if ctype == "emit_statement":
                call = _child_by_type(child, "call_expression")
                if call:
                    ev_name = _get_call_name(call, src)
                    if ev_name:
                        ev_id = event_names.get(ev_name, make_node_id(rel_path, f"{contract_name}_{ev_name}"))
                        result.edges.append(Edge(
                            source=fn_id, target=ev_id, relation="emits",
                            source_file=rel_path, source_location=_loc(child),
                        ))

            # assignment (state var write)
            elif ctype == "expression_statement":
                expr = child.children[0] if child.children else None
                if expr and expr.type == "assignment_expression":
                    lhs = expr.children[0] if expr.children else None
                    if lhs:
                        lhs_ids = _collect_identifiers(lhs, src)
                        for name in lhs_ids:
                            if name in state_vars:
                                result.edges.append(Edge(
                                    source=fn_id, target=state_vars[name], relation="writes_var",
                                    source_file=rel_path, source_location=_loc(expr),
                                ))

            # function call
            elif ctype == "call_expression":
                call_name = _get_call_name(child, src)
                if call_name:
                    if call_name in function_names:
                        result.edges.append(Edge(
                            source=fn_id, target=function_names[call_name], relation="calls",
                            source_file=rel_path, source_location=_loc(child),
                        ))
                    elif call_name in {"call", "delegatecall", "staticcall",
                                       "transfer", "send", "safeTransfer",
                                       "safeTransferFrom"}:
                        ext_id = make_node_id(rel_path, f"external_{call_name}")
                        result.edges.append(Edge(
                            source=fn_id, target=ext_id, relation="external_call",
                            unresolved=True, confidence_score=0.8,
                            source_file=rel_path, source_location=_loc(child),
                        ))
                    else:
                        # Cross-contract call (unresolved)
                        ext_id = make_node_id(rel_path, f"external_{call_name}")
                        result.edges.append(Edge(
                            source=fn_id, target=ext_id, relation="calls",
                            unresolved=True, confidence_score=0.8,
                            source_file=rel_path, source_location=_loc(child),
                        ))

            # identifier access — state var read
            elif ctype == "identifier":
                name = _node_text(child, src)
                if name in state_vars and fn_id:
                    result.edges.append(Edge(
                        source=fn_id, target=state_vars[name], relation="reads_var",
                        source_file=rel_path, source_location=_loc(child),
                        confidence_score=0.9,  # identifiers can be params too; slight uncertainty
                    ))

            # recurse
            _walk_body(child, fn_id, contract_name, rel_path)

    # ── Top-level walk ──────────────────────────────────────────────────────

    for top_node in tree.root_node.children:
        ttype = top_node.type

        if ttype in ("contract_declaration", "interface_declaration", "library_declaration"):
            name_node = _child_by_type(top_node, "identifier")
            if not name_node:
                continue
            contract_name = _node_text(name_node, src)
            contract_id = make_node_id(rel_path, contract_name)
            module_names[contract_name] = contract_id

            result.nodes.append(Node(
                id=contract_id,
                label=contract_name,
                node_kind="Module",
                source_file=rel_path,
                source_location=_loc(top_node),
            ))

            # Inheritance edges
            for inh in _iter_nodes_by_type(top_node, "inheritance_specifier"):
                parent_name_node = _child_by_type(inh, "identifier") or inh
                parent_name = _node_text(parent_name_node, src).split("(")[0].strip()
                parent_id = make_node_id(rel_path, parent_name)
                result.edges.append(Edge(
                    source=contract_id, target=parent_id,
                    relation="inherits", unresolved=True, confidence_score=0.9,
                    source_file=rel_path, source_location=_loc(inh),
                ))

            _walk_contract(top_node, contract_id, contract_name)

        elif ttype == "constant_variable_declaration":
            name_node = _child_by_type(top_node, "identifier")
            if name_node:
                const_name = _node_text(name_node, src)
                const_id = make_node_id(rel_path, const_name)
                result.nodes.append(Node(
                    id=const_id, label=const_name, node_kind="Constant",
                    source_file=rel_path, source_location=_loc(top_node),
                ))

    # Add hyperedges for contracts with multiple modifiers (potential access-control cluster)
    _add_modifier_hyperedges(result, rel_path)

    return result


def _iter_nodes_by_type(node, target_type: str):
    """DFS yield all descendant nodes of given type."""
    if node.type == target_type:
        yield node
    for child in node.children:
        yield from _iter_nodes_by_type(child, target_type)


def _get_call_name(call_node, src: bytes) -> Optional[str]:
    """Extract the function name from a call_expression node."""
    # call_expression → function: identifier | member_expression
    first = call_node.children[0] if call_node.children else None
    if not first:
        return None
    if first.type == "identifier":
        return _node_text(first, src)
    if first.type == "member_expression":
        prop = _child_by_type(first, "property_identifier") or _child_by_type(first, "identifier")
        return _node_text(prop, src) if prop else None
    return None


def _add_modifier_hyperedges(result: ExtractionResult, rel_path: str):
    """Create hyperedges grouping functions that share the same modifier (access-control cluster)."""
    modifier_to_fns: dict[str, list[str]] = {}
    for edge in result.edges:
        e = edge if isinstance(edge, Edge) else None
        if e and e.relation == "has_modifier":
            modifier_to_fns.setdefault(e.target, []).append(e.source)

    for mod_id, fn_ids in modifier_to_fns.items():
        if len(fn_ids) >= 3:
            he_id = f"cluster_modifier_{mod_id}"
            result.hyperedges.append(Hyperedge(
                id=he_id,
                label=f"Functions gated by modifier {mod_id}",
                nodes=fn_ids,
                relation="share_access_control",
                confidence="EXTRACTED",
                confidence_score=1.0,
                source_file=rel_path,
            ))


# ── Regex fallback (when tree-sitter unavailable) ─────────────────────────────

def _regex_fallback(file_path: str) -> ExtractionResult:
    """
    Emit coarse nodes via regex when tree-sitter is unavailable.
    Produces INFERRED edges with lower confidence.
    Covers contract names, state vars, functions, modifiers, and events.
    """
    result = ExtractionResult()
    rel_path = file_path
    src = Path(file_path).read_text(errors="ignore")
    contract_names: list[tuple[str, str]] = []

    def line_for(offset: int) -> dict:
        return {"line": src[:offset].count("\n") + 1, "col": 0}

    for m in re.finditer(
        r'\bcontract\s+(\w+)(?:\s+is\s+([^{]+))?\s*\{', src
    ):
        contract_name = m.group(1)
        contract_id = make_node_id(rel_path, contract_name)
        contract_names.append((contract_name, contract_id))
        result.nodes.append(Node(
            id=contract_id, label=contract_name, node_kind="Module",
            source_file=rel_path,
            source_location=line_for(m.start()),
        ))
        if m.group(2):
            for parent in re.split(r',\s*', m.group(2).strip()):
                parent = parent.strip()
                if parent:
                    result.edges.append(Edge(
                        source=contract_id,
                        target=make_node_id(rel_path, parent),
                        relation="inherits",
                        confidence="INFERRED",
                        confidence_score=0.8,
                        unresolved=True,
                        source_file=rel_path,
                    ))

    contract_name, contract_id = contract_names[0] if contract_names else (Path(file_path).stem, "")

    def declare(node: Node) -> None:
        result.nodes.append(node)
        if contract_id:
            result.edges.append(Edge(
                source=contract_id,
                target=node.id,
                relation="declares",
                confidence="INFERRED",
                confidence_score=0.85,
                source_file=rel_path,
                source_location=node.source_location,
            ))

    state_var_pattern = re.compile(
        r'^\s*(?!function\b|event\b|modifier\b|constructor\b|return\b|if\b|for\b|while\b|emit\b|require\b)'
        r'(?:mapping\s*\([^;]+\)|[A-Za-z_]\w*(?:\s*\[[^\]]*\])?)'
        r'(?:\s+(?:public|private|internal|external|constant|immutable|override|virtual))*'
        r'\s+([A-Za-z_]\w*)\s*(?:=|;)',
        re.M,
    )
    for m in state_var_pattern.finditer(src):
        var_name = m.group(1)
        var_id = make_node_id(rel_path, f"{contract_name}_{var_name}")
        declare(Node(
            id=var_id,
            label=f"{contract_name}.{var_name}",
            node_kind="StateVar",
            source_file=rel_path,
            source_location=line_for(m.start()),
        ))

    for m in re.finditer(r'\bmodifier\s+(\w+)\s*(?:\(|\{)', src):
        mod_name = m.group(1)
        mod_id = make_node_id(rel_path, f"{contract_name}_{mod_name}")
        declare(Node(
            id=mod_id,
            label=f"{contract_name}.{mod_name}",
            node_kind="Modifier",
            source_file=rel_path,
            source_location=line_for(m.start()),
        ))

    for m in re.finditer(r'\bfunction\s+(\w+)\s*\(', src):
        fn_name = m.group(1)
        fn_id = make_node_id(rel_path, f"{contract_name}_{fn_name}")
        declare(Node(
            id=fn_id, label=f"{contract_name}.{fn_name}", node_kind="Function",
            source_file=rel_path,
            source_location=line_for(m.start()),
        ))

    for m in re.finditer(r'\bevent\s+(\w+)\s*\(', src):
        ev_name = m.group(1)
        ev_id = make_node_id(rel_path, f"{contract_name}_{ev_name}")
        declare(Node(
            id=ev_id, label=f"{contract_name}.{ev_name}", node_kind="Event",
            source_file=rel_path,
            source_location=line_for(m.start()),
        ))

    return result
