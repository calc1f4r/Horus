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

## Raw Findings Structure

The `reports/` directory contains raw audit findings that seed database entries:

```
reports/<topic>_findings/
├── m-01-missing-staleness-check-in-pythoracle.md
├── h-02-price-manipulation-via-flash-loan.md
└── [additional reports].md
```

**Naming convention**: `[severity]-[issue-number]-[description].md`

**Automated Category Branches**: 
A GitHub Actions workflow (`split-reports.yml`) automatically isolates each subdirectory in the `reports/` folder into its own Git branch (e.g., `reports/<topic>`). This allows agents and users to clone just the reports they need for specific domains using:
```bash
git clone -b reports/<topic> --single-branch https://github.com/calc1f4r/Vulnerability-database.git
```
- Severity prefixes: `c-` (Critical), `h-` (High), `m-` (Medium), `l-` (Low)

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
