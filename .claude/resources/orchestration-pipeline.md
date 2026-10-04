# Orchestration Pipeline

> **Purpose**: Master reference for the graph-aware 11-phase configurable audit pipeline (plus opt-in Phase 12 DB flywheel) with Phase 0 graph foundation, prior-art-seeded iterative parallel discovery with an economic lane and coverage tracking, optional PoC/FV execution, a profitability gate, and a judging self-loop (pre-judge → polish → deep-review → remediation-safety gate). Defines phase transitions, data handoffs, sub-agent contracts, error handling, and context budgets.
> **Consumer**: `audit-orchestrator` agent. This reference must stay consistent with `audit-orchestrator.md` — when they disagree, the orchestrator wins.

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
│ Phase 1: RECONNAISSANCE             │  Sub-agent: recon-specialist
│ Protocol detection, scope, manifests│  Output: 00-scope.md (machine-readable
│ + diff scoping with blast radius    │  scope block), pipeline-state.md
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
    ┌── PRE-ROUNDS ──────────────────┐
    │ prior-art-matcher → 04-prior-art.md (discovery seeds) │
    │ grep-prune + shard (--scope-file 00-scope.md)         │
    │ extract_reasoning_seeds.py → reasoning-seeds.md       │
    └────────┬─────────────────────────┘
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
              │Economic│
              │ Lane   │
              │4E/4F/4G│
              └───┬────┘
               │ attack-graph-synthesizer → attack-candidates.json (post-discovery)
               ▼
    orchestrator → discovery-state-round-1.md
               │
    ┌── BETWEEN ROUNDS ────────────────┐
    │ attack-coverage-tracker → attack-coverage.json │
    │ + round-N-targets.md (unattacked surface)      │
    └──────────┬─────────────────────────┘
               │
    ┌──── ROUND 2+ (cross-pollination) ─┐
    │  All streams read shared state +   │
    │  round-N-targets.md; cross-check,  │
    │  gap-fill, go deeper               │
    └──────────┬─────────────────────────┘
               │ ... repeat for N rounds ...
               ▼
═══════════════════════════════════════════════════════
 TRIAGE (Phase 5)
═══════════════════════════════════════════════════════
               │
┌─────────────────────────────────────┐
│ Phase 5: MERGE & TRIAGE            │  Sub-agent: finding-merger
│ Root-cause clustering, falsify,     │  Output: 05-findings-triaged.md
│ conservation, severity+confidence   │  (+ coverage-report.md gate before)
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
│ Phase 6a: PROFITABILITY GATE        │  Sub-agent: economic-attack-simulator
│ [CONDITIONAL — HIGH/CRITICAL in     │  Output: 06-profitability.md
│ full mode with economic findings]   │  → feeds Phases 8/10/11 as impact
└──────────────┬──────────────────────┘  evidence
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
┌─────────────────────────────────────┐
│ Phase 10b: REMEDIATION SAFETY GATE  │  Sub-agent: remediation-safety-checker
│ Verify recommended fixes are safe   │  Output: 10b-remediation-safety.md
│ UNSAFE remediation cannot ship      │
└──────────────┬──────────────────────┘
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
               │
               ▼
