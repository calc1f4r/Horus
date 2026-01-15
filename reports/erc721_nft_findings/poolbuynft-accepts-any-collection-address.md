---
# Core Classification
protocol: Nemeos
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59588
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
source_link: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Sebastian Banescu
  - Faycal Lalidji
  - Guillermo Escobero
---

## Vulnerability Title

`Pool.buyNFT()` Accepts Any Collection Address

### Overview


This bug report discusses a problem with the code in `Pool.sol` that has been fixed in two specific versions. The issue was reported by the Nemeos team before the security review began. The problem is that `Pool.buyNFT()` accepts `collectionAddress_` as a parameter, which could potentially allow borrowers to buy NFTs from other collections using the pool's funds. The recommendation is to remove the `collectionAddress_` parameter from `buyNFT()` and use the fixed value set in `initialize()`, called `nftCollection`, instead.

### Original Finding Content

**Update**
Fixed in `cf9ac5d632c0c35c9e8337e501392d2a30d1d098` and `e52634bb4b64c8bdb519a5e6aacbd80f033d246a`. The NFT collection address is not passed as a parameter anymore.

**File(s) affected:**`Pool.sol`

**Description:**_Note: This issue was disclosed by the Nemeos team before the start of the security review._

Each deployed pool is associated with a fixed NFT collection (external address) and a minimal deposit percentage. However, `Pool.buyNFT()` accepts `collectionAddress_` as a parameter, breaking that association.

This could allow borrowers to buy NFTs from other arbitrary collections using the pool funds allocated for another collection.

**Recommendation:** Even if this is controlled by the off-chain validation by the oracle, consider removing the `collectionAddress_` parameter from `buyNFT()`. Instead, just use the fixed value set in `initialize()`: `nftCollection`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Nemeos |
| Report Date | N/A |
| Finders | Sebastian Banescu, Faycal Lalidji, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/nemeos/d98ae938-43ff-44f4-85c8-5852466df646/index.html

### Keywords for Search

`vulnerability`

