# Orchestration Pipeline

> **Purpose**: Master reference for the graph-aware 11-phase configurable audit pipeline with Phase 0 graph foundation, iterative parallel discovery, optional PoC/FV execution, and a judging self-loop (pre-judge → polish → deep-review). Defines phase transitions, data handoffs, sub-agent contracts, error handling, and context budgets.
> **Consumer**: `audit-orchestrator` agent.

---

## Configuration Options

| Option | Values | Default | Effect |
|--------|--------|---------|--------|
| `--static-only` | flag | OFF | Skip Phases 6 (PoC) and 7 (FV) |
| `--judge=X` | sherlock, cantina, code4rena | all 3 | Use single judge in self-loop |
| `--discovery-rounds=N` | 1-5 | 2 | Number of iterative discovery rounds |

---

## Pipeline Overview

```
User Input: @audit-orchestrator <path> [hint] [--static-only] [--judge=X] [--discovery-rounds=N]
    │
    ▼
═══════════════════════════════════════════════════════
 GRAPH + SEQUENTIAL FOUNDATION (Phase 0, then Phases 1-3)
═══════════════════════════════════════════════════════
    │
┌─────────────────────────────────────┐
│ Phase 0: GRAPH FOUNDATION           │  Self (soft gate)
│ graphify codebase, blockchain AST,  │  Output: graph/graph.json,
│ MCP server, coverage, memory recall │          graph/coverage.jsonl
└──────────────┬──────────────────────┘
               │ graphAvailable, mcpEndpoint, memoryRecall
               ▼
┌─────────────────────────────────────┐
│ Phase 1: RECONNAISSANCE             │  Self (no sub-agent)
│ Protocol detection, scope, manifests│  Output: 00-scope.md, pipeline-state.md
└──────────────┬──────────────────────┘
               │ protocolTypes, manifestList, filesInScope, config
               ▼
┌─────────────────────────────────────┐
│ Phase 2: CONTEXT BUILDING           │  Sub-agent: audit-context-building
│ Line-by-line codebase analysis      │  Output: 01-context.md + context/*.md
└──────────────┬──────────────────────┘
               │ architecture, functions, invariantCandidates
               ▼
┌─────────────────────────────────────┐
│ Phase 3: INVARIANT EXTRACTION +     │  Sub-agents: invariant-writer (sequential)
│ REVIEW (sequential pair)            │  then invariant-reviewer
│                                     │  Output: 02-invariants-reviewed.md
└──────────────┬──────────────────────┘
               │ reviewedInvariantSpecs (INV-*)
               ▼
═══════════════════════════════════════════════════════
 ITERATIVE PARALLEL DISCOVERY (Phase 4 — N rounds)
 Streams write → orchestrator merges → streams re-read
═══════════════════════════════════════════════════════
               │
    ┌──── ROUND 1 (independent) ─────┐
    │          │          │           │
    ▼          ▼          ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ 4A: DB │ │ 4B:    │ │ 4C:    │ │ 4D:    │
│ Hunt + │ │Reason  │ │Persona │ │Valid.  │
│ Graph  │ │        │ │        │ │        │
└───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘
    │          │          │           │
    └──────────┴────┬─────┴───────────┘
                    ▼
              ┌────────┐
              │ 4E:    │
              │Attack  │
              │Graph   │
              └───┬────┘
               │ Round 1 findings
               ▼
    orchestrator → discovery-state-round-1.md
               │
    ┌──── ROUND 2+ (cross-pollination) ─┐
    │  All streams read shared state     │
    │  Cross-check, gap-fill, go deeper  │
    └──────────┬─────────────────────────┘
               │ ... repeat for N rounds ...
               ▼
═══════════════════════════════════════════════════════
 TRIAGE (Phase 5)
═══════════════════════════════════════════════════════
               │
┌─────────────────────────────────────┐
│ Phase 5: MERGE & TRIAGE            │  Self
│ Cross-source correlation, dedup,    │  Output: 05-findings-triaged.md
│ falsification, severity             │
└──────────────┬──────────────────────┘
               │ triagedFindings (F-NNN) with stable IDs
               ▼
═══════════════════════════════════════════════════════
 OPTIONAL DYNAMIC TESTING (Phases 6-7)
 [SKIPPED if --static-only]
═══════════════════════════════════════════════════════
               │
┌─────────────────────────────────────┐
│ Phase 6: PoC GENERATION & EXECUTION│  Sub-agent: poc-writing × N
│ [CONDITIONAL — skip if static-only] │  + Self (execution)
│                                     │  Output: pocs/ + 06-poc-results.md
└──────────────┬──────────────────────┘
               │
┌─────────────────────────────────────┐
│ Phase 7: FV GENERATION & EXECUTION │  Sub-agents: medusa, certora, halmos
│ [CONDITIONAL — skip if static-only] │  + Self (execution)
│                                     │  Output: fuzzing/ + certora/ + halmos/
│                                     │         + 07-fv-results.md
└──────────────┬──────────────────────┘
               │
═══════════════════════════════════════════════════════
 JUDGING SELF-LOOP (Phases 8-10)
 Judge → Polish → Deep Review (same judges review twice)
═══════════════════════════════════════════════════════
               │
┌─────────────────────────────────────┐
│ Phase 8: PRE-JUDGING                │  Judge(s) per --judge flag
│ Validity screen on raw findings     │  Output: 08-pre-judge-results.md
└──────────────┬──────────────────────┘
               │ only VALID findings proceed
               ▼
┌─────────────────────────────────────┐
│ Phase 9: ISSUE POLISHING            │  Sub-agent: issue-writer × N
│ Submission-ready write-ups          │  Output: issues/ + 09-polished-findings.md
│ (valid findings ONLY)               │
└──────────────┬──────────────────────┘
               │ polished issues
               ▼
┌─────────────────────────────────────┐
│ Phase 10: DEEP REVIEW               │  Same judge(s) as Phase 8
│ Line-by-line verification           │  Output: 10-deep-review.md
│ of polished issues                  │
└──────────────┬──────────────────────┘
               │ CONFIRMED findings only
               ▼
═══════════════════════════════════════════════════════
 REPORT (Phase 11)
═══════════════════════════════════════════════════════
               │
┌─────────────────────────────────────┐
│ Phase 11: REPORT ASSEMBLY           │  Self
│ Final report with judge verdicts,   │  Output: CONFIRMED-REPORT.md
│ execution evidence (if available),  │
│ cross-pollination record            │
└─────────────────────────────────────┘
```

---

## Common Pipeline Bus

All agents communicate through the **pipeline bus** — a shared file system under `audit-output/`. The orchestrator maintains `pipeline-state.md` which tracks every artifact's production status, consumption, and verification.

### Pipeline Bus Rules

1. **Every agent reads FROM and writes TO `audit-output/`** — no side channels
2. **Phase N+1 may only start after Phase N outputs are verified** (phase gates)
3. **Parallel phases write to SEPARATE files** — orchestrator merges
4. **`pipeline-state.md` is the canonical record** — update after every phase
5. **Every finding gets a unique stable ID at birth** that persists through all phases
6. **`memory-state.md` is the cross-cutting knowledge bus** — every agent reads before starting and writes a memory entry after completing (see [memory-state.md](memory-state.md)). The orchestrator consolidates memory between phases.

### Data Contract: What Each Phase Produces and Consumes

| Phase | Produces | Consumes |
|-------|----------|----------|
| 0 | `graph/graph.json`, `graph/mcp.pid`, `graph/mcp.endpoint`, `graph/coverage.jsonl`, optional `memory-recall.md` | Codebase path, graphify, optional `horus-graphify-blockchain`, optional `~/.horus/lessons.db` |
| 1 | `00-scope.md`, `pipeline-state.md`, `memory-state.md` (init) | Codebase path, DB/index.json |
| 2 | `01-context.md`, `context/*.md` | `00-scope.md`, `memory-state.md` |
| 3 | `02-invariants-reviewed.md` | `01-context.md`, DB manifests, `memory-state.md` |
| 4 (per round) | `*-RN.md` outputs per stream, `attack-candidates.*`, `discovery-state-round-N.md` | Hunt cards, `DB/graphify-out/graph.json`, `graph/graph.json`, invariants, context, previous round state, `memory-state.md` |
| 5 | `05-findings-triaged.md` | All Phase 4 outputs from all rounds, `memory-state.md` |
| 6 [CONDITIONAL] | `pocs/F-NNN-poc.*`, `06-poc-results.md` | `05-findings-triaged.md`, codebase, `memory-state.md` |
| 7 [CONDITIONAL] | `fuzzing/`, `certora/`, `halmos/`, `07-fv-results.md` | `02-invariants-reviewed.md`, codebase, `memory-state.md` |
| 8 | `08-pre-judge-results.md` | `05-findings-triaged.md`, execution evidence (if available), `memory-state.md` |
| 9 | `issues/F-NNN-issue.md`, `09-polished-findings.md` | `08-pre-judge-results.md`, triaged findings, execution evidence, `memory-state.md` |
| 10 | `10-deep-review.md` | `09-polished-findings.md`, `issues/F-NNN-issue.md`, `memory-state.md` |
| 11 | `CONFIRMED-REPORT.md` | ALL outputs |

---

## Phase Details

### Phase 0: Graph Foundation

| Attribute | Value |
|-----------|-------|
| **Agent** | Self (orchestrator) |
| **Input** | Codebase path + optional memory flag |
| **Output** | `audit-output/graph/graph.json`, `mcp.pid`, `mcp.endpoint`, `coverage.jsonl`, optional `memory-recall.md` |
| **Sub-agents** | None |
| **Estimated context** | Small; graph construction is file/tool driven |

**Steps**:
1. Create `audit-output/graph/`.
2. Run graphify on the target codebase.
3. If `horus-graphify-blockchain` is installed and blockchain DSL files exist, emit `blockchain-ast.json`.
4. Finalize graphify output and optional blockchain AST into queryable node-link JSON with `python3 scripts/finalize_audit_graph.py --codebase <path> --blockchain-ast audit-output/graph/blockchain-ast.json --out audit-output/graph/graph.json`.
5. Start graphify MCP with `python3 -m graphify.serve audit-output/graph/graph.json` when available.
6. Write `coverage.jsonl` for later blind-spot tracking.
7. If memory is enabled, query `scripts/lessons_db.py` and write `memory-recall.md`.

**Graph contract**: `graph.json` means graphify node-link JSON that can be loaded by graphify CLI/MCP. Raw `.graphify_extract.json` is an intermediate extraction file and must not be served directly.

**Phase gate**: Soft gate. If graph construction, finalization, or MCP startup fails, log the failure and continue to Phase 1 without graph features.

**Transition**: Pass graph artifact paths and memory recall path to all downstream agents.

---

### Phase 1: Reconnaissance

| Attribute | Value |
|-----------|-------|
| **Agent** | Self (orchestrator) |
| **Input** | Codebase path + optional protocol hint |
| **Output** | `audit-output/00-scope.md`, `audit-output/pipeline-state.md` |
| **Sub-agents** | None |
| **Estimated context** | ~500 lines (index.json + directory scan) |

**Steps**:
1. Create `audit-output/` directory with subdirectories: `pocs`, `fuzzing`, `certora`, `halmos`, `issues`, `context`, `personas`, `graph`, `attack-proofs`, `plan-execution`
2. Scan codebase for source files (all supported languages)
3. Detect language/framework using [protocol-detection.md](protocol-detection.md) signals
4. If user provided protocol hint → map directly to `protocolContext.mappings`
5. If no hint → run auto-detection, collect all matches
6. Read `DB/index.json` (~330 lines)
7. Resolve manifest list from all matched protocol types (union + dedupe)
8. Note corresponding hunt card files from `index.json` `huntcards.perManifest`
9. Load `DB/manifests/keywords.json`, scan first 100 lines of target code for keyword hits
10. Always include `general-security` + `unique` as baseline
11. Write `audit-output/00-scope.md`
12. Initialize `audit-output/pipeline-state.md` with metadata + all phases NOT_STARTED

**Phase gate**: `00-scope.md` exists with protocol types, manifest list, files in scope. At least 1 source file detected.

**Transition**: Pass `filesInScope`, `protocolTypes`, `manifestList` to Phase 2.

---

### Phase 2: Context Building

| Attribute | Value |
|-----------|-------|
| **Agent** | `audit-context-building` (coordinator sub-agent) |
| **Input** | `00-scope.md` + codebase path |
| **Output** | `audit-output/01-context.md` + `audit-output/context/*.md` |
| **Internal sub-agents** | `function-analyzer` ×N, `system-synthesizer` |
| **Estimated context** | Large — sub-agent manages its own context |

**Phase gate**: `01-context.md` exists with Contract Inventory, Actor Model, Trust Boundaries, Invariant Candidates.

**Error handling**: Retry with top 5 files on failure. Partial output is acceptable.

---

### Phase 3: Invariant Extraction + Review (Sequential Pair)

| Attribute | Value |
|-----------|-------|
| **Agents** | `invariant-writer` then `invariant-reviewer` (sequential) |
| **Input** | `01-context.md` + DB manifests |
| **Output** | `02-invariants.md` → `02-invariants-reviewed.md` |

**Step 3A**: Spawn `invariant-writer` → `02-invariants.md`
**Step 3B**: Spawn `invariant-reviewer` with `02-invariants.md` as input → `02-invariants-reviewed.md`

**Phase gate**: `02-invariants-reviewed.md` exists with at least 5 invariants across 2+ categories. Fall back to `02-invariants.md` if reviewer fails.

---

### Phase 4: Iterative Parallel Discovery (N rounds)

**This is the most compute-intensive phase.** Four independent discovery streams run **simultaneously** across multiple **rounds**. Between rounds, the orchestrator writes a shared discovery state file enabling cross-pollination.

| Stream | Agent(s) | Output per round | What It Finds |
|--------|----------|------------------|---------------|
| **4A** | Self (grep-prune) + N × `invariant-catcher` | `03-findings-shard-*-RN.md` | Known DB vulnerability patterns |
| **4B** | `protocol-reasoning` | `04a-reasoning-findings-RN.md` | Novel bugs, cross-domain interactions |
| **4C** | `multi-persona-orchestrator` (6 personas) | `04c-persona-findings-RN.md` | Multi-angle deep reasoning findings |
| **4D** | `missing-validation-reasoning` | `04d-validation-findings-RN.md` | Input validation gaps |

**Round loop**:
1. Round 1: All 4 streams run independently
2. Orchestrator merges → `discovery-state-round-1.md` (cross-pollination bus)
3. Round 2+: All streams re-run reading shared state — cross-check, gap-fill, variants
4. Repeat for `--discovery-rounds` iterations

**Cross-pollination state file** (`discovery-state-round-N.md`) contains:
- Cumulative finding summary table
- Cross-check requests (findings needing verification from other streams)
- Unexplored areas (code areas with zero coverage)
- Variant suggestions (root causes likely to have more instances)

**Wait barrier**: ALL streams must complete per round before writing state and proceeding.

**Error handling per stream**:

| Stream | Failure | Recovery |
|--------|---------|----------|
| 4A shard K | Retry shard K once | Continue with other shards |
| 4A all shards | Fall back to single-agent DB hunt | |
| 4B | Retry top 3 domains, 2 rounds | Skip if still fails |
| 4C | Retry 3 personas, 1 round | Skip if still fails |
| 4D | Skip | Other streams cover core vulns |
| Any stream R2+ | Skip that stream for remaining rounds | Use its earlier round findings |

---

### Phase 5: Merge, Deduplicate & Triage

| Attribute | Value |
|-----------|-------|
| **Agent** | Self |
| **Input** | All Phase 4 outputs from ALL rounds + `discovery-state-round-*.md` |
| **Output** | `05-findings-triaged.md` |

**Sequence**:
1. **Merge** all findings from 4 streams
2. **Cross-source correlation** — findings from 2+ streams get confidence boost
3. **Deduplicate** by root cause (5 critical questions)
4. **Falsification** protocol (5 checks per finding)
5. **Severity assessment** (Impact × Likelihood matrix)
6. **Assign stable IDs**: F-001, F-002, ... — these persist through ALL remaining phases
7. **Write** `05-findings-triaged.md` with summary, correlation table, findings, excluded findings

**Phase gate**: `05-findings-triaged.md` exists.

---

### Phase 6: PoC Generation & EXECUTION [CONDITIONAL]