┌─────────────────────────────────────┐
│ Phase 12: DB FLYWHEEL               │  Sub-agent: findings-db-synthesizer
│ [OPT-IN] confirmed findings → DB    │  Output: DB entries + invariants
│ entries + invariant library growth  │  (runs generation contract)
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
| 1 | `00-scope.md` (machine-readable scope block), `pipeline-state.md`, `memory-state.md` (init) | Codebase path, DB/index.json |
| 2 | `01-context.md`, `context/*.md` | `00-scope.md`, `memory-state.md` |
| 3 | `02-invariants-reviewed.md` | `01-context.md`, DB manifests, `memory-state.md` |
| 4 (pre-rounds) | `04-prior-art.md`, `hunt-card-hits.json`, `hunt-card-shards.json`, `reasoning-seeds.md` | `00-scope.md` (scope block via `--scope-file`), reports/, DeFiHackLabs, hunt cards |
| 4 (per round) | `*-RN.md` outputs per stream, `04e-tokenomics-findings.md`, `04f-risk-param-findings.md`, `04g-manipulation-findings.md` (conditional economic lane), `attack-candidates.*`, `attack-coverage.json`, `round-N-targets.md`, `coverage-report.md` (final round), `discovery-state-round-N.md` | Hunt cards, `04-prior-art.md` seeds, `DB/graphify-out/graph.json`, `graph/graph.json`, invariants, context, previous round state + targets, `memory-state.md` |
| 5 | `05-findings-triaged.md` | All Phase 4 outputs from all rounds, `coverage-report.md`, `memory-state.md` |
| 6 [CONDITIONAL] | `pocs/F-NNN-poc.*`, `06-poc-results.md` | `05-findings-triaged.md`, codebase, `memory-state.md` |
| 6a [CONDITIONAL] | `06-profitability.md` | `05-findings-triaged.md`, `attack-candidates.json`, exploit chains |
| 7 [CONDITIONAL] | `fuzzing/`, `certora/`, `halmos/`, `07-fv-results.md` | `02-invariants-reviewed.md`, codebase, `memory-state.md` |
| 8 | `08-pre-judge-results.md` | `05-findings-triaged.md`, execution evidence + `06-profitability.md` (if available), `memory-state.md` |
| 9 | `issues/F-NNN-issue.md`, `09-polished-findings.md` | `08-pre-judge-results.md`, triaged findings, execution evidence, `06-profitability.md` (if available), `memory-state.md` |
| 10 | `10-deep-review.md` | `09-polished-findings.md`, `issues/F-NNN-issue.md`, `06-profitability.md` (if available), `memory-state.md` |
| 10b | `10b-remediation-safety.md` | `09-polished-findings.md`, `01-context.md`, `02-invariants-reviewed.md`, DB anti-pattern hunt cards |
| 11 | `CONFIRMED-REPORT.md` | ALL outputs (incl. `06-profitability.md`, `10b-remediation-safety.md`) |
| 12 [OPT-IN] | DB entries, hunt-card enrichments, `invariants/` candidates | `CONFIRMED-REPORT.md`, `05-findings-triaged.md`, judge verdict logs, PoCs |

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
| **Agent** | `recon-specialist` (sub-agent; orchestrator falls back to inline recon only when unavailable) |
| **Input** | Codebase path + optional protocol hint + optional `--diff=<base_ref>` |
| **Output** | `audit-output/00-scope.md` (incl. machine-readable scope block + dependency list), `audit-output/pipeline-state.md` |
| **Sub-agents** | None (recon-specialist is itself a sub-agent) |
| **Estimated context** | ~500 lines (index.json + directory scan) |

**recon-specialist owns**:
1. Protocol detection mapped to `DB/index.json` protocol routing
2. Scope resolution (in/out-of-scope files with rationale, dependency list)
3. External surface mapping (oracles, deployed addresses, proxies, tokens, fee receivers, privileged roles)
4. Diff scoping: with a base ref, only changed code + blast radius is scope
5. Emits `00-scope.md` with the machine-readable JSON scope block — `grep_prune.py` and `partition_shards.py` consume it via `--scope-file`; the orchestrator's gate parses it for Phase 4 spawn conditions

**Phase gate**: `00-scope.md` exists with protocol types, manifest list, files in scope, and a JSON scope block that parses. At least 1 source file detected.

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

**This is the most compute-intensive phase.** Four independent discovery streams run **simultaneously** across multiple **rounds**, preceded by prior-art seeding and accompanied (conditionally) by the economic lane. Between rounds, the coverage tracker steers the next round at unattacked surface.

**Pre-rounds (before Round 1)**:
1. Spawn `prior-art-matcher` → `04-prior-art.md`: lineage fingerprinting, prior audits (local `reports/` then Solodit), DeFiHackLabs incident matching — applicable items become high-priority discovery seeds
2. Grep-prune hunt cards with `--scope-file audit-output/00-scope.md` → shard → extract `reasoning-seeds.md` from surviving cards
3. If prior-art-matcher fails or finds no lineage, log and continue unseeded

| Stream | Agent(s) | Output per round | What It Finds |
|--------|----------|------------------|---------------|
| **4A** | Self (grep-prune) + N × `invariant-catcher` | `03-findings-shard-*-RN.md` | Known DB vulnerability patterns |
| **4B** | `protocol-reasoning` (consumes `reasoning-seeds.md`) | `04a-reasoning-findings-RN.md` | Novel bugs, cross-domain interactions |
| **4C** | `multi-persona-orchestrator` (6 personas) | `04c-persona-findings-RN.md` | Multi-angle deep reasoning findings |
| **4D** | `missing-validation-reasoning` | `04d-validation-findings-RN.md` | Input validation gaps |
| **4E** [CONDITIONAL] | `tokenomics-auditor` | `04e-tokenomics-findings.md` | Token/emission/vesting/treasury value-flow bugs (spawn when scope contains token/emission/vesting/treasury contracts) |
| **4F** [CONDITIONAL] | `risk-parameter-reviewer` | `04f-risk-param-findings.md` | LTV/liquidation/IRM/peg parameter breaks (spawn when lending/stablecoin mechanics in scope) |
| **4G** [CONDITIONAL] | `manipulation-feasibility-analyst` | `04g-manipulation-findings.md` | Oracle manipulation cost vs. extractable value, MEV surface (spawn when any price feed or DEX interaction in scope) |

