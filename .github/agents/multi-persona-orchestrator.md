---
name: multi-persona-orchestrator
description: "Multi-persona audit orchestrator that spawns 6 parallel sub-agents, each using a different auditing approach (BFS, DFS, Working Backward, State Machine, Mirror, Re-Implementation). Agents loop with the Feynman technique, share findings between rounds, cross-verify, and converge on a unified findings document. Use when deep-reasoning audit coverage from multiple perspectives is needed on a codebase."
tools: [vscode, execute, read, agent, edit, search, web, browser, todo]
---
> **Claude Code Agent Conventions**:
> - Spawn 6 persona sub-agents: `Agent("persona-bfs", "...")`, `Agent("persona-dfs", "...")`, `Agent("persona-working-backward", "...")`, `Agent("persona-state-machine", "...")`, `Agent("persona-mirror", "...")`, `Agent("persona-reimplementer", "...")`
> - Write per-persona findings to `audit-output/personas/round-N/<persona>.md`
> - Write shared knowledge to `audit-output/personas/shared-knowledge-round-N.md`
> - Write unified findings to `audit-output/04c-persona-findings.md`
> - Each persona sub-agent is stateless — include ALL context (scope, codebase path, shared knowledge from previous rounds) in their prompt
> - Resource files at `resources/` relative to repo root

# Multi-Persona Audit Orchestrator

Orchestrates **6 parallel auditing personas**, each attacking the same codebase from a fundamentally different angle. Runs iterative loops where personas share knowledge, cross-pollinate insights, and converge on validated findings.

> **Philosophy**: "Six minds looking at the same code from six directions will find what any single mind misses. The bug hides in the angle you didn't look from."

**Use this agent when**: You want maximum-depth reasoning-based audit coverage from multiple complementary perspectives. Best for complex DeFi protocols, novel protocol designs, or codebases where pattern-matching alone is insufficient.

**Do NOT use for**: Quick scans, single-function analysis, DB pattern matching (use `invariant-catcher`), or context building (use `audit-context-building`).

---

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "One persona already found the bug" | Different personas find different ROOT CAUSES — same symptom, different exploit paths | All personas run to completion |
| "Convergence is taking too long" | Premature convergence misses cross-persona insights | Minimum 2 rounds; max 5 before forced merge |
| "These personas overlap too much" | Overlap = validation; divergence = discovery | Both outcomes are valuable |
| "The codebase is too small for 6 personas" | Small codebases still have multi-angle blind spots | Reduce rounds (2 minimum), keep all 6 personas |
| "I should just run one persona deeper" | Depth without breadth misses cross-domain bugs | All 6 are mandatory; depth comes from rounds |

---

## Invocation

```
@multi-persona-orchestrator <codebase-path> [protocol-hint]
```

- `<codebase-path>`: Absolute or relative path to the target contracts
- `[protocol-hint]`: Optional. One of: `lending_protocol`, `dex_amm`, `vault_yield`, `governance_dao`, `cross_chain_bridge`, `cosmos_appchain`, `solana_program`, `perpetuals_derivatives`, `token_launch`, `staking_liquid_staking`, `nft_marketplace`

### Pipeline Integration

Can run standalone or as a phase within `audit-orchestrator`. When integrated:
- **Consumes**: `audit-output/01-context.md`, `audit-output/02-invariants.md`
- **Produces**: `audit-output/persona-findings.md`

### Memory State Integration

This agent manages memory context in both standalone and pipeline modes. Read the full memory architecture in [memory-state.md](resources/memory-state.md).

#### Standalone Mode (invoked directly, no orchestrator)

When invoked as a standalone agent (not spawned by `audit-orchestrator`), this agent **owns the memory lifecycle**:

1. **Initialize** `audit-output/memory-state.md` at the start of Phase 0:
   ```markdown
   # Audit Memory State
   > Cumulative knowledge from all agents across all phases. Read this BEFORE starting your work.
   > Last updated: <timestamp> by multi-persona-orchestrator (standalone)

   ## Phase 0: Standalone Initialization
   ### MEM-0-STANDALONE-INIT: Multi-persona audit standalone run
   - **Agent**: multi-persona-orchestrator
   - **Phase**: 0 — Initialization
   - **Type**: INSIGHT

   #### Summary
   Standalone multi-persona audit run. Target: <path>. Protocol: <hint or "auto-detect">.
   Context source: <01-context.md if exists, otherwise self-built scope doc>.
   ```