| Attribute | Value |
|-----------|-------|
| **Condition** | **SKIPPED** if `--static-only` is set |
| **Agent** | `poc-writing` × N (generation) + Self (execution) |
| **Input** | `05-findings-triaged.md` + codebase |
| **Output** | `audit-output/pocs/F-NNN-poc.*` + `audit-output/06-poc-results.md` |

When skipped: Log `Phase 6: SKIPPED (--static-only mode)` to pipeline-state.md. Set all PoC statuses to N/A.

**Critical difference from old pipeline**: PoCs are not just generated — they are **compiled and run**.

**Sequence**:
1. For each CRITICAL/HIGH finding → spawn `poc-writing` sub-agent
2. For each generated PoC → **execute** using the target framework's test runner
3. Record results: PASS / COMPILE_FAIL / ASSERT_FAIL / REVERT / TIMEOUT / SKIP
4. **Retry policy**: For COMPILE_FAIL or ASSERT_FAIL, re-spawn `poc-writing` with error output (max 2 attempts total)
5. Write `06-poc-results.md` with summary table + execution logs

**Phase gate**: `06-poc-results.md` exists with results for every CRITICAL/HIGH finding.

---

### Phase 7: FV Generation & EXECUTION [CONDITIONAL]

| Attribute | Value |
|-----------|-------|
| **Condition** | **SKIPPED** if `--static-only` is set |
| **Agent** | `medusa-fuzzing` + `certora-verification` + `halmos-verification` (parallel generation) + Self (execution) |
| **Input** | `02-invariants-reviewed.md` + codebase |
| **Output** | `audit-output/fuzzing/`, `audit-output/certora/`, `audit-output/halmos/`, `audit-output/07-fv-results.md` |

When skipped: Log `Phase 7: SKIPPED (--static-only mode)` to pipeline-state.md. Set all FV statuses to N/A.

**Sequence**:
1. Spawn all 3 FV generators in parallel
2. For each generated suite → **compile** (forge build)
3. For each compiled suite → **execute** (medusa fuzz / halmos / certoraRun)
4. Map violations to existing findings or create NEW findings
5. Write `07-fv-results.md` with results per tool + invariant violation → finding mapping

**Phase gate**: `07-fv-results.md` exists.

---

### Phase 8: Pre-Judging (Validity Screen)

| Attribute | Value |
|-----------|-------|
| **Agent** | Judge(s) per `--judge` flag (single or all 3 in parallel) |
| **Input** | `05-findings-triaged.md`, `06-poc-results.md` (if available), `07-fv-results.md` (if available) |
| **Output** | `08-pre-judge-results.md` |

First pass of the **judging self-loop**. Judge(s) assess raw triaged findings for validity before polishing.

**Judge selection**:
- `--judge=sherlock` → sherlock-judging only (consensus 1/1)
- `--judge=cantina` → cantina-judge only (consensus 1/1)
- `--judge=code4rena` → code4rena-judge only (consensus 1/1)
- Default → all 3 judges in parallel (consensus 2/3)

**Rule**: Finding proceeds to Phase 9 only if it meets the consensus threshold for VALID.

**Phase gate**: `08-pre-judge-results.md` exists with VALID/INVALID verdicts for every finding.

---

### Phase 9: Issue Polishing (Valid Findings Only)

| Attribute | Value |
|-----------|-------|
| **Agent** | `issue-writer` × N |
| **Input** | `08-pre-judge-results.md` (validated list), `05-findings-triaged.md`, execution evidence (if available) |
| **Output** | `audit-output/issues/F-NNN-issue.md` + `audit-output/09-polished-findings.md` |

Only polish findings that passed Phase 8 pre-judging.

**Phase gate**: `09-polished-findings.md` exists.

---

### Phase 10: Deep Review (Line-by-Line Judge Verification)

| Attribute | Value |
|-----------|-------|
| **Agent** | Same judge(s) as Phase 8 (completes the self-loop) |
| **Input** | `09-polished-findings.md`, `issues/F-NNN-issue.md` |
| **Output** | `10-deep-review.md` |

Second pass of the **judging self-loop**. Same judge(s) review polished issues line by line, verifying every code reference, claim, and severity assignment.

