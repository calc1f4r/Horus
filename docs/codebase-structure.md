# Horus — Codebase Structure

> Comprehensive reference for repository layout, data flow, and conventions. For search workflows, see [DB/SEARCH_GUIDE.md](../DB/SEARCH_GUIDE.md). For the broader system, see [agentic-workflow.md](agentic-workflow.md).

---

## Directory Layout

```
Horus/
│
├── DB/                                    # Core Horus knowledge base
│   ├── index.json                         #   Master router (Tier 1) — START HERE
│   ├── SEARCH_GUIDE.md                    #   Agent search workflows
│   │
│   ├── manifests/                         #   Pattern-level indexes (Tier 2)
│   │   ├── oracle.json                    #     107 patterns · 12 files
│   │   ├── amm.json                       #     148 patterns · 9 files
│   │   ├── bridge.json                    #     92 patterns · 10 files
│   │   ├── tokens.json                    #     47 patterns · 3 files
│   │   ├── cosmos.json                    #     416 patterns · 43 files
│   │   ├── solana.json                    #     68 patterns · 2 files
│   │   ├── sui-move.json                  #     304 patterns · 16 files
│   │   ├── general-defi.json              #     438 patterns · 46 files
│   │   ├── general-security.json          #     153 patterns · 15 files
│   │   ├── general-infrastructure.json    #     142 patterns · 14 files
│   │   ├── general-governance.json        #     118 patterns · 13 files
│   │   ├── unique.json                    #     121 patterns · 21 files
│   │   ├── account-abstraction.json       #     4 patterns · 4 files
│   │   ├── zk-rollup.json                #     100 patterns · 10 files
│   │   ├── keywords.json                  #     Keyword → manifest routing
│   │   └── huntcards/                     #   Compressed detection cards (Tier 1.5)
│   │       ├── all-huntcards.json         #     1,362 cards — all manifests combined
│   │       ├── oracle-huntcards.json      #     Per-manifest hunt cards
│   │       ├── amm-huntcards.json
│   │       ├── bridge-huntcards.json
│   │       ├── cosmos-huntcards.json
│   │       ├── general-defi-huntcards.json
│   │       ├── general-governance-huntcards.json
│   │       ├── general-infrastructure-huntcards.json
│   │       ├── general-security-huntcards.json
│   │       ├── solana-huntcards.json
│   │       ├── sui-move-huntcards.json
│   │       ├── tokens-huntcards.json
│   │       ├── unique-huntcards.json
│   │       ├── account-abstraction-huntcards.json
│   │       └── zk-rollup-huntcards.json
│   │
│   ├── graphify-out/                      #   Generated DB knowledge graph (Tier 2.5)
│   │   ├── graph.json                     #     5,270 nodes · 51,146 edges
│   │   ├── GRAPH_REPORT.md                #     Graph summary and central concepts
│   │   └── wiki/                          #     Curated agent-crawlable community pages
│   │
│   ├── oracle/                            #   Oracle vulnerabilities
│   │   ├── chainlink/                     #     Chainlink price feeds & aggregators
│   │   ├── pyth/                          #     Pyth Network oracle patterns
│   │   └── price-manipulation/            #     TWAP, spot price, flash loan manipulation
│   │
│   ├── amm/                               #   AMM vulnerabilities
│   │   ├── concentrated-liquidity/        #     Uniswap V3-style tick/range patterns
│   │   └── constantproduct/               #     Constant product AMM edge cases
│   │
│   ├── bridge/                            #   Cross-chain bridge vulnerabilities
│   │   ├── layerzero/                     #     LayerZero V1/V2 patterns
│   │   ├── wormhole/                      #     Wormhole message verification
│   │   ├── hyperlane/                     #     Hyperlane ISM/routing
│   │   ├── ccip/                          #     Chainlink CCIP integration
│   │   ├── axelar/                        #     Axelar GMP patterns
│   │   ├── stargate/                      #     Stargate/LayerZero finance
│   │   └── custom/                        #     Custom bridge implementations
│   │
│   ├── tokens/                            #   Token standard vulnerabilities
│   │   └── erc20/                         #     ERC20, ERC4626, ERC721 patterns
│   │
│   ├── cosmos/                            #   Cosmos SDK / IBC vulnerabilities
│   │   ├── app-chain/                     #     App-chain module patterns
│   │   └── unique/                        #     Cosmos-specific unique exploits
│   │
│   ├── Solana-chain-specific/             #   Solana program vulnerabilities
│   ├── Sui-Move-specific/                 #   Sui Move object model & DeFi logic
│   ├── account-abstraction/               #   ERC-4337, ERC-7579, paymasters, session keys
│   ├── zk-rollup/                         #   ZK circuits, fraud proofs, L1-L2 messaging
│   │
│   ├── general/                           #   Cross-cutting vulnerability patterns
│   │   ├── access-control/                #     Role-based, ownership, authorization
│   │   ├── arbitrary-call/                #     Arbitrary external call patterns
│   │   ├── bonding-curve/                 #     Bonding curve pricing logic
│   │   ├── bridge/                        #     Generic bridge patterns
│   │   ├── business-logic/                #     Protocol-specific logic flaws
│   │   ├── calculation/                   #     Arithmetic and accounting errors
│   │   ├── dao-governance-vulnerabilities/ #    DAO governance attack vectors
│   │   ├── diamond-proxy/                 #     EIP-2535 diamond proxy patterns
│   │   ├── erc7702-integration/           #     ERC-7702 delegation patterns
│   │   ├── fee-on-transfer-tokens/        #     Fee-on-transfer token handling
│   │   ├── flash-loan/                    #     Flash loan attack patterns & exploit scenarios
│   │   ├── initialization/                #     Initializer and constructor issues
│   │   ├── integer-overflow/              #     Integer overflow/underflow
│   │   ├── malicious/                     #     Rug pulls, backdoors, honeypots
│   │   ├── mev-bot/                       #     MEV extraction and sandwich attacks
│   │   ├── missing-validations/           #     Missing input/state validation
│   │   ├── precision/                     #     Rounding and precision loss
│   │   ├── proxy-vulnerabilities/         #     UUPS, Transparent, Beacon proxy issues
│   │   ├── randomness/                    #     On-chain randomness flaws
│   │   ├── reentrancy/                    #     Cross-function, cross-contract, read-only
│   │   ├── restaking/                     #     Liquid staking/restaking patterns
│   │   ├── rounding-precision-loss/       #     Rounding direction and truncation
│   │   ├── signature/                     #     Signature replay, malleability, EIP-712
│   │   ├── slippage-protection/           #     Slippage/deadline protection
│   │   ├── stablecoin-vulnerabilities/    #     Depeg, oracle reliance, redemption
│   │   ├── storage-collision/             #     Storage slot collision in proxies
│   │   ├── token-compatibility/           #     Non-standard token edge cases
│   │   ├── uups-proxy/                    #     UUPS-specific upgrade issues
│   │   ├── validation/                    #     General validation patterns
│   │   ├── vault-inflation-attack/        #     ERC4626 vault inflation/donation
│   │   └── yield-strategy-vulnerabilities/ #    Yield strategy accounting errors
│   │
│   └── unique/                            #   Protocol-specific real-world exploits
│       ├── amm/                           #     AMM-specific unique exploits
│       ├── defihacklabs/                  #     Exploits sourced from DeFiHackLabs
│       └── erc4626/                       #     ERC4626-specific unique exploits
│
├── reports/                               # Raw audit findings — 22,200+ across 49 categories
│   ├── chainlink_findings/                #   564 Chainlink oracle reports
│   ├── lending_borrowing_findings/        #   3,787 lending/borrowing reports
│   ├── yield_protocol_findings/           #   4,329 yield protocol reports
│   ├── erc721_nft_findings/               #   1,730 NFT reports
│   ├── erc4626_findings/                  #   1,324 vault reports
│   ├── stablecoin_findings/               #   1,535 stablecoin reports
│   ├── cosmos_cometbft_findings/          #   847 Cosmos/CometBFT reports
│   ├── missing_validations_findings/      #   827 validation reports
│   ├── bridge_crosschain_findings/        #   818 bridge reports
│   ├── lst_restaking_findings/            #   815 LST/restaking reports
│   └── ...                                #   (39 more categories)
│
├── DeFiHackLabs/                          # Real-world exploit PoCs (Git submodule)
│   ├── src/test/                          #   Foundry test cases for past exploits
│   └── ...
│
├── scripts/                               # Automation & utility scripts
│   ├── classify_and_group.py              #   Classify reports by vulnerability type
│   ├── generate_entries.py                #   Generate DB entries from reports
│   ├── generate_micro_directives.py       #   Generate hunt card micro-directives
│   ├── build_db_graph.py                  #   Build DB/graphify-out graph artifacts
│   ├── finalize_audit_graph.py            #   Finalize audit-time graphify output
│   ├── validate_retrieval_pipeline.py     #   Full retrieval/graph validation
│   ├── validate_codex_runtime.py          #   Generated runtime surface validation
│   ├── grep_prune.py                      #   Prune hunt cards by grep hits
│   ├── partition_shards.py                #   Partition cards into agent shards
│   ├── merge_shard_findings.py            #   Merge parallel shard findings
│   ├── db_quality_check.py                #   Validate DB integrity
│   ├── rebuild_report_artifacts.py        #   Rebuild report branch artifacts
│   ├── update_codebase_structure.py       #   Auto-update this file's branch table
│   └── ...                                #   additional utility scripts
│
├── .github/
│   ├── agents/                            # 38 generated GitHub-facing audit agents
│   │   ├── audit-orchestrator.md          #   Entry point — 11-phase pipeline
│   │   ├── audit-context-building.md      #   Line-by-line codebase analysis
│   │   ├── function-analyzer.md           #   Per-contract function analysis
│   │   ├── system-synthesizer.md          #   Global context synthesis
│   │   ├── invariant-writer.md            #   System invariant extraction
│   │   ├── invariant-reviewer.md          #   Invariant hardening for FV
│   │   ├── invariant-indexer.md           #   Canonical invariant indexing
│   │   ├── invariant-catcher.md           #   DB-powered pattern hunting
│   │   ├── protocol-reasoning.md          #   Deep reasoning-based discovery
│   │   ├── missing-validation-reasoning.md #  Input validation scanning
│   │   ├── multi-persona-orchestrator.md  #   6-persona parallel auditing
│   │   ├── persona-bfs.md                 #   BFS auditing approach
│   │   ├── persona-dfs.md                 #   DFS auditing approach
│   │   ├── persona-working-backward.md    #   Sink-to-source tracing
│   │   ├── persona-state-machine.md       #   State transition analysis
│   │   ├── persona-mirror.md              #   Symmetry/asymmetry detection
│   │   ├── persona-reimplementer.md       #   Re-implementation diffing
│   │   ├── poc-writing.md                 #   Compilable exploit test generation
│   │   ├── issue-writer.md                #   Finding polishing for submission
│   │   ├── variant-template-writer.md     #   Report → DB entry conversion
│   │   ├── solodit-fetching.md            #   Solodit/Cyfrin API fetching
│   │   ├── medusa-fuzzing.md              #   Medusa fuzzing harness generation
│   │   ├── certora-verification.md        #   Certora CVL spec generation
│   │   ├── halmos-verification.md         #   Halmos symbolic test generation
│   │   ├── certora-sui-move-verification.md # Certora CVLM for Sui Move
│   │   ├── sui-prover-verification.md     #   Sui Prover spec generation
│   │   ├── sherlock-judging.md            #   Sherlock severity validation
│   │   ├── cantina-judge.md               #   Cantina severity validation
│   │   ├── code4rena-judge.md             #   Code4rena severity validation
│   │   └── db-quality-monitor.md          #   DB health monitoring & auto-fix
│   │
│   └── agents/resources/                  # Resource parity mirror from .claude/resources
│       ├── audit-report-template.md       #   Final report structure template
│       ├── inter-agent-data-format.md     #   Standardized data contracts between phases
│       ├── protocol-detection.md          #   Auto-classification decision tree
│       ├── orchestration-pipeline.md      #   7-phase pipeline specification
│       ├── reasoning-skills.md            #   Core reasoning framework
│       ├── domain-decomposition.md        #   Domain decomposition strategy
│       ├── invariant-writing-guide.md     #   Invariant extraction methodology
│       ├── poc-templates.md               #   PoC code templates
│       ├── certora-reference.md           #   Certora CVL language reference
│       ├── medusa-reference.md            #   Medusa configuration reference
│       ├── sherlock-judging-criteria.md    #   Sherlock judging rules
│       ├── cantina-criteria.md            #   Cantina judging rules
│       ├── code4rena-judging-criteria.md  #   Code4rena judging rules
│       └── ...                            #   (21 more reference files)
│
├── TEMPLATE.md                            # Canonical vulnerability entry structure
├── Example.md                             # Reference implementation of an entry
├── docs/
│   ├── architecture.png                   #   Architecture diagram (PNG)
│   ├── architecture.excalidraw            #   Architecture diagram (editable)
│   ├── agentic-workflow.md                #   End-to-end system and workflow overview
│   ├── db-guide.md                        #   DB entry conventions & search workflows
│   └── codebase-structure.md              #   This file
├── CONTRIBUTING.md                        # Contribution guidelines
├── LICENSE                                # MIT License
└── README.md                              # Project overview and quick start
```

