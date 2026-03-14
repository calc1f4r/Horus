# AGENTS.md

This document gives agent models (like you) practical guidance for making safe, correct, and minimal changes in this repository. It captures project conventions, architecture, invariants, and how to run and extend tests.

## Scope & Goals

- Primary domain: Creation of Vulnerability database entries for smart contract security and blockchain appchains. 
- Core guarantees:
  - Making sure every vulnerability entry is well-structured, semantically rich, and optimized for vector search.
  - Ensuring consistency with existing entries and adherence to the provided template.

---

## Architecture: 4-Tier Search

The database uses a **tiered architecture** for precision. Never read entire vulnerability files — use hunt cards or manifests to find exact line ranges.

```
Tier 1:   DB/index.json                          ← Router (~350 lines). Start here.
   ↓  
Tier 1.5: DB/manifests/huntcards/*-huntcards.json ← Compressed detection cards (~55K tokens for ALL 451 patterns)
   ↓  
Tier 2:   DB/manifests/<name>.json                ← Full pattern-level index with line ranges (11 manifests)
   ↓  
Tier 3:   DB/**/*.md                              ← Vulnerability content. Read ONLY targeted line ranges.
```

**Hunt Cards (Tier 1.5)**: Enriched detection cards with `grep` patterns, one-line detection rules, **micro-directives** (`check` steps, `antipattern`, `securePattern`), category tags, and `neverPrune` flags for CRITICAL patterns. Load `DB/manifests/huntcards/all-huntcards.json` to fit ALL patterns in context. For each card: grep target code → on hit, execute `card.check` steps directly against the target code. Only read full .md entry (`card.ref` + `card.lines`) for confirmed true/likely positives.

For the full search guide, see `DB/SEARCH_GUIDE.md`.

---

## 🔍 Quick Start: Finding Vulnerability Patterns

### Step 1: Load the Router

Read `DB/index.json` (~330 lines). It contains:
- **`protocolContext`** — maps protocol types to relevant manifests + focus patterns
- **`manifests`** — lists all 11 manifest files with descriptions and pattern counts
- **`auditChecklist`** — quick security checks by category
- **`keywordIndex`** — points to `DB/manifests/keywords.json` for keyword search

### Step 2: Load Hunt Cards (Preferred) or Manifests

**For bulk scanning (audits)**: Load hunt cards instead of full manifests:
- `DB/manifests/huntcards/all-huntcards.json` — ALL 451 patterns (~55K tokens)
- `DB/manifests/huntcards/<manifest>-huntcards.json` — per-manifest cards

Each card has a `grep` field for searching target code and `ref` + `lines` for reading the full DB entry on hit.

**For browsing/targeted lookup**: Load 1-3 relevant manifests:

| Manifest | Patterns | Focus |
|----------|----------|-------|
| `oracle` | 39 | Chainlink, Pyth, price manipulation |
| `amm` | 65 | Concentrated liquidity, constant product |
| `bridge` | 32 | LayerZero, Wormhole, Hyperlane |
| `tokens` | 33 | ERC20, ERC4626, ERC721 |
| `cosmos` | 26 | Cosmos SDK, IBC, staking |
| `solana` | 38 | Solana programs, Token-2022 |
| `general-security` | 31 | Access control, signatures, validation |
| `general-defi` | 115 | Flash loans, vaults, precision, calculations |
| `general-infrastructure` | 41 | Proxies, reentrancy, storage |
| `general-governance` | 56 | Governance, stablecoins, rug pulls, MEV |
| `unique` | 59 | Protocol-specific unique exploits |

### Step 3: Find Specific Patterns

Each manifest entry has:
```json
{
  "id": "oracle-staleness-001",
  "title": "Missing Staleness Check",
  "lineStart": 93,    ← Use these with read_file
  "lineEnd": 248,     ← to read ONLY this section
  "severity": ["MEDIUM"],
  "codeKeywords": ["getPriceUnsafe", "publishTime"],
  "rootCause": "No freshness validation on oracle price data..."
}
```

### Step 4: Read Targeted Content

```
read_file("DB/oracle/pyth/PYTH_ORACLE_VULNERABILITIES.md", startLine=93, endLine=248)
```

This gives you **exactly** the vulnerability pattern — no noise, no wasted context.

---

## Search Workflows

