# AGENTS.md

This document gives agent models (like you) practical guidance for making safe, correct, and minimal changes in this repository. It captures project conventions, architecture, invariants, and how to run and extend tests.

## Scope & Goals

- Primary domain: Creation of Vulnerability database entries for smart contract security and blockchain appchains. 
- Core guarantees:
  - Making sure every vulnerability entry is well-structured, semantically rich, and optimized for vector search.
  - Ensuring consistency with existing entries and adherence to the provided template.

---

## 🔍 Quick Start: Using the Vulnerability Index

**Always start with `DB/index.json`** - this is your entry point for finding relevant vulnerability patterns.

### How to Use the Index

1. **Read the index first:**
   ```
   Load DB/index.json to understand available vulnerability categories and files
   ```

2. **Find files by keyword** (use `searchIndex`):
   ```json
   // Looking for chainlink vulnerabilities?
   searchIndex.mappings["chainlink"] → returns list of relevant files
   ```

3. **Find files by protocol context** (use `protocolContext`):
   ```json
   // Auditing a lending protocol?
   protocolContext.mappings["lending_protocol"] → returns priority files to read
   
   // Auditing a DEX/AMM?
   protocolContext.mappings["dex_amm"] → returns AMM-specific vulnerability files
   ```

4. **Browse by category** (use `categories`):
   ```json
   // Exploring oracle vulnerabilities?
   categories.oracle.subcategories → chainlink, pyth with their files
   ```

### Available Protocol Contexts

| Context | Use When Auditing |
|---------|-------------------|
| `lending_protocol` | Aave, Compound, lending/borrowing protocols |
| `dex_amm` | Uniswap, SushiSwap, decentralized exchanges |
| `vault_yield` | ERC4626 vaults, yield aggregators, strategies |
| `governance_dao` | DAOs, governance systems, voting contracts |
| `cross_chain` | Bridges, LayerZero, Wormhole integrations |
| `cosmos_appchain` | Cosmos SDK chains, IBC, app-chains |
| `solana_program` | Solana programs, Anchor, SPL tokens |
| `nft_marketplace` | NFT platforms, ERC721 marketplaces |

---

## Workflow for Vulnerability Discovery

```
1. Identify protocol type → Check protocolContext mappings
2. Search by keywords → Check searchIndex mappings  
3. Read category files → Deep dive into relevant categories
4. Check unique exploits → Review DB/unique/ for protocol-specific patterns
5. Apply patterns → Match against target codebase
```

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `DB/index.json` | **START HERE** - Index of all vulnerability files |
| `TEMPLATE.md` | Structure for new vulnerability entries |
| `Example.md` | Reference implementation of an entry |
| `CodebaseStructure.md` | Repository layout and organization |