---

## 4-Tier Search Architecture

```
Tier 1    DB/index.json                            ← Lean router. ALWAYS start here.
   ↓
Tier 1.5  DB/manifests/huntcards/all-huntcards.json ← 1,362 compressed detection cards
   ↓                                                   with grep patterns & micro-directives
Tier 2    DB/manifests/<name>.json                  ← Full pattern-level indexes with line ranges
   ↓
Tier 2.5  DB/graphify-out/graph.json                ← Additive related-variant expansion
   ↓
Tier 3    DB/**/*.md                                ← Vulnerability content.
                                                       Read ONLY targeted line ranges.
```

### Search Workflows

**By protocol type:**
```
DB/index.json → protocolContext.mappings.lending_protocol
  → manifests: ["oracle", "general-defi", "tokens", "general-security"]
  → Load manifests → search patterns → read line ranges
```

**By keyword:**
```
DB/manifests/keywords.json → "getPriceUnsafe" → ["oracle"]
  → Load DB/manifests/oracle.json → find pattern → read targeted line ranges
```

**Bulk audit (hunt cards):**
```
DB/manifests/huntcards/all-huntcards.json
  → optional graph expansion → grep target code per card.grep → prune zero-hit cards → shard → spawn sub-agents
```

For the full search guide, see [DB/SEARCH_GUIDE.md](../DB/SEARCH_GUIDE.md).