### By Protocol Type (Most Common)
```
index.json → protocolContext.mappings.lending_protocol
  → manifests: ["oracle", "general-defi", "tokens", "general-security"]
  → focusPatterns: ["staleness", "liquidation", "flash loan", ...]
→ Load manifests → search patterns → read line ranges
```

### By Keyword
```
DB/manifests/keywords.json → "getPriceUnsafe" → ["oracle"]
→ Load oracle.json → search codeKeywords → read line ranges
```

### By Severity
```
Load manifest → filter patterns where severity includes "HIGH" or "CRITICAL"
→ Read matching line ranges
```

### Available Protocol Contexts

| Context | Use When Auditing |
|---------|-------------------|
| `lending_protocol` | Aave, Compound, lending/borrowing protocols |
| `dex_amm` | Uniswap, SushiSwap, decentralized exchanges |
| `vault_yield` | ERC4626 vaults, yield aggregators, strategies |
| `governance_dao` | DAOs, governance systems, voting contracts |
| `cross_chain_bridge` | Bridges, LayerZero, Wormhole integrations |
| `cosmos_appchain` | Cosmos SDK chains, IBC, app-chains |
| `solana_program` | Solana programs, SPL tokens |
| `perpetuals_derivatives` | Perpetual DEXes, options, derivatives |
| `token_launch` | Token launches, meme coins, trading contracts |
| `staking_liquid_staking` | Staking protocols, liquid staking |
| `nft_marketplace` | NFT platforms, ERC721 marketplaces |

### Dynamic Context Pruning (Category Branches)
When fetching reference files or raw audits, agents should be mindful of token limits. A GitHub Action automatically creates isolated branches for every category in the `reports/` directory. Rather than loading the entire `reports` context, agents or workflows can fetch and mount specific vulnerabilities:
```bash
# Example: Fetching only ERC4626 vault reports
git clone -b reports/erc4626 --single-branch https://github.com/calc1f4r/Vulnerability-database.git
```

---

## Workflow for Vulnerability Discovery

### Standard (Browsing/Targeted)
```
1. Identify protocol type → Read index.json protocolContext
2. Load relevant manifests (1-3) → Browse patterns by title/severity/keywords
3. Read exact line ranges → Get precise vulnerability content
4. Check unique exploits → Load DB/manifests/unique.json
5. Apply patterns → Match against target codebase
```

### Bulk Hunt (Audit Mode — Recommended for Full Audits)
```
1. Identify protocol type → Read index.json protocolContext
2. Load enriched hunt cards for resolved manifests (or all-huntcards.json)
3. For each card, grep target code: `grep -rn "card.grep" <target_path>`
4. Cards with `neverPrune: true` always survive (CRITICAL safety net)
5. Prune cards with zero grep hits (removes ~60-80% of patterns)
6. PARTITION surviving cards into shards of 50-80 cards (grouped by cat tag)
   - neverPrune cards are duplicated into every shard
7. SPAWN one sub-agent per shard (parallel) — each gets shard cards + full target code
8. Per-shard: PASS 1 (micro-directives) + PASS 2 (evidence lookup for true/likely positives)
9. MERGE all shard findings → deduplicate by root cause → 03-findings-raw.md
```

---

## Regenerating Manifests

When vulnerability files are added or updated:
```bash
python3 generate_manifests.py
```

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `DB/index.json` | **START HERE** — Lean router to manifests + hunt cards |
| `DB/manifests/huntcards/all-huntcards.json` | **ALL hunt cards** — 451 compressed detection cards (~55K tokens) |
| `DB/manifests/huntcards/<name>-huntcards.json` | Per-manifest hunt cards |
| `DB/manifests/*.json` | Full pattern-level indexes with line ranges |
| `DB/SEARCH_GUIDE.md` | Detailed search guide for agents |
| `TEMPLATE.md` | Structure for new vulnerability entries |
| `Example.md` | Reference implementation of an entry |
| `generate_manifests.py` | Re-generates manifests after DB changes |

---

## Audit Orchestrator — General Purpose Audit Agent

The `audit-orchestrator` agent (`.github/agents/audit-orchestrator.md`) is the **primary entry point** for auditing an unfamiliar codebase. It takes a codebase path, an optional protocol hint, and optional flags for pipeline configuration.

### Invocation

