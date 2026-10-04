---
# Core Classification
protocol: Puffer Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46027
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/87903648-d580-4572-ad06-276c5c1395c7
source_link: https://cdn.cantina.xyz/reports/cantina_puffer_february2025.pdf
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
finders_count: 2
finders:
  - 0xWeiss
  - Windhustler
---

## Vulnerability Title

Incorrect symbol for staked token 

### Overview

See description below for full details.

### Original Finding Content

## Context
CarrotStaker.sol#L37

## Description
The current symbol from staked carrot is set to `sCarrot`, in lowercase:

```solidity
constructor(address carrot, address initialOwner) ERC20("Staked Carrot", "sCarrot") Ownable(initialOwner) {
```

However, if the symbol of the CARROT token is set uppercase.

## Recommendation
Make the following change to the symbol:

```solidity
- constructor(address carrot, address initialOwner) ERC20("Staked Carrot", "sCarrot") Ownable(initialOwner) {
+ constructor(address carrot, address initialOwner) ERC20("Staked Carrot", "sCARROT") Ownable(initialOwner) {
```

## Additional Information
- **Puffer Finance**: Fixed in PR 98.
- **Cantina Managed**: Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Puffer Finance |
| Report Date | N/A |
| Finders | 0xWeiss, Windhustler |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_puffer_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/87903648-d580-4572-ad06-276c5c1395c7

### Keywords for Search

`vulnerability`

