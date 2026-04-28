# Horus Graph Evolution Plan — Build Progress

**Last updated**: 2026-04-28 by Codex
**Plan document**: `docs/HORUS_GRAPH_EVOLUTION_PLAN.md`
**Next agent**: Codex (or Claude continuation)

---

## Status Summary

| Doable | Status | Notes |
|--------|--------|-------|
| D1: graphify DB graph | DONE | `scripts/build_db_graph.py` builds graphify artifacts; graph has 2139 nodes / 11969 edges; invariant-catcher wired |
| D2: horus-graphify-blockchain pkg | DONE (v1) | Installs cleanly; Solidity tree-sitter active; Move/Cairo fall back to regex; tests pass |
| D3: Phase 0 in audit-orchestrator | DONE | Phase 0 section inserted; checklist updated; mkdir updated; phase table updated |
| D4: lessons_db.py | DONE | Full implementation at `scripts/lessons_db.py` |
| D5: db-quality-monitor gap analysis | PARTIAL | Agent mode documented; draft/telemetry dirs created; generator/checker ignore graph/draft artifacts |
| D6: attack-graph-synthesizer agent | DONE | Agent + skill created |
| D7: Progress tracking | IN PROGRESS | This file |

---

## Completed Artifacts

### D3 — audit-orchestrator Phase 0 (DONE)
- File edited: `.claude/agents/audit-orchestrator.md`
- Changes:
  - Inserted `## Phase 0: Graph Foundation` section before `## Phase 1`
  - Added `- [ ] Phase 0:` to workflow checklist
  - Added `| 0 | COMPLETE | ...` row to pipeline-state.md template
  - Added `graph/`, `attack-proofs/`, `plan-execution/` to mkdir

### D4 — lessons_db.py (DONE)
- File: `scripts/lessons_db.py`
- Subcommands: `init`, `ingest`, `query`, `purge`, `stats`
- SQLite FTS5 schema with privacy scrubbing
- Parses `CONFIRMED-REPORT.md` or `10-deep-review.md`
- Lesson categories: `false_negative`, `confirmed_hit`, `multi_step_attack`
- Privacy: opt-in via `--memory` flag (HORUS_MEMORY env var)
- Test it: `python3 scripts/lessons_db.py init && python3 scripts/lessons_db.py stats`

### D6 — attack-graph-synthesizer (DONE)
- Agent: `.claude/agents/attack-graph-synthesizer.md`
- Skill: `.claude/skills/attack-graph-synthesizer/SKILL.md`
- Algorithm: entry-point BFS (depth≤5) + hyperedge expansion + invariant matching + reachability sketches
- Output: `audit-output/attack-candidates.json` + `audit-output/attack-candidates.md` + `audit-output/attack-proofs/*.md`
- Hands off to `protocol-reasoning` for deep validation

### D1 — DB graphify graph (DONE)
- Builder: `scripts/build_db_graph.py`
- Outputs:
  - `DB/graphify-out/graph.json`
  - `DB/graphify-out/GRAPH_REPORT.md`
  - `DB/graphify-out/wiki/index.md`
  - `DB/graphify-out/.graphify_version`
  - `.graphify-version`
- Current graph: 2139 nodes, 11969 edges, 17 communities
- MCP smoke check: `timeout 2 python3 -m graphify.serve DB/graphify-out/graph.json` stays alive until timeout after installing `mcp`
- Query smoke check: `graphify query oracle --graph DB/graphify-out/graph.json --budget 800`
- Added graph-augmented hunting docs in `.claude/resources/db-hunting-workflow.md`

### D2 — horus-graphify-blockchain package (DONE v1)
- Location: `scripts/horus_graphify_blockchain/`
- Structure:
  ```
  scripts/horus_graphify_blockchain/
  ├── pyproject.toml
  ├── GRAMMARS.md              ← grammar sources and verification instructions
  ├── horus_graphify_blockchain/
  │   ├── __init__.py
  │   ├── schema.py            ← Node, Edge, Hyperedge, ExtractionResult, make_node_id
  │   ├── detect.py            ← extension → language detection, iter_blockchain_files
  │   ├── extractor.py         ← extract_file, extract_directory dispatcher
  │   ├── cli.py               ← `horus-graphify-blockchain extract/languages` CLI
  │   └── languages/
  │       ├── __init__.py
  │       ├── solidity.py      ← tree-sitter + regex fallback
  │       ├── move_sui.py      ← tree-sitter + regex fallback + hot-potato detection
  │       └── cairo.py         ← tree-sitter + regex fallback + component hyperedge
  └── tests/
      ├── test_extractor.py    ← pytest suite for all 3 languages
      └── fixtures/
          ├── solidity/ERC20.sol
          ├── move_sui/coin.move
          └── cairo/erc20.cairo
  ```