**Verdicts per finding**: CONFIRMED / CONFIRMED-DOWNGRADED / REJECTED / NEEDS-REVISION

**Confirmation criteria**:
- **Full mode**: consensus threshold met in both rounds + execution evidence (PoC PASS or FV VIOLATED)
- **Static-only mode**: consensus threshold met in both rounds (no execution evidence required)

**Phase gate**: `10-deep-review.md` exists with final verdicts.

---

### Phase 11: Report Assembly

| Attribute | Value |
|-----------|-------|
| **Agent** | Self |
| **Input** | ALL pipeline artifacts |
| **Output** | `CONFIRMED-REPORT.md` |

Final report includes: configuration used, executive summary, confirmed findings with judge verdicts from both rounds, execution evidence (if full mode), invariant specifications, discovery cross-pollination record, pipeline execution record, rejected/downgraded findings, appendix.

---

## Error Handling Summary

| Phase | Failure Mode | Recovery |
|-------|-------------|----------|
| 1 | Can't detect protocol | Load ALL 11 manifests |
| 2 | Context building timeout | Retry with top 5 files; use partial output |
| 3 | Invariant extraction fails | Use invariant candidates from Phase 2 directly |
| 3 | Invariant review fails | Use `02-invariants.md` directly |
| 4 R1 | DB search finds no matches | Proceed — novel vulnerabilities possible |
| 4 R1 | Shard K fails | Retry once; continue with other shards |
| 4 R1 | Reasoning agent timeout | Retry top 3 domains + 2 rounds; skip if still fails |
| 4 R1 | Multi-persona fails | Retry 3 personas + 1 round; skip if still fails |
| 4 R1 | Validation agent fails | Skip — other streams cover core vulns |
| 4 R2+ | Any stream fails | Skip that stream for remaining rounds; use earlier round findings |
| 5 | Merge fails | Manual merge of available findings |
| 6 | PoC compile/assert fail | Retry once with error context; record failure |
| 6 | Skipped (static-only) | Normal — log SKIPPED |
| 7 | FV generation fails | Note in report; don't block pipeline |
| 7 | FV execution fails | Record error; FV artifacts still useful as specs |
| 7 | Skipped (static-only) | Normal — log SKIPPED |
| 8 | Judge fails | Retry once; if single-judge mode, try alternate judge as fallback |
| 8 | 2+ judges fail (triple mode) | Use remaining judge + orchestrator self-assessment |
| 9 | Issue writer fails | Use raw finding description instead |
| 10 | Judge fails | Same recovery as Phase 8 |
| 10 | NEEDS-REVISION verdict | Re-run issue-writer with feedback, re-judge (max 1 retry) |
| 11 | Any missing artifact | Note gap in report; proceed with available data |

---

## Context Budget Guidelines

| Phase | Max Context Lines | Strategy |
|-------|-------------------|----------|
| 1 | 500 | Read index.json + targeted file listing |
| 2 | Delegated | Coordinator manages sub-agent context |
| 3 | Delegated | Sub-agents manage own context |
| 4A (self) | Variable | Load only required hunt-card subsets, grep-prune, partition |
| 4A (subs) | ~30K per shard | Cards + code + invariants |
| 4B | Delegated | Spawns domain sub-agents internally |
| 4C | Delegated | Spawns 6 persona sub-agents internally |
| 4D | Delegated | Sub-agent manages own context |
| 5 | 2000 | Merge + deduplicate + triage |
| 6 | Per-finding | One poc-writing spawn per finding |
| 7 | Delegated | Sub-agents manage own context |
| 8 | Per-finding | One issue-writer spawn per finding |
| 9 | Delegated | Sub-agents manage own context |
| 10 | 1500 | Read verdicts + PoC results + FV results |
| 11 | 1000 | Assemble report from structured sections |

---

## Abort Conditions

Stop the pipeline early if:

1. **No source code found** at the provided path → Report error immediately
2. **Codebase is trivially small** (<50 LOC) → Run abbreviated pipeline (skip FV, persona)
3. **Phase 2 reveals the code is a test file / mock** → Report and stop
4. **All findings fail falsification AND confirmation** → Report "no vulnerabilities found" with full methodology notes
