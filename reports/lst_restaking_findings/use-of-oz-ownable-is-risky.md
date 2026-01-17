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
solodit_id: 46025
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

Use of OZ Ownable is risky 

### Overview

See description below for full details.

### Original Finding Content

## Security Review of CarrotStaker.sol

## Context
CarrotStaker.sol#L16

## Description
OpenZeppelin Ownable is used by CarrotStaker to manage contract ownership. However, this is risky because it allows single-step ownership transfers.

## Recommendation
Consider using Ownable2Step that, as documented, includes a two-step mechanism to transfer ownership, where the new owner must call `acceptOwnership` in order to replace the old one. This can help prevent common mistakes, such as transfers of ownership to incorrect accounts, or to contracts that are unable to interact with the permission system.

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

