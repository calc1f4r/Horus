# Orchestration Pipeline

> **Purpose**: Master reference for the 7-phase audit pipeline. Defines phase transitions, data handoffs, sub-agent contracts, error handling, and context budgets.
> **Consumer**: `audit-orchestrator` agent.

---

## Pipeline Overview

```
User Input: @audit-orchestrator <path> [hint]
    │
    ▼
┌─────────────────────────────────────┐
│ Phase 1: RECONNAISSANCE             │  Self (no sub-agent)
│ Protocol detection, scope, manifests│  Output: 00-scope.md
└──────────────┬──────────────────────┘
               │ protocolTypes, manifestList, filesInScope
               ▼
┌─────────────────────────────────────┐
│ Phase 2: CONTEXT BUILDING           │  Sub-agent: audit-context-building
│ Line-by-line codebase analysis      │  Output: 01-context.md
└──────────────┬──────────────────────┘
               │ architecture, functions, invariantCandidates
               ▼
┌─────────────────────────────────────┐
│ Phase 3: INVARIANT EXTRACTION       │  Sub-agent: invariant-writer
│ Structured property specs           │  Output: 02-invariants.md
└──────────────┬──────────────────────┘
               │ invariantSpecs (INV-*)
               ▼
┌─────────────────────────────────────┐
│ Phase 4: DB-POWERED HUNTING         │  Self + Sub-agent: invariant-catcher
│ Pattern matching against 537+ vulns │  Output: 03-findings-raw.md
└──────────────┬──────────────────────┘
               │ rawFindings (F-NNN)
               ▼
┌─────────────────────────────────────┐
│ Phase 4a: REASONING DISCOVERY       │  Sub-agent: protocol-reasoning-agent
│ Domain decomposition, 4-round deep  │  Output: 04a-reasoning-findings.md
│ reasoning, reachability proofs      │  (spawns domain sub-agents internally)
└──────────────┬──────────────────────┘
               │ reasoningFindings (F-4a-NNN)
               ▼
┌─────────────────────────────────────┐
│ Phase 5: VALIDATION GAP ANALYSIS    │  Sub-agent: missing-validation-reasoning
│ Input validation, access control    │  Output: 04-validation-findings.md
└──────────────┬──────────────────────┘
               │ additionalFindings (F-NNN)
               ▼
┌─────────────────────────────────────┐
│ Phase 6: TRIAGE & PoC              │  Self + Sub-agent: poc-writer (per finding)
│ Dedup, falsify, severity, PoCs     │  Output: 05-findings-triaged.md + pocs/
└──────────────┬──────────────────────┘
               │ triagedFindings + PoCs
               ▼
┌─────────────────────────────────────┐
│ Phase 7: DOWNSTREAM GENERATION      │  Sub-agents: medusa-fuzzing,
│ Fuzzing, formal verification,       │  certora-verification,
│ Sherlock + Cantina judging          │  sherlock-judging, cantina-judge
│                                     │  Output: 06/07-validation + fuzzing/ + certora/
└──────────────┬──────────────────────┘
               │ all artifacts
               ▼
┌─────────────────────────────────────┐
│ FINAL: REPORT ASSEMBLY              │  Self (no sub-agent)
│ Merge all outputs into report       │  Output: AUDIT-REPORT.md
└─────────────────────────────────────┘
```

---

## Phase Details

### Phase 1: Reconnaissance

| Attribute | Value |
|-----------|-------|
| **Agent** | Self (orchestrator) |
| **Input** | Codebase path + optional protocol hint |
| **Output** | `audit-output/00-scope.md` |
| **Sub-agents** | None |
| **Estimated context** | ~500 lines (index.json + directory scan) |

**Steps**:
1. Create `audit-output/` directory
2. Scan codebase: `find <path> -name "*.sol" -o -name "*.rs" -o -name "*.go" | head -50`
3. Detect language/framework using [protocol-detection.md](protocol-detection.md) signals
4. If user provided protocol hint → map directly to `protocolContext.mappings`
5. If no hint → run auto-detection, collect all matches
6. Read `DB/index.json` (~330 lines)
7. Resolve manifest list from all matched protocol types (union + dedupe)
8. Load `DB/manifests/keywords.json`, scan first 100 lines of target code for keyword hits to discover additional manifests
9. For maximum depth: include all manifests from matched types + `general-security` + `unique` as baseline
10. Write scope document to `audit-output/00-scope.md`

**Transition**: Pass `filesInScope`, `protocolTypes`, `manifestList` to Phase 2.

---

### Phase 2: Context Building

| Attribute | Value |
|-----------|-------|
| **Agent** | `audit-context-building` (sub-agent) |
| **Input** | Scope document + codebase path |
| **Output** | `audit-output/01-context.md` |
| **Sub-agents** | May spawn its own sub-agents for dense functions |
| **Estimated context** | Large — sub-agent manages its own context |

**Sub-agent prompt template**:
```
You are the audit-context-building agent. Analyze the following codebase for a security audit.

TARGET CODEBASE: <path>
FILES IN SCOPE: <file list from 00-scope.md>
PROTOCOL TYPE: <detected types>

Perform your full 3-phase workflow (orientation → micro-analysis → global understanding).

Write your complete output to audit-output/01-context.md following the format in
resources/inter-agent-data-format.md (Phase 2: Context Output section).

Include: Contract inventory, actor model, state variable map, function analysis,
cross-function flows, trust boundaries, invariant candidates, assumption register.
```

**Transition**: Read `audit-output/01-context.md`, extract `invariantCandidates` section for Phase 3.

**Error handling**: If sub-agent times out or fails, retry once with a reduced scope (top 5 entry-point files only). If still fails, log the error and continue to Phase 3 with whatever partial output exists.

---

### Phase 3: Invariant Extraction

| Attribute | Value |
|-----------|-------|
| **Agent** | `invariant-writer` (sub-agent) |
| **Input** | Context output from Phase 2 |
| **Output** | `audit-output/02-invariants.md` |
| **Estimated context** | Medium — reads context, produces specs |

**Sub-agent prompt template**:
```
You are the invariant-writer agent. Extract all invariants from the audit context.

Read audit-output/01-context.md for the complete codebase analysis.
TARGET CODEBASE: <path>

Perform your full 4-phase workflow (ingest → extract → validate → write).

Write output to audit-output/02-invariants.md following the format in
resources/inter-agent-data-format.md (Phase 3: Invariant Spec section).

Every invariant must have: ID, Property, Scope, Why, Testable.
Categories: Solvency, Access Control, State Machine, Arithmetic, Oracle, Cross-Contract.
```

**Transition**: Read `audit-output/02-invariants.md`, pass invariant specs + manifest list to Phase 4.

**Error handling**: If sub-agent fails, extract invariant candidates from Phase 2 context directly and use those (they won't be as structured but are usable).

---

### Phase 4: DB-Powered Hunting

| Attribute | Value |
|-----------|-------|
| **Agent** | Self (DB search) + `invariant-catcher` (sub-agent) |
| **Input** | Manifest list + invariant specs + codebase path |
| **Output** | `audit-output/03-findings-raw.md` |
| **Estimated context** | Variable — depends on number of manifests |

**Self-driven DB search sequence**:
1. For each manifest in `manifestList`:
   a. Load the manifest JSON
   b. For each pattern, extract `codeKeywords`
   c. Search target codebase: `grep -r "keyword1\|keyword2" <path> --include="*.sol"`
   d. For each hit: record manifest pattern ID, target file + line, keyword matched
2. Score hits: exact keyword match → HIGH, partial → MEDIUM
3. For HIGH-relevance hits, read the DB vulnerability content using `lineStart/lineEnd`:
   `read_file("DB/<path>/<file>.md", startLine=<lineStart>, endLine=<lineEnd>)`
4. Build a **pattern hit list** with: pattern ID, DB source, target locations, relevance score

**Sub-agent prompt template**:
```
You are the invariant-catcher agent. Hunt for vulnerability patterns in the target codebase.

TARGET CODEBASE: <path>
PROTOCOL TYPE: <detected types>

PATTERN HIT LIST (from DB scan):
<paste pattern hit list>

INVARIANT SPECS:
Read audit-output/02-invariants.md

Perform your full 5-step workflow (map → read DB → build patterns → hunt → report).

For each pattern hit, validate whether the target code is actually vulnerable:
- True positive: matches pattern AND has required preconditions
- Likely positive: matches but needs manual verification
- False positive: matches syntactically but not exploitable

Write ALL findings to audit-output/03-findings-raw.md using the Finding Schema
from resources/inter-agent-data-format.md.
```

**Transition**: Read raw findings, pass to Phase 4a alongside context.

**Error handling**: If invariant-catcher sub-agent fails, use the self-driven DB search results as raw findings (lower confidence but still useful).

---

### Phase 4a: Reasoning-Based Discovery

| Attribute | Value |
|-----------|-------|
| **Agent** | `protocol-reasoning-agent` (sub-agent) |
| **Input** | Codebase path + context + invariants + Phase 4 findings + manifest list |
| **Output** | `audit-output/04a-reasoning-findings.md` |
| **Estimated context** | Large — sub-agent manages its own context, spawns domain sub-agents |

**Sub-agent prompt template**:
```
You are the protocol-reasoning-agent. Perform deep reasoning-based vulnerability discovery.

TARGET CODEBASE: <path>
PROTOCOL TYPE: <detected types>
MANIFEST LIST: <manifests>

PIPELINE CONTEXT:
  - Read audit-output/01-context.md for architecture
  - Read audit-output/02-invariants.md for invariants
  - Read audit-output/03-findings-raw.md to avoid duplicates

Perform your full 6-phase workflow (Seeds → Domains → Round 1-4 → Merge).
Severity filter: MEDIUM, HIGH, CRITICAL only.
Every finding requires a reachability proof.

Write output to audit-output/04a-reasoning-findings.md following the format in
resources/inter-agent-data-format.md (Phase 4a section).
```

**Transition**: Read reasoning findings, merge with Phase 4 raw findings, pass to Phase 5.

**Error handling**: If sub-agent fails, retry once with reduced scope (top 3 domains, 2 rounds). If still fails, log and continue — Phase 4 findings remain valid.

---

### Phase 5: Validation Gap Analysis

| Attribute | Value |
|-----------|-------|
| **Agent** | `missing-validation-reasoning` (sub-agent) |
| **Input** | Codebase path + context from Phase 2 |
| **Output** | `audit-output/04-validation-findings.md` |
| **Estimated context** | Medium |

**Sub-agent prompt template**:
```
You are the missing-validation-reasoning agent. Scan for input validation vulnerabilities.

TARGET CODEBASE: <path>
CONTEXT: Read audit-output/01-context.md for architecture and function analysis.

Perform your full 5-phase workflow (constructor audit → invariants → attack surface → reasoning → documentation).

Write findings to audit-output/04-validation-findings.md using the Finding Schema
from resources/inter-agent-data-format.md.

Focus: zero-address checks, stale oracle data, array length mismatches,
numeric bounds, access control gaps, contract existence checks.
```

**Transition**: Merge validation findings with raw findings from Phase 4, pass all to Phase 6.

---

### Phase 6: Triage & PoC Generation

| Attribute | Value |
|-----------|-------|
| **Agent** | Self (triage) + `poc-writer` (sub-agent, per HIGH/CRIT finding) |
| **Input** | All raw findings from Phases 4+5 |
| **Output** | `audit-output/05-findings-triaged.md` + `audit-output/pocs/` |
| **Estimated context** | Variable — per-finding PoC spawns |

**Triage sequence**:
1. **Merge** all findings from `03-findings-raw.md`, `04a-reasoning-findings.md`, and `04-validation-findings.md`
2. **Deduplicate** by root cause — group findings that share the same underlying issue
3. **Falsification** — for each finding, apply the 5-check falsification protocol from [root-cause-analysis.md](root-cause-analysis.md):
   - Is there a check I missed that prevents this?
   - Does the execution order actually allow this?
   - Are the preconditions realistic?
   - Is there an external safeguard?
   - Can the impact actually be realized?
4. **Confidence scoring** — HIGH (include fully), MEDIUM (include with caveats), LOW (include as "potential"), SPECULATIVE (exclude)
5. **Severity assessment** — Impact × Likelihood matrix
6. **Exclude** findings that fail falsification (move to "Excluded Findings" section)
7. **Number** surviving findings sequentially: F-001, F-002, ...

**PoC generation** (for CRITICAL and HIGH findings only):
```
For each CRITICAL/HIGH finding:
  Spawn poc-writer sub-agent with:
    - Finding details (root cause, affected code, attack scenario)
    - Target codebase path
    - Output path: audit-output/pocs/F-NNN-poc.t.sol
```

**Transition**: Pass triaged findings to Phase 7.

---

### Phase 7: Downstream Generation

| Attribute | Value |
|-----------|-------|
| **Agents** | `medusa-fuzzing`, `certora-verification`, `sherlock-judging`, `cantina-judge` |
| **Input** | Invariant specs + triaged findings |
| **Outputs** | `audit-output/fuzzing/`, `audit-output/certora/`, `06-sherlock-validation.md`, `07-cantina-validation.md` |

**Spawn sequence** (these can run in parallel via agent tool):

1. **Medusa Fuzzing** — spawn `medusa-fuzzing` with invariant specs from `02-invariants.md`
2. **Certora Verification** — spawn `certora-verification` with invariant specs
3. **Sherlock Judging** — spawn `sherlock-judging` with triaged findings from `05-findings-triaged.md`
4. **Cantina Judging** — spawn `cantina-judge` with triaged findings

**Error handling**: If any downstream agent fails, note the failure in the report but don't block report assembly. Each downstream artifact is optional.

---

## Error Handling Summary

| Phase | Failure Mode | Recovery |
|-------|-------------|----------|
| 1 | Can't detect protocol | Load ALL 11 manifests |
| 2 | Context building timeout | Retry with top 5 files; use partial output |
| 3 | Invariant extraction fails | Use invariant candidates from Phase 2 directly |
| 4 | DB search finds no matches | Proceed — novel vulnerabilities possible |
| 4 | Invariant-catcher fails | Use self-driven DB search results |
| 4a | Reasoning agent timeout | Retry with top 3 domains + 2 rounds; skip if still fails |
| 5 | Validation agent fails | Skip — Phase 4+4a findings still valid |
| 6 | PoC generation fails | Document finding without PoC; add note |
| 7 | Any downstream fails | Note in report; don't block assembly |
| Final | Severity disagreement | Use LOWER rating (conservative) |

---

## Context Budget Guidelines

| Phase | Max Context Lines | Strategy |
|-------|-------------------|----------|
| 1 | 500 | Read index.json + targeted file listing |
| 2 | Delegated | Sub-agent manages own context |
| 3 | Delegated | Sub-agent manages own context |
| 4 (self) | 2000 | Load manifests one at a time, discard after keyword extraction |
| 4 (sub) | Delegated | Sub-agent manages own context |
| 4a | Delegated | Sub-agent manages own context; spawns domain sub-agents |
| 5 | Delegated | Sub-agent manages own context |
| 6 | 1500 | Merge findings, deduplicate, triage |
| 7 | Delegated | Sub-agents manage own context |
| Final | 1000 | Assemble report from structured sections |

---

## Abort Conditions

Stop the pipeline early if:

1. **No source code found** at the provided path → Report error immediately
2. **Codebase is trivially small** (<50 LOC) → Run abbreviated pipeline (skip Phase 3, 7)
3. **Phase 2 reveals the code is a test file / mock** → Report and stop
4. **All findings fail falsification** → Report "no vulnerabilities found" with methodology notes
