# AGENTS.md

This document gives agent models (like you) practical guidance for making safe, correct, and minimal changes in this repository. It captures project conventions, architecture, invariants, and how to run and extend tests.

## Scope & Goals

- Primary domain: Creation of Vulnerability database entries for smart contract security and blockchain appchains. 
- Core guarantees:
  - Making sure every vulnerability entry is well-structured, semantically rich, and optimized for vector search.
  - Ensuring consistency with existing entries and adherence to the provided template.

---

## Architecture: 3-Tier Search

The database uses a **tiered architecture** for precision. Never read entire vulnerability files — use manifests to find exact line ranges.

```
Tier 1: DB/index.json              ← Router (~330 lines). Start here.
   ↓  
Tier 2: DB/manifests/<name>.json   ← Pattern-level index with line ranges (11 manifests)
   ↓  
Tier 3: DB/**/*.md                 ← Vulnerability content. Read ONLY targeted line ranges.
```

For the full search guide, see `DB/SEARCH_GUIDE.md`.

---

## 🔍 Quick Start: Finding Vulnerability Patterns

### Step 1: Load the Router

Read `DB/index.json` (~330 lines). It contains:
- **`protocolContext`** — maps protocol types to relevant manifests + focus patterns
- **`manifests`** — lists all 11 manifest files with descriptions and pattern counts
- **`auditChecklist`** — quick security checks by category
- **`keywordIndex`** — points to `DB/manifests/keywords.json` for keyword search

### Step 2: Load the Right Manifest

Based on the protocol type or keyword, load 1-3 relevant manifests:

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

```
1. Identify protocol type → Read index.json protocolContext
2. Load relevant manifests (1-3) → Browse patterns by title/severity/keywords
3. Read exact line ranges → Get precise vulnerability content
4. Check unique exploits → Load DB/manifests/unique.json
5. Apply patterns → Match against target codebase
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
| `DB/index.json` | **START HERE** — Lean router to manifests |
| `DB/manifests/*.json` | Pattern-level indexes with line ranges |
| `DB/SEARCH_GUIDE.md` | Detailed search guide for agents |
| `TEMPLATE.md` | Structure for new vulnerability entries |
| `Example.md` | Reference implementation of an entry |
| `generate_manifests.py` | Re-generates manifests after DB changes |

