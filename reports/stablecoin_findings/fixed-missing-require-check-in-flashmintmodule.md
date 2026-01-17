---
# Core Classification
protocol: Fathom Stablecoin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31024
audit_firm: Oxorio
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom Stablecoin.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Oxorio
---

## Vulnerability Title

[FIXED] Missing `require` check in `FlashMintModule`

### Overview

See description below for full details.

### Original Finding Content

##### Location
File | Location | Line
--- | --- | ---
[FlashMintModule.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/flash-mint/FlashMintModule.sol#L162 "/contracts/main/flash-mint/FlashMintModule.sol" "/contracts/main/flash-mint/FlashMintModule.sol") | contract `FlashMintModule` > function `flashLoan` | 162

##### Description
In the function `flashLoan` of the contract `FlashMintModule`, there is no validation that after the `settleSystemBadDebt` call, the current amount of the `stablecoin` in `BookKeeper` equals or is greater than the previous amount plus fees, while this check is present in the `bookKeeperFlashLoan` function.
##### Recommendation
We recommend adding the same `require` to the `flashLoan` function to ensure the same level of security in both functions.
##### Update
###### Client's response
Fixed in commit [`754fd35abc2c6ea77e5e4e375fb587b8fcf114a6`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/commit/754fd35abc2c6ea77e5e4e375fb587b8fcf114a6).
Fixed as suggested.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Oxorio |
| Protocol | Fathom Stablecoin |
| Report Date | N/A |
| Finders | Oxorio |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom Stablecoin.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

