---
# Core Classification
protocol: Particle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60385
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/particle/3cd57a7b-681f-4f38-b0cd-9fd6f2f37a89/index.html
source_link: https://certificate.quantstamp.com/full/particle/3cd57a7b-681f-4f38-b0cd-9fd6f2f37a89/index.html
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Michael Boyle
  - Zeeshan Meghji
  - Faycal Lalidji
  - Gelei Deng
---

## Vulnerability Title

Malicious Nft Contract Can Repay Liens without Transfering Nft

### Overview


The client has reported a bug in the `ParticleExchange.sol` file. The function `onERC721Received()` can be called by both external accounts and smart contracts. However, if a smart contract calls the function without actually transferring the NFT, the Lien will still be considered repaid. The client recommends checking that the NFT is actually received before calling the `_execRepayWithNft()` function. This bug has been marked as "Fixed" by the client and the fix can be found in the `a6290e37e2ebde7397b8d8efdc505bda4cf3fd15` update.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `a6290e37e2ebde7397b8d8efdc505bda4cf3fd15`. The client provided the following explanation:

> Check NFT is received in the beginning of `onERC721Received` for the data branches

**File(s) affected:**`ParticleExchange.sol`

**Description:** The `onERC721Received()` function can be called by externally owned accounts and smart contracts alike. If an NFT contract is able to call `onERC721Received()` without actually transferring the NFT, the Lien will still be considered repaid.

**Recommendation:** Consider checking that the NFT in the Lien is actually received by the contract before calling `_execRepayWithNft()`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Particle |
| Report Date | N/A |
| Finders | Michael Boyle, Zeeshan Meghji, Faycal Lalidji, Gelei Deng |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/particle/3cd57a7b-681f-4f38-b0cd-9fd6f2f37a89/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/particle/3cd57a7b-681f-4f38-b0cd-9fd6f2f37a89/index.html

### Keywords for Search

`vulnerability`