---

## Key Files

| File | Purpose |
|------|---------|
| `DB/index.json` | Master router — protocol context, manifest listing, audit checklist, keyword index |
| `DB/manifests/huntcards/all-huntcards.json` | All 1,362 hunt cards — primary interface for bulk audits |
| `DB/manifests/<name>.json` | Per-category manifests with pattern IDs, titles, line ranges, severity, keywords |
| `DB/manifests/keywords.json` | Keyword → manifest routing for targeted lookup |
| `DB/graphify-out/graph.json` | Graphify-compatible DB graph for additive related-card expansion |
| `DB/graphify-out/GRAPH_REPORT.md` | Graph summary, community data, and central concepts |
| `DB/SEARCH_GUIDE.md` | Comprehensive search guide for agent consumption |
| `TEMPLATE.md` | Canonical structure for all vulnerability entries |
| `Example.md` | Reference implementation showing a complete entry |
| `docs/db-guide.md` | DB entry conventions, search workflows, audit mode |
| `scripts/generate_manifests.py` | Regenerates all manifests and hunt cards from DB content |
| `scripts/build_db_graph.py` | Rebuilds DB graph artifacts from manifests and hunt cards |
| `scripts/finalize_audit_graph.py` | Converts audit-time graphify output into queryable node-link JSON |
| `scripts/validate_retrieval_pipeline.py` | Runs the full retrieval, graph, sync, and finalizer validation suite |
| `scripts/solodit_fetcher.py` | Fetches vulnerability reports from the Solodit/Cyfrin API |

---

## Raw Findings (`reports/`)

The `reports/` directory contains **22,200+ raw audit findings** across 49 categories that serve as source data for DB entries. Each vulnerability entry in `DB/` can reference specific report files via relative paths.

### Naming Convention

```
[severity]-[issue-number]-[description].md
```

Severity prefixes: `c-` (Critical), `h-` (High), `m-` (Medium), `l-` (Low)

### How Agents Should Fetch Reports

Reports are not included when cloning the main branch. Agents fetch them on demand using one of three methods:

**Method 1 — Single file (preferred):**
```bash
mkdir -p reports/<CATEGORY>
gh api "repos/calc1f4r/Horus/contents/reports/<CATEGORY>/<FILE>?ref=hunt-cards" \
  --jq '.content' | base64 -d > reports/<CATEGORY>/<FILE>
```

**Method 2 — List files in a category:**
```bash
gh api "repos/calc1f4r/Horus/contents/reports/<CATEGORY>?ref=hunt-cards" \
  --jq '.[].name'
```

**Method 3 — Clone an entire category branch:**
```bash
gh repo clone calc1f4r/Horus reports/<CATEGORY> \
  -- --branch reports/<BRANCH> --single-branch --depth 1
```

### Path Resolution

DB entries reference reports using relative paths. To resolve:

```
DB entry:     DB/amm/concentrated-liquidity/dos-arithmetic.md
Reference:    ../../../reports/constant_liquidity_amm/fullmath-overflow.md
Resolved to:  reports/constant_liquidity_amm/fullmath-overflow.md
```

**Rule:** Strip all leading `../` from the reference path. The result is always `reports/<category>/<file>.md`.

---

## Report Branches Reference

<!-- BEGIN REPORT_BRANCHES — auto-generated by update-codebase-structure.yml, do not edit manually -->
Each branch below contains **only** the reports for that category.

**Fetch a single file** (replace `<CATEGORY>` and `<FILE>`):
```bash
mkdir -p reports/<CATEGORY>
gh api "repos/calc1f4r/Horus/contents/reports/<CATEGORY>/<FILE>?ref=hunt-cards" --jq '.content' | base64 -d > reports/<CATEGORY>/<FILE>
```

**Clone entire category** into `reports/`:
```bash
gh repo clone calc1f4r/Horus reports/<CATEGORY> -- --branch reports/<BRANCH> --single-branch --depth 1
```

| Branch | Source Directory (CATEGORY) | Reports |
|--------|---------------------------|---------|
| `reports/ZenithReports` | `ZenithReports` | 2 |
| `reports/access_control` | `access_control_findings` | 60 |
| `reports/account_abstraction` | `account_abstraction_findings` | 223 |
| `reports/airdrop_merkle` | `airdrop_merkle_findings` | 6 |
| `reports/arbitrary_call` | `arbitrary_call_findings` | 59 |
| `reports/bonding_curve` | `bonding_curve_findings` | 131 |
| `reports/bridge_crosschain` | `bridge_crosschain_findings` | 818 |
| `reports/chainlink` | `chainlink_findings` | 564 |
| `reports/constant_liquidity_amm` | `constant_liquidity_amm` | 508 |
| `reports/constant_product` | `constant_product` | 130 |
| `reports/cosmos_cometbft` | `cosmos_cometbft_findings` | 847 |
| `reports/dao_governance` | `dao_governance_findings` | 229 |
| `reports/dex_aggregator` | `dex_aggregator_findings` | 32 |
| `reports/diamond_proxy` | `diamond_proxy_findings` | 13 |
| `reports/eigenlayer` | `eigenlayer_findings` | 338 |
| `reports/erc20_token` | `erc20_token_findings` | 761 |
| `reports/erc4626` | `erc4626_findings` | 1324 |
| `reports/erc721_nft` | `erc721_nft_findings` | 1730 |
| `reports/erc7702` | `erc7702_findings` | 9 |
| `reports/fee_on_transfer` | `fee_on_transfer_findings` | 60 |
| `reports/flash_loan` | `flash_loan_findings` | 407 |
| `reports/initialization` | `initialization_findings` | 18 |
| `reports/integer_overflow` | `integer_overflow_findings` | 27 |
| `reports/keeper_automation` | `keeper_automation_findings` | 3 |
| `reports/lending_borrowing` | `lending_borrowing_findings` | 3787 |
| `reports/lending_rate_model` | `lending_rate_model_findings` | 20 |
| `reports/lst_restaking` | `lst_restaking_findings` | 815 |
| `reports/mev` | `mev_findings` | 20 |
| `reports/missing_validations` | `missing_validations_findings` | 827 |
| `reports/nft_marketplace` | `nft_marketplace_findings` | 59 |
| `reports/options` | `options_findings` | 5 |
| `reports/ottersec_move_audits` | `ottersec_move_audits` | 0 |
| `reports/perpetuals_derivatives` | `perpetuals_derivatives_findings` | 378 |
| `reports/price_manipulation` | `price_manipulation_findings` | 41 |
| `reports/proxy` | `proxy_findings` | 479 |
| `reports/pyth` | `pyth_findings` | 198 |
| `reports/randomness` | `randomness_findings` | 44 |
| `reports/reentrancy` | `reentrancy_findings` | 60 |
| `reports/signature` | `signature_findings` | 10 |
| `reports/slippage` | `slippage_findings` | 59 |
| `reports/solana` | `solana_findings` | 216 |
| `reports/stablecoin` | `stablecoin_findings` | 1535 |
| `reports/storage_collision` | `storage_collision_findings` | 14 |
| `reports/sui_move` | `sui_move_findings` | 70 |
| `reports/token2022` | `token2022_findings` | 77 |
| `reports/vault_inflation` | `vault_inflation_findings` | 60 |
| `reports/vetoken` | `vetoken_findings` | 377 |
| `reports/yield_protocol` | `yield_protocol_findings` | 4329 |
| `reports/zk_rollup` | `zk_rollup_findings` | 431 |

**Total: 49 branches · 22,210 reports**

> Report counts and branches are auto-updated by `update-codebase-structure.yml` on every push that modifies `reports/`.
<!-- END REPORT_BRANCHES -->

---

## Database Entry Structure

Each vulnerability entry follows the path convention:

```
DB/<category>/<subcategory>/<ENTRY>.md
```

Every `.md` entry contains:

| Section | Purpose |
|---------|---------|
| **YAML frontmatter** | Metadata for indexing — protocol, chain, category, severity, primitives, tags |
| **Overview** | 1–2 sentence summary of the vulnerability class |
| **Root Cause** | Fundamental issue: missing check, incorrect assumption, unhandled edge case |
| **Attack Scenario** | Step-by-step exploitation path |
| **Vulnerable Pattern Examples** | 3+ real code examples with severity tags and inline annotations |
| **Secure Implementation** | 2+ fixed code patterns showing the correct approach |
| **Detection Patterns** | Search queries and grep patterns for audit use |
| **Keywords** | 10+ terms optimized for vector retrieval |

See [TEMPLATE.md](../TEMPLATE.md) for the full specification and [Example.md](../Example.md) for a reference implementation.

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/generate_manifests.py` | Regenerates all manifests and hunt cards from DB/ content |
| `scripts/solodit_fetcher.py` | Fetches vulnerability reports from the Solodit/Cyfrin API |
| `scripts/classify_and_group.py` | Classifies raw reports by vulnerability type |
| `scripts/generate_entries.py` | Generates DB entries from classified reports |
| `scripts/generate_micro_directives.py` | Enriches hunt cards with micro-directives |
| `scripts/build_db_graph.py` | Rebuilds `DB/graphify-out/` from generated retrieval artifacts |
| `scripts/finalize_audit_graph.py` | Finalizes audit-time graphify output into queryable graph JSON |
| `scripts/grep_prune.py` | Prunes hunt cards based on grep hit results |
| `scripts/partition_shards.py` | Partitions surviving hunt cards into agent shards |
| `scripts/merge_shard_findings.py` | Merges findings from parallel shard agents |
| `scripts/db_quality_check.py` | Validates DB integrity (line ranges, references, structure) |
| `scripts/validate_retrieval_pipeline.py` | Validates tests, DB quality, graph queries, sync checks, and graph finalization |
| `scripts/validate_codex_runtime.py` | Validates generated Codex runtime surfaces and skill links |
| `scripts/rebuild_report_artifacts.py` | Rebuilds report branch artifacts |
| `scripts/update_codebase_structure.py` | Auto-updates the report branch table in this file |
| `scripts/extract_defihacklabs.py` | Extracts vulnerability patterns from DeFiHackLabs PoCs |
| `scripts/classify_cosmos.py` | Cosmos-specific report classification |
| `scripts/generate_cosmos_entries.py` | Generates Cosmos DB entries |
| `scripts/generate_cosmos_v2.py` | V2 Cosmos entry generator |
| `scripts/download_ottersec_move.py` | Downloads OtterSec Move audit reports |

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| [README.md](../README.md) | Project overview, runtime surfaces, and quick start |
| [agentic-workflow.md](agentic-workflow.md) | End-to-end architecture and workflow overview |
| [DB/index.json](../DB/index.json) | Master router — agents start here |
| [DB/SEARCH_GUIDE.md](../DB/SEARCH_GUIDE.md) | Detailed search workflows for agents |
| [TEMPLATE.md](../TEMPLATE.md) | Canonical entry structure specification |
| [Example.md](../Example.md) | Reference implementation of a complete entry |
| [docs/db-guide.md](db-guide.md) | DB entry conventions, search workflows, audit mode |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Contribution guidelines and quality checklist |
