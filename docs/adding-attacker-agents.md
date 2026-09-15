# Adding Attacker Agents — Gap Analysis & Playbook

> **Purpose**: How to grow the discovery ("attacker") layer of the audit pipeline — where the current roster falls short, how to validate a gap is real, and the house pattern every new attacker agent must follow.
> **Audience**: Anyone extending `.claude/agents/` with new discovery agents (the A-series tracker issues #9–#21 are resolved on GitHub).

---

## 1. What counts as an attacker agent

An attacker agent's job is to *produce candidate findings* in Phase 4 (Iterative Discovery) — as opposed to context agents (Phase 2), validators (Phase 6–7 PoC/fuzz/FV), judges (Phase 8/10), or DB agents (post-audit). Attackers come in three shapes:

1. **Lane runners** — the orchestrator's four parallel discovery lanes.
2. **Class specialists** — deep attackers for one vulnerability class (`missing-validation-reasoning` is the model).
3. **Meta attackers** — don't find bugs themselves; make every other attacker better (coverage tracking, round targeting).

## 2. Current roster and what each covers

| Lane / agent | Shape | What it attacks | Blind spot by design |
|---|---|---|---|
| **4A** DB hunt-card loop (`invariant-catcher`, `grep_prune.py` → `03-findings-*`) | Lane | Known patterns from `DB/manifests/huntcards/` matched against code | Only finds what the DB already generalizes; weak on novel compositions |
| **4B** `protocol-reasoning` | Lane | Domain-decomposed reasoning seeded by DB root causes; 4 rounds (standard → cross-domain → edge-case → completeness) | Reasoning depth bounded by turn budget; breadth-first over depth-first |
| **4C** `multi-persona-orchestrator` (6 personas) | Lane | Cognitive strategies: BFS, DFS, backward-from-sink, state machine, mirror pairs, re-implementation diff | Strategies are code-shape-based — none model an *adversary* or the *external world* |
| **4D** `missing-validation-reasoning` | Specialist | Input/hygiene validation gaps in gatekeeper functions | Validation only — not authz, not external-contract hostility |
| `attack-graph-synthesizer` | Specialist | Multi-step chains via `DB/graphify-out/graph.json` against invariants | Chain *composition*; relies on candidates existing to compose |
| **4E–4G** economic lane (`tokenomics-auditor`, `risk-parameter-reviewer`, `manipulation-feasibility-analyst`) | Specialists (scope-gated) | Economic layer: tokenomics value flows, risk parameters, oracle manipulation feasibility | Economics only |
| A06 `economic-attack-simulator` (Phase 6a gate) | Gate | Per-attack net-USD profit: PROFITABLE / CONDITIONAL / UNPROFITABLE | Validation only — gates PoC spend and feeds judges |

## 3. Gap analysis — four dimensions

### 3.1 Vulnerability-class gaps (no specialist exists)

- **Access control / privileged paths.** Role escalation, initializer abuse, timelock windows, "which key can steal or brick". Access control failures are a top DeFi incident class, yet only `missing-validation` touches its edge (constructor/setter checks) and no persona is privilege-focused.
- **Hostile external world.** Nothing treats the protocol's *dependencies* as adversarial: fee-on-transfer/rebasing/no-return ERC-20s, ERC-721 receiver hooks, ERC-1271 callbacks, permit races. The DB has scattered cards; no attacker composes them.
- **Cross-chain message flows.** Bridges are the largest historical loss category. The `bridge` manifest holds patterns, but no reasoning attacker handles domain replay, double execution, or failure-delivery paths.
- **Signatures & cryptography** (backlog): EIP-712 domain confusion, nonce/permit replay across chains, `ecrecover` malleability, ERC-1271 bypass.
- **Upgradeability layouts** (backlog): storage-gap math, initializer shadowing — partially covered by DB cards.
- **Gas/griefing/DoS** (backlog): unbounded loops, blocking patterns, OOG traps.

### 3.2 Attacker-profile gaps (no persona models an adversary)

The 6 personas are *reading strategies*, not adversaries. Missing profiles: malicious privileged operator (what does a compromised admin key actually get?), hostile integration counterparty (above), and economic rational attacker (now covered by A06/A09).

### 3.3 Capability gaps (no agent wields the tool)

- **Fork-state hunting** — discovery against forked mainnet state (real positions, real rates, real liquidity), not just source. `poc-writing` forks for *validation*; nothing hunts in forks.
- **Differential execution** — `persona-reimplementer` hypothesizes; a differential agent would actually run a reference implementation against the real code and diff outputs.
- **Bytecode-vs-source** — verify the deployed artifact matches audited source (proxies, immutables, constructor args).
- **PoC mutation** — take DeFiHackLabs exploits for the same *mechanism* and mutate them onto the target (analogical attack transfer). Distinct from `prior-art-matcher` (A03), which matches by lineage, not mechanism mutation.

### 3.4 Process gaps (meta)

- **No coverage ledger.** ~~`memory-state.md` records DEAD_ENDs, but nothing tracks *which functions/paths/invariants were attacked in which round*~~ **Fixed**: `attack-coverage-tracker` (A14) maintains `attack-coverage.json` and emits `round-N-targets.md` steering rounds at unattacked surface.
- **No claim verification.** Sponsors' docs make falsifiable claims ("1:1 backing", "admin cannot move user funds"); no agent extracts and attacks them. Still open — A15 (claim-verifier) was rejected; claim attacks live in `manipulation-feasibility-analyst`'s doc-claim-vs-constant verification for oracle claims only.

## 4. Decision — what got filed vs rejected

**Filed and shipped**: A14 (`attack-coverage-tracker`) now exists, alongside A01–A10 — recon-specialist, finding-merger, prior-art-matcher, findings-db-synthesizer, mitigation-reviewer, economic-attack-simulator, tokenomics-auditor, risk-parameter-reviewer, manipulation-feasibility-analyst, remediation-safety-checker.

**Rejected**: class-specialist proposals — access-control-attacker (A11), hostile-integration-attacker (A12), cross-chain-attacker (A13), claim-verifier (A15). Rationale: `protocol-reasoning`'s seeded rounds already own vulnerability-class reasoning, and the DB hunt cards already carry the class patterns. A new lane that reasons about *a vulnerability class* duplicates 4A+4B; new agents must change the **kind of work**, not the vulnerability class. Concretely, accepted kinds so far: coordination/meta (A14, A02), economics layer (A06–A09), validation gates (A06, A10), engagement modes (A05), DB flywheel (A04).

**Rule going forward**: if a class needs more depth, widen `protocol-reasoning` — better reasoning seeds from the relevant manifest, a dedicated round mode, or new DB entries — do not add a class-specialist lane. See Step 1 below.

## 5. Playbook — adding a new attacker agent

### Step 1 — Validate the gap is real

Before writing anything, check all three:

1. **Not a vulnerability-class gap.** This is the decisive check: `protocol-reasoning` (4B) seeded by DB hunt cards already reasons over every vulnerability class — access control, weird tokens, cross-chain flows included. A class gap is fixed by widening 4B (better seeds from the relevant manifest, a new round mode, new DB entries), **not** by a new specialist lane. Class-specialist proposals (A11–A13) were rejected on exactly this basis.
2. **Not a DB pattern duplicate.** Search `DB/index.json` + hunt cards for the class. If the DB generalizes it well, extend the DB or the seeds, not the agent roster.
3. **Not a strategy duplicate.** Re-read the 6 personas and `protocol-reasoning`'s four rounds. If the new agent would find the same bugs via a slightly different reading strategy, don't add it — widen a persona.
4. **Changes the kind of work.** The surviving proposals change *what* gets done, not *which class* gets read: coordination (A14), quantification (A06), parameter tables (A08), report gating (A10), lineage retrieval (A03). A meta agent must measurably improve other agents' yield — otherwise it's overhead.

Rule of thumb: add an attacker when it needs a *different mental model or tool* (adversary economics, coverage ledger, fork state), not a different grep — and never merely a different vulnerability class.

### Step 2 — Pick the integration point

- **Specialist lane** (like 4D): new letter, e.g. 04h. Runs parallel to existing lanes each discovery round; spawn condition can be scope-gated (e.g. A13 only when bridge/CCIP/LayerZero contracts in scope).
- **Persona**: only if it's a reading strategy — then it belongs inside `multi-persona-orchestrator`'s roster, not a new lane.
- **Meta**: writes to `audit-output/` state files consumed by the orchestrator's round planning (see A14), not `04*` findings.

### Step 3 — Write `.claude/agents/<name>.md` per the house pattern

Model on `missing-validation-reasoning.md`. Required sections:

- **Frontmatter**: `name`, `description` (trigger conditions — when to use, when NOT to), `tools`, `maxTurns` (specialists get 50–100).
- **"Requires prior context"** line: `audit-context-building` output (`01-context.md`, `02-invariants.md`).
- **"Do NOT use for"** line: route readers to the right sibling agent.
- **Sub-agent mode**: read inputs by exact path, write findings to `audit-output/04<letter>-<name>-findings.md` (plus `-round-N`) in the standard Finding Schema from `.claude/resources/inter-agent-data-format.md`.
- **Memory state integration**: read `memory-state.md` (PATTERN/DEAD_END entries) before starting; append `MEM-4<LETTER>-R<round>-<NAME>` after.
- **Rationalizations (Do Not Skip)**: the house signature — enumerate the self-deceptions this specialist is prone to ("the modifier checks the role, so the path is safe" …) and require the agent to argue past each.
- **Reachability proof requirement**: every finding must include the Step-1..N actor/state chain ending in a violated invariant with quantified impact — no "could potentially" findings.
- **Empirical grounding**: cite the incident class (DeFiHackLabs counts, DB root-cause IDs) the agent is seeded from.

### Step 4 — Write `.claude/skills/<name>/SKILL.md`

Frontmatter mirrors the agent (`context: fork`, `agent: <name>`, `argument-hint`); body is the operational checklist version of the agent doc. Skill = how a human/orchestrator invokes it; agent = the mind.

### Step 5 — Wire it in

- `audit-orchestrator` Phase 4: add the lane to the fan-out, including round loop and spawn conditions.
- `.claude/resources/inter-agent-data-format.md`: register the new artifact filenames and any schema extensions (follow the `04a` extended-schema precedent).
- Round cross-pollination: if the lane should share knowledge between rounds, hook into `discovery-state-round-N.md`.

### Step 6 — Seed from the DB (and feed back)

If the vulnerability class lacks DB entries, add them **first** via `TEMPLATE.md` + `docs/db-guide.md` workflow (`generate_manifests.py`, `db_quality_check.py`), then let the agent be seeded by its own hunt cards. Post-audit, confirmed findings flow back through A04 (`findings-db-synthesizer`) — new attacker agents multiply DB growth.

### Step 7 — Regeneration contract (non-negotiable)

```bash
python3 scripts/sync_codex_compat.py
python3 scripts/sync_codex_compat.py --sync-github-agents
python3 scripts/validate_codex_runtime.py
```

Never hand-edit `.agents/skills/`, `.codex/`, or `.github/agents/`.

### Step 8 — Eval and calibration (define before first run)

- **Recall eval**: replay against a known-buggy target — a DeFiHackLabs PoC case or past contest repo. The agent must surface the known bug with a reachability proof. If it can't find a bug its class was built for, the prompt is wrong — iterate before shipping.
- **Precision eval**: run against a clean, well-audited target. False-positive rate matters more than raw yield; a specialist that cries wolf gets its lane deprioritized by the orchestrator.
- **Signal check on real runs**: after N audits, compare findings-accepted-by-judges per lane. A lane with consistently low judge-validation rate is mis-seeded or redundant — retire or re-scope it.

## 6. Anti-patterns

- **Grep-in-a-trench-coat**: an agent that just re-runs hunt-card patterns 4A already covers. Extend the DB, not the agent roster.
- **Persona clones**: "aggressive reader", "paranoid reader" — reading postures aren't adversaries; personas are capped at strategies that change *traversal order*.
- **God attackers**: "finds all logic bugs" — every specialist needs a class boundary and a "Do NOT use for" escape hatch.
- **Unfalsifiable findings**: no reachability proof, no invariant violated, no quantified impact → the finding dies in triage (A02) anyway; don't let agents emit them.

## 7. Backlog (candidate attackers, not yet filed)

Per §4's decision, the class/profile rows below are **not** new-agent candidates — they are `protocol-reasoning` seed/DB widening work. Only the capability rows (different tool, different data) qualify as future agents.

| Candidate | Dimension | Route |
|---|---|---|
| signature-replay coverage | class | widen 4B seeds + DB entries, no new agent |
| upgradeability-layout coverage | class | widen 4B seeds + DB entries, no new agent |
| gas-griefing coverage | class | widen 4B seeds + DB entries, no new agent |
| malicious-operator reasoning | profile | widen 4B round mode, no new agent |
| docs-claims attack | process | revisit only with a demonstrated 4B blind spot |
| fork-state-attacker | capability | agent candidate — hunts against live mainnet fork state |
| differential-execution-attacker | capability | agent candidate — runs reference impl vs actual, diffs outputs |
| bytecode-vs-source-verifier | capability | agent candidate — deployed artifact vs audited source |
| poc-mutation-attacker | capability | agent candidate — mutates DeFiHackLabs exploits by mechanism onto target |

File a capability candidate when its eval target exists (a replayable known-bug case for its class) — Step 8 requires it.
