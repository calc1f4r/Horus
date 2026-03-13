<div align="center">

# Vulnerability Database

**A production-grade, agent-optimized vulnerability pattern database for smart contract security auditing.**

1,674 vulnerability patterns from real-world audits and on-chain exploits, structured into a tiered search system built for LLM-powered audit agents — spanning EVM, Solana, Cosmos, Sui Move, and ZK Rollup ecosystems.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Patterns](https://img.shields.io/badge/patterns-1%2C674-brightgreen)](DB/manifests)
[![Manifests](https://img.shields.io/badge/manifests-14-orange)](DB/manifests)
[![Hunt Cards](https://img.shields.io/badge/hunt%20cards-1%2C267-red)](DB/manifests/huntcards)
[![Agents](https://img.shields.io/badge/agents-30-blueviolet)](.github/agents)
[![Reports](https://img.shields.io/badge/raw%20reports-22%2C200%2B-yellow)](reports)

</div>

---

## Overview

The Vulnerability Database is a curated knowledge base purpose-built for AI-assisted smart contract auditing. Rather than storing flat lists of findings, it uses a **4-tier precision architecture** that lets agents load only the context they need — reducing token usage by 60–80% compared to naive full-file reads.

The database ships with a **30-agent audit pipeline** that can take an unfamiliar codebase from zero to a triaged report with PoCs, fuzzing harnesses, formal verification specs, and multi-platform severity validation — all powered by the patterns stored here.

### Key Numbers

| Metric | Count |
|--------|-------|
| Vulnerability patterns | 1,674 |
| Hunt cards (compressed detection cards) | 1,267 |
| Manifests (category indexes) | 14 |
| DB content files | 214 |
| Raw source reports | 22,200+ |
| Specialized audit agents | 30 |
| Supported ecosystems | EVM, Solana, Cosmos, Sui Move, ZK Rollups |

---

## 4-Tier Search Architecture

```
Tier 1    DB/index.json                            ← Lean router. ALWAYS start here.
   ↓
Tier 1.5  DB/manifests/huntcards/all-huntcards.json ← 1,267 compressed detection cards
   ↓                                                   with grep patterns & micro-directives
Tier 2    DB/manifests/<name>.json                  ← Full pattern index with line ranges
   ↓
Tier 3    DB/**/*.md                                ← Vulnerability content.
                                                       Read ONLY targeted line ranges.
```

**Why it matters:** An agent auditing a lending protocol loads ~3 manifests (~2K patterns) instead of reading all 214 files. Hunt cards compress those patterns further into grep-first detection cards, letting agents scan a full codebase in a single pass and only read detailed content for confirmed hits.

### Hunt Cards (Tier 1.5)

Hunt cards are the primary interface for bulk auditing. Each card contains:

| Field | Purpose |
|-------|---------|
| `grep` | Regex pattern to search target code |
| `detect` | One-line description of the root cause |
| `check` | Micro-directives — exact steps to verify on a grep hit |
| `antipattern` | The vulnerable code pattern |
| `securePattern` | The correct implementation |
| `neverPrune` | `true` for CRITICAL patterns that always survive pruning |
| `ref` + `lines` | Pointer to the full `.md` entry for confirmed positives |

---

## Vulnerability Coverage

| Manifest | Patterns | Files | Focus |
|---|---|---|---|
| `cosmos` | 374 | 43 | Cosmos SDK, IBC, staking, CometBFT, app-chain invariants |
| `general-defi` | 319 | 43 | Flash loans, vaults, slippage, precision, calculations, yield |
| `sui-move` | 243 | 17 | Sui Move object model, access control, DeFi logic, bridges |
| `zk-rollup` | 100 | 10 | Circuit constraints, fraud proofs, sequencer, L1-L2 messaging |
| `general-security` | 93 | 15 | Access control, signatures, input validation, initialization |
| `general-infrastructure` | 85 | 14 | Proxies, reentrancy, storage collision, upgrades |
| `oracle` | 84 | 12 | Chainlink, Pyth, price manipulation, staleness |
| `bridge` | 82 | 10 | LayerZero, Wormhole, Hyperlane, CCIP, Axelar, Stargate |
| `unique` | 79 | 21 | Protocol-specific exploits from real-world incidents |
| `general-governance` | 71 | 11 | DAOs, stablecoins, MEV, randomness, malicious patterns |
| `amm` | 67 | 9 | Concentrated liquidity, constant product, sandwich attacks |
| `solana` | 40 | 2 | Solana programs, Anchor, Token-2022, SPL |
| `tokens` | 33 | 3 | ERC20, ERC4626, ERC721, token compatibility |
| `account-abstraction` | 4 | 4 | ERC-4337, ERC-7579, paymasters, session keys |
| **Total** | **1,674** | **214** | |

---

## Protocol-to-Manifest Routing

The `protocolContext` section of `DB/index.json` maps protocol types to the manifests an agent should load. This eliminates guesswork and ensures relevant coverage.

| Auditing | Load These Manifests |
|---|---|
| Lending / Borrowing | `oracle`, `general-defi`, `tokens`, `general-security` |
| DEX / AMM | `amm`, `general-defi`, `oracle` |
| Vaults / Yield (ERC4626) | `tokens`, `general-defi`, `general-infrastructure` |
| Governance / DAO | `general-governance`, `general-security` |
| Cross-chain Bridges | `bridge`, `general-infrastructure`, `general-security` |
| Cosmos App-chains | `cosmos`, `general-security` |
| Solana Programs | `solana`, `general-security` |
| Sui Move Contracts | `sui-move`, `general-security` |
| Perpetuals / Derivatives | `oracle`, `general-defi`, `amm` |
| Staking / Liquid Staking | `tokens`, `general-defi`, `general-governance` |
| ZK Rollups | `zk-rollup`, `general-infrastructure`, `general-security` |
| Token Launches | `tokens`, `general-defi`, `general-governance` |

---

## Agent Ecosystem

The `.github/agents/` directory contains **30 specialized agents** organized into a multi-phase audit pipeline with parallel execution, multi-persona reasoning, and downstream formal verification.

### Entry Point

```
@audit-orchestrator <codebase-path> [protocol-hint]
```

### Pipeline

```
Phase 1  Reconnaissance        → Protocol detection, scope, manifest resolution
Phase 2  Context Building      → audit-context-building → function-analyzer (per contract)
                                  → system-synthesizer (global context)
Phase 3  Invariant Extraction  → invariant-writer → invariant-reviewer
Phase 4  DB-Powered Hunting    → N × invariant-catcher (parallel shards)
Phase 4a Reasoning Discovery   → protocol-reasoning (domain decomposition + sub-agents)
         Multi-Persona Audit   → multi-persona-orchestrator
                                  → 6 parallel personas (BFS, DFS, Working Backward,
                                     State Machine, Mirror, Re-Implementation)
Phase 5  Validation Gaps       → missing-validation-reasoning
Phase 6  Triage & PoC          → poc-writing → issue-writer
Phase 7  Downstream Generation → medusa-fuzzing, certora-verification, halmos-verification,
                                  certora-sui-move-verification, sui-prover-verification
         Severity Validation   → sherlock-judging, cantina-judge, code4rena-judge
```

### Agent Reference

<details>
<summary><strong>Orchestration & Context (5 agents)</strong></summary>

| Agent | Role |
|---|---|
| `audit-orchestrator` | Entry point — orchestrates the full 7-phase pipeline |
| `audit-context-building` | Coordinates per-contract analysis; spawns function-analyzer + system-synthesizer |
| `function-analyzer` | Ultra-granular line-by-line function analysis for a single contract |
| `system-synthesizer` | Synthesizes per-contract outputs into a unified global context document |
| `db-quality-monitor` | Monitors 4-tier architecture integrity, manifest health, and auto-remediates |

</details>

<details>
<summary><strong>Invariant & Property Extraction (3 agents)</strong></summary>

| Agent | Role |
|---|---|
| `invariant-writer` | Dual-mode extraction: "What Should Happen" + "What Must Never Happen" |
| `invariant-reviewer` | Reviews and hardens invariants for formal verification readiness |
| `invariant-indexer` | Indexes canonical invariants from production DeFi protocols |

</details>

<details>
<summary><strong>Vulnerability Hunting (4 agents)</strong></summary>

| Agent | Role |
|---|---|
| `invariant-catcher` | Hunts DB patterns against target code in parallel shards |
| `protocol-reasoning` | Deep reasoning-based discovery with domain decomposition |
| `missing-validation-reasoning` | Input validation and hygiene scanner |
| `multi-persona-orchestrator` | Coordinates 6 parallel auditing personas with cross-verification |

</details>

<details>
<summary><strong>Multi-Persona Auditors (6 agents)</strong></summary>

| Agent | Approach |
|---|---|
| `persona-bfs` | Maps entry points, then progressively deepens |
| `persona-dfs` | Verifies leaf functions, then works upward |
| `persona-working-backward` | Traces from critical sinks to attacker-controllable sources |
| `persona-state-machine` | Maps all protocol states and transitions for illegal paths |
| `persona-mirror` | Analyzes paired/opposite functions for asymmetries |
| `persona-reimplementer` | Re-implements functions hypothetically, then diffs |

</details>

<details>
<summary><strong>Output & Reporting (3 agents)</strong></summary>

| Agent | Role |
|---|---|
| `poc-writing` | Writes compilable exploit tests (Foundry, Hardhat, Anchor, etc.) |
| `issue-writer` | Polishes findings into submission-ready write-ups |
| `variant-template-writer` | Converts audit reports into TEMPLATE.md-compliant DB entries |

</details>

<details>
<summary><strong>Formal Verification (5 agents)</strong></summary>

| Agent | Role |
|---|---|
| `medusa-fuzzing` | Generates Medusa-compatible property test harnesses |
| `certora-verification` | Generates Certora CVL formal specs + Gambit mutation configs |
| `halmos-verification` | Generates Halmos symbolic test suites for Foundry |
| `certora-sui-move-verification` | Generates Certora CVLM specs for Sui Move |
| `sui-prover-verification` | Generates Asymptotic Sui Prover specs for Sui Move |

</details>

<details>
<summary><strong>Severity Validation (3 agents)</strong></summary>

| Agent | Role |
|---|---|
| `sherlock-judging` | Validates findings against Sherlock audit platform criteria |
| `cantina-judge` | Validates findings against Cantina severity matrix |
| `code4rena-judge` | Validates findings against Code4rena competition standards |

</details>

<details>
<summary><strong>Data Collection (1 agent)</strong></summary>

| Agent | Role |
|---|---|
| `solodit-fetching` | Fetches raw findings from the Solodit/Cyfrin API |

</details>

---

## Searching the Database

### By Protocol Type (Most Common)

```
1. Read DB/index.json → protocolContext.mappings.<protocol_type>
2. Load the listed manifests (1-3 typically)
3. Browse patterns by title / severity / codeKeywords
4. Read targeted line ranges from the .md files
```

### By Keyword

```
1. Read DB/manifests/keywords.json → find your keyword
2. Follow the pointer to the relevant manifest
3. Find the pattern entry → read only lineStart–lineEnd
```

### Bulk Audit (Recommended for Full Audits)

```
1. Load DB/manifests/huntcards/all-huntcards.json (1,267 cards)
2. grep target code for each card.grep pattern
3. Cards with neverPrune: true always survive regardless of grep hits
4. Prune cards with zero hits → typically removes 60-80%
5. Partition surviving cards into shards of 50-80
6. Spawn one invariant-catcher sub-agent per shard (parallel)
7. Merge shard findings → deduplicate by root cause
```

---

## Repository Structure

```
Vulnerability-database/
├── DB/                               # Vulnerability database (214 files, 1,674 patterns)
│   ├── index.json                    #   Master router — START HERE
│   ├── SEARCH_GUIDE.md               #   Detailed agent search guide
│   ├── manifests/                    #   14 pattern-level indexes + keywords
│   │   ├── huntcards/                #   1,267 compressed detection cards
│   │   │   ├── all-huntcards.json    #     All cards in one file
│   │   │   └── *-huntcards.json      #     Per-manifest cards (15 files)
│   │   ├── *.json                    #     Category manifests with line ranges
│   │   └── keywords.json             #     Keyword → manifest routing
│   ├── oracle/                       #   Chainlink, Pyth, price manipulation
│   ├── amm/                          #   Concentrated liquidity, constant product
│   ├── bridge/                       #   LayerZero, Wormhole, Hyperlane, CCIP, Axelar
│   ├── tokens/                       #   ERC20, ERC4626, ERC721
│   ├── cosmos/                       #   Cosmos SDK, IBC, CometBFT, app-chains
│   ├── Solona-chain-specific/        #   Solana programs, Token-2022
│   ├── Sui-Move-specific/            #   Sui Move object model, DeFi, bridges
│   ├── account-abstraction/          #   ERC-4337, ERC-7579, paymasters
│   ├── zk-rollup/                    #   ZK circuits, fraud proofs, sequencers
│   ├── general/                      #   Access control, reentrancy, proxies, DeFi, governance
│   └── unique/                       #   Protocol-specific real-world exploits
│
├── reports/                          # 22,200+ raw audit findings (49 categories)
├── DeFiHackLabs/                     # Real-world exploit PoCs (submodule)
├── scripts/                          # Automation and utility scripts (15 files)
│
├── .github/agents/                   # 30 specialized audit agents
│   └── resources/                    #   Agent reference materials (34 files)
│
├── TEMPLATE.md                       # Canonical DB entry structure
├── Example.md                        # Reference implementation of an entry
├── Agents.md                         # Agent guidance & workflow documentation
├── CodebaseStructure.md              # Detailed codebase structure reference
├── CONTRIBUTING.md                   # Contribution guidelines
├── generate_manifests.py             # Regenerates manifests + hunt cards
└── solodit_fetcher.py                # Solodit/Cyfrin API fetcher
```

---

## Targeted Access via Category Branches

Raw reports are split into per-category Git branches by a GitHub Actions workflow, so agents and users can clone exactly the data they need without pulling the full 22K+ report corpus.

```bash
# Clone a single report category
git clone -b reports/<topic> --single-branch \
  https://github.com/calc1f4r/Vulnerability-database.git

# Example: ERC4626 vault reports only
git clone -b reports/erc4626 --single-branch \
  https://github.com/calc1f4r/Vulnerability-database.git
```

See [CodebaseStructure.md](CodebaseStructure.md) for the full branch-to-category mapping and report fetch methods.

---

## Getting Started

### Adding New Entries

```bash
# 1. Fetch raw findings from Solodit
python3 solodit_fetcher.py --keyword "<topic>" --output ./reports/<topic>_findings/

# 2. Use variant-template-writer agent to synthesize findings into DB entries
@variant-template-writer <topic>

# 3. Regenerate all manifests and hunt cards
python3 generate_manifests.py
```

### Running a Full Audit

```bash
# Point the orchestrator at any smart contract codebase
@audit-orchestrator /path/to/contracts [lending_protocol]
```

The orchestrator auto-detects the protocol type, resolves the relevant manifests, and runs the full 7-phase pipeline.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding vulnerability entries, improving agents, and maintaining database quality.

---

## License

MIT — see [LICENSE](LICENSE) for details.
