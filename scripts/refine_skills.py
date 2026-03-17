#!/usr/bin/env python3
"""
Refines all .claude/skills/*/SKILL.md files to follow proper Claude Code skill semantics.

Current problem: Skills are identical copies of agent files (~74-1676 lines each).
Fix: Skills should be thin invocation wrappers that delegate to agents via context: fork.

Per https://code.claude.com/docs/en/skills:
- Skills use YAML frontmatter (name, description, context, agent, argument-hint, etc.)
- Skills with context: fork delegate to .claude/agents/<name>.md
- Skill content becomes the task prompt for the subagent
- Keep SKILL.md under 500 lines
- user-invocable: false for sub-agent-only skills
"""

import os
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent / ".claude" / "skills"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SKILL DEFINITIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SKILLS = {

# ──────────────────────────────────────────────────
# 1. AUDIT ORCHESTRATOR — Main entry point
# ──────────────────────────────────────────────────
"audit-orchestrator": r'''---
name: audit-orchestrator
description: "Run a full end-to-end smart contract security audit. Orchestrates 20+ sub-agents across 11 phases: reconnaissance, context building, invariant extraction, iterative discovery (DB hunting + reasoning + multi-persona + validation gaps), merge & triage, PoC generation, formal verification, judging, issue polishing, deep review, and report assembly. Use when auditing an unfamiliar codebase, running a contest-grade security review, or performing comprehensive vulnerability discovery."
context: fork
agent: audit-orchestrator
argument-hint: <codebase-path> [protocol-hint] [--static-only] [--judge=sherlock|cantina|code4rena] [--discovery-rounds=N]
---

Run a complete security audit on the codebase at `$ARGUMENTS`.

## Pipeline overview

| Phase | What happens |
|-------|-------------|
| 1. Reconnaissance | Protocol detection, scope definition, manifest resolution |
| 2. Context Building | Spawns `audit-context-building` for deep code analysis |
| 3. Invariant Extraction | Spawns `invariant-writer` → `invariant-reviewer` |
| 4. Iterative Discovery | N rounds of 4-way parallel fan-out (DB hunting, reasoning, multi-persona, validation gaps) |
| 5. Merge & Triage | Cross-source correlation, dedup, falsification, severity assignment |
| 6. PoC Generation | Spawns `poc-writing` per CRITICAL/HIGH finding (skip with `--static-only`) |
| 7. Formal Verification | Spawns `medusa-fuzzing`, `certora-verification`, `halmos-verification` (skip with `--static-only`) |
| 8. Pre-Judging | Judge(s) screen all triaged findings |
| 9. Issue Polishing | Spawns `issue-writer` for valid findings |
| 10. Deep Review | Judge(s) do line-by-line verification |
| 11. Report Assembly | Produces `audit-output/CONFIRMED-REPORT.md` |

## Flags

- `--static-only` — Skip Phases 6-7 (no PoC/FV). Findings confirmed through judging only.
- `--judge=X` — Use a single judge instead of all 3. Options: `sherlock`, `cantina`, `code4rena`.
- `--discovery-rounds=N` — Number of iterative discovery rounds (default: 2, max: 5).

## Output

All artifacts go to `audit-output/`:
- `CONFIRMED-REPORT.md` — Final report with only judge-verified findings
- `pipeline-state.md` — Pipeline progress tracker
- `00-scope.md` through `10-deep-review.md` — Phase artifacts

## Related skills

- [/audit-context-building](../audit-context-building/SKILL.md) — Deep codebase analysis (Phase 2)
- [/invariant-writer](../invariant-writer/SKILL.md) — Invariant extraction (Phase 3)
- [/poc-writing](../poc-writing/SKILL.md) — Exploit test generation (Phase 6)
- [/sherlock-judging](../sherlock-judging/SKILL.md) — Sherlock criteria validation (Phase 8/10)
- [/cantina-judge](../cantina-judge/SKILL.md) — Cantina criteria validation (Phase 8/10)
- [/code4rena-judge](../code4rena-judge/SKILL.md) — Code4rena criteria validation (Phase 8/10)
''',

# ──────────────────────────────────────────────────
# 2. AUDIT CONTEXT BUILDING
# ──────────────────────────────────────────────────
"audit-context-building": r'''---
name: audit-context-building
description: "Build deep architectural context for a smart contract codebase before vulnerability hunting. Distributes per-contract analysis across sub-agents, then synthesizes a global context document. Use when preparing for a security audit, architecture review, threat modeling, or when bottom-up codebase comprehension is needed."
context: fork
agent: audit-context-building
argument-hint: <codebase-path>
---

Build deep architectural context for the codebase at `$ARGUMENTS`.

## What this does

1. **Scoping** — Identifies all in-scope contract files, their dependencies, and the protocol type
2. **Per-contract analysis** — Spawns one `function-analyzer` sub-agent per contract for line-by-line micro-analysis
3. **Synthesis** — Spawns `system-synthesizer` to produce a unified `01-context.md` with:
   - System-wide invariants and trust boundaries
   - Cross-contract data flows and call graphs
   - Actor models and privilege hierarchies
   - Storage layout and upgrade patterns

## Output

- `audit-output/context/*.md` — Per-contract analysis files
- `audit-output/01-context.md` — Global context document

## Related skills

- [/function-analyzer](../function-analyzer/SKILL.md) — Per-contract function analysis (spawned internally)
- [/system-synthesizer](../system-synthesizer/SKILL.md) — Global context synthesis (spawned internally)
- [/audit-orchestrator](../audit-orchestrator/SKILL.md) — Parent pipeline that invokes this skill
- [/invariant-writer](../invariant-writer/SKILL.md) — Consumes the context output
''',

# ──────────────────────────────────────────────────
# 3. FUNCTION ANALYZER (sub-agent only)
# ──────────────────────────────────────────────────
"function-analyzer": r'''---
name: function-analyzer
description: "Per-contract ultra-granular function analysis. Performs line-by-line micro-analysis of every non-trivial function in a single contract file. Pure context building — no vulnerability identification. Spawned by audit-context-building."
context: fork
agent: function-analyzer
user-invocable: false
---

Analyze every function in the contract file provided as input. For each non-trivial function, produce:

1. **Signature** — Full function signature with visibility and modifiers
2. **Purpose** — One-line description of what the function does
3. **State reads/writes** — Which storage slots are read and written
4. **External calls** — All cross-contract calls with target and selector
5. **Access control** — Guards, modifiers, role checks
6. **Math operations** — Arithmetic with precision/rounding analysis
7. **Edge cases** — Boundary conditions, zero inputs, max values

Write output to the designated per-contract file in `audit-output/context/`.

## Related skills

- [/audit-context-building](../audit-context-building/SKILL.md) — Parent coordinator that spawns this
- [/system-synthesizer](../system-synthesizer/SKILL.md) — Consumes the output of all function-analyzers
''',

# ──────────────────────────────────────────────────
# 4. SYSTEM SYNTHESIZER (sub-agent only)
# ──────────────────────────────────────────────────
"system-synthesizer": r'''---
name: system-synthesizer
description: "Synthesizes per-contract analysis files into a global context document with system-wide invariants, cross-contract flows, trust boundaries, and actor models. Spawned by audit-context-building after all function-analyzers complete."
context: fork
agent: system-synthesizer
user-invocable: false
---

Read all per-contract context files from `audit-output/context/` and synthesize a compact `01-context.md` containing:

1. **System architecture** — How contracts interact, inheritance hierarchy
2. **Cross-contract data flows** — Token flows, callback patterns, delegate calls
3. **Trust boundaries** — Which contracts trust which, admin vs user paths
4. **Actor model** — All roles (admin, user, keeper, liquidator, etc.) and their capabilities
5. **System-wide invariants** — Properties that must hold across all contracts
6. **Attack surface** — External entry points ranked by risk

## Related skills

- [/audit-context-building](../audit-context-building/SKILL.md) — Parent coordinator that spawns this
- [/function-analyzer](../function-analyzer/SKILL.md) — Produces the per-contract files this skill reads
- [/invariant-writer](../invariant-writer/SKILL.md) — Consumes the synthesized context
''',

# ──────────────────────────────────────────────────
# 5. INVARIANT WRITER
# ──────────────────────────────────────────────────
"invariant-writer": r'''---
name: invariant-writer
description: "Extract and document all system invariants, properties, and constraints from a smart contract codebase. Uses dual-mode analysis: 'What Should Happen' (positive specification from specs/standards) and 'What Must Never Happen' (adversarial multi-call attack sequences). Produces language-agnostic invariants consumed by fuzzing and formal verification tools. Use when preparing invariant suites, writing property specifications, or before fuzzing campaigns."
context: fork
agent: invariant-writer
argument-hint: <codebase-path>
---

Extract all invariants from the codebase at `$ARGUMENTS`.

## What this does

Runs two complementary analysis passes:

### Pass 1: "What Should Happen"
- Reads specs, standards, docs, reference implementations
- Extracts positive properties: conservation laws, ordering guarantees, access control rules

### Pass 2: "What Must Never Happen"
- Adversarial, fear-driven analysis
- Multi-call attack sequences, flash loan scenarios, reentrancy paths
- Identifies properties that, if broken, indicate a vulnerability

## Output

- `audit-output/02-invariants.md` — Structured invariant specification

Each invariant includes: ID, category, property statement, boundary conditions, attack vectors it guards against, and whether it's suitable for fuzzing vs formal verification.

## Related skills

- [/invariant-reviewer](../invariant-reviewer/SKILL.md) — Reviews and hardens the output
- [/audit-context-building](../audit-context-building/SKILL.md) — Produces the context this skill consumes
- [/medusa-fuzzing](../medusa-fuzzing/SKILL.md) — Converts invariants to Medusa harnesses
- [/halmos-verification](../halmos-verification/SKILL.md) — Converts invariants to Halmos tests
- [/certora-verification](../certora-verification/SKILL.md) — Converts invariants to CVL specs
''',

# ──────────────────────────────────────────────────
# 6. INVARIANT REVIEWER
# ──────────────────────────────────────────────────
"invariant-reviewer": r'''---
name: invariant-reviewer
description: "Review and harden invariant specifications produced by invariant-writer. Re-understands the protocol, researches canonical invariants for the protocol type, enforces multi-step attack vector coverage, calibrates bounds, and produces a revised invariant file ready for formal verification. Use after invariant-writer or when invariant quality is suspect."
context: fork
agent: invariant-reviewer
argument-hint: <path-to-invariants-file>
---

Review and harden the invariant specification at `$ARGUMENTS`.

## What this does

1. **Re-understanding** — Reads the protocol independently (does not trust the writer's framing)
2. **Canonical research** — Looks up known invariants for this protocol type from `invariants/` reference files
3. **Gap analysis** — Checks for missing invariant categories: conservation, ordering, access control, timing, cross-contract
4. **Multi-step coverage** — Ensures invariants cover 2-step and 3-step attack sequences, not just single-call
5. **Bound calibration** — Tightens or loosens numerical bounds to avoid over/under-specification
6. **FV readiness** — Reformulates invariants for formal verification tool consumption

## Output

- `audit-output/02-invariants-reviewed.md` — Hardened invariant specification

## Related skills

- [/invariant-writer](../invariant-writer/SKILL.md) — Produces the invariants this skill reviews
- [/medusa-fuzzing](../medusa-fuzzing/SKILL.md) — Consumes reviewed invariants
- [/halmos-verification](../halmos-verification/SKILL.md) — Consumes reviewed invariants
- [/certora-verification](../certora-verification/SKILL.md) — Consumes reviewed invariants
- [/invariant-indexer](../invariant-indexer/SKILL.md) — Provides canonical invariant references
''',

# ──────────────────────────────────────────────────
# 7. INVARIANT CATCHER
# ──────────────────────────────────────────────────
"invariant-catcher": r'''---
name: invariant-catcher
description: "Hunt for known vulnerability patterns in smart contract codebases using the Vulnerability Database (DB/). Language-agnostic. Searches by vulnerability class, extracts detection patterns from DB entries, runs grep/ripgrep against target code, and generates structured findings. Use when performing variant analysis, systematically searching for known vulnerability classes, or doing DB-powered hunting during an audit."
context: fork
agent: invariant-catcher
argument-hint: <codebase-path> [vulnerability-topic]
---

Hunt for vulnerability patterns in the codebase at `$0` for topic `$1`.

## What this does

1. **Load hunt cards** — Reads `DB/manifests/huntcards/all-huntcards.json` for detection patterns
2. **Grep pruning** — Runs each card's `grep` pattern against target code, discards zero-hit cards
3. **Shard partitioning** — Groups surviving cards into shards of 50-80 patterns by category
4. **Per-shard analysis** — For each shard, executes micro-directive `check` steps against matching code
5. **Evidence lookup** — For true/likely positives, reads the full DB entry via `card.ref` + `card.lines`
6. **Findings report** — Produces structured findings with root cause, impact, and code references

## Output

- `audit-output/03-findings-shard-<id>.md` — Per-shard findings

## Related skills

- [/audit-orchestrator](../audit-orchestrator/SKILL.md) — Parent pipeline (Phase 4A)
- [/protocol-reasoning](../protocol-reasoning/SKILL.md) — Complementary reasoning-based discovery (Phase 4B)
- [/multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Complementary persona-based discovery (Phase 4C)
- [/db-quality-monitor](../db-quality-monitor/SKILL.md) — Validates the DB hunt cards this skill depends on
''',

# ──────────────────────────────────────────────────
# 8. INVARIANT INDEXER
# ──────────────────────────────────────────────────
"invariant-indexer": r'''---
name: invariant-indexer
description: "Index canonical invariants from major DeFi protocol repositories, formal verification specs, fuzzing harnesses, and documented properties. Writes structured reference files into invariants/<category>/. Use when building protocol-level invariant reference libraries, studying how top protocols specify formal properties, or bootstrapping invariant suites."
context: fork
agent: invariant-indexer
argument-hint: <protocol-name-or-github-url>
---

Index invariants from `$ARGUMENTS`.

## What this does

1. **Source discovery** — Finds formal specs, fuzzing harnesses, property tests, and documented invariants in the target repository
2. **Extraction** — Pulls out each invariant with its category, property statement, and source reference
3. **Classification** — Tags invariants by type: conservation, ordering, access control, timing, liveness, safety
4. **Deduplication** — Merges equivalent invariants across sources
5. **Output** — Writes structured reference files to `invariants/<category>/`

## Sources it searches

- Certora CVL specs (`*.spec`)
- Echidna/Medusa harnesses (`property_*`, `invariant_*`)
- Halmos symbolic tests (`check_*`)
- Foundry invariant tests
- Scribble annotations
- Documented properties in READMEs and audits

## Related skills

- [/invariant-writer](../invariant-writer/SKILL.md) — Consumes indexed invariants as seed context
- [/invariant-reviewer](../invariant-reviewer/SKILL.md) — Uses indexed invariants for gap analysis
- [/medusa-fuzzing](../medusa-fuzzing/SKILL.md) — Targets protocols whose invariants were indexed
''',

# ──────────────────────────────────────────────────
# 9. PROTOCOL REASONING
# ──────────────────────────────────────────────────
"protocol-reasoning": r'''---
name: protocol-reasoning
description: "Deep reasoning-based vulnerability discovery. Decomposes codebases into domains, spawns specialized sub-agents per domain, and uses DB vulnerability root causes as reasoning seeds. Iterates 4 rounds: standard → cross-domain → edge cases → completeness. Requires reachability proofs. Focuses on MEDIUM/HIGH/CRITICAL severity. Use for reasoning-first vulnerability discovery beyond pattern matching."
context: fork
agent: protocol-reasoning
argument-hint: <codebase-path>
---

Perform deep reasoning-based vulnerability discovery on `$ARGUMENTS`.

## What this does

Unlike pattern-matching (`invariant-catcher`), this skill reasons from first principles about how the protocol can be broken.

### Round 1: Standard analysis
- Decomposes the codebase into domains (e.g., lending, oracle, liquidation)
- Spawns one sub-agent per domain with relevant DB root causes as reasoning seeds

### Round 2: Cross-domain
- Looks for vulnerabilities that span multiple domains (e.g., oracle + liquidation)

### Round 3: Edge cases
- Explores boundary conditions, overflow/underflow, rounding, empty states

### Round 4: Completeness
- Reviews coverage gaps, checks for missed attack vectors

Every finding requires a **reachability proof** — a concrete call chain from a public function to the vulnerable code.

## Output

- `audit-output/04a-reasoning-findings.md`

## Related skills

- [/invariant-catcher](../invariant-catcher/SKILL.md) — Complementary pattern-based hunting
- [/multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Complementary persona-based hunting
- [/missing-validation-reasoning](../missing-validation-reasoning/SKILL.md) — Complementary input validation scanning
- [/audit-orchestrator](../audit-orchestrator/SKILL.md) — Parent pipeline (Phase 4B)
''',

# ──────────────────────────────────────────────────
# 10. MISSING VALIDATION REASONING
# ──────────────────────────────────────────────────
"missing-validation-reasoning": r'''---
name: missing-validation-reasoning
description: "Specialized reasoning-based auditor for input validation and hygiene vulnerabilities. Scans for zero-address checks, stale oracle data, array length mismatches, numeric bounds, arbitrary calldata forwarding, unvalidated token/callback addresses, and access control gaps. Use when reviewing constructors, initialize functions, admin setters, oracle integrations, or batch operations."
context: fork
agent: missing-validation-reasoning
argument-hint: <codebase-path>
---

Scan for missing input validation vulnerabilities in `$ARGUMENTS`.

## What this checks

| Category | Examples |
|----------|----------|
| Zero-address | Missing `address(0)` checks on token/receiver/admin params |
| Stale data | No freshness validation on oracle prices, no heartbeat checks |
| Array mismatches | `arrays.length != otherArrays.length` without require |
| Numeric bounds | Missing min/max checks, uncapped slippage, zero-amount |
| Arbitrary forwarding | Unvalidated calldata in `.call()`, delegate patterns |
| Token validation | Unvalidated token addresses in multi-token systems |
| Access control | Missing modifiers on state-changing functions, constructor gaps |

## Output

- `audit-output/04d-validation-findings.md`

## Related skills

- [/protocol-reasoning](../protocol-reasoning/SKILL.md) — Broader reasoning-based discovery
- [/invariant-catcher](../invariant-catcher/SKILL.md) — Pattern-based hunting
- [/audit-orchestrator](../audit-orchestrator/SKILL.md) — Parent pipeline (Phase 4D)
''',

# ──────────────────────────────────────────────────
# 11. MULTI-PERSONA ORCHESTRATOR
# ──────────────────────────────────────────────────
"multi-persona-orchestrator": r'''---
name: multi-persona-orchestrator
description: "Multi-persona audit orchestrator that spawns 6 parallel auditing personas (BFS, DFS, Working Backward, State Machine, Mirror, Re-Implementation). Agents share findings between rounds, cross-verify, and converge on unified findings. Use when deep-reasoning audit coverage from multiple perspectives is needed."
context: fork
agent: multi-persona-orchestrator
argument-hint: <codebase-path>
---

Run multi-persona audit on `$ARGUMENTS`.

## Personas

| Persona | Strategy | Spawns |
|---------|----------|--------|
| **BFS** | Maps entry points, then progressively deepens | `persona-bfs` |
| **DFS** | Verifies leaf functions, then works upward | `persona-dfs` |
| **Working Backward** | Traces from critical sinks to attacker sources | `persona-working-backward` |
| **State Machine** | Maps all states/transitions, finds illegal paths | `persona-state-machine` |
| **Mirror** | Analyzes paired/opposite functions for asymmetries | `persona-mirror` |
| **Re-Implementation** | Hypothetically re-implements, then diffs | `persona-reimplementer` |

## Process

1. **Round 1** — All 6 personas analyze independently
2. **Knowledge sharing** — Findings aggregated into `shared-knowledge-round-N.md`
3. **Round 2+** — Personas cross-verify, build on each other's findings
4. **Convergence** — Unified findings document with cross-persona validation

## Output

- `audit-output/04c-persona-findings.md`
- `audit-output/personas/round-N/*.md` — Per-persona per-round findings

## Related skills

- [/persona-bfs](../persona-bfs/SKILL.md) — BFS persona (spawned internally)
- [/persona-dfs](../persona-dfs/SKILL.md) — DFS persona (spawned internally)
- [/persona-working-backward](../persona-working-backward/SKILL.md) — Working Backward persona
- [/persona-state-machine](../persona-state-machine/SKILL.md) — State Machine persona
- [/persona-mirror](../persona-mirror/SKILL.md) — Mirror persona
- [/persona-reimplementer](../persona-reimplementer/SKILL.md) — Re-Implementation persona
- [/audit-orchestrator](../audit-orchestrator/SKILL.md) — Parent pipeline (Phase 4C)
''',

# ──────────────────────────────────────────────────
# 12-17. PERSONA SKILLS (sub-agent only)
# ──────────────────────────────────────────────────
"persona-bfs": r'''---
name: persona-bfs
description: "BFS auditing persona — maps entry points then progressively deepens. Language-agnostic. Applies Feynman questioning at every depth layer. Spawned by multi-persona-orchestrator."
context: fork
agent: persona-bfs
user-invocable: false
---

Perform Breadth-First Search audit on the target codebase.

## Strategy

1. **Depth 0** — Enumerate all external/public entry points
2. **Depth 1** — For each entry point, map immediate internal calls and state changes
3. **Depth 2** — Follow internal calls one level deeper, check interaction patterns
4. **Depth N** — Continue until leaf functions reached

At each depth layer, apply Feynman questioning:
- "Can I explain exactly what this function does in simple terms?"
- "What would break if this assumption were wrong?"
- "What's the simplest way an attacker could abuse this?"

## Output format

Write findings to the designated personas output file with: finding ID, severity, root cause, affected functions, and reachability proof.

## Related skills

- [/multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Parent orchestrator
- [/persona-dfs](../persona-dfs/SKILL.md) — Complementary DFS approach
''',

"persona-dfs": r'''---
name: persona-dfs
description: "DFS auditing persona — verifies leaf functions then works upward. Language-agnostic. Applies Feynman questioning at every stack depth. Spawned by multi-persona-orchestrator."
context: fork
agent: persona-dfs
user-invocable: false
---

Perform Depth-First Search audit on the target codebase.

## Strategy

1. **Identify leaf functions** — Functions that make no further internal calls
2. **Verify leaves** — Check each leaf for correctness, edge cases, overflow
3. **Work upward** — Verify callers of verified leaves, checking composition safety
4. **Reach entry points** — Confirm the full stack is sound or find where it breaks

At each stack depth, apply Feynman questioning:
- "If the callee is correct, can the caller still misuse the return value?"
- "Does the caller check all error conditions from the callee?"

## Output format

Write findings to the designated personas output file.

## Related skills

- [/multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Parent orchestrator
- [/persona-bfs](../persona-bfs/SKILL.md) — Complementary BFS approach
''',

"persona-working-backward": r'''---
name: persona-working-backward
description: "Working Backward auditing persona — traces from critical sinks to attacker-controllable sources. Optimized for speedrun/bug-bounty style hunting. Language-agnostic. Spawned by multi-persona-orchestrator."
context: fork
agent: persona-working-backward
user-invocable: false
---

Perform Working Backward audit on the target codebase.

## Strategy

1. **Identify critical sinks** — `transfer`, `selfdestruct`, `delegatecall`, storage writes to balances/ownership
2. **Trace backward** — For each sink, follow the data flow backward to its sources
3. **Find attacker control** — Identify which sources are attacker-controllable (function params, `msg.sender`, `msg.value`)
4. **Verify path** — Check if any guards along the path can be bypassed

## Output format

Write findings to the designated personas output file.

## Related skills

- [/multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Parent orchestrator
- [/persona-state-machine](../persona-state-machine/SKILL.md) — Complementary state analysis
''',

"persona-state-machine": r'''---
name: persona-state-machine
description: "State Machine auditing persona — maps all protocol states, transitions, and cross-contract interactions to find illegal state paths. Specializes in finding unique exploits through exhaustive state-transition analysis. Language-agnostic. Spawned by multi-persona-orchestrator."
context: fork
agent: persona-state-machine
user-invocable: false
---

Perform State Machine audit on the target codebase.

## Strategy

1. **Map states** — Identify all protocol states (stored in state variables, enums, booleans, phases)
2. **Map transitions** — For each state, identify which functions cause transitions and their conditions
3. **Build transition graph** — Draw the complete state machine
4. **Find illegal paths** — Look for:
   - Transitions that skip required intermediate states
   - States that should be unreachable but aren't
   - Circular transitions that drain value
   - Race conditions between transitions

## Output format

Write findings to the designated personas output file.

## Related skills

- [/multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Parent orchestrator
- [/persona-working-backward](../persona-working-backward/SKILL.md) — Complementary backward tracing
''',

"persona-mirror": r'''---
name: persona-mirror
description: "Mirror auditing persona — analyzes paired/opposite functions for asymmetries (deposit/withdraw, mint/burn, stake/unstake, lock/unlock). Language-agnostic. Spawned by multi-persona-orchestrator."
context: fork
agent: persona-mirror
user-invocable: false
---

Perform Mirror audit on the target codebase.

## Strategy

1. **Identify function pairs** — deposit/withdraw, mint/burn, stake/unstake, open/close, lock/unlock, borrow/repay
2. **Compare semantics** — For each pair, check:
   - Do they handle fees symmetrically?
   - Do they update the same state variables in reverse?
   - Do they have matching access control?
   - Do they handle edge cases (zero, max, dust) the same way?
3. **Check roundtrip** — Does `action → reverse_action` return to the exact original state?
4. **Find asymmetries** — Any difference is a potential vulnerability

## Output format

Write findings to the designated personas output file.

## Related skills

- [/multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Parent orchestrator
- [/persona-reimplementer](../persona-reimplementer/SKILL.md) — Complementary re-implementation approach
''',

"persona-reimplementer": r'''---
name: persona-reimplementer
description: "Re-Implementation auditing persona — hypothetically re-implements functions then diffs against actual code. Requires deep protocol intuition. Language-agnostic. Spawned by multi-persona-orchestrator."
context: fork
agent: persona-reimplementer
user-invocable: false
---

Perform Re-Implementation audit on the target codebase.

## Strategy

1. **Read the spec** — Understand what each function SHOULD do from docs, comments, interfaces
2. **Mentally re-implement** — Write pseudocode for what a correct implementation would look like
3. **Diff against actual** — Compare your re-implementation with the actual code
4. **Flag divergences** — Any difference between "what it should do" and "what it does" is a finding candidate

Focus on:
- Missing checks your implementation would include
- Different ordering of operations
- Missing event emissions
- Incorrect math formulas vs specification

## Output format

Write findings to the designated personas output file.

## Related skills

- [/multi-persona-orchestrator](../multi-persona-orchestrator/SKILL.md) — Parent orchestrator
- [/persona-mirror](../persona-mirror/SKILL.md) — Complementary symmetry analysis
''',

# ──────────────────────────────────────────────────
# 18. POC WRITING
# ──────────────────────────────────────────────────
"poc-writing": r'''---
name: poc-writing
description: "Write honest, minimal, compilable exploit tests that prove smart contract vulnerabilities. Adapts to the target codebase's language and test framework (Foundry, Hardhat, Anchor, etc.). Enforces reachability-first methodology. Use when a vulnerability needs a PoC to prove impact, validate an audit finding, or demonstrate to a protocol team."
context: fork
agent: poc-writing
argument-hint: <finding-description-or-file>
---

Write a Proof-of-Concept exploit for `$ARGUMENTS`.

## Methodology

### Phase 0: Reachability Gate (MANDATORY)
Before writing any code, prove the vulnerability is reachable through the public API by an unprivileged user. If not reachable — refuse to write the PoC.

### Phase 1: Understand the vulnerability
Answer: What's the root cause? What's the impact? What preconditions are needed?

### Phase 2: Set up realistic state
Fork mainnet or set up minimal realistic protocol state. Never use phantom interfaces.

### Phase 3: Write exploit
Follow the SNAPSHOT → EXPLOIT → VERIFY pattern:
1. Record state before exploit
2. Execute the attack
3. Assert the exploited state proves the vulnerability

### Phase 4: Compile and run
Fix errors honestly — never mock away security checks to make tests pass.

### Phase 5: Pre-flight checklist
- [ ] No admin/owner roles used by attacker
- [ ] No phantom interfaces or fake contracts
- [ ] Assertions prove actual impact (value lost, state corrupted)
- [ ] Test passes on clean fork

## Related skills

- [/issue-writer](../issue-writer/SKILL.md) — Polishes findings that have PoCs
- [/audit-orchestrator](../audit-orchestrator/SKILL.md) — Parent pipeline (Phase 6)
''',

# ──────────────────────────────────────────────────
# 19. ISSUE WRITER
# ──────────────────────────────────────────────────
"issue-writer": r'''---
name: issue-writer
description: "Polish a validated vulnerability finding into a submission-ready write-up in Sherlock format. Use after triage to convert raw findings into professional audit report entries or contest submissions."
context: fork
agent: issue-writer
argument-hint: <finding-file-or-description>
---

Polish the finding at `$ARGUMENTS` into a submission-ready write-up.

## Output format (Sherlock-style)

```markdown
## [Title] — concise, specific, no filler

### Summary
One paragraph: root cause + impact.

### Root Cause
Specific code reference with line numbers.

### Internal Pre-conditions
Protocol state required (not attacker actions).

### External Pre-conditions
Market/oracle conditions required.

### Attack Path
Numbered steps from attacker's perspective.

### Impact
Quantified loss with concrete numbers.

### PoC
Compilable test or step-by-step reproduction.

### Mitigation
Specific code fix with diff.
```

## Quality checklist

- [ ] Title is specific (not "Reentrancy vulnerability")
- [ ] Root cause points to exact code lines
- [ ] Attack path is step-by-step, not hand-wavy
- [ ] Impact is quantified (not "funds at risk")
- [ ] Mitigation is implementable (not "add a check")

## Related skills

- [/poc-writing](../poc-writing/SKILL.md) — Generates PoCs referenced in the write-up
- [/sherlock-judging](../sherlock-judging/SKILL.md) — Validates the write-up against Sherlock criteria
- [/cantina-judge](../cantina-judge/SKILL.md) — Validates against Cantina criteria
- [/code4rena-judge](../code4rena-judge/SKILL.md) — Validates against Code4rena criteria
''',

# ──────────────────────────────────────────────────
# 20. SHERLOCK JUDGING (inline reference)
# ──────────────────────────────────────────────────
"sherlock-judging": r'''---
name: sherlock-judging
description: "Validate a security finding against Sherlock audit platform standards. Determines severity (High/Medium/Invalid), checks validity, and assesses duplication. Use when validating findings for Sherlock contests, determining Sherlock severity, or checking if an issue meets Sherlock judging criteria."
context: fork
agent: sherlock-judging
argument-hint: <finding-to-validate>
---

Validate the finding at `$ARGUMENTS` against Sherlock judging criteria.

## Severity thresholds

| Severity | Criteria |
|----------|----------|
| **High** | Direct loss of funds >1% of affected party AND >$10. No extensive limitations on scope/conditions. |
| **Medium** | Conditional loss or broken core functionality. Requires specific but reasonable conditions. |
| **Invalid** | Theoretical only, requires admin error, informational, or gas optimization. |

## Key Sherlock rules

- **Likelihood is ignored** — only impact magnitude matters for severity
- **Hierarchy of truth**: README > code > warden interpretation
- **Repeatable small losses** compound — don't dismiss them
- **Admin trust**: Admin actions per docs are trusted; admin-as-attacker is invalid unless contest says otherwise

## Validation checklist

- [ ] Does the finding meet the quantitative loss threshold?
- [ ] Is the attack path reachable without admin/owner?
- [ ] Are preconditions reasonable (not "99 things must align")?
- [ ] Does it break a core protocol invariant or just an edge case?
- [ ] Is it a duplicate of another finding (same root cause)?

For full criteria, see [sherlock-judging-criteria.md](../../resources/sherlock-judging-criteria.md).

## Related skills

- [/cantina-judge](../cantina-judge/SKILL.md) — Cantina criteria (different severity matrix)
- [/code4rena-judge](../code4rena-judge/SKILL.md) — Code4rena criteria
- [/issue-writer](../issue-writer/SKILL.md) — Polishes findings for submission
''',

# ──────────────────────────────────────────────────
# 21. CANTINA JUDGE (inline reference)
# ──────────────────────────────────────────────────
"cantina-judge": r'''---
name: cantina-judge
description: "Validate a security finding against Cantina audit platform standards. Determines severity using impact × likelihood matrix, applies severity caps, and checks for invalid/duplicate categories. Use when validating findings for Cantina submission, determining Cantina severity, or checking if a finding would be capped or invalid."
context: fork
agent: cantina-judge
argument-hint: <finding-to-validate>
---

Validate the finding at `$ARGUMENTS` against Cantina judging criteria.

## Severity matrix: Impact × Likelihood

|  | High Impact | Medium Impact | Low Impact |
|--|-------------|---------------|------------|
| **High Likelihood** | Critical | High | Medium |
| **Medium Likelihood** | High | Medium | Low |
| **Low Likelihood** | Medium | Low | Low |

## Key Cantina rules

- Severity = Impact × Likelihood (both dimensions matter, unlike Sherlock)
- **Severity caps apply** — certain finding types are capped regardless of impact
- **Out-of-scope** findings are invalid even if technically correct
- Duplicates: same root cause = duplicate, even if different impact description

## Validation checklist

- [ ] Impact correctly classified (High/Medium/Low)?
- [ ] Likelihood correctly classified (High/Medium/Low)?
- [ ] Matrix lookup gives correct severity?
- [ ] Any severity caps applicable?
- [ ] Finding is in-scope per contest rules?

For full criteria, see [cantina-criteria.md](../../resources/cantina-criteria.md).

## Related skills

- [/sherlock-judging](../sherlock-judging/SKILL.md) — Sherlock criteria (impact-only severity)
- [/code4rena-judge](../code4rena-judge/SKILL.md) — Code4rena criteria
- [/issue-writer](../issue-writer/SKILL.md) — Polishes findings for submission
''',

# ──────────────────────────────────────────────────
# 22. CODE4RENA JUDGE (inline reference)
# ──────────────────────────────────────────────────
"code4rena-judge": r'''---
name: code4rena-judge
description: "Validate a security finding against Code4rena audit competition standards. Determines severity (High/Medium/QA/Invalid), checks in-scope validity, applies severity caps, and assesses submission quality. Use when validating findings for Code4rena contests, determining C4 severity, or checking if an issue meets C4 judging criteria."
context: fork
agent: code4rena-judge
argument-hint: <finding-to-validate>
---

Validate the finding at `$ARGUMENTS` against Code4rena judging criteria.

## Severity classification

| Severity | Criteria |
|----------|----------|
| **High** | Assets can be stolen/lost directly, or protocol can be rendered inoperable |
| **Medium** | Assets not at direct risk, but function of the protocol or availability could be impacted; or leak value with hypothetical attack path |
| **QA** | Low-risk issues: state handling, input validation, informational |
| **Gas** | Gas optimization only |
| **Invalid** | Out of scope, theoretical, already known, or duplicate |

## Key C4 rules

- **In-scope check** — Only files listed in the contest scope qualify
- **Known issues** — Findings in the known issues list are invalid
- **Bot race** — Automated findings from C4 bots are excluded from manual submissions
- **Severity downgrade** — Wardens can dispute, but judges make final call
- **Duplicates** — Same root cause = duplicate; best report chosen as primary

## Validation checklist

- [ ] Is the finding in the contest scope?
- [ ] Is it already in the known issues list?
- [ ] Does severity match the C4 criteria above?
- [ ] Is the attack path concrete (not theoretical)?
- [ ] Would a warden dispute succeed or fail?

For full criteria, see [code4rena-judging-criteria.md](../../resources/code4rena-judging-criteria.md).

## Related skills

- [/sherlock-judging](../sherlock-judging/SKILL.md) — Sherlock criteria
- [/cantina-judge](../cantina-judge/SKILL.md) — Cantina criteria
- [/issue-writer](../issue-writer/SKILL.md) — Polishes findings for submission
''',

# ──────────────────────────────────────────────────
# 23. MEDUSA FUZZING
# ──────────────────────────────────────────────────
"medusa-fuzzing": r'''---
name: medusa-fuzzing
description: "Convert invariant specifications into compilable Medusa-compatible Solidity test harnesses and medusa.json configuration. Produces property tests (property_ prefix), assertion tests, ghost variable tracking, actor proxies, and bounding utilities. Use when setting up a Medusa fuzzing campaign or converting invariant specs to harness code."
context: fork
agent: medusa-fuzzing
argument-hint: <path-to-invariants-file>
---

Generate Medusa fuzzing harnesses from invariants at `$ARGUMENTS`.

## What this produces

1. **Property tests** — `property_*` functions that return `bool` for stateless invariant checks
2. **Assertion tests** — Functions with `assert()` for stateful multi-step scenarios
3. **Ghost variables** — Tracking variables for cumulative properties (total deposited, total withdrawn)
4. **Actor proxies** — Multi-user simulation with `ActorProxy` pattern
5. **Bounding utilities** — `clampBetween()`, `clampLte()` for input constraining
6. **medusa.json** — Fuzzing configuration with corpus, coverage, and timeout settings

## Compile-first workflow

All harnesses are validated with `forge build` before being considered complete. If compilation fails, the agent fixes the errors iteratively.

## Output

- `test/fuzzing/` — Harness contracts
- `medusa.json` — Fuzzing configuration

For Medusa API reference, see [medusa-reference.md](../../resources/medusa-reference.md).
For templates, see [medusa-templates.md](../../resources/medusa-templates.md).

## Related skills

- [/invariant-writer](../invariant-writer/SKILL.md) — Produces the invariant specs this consumes
- [/invariant-reviewer](../invariant-reviewer/SKILL.md) — Hardens invariants before conversion
- [/halmos-verification](../halmos-verification/SKILL.md) — Alternative: symbolic testing
- [/certora-verification](../certora-verification/SKILL.md) — Alternative: formal verification
''',

# ──────────────────────────────────────────────────
# 24. HALMOS VERIFICATION
# ──────────────────────────────────────────────────
"halmos-verification": r'''---
name: halmos-verification
description: "Convert invariant specifications into compilable Halmos symbolic test suites (.t.sol) that run inside Foundry. Produces check_ prefix functions using halmos-cheatcodes (svm.createUint256, svm.createAddress) for exhaustive verification over all possible inputs. Use when setting up Halmos formal verification or converting invariant specs to symbolic tests."
context: fork
agent: halmos-verification
argument-hint: <path-to-invariants-file>
---

Generate Halmos symbolic tests from invariants at `$ARGUMENTS`.

## What this produces

1. **Symbolic test functions** — `check_*` prefix functions with `svm.create*` symbolic inputs
2. **Multi-path coverage** — Tests that explore all branches exhaustively
3. **Cross-function composition** — Tests that combine multiple function calls symbolically
4. **Arithmetic safety** — Overflow/underflow checks with symbolic bounds
5. **Access control verification** — Symbolic sender with role checks
6. **State machine tests** — Symbolic state transitions

## Key patterns

```solidity
function check_invariant_name() public {
    uint256 amount = svm.createUint256("amount");
    address user = svm.createAddress("user");
    // ... setup and action ...
    assert(/* invariant holds */);
}
```

## Compile-first workflow

All tests validated with `forge build` then `halmos --function check_*`.

## Output

- `test/halmos/` — Symbolic test contracts

## Related skills

- [/invariant-writer](../invariant-writer/SKILL.md) — Produces the invariant specs this consumes
- [/medusa-fuzzing](../medusa-fuzzing/SKILL.md) — Alternative: property-based fuzzing
- [/certora-verification](../certora-verification/SKILL.md) — Alternative: CVL formal verification
''',

# ──────────────────────────────────────────────────
# 25. CERTORA VERIFICATION
# ──────────────────────────────────────────────────
"certora-verification": r'''---
name: certora-verification
description: "Convert invariant specifications into Certora CVL .spec and .conf files. Handles compilation, Python environment, and configuration issues proactively. Produces general specifications, handles admin conditions correctly, avoids vacuous rules, supports mutation testing via Gambit, and generates satisfy statements. Use when setting up Certora formal verification or converting invariant specs to CVL."
context: fork
agent: certora-verification
argument-hint: <path-to-invariants-file>
---

Generate Certora CVL specs from invariants at `$ARGUMENTS`.

## What this produces

1. **CVL spec files** (`.spec`) — Rules, invariants, ghosts, hooks, and functions
2. **Configuration files** (`.conf`) — Certora Prover settings, contract linking, solc paths
3. **Satisfy statements** — For every rule, to detect vacuity
4. **Gambit config** — Mutation testing configuration (optional)

## Key CVL patterns

```cvl
rule transferPreservesTotalSupply(address from, address to, uint256 amount) {
    uint256 totalBefore = totalSupply();
    transfer(from, to, amount);
    uint256 totalAfter = totalSupply();
    assert totalBefore == totalAfter;
}
```

## Compile-first workflow

Runs `certoraRun` to validate specs. Fixes compilation errors iteratively.

## Output

- `certora/specs/` — CVL specification files
- `certora/conf/` — Configuration files

For CVL reference, see [certora-reference.md](../../resources/certora-reference.md).
For templates, see [certora-templates.md](../../resources/certora-templates.md).

## Related skills

- [/invariant-writer](../invariant-writer/SKILL.md) — Produces the invariant specs this consumes
- [/medusa-fuzzing](../medusa-fuzzing/SKILL.md) — Alternative: property-based fuzzing
- [/halmos-verification](../halmos-verification/SKILL.md) — Alternative: symbolic testing
- [/certora-sui-move-verification](../certora-sui-move-verification/SKILL.md) — Certora for Sui Move
''',

# ──────────────────────────────────────────────────
# 26. CERTORA SUI MOVE VERIFICATION
# ──────────────────────────────────────────────────
"certora-sui-move-verification": r'''---
name: certora-sui-move-verification
description: "Convert invariant specifications into Certora Sui Prover Move specs using the CVLM library. Handles installation, Sui CLI setup, Move.toml configuration, and platform summaries. Produces Move-based specification modules. Use when setting up Certora formal verification for Sui Move contracts."
context: fork
agent: certora-sui-move-verification
argument-hint: <path-to-sui-move-project>
---

Generate Certora CVLM specs for the Sui Move project at `$ARGUMENTS`.

## What this produces

1. **CVLM spec modules** — Move modules with `#[spec]` annotations using the CVLM library
2. **Rules** — Verification rules using MathInt arithmetic
3. **Ghosts and shadows** — State tracking across function calls
4. **Parametric rules** — Rules that verify properties across all entry points
5. **Platform summaries** — Summaries for Sui framework functions
6. **Move.toml updates** — Dependency configuration for the CVLM library

## Output

- `spec/` package in the target project

For CVLM reference, see [certora-sui-move-reference.md](../../resources/certora-sui-move-reference.md).
For templates, see [certora-sui-move-templates.md](../../resources/certora-sui-move-templates.md).

## Related skills

- [/certora-verification](../certora-verification/SKILL.md) — Certora for Solidity (CVL)
- [/sui-prover-verification](../sui-prover-verification/SKILL.md) — Alternative Sui prover
- [/invariant-writer](../invariant-writer/SKILL.md) — Produces invariant specs
''',

# ──────────────────────────────────────────────────
# 27. SUI PROVER VERIFICATION
# ──────────────────────────────────────────────────
"sui-prover-verification": r'''---
name: sui-prover-verification
description: "Convert invariant specifications into Sui Prover formal verification specs for Sui Move contracts. Uses the Asymptotic Sui Prover via requires/ensures/asserts specification style. Produces Move specification modules with ghost variables, loop invariants, and Integer/Real math. Use when setting up Sui Prover for Sui Move verification."
context: fork
agent: sui-prover-verification
argument-hint: <path-to-sui-move-project>
---

Generate Sui Prover specs for the Sui Move project at `$ARGUMENTS`.

## What this produces

1. **Spec modules** — Move modules with `#[spec(prove)]` functions
2. **Ghost variables** — `#[spec(global)]` ghost state for tracking
3. **Pre/post conditions** — `requires` and `ensures` annotations
4. **Loop invariants** — `#[spec(loop_invariant)]` for loop verification
5. **Datatype invariants** — Structural properties on Move objects
6. **Integer/Real math** — Precise arithmetic using `Integer` and `Real` types

## Output

- `spec/` package in the target project

For Sui Prover reference, see [sui-prover-reference.md](../../resources/sui-prover-reference.md).

## Related skills

- [/certora-sui-move-verification](../certora-sui-move-verification/SKILL.md) — Alternative: Certora CVLM
- [/invariant-writer](../invariant-writer/SKILL.md) — Produces invariant specs
''',

# ──────────────────────────────────────────────────
# 28. SOLODIT FETCHING
# ──────────────────────────────────────────────────
"solodit-fetching": r'''---
name: solodit-fetching
description: "Fetch vulnerability reports from the Solodit/Cyfrin API for a given topic and store them in reports/<topic>/. Use when collecting raw audit findings for a new vulnerability topic, populating the reports/ directory, or preparing input for variant-template-writer."
context: fork
agent: solodit-fetching
argument-hint: <topic>
---

Fetch vulnerability reports for topic `$ARGUMENTS`.

## Workflow

1. Activate virtual environment: `source .venv/bin/activate`
2. Fetch primary topic: `python3 solodit_fetcher.py --keyword "$ARGUMENTS" --output ./reports/${ARGUMENTS}_findings`
3. Fetch related protocols (e.g., Chainlink → any protocol using Chainlink oracles)
4. Deduplicate results
5. Verify output in `reports/${ARGUMENTS}_findings/`

## Rules

- Always activate venv first
- Always use `python3`
- Never apply quality filters (no `--quality` flag)
- Never add duplicate findings
- Always search related protocols that use the target feature

## Output

- `reports/<topic>_findings/` — Fetched vulnerability reports

## Related skills

- [/variant-template-writer](../variant-template-writer/SKILL.md) — Consumes fetched reports to create DB entries
- [/invariant-catcher](../invariant-catcher/SKILL.md) — Uses DB entries for vulnerability hunting
''',

# ──────────────────────────────────────────────────
# 29. VARIANT TEMPLATE WRITER
# ──────────────────────────────────────────────────
"variant-template-writer": r'''---
name: variant-template-writer
description: "Analyze security audit reports from reports/<topic>/ to identify cross-report vulnerability patterns and create TEMPLATE.md-compliant database entries optimized for vector search. Synthesizes 5-10+ reports per pattern. Use when synthesizing audit findings into DB entries, performing variant analysis, or creating vulnerability templates."
context: fork
agent: variant-template-writer
argument-hint: <topic>
---

Create DB entries from reports in `reports/$ARGUMENTS/`.

## What this does

1. **Read reports** — Loads all findings from `reports/$ARGUMENTS/`
2. **Pattern clustering** — Groups findings by root cause across auditors
3. **Severity consensus** — Determines severity from cross-auditor agreement
4. **Template generation** — Creates TEMPLATE.md-compliant entries with:
   - Frontmatter (title, severity, keywords, category)
   - Description and root cause analysis
   - Detection patterns (grep, code keywords)
   - Vulnerable and secure code examples
   - Real-world references from the source reports
5. **Vector search optimization** — Ensures entries are discoverable by hunt cards

## Output

- `DB/<category>/<subcategory>/<ENTRY_NAME>.md` — New vulnerability entries

After creating entries, run `python3 generate_manifests.py` to update manifests and hunt cards.

## Related skills

- [/solodit-fetching](../solodit-fetching/SKILL.md) — Fetches the reports this skill consumes
- [/db-quality-monitor](../db-quality-monitor/SKILL.md) — Validates the entries this skill creates
''',

# ──────────────────────────────────────────────────
# 30. DB QUALITY MONITOR
# ──────────────────────────────────────────────────
"db-quality-monitor": r'''---
name: db-quality-monitor
description: "Monitor and fix the Vulnerability Database pipeline: 4-tier architecture integrity, manifest generation, hunt card alignment, TEMPLATE.md compliance, line-range accuracy, protocolContext routing, keyword index fidelity, and duplicate detection. Use for periodic DB health checks, CI validation after entry changes, or diagnosing why an audit agent received wrong context."
context: fork
agent: db-quality-monitor
argument-hint: "[--fix] [--check=manifests|huntcards|entries|all]"
disable-model-invocation: true
---

Run quality checks on the Vulnerability Database. $ARGUMENTS

## What this checks

| Check | What it validates |
|-------|-------------------|
| **4-tier integrity** | index.json → manifests → hunt cards → .md entries all link correctly |
| **Line ranges** | Manifest `lineStart`/`lineEnd` match actual content in .md files |
| **Hunt card alignment** | Every manifest pattern has a matching hunt card |
| **TEMPLATE.md compliance** | Entries follow required frontmatter and section structure |
| **Keyword index** | `keywords.json` covers all codeKeywords from manifests |
| **protocolContext routing** | Protocol types map to correct manifests |
| **Duplicate detection** | No two entries have the same root cause |
| **Script health** | `generate_manifests.py` runs without errors |

## Auto-fix mode

With `--fix`, spawns sub-agents to:
- Regenerate manifests from source .md files
- Patch frontmatter in non-compliant entries
- Update line ranges in manifests
- Remove duplicate entries

## Related skills

- [/variant-template-writer](../variant-template-writer/SKILL.md) — Creates entries this skill validates
- [/audit-orchestrator](../audit-orchestrator/SKILL.md) — Pipeline that depends on DB quality
- [/invariant-catcher](../invariant-catcher/SKILL.md) — Consumer of hunt cards this skill validates
''',

}

def write_skill(name: str, content: str):
    """Write a SKILL.md file for the given skill name."""
    skill_dir = SKILLS_DIR / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"
    # Strip leading/trailing whitespace but keep the content
    content = content.strip() + "\n"
    skill_file.write_text(content)
    lines = content.count("\n")
    print(f"  ✓ {name}/SKILL.md ({lines} lines)")

def main():
    print(f"Refining {len(SKILLS)} skills in {SKILLS_DIR}\n")
    
    for name, content in SKILLS.items():
        write_skill(name, content)
    
    print(f"\nDone! Refined {len(SKILLS)} skills.")
    print("\nVerifying line counts (should all be under 500):")
    for name in sorted(SKILLS.keys()):
        path = SKILLS_DIR / name / "SKILL.md"
        lines = path.read_text().count("\n")
        status = "✓" if lines < 500 else "✗ OVER LIMIT"
        print(f"  {status} {name}: {lines} lines")

if __name__ == "__main__":
    main()
