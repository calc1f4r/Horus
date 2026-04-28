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


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "DB"
OUT = DB / "graphify-out"


def _slug(value: str, *, prefix: str = "") -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return f"{prefix}{slug}" if prefix else slug


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


def _load_cards() -> list[dict]:
    path = DB / "manifests" / "huntcards" / "all-huntcards.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("cards", [])


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


def build_extraction(cards: list[dict]) -> dict:
    nodes: dict[str, dict] = {}
    edges: list[dict] = []

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

    for card in cards:
        card_id = card["id"]
        ref = str(card.get("ref", ""))
        source_file = ref or "DB/manifests/huntcards/all-huntcards.json"
        nodes[card_id] = _node(card_id, card.get("title", card_id), "HuntCard", source_file)

        if ref:
            ref_id = _slug(ref, prefix="entry_")
            nodes.setdefault(ref_id, _node(ref_id, ref, "DBEntry", ref))
            edges.append(_edge(ref_id, card_id, "defines_hunt_card", source_file))

        for category in card.get("cat", []):
            cid = _slug(str(category), prefix="cat_")
            nodes.setdefault(cid, _node(cid, str(category), "Category", "DB/index.json"))
            edges.append(_edge(card_id, cid, "belongs_to", source_file))

        for term in _grep_terms(card):
            if term not in common_terms:
                continue
            tid = _slug(term, prefix="kw_")
            nodes.setdefault(tid, _node(tid, term, "Keyword", source_file))
            edges.append(_edge(card_id, tid, "mentions_keyword", source_file, confidence="INFERRED"))

    return {
        "nodes": list(nodes.values()),
        "edges": edges,
        "hyperedges": [],
        "input_tokens": 0,
        "output_tokens": 0,
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    cards = _load_cards()
    extraction = build_extraction(cards)
    (OUT / ".graphify_extract.json").write_text(json.dumps(extraction, indent=2), encoding="utf-8")

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

    export.to_json(graph, communities, str(OUT / "graph.json"), force=True)
    graph_data = json.loads((OUT / "graph.json").read_text(encoding="utf-8"))
    graph_data["edges"] = graph_data.get("links", [])
    (OUT / "graph.json").write_text(json.dumps(graph_data, indent=2), encoding="utf-8")

    graph_report = report.generate(
        graph,
        communities,
        cohesion,
        community_labels,
        gods,
        surprises,
        detection,
        token_cost,
        str(DB),
        suggested_questions=questions,
    )
    (OUT / "GRAPH_REPORT.md").write_text(graph_report, encoding="utf-8")
    wiki.to_wiki(graph, communities, OUT / "wiki", community_labels, cohesion, gods)

    try:
        graphify_version = version("graphifyy")
    except PackageNotFoundError:
        graphify_version = "unknown"
    (OUT / ".graphify_version").write_text(graphify_version, encoding="utf-8")
    (ROOT / ".graphify-version").write_text(graphify_version, encoding="utf-8")

    print(f"DB graph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    print(f"Communities: {len(communities)}")
    print(f"Graphify version: {graphify_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
