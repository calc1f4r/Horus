<div align="center">

# Vulnerability Database

**A production-grade, agent-optimized vulnerability pattern database for smart contract security.**

Aggregates 815+ vulnerability patterns from real-world audits and on-chain exploits into a structured, tiered search system built for LLM-powered audit agents — covering EVM, Solana, and Cosmos ecosystems.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Patterns](https://img.shields.io/badge/patterns-815%2B-brightgreen)](DB/manifests)
[![Manifests](https://img.shields.io/badge/manifests-11-orange)](DB/manifests)
[![Hunt Cards](https://img.shields.io/badge/hunt%20cards-451%2B-red)](DB/manifests/huntcards)

</div>

---

## Overview

The Vulnerability Database is a curated knowledge base purpose-built for AI-assisted smart contract auditing. Rather than storing flat lists of findings, it uses a **4-tier precision architecture** that lets agents load only the context they need — reducing token usage by 60–80% compared to naive full-file reads.

The database ships with a **21-agent audit pipeline** that can take an unfamiliar codebase from zero to a triaged report with PoCs, fuzzing harnesses, and formal verification specs — all powered by the patterns stored here.

![Architecture diagram showing the full 4-tier search system and agent pipeline](./Architecture.png)

---

## 4-Tier Search Architecture

```
Tier 1    DB/index.json                            ← Lean router. ALWAYS start here.
   ↓
Tier 1.5  DB/manifests/huntcards/all-huntcards.json ← 451+ compressed detection cards
   ↓                                                   with grep patterns & micro-directives
Tier 2    DB/manifests/<name>.json                  ← Full pattern index with line ranges
   ↓
Tier 3    DB/**/*.md                                ← Vulnerability content.
                                                       Read ONLY targeted line ranges.
```

**Hunt Cards (Tier 1.5)** are the primary interface for bulk auditing. Each card contains:
- `grep` — regex pattern to search target code
- `detect` — one-line description of the root cause
- `check` — micro-directives: exact steps to verify on a grep hit
- `antipattern` — the vulnerable code pattern
- `securePattern` — the correct implementation
- `neverPrune` — `true` for CRITICAL patterns that always survive pruning
- `ref` + `lines` — pointer to the full `.md` entry for confirmed positives

---

## Vulnerability Coverage

| Manifest | Patterns | Files | Focus |
|---|---|---|---|
| `oracle` | 78 | 11 | Chainlink, Pyth, price manipulation, staleness |
| `general-defi` | 199 | 24 | Flash loans, vaults, slippage, precision, calculations |
| `general-security` | 87 | 14 | Access control, signatures, input validation, initialization |
| `general-infrastructure` | 85 | 14 | Proxies, reentrancy, storage collision, upgrades |
| `general-governance` | 71 | 11 | DAOs, stablecoins, MEV, randomness, malicious patterns |
| `unique` | 79 | 21 | Protocol-specific exploits from real-world incidents |
| `amm` | 67 | 9 | Concentrated liquidity, constant product, sandwich attacks |
| `bridge` | 49 | 7 | LayerZero, Wormhole, Hyperlane, custom cross-chain |
| `solana` | 40 | 2 | Solana programs, Anchor, Token-2022, SPL |
| `tokens` | 33 | 3 | ERC20, ERC4626, ERC721, token compatibility |
| `cosmos` | 27 | 14 | Cosmos SDK, IBC, staking, app-chain invariants |
| **Total** | **815+** | **130** | |

---

## Protocol-to-Manifest Mapping

| Auditing | Load these manifests |
|---|---|
| Lending / Borrowing (Aave, Compound) | `oracle`, `general-defi`, `tokens`, `general-security` |
| DEX / AMM (Uniswap, Curve) | `amm`, `general-defi`, `oracle` |
| Vaults / Yield (ERC4626) | `tokens`, `general-defi`, `general-infrastructure` |
| Governance / DAO | `general-governance`, `general-security` |
| Cross-chain Bridges | `bridge`, `general-infrastructure`, `general-security` |
| Cosmos App-chains | `cosmos`, `general-security` |
| Solana Programs | `solana`, `general-security` |
| Perpetuals / Derivatives | `oracle`, `general-defi`, `amm` |
| Staking / Liquid Staking | `tokens`, `general-defi`, `general-governance` |

---

## Agent Ecosystem

The `.github/agents/` directory contains 21 specialized agents that form a complete audit pipeline.

### Entry Point

```
@audit-orchestrator <codebase-path> [protocol-hint]
```

The `audit-orchestrator` runs a 7-phase pipeline, spawning sub-agents in parallel:

```
Phase 1  Reconnaissance       → Protocol detection, scope, manifest resolution
Phase 2  Context Building     → audit-context-building
Phase 3  Invariant Extraction → invariant-writer
Phase 4  DB-powered Hunting   → N × invariant-catcher (parallel shards)
Phase 4a Reasoning Discovery  → protocol-reasoning
Phase 5  Validation Gaps      → missing-validation-reasoning
Phase 6  Triage & PoC         → poc-writing
Phase 7  Downstream           → medusa-fuzzing, certora-verification,
                                 sherlock-judging, cantina-judge
```

### All Agents

| Agent | Role |
|---|---|
| `audit-orchestrator` | Entry point — orchestrates all 7 phases |
| `audit-context-building` | Line-by-line codebase comprehension; spawns sub-agents |
| `function-analyzer` | Per-contract ultra-granular function analysis (sub-agent) |
| `system-synthesizer` | Synthesizes per-contract files into global context (sub-agent) |
| `invariant-writer` | Extracts all system invariants |
| `invariant-reviewer` | Reviews & hardens invariants for FV readiness |
| `invariant-catcher` | Hunts DB patterns against target code (parallel shards) |
| `protocol-reasoning` | Deep reasoning-based vulnerability discovery |
| `missing-validation-reasoning` | Input validation scanner |
| `poc-writing` | Writes compilable Foundry/Hardhat exploit tests |
| `issue-writer` | Polishes findings into Sherlock-format submissions |
| `medusa-fuzzing` | Generates Medusa fuzzing harnesses |
| `certora-verification` | Generates Certora CVL formal specs |
| `certora-sui-move-verification` | Generates Certora CVLM specs for Sui Move contracts |
| `sui-prover-verification` | Generates Asymptotic Sui Prover specs for Sui Move |
| `sherlock-judging` | Validates findings against Sherlock severity criteria |
| `cantina-judge` | Validates findings against Cantina severity criteria |
| `code4rena-judge` | Validates findings against Code4rena severity criteria |
| `variant-template-writer` | Converts audit reports into DB entries |
| `solodit-fetching` | Fetches raw findings from the Solodit/Cyfrin API |
| `db-quality-monitor` | Monitors 4-tier architecture integrity, manifest health, and auto-fixes |

---

## Searching the Database

### By Protocol Type

```
1. Read DB/index.json → protocolContext.mappings.<type>
2. Load the listed manifests
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
1. Load DB/manifests/huntcards/all-huntcards.json  (~55K tokens for all 451+ cards)
2. grep target code for each card.grep pattern
3. Cards with neverPrune: true always kept regardless of grep hits
4. Prune cards with zero hits  →  removes ~60-80% of cards
5. Partition surviving cards into shards of 50-80
6. Spawn one invariant-catcher sub-agent per shard (parallel)
7. Merge shard findings  →  03-findings-raw.md
```

---

## Repository Structure

```
Vulnerability-database/
├── DB/
│   ├── index.json                    # Master router — START HERE
│   ├── SEARCH_GUIDE.md               # Full search guide for agents
│   ├── manifests/
│   │   ├── *.json                    # 11 pattern-level manifest indexes
│   │   ├── keywords.json             # Keyword → manifest routing
│   │   └── huntcards/
│   │       ├── all-huntcards.json    # ALL 451+ hunt cards in one file
│   │       └── *-huntcards.json      # Per-manifest hunt cards
│   ├── oracle/                       # Chainlink, Pyth, price manipulation
│   ├── amm/                          # Concentrated liquidity, constant product
│   ├── bridge/                       # LayerZero, Wormhole, Hyperlane, custom
│   ├── tokens/                       # ERC20, ERC4626, ERC721
│   ├── cosmos/                       # Cosmos SDK, IBC, app-chains
│   ├── Solona-chain-specific/        # Solana programs, Token-2022
│   ├── general/                      # Access control, reentrancy, proxies, DeFi
│   └── unique/                       # Protocol-specific real-world exploits
├── reports/                          # Raw audit findings and source data
├── .github/
│   └── agents/                       # 13 audit agent skill definitions
│       └── resources/                # Agent reference materials
├── DeFiHackLabs/                     # Real-world exploit PoCs (submodule)
├── TEMPLATE.md                       # Canonical DB entry structure
├── Example.md                        # Reference implementation of an entry
├── Agents.md                         # Agent guidance & workflow documentation
├── CodebaseStructure.md              # Repository structure reference
└── CONTRIBUTING.md                   # Contribution guidelines
```

---

## ⚡ Targeted Access via Category Branches

To preserve API context length and simplify fetching raw vulnerability reporting data, our `reports/` directory is automatically split. A GitHub Actions workflow isolates each subdirectory in the `reports/` folder into its own dedicated Git branch. This allows you to clone exactly the domains you need without fetching the entire history:

```bash
# General syntax:
git clone -b reports/<topic> --single-branch https://github.com/calc1f4r/Vulnerability-database.git

# Example: Fetching only ERC4626 vault audit reports
git clone -b reports/erc4626 --single-branch https://github.com/calc1f4r/Vulnerability-database.git
```

---

## Adding New Entries

```bash
# 1. Fetch raw findings from Solodit
python3 solodit_fetcher.py --keyword "<topic>" --output ./reports/<topic>_findings/

# 2. Use variant-template-writer agent to synthesize findings into DB entries
#    following TEMPLATE.md

# 3. Regenerate all manifests and hunt cards
python3 generate_manifests.py
```

See [TEMPLATE.md](TEMPLATE.md) for the canonical entry structure and [Example.md](Example.md) for a reference implementation.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding vulnerability entries, improving detection agents, and maintaining the database quality.

---

## License

MIT — see [LICENSE](LICENSE) for details.