- Fixed package backend (`setuptools.build_meta`) and added missing `README.md`.
- Strengthened Solidity regex fallback and fixed Solidity tree-sitter traversal through `contract_body` / `function_body`.
- Verified grammar packages:
  - `tree-sitter-solidity==1.2.13` works and is active.
  - `tree-sitter-move==0.0.2` installs but import fails with invalid ELF header; regex fallback active.
  - `tree-sitter-cairo==0.0.2` installs but import fails due missing `typed_parser`; regex fallback active.
- Tests: `/tmp/horus-test-venv/bin/python -m pytest scripts/horus_graphify_blockchain/tests/ -v` → 20 passed.

**Remaining optional D2 work:**
- Phase 2b: add `languages/vyper.py`, `languages/sway.py`, `languages/tact.py`.
- Revisit Move/Cairo when usable grammar packages are available.

---

## Remaining Doables (for Codex)

### D5 — db-quality-monitor gap analysis (PARTIAL)

- Added `--gap-analysis <audit-output-dir>` mode spec to `.claude/agents/db-quality-monitor.md`.
- Created `DB/_drafts/README.md` and `DB/_telemetry/README.md`.
- Added draft/telemetry conventions to `.claude/rules/db-entries.md`.
- Updated `scripts/generate_manifests.py` to ignore `_drafts`, `_telemetry`, `graphify-out`, and generated manifest dirs.
- Updated `scripts/db_quality_check.py` to ignore graph/draft/telemetry artifacts as DB entries.

**Remaining D5 work:**
- Implement or run an actual gap-analysis execution on a known past audit.
- Produce `audit-output/<id>/db-gap-analysis.md` and sample telemetry sidecars.
- Validate a generated draft against `TEMPLATE.md`.

---

## New Rules Files

Created by Claude before Codex resumed:
1. `.claude/rules/graph-artifacts.md`
2. `.claude/rules/lessons-db.md`
3. `.claude/rules/draft-hunt-cards.md`

---

## CLAUDE.md Updates

Done before Codex resumed.

---

## Recall Benchmark (NOT started, needed for validation)

Per plan §15: Build `tests/benchmark/findings.jsonl` from 10 past confirmed audits.
Schema per finding:
```json
{
  "audit_id": "...",
  "finding_id": "F-001",
  "title": "...",
  "severity": "HIGH",
  "category": "oracle",
  "multi_step": false,
  "would_grep_find_it": true,
  "ecosystem": "evm",
  "protocol_type": "lending_protocol"
}
```

---

## Quick Validation Commands (run these to verify what's working)

```bash
# Verify D4 (lessons_db.py)
python3 /home/calc1f4r/Horus/scripts/lessons_db.py init
python3 /home/calc1f4r/Horus/scripts/lessons_db.py stats

# Verify D2 (blockchain extractor — regex fallback, no tree-sitter needed)
cd /home/calc1f4r/Horus
pip install -e scripts/horus_graphify_blockchain/
horus-graphify-blockchain languages
horus-graphify-blockchain extract scripts/horus_graphify_blockchain/tests/fixtures/solidity/ERC20.sol

# Run D2 tests
pytest scripts/horus_graphify_blockchain/tests/ -v

# Verify D3 (orchestrator has Phase 0)
grep -n "Phase 0" .claude/agents/audit-orchestrator.md | head -5

# Verify D6 (attack-graph-synthesizer exists)
ls .claude/agents/attack-graph-synthesizer.md .claude/skills/attack-graph-synthesizer/SKILL.md
```

---

## Open Questions Still Pending User Answer

See `docs/HORUS_GRAPH_EVOLUTION_PLAN.md §4` for full list.
Key ones:
- Q1: Where does horus-graphify-blockchain live long-term? (current: scripts/ directory)
- Q4: Does a recall benchmark exist?
- Q5: Are optional deepeners (Slither) fully banned or opt-in allowed?

---

## Context for the Next Agent (Codex)

**You are continuing implementation of the Horus Graph Evolution Plan.**

Read these files first, in order:
1. `/home/calc1f4r/Horus/docs/HORUS_GRAPH_EVOLUTION_PLAN.md` — full plan with all specs
2. This file (`audit-output/plan-execution/PROGRESS.md`) — what's done
3. `/home/calc1f4r/Horus/CLAUDE.md` — project conventions

Start with the highest-value remaining tasks:
1. **D5 execution validation** — run gap analysis on a known confirmed audit and inspect draft quality.
2. **Recall benchmark** — build `tests/benchmark/findings.jsonl`.
3. **D2 Phase 2b** — Vyper/Sway/Tact extraction modules if needed.
4. **D3 follow-through** — update diagrams/resources if strict plan completeness is required.

Do NOT rebuild anything already listed as DONE above — check this file first.
