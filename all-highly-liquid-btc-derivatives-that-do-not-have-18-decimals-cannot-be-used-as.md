---
# Core Classification
protocol: Bima
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46147
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/0e4d03d9-b8c4-4cd7-ab20-15a480096d49
source_link: https://cdn.cantina.xyz/reports/cantina_bima_december2024.pdf
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
finders_count: 1
finders:
  - ladboy233
---

## Vulnerability Title

All highly liquid BTC derivatives that do not have 18 decimals cannot be used as a collateral to mint stable coins 

### Overview


The bug report discusses an issue with the code in Factory.sol that prevents certain BTC derivatives from being used as collateral to mint stable coins. The code currently requires the collateral to have 18 decimals, but some of the most liquid BTC derivatives only have 8 decimals. This means that these derivatives cannot be used as collateral, which limits the functionality of the protocol. The recommendation is to remove the decimal check and make the code compatible with different precision collaterals. This issue has been fixed in commit 88502152 by Bima and Cantina Managed has also fixed it by adding a wrapper that converts low decimal tokens to 18 decimals. This bug is considered low risk.

### Original Finding Content

## Context
Factory.sol#L70-L78

## Description
The code enforces that the collateral must have 18 decimals.

```solidity
require(collateralToken.decimals() == BIMA_COLLATERAL_DECIMALS, "Invalid collateral decimals");
```

The protocol intends to use BTC derivatives as collateral to mint stable coins. However, some of the most liquid BTC derivatives such as WBTC, renBTC, and imBTC have 8 decimals. The impact is that these highly liquid BTC derivatives cannot be used as collateral to mint stable coins.

## Recommendation
Remove the decimal check and ensure the code is compatible with the different precision collaterals.

## Bima
Fixed in commit 88502152.

## Cantina Managed
Fixed by adding a wrapper that wraps low decimal tokens to 18 decimals.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Bima |
| Report Date | N/A |
| Finders | ladboy233 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_bima_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/0e4d03d9-b8c4-4cd7-ab20-15a480096d49

### Keywords for Search

`vulnerability`