```
@audit-orchestrator <codebase-path> [protocol-hint] [--static-only] [--judge=sherlock|cantina|code4rena] [--discovery-rounds=N]
```

**Flags**:
- `--static-only` — Skip Phases 6-7 (no PoC generation, no FV execution). Findings confirmed through judging self-loop only.
- `--judge=X` — Use a single judge instead of all 3. Consensus becomes 1/1.
- `--discovery-rounds=N` — Number of iterative discovery rounds (default: 2, max: 5). Higher = more cross-pollination.

### Pipeline

```
Phase 1:  Reconnaissance      → Protocol detection, scope, manifest resolution
Phase 2:  Context Building     → Sub-agent: audit-context-building
Phase 3:  Invariant Extraction → Sub-agent: invariant-writer (3A) → invariant-reviewer (3B)
Phase 4:  Iterative Discovery  → N rounds of 4-way parallel fan-out:
  4A: DB-powered Hunting  → Self (grep-prune + partition) + N × Sub-agent: invariant-catcher
  4B: Reasoning Discovery → Sub-agent: protocol-reasoning
  4C: Multi-Persona Audit → Sub-agent: multi-persona-orchestrator (6 personas)
  4D: Validation Gaps     → Sub-agent: missing-validation-reasoning
  Between rounds: orchestrator writes discovery-state-round-N.md (cross-pollination bus)
Phase 5:  Merge & Triage      → Self (cross-source correlation, dedup, falsification, severity)
Phase 6:  PoC Gen + EXECUTION → [CONDITIONAL] Sub-agent: poc-writing × N → compile → run
Phase 7:  FV Gen + EXECUTION  → [CONDITIONAL] Sub-agents: medusa-fuzzing, certora-verification,
                                  halmos-verification → compile → run
Phase 8:  Pre-Judging         → Judge(s) screen all triaged findings (VALID/INVALID)
Phase 9:  Issue Polishing      → Sub-agent: issue-writer × N (valid findings only)
Phase 10: Deep Review          → Same judge(s) do line-by-line verification (CONFIRMED/NEEDS-REVISION/REJECTED)
Phase 11: Report Assembly     → Produces audit-output/CONFIRMED-REPORT.md
```

### Agent Dependency Graph

```
                        ┌─────────────────────┐
                        │  audit-orchestrator  │  ← ENTRY POINT
                        └──────────┬──────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
┌──────────────────┐  ┌────────────────────┐  ┌──────────────────────┐
│ audit-context-   │  │ N × invariant-     │  │ missing-validation-  │
│ building         │  │ catcher (parallel  │  │ reasoning            │
└────────┬─────────┘  │ shards)            │  └──────────────────────┘
         │            └────────────────────┘
         ▼                                     ┌──────────────────────┐
┌──────────────────┐                           │ protocol-reasoning   │
│ invariant-writer │                           │ (spawns domain       │
└────────┬─────────┘                           │ sub-agents)          │
         │                                     └──────────────────────┘
         ▼
┌──────────────────┐                           ┌──────────────────────┐
│ invariant-       │                           │ multi-persona-       │
│ reviewer         │                           │ orchestrator         │
└────────┬─────────┘                           │ (spawns 6 personas)  │
         │                                     └──────────────────────┘
         │
    Phase 4 runs iteratively (N rounds)
    Between rounds: discovery-state-round-N.md cross-pollination
         │
    ┌────┴─────┬──────┐  ← [CONDITIONAL: skipped if --static-only]
    ▼          ▼      ▼
┌────────┐ ┌──────┐ ┌────────┐
│ medusa │ │certora│ │ halmos │  ← FV generated AND executed
│ fuzzing│ │verif. │ │ verif. │
└────────┘ └──────┘ └────────┘

Post-triage:
  ├── poc-writing (per CRITICAL/HIGH finding) → EXECUTION [CONDITIONAL]
  ├── Phase 8: Pre-Judging ────────────────── judge(s) screen validity
  │   (--judge=X: single judge; default: sherlock + cantina + code4rena)
  ├── Phase 9: issue-writer (valid findings only)
  ├── Phase 10: Deep Review ─────────────── same judge(s) line-by-line
  │   CONFIRMED / NEEDS-REVISION / REJECTED
  │   NEEDS-REVISION → retry once via Phase 9
  └── CONFIRMED-REPORT.md
```

### Data Pipeline Producers & Consumers

> **Cross-cutting**: `memory-state.md` is read and written by ALL agents. Every agent reads it before starting and appends a memory entry after completing. The orchestrator consolidates between phases. See [memory-state.md](.github/agents/resources/memory-state.md).

| Agent | Produces | Consumes |
|-------|----------|----------|
| `audit-orchestrator` | `00-scope.md`, `pipeline-state.md`, `memory-state.md` (init + consolidation), `hunt-card-shards.json`, `reasoning-seeds.md`, `discovery-state-round-*.md`, `03-findings-raw.md` (merged), `05-findings-triaged.md`, `08-pre-judge-results.md`, `10-deep-review.md`, `CONFIRMED-REPORT.md` | All outputs |
| `audit-context-building` | `01-context.md`, `context/*.md` | Scope |
| `invariant-writer` | `02-invariants.md` | Context |
| `invariant-reviewer` | `02-invariants-reviewed.md` | Invariants, context, DB manifests |
| `invariant-catcher` (×N shards) | `03-findings-shard-<id>.md` | Shard cards, invariants, target code |
| `protocol-reasoning` | `04a-reasoning-findings.md` | Context, invariants, reasoning seeds, manifests |
| `multi-persona-orchestrator` | `04c-persona-findings.md`, `personas/round-N/*.md`, `personas/shared-knowledge-round-N.md` | Context, invariants |
| `missing-validation-reasoning` | `04d-validation-findings.md` | Context |
| `poc-writing` | `pocs/F-NNN-poc.{ext}` | Individual findings |
| `issue-writer` | `issues/F-NNN-issue.md` | Individual findings + PoC results + FV results |
| `medusa-fuzzing` | `fuzzing/` harnesses | Invariant specs |
| `certora-verification` | `certora/` specs | Invariant specs |
| `halmos-verification` | `halmos/` symbolic tests | Invariant specs |
| `sherlock-judging` | `08-pre-judge-sherlock.md`, `10-deep-review-sherlock.md` | Triaged findings (Phase 8), polished findings (Phase 10) |
| `cantina-judge` | `08-pre-judge-cantina.md`, `10-deep-review-cantina.md` | Triaged findings (Phase 8), polished findings (Phase 10) |
| `code4rena-judge` | `08-pre-judge-code4rena.md`, `10-deep-review-code4rena.md` | Triaged findings (Phase 8), polished findings (Phase 10) |
| `persona-bfs` (×1 per round) | `personas/round-N/bfs.md` | Scope, shared knowledge, target code |
| `persona-dfs` (×1 per round) | `personas/round-N/dfs.md` | Scope, shared knowledge, target code |
| `persona-working-backward` (×1 per round) | `personas/round-N/backward.md` | Scope, shared knowledge, target code |
| `persona-state-machine` (×1 per round) | `personas/round-N/state-machine.md` | Scope, shared knowledge, target code |
| `persona-mirror` (×1 per round) | `personas/round-N/mirror.md` | Scope, shared knowledge, target code |
| `persona-reimplementer` (×1 per round) | `personas/round-N/reimpl.md` | Scope, shared knowledge, target code |

### New Resource Files

| Resource | Purpose |
|----------|---------|
| `.github/agents/resources/inter-agent-data-format.md` | Standardized data contracts between pipeline phases |
| `.github/agents/resources/protocol-detection.md` | Auto-classification decision tree for codebases |
| `.github/agents/resources/audit-report-template.md` | Final report structure and quality checklist |
| `.github/agents/resources/orchestration-pipeline.md` | 11-phase pipeline with error handling, context budgets, and phase gates |
| `.github/agents/resources/reasoning-skills.md` | Core reasoning framework for deep vulnerability analysis |
| `.github/agents/resources/domain-decomposition.md` | Domain decomposition strategy for reasoning agent |
| `.github/agents/resources/certora-sui-move-reference.md` | CVLM type system, manifest functions, ghosts, shadows, CLI reference for Sui Move |
| `.github/agents/resources/certora-sui-move-templates.md` | Copy-paste CVLM spec patterns for Sui Move verification |
| `.github/agents/resources/sui-prover-reference.md` | Sui Prover spec API, math types, ghost variables, quantifiers, CLI, debugging |
| `.github/agents/resources/memory-state.md` | Mem0-inspired cross-cutting memory bus architecture for inter-agent knowledge sharing |

