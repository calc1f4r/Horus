# Vulnerability Database — Codebase Structure

## Purpose

This repository is a comprehensive vulnerability pattern database for smart contract security audits. It aggregates findings from multiple audit firms into structured, searchable entries optimized for LLM-based code analysis and pattern matching.

---

## Directory Structure

```
vuln-database/
├── DB/                              # Main vulnerability database
│   ├── index.json                   # Master router — START HERE
│   ├── SEARCH_GUIDE.md              # Detailed search guide
│   ├── manifests/                   # Pattern-level indexes with line ranges
│   │   ├── oracle.json
│   │   ├── amm.json
│   │   ├── bridge.json
│   │   ├── tokens.json
│   │   ├── cosmos.json
│   │   ├── solana.json
│   │   ├── general-defi.json
│   │   ├── general-security.json
│   │   ├── general-infrastructure.json
│   │   ├── general-governance.json
│   │   ├── unique.json
│   │   ├── keywords.json
│   │   └── huntcards/               # Compressed detection cards (Tier 1.5)
│   │       ├── all-huntcards.json   # ALL 451+ cards in one file
│   │       └── *-huntcards.json     # Per-manifest cards
│   ├── oracle/                      # Oracle vulnerabilities
│   │   ├── chainlink/
│   │   ├── pyth/
│   │   └── price-manipulation/
│   ├── amm/                         # AMM vulnerabilities
│   │   ├── concentrated-liquidity/
│   │   └── constantproduct/
│   ├── bridge/                      # Cross-chain bridge vulnerabilities
│   │   ├── layerzero/
│   │   ├── wormhole/
│   │   ├── hyperlane/
│   │   ├── ccip/
│   │   ├── axelar/
│   │   ├── stargate/
│   │   └── custom/
│   ├── tokens/                      # Token standard vulnerabilities
│   │   └── erc20/
│   ├── cosmos/                      # Cosmos SDK / IBC vulnerabilities
│   │   ├── app-chain/
│   │   └── unique/
│   ├── Solona-chain-specific/       # Solana program vulnerabilities
│   ├── general/                     # General security patterns
│   │   ├── access-control/
│   │   ├── calculation/
│   │   ├── flash-loan/
│   │   ├── missing-validations/
│   │   ├── precision/
│   │   ├── proxy-vulnerabilities/
│   │   ├── reentrancy/
│   │   ├── signature/
│   │   ├── slippage-protection/
│   │   ├── stablecoin-vulnerabilities/
│   │   ├── storage-collision/
│   │   ├── token-compatibility/
│   │   ├── vault-inflation-attack/
│   │   └── [additional categories]/
│   └── unique/                      # Protocol-specific unique exploits
├── reports/                         # Raw audit findings (source data)
│   ├── chainlink_findings/
│   ├── pyth_findings/
│   ├── bridge_crosschain_findings/
│   ├── solana_findings/
│   └── [topic]_findings/
├── DeFiHackLabs/                    # Real-world exploit PoCs
├── Variant-analysis/                # Semgrep/CodeQL detection templates
│   ├── Methodology.md
│   ├── Skills.md
│   └── resources/
├── .github/agents/                  # 21 AI agent skill definitions
│   └── resources/                   # Agent reference materials
├── TEMPLATE.md                      # Canonical entry structure
├── Example.md                       # Reference implementation
├── Agents.md                        # Agent guidance document
├── CONTRIBUTING.md                  # Contribution guidelines
├── generate_manifests.py            # Manifest regeneration script
└── solodit_fetcher.py               # Solodit API fetcher
```

---

## Key Files

### DB/index.json — START HERE

**Purpose**: Lean router (~330 lines) that points agents to the right manifest files.

**Contains**:
- `protocolContext`: Maps protocol types (lending, DEX, vault, etc.) to relevant manifests and focus patterns
- `manifests`: Lists all 11 manifest files with descriptions and pattern counts
- `auditChecklist`: Quick security checks by category
- `keywordIndex`: Points to `DB/manifests/keywords.json` for keyword lookup

### 4-Tier Search Architecture

```
Tier 1:   DB/index.json                               ← Lean router. Start here.
   ↓
Tier 1.5: DB/manifests/huntcards/all-huntcards.json   ← 451+ compressed detection cards
   ↓                                                     with grep patterns & micro-directives
Tier 2:   DB/manifests/<name>.json                    ← Pattern-level indexes with line ranges
   ↓
Tier 3:   DB/**/*.md                                  ← Vulnerability content.
                                                          Read ONLY targeted line ranges.
```

**Usage**:
```
// By protocol type
DB/index.json → protocolContext.mappings.lending_protocol
  → manifests: ["oracle", "general-defi", "tokens", "general-security"]

// By keyword
DB/manifests/keywords.json → "getPriceUnsafe" → ["oracle"]
  → Load DB/manifests/oracle.json → find pattern → read targeted line ranges

// Bulk audit (hunt cards)
DB/manifests/huntcards/all-huntcards.json
  → grep target code per card.grep → prune zero-hit cards → shard → spawn sub-agents
```

For the full search guide, see `DB/SEARCH_GUIDE.md`.

### TEMPLATE.md

Defines the canonical structure for all vulnerability entries. Every new entry must follow this template for consistent vectorization and searchability.

### solodit_fetcher.py

Fetches vulnerabilities from the Solodit/Cyfrin database by keyword.

```bash
source .venv/bin/activate
python3 solodit_fetcher.py --keyword "pyth" --output ./reports/pyth_findings/
```

---

## Raw Findings (reports/)

The `reports/` directory contains **22,000+** raw audit findings that seed database entries. Each vulnerability entry in `DB/` references specific report files via relative paths like:

```
**Reference**: [fullmath-requires-overflow-behavior.md](../../../reports/constant_liquidity_amm/fullmath-requires-overflow-behavior.md)
```

**Naming convention**: `[severity]-[issue-number]-[description].md`
- Severity prefixes: `c-` (Critical), `h-` (High), `m-` (Medium), `l-` (Low)

### How Agents Should Fetch Reports

Reports are NOT included when cloning the main branch. Agents must fetch them on demand using the methods below, **always into a local `reports/` directory**.

#### Method 1: Fetch a Single Report File (Preferred — saves context)

When a DB entry references a specific report, extract the path and fetch just that file:

```bash
# 1. Parse the relative path from the DB entry:
#    ../../../reports/constant_liquidity_amm/fullmath-requires-overflow-behavior.md
#    → reports/constant_liquidity_amm/fullmath-requires-overflow-behavior.md

# 2. Create the local directory and fetch the file:
mkdir -p reports/constant_liquidity_amm
gh api "repos/calc1f4r/Vulnerability-database/contents/reports/constant_liquidity_amm/fullmath-requires-overflow-behavior.md?ref=hunt-cards" \
  --jq '.content' | base64 -d > reports/constant_liquidity_amm/fullmath-requires-overflow-behavior.md
```

#### Method 2: List Files in a Report Category

To discover what reports exist in a category before fetching:

```bash
# List all files in a report category
gh api "repos/calc1f4r/Vulnerability-database/contents/reports/constant_liquidity_amm?ref=hunt-cards" \
  --jq '.[].name'
```

#### Method 3: Clone an Entire Report Category (when you need many reports)

Each `reports/` subdirectory is automatically split into its own Git branch by the `split-reports.yml` workflow. Clone a category branch when you need bulk access:

```bash
# Clone all 508 concentrated liquidity AMM reports
mkdir -p reports
gh repo clone calc1f4r/Vulnerability-database reports/constant_liquidity_amm \
  -- --branch reports/constant_liquidity_amm --single-branch --depth 1
```

### Path Resolution for Agents

DB entries reference reports using relative paths from their location in `DB/`. To resolve:

```
DB entry location:   DB/amm/concentrated-liquidity/dos-arithmetic-initialization.md
Reference path:      ../../../reports/constant_liquidity_amm/fullmath-requires-overflow-behavior.md
Resolved to:         reports/constant_liquidity_amm/fullmath-requires-overflow-behavior.md
```

**Resolution rule**: Strip all leading `../` from the reference path. The result is always `reports/<category>/<file>.md`.

---

## Report Branches Reference

<!-- BEGIN REPORT_BRANCHES — auto-generated by update-codebase-structure.yml, do not edit manually -->
Each branch below contains **only** the reports for that category.

**Fetch a single file** (replace `<CATEGORY>` and `<FILE>`):
```bash
mkdir -p reports/<CATEGORY>
gh api "repos/calc1f4r/Vulnerability-database/contents/reports/<CATEGORY>/<FILE>?ref=hunt-cards" --jq '.content' | base64 -d > reports/<CATEGORY>/<FILE>
```

**Clone entire category** into `reports/`:
```bash
gh repo clone calc1f4r/Vulnerability-database reports/<CATEGORY> -- --branch reports/<BRANCH> --single-branch --depth 1
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

Each vulnerability entry in `DB/` follows:

```
DB/<category>/<subcategory>/<ENTRY>.md
```

Every `.md` entry contains:
- **YAML frontmatter** — metadata for indexing (title, tags, severity)
- **Overview** — vulnerability class description
- **Vulnerable pattern examples** — real code with severity tags
- **Secure implementation** — fixed code patterns
- **Detection patterns** — search queries for audits
- **Keywords** — terms for vector retrieval

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| [DB/index.json](DB/index.json) | Master router — agents start here |
| [DB/SEARCH_GUIDE.md](DB/SEARCH_GUIDE.md) | Detailed search guide |
| [TEMPLATE.md](TEMPLATE.md) | Entry structure specification |
| [Example.md](Example.md) | Reference implementation |
| [Agents.md](Agents.md) | Agent guidance |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |
