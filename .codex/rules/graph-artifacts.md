---
description: Conventions for audit-output/graph/ artifacts produced by Phase 0 and attack-graph-synthesizer
globs: ["audit-output/graph/**", "audit-output/attack-candidates*", "audit-output/attack-proofs/**"]
---

# Graph Artifacts Conventions

## Directory Layout

```
audit-output/graph/
├── graph.json          ← merged codebase knowledge graph (graphify format)
├── mcp.pid             ← PID of running MCP server (absent if server not started)
├── coverage.jsonl      ← append-only node coverage log
└── blockchain-ast.json ← raw output from horus-graphify-blockchain (pre-merge)
```

## graph.json Schema

Produced by graphify and/or `graphify merge-graphs`. Must conform to:
- `nodes`: list of `{id, label, node_kind, ...metadata}`
- `edges`: list of `{source, target, relation, confidence, confidence_score}`
- `hyperedges`: list of `{id, label, nodes, relation}`

Node ID convention: `{filename_stem}_{entity_name}` — lowercase, `[a-z0-9_]` only. No chunk suffixes.

## coverage.jsonl Format

One JSON object per line:
```json
{"agent": "<agent-name>", "node_id": "<id>", "phase": "<phase-tag>", "ts": "<iso8601>"}
```

Valid phase tags: `0-foundation`, `4-protocol-reasoning`, `4-ags` (attack-graph-synthesizer), `4-invariant-catcher`.

**Append only** — never delete or overwrite entries. The log is used for blind-spot analysis.

## MCP Server

Started by Phase 0. PID written to `graph/mcp.pid`. Agents check if server is alive before querying:
```bash
MCP_PID=$(cat audit-output/graph/mcp.pid 2>/dev/null)
[[ -n "$MCP_PID" ]] && kill -0 "$MCP_PID" 2>/dev/null && echo "MCP running"
```

Exposes: `query_graph`, `get_node`, `get_neighbors`, `get_community`, `god_nodes`, `graph_stats`, `shortest_path`.

## attack-candidates.json Schema

Written by attack-graph-synthesizer. Consumed by protocol-reasoning.
- Top-level: `generated_at`, `ecosystem`, `protocol_type`, `graph_source`, `candidates`, `filtered_count`, `total_paths_explored`
- Per candidate: `id` (atk-NNN), `path`, `path_source` (bfs|hyperedge), `hypothesized_violation`, `invariant_severity`, `preconditions`, `severity_estimate`, `requires_compromised_role`, `attacker_capable`, `proof_path`, `validator`

## attack-proofs/ Format

One file per candidate: `audit-output/attack-proofs/atk-NNN.md`.
Required sections: `## Path`, `## Hypothesized invariant violation`, `## Required attacker capabilities`, `## Transaction sequence (conceptual)`, `## Confidence`, `## Validator`.

## Soft-Gate Rule

If `audit-output/graph/graph.json` does not exist, agents that depend on it (attack-graph-synthesizer, invariant-catcher Step 0) log a warning and skip graph features — they do NOT abort. The audit proceeds without graph enrichment.
