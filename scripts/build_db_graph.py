#!/usr/bin/env python3
"""
Build a graphify knowledge graph for the Horus vulnerability DB.

This is a deterministic fallback for environments where the `/graphify` agent
skill cannot run its semantic sub-agent extraction. It still uses graphify's
graph substrate for build, clustering, reporting, wiki, and JSON export.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from graphify import analyze, build, cluster, export, report, wiki

from horus_retrieval.protocol_context import PROTOCOL_CONTEXTS


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "DB"
OUT = DB / "graphify-out"
MAX_WIKI_COMMUNITIES = 80
BROAD_SEMANTIC_LABELS = {
    "critical",
    "high",
    "medium",
    "low",
    "logical_error",
    "logical error",
    "logic_error",
    "logic error",
    "economic_exploit",
    "economic exploit",
    "dos",
    "denial_of_service",
    "denial of service",
    "missing_validation",
    "missing validation",
    "fund_loss",
    "fund loss",
    "root",
}
BROAD_NODE_KINDS = {"Category", "Manifest", "ProtocolContext", "Severity"}


def _slug(value: str, *, prefix: str = "") -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return f"{prefix}{slug}" if prefix else slug


def _is_broad_semantic(label: str, kind: str) -> bool:
    cleaned = label.strip().lower()
    if kind == "GraphHint" and len(re.findall(r"[a-z0-9]+", cleaned)) < 3:
        return True
    return kind in BROAD_NODE_KINDS or cleaned in BROAD_SEMANTIC_LABELS


def _edge(source: str, target: str, relation: str, source_file: str, confidence: str = "EXTRACTED") -> dict:
    return {
        "source": source,
        "target": target,
        "relation": relation,
        "confidence": confidence,
        "confidence_score": 1.0 if confidence == "EXTRACTED" else 0.85,
        "source_file": source_file,
    }


def _node(node_id: str, label: str, kind: str, source_file: str) -> dict:
    return {
        "id": node_id,
        "label": label,
        "node_kind": kind,
        "file_type": "document",
        "source_file": source_file,
    }


def _grep_terms(card: dict) -> list[str]:
    terms: list[str] = []
    for raw in str(card.get("grep", "")).split("|"):
        raw = raw.strip()
        if not raw or len(raw) < 3:
            continue
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{2,}", raw):
            terms.append(raw)
    return terms[:12]


def _iter_text(value) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        result: list[str] = []
        for nested in value.values():
            result.extend(_iter_text(nested))
        return result
    if isinstance(value, list):
        result: list[str] = []
        for nested in value:
            result.extend(_iter_text(nested))
        return result
    return []


def _split_semantic_field(value) -> list[str]:
    terms: list[str] = []
    for raw in _iter_text(value):
        for part in re.split(r"[|,]", raw):
            cleaned = part.strip().strip("{}[]()")
            if cleaned and cleaned.lower() not in {"unknown", "n/a", "none"}:
                terms.append(cleaned)
    return list(dict.fromkeys(terms))


def _load_cards(db: Path = DB) -> list[dict]:
    path = db / "manifests" / "huntcards" / "all-huntcards.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("cards", [])


def _load_manifest_context(db: Path = DB) -> dict[str, dict]:
    contexts: dict[str, dict] = {}
    manifests_dir = db / "manifests"
    for manifest_path in sorted(manifests_dir.glob("*.json")):
        if manifest_path.name == "keywords.json":
            continue
        manifest_name = manifest_path.stem
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        for file_entry in data.get("files", []):
            frontmatter = file_entry.get("frontmatter", {}) or {}
            for pattern in file_entry.get("patterns", []):
                contexts[pattern.get("id", "")] = {
                    "manifest": manifest_name,
                    "file": file_entry.get("file", ""),
                    "frontmatter": frontmatter,
                    "pattern": pattern,
                }
    return contexts


def _community_labels(cards: list[dict]) -> dict[str, str]:
    labels: dict[str, str] = {}
    by_ref: dict[str, Counter] = defaultdict(Counter)
    for card in cards:
        ref = str(card.get("ref", ""))
        for cat in card.get("cat", [])[:4]:
            by_ref[ref][str(cat)] += 1
    for ref, counts in by_ref.items():
        if counts:
            labels[ref] = counts.most_common(1)[0][0]
    return labels


def _add_semantic_node(
    nodes: dict[str, dict],
    edges: list[dict],
    card_id: str,
    label: str,
    kind: str,
    relation: str,
    source_file: str,
    buckets: dict[str, set[str]],
    *,
    confidence: str = "EXTRACTED",
) -> None:
    if not label:
        return
    node_id = _slug(label, prefix=f"{kind.lower()}_")
    nodes.setdefault(node_id, _node(node_id, label, kind, source_file))
    if _is_broad_semantic(label, kind):
        return
    edges.append(_edge(card_id, node_id, relation, source_file, confidence=confidence))
    edges.append(_edge(node_id, card_id, f"expands_to_{relation}", source_file, confidence=confidence))
    if kind != "Manifest":
        buckets[f"{kind}:{node_id}"].add(card_id)


def _add_related_variant_edges(edges: list[dict], buckets: dict[str, set[str]], source_file: str) -> None:
    seen: set[tuple[str, str]] = set()
    for _bucket, card_ids in sorted(buckets.items()):
        ordered = sorted(card_ids)
        if len(ordered) < 2:
            continue

        # Keep dense similarity local for small buckets, and bounded for broad
        # concepts like "flash loan" so graph expansion improves without turning
        # every common term into a full clique.
        pairs: list[tuple[str, str]] = []
        if len(ordered) <= 20:
            for i, source in enumerate(ordered):
                for target in ordered[i + 1:]:
                    pairs.append((source, target))
        else:
            for i, source in enumerate(ordered):
                for target in ordered[i + 1:i + 4]:
                    pairs.append((source, target))

        for source, target in pairs[:150]:
            for edge_source, edge_target in ((source, target), (target, source)):
                key = (edge_source, edge_target)
                if key in seen:
                    continue
                seen.add(key)
                edges.append(_edge(edge_source, edge_target, "related_variant", source_file, confidence="INFERRED"))


def _wiki_priority(
    cid: int,
    node_ids: list[str],
    cohesion: dict[int, float],
    community_labels: dict[int, str],
) -> tuple[int, float, int, str]:
    """Rank communities for the checked-in agent wiki.

    The full graph still exports every community in graph.json and GRAPH_REPORT.md.
    The wiki is a browsing surface, so singleton/tiny semantic communities are
    lower value than larger communities with named vulnerability topics.
    """
    label = community_labels.get(cid, "")
    generic = 1 if label.startswith("DB Community ") else 0
    return (len(node_ids), cohesion.get(cid, 0.0), -generic, label)


def _curate_wiki_communities(
    communities: dict[int, list[str]],
    community_labels: dict[int, str],
    cohesion: dict[int, float],
    limit: int = MAX_WIKI_COMMUNITIES,
) -> dict[int, list[str]]:
    eligible = {
        cid: node_ids
        for cid, node_ids in communities.items()
        if len(node_ids) > 1
    }
    if not eligible:
        eligible = dict(communities)

    if len(eligible) <= limit:
        return dict(sorted(eligible.items()))

    ranked = sorted(
        eligible.items(),
        key=lambda item: _wiki_priority(item[0], item[1], cohesion, community_labels),
        reverse=True,
    )
    selected = dict(ranked[:limit])
    return dict(sorted(selected.items()))


def _reset_wiki_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for wiki_file in path.glob("*.md"):
        wiki_file.unlink()


def build_extraction(cards: list[dict], *, db: Path = DB) -> dict:
    manifest_context = _load_manifest_context(db)
    nodes: dict[str, dict] = {}
    edges: list[dict] = []
    semantic_buckets: dict[str, set[str]] = defaultdict(set)

    nodes["horus_db"] = _node("horus_db", "Horus Vulnerability DB", "Corpus", "DB")

    category_counts: Counter[str] = Counter()
    term_counts: Counter[str] = Counter()
    for card in cards:
        category_counts.update(str(c) for c in card.get("cat", []))
        term_counts.update(_grep_terms(card))

    common_terms = {term for term, _ in term_counts.most_common(350)}

    for category in category_counts:
        cid = _slug(category, prefix="cat_")
        nodes[cid] = _node(cid, category, "Category", "DB/index.json")
        edges.append(_edge("horus_db", cid, "contains_category", "DB/index.json"))

    protocol_manifest_map: dict[str, set[str]] = {
        name: set(context.manifests)
        for name, context in PROTOCOL_CONTEXTS.items()
    }
    for protocol_name, manifests in protocol_manifest_map.items():
        pid = _slug(protocol_name, prefix="protocol_")
        nodes[pid] = _node(pid, protocol_name, "ProtocolContext", "DB/index.json")
        edges.append(_edge("horus_db", pid, "contains_protocol_context", "DB/index.json"))
        for manifest_name in sorted(manifests):
            mid = _slug(manifest_name, prefix="manifest_")
            nodes.setdefault(mid, _node(mid, manifest_name, "Manifest", f"DB/manifests/{manifest_name}.json"))
            edges.append(_edge(pid, mid, "routes_to_manifest", "DB/index.json"))

    for card in cards:
        card_id = card["id"]
        ref = str(card.get("ref", ""))
        source_file = ref or "DB/manifests/huntcards/all-huntcards.json"
        context = manifest_context.get(card_id, {})
        manifest_name = context.get("manifest", "")
        frontmatter = context.get("frontmatter", {}) or {}
        pattern = context.get("pattern", {}) or {}
        nodes[card_id] = _node(card_id, card.get("title", card_id), "HuntCard", source_file)

        if ref:
            ref_id = _slug(ref, prefix="entry_")
            nodes.setdefault(ref_id, _node(ref_id, ref, "DBEntry", ref))
            edges.append(_edge(ref_id, card_id, "defines_hunt_card", source_file))

        for category in card.get("cat", []):
            cid = _slug(str(category), prefix="cat_")
            nodes.setdefault(cid, _node(cid, str(category), "Category", "DB/index.json"))

        for term in _grep_terms(card):
            if term not in common_terms:
                continue
            tid = _slug(term, prefix="kw_")
            nodes.setdefault(tid, _node(tid, term, "Keyword", source_file))
            edges.append(_edge(card_id, tid, "mentions_keyword", source_file, confidence="INFERRED"))
            edges.append(_edge(tid, card_id, "keyword_expands_to_card", source_file, confidence="INFERRED"))

        if manifest_name:
            _add_semantic_node(
                nodes,
                edges,
                card_id,
                manifest_name,
                "Manifest",
                "belongs_to_manifest",
                f"DB/manifests/{manifest_name}.json",
                semantic_buckets,
            )

            for protocol_name, manifests in protocol_manifest_map.items():
                if manifest_name in manifests:
                    _add_semantic_node(
                        nodes,
                        edges,
                        card_id,
                        protocol_name,
                        "ProtocolContext",
                        "relevant_to_protocol",
                        "DB/index.json",
                        semantic_buckets,
                    )

        _add_semantic_node(
            nodes,
            edges,
            card_id,
            str(card.get("severity", "")),
            "Severity",
            "has_severity",
            source_file,
            semantic_buckets,
        )

        for root_cause in _split_semantic_field(frontmatter.get("root_cause_family")):
            _add_semantic_node(
                nodes,
                edges,
                card_id,
                root_cause,
                "RootCauseFamily",
                "has_root_cause_family",
                source_file,
                semantic_buckets,
            )

        for attack_type in _split_semantic_field(frontmatter.get("attack_type")):
            _add_semantic_node(
                nodes,
                edges,
                card_id,
                attack_type,
                "AttackType",
                "has_attack_type",
                source_file,
                semantic_buckets,
            )

        for component in _split_semantic_field(frontmatter.get("affected_component")):
            _add_semantic_node(
                nodes,
                edges,
                card_id,
                component,
                "AffectedComponent",
                "affects_component",
                source_file,
                semantic_buckets,
            )

        graph_hints = card.get("graphHints") or pattern.get("graphHints") or {}
        for hint in _iter_text(graph_hints):
            _add_semantic_node(
                nodes,
                edges,
                card_id,
                hint,
                "GraphHint",
                "has_graph_hint",
                source_file,
                semantic_buckets,
                confidence="INFERRED",
            )

        evidence = card.get("reportEvidence") or pattern.get("reportEvidence") or {}
        if isinstance(evidence, dict):
            consensus = evidence.get("severityConsensus")
            if consensus:
                _add_semantic_node(
                    nodes,
                    edges,
                    card_id,
                    str(consensus),
                    "ReportEvidence",
                    "has_report_severity_consensus",
                    source_file,
                    semantic_buckets,
                    confidence="INFERRED",
                )
            for report_path in evidence.get("sampleReports", [])[:5]:
                _add_semantic_node(
                    nodes,
                    edges,
                    card_id,
                    str(report_path),
                    "ReportEvidence",
                    "supported_by_report",
                    source_file,
                    semantic_buckets,
                    confidence="INFERRED",
                )

    _add_related_variant_edges(edges, semantic_buckets, "DB/manifests/huntcards/all-huntcards.json")

    return {
        "nodes": list(nodes.values()),
        "edges": edges,
        "hyperedges": [],
        "input_tokens": 0,
        "output_tokens": 0,
    }


def build_db_graph(
    *,
    db: Path = DB,
    out: Path = OUT,
    root: Path = ROOT,
    emit=print,
) -> dict[str, int | str]:
    """Build DB graph artifacts into `out` and return summary counts."""
    out.mkdir(parents=True, exist_ok=True)
    cards = _load_cards(db)
    extraction = build_extraction(cards, db=db)
    (out / ".graphify_extract.json").write_text(json.dumps(extraction, indent=2), encoding="utf-8")

    graph = build.build([extraction], directed=True)
    communities = cluster.cluster(graph)
    cohesion = cluster.score_all(graph, communities)
    gods = analyze.god_nodes(graph, top_n=15)
    surprises = analyze.surprising_connections(graph, communities, top_n=10)

    labels_by_ref = _community_labels(cards)
    community_labels: dict[int, str] = {}
    for cid, node_ids in communities.items():
        cat_counts: Counter[str] = Counter()
        for node_id in node_ids:
            label = graph.nodes[node_id].get("label", "")
            if label in labels_by_ref:
                cat_counts[labels_by_ref[label]] += 1
            if graph.nodes[node_id].get("node_kind") == "Category":
                cat_counts[label] += 3
        community_labels[cid] = cat_counts.most_common(1)[0][0] if cat_counts else f"DB Community {cid}"

    questions = analyze.suggest_questions(graph, communities, community_labels)
    detection = {
        "total_files": len({c.get("ref") for c in cards if c.get("ref")}),
        "total_words": sum(len(str(c).split()) for c in cards),
    }
    token_cost = {"input": 0, "output": 0}

    export.to_json(graph, communities, str(out / "graph.json"), force=True)
    graph_data = json.loads((out / "graph.json").read_text(encoding="utf-8"))
    graph_data["edges"] = graph_data.get("links", [])
    (out / "graph.json").write_text(json.dumps(graph_data, indent=2), encoding="utf-8")

    graph_report = report.generate(
        graph,
        communities,
        cohesion,
        community_labels,
        gods,
        surprises,
        detection,
        token_cost,
        str(db),
        suggested_questions=questions,
    )
    (out / "GRAPH_REPORT.md").write_text(graph_report, encoding="utf-8")
    wiki_dir = out / "wiki"
    _reset_wiki_dir(wiki_dir)
    wiki_communities = _curate_wiki_communities(communities, community_labels, cohesion)
    wiki_labels = {cid: community_labels[cid] for cid in wiki_communities}
    wiki_cohesion = {cid: cohesion[cid] for cid in wiki_communities if cid in cohesion}
    wiki_count = wiki.to_wiki(graph, wiki_communities, wiki_dir, wiki_labels, wiki_cohesion, gods)

    try:
        graphify_version = version("graphifyy")
    except PackageNotFoundError:
        graphify_version = "unknown"
    (out / ".graphify_version").write_text(graphify_version, encoding="utf-8")
    root.mkdir(parents=True, exist_ok=True)
    (root / ".graphify-version").write_text(graphify_version, encoding="utf-8")

    emit(f"DB graph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    emit(f"Communities: {len(communities)}")
    emit(f"Wiki articles: {wiki_count} ({len(wiki_communities)} curated communities)")
    emit(f"Graphify version: {graphify_version}")
    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "communities": len(communities),
        "wiki_articles": wiki_count,
        "curated_communities": len(wiki_communities),
        "graphify_version": graphify_version,
    }


def main() -> int:
    build_db_graph()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
