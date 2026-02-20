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
| `solana_program` | Solana programs, Anchor, SPL tokens |
| `perpetuals_derivatives` | Perpetual DEXes, options, derivatives |
| `token_launch` | Token launches, meme coins, trading contracts |
| `staking_liquid_staking` | Staking protocols, liquid staking |
| `nft_marketplace` | NFT platforms, ERC721 marketplaces |

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

The `audit-orchestrator` agent (`.github/agents/audit-orchestrator.md`) is the **primary entry point** for auditing an unfamiliar codebase. It takes a codebase path and an optional protocol hint, then runs a 7-phase pipeline using specialized sub-agents.

### Invocation

```
@audit-orchestrator <codebase-path> [protocol-hint]
```

### Pipeline

```
Phase 1: Reconnaissance      → Protocol detection, scope, manifest resolution
Phase 2: Context Building     → Sub-agent: audit-context-building
Phase 3: Invariant Extraction → Sub-agent: invariant-writer
Phase 4: DB-powered Hunting   → Self (grep-prune + partition + merge) + N × Sub-agent: invariant-catcher (parallel shards)
Phase 4a: Reasoning Discovery  → Sub-agent: protocol-reasoning-agent
Phase 5: Validation Gaps      → Sub-agent: missing-validation-reasoning
Phase 6: Triage & PoC         → Self + Sub-agent: poc-writing
Phase 7: Downstream Gen       → Sub-agents: medusa-fuzzing, certora-verification,
                                 sherlock-judging, cantina-judge
Final:   Report Assembly      → Produces audit-output/AUDIT-REPORT.md
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
         │                                     
         ▼                                     ┌──────────────────────┐
┌──────────────────┐                           │ protocol-reasoning-  │
│ invariant-writer │                           │ agent (spawns domain │
└────────┬─────────┘                           │ sub-agents)          │
         │                                     └──────────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────────┐
│ medusa │ │ certora  │
│ fuzzing│ │ verif.   │
└────────┘ └──────────┘

Post-triage:
  ├── poc-writing (per CRITICAL/HIGH finding)
  ├── issue-writer (polishes findings for submission)
  ├── sherlock-judging (severity validation)
  └── cantina-judge (severity validation)
```

### Data Pipeline Producers & Consumers

| Agent | Produces | Consumes |
|-------|----------|----------|
| `audit-orchestrator` | `00-scope.md`, `hunt-card-shards.json`, `03-findings-raw.md` (merged), `05-findings-triaged.md`, `AUDIT-REPORT.md` | All outputs |
| `audit-context-building` | `01-context.md` | Scope |
| `invariant-writer` | `02-invariants.md` | Context |
| `invariant-catcher` (×N shards) | `03-findings-shard-<id>.md` | Shard cards, invariants, target code |
| `protocol-reasoning-agent` | `04a-reasoning-findings.md` | Context, invariants, raw findings, manifests |
| `missing-validation-reasoning` | `04-validation-findings.md` | Context |
| `poc-writing` | `pocs/F-NNN-poc.t.sol` | Individual findings |
| `issue-writer` | Polished submission | Individual findings |
| `medusa-fuzzing` | `fuzzing/` harnesses | Invariant specs |
| `certora-verification` | `certora/` specs | Invariant specs |
| `sherlock-judging` | `06-sherlock-validation.md` | Triaged findings |
| `cantina-judge` | `07-cantina-validation.md` | Triaged findings |

### New Resource Files

| Resource | Purpose |
|----------|---------|
| `.github/agents/resources/inter-agent-data-format.md` | Standardized data contracts between pipeline phases |
| `.github/agents/resources/protocol-detection.md` | Auto-classification decision tree for codebases |
| `.github/agents/resources/audit-report-template.md` | Final report structure and quality checklist |
| `.github/agents/resources/orchestration-pipeline.md` | 7-phase pipeline with error handling and context budgets |
| `.github/agents/resources/reasoning-skills.md` | Core reasoning framework for deep vulnerability analysis |
| `.github/agents/resources/domain-decomposition.md` | Domain decomposition strategy for reasoning agent |

### All Agents

| Agent | File | Purpose |
|-------|------|---------|
| `audit-orchestrator` | `.github/agents/audit-orchestrator.md` | **Entry point** — orchestrates full audit pipeline |
| `audit-context-building` | `.github/agents/audit-context-building.md` | Line-by-line codebase analysis |
| `invariant-writer` | `.github/agents/invariant-writer-agent.md` | Extracts all system invariants |
| `invariant-catcher` | `.github/agents/invariant-catcher-agent.md` | Hunts for DB vulnerability patterns |
| `protocol-reasoning-agent` | `.github/agents/protocol-reasoning-agent.md` | Deep reasoning-based vulnerability discovery |
| `missing-validation-reasoning` | `.github/agents/missing-validation-reasoning-agent.md` | Input validation scanner |
| `poc-writing` | `.github/agents/poc-writer-agent.md` | Writes Foundry/Hardhat exploit tests |
| `issue-writer` | `.github/agents/issue-writer-agent.md` | Polishes findings for submission |
| `medusa-fuzzing` | `.github/agents/medusa-fuzzing-agent.md` | Generates Medusa fuzzing harnesses |
| `certora-verification` | `.github/agents/certora-verification-agent.md` | Generates Certora CVL specs |
| `sherlock-judging` | `.github/agents/sherlock-judge-agent.md` | Validates against Sherlock criteria |
| `cantina-judge` | `.github/agents/cantina-judge-agent.md` | Validates against Cantina criteria |
| `variant-template-writer` | `.github/agents/variant-template-writer.agent.md` | Creates DB entries from reports |
| `defihacklabs-indexer` | `.github/agents/defihacklabs-indexer.agent.md` | Indexes DeFiHackLabs exploits |
| `solodit-fetching` | `.github/agents/solodit-fetching-agent.md` | Fetches reports from Solodit API |

