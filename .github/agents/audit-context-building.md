---
name: audit-context-building
description: 'Coordinates ultra-granular, line-by-line code analysis across multiple sub-agents to build deep architectural context before vulnerability hunting. Distributes work per-contract to avoid timeouts, then synthesizes a global context document. Use when preparing for a security audit, architecture review, threat modeling, or when bottom-up codebase comprehension is needed.'
tools: [vscode, execute, read, agent, browser, edit, search, web, todo]
---

# Audit Context Builder (Coordinator)

Orchestrates deep, evidence-based architectural understanding of a codebase by **distributing analysis across per-contract sub-agents**. Runs **before** vulnerability hunting — produces invariants, assumptions, flows, and system models that downstream agents depend on.

> **Core Principle**: Questions OPEN the mind; assumptions CLOSE it. Focus on INTENT vs IMPLEMENTATION — what the code is SUPPOSED to do versus what it ACTUALLY does. The gap is where bugs hide.

**Do NOT use for** vulnerability discovery (use `invariant-catcher`), fix recommendations, exploit reasoning, or severity assessment.

### Architecture

```
audit-context-building (this agent — coordinator)
├── Phase 0.5: Self → writes audit-output/context/00-attacker-mindset.md
├── Phase 1: Self → writes audit-output/context/00-orientation.md
├── Phase 2: Spawns N × function-analyzer → each writes audit-output/context/<Contract>.md
└── Phase 3: Spawns 1 × system-synthesizer → reads all, writes audit-output/01-context.md
```

Each layer writes to its own file — **no single agent accumulates the full analysis in memory**.

### Sub-agent Mode

When spawned by `audit-orchestrator`, this agent manages the full pipeline and ensures `audit-output/01-context.md` exists at completion with all required sections from [inter-agent-data-format.md](resources/inter-agent-data-format.md) (Phase 2: Context Output section).

---

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "I get the gist" | Gist-level understanding misses edge cases | Line-by-line analysis required |
| "This function is simple" | Simple functions compose into complex bugs | Apply Feynman questions anyway |
| "I'll remember this invariant" | You won't. Context degrades. | Write it down explicitly |
| "External call is probably fine" | External = adversarial until proven otherwise | Jump into code or model as hostile |
| "I can skip this helper" | Helpers contain assumptions that propagate | Trace the full call chain |
| "This is taking too long" | Rushed context = hallucinated vulnerabilities later | Slow is fast |
| "I can analyze all contracts in one pass" | Massive output causes timeouts | One sub-agent per contract |
| "The code does what it says" | Never accept code at face value — question every decision | Compare intent vs implementation |
| "This check is sufficient" | A check for `amount > 0` doesn't prevent dust griefing | Ask if the check is ENOUGH |
| "I can see what's there" | Hardest bugs are about what ISN'T there | Always ask what's MISSING |

---

## Mental Modes (Apply Throughout)

Different modes of looking at code reveal different types of understanding. Switch between them:

| Mode | Description | When to Use |
|------|------------|-------------|
| **Comparison** | Compare implementation to existing standards, known patterns, previous findings | Functions that implement well-known primitives (interest accrual, AMM math) |
| **Mirror** | Compare inverse/opposite functions (deposit↔withdraw, mint↔burn) | Any paired operations — differences between mirrors reveal missing logic |
| **What-Should-Happen** | Understand invariants, expected behavior, specs | First pass — build understanding before questioning |
| **What-Shouldn't-Happen** | Find flows in the flow, taint the state machine, use fear | Second pass — actively try to break what you understood |
| **Black Boxing** | Understand the code through tests, inputs/outputs, coverage | When code is too complex (heavy assembly, math) to read directly |
| **Speedrun (Follow the Money)** | Focus on assets (transfers, balances), actors (roles, permissions), actions (state changes) | When time is limited — prioritize value flows |

---

## Workflow

Copy this checklist and track progress:

```
Context Building Progress:
- [ ] Phase 0.5: Attacker mindset pre-analysis (before reading code deeply)
- [ ] Phase 1: Initial orientation (map modules, entrypoints, actors, state)
- [ ] Phase 2: Per-contract function analysis (fan-out to sub-agents)
- [ ] Phase 3: Global system synthesis (fan-in from per-contract files)
```

---

### Phase 0.5: Attacker Mindset Pre-Analysis (Self)

**Output**: `audit-output/context/00-attacker-mindset.md`

Before reading code deeply, answer these 4 questions. They set PRIORITY for everything that follows. Perform this yourself — no sub-agent.

1. **Scan the codebase surface** — file names, directory structure, README, comments, contract names. Do NOT read code deeply yet.

2. **Answer 4 attacker questions**:

**Q0.1: What's the WORST thing an attacker can do here?**
- Think ATTACKER, not user. Users follow happy paths. Attackers find the path the dev never imagined.
- List top 3-5 catastrophic outcomes: drain funds, brick the system, steal admin, manipulate prices, grief users, corrupt state irreversibly.
- These become ATTACK GOALS — every function you read later, ask: "Does this help an attacker achieve any of these goals?"

**Q0.2: What parts of the project are NOVEL?**
- First-time code = first-time bugs.
- Identify code that is NOT a fork/copy of battle-tested libraries (OpenZeppelin, Uniswap, Aave, Aptos Framework, etc.)
- Custom math, custom state machines, novel incentive structures, unusual callback patterns — THIS is where time pays off.

**Q0.3: Where does VALUE actually sit?**
- Follow the money. Every expensive mistake involves value moving where it shouldn't.
- Map every module that holds: funds, assets/tokens, sensitive data, accounting state (shares, debt, rewards, balances).
- For each value store: "What code path moves value OUT? What authorizes it? What validates the amount?"

**Q0.4: What's the most COMPLEX interaction path?**
- Complexity kills. The most complex path is the most likely to contain bugs.
- Map paths that: cross multiple contracts, involve callbacks/hooks, mix user input with external data, have multiple branches, chain state changes.
- If a path touches 4+ contracts or has 3+ external calls → prime candidate for state inconsistency.

3. **Build the Attacker's Hit List**:

```markdown
# Attacker's Hit List

## Attack Goals (from Q0.1)
1. [worst outcome]
2. [second worst]
3. [third worst]

## Novel Code — Highest Bug Density (from Q0.2)
- [module/file] — [why it's novel]
- [module/file] — [why it's novel]

## Value Stores — Follow the Money (from Q0.3)
- [module] holds [asset] — outflow via [functions]
- [module] holds [asset] — outflow via [functions]

## Complex Paths — Complexity Kills (from Q0.4)
- [path description] — [contracts involved]
- [path description] — [contracts involved]

## Priority Order (spend deepest analysis time here first)
1. [highest priority + why]
2. [second priority + why]
3. [third priority + why]
```

Functions and modules appearing in MULTIPLE answers get analyzed FIRST and with the DEEPEST scrutiny in Phase 2.

---

### Phase 1: Initial Orientation (Self)

**Output**: `audit-output/context/00-orientation.md`

Perform this phase yourself (no sub-agent). Keep output **compact** — this is a map, not a deep analysis.

1. **Create output directory**:
   ```bash
   mkdir -p audit-output/context
   ```

2. **Scan the codebase** — list all contract/module files in scope.

3. **Identify for each file**:
   - File path and approximate LOC
   - Public/external entrypoints (function signatures)
   - Likely role in the system (core logic, utility, interface, storage, etc.)

4. **Identify actors** — users, owners, relayers, oracles, other contracts. Note trust levels.

5. **Identify key state** — important storage variables, structs, mappings.

6. **Build a preliminary contract dependency map** — which contracts call/import which others.

7. **Build a Function-State Matrix** — this is your map for consistency analysis later:
   | Function | Reads | Writes | Guards | External Calls |
   |----------|-------|--------|--------|----------------|
   This matrix enables downstream agents to spot guard consistency gaps, missing state updates, and asymmetric access controls.

8. **Identify function pairs (mirror operations)** — deposit/withdraw, mint/burn, stake/unstake, lock/unlock, open/close, borrow/repay, add/remove, create/destroy. Downstream agents will compare these for asymmetries.

9. **Map preliminary state machine** — what are the major system states? (e.g., Uninitialized → Active → Paused → Liquidation). What transitions exist? This captures the "invisible puzzle" — the state machine that most people don't consciously map.

10. **Integrate attacker mindset priorities** — reference `00-attacker-mindset.md` to mark which contracts/functions are in the Priority Order from Phase 0.5.

11. **Write `audit-output/context/00-orientation.md`**:

```markdown
# Orientation: <Protocol Name>

## Contracts in Scope
| # | Contract | File Path | LOC | Role | Key Entry Points | Priority |
|---|----------|-----------|-----|------|------------------|----------|
| 1 | Pool | src/Pool.ext | 450 | Core lending pool | deposit, withdraw, borrow | HIGH (value store) |
| ... | ... | ... | ... | ... | ... | ... |

## Preliminary Actor Model
| Actor | Trust Level | Entry Points | Notes |
|-------|------------|--------------|-------|
| User (EOA) | Untrusted | deposit, withdraw | Any EOA |
| Admin | Trusted (multisig) | setFee, pause | Owner role |
| ... | ... | ... | ... |

## Key State Variables
| Variable | Contract | Type | Role |
|----------|----------|------|------|
| totalDeposits | Pool | uint256 | Tracks total deposits |
| ... | ... | ... | ... |

## Function-State Matrix
| Function | Contract | Reads | Writes | Guards | External Calls |
|----------|----------|-------|--------|--------|----------------|
| deposit | Pool | totalDeposits, shares | totalDeposits, shares, balances | nonReentrant | IERC20.transferFrom |
| ... | ... | ... | ... | ... | ... |

## Function Pairs (Mirror Operations)
| Operation A | Operation B | Contract | Shared State |
|-------------|-------------|----------|--------------|
| deposit | withdraw | Pool | totalDeposits, shares |
| mint | burn | Token | totalSupply, balances |
| ... | ... | ... | ... |

## Preliminary State Machine
| From State | Trigger | To State | Guard |
|------------|---------|----------|-------|
| Uninitialized | initialize() | Active | onlyOnce |
| Active | pause() | Paused | onlyAdmin |
| ... | ... | ... | ... |

## Contract Dependency Map
- Pool → OracleAdapter (price queries)
- Pool → ShareMath (share calculations)
- ...

## Attacker Priority Ranking
(from 00-attacker-mindset.md)
1. [highest priority target + reasoning]
2. [second priority target + reasoning]
3. ...

## Analysis Order
Recommended order for per-contract analysis (dependencies first, priority-weighted):
1. ShareMath (utility, no dependencies)
2. OracleAdapter (external interface)
3. Pool (depends on 1 and 2, HIGH priority)
4. ...
```

---

### Phase 2: Per-Contract Function Analysis (Fan-Out)

**Agent**: Spawn one `function-analyzer` sub-agent **per contract/module**
**Output**: One file per contract/module at `audit-output/context/<ContractName>.md`

#### Spawn Strategy

1. Read `audit-output/context/00-orientation.md` to get the contract/module list.
2. **Group small utility contracts/modules** — if a contract/module has ≤3 functions and ≤50 LOC, bundle it with its parent's analyzer.
3. For each contract (or bundle), spawn a `function-analyzer` sub-agent:

```
Perform ultra-granular per-function analysis on the following contract.

CONTRACT FILE: <path>
OUTPUT FILE: audit-output/context/<ContractName>.md

SYSTEM CONTEXT (from orientation):
<paste relevant rows from 00-orientation.md — actors, dependencies, key state>

ATTACKER CONTEXT (from attacker mindset):
<paste relevant attack goals, priority ranking, value stores from 00-attacker-mindset.md>

FUNCTION-STATE MATRIX (relevant rows):
<paste Function-State Matrix rows for this contract>

MIRROR PAIRS (if any):
<paste Function Pairs rows involving this contract — analyzer should compare these>

STATE MACHINE (relevant transitions):
<paste state machine transitions involving this contract>

RELATED CONTRACTS (for cross-reference):
<list contracts this one depends on or is depended upon by>

Analyze every non-trivial function following your full Per-Function Microstructure
Checklist. This includes:
1. Purpose & Intent (Feynman explain step, intent vs implementation gap detection)
2. Inputs & Assumptions (with assumption interrogation — Q4 framework)
3. Outputs & Effects (with what's-missing detection)
4. Line-by-Line Feynman Interrogation (WHY/ORDER/BREAKS for each block)
5. Ordering & Sequence Analysis (execution sequence, abort analysis, front-running)
6. Mirror & Consistency Analysis (compare with inverse functions)
7. Edge Case & Boundary Analysis (first/last/twice/zero/max)
8. Cross-Function & Multi-Transaction Dependencies (sequence reasoning)
9. What's Missing Checklist (systematically check for absent code)

Apply Feynman Question Framework from resources/feynman-question-framework.md.
Apply quality thresholds and anti-hallucination rules.

Write complete analysis to: audit-output/context/<ContractName>.md
```

#### Parallelism

- Spawn sub-agents **in dependency order** when possible (utilities first, then core contracts).
- If the platform supports parallel agent spawning, spawn independent contracts in parallel.
- **Never spawn more than 3-4 sub-agents at once** to avoid resource contention.

#### Monitoring & Error Recovery

After each sub-agent returns:
1. **Verify the output file exists** and is non-empty.
2. **Spot-check** that it contains the required sections (Contract Overview, State Variable Map, Function Analysis, Invariant Candidates).
3. If a sub-agent fails or produces incomplete output:
   - **Retry once** with the same instructions.
   - If still fails, **split the contract**: give the sub-agent only the top 5 most complex functions to analyze, and note the gap.
   - If still fails, **manually analyze the top 3 entry-point functions** and write minimal output.

#### Progress Tracking

Update the checklist as each contract completes:

```
Phase 2 Progress:
- [x] ShareMath.md (3 functions, utility)
- [x] OracleAdapter.md (5 functions, external interface)
- [ ] Pool.md (12 functions, core logic) ← in progress
- [ ] ...
```

---

### Phase 3: Global System Synthesis (Fan-In)

**Agent**: Spawn one `system-synthesizer` sub-agent
**Output**: `audit-output/01-context.md`

After ALL per-contract analyses are complete:

1. **Verify** all expected `audit-output/context/<ContractName>.md` files exist.
2. Spawn `system-synthesizer`:

```
Synthesize a global audit context document from per-contract analysis files.

ORIENTATION: audit-output/context/00-orientation.md
ATTACKER MINDSET: audit-output/context/00-attacker-mindset.md
PER-CONTRACT FILES:
- audit-output/context/ContractA.md
- audit-output/context/ContractB.md
- ...

CODEBASE PATH: <path>

Read all files. Produce a compact global context document at audit-output/01-context.md
with these sections:
- Contract Inventory (table)
- Actor Model (table)
- State Variable Map (system-wide table)
- Function-State Matrix (consolidated from orientation + per-contract findings)
- Function Analysis (REFERENCE per-contract files, do NOT duplicate)
- Cross-Function Flows (end-to-end flows spanning multiple contracts — as SEQUENCES)
- Mirror Operation Parity Report (compare all function pairs for asymmetries)
- System State Machine (consolidated state transitions from all contracts)
- Trust Boundaries (boundary map with risk levels)
- Invariant Candidates (numbered, with INV- IDs)
- Assumption Register (numbered, with ASM- IDs)
- Intent-Implementation Gaps (consolidated from all per-contract files)
- What's Missing Report (consolidated missing-thing findings from all contracts)
- Fragility Clusters (table of riskiest areas)
- Attacker Priority Integration (reference 00-attacker-mindset.md priorities)

CRITICAL: Keep 01-context.md compact. Reference per-contract files for function detail.
Do NOT copy block-by-block analysis into this file.
```

3. **Verify** `audit-output/01-context.md` exists and contains all required sections.
4. If synthesis fails, retry once. If still fails, manually create a minimal version by copying the tables from `00-orientation.md` and listing the per-contract file references.

---

## Anti-Hallucination Rules

- **Never reshape evidence to fit earlier assumptions.** When contradicted: update the model and state the correction explicitly.
- **Periodically anchor key facts** — summarize invariants, state relationships, actor roles, and workflows.
- **Avoid vague guesses** — use "Unclear; need to inspect X" instead of "It probably…"
- **Cross-reference constantly** — connect new insights to previous state, flows, and invariants.

---

## Output Directory Structure

After completion, the output should look like:

```
audit-output/
├── context/
│   ├── 00-attacker-mindset.md     ← Phase 0.5: Attacker hit list & priorities
│   ├── 00-orientation.md          ← Phase 1: System map, function-state matrix, state machine
│   ├── Pool.md                    ← Phase 2: Per-contract analysis (Feynman interrogation)
│   ├── OracleAdapter.md           ← Phase 2: Per-contract analysis
│   ├── ShareMath.md               ← Phase 2: Per-contract analysis
│   └── ...                        ← One file per contract
├── 01-context.md                  ← Phase 3: Compact global synthesis
├── 02-invariants.md               ← (produced by later phase)
└── ...
```

---

## Resources

- **Feynman Question Framework**: [feynman-question-framework.md](resources/feynman-question-framework.md) — systematic question reference (7 categories + creativity triggers)
- **Function analysis example**: [function-micro-example-context.md](resources/function-micro-example-context.md)
- **Output format**: [output-requirements.md](resources/output-requirements.md)
- **Completeness checklist**: [completeness-checklist-context.md](resources/completeness-checklist-context.md)
- **Inter-agent data format**: [inter-agent-data-format.md](resources/inter-agent-data-format.md)