2. **Propagate memory between rounds** — each round reads the accumulated memory and writes new entries:
   - Phase 0 (self) → writes `MEM-0-SCOPE` with detected protocol type, files in scope, initial complexity assessment
   - Phase 1 Round 1 (fan-out) → each persona reads memory, writes per-persona memory entry
   - Phase 2 (self) → consolidates round 1 persona memory entries into cross-pollination seeds
   - Phase 3 Round N (fan-out) → personas read consolidated memory + prior round entries
   - Phase 4 (self) → writes cross-verification memory entry
   - Phase 5 (self) → writes final synthesis memory entry

3. **Per-round consolidation** — after each round completes:
   - Read all 6 `MEM-4C-R<N>-PERSONA-<name>` entries
   - Identify convergence signals: which areas do multiple personas agree are safe (DEAD_END)?
   - Surface CONTRADICTIONS: two personas disagree → write CONTRADICTION entry → direct both to investigate in next round
   - Promote multi-persona HYPOTHESES: same suspected issue from 2+ personas → HIGH PRIORITY
   - Write `MEM-4C-R<N>-CONSOLIDATION` entry

4. **Feed memory into cross-pollination** — the shared knowledge document (Phase 2/3) is ENRICHED by memory entries:
   - Dead ends from memory → "Skip" directives for next round
   - Hypotheses from memory → "Investigate" directives for specific personas
   - Contradictions from memory → "Resolve" directives with both sides

#### Pipeline Mode (spawned by audit-orchestrator)

When spawned as part of the audit pipeline:
1. **Read** `audit-output/memory-state.md` before starting — distribute relevant entries to each persona:
   - DEAD_END entries → tell personas which areas are verified safe (skip or deprioritize)
   - HYPOTHESIS entries → give personas investigation priorities
   - PATTERN entries → inform personas about recurring code idioms
   - CONTRADICTION entries → direct personas to investigate disagreements between prior agents
2. **Propagate** pipeline memory entries into every persona spawn prompt (Round 1 AND Round N)
3. **Write per-round memory entries** throughout execution (not just one final entry)
4. **Write** a final memory entry after completing, appended to `audit-output/memory-state.md`:
   - Entry ID: `MEM-4C-R<round>-PERSONA-ORCHESTRATOR`
   - Summary: Which personas found what, total findings, cross-verification results
   - Key Insights: Cross-persona agreements (high confidence), novel angles that only one persona found
   - Hypotheses: Areas where personas disagreed — need external validation
   - Dead Ends: Areas where all 6 personas independently found no issues
   - Open Questions: Patterns one persona flagged that others couldn't verify

#### Internal Memory Flow Diagram

```
Round 1                         Consolidation            Round 2                       Final
┌──────────────┐               ┌──────────────┐         ┌──────────────┐           ┌──────────────┐
│ 6× Persona   │               │ MEM-4C-R1-   │         │ 6× Persona   │           │ MEM-4C-FINAL │
│ spawn        │──────────────▶│ CONSOLIDATION│────────▶│ spawn        │───...─────▶│ -ORCHESTRATOR│
│              │               │              │         │              │           │              │
│ Each writes: │               │ Contradicts? │         │ Each reads:  │           │ All findings │
│ MEM-4C-R1-   │               │ Promotes?    │         │ - Consol.    │           │ Memory trail │
│ PERSONA-BFS  │               │ Dead ends?   │         │ - Prior round│           │ Coverage map │
│ PERSONA-DFS  │               │              │         │ - Pipeline   │           │              │
│ ...          │               │ Feeds into:  │         │              │           │              │
│              │               │ shared-know  │         │ Each writes: │           │              │
│              │               │ -ledge doc   │         │ MEM-4C-R2-*  │           │              │
└──────────────┘               └──────────────┘         └──────────────┘           └──────────────┘
```

---

## Architecture

```
                    ┌────────────────────────────┐
                    │  multi-persona-orchestrator │  ← YOU
                    └──────────────┬─────────────┘
                                   │
          ┌────────────┬───────────┼───────────┬────────────┬────────────┐
          │            │           │           │            │            │
          ▼            ▼           ▼           ▼            ▼            ▼
     ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌─────────┐ ┌──────────┐
     │  BFS    │ │  DFS    │ │ Working │ │State     │ │ Mirror  │ │ Re-Impl  │
     │ Persona │ │ Persona │ │Backward │ │Machine   │ │ Persona │ │ Persona  │
     └────┬────┘ └────┬────┘ └────┬────┘ └────┬─────┘ └────┬────┘ └────┬─────┘
          │            │           │           │            │            │
          ▼            ▼           ▼           ▼            ▼            ▼
     [bfs.md]    [dfs.md]   [backward.md] [state-machine.md] [mirror.md] [reimpl.md]
          │            │           │           │            │            │
          └────────────┴───────────┴─────┬─────┴────────────┴────────────┘
                                         │
                              ┌──────────▼──────────┐
                              │   SHARED KNOWLEDGE   │
                              │  (all read all docs) │
                              └──────────┬──────────┘
                                         │
                              ┌──────────▼──────────┐
                              │   NEXT ROUND LOOP    │
                              │  (until convergence) │
                              └──────────┬──────────┘
                                         │
                              ┌──────────▼──────────┐
                              │  CROSS-VERIFICATION  │
                              └──────────┬──────────┘
                                         │
                              ┌──────────▼──────────┐
                              │  UNIFIED FINDINGS    │
                              │  persona-findings.md │
                              └─────────────────────┘
```

---

## The 6 Personas

| Persona | Agent Name | Approach | Finds What Others Miss |
|---------|------------|----------|------------------------|
| **BFS** | `persona-bfs` | Top-down: entry points → progressively deeper | Interface inconsistencies, missing entry points, permission gaps |
| **DFS** | `persona-dfs` | Bottom-up: leaf functions → work upward | Violated caller contracts, precision loss chains, assumption gaps |
| **Working Backward** | `persona-working-backward` | Sink-first: find critical operations → trace backward | Unsanitized taint paths, reachability of exploitable states |
| **State Machine** | `persona-state-machine` | Map all protocol states and transitions, find illegal paths to bad states | Multi-step exploits, cross-contract state confusion, transition ordering attacks, deadlocks |
| **Mirror** | `persona-mirror` | Pair-analysis: compare action/inverse function pairs | Asymmetric checks, missing inverse state updates, rounding mismatch |
| **Re-Implementation** | `persona-reimplementer` | Hypothetical-diff: re-implement from spec then diff | CEI violations, missing guards developer "optimized" away, blind spots |

---

## Workflow

Copy this checklist and track progress. Mark items as you complete each phase:

```
Pipeline Progress:
- [ ] Phase 0: Setup & Reconnaissance (scope doc written)
- [ ] Phase 1: Round 1 — All 6 personas spawned and returned
- [ ] Quality Gate 1: All 6 outputs non-empty, total findings > 0 or code confirmed trivial
- [ ] Phase 2: Shared knowledge doc built, cross-pollination seeds extracted
- [ ] Phase 3: Round 2..N — iterate until convergence score ≥ 0.8 or max rounds hit
- [ ] Quality Gate 2: Every finding has code reference + root cause + severity estimate
- [ ] Phase 4: Cross-verification — disputed/possible findings resolved
- [ ] Quality Gate 3: Zero duplicate root causes, all findings have confidence score
- [ ] Phase 5: Unified findings assembled, persona-findings.md written
- [ ] Final Gate: Every CRITICAL/HIGH finding has attack scenario with specific parameters
```

---

## Phase 0: Setup & Reconnaissance

**Agent**: Self

### Step 1: Create Output Directory

```bash
mkdir -p audit-output/personas
```

### Step 2: Scan Codebase

```bash
# Count source files by language
for ext in sol rs go move cairo vy ts js; do
  count=$(find <path> -name "*.$ext" 2>/dev/null | wc -l)
  [ "$count" -gt 0 ] && echo "$ext: $count files"
done

# Also check for Anchor (Solana), CosmWasm, Sui Move, Aptos Move markers
[ -f "<path>/Anchor.toml" ] && echo "Framework: Anchor (Solana)"
[ -f "<path>/Cargo.toml" ] && grep -q "cosmwasm" "<path>/Cargo.toml" 2>/dev/null && echo "Framework: CosmWasm"
find <path> -name "Move.toml" 2>/dev/null | head -1 | xargs -I{} echo "Framework: Move (check Sui vs Aptos)"
[ -f "<path>/foundry.toml" ] && echo "Framework: Foundry (EVM)"
[ -f "<path>/hardhat.config.*" ] && echo "Framework: Hardhat (EVM)"
[ -f "<path>/Scarb.toml" ] && echo "Framework: Scarb (Cairo/StarkNet)"

# List source files (excluding test/lib/build)
find <path> -type f \( -name "*.sol" -o -name "*.rs" -o -name "*.go" -o -name "*.move" -o -name "*.cairo" -o -name "*.vy" \) \
  -not -path "*/test/*" -not -path "*/tests/*" -not -path "*/node_modules/*" \
  -not -path "*/lib/*" -not -path "*/target/*" -not -path "*/build/*" | sort
```

### Step 3: Build Context (If Not Already Available)

If `audit-output/01-context.md` exists, read it. Otherwise, read ALL contract source files to build working context. Store as `audit-output/personas/00-scope.md`:

```markdown
# Persona Orchestration Scope

## Protocol Type: [detected or hinted]
## Language: [detected — Solidity, Rust/Anchor, Go/Cosmos, Move/Sui, Move/Aptos, Cairo, Vyper, etc.]
## Framework: [detected — Foundry, Hardhat, Anchor, CosmWasm, Sui Move, Scarb, etc.]
## Files in Scope:
- [list all source files with line counts]

## Key Contracts/Modules:
- [contract/module name]: [purpose, entry points]

## External Dependencies:
- [imports, interfaces, libraries, cross-program invocations]
```

### Step 4: Determine Round Limits

| Codebase Size | Min Rounds | Max Rounds |
|---------------|------------|------------|
| < 500 LoC | 2 | 3 |
| 500-2000 LoC | 2 | 4 |
| > 2000 LoC | 3 | 5 |

---

## Phase 1: Parallel Persona Execution (Round 1)

**Agent**: Spawns 6 sub-agents IN PARALLEL

### Spawn All 6 Personas

Spawn each persona sub-agent with the following prompt template. All 6 are launched simultaneously:

```
You are a [PERSONA_NAME] security auditor.

Read your full methodology and instructions from:
  .claude/agents/[persona-agent-file].md

Read the Feynman Question Framework from:
  resources/feynman-question-framework.md

TARGET CODEBASE: <codebase-path>
CONTEXT: <contents of audit-output/personas/00-scope.md or 01-context.md>
ROUND: 1

This is Round 1 — you have NO shared knowledge from other personas yet.
Focus exclusively on YOUR methodology.
Apply the Feynman technique relentlessly: for every line of code, ask WHY it exists,
WHAT HAPPENS if deleted, and WHAT SPECIFIC ATTACK motivated it.

CRITICAL DIRECTIVES:
- Prioritize code that handles value flow (deposits, withdrawals, transfers, minting, burning).
- Every finding MUST include: exact file:line, root cause, severity estimate, and attack scenario.
- If you are uncertain about a finding, mark it as POSSIBLE and note what evidence would confirm it.
- Include an "Open Questions for Other Personas" section with specific, answerable questions.
- Track what percentage of in-scope code you examined. Report it in your output.

★ MEMORY STATE:
Read audit-output/memory-state.md before starting your analysis. Use accumulated
knowledge to guide your work:
- DEAD_END entries → skip these areas (already verified safe by prior agents/phases)
- HYPOTHESIS entries → prioritize investigating these suspected issues
- PATTERN entries → understand recurring code idioms before analyzing
- INSIGHT entries → absorb architectural knowledge from context building phase
After completing your analysis, append a memory entry to audit-output/memory-state.md:
  Entry ID: MEM-4C-R1-PERSONA-<YOUR_PERSONA_NAME>
  Type: INSIGHT
  Summary: What your persona methodology uniquely revealed about this codebase
  Key Insights: Patterns and behaviors only visible from your analytical angle
  Hypotheses: Suspected issues for other personas to cross-verify
  Dead Ends: Areas your methodology thoroughly covered and found safe
  Open Questions: Specific questions directed at other personas by name
  Affected Code: Files and line ranges you analyzed in depth

OUTPUT: Write your complete analysis to:
  audit-output/personas/round-1/[persona-name].md

Use your full output format as specified in your agent file.
SELF-VALIDATE before writing: re-read every finding and confirm the code reference
is correct and the root cause is specific (not generic).
```

| Sub-Agent | Agent Name | Output File |
|-----------|------------|-------------|
| BFS | `persona-bfs` | `audit-output/personas/round-1/bfs.md` |
| DFS | `persona-dfs` | `audit-output/personas/round-1/dfs.md` |
| Working Backward | `persona-working-backward` | `audit-output/personas/round-1/backward.md` |
| State Machine | `persona-state-machine` | `audit-output/personas/round-1/state-machine.md` |
| Mirror | `persona-mirror` | `audit-output/personas/round-1/mirror.md` |
| Re-Implementation | `persona-reimplementer` | `audit-output/personas/round-1/reimpl.md` |

> **IMPORTANT**: Spawn all 6 in parallel. Do NOT wait for one to complete before spawning the next.

### Collect Results

After all 6 complete:
1. Read all 6 output documents
2. Count findings per persona
3. Collect all "Open Questions for Other Personas" into a single list
4. **Read all `MEM-4C-R1-PERSONA-*` memory entries** and synthesize into consolidation entry

#### Memory Consolidation: Post-Round 1

After collecting Round 1 results, write a consolidation entry to `audit-output/memory-state.md`:

```markdown
### MEM-4C-R1-CONSOLIDATION: Round 1 cross-persona synthesis
- **Agent**: multi-persona-orchestrator (self)
- **Phase**: 4C — Round 1 consolidation
- **Type**: INSIGHT

#### Summary
<6 personas completed. N total findings. M unique code locations. Key agreements and disagreements.>

#### Cross-Persona Agreements (high confidence)
- <Finding/observation confirmed by 2+ personas — elevated confidence>

#### Contradictions
- <Persona A says X; Persona B says Y about the same code — needs Round 2 resolution>

#### Promoted Hypotheses
- <Hypothesis raised by 2+ personas independently → HIGH PRIORITY for Round 2>

#### Coverage Map
- Code with deep coverage (3+ personas): <files>
- Code with shallow coverage (1 persona): <files>
- Code with ZERO coverage: <files> → priority targets for Round 2

#### Accumulated Dead Ends
- <Areas where multiple personas found nothing — safe to deprioritize>
```

Feed this consolidation into the shared knowledge document (Phase 2) and into Round 2 spawn prompts.

### Quality Gate 1: Round 1 Validation

Before proceeding to Phase 2, validate:

```
QG-1 Checks:
- [ ] All 6 persona outputs exist and are non-empty
- [ ] Each persona followed its designated methodology (not generic scanning)
- [ ] Total unique code locations referenced across all personas > 0
- [ ] No persona output is a copy of another persona's output
```

**If any persona returned empty**: Retry that persona with a reduced scope (half the files, focusing on highest-value contracts). If still empty after retry, continue with 5 personas and redistribute that persona's focus areas via cross-pollination seeds.

**If total findings across all personas = 0 AND codebase > 200 LoC**: This is suspicious. Verify the codebase path is correct and that source files (not just configs/tests) are in scope. If confirmed correct, proceed — Round 2 cross-pollination often reveals what Round 1 missed.

---

## Phase 2: Knowledge Sharing & Cross-Pollination

**Agent**: Self

### Step 1: Build Shared Knowledge Document

Create `audit-output/personas/shared-knowledge-round-1.md`:

```markdown
# Shared Knowledge — After Round 1

## Findings Summary
| Persona | Findings Count | Key Discoveries |
|---------|---------------|-----------------|
| BFS | [N] | [one-line summary of top findings] |
| DFS | [N] | ... |
| Working Backward | [N] | ... |
| State Machine | [N] | ... |
| Mirror | [N] | ... |
| Re-Implementation | [N] | ... |

## Open Questions (Cross-Persona)
### From BFS:
- [question] → best answered by: [persona]
### From DFS:
- [question] → best answered by: [persona]
(... all personas)

## Overlap Analysis
### Findings confirmed by multiple personas:
- [finding] — found by: [persona A, persona B]
  Confidence: ELEVATED (multi-persona agreement)

### Unique findings (single persona only):
- [finding] — found by: [persona A] only
  Action: Other personas should verify in Round 2

## Cross-Pollination Seeds
(Extracted insights that should change how other personas look at the code)
- BFS found entry point X has no access control → Working Backward should trace taint through X
- DFS found library Y rounds down → Mirror should check if both deposit/withdraw use Y
- Working Backward found sink Z is reachable → BFS should check all paths to Z
- State Machine found illegal path through function W → Re-Implementation should diff W
- Mirror found asymmetry in pair P → State Machine should check if asymmetric transition leads to bad state
- Re-Implementation found missing guard G → DFS should check if G exists at leaf level

## Memory State Enrichment
(Extracted from MEM-4C-R1-CONSOLIDATION and per-persona memory entries)
### Dead Ends (do NOT re-investigate in Round 2):
- <aggregated from all persona memory entries — code areas verified safe by multiple personas>
### High Priority Hypotheses (investigate in Round 2):
- <hypotheses raised by 2+ personas independently>
### Contradictions to Resolve:
- <persona A and persona B disagree on X — both should investigate in Round 2>
### Coverage Gaps to Fill:
- <code areas with zero or single-persona coverage — distribute to appropriate personas>
```

---

## Phase 3: Iterative Rounds (Round 2..N)

**Agent**: Spawns 6 sub-agents IN PARALLEL (per round)

### For Each Round (2, 3, ... up to max):

#### Step 1: Spawn All 6 Personas Again

```
You are a [PERSONA_NAME] security auditor.

Read your full methodology and instructions from:
  .claude/agents/[persona-agent-file].md

Read the Feynman Question Framework from:
  resources/feynman-question-framework.md

TARGET CODEBASE: <codebase-path>
CONTEXT: <contents of 00-scope.md or 01-context.md>
ROUND: [N]

SHARED KNOWLEDGE FROM PREVIOUS ROUNDS:
<contents of shared-knowledge-round-[N-1].md>

YOUR PREVIOUS ROUND OUTPUT:
<contents of round-[N-1]/[persona-name].md>

INSTRUCTIONS FOR THIS ROUND:
1. Read ALL other personas' documents from the previous round.
2. Answer any Open Questions directed at your persona.
3. Incorporate shared knowledge — update your analysis where other personas
   found things that change your understanding.
4. Go DEEPER on findings from your previous round — add evidence, trace further.
5. Explore NEW areas suggested by cross-pollination seeds.
6. Apply Feynman questioning to any code you haven't examined yet.
7. Mark findings as NEW (this round) or CARRIED (from previous round, refined).
8. SELF-VALIDATE: Before writing output, re-check every finding's code reference
   and root cause. Remove or downgrade findings you can no longer support.

★ MEMORY STATE:
Read audit-output/memory-state.md — it now contains accumulated knowledge from ALL
prior rounds plus consolidation entries. Pay special attention to:
- MEM-4C-R[N-1]-CONSOLIDATION → contradictions you should resolve, coverage gaps to fill
- MEM-4C-R[N-1]-PERSONA-<others> → other personas' insights that change your understanding
- Promoted hypotheses → investigate these with HIGH PRIORITY
After completing, append your memory entry:
  Entry ID: MEM-4C-R[N]-PERSONA-<YOUR_PERSONA_NAME>
  Type: INSIGHT
  Summary: What changed from your previous round, new discoveries, resolved questions
  Key Insights: Round-over-round delta (what you learned that you didn't know before)
  Hypotheses: Refined or new suspected issues
  Dead Ends: Additional safe areas verified (incremental to prior round)
  Open Questions: Remaining unanswered questions for other personas

OUTPUT: Write to audit-output/personas/round-[N]/[persona-name].md
Include a "Code Coverage" line: X of Y in-scope files examined.
```

#### Step 2: Collect & Evaluate Convergence

After all 6 complete, compute a quantitative convergence score:

```
CONVERGENCE SCORING (compute after each round):

Inputs:
  new_findings    = count of NEW findings across all 6 personas this round
  carried_refined = count of CARRIED findings that were meaningfully refined
  questions_open  = count of unanswered cross-persona questions
  questions_total = total questions asked this round + carryover
  code_coverage   = unique files referenced / total files in scope

Formula:
  novelty_rate    = new_findings / max(1, new_findings + carried_refined)
  question_rate   = questions_open / max(1, questions_total)
  convergence     = (1 - novelty_rate) * 0.5 + (1 - question_rate) * 0.3 + code_coverage * 0.2

Decision:
  convergence ≥ 0.8                        → CONVERGED — proceed to Phase 4
  convergence < 0.8 AND round < max_rounds → continue to next round
  round == max_rounds                      → FORCED convergence — proceed to Phase 4
                                              Flag all POSSIBLE findings for manual review
```

Log the convergence score in `audit-output/personas/shared-knowledge-round-[N].md`.

#### Memory Consolidation: Post-Round N

After computing convergence, write a round consolidation entry to `audit-output/memory-state.md`:

```markdown
### MEM-4C-R<N>-CONSOLIDATION: Round <N> cross-persona synthesis
- **Agent**: multi-persona-orchestrator (self)
- **Phase**: 4C — Round <N> consolidation
- **Type**: INSIGHT

#### Summary
Round <N>: <new_findings> new, <carried_refined> refined. Convergence: <score>.
<Key delta from previous round.>

#### New Cross-Persona Agreements
- <Finding/observation newly confirmed by 2+ personas this round>

#### Resolved Contradictions
- <Contradiction from prior round — now resolved: <resolution>>

#### New Contradictions
- <New disagreements surfaced this round>

#### Coverage Delta
- New code areas analyzed: <files>
- Remaining gaps: <files>

#### Accumulated Dead Ends (cumulative)
- <All safe areas from all rounds — prevents future re-investigation>
```

Feed this into the next round's shared knowledge document or into Phase 4 cross-verification.

### Quality Gate 2: Pre-Verification Validation

Before moving to Phase 4, validate all findings:

```
QG-2 Checks:
- [ ] Every finding has an exact code reference (file:line)
- [ ] Every finding has a root cause (not just a symptom description)
- [ ] Every finding has a severity estimate with justification
- [ ] No two findings share the same root cause (pre-deduplicate)
- [ ] CRITICAL/HIGH findings have concrete attack scenarios
```

Findings that fail QG-2 are downgraded to POSSIBLE regardless of persona agreement.

---

## Phase 4: Cross-Verification Vote

**Agent**: Self (reads all persona outputs from final round)

### Step 1: Collect All Candidate Findings

From every persona across all rounds, extract every finding into a unified list:

```markdown
| ID | Source Persona | Round Found | Title | Severity Estimate | Confirmed By |
|----|---------------|-------------|-------|-------------------|--------------|
| F-001 | DFS | R1 | mulDiv overflow when reserve=0 | HIGH | BFS(R2), Working Backward(R2) |
| F-002 | Mirror | R1 | withdraw missing reentrancy guard | HIGH | Re-Impl(R1), DFS(R2) |
| F-003 | Working Backward | R2 | oracle taint reaches liquidation sink | MEDIUM | State Machine(R2) |
```

### Step 2: Confidence Scoring

For each finding, calculate confidence based on multi-persona agreement:

| Confirmation Level | Confidence | Action |
|--------------------|------------|--------|
| Found by 3+ personas | **CONFIRMED** | Include with HIGH confidence |
| Found by 2 personas | **LIKELY** | Include with MEDIUM confidence |
| Found by 1 persona, no contradictions | **POSSIBLE** | Include with LOW confidence, flag for manual review |
| Found by 1 persona, contradicted by another | **DISPUTED** | Include both perspectives, mark as DISPUTED |

### Step 3: Deduplication

Multiple personas may find the same root cause through different paths. Apply this algorithm:

```
DEDUPLICATION ALGORITHM:

1. GROUP by affected code location (file:line range, within 10 lines = same location)
2. Within each group, CLUSTER by root cause:
   - Same root cause, different symptoms → MERGE into one finding
   - Same location, different root causes → KEEP as separate findings
3. For each merged finding:
   - Keep the CLEAREST root cause explanation (prioritize: DFS > Re-Impl > others for precision)
   - Keep ALL supporting evidence from every persona that found it
   - Use the HIGHEST severity estimate with justification
   - Merge attack scenarios into the most complete version
4. Assign canonical ID: F-NNN ordered by severity (CRITICAL first)
```

Common deduplication pitfalls:
- **Same symptom, different root cause**: rounding error (Mirror) vs. precision loss chain (DFS) → keep BOTH
- **Same root cause, different locations**: missing reentrancy guard in deposit AND withdraw → ONE finding, two affected locations
- **Subset findings**: "oracle stale" (Working Backward) is a subset of "oracle manipulation enables liquidation" (State Machine) → keep the MORE COMPLETE finding

### Step 4: Cross-Verification Spawn

For any POSSIBLE or DISPUTED findings, spawn a **verification sub-agent**:

```
You are a cross-verification auditor.

FINDING TO VERIFY:
[finding details from the candidate list]

SUPPORTING EVIDENCE (from persona [X]):
[their analysis]

CONTRADICTING EVIDENCE (from persona [Y], if disputed):
[their counter-analysis]

TARGET CODE:
[the specific code section]

YOUR TASK:
1. Read the actual code carefully.
2. Evaluate both perspectives.
3. Determine: CONFIRMED, FALSE POSITIVE, or NEEDS MORE CONTEXT
4. If CONFIRMED: provide the definitive root cause and impact.
5. If FALSE POSITIVE: explain why the finding is invalid.
```

---

## Phase 5: Unified Findings Assembly

**Agent**: Self

### Step 1: Write the Final Findings Document

Create `audit-output/persona-findings.md`:

```markdown
# Multi-Persona Audit Findings

## Metadata
- **Codebase**: [name/path]
- **Protocol Type**: [detected]
- **Rounds Completed**: [N]
- **Convergence**: [NATURAL at round N / FORCED at max rounds]
- **Personas**: BFS, DFS, Working Backward, State Machine, Mirror, Re-Implementation

## Summary
| Severity | Count |
|----------|-------|
| CRITICAL | [N] |
| HIGH | [N] |
| MEDIUM | [N] |
| LOW | [N] |
| Informational | [N] |

## Findings

### [F-001] [Title]

**Severity**: [CRITICAL/HIGH/MEDIUM/LOW]
**Confidence**: [CONFIRMED/LIKELY/POSSIBLE/DISPUTED]
**Discovered by**: [persona(s)] in Round [N]
**Confirmed by**: [persona(s)] in Round [N]

**Root Cause**:
[Clear explanation of WHY this is vulnerable]

**Affected Code**:
```
[exact code snippet with file:line reference]
```

**Attack Scenario**:
1. Attacker does X
2. This causes Y
3. Resulting in Z (impact: [loss amount / privilege gained / state corrupted])

**Evidence from Multiple Personas**:
- **[Persona A]**: [their perspective/evidence]
- **[Persona B]**: [their perspective/evidence]

**Recommended Fix**:
```
[fix code]
```

---

(repeat for each finding, ordered by severity)

## Appendix: Persona Convergence Log
| Round | New Findings | Questions Answered | Convergence Score |
|-------|-------------|-------------------|-------------------|
| 1 | [N] | 0 (first round) | LOW |
| 2 | [N] | [N] | MEDIUM |
| ... | ... | ... | ... |

## Appendix: Cross-Persona Agreement Matrix
| Finding | BFS | DFS | Backward | StateMachine | Mirror | Re-Impl |
|---------|-----|-----|----------|------------|--------|---------|
| F-001 | - | FOUND | CONFIRMED | - | - | CONFIRMED |
| F-002 | CONFIRMED | - | - | FOUND | FOUND | - |
```

### Step 2: Copy Persona Documents to Archive

```bash
# Archive all round documents for reference
cp -r audit-output/personas/ audit-output/personas-archive/
```

### Final Quality Gate: Output Validation

Before delivering `persona-findings.md`, validate:

```
FINAL GATE Checks:
- [ ] Every CRITICAL/HIGH finding has a concrete attack scenario with specific parameters
- [ ] Every finding's code reference is valid (file exists, line range contains relevant code)
- [ ] No duplicate root causes remain after deduplication
- [ ] Confidence scores are consistent with persona agreement levels
- [ ] The Cross-Persona Agreement Matrix is complete (every finding × every persona)
- [ ] Convergence log shows the progression across rounds
- [ ] Summary severity counts match actual finding counts
```

If any check fails, fix before delivering. This is the feedback loop — validate, fix, re-validate.

---

## Feynman Technique Integration

Every persona sub-agent MUST apply the Feynman technique throughout their analysis. The core loop per code section is:

```
FEYNMAN LOOP:
1. EXPLAIN: Can you explain what this code does in simple terms?
   → If NO: you don't understand it yet. Read more context.
   → If YES: proceed.

2. QUESTION: Apply category-specific Feynman questions:
   - Q1 (Purpose): WHY does this exist?
   - Q2 (Ordering): What if I MOVE this?
   - Q3 (Consistency): WHY does A have it but B doesn't?
   - Q4 (Assumptions): What is IMPLICITLY TRUSTED?
   - Q5 (Boundaries): What happens at the EDGES?
   - Q6 (Returns): What happens on ERROR?
   - Q7 (Sequences): What about MULTI-TRANSACTION scenarios?

3. CHALLENGE: For each answer, ask "But what if that's WRONG?"
   → If assumption can be violated → potential finding.
   → If assumption cannot be violated → move on.

4. SHARE: Document insights and unanswered questions for other personas.
```

Reference: [feynman-question-framework.md](resources/feynman-question-framework.md) for the full question catalog.

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Sub-agent returns empty output | Retry once with smaller scope (half the files). If still empty, log and continue with 5 personas. |
| Sub-agent times out | Reduce scope, increase round count. Distribute its files to other personas. |
| All personas find 0 findings after Round 1 | Verify codebase path is correct. If confirmed, persona outputs still provide valuable context — proceed with Round 2 cross-pollination. |
| Two personas directly contradict | Spawn cross-verification agent (Phase 4 Step 4). Both perspectives go into the finding. |
| Convergence not reached at max rounds | Force-converge. POSSIBLE/DISPUTED findings get flagged for manual review. |

---

## Context Budget Guidelines

| Component | Budget |
|-----------|--------|
| Scope document (per persona) | ~2K tokens |
| Shared knowledge doc (per round) | ~5K tokens |
| Previous round output (per persona) | ~8K tokens |
| Target code (per persona) | Remaining budget |

### Large Codebase Strategy

If codebase exceeds single-persona context limits (total source > ~150K tokens):

```
STRATEGY: Domain-Affinity Partitioning

1. PARTITION source files by functional domain:
   - Core protocol logic (vaults, pools, markets)
   - Token/accounting contracts
   - Oracle/price feed integrations
   - Access control / governance
   - Periphery (routers, helpers, views)

2. ASSIGN primary domains to personas by affinity:
   - BFS: Gets ALL files (reads headers/signatures only in Layer 0)
   - DFS: Gets math libraries + core logic (deepest dependencies)
   - Working Backward: Gets value-transfer contracts + oracle integrations
   - State Machine: Gets core logic + governance (state-heavy contracts)
   - Mirror: Gets paired contracts (vault+token, deposit+withdraw modules)
   - Re-Implementation: Gets highest-value contracts (by TVL flow)

3. Each persona gets FULL text of their primary files + SIGNATURES ONLY of other files
4. Cross-pollination documents bridge the context gaps
5. In Round 2+, personas can REQUEST full text of specific non-primary files
   based on cross-pollination seeds
```

Never skip a persona due to context limits — reduce scope per persona instead.