Economic-lane spawn conditions are derived from the machine-readable scope block (`protocol_types`, `external_surface`), not guesswork. 4G's FEASIBLE scenarios feed the Phase 6a profitability gate.

Post-discovery: `attack-graph-synthesizer` walks the codebase graph against the invariant suite → `attack-candidates.json` for `protocol-reasoning` validation.

**Round loop**:
1. Round 1: All streams run independently
2. Orchestrator merges → `discovery-state-round-1.md` (cross-pollination bus)
3. Between rounds: `attack-coverage-tracker` updates `attack-coverage.json` and emits `round-N-targets.md` (never-attacked, pattern-only, unexercised-invariant, untraversed-edge gaps) — injected into every lane prompt for rounds > 1
4. Round 2+: All streams re-run reading shared state + round targets — cross-check, gap-fill, variants
5. Repeat for `--discovery-rounds` iterations
6. Final round: `attack-coverage-tracker` emits `coverage-report.md` (honest attack/invariant coverage percentages) before Phase 5

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
| **Agent** | `finding-merger` (sub-agent; orchestrator falls back to inline triage only when unavailable) |
| **Input** | All Phase 4 outputs from ALL rounds + `discovery-state-round-*.md` + `coverage-report.md` + `memory-state.md` |
| **Output** | `05-findings-triaged.md` |

**Sequence** (owned by finding-merger):
1. **Ingest** every `04*` findings artifact — conservation-checked, no finding silently dropped (every input appears in exactly one cluster or is recorded as dismissed with reason)
2. **Root-cause clustering** — group by underlying cause, not symptom or reporter
3. **Falsification pass** — re-read cited line ranges, attempt disproof; INVALID verdicts carry file:line disproof
4. **Severity pre-assignment** with confidence (HIGH/MED/LOW — judges own final severity)
5. **Deduplicate** against `memory-state.md` DEAD_END entries
6. **Assign stable IDs**: F-001, F-002, ... — these persist through ALL remaining phases
7. **Write** `05-findings-triaged.md` per the inter-agent Finding Schema with merged evidence, reporter list, falsification verdict, and `unaccounted: 0`

**Phase gate**: `05-findings-triaged.md` exists and finding-merger reports unaccounted = 0.

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

### Phase 6a: Profitability Gate [CONDITIONAL]

| Attribute | Value |
|-----------|-------|
| **Condition** | Full mode (not `--static-only`) and HIGH/CRITICAL findings with economic impact or exploit chains present |
| **Agent** | `economic-attack-simulator` |
| **Input** | `05-findings-triaged.md`, `attack-candidates.json`, exploit chains |
| **Output** | `audit-output/06-profitability.md` |

Per candidate attack: attacker profit model (flash-loan cost, gas, slippage/price impact, achievable oracle deviation, MEV competition), net-USD profit under best/typical/worst conditions. Verdicts: `PROFITABLE` / `CONDITIONAL (parameters listed)` / `UNPROFITABLE (binding constraint named)`.

Gate rules: UNPROFITABLE findings skip `poc-writing` (recorded, not silently dropped); CONDITIONAL findings proceed with the flip-regime documented; `06-profitability.md` flows into Phases 8, 9, 10, and 11 as quantified-impact evidence for judges and the report.

**Phase gate**: `06-profitability.md` exists when the gate condition held; findings it covers carry verdicts.

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

### Phase 10b: Remediation Safety Gate

| Attribute | Value |
|-----------|-------|
| **Agent** | `remediation-safety-checker` |
| **Input** | `09-polished-findings.md`, `issues/F-NNN-issue.md`, `01-context.md`, `02-invariants-reviewed.md`, DB anti-pattern hunt cards |
| **Output** | `audit-output/10b-remediation-safety.md` |

Every remediation Horus recommends gets one verdict — `SAFE` / `RISKY (concerns listed)` / `UNSAFE (do not ship as-is)` — across six checks: root-cause coverage, blast radius, honest-flow impact, cross-finding fix interactions, invariant compliance, and DB anti-pattern query of the fix pattern itself. RISKY/UNSAFE verdicts ship rewritten remediation text into the report draft before Phase 11.

**Gate rule**: Phase 11 refuses to assemble a report containing an UNSAFE remediation.

**Phase gate**: `10b-remediation-safety.md` exists with exactly one verdict per remediation.

---

### Phase 11: Report Assembly

| Attribute | Value |
|-----------|-------|
| **Agent** | Self |
| **Input** | ALL pipeline artifacts |
| **Output** | `CONFIRMED-REPORT.md` |

Final report includes: configuration used, executive summary, confirmed findings with judge verdicts from both rounds, execution evidence (if full mode), profitability verdicts with quantified net-USD impact where the simulator ran, remediation-safety verdicts, invariant specifications, discovery cross-pollination record, pipeline execution record, rejected/downgraded findings, appendix.

---

### Phase 12: DB Flywheel [OPT-IN]

| Attribute | Value |
|-----------|-------|
| **Agent** | `findings-db-synthesizer` |
| **Input** | `CONFIRMED-REPORT.md`, `05-findings-triaged.md`, `issues/`, judge verdict logs, PoCs |
| **Output** | New TEMPLATE.md-compliant DB entries (CONFIRMED or HIGH-with-PoC findings only), hunt-card enrichments, `invariants/` candidates; runs the generation contract (`generate_manifests.py`, `build_db_graph.py` when needed, `db_quality_check.py`) and only commits when the quality check passes |

Closes the loop: every audit's judge-confirmed findings become next audit's DB hunting strength. Dedup against the existing DB first — `enrich beats duplicate`; invalidated findings contribute misjudgment notes only, never entries.

**Phase gate**: opt-in only; skipped silently otherwise.

---

## Error Handling Summary

| Phase | Failure Mode | Recovery |
|-------|-------------|----------|
| 1 | Can't detect protocol | Load ALL 14 manifests |
| 1 | recon-specialist fails | Fall back to orchestrator inline recon (legacy path) |
| 2 | Context building timeout | Retry with top 5 files; use partial output |
| 3 | Invariant extraction fails | Use invariant candidates from Phase 2 directly |
| 3 | Invariant review fails | Use `02-invariants.md` directly |
| 4 pre | prior-art-matcher fails / no lineage | Log and continue — discovery proceeds unseeded |
| 4 R1 | DB search finds no matches | Proceed — novel vulnerabilities possible |
| 4 R1 | Shard K fails | Retry once; continue with other shards |
| 4 R1 | Reasoning agent timeout | Retry top 3 domains + 2 rounds; skip if still fails |
| 4 R1 | Multi-persona fails | Retry 3 personas + 1 round; skip if still fails |
| 4 R1 | Validation agent fails | Skip — other streams cover core vulns |
| 4 econ | Economic-lane agent out of surface | Fast no-op with logged reason (by design) |
| 4 | attack-coverage-tracker fails | Log; rounds proceed without targets file |
| 4 R2+ | Any stream fails | Skip that stream for remaining rounds; use earlier round findings |
| 5 | finding-merger fails | Fall back to orchestrator inline triage (legacy path) |
| 6 | PoC compile/assert fail | Retry once with error context; record failure |
| 6 | Skipped (static-only) | Normal — log SKIPPED |
| 6a | Simulator fails or no economic findings | Skip gate; judges proceed without profit evidence |
| 7 | FV generation fails | Note in report; don't block pipeline |
| 7 | FV execution fails | Record error; FV artifacts still useful as specs |
| 7 | Skipped (static-only) | Normal — log SKIPPED |
| 8 | Judge fails | Retry once; if single-judge mode, try alternate judge as fallback |
| 8 | 2+ judges fail (triple mode) | Use remaining judge + orchestrator self-assessment |
| 9 | Issue writer fails | Use raw finding description instead |
| 10 | Judge fails | Same recovery as Phase 8 |
| 10 | NEEDS-REVISION verdict | Re-run issue-writer with feedback, re-judge (max 1 retry) |
| 10b | remediation-safety-checker fails | Gate degrades open with warning; UNSAFE cannot be asserted |
| 11 | Any missing artifact | Note gap in report; proceed with available data |
| 12 | Quality check fails after entry writes | Do not commit; report failure honestly |

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
| 5 | Delegated | finding-merger manages own context (fallback: 2000 inline) |
| 6 | Per-finding | One poc-writing spawn per finding |
| 6a | Delegated | economic-attack-simulator manages own context |
| 7 | Delegated | Sub-agents manage own context |
| 8 | Per-finding | One issue-writer spawn per finding |
| 9 | Delegated | Sub-agents manage own context |
| 10 | 1500 | Read verdicts + PoC results + FV results |
| 10b | Delegated | remediation-safety-checker manages own context |
| 11 | 1000 | Assemble report from structured sections |
| 12 | Delegated | findings-db-synthesizer manages own context |

---

## Abort Conditions

Stop the pipeline early if:

1. **No source code found** at the provided path → Report error immediately
2. **Codebase is trivially small** (<50 LOC) → Run abbreviated pipeline (skip FV, persona)
3. **Phase 2 reveals the code is a test file / mock** → Report and stop
4. **All findings fail falsification AND confirmation** → Report "no vulnerabilities found" with full methodology notes
