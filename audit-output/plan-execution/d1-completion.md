# D1 Completion — Graphify the Vulnerability DB

Status: complete for v1 deterministic DB graph.

## Outputs

- `DB/graphify-out/graph.json`
- `DB/graphify-out/GRAPH_REPORT.md`
- `DB/graphify-out/wiki/index.md`
- `DB/graphify-out/.graphify_version`
- `.graphify-version`
- `scripts/build_db_graph.py`

## Validation

- Graph nodes: 2139
- Graph edges: 11969
- Wiki markdown files: 51
- God nodes include vulnerability concepts: `cosmos`, `ibc`, `appchain`, `defi`, `calculation`, `vault`, `flash-loan`, `amm`, `reentrancy`
- Query smoke test:
  - `graphify query oracle --graph DB/graphify-out/graph.json --budget 800`
- MCP smoke test:
  - `timeout 2 python3 -m graphify.serve DB/graphify-out/graph.json`
  - Result: server stayed alive until timeout after installing `mcp`, with no startup traceback.

## Notes

The graph is built deterministically from canonical hunt-card and manifest data
using graphify's build, cluster, report, wiki, and JSON export modules. This is
the practical v1 path for Codex because the `/graphify` slash-command semantic
sub-agent flow is not directly callable from this environment.