### All Agents

| Agent | File | Purpose |
|-------|------|---------|
| `audit-orchestrator` | `.github/agents/audit-orchestrator.md` | **Entry point** — orchestrates full audit pipeline |
| `audit-context-building` | `.github/agents/audit-context-building.md` | Line-by-line codebase analysis |
| `invariant-writer` | `.github/agents/invariant-writer.md` | Extracts all system invariants |
| `invariant-reviewer` | `.github/agents/invariant-reviewer.md` | Reviews & hardens invariants for multi-step coverage and FV readiness |
| `invariant-catcher` | `.github/agents/invariant-catcher.md` | Hunts for DB vulnerability patterns |
| `protocol-reasoning` | `.github/agents/protocol-reasoning.md` | Deep reasoning-based vulnerability discovery |
| `missing-validation-reasoning` | `.github/agents/missing-validation-reasoning.md` | Input validation scanner |
| `poc-writing` | `.github/agents/poc-writing.md` | Writes exploit tests using the target codebase's native test framework |
| `issue-writer` | `.github/agents/issue-writer.md` | Polishes findings for submission |
| `medusa-fuzzing` | `.github/agents/medusa-fuzzing.md` | Generates Medusa fuzzing harnesses |
| `certora-verification` | `.github/agents/certora-verification.md` | Generates Certora CVL specs |
| `halmos-verification` | `.github/agents/halmos-verification.md` | Generates Halmos symbolic test suites for Solidity formal verification |
| `certora-sui-move-verification` | `.github/agents/certora-sui-move-verification.md` | Generates Certora CVLM specs for Sui Move contracts |
| `sui-prover-verification` | `.github/agents/sui-prover-verification.md` | Generates Asymptotic Sui Prover specs for Sui Move contracts |
| `sherlock-judging` | `.github/agents/sherlock-judging.md` | Validates against Sherlock criteria |
| `cantina-judge` | `.github/agents/cantina-judge.md` | Validates against Cantina criteria |
| `code4rena-judge` | `.github/agents/code4rena-judge.md` | Validates against Code4rena criteria |
| `variant-template-writer` | `.github/agents/variant-template-writer.md` | Creates DB entries from reports |
| `solodit-fetching` | `.github/agents/solodit-fetching.md` | Fetches reports from Solodit API |
| `function-analyzer` | `.github/agents/function-analyzer.md` | Per-contract ultra-granular function analysis (spawned by audit-context-building) |
| `system-synthesizer` | `.github/agents/system-synthesizer.md` | Synthesizes per-contract context into global context document (spawned by audit-context-building) |
| `invariant-indexer` | `.github/agents/invariant-indexer.md` | Indexes canonical invariants from production DeFi protocols into per-category reference files for invariant-writer |
| `db-quality-monitor` | `.github/agents/db-quality-monitor.md` | Monitors full pipeline: 4-tier architecture integrity, manifest generation, hunt cards, script health, context delivery quality, and auto-fixes via sub-agents |
| `multi-persona-orchestrator` | `.github/agents/multi-persona-orchestrator.md` | Orchestrates 6 parallel auditing personas (BFS, DFS, Working Backward, State Machine, Mirror, Re-Implementation) with iterative knowledge sharing and cross-verification |
| `persona-bfs` | `.github/agents/persona-bfs.md` | BFS auditing persona — maps entry points then progressively deepens (spawned by multi-persona-orchestrator) |
| `persona-dfs` | `.github/agents/persona-dfs.md` | DFS auditing persona — verifies leaf functions then works upward (spawned by multi-persona-orchestrator) |
| `persona-working-backward` | `.github/agents/persona-working-backward.md` | Working Backward persona — traces from critical sinks to attacker-controllable sources (spawned by multi-persona-orchestrator) |
| `persona-state-machine` | `.github/agents/persona-state-machine.md` | State Machine persona — maps all protocol states and transitions to find illegal paths to bad states (spawned by multi-persona-orchestrator) |
| `persona-mirror` | `.github/agents/persona-mirror.md` | Mirror persona — analyzes paired/opposite functions for asymmetries (spawned by multi-persona-orchestrator) |
| `persona-reimplementer` | `.github/agents/persona-reimplementer.md` | Re-Implementation persona — hypothetically re-implements functions then diffs (spawned by multi-persona-orchestrator) |

