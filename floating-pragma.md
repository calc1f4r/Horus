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
solodit_id: 46028
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

Floating Pragma 

### Overview

See description below for full details.

### Original Finding Content

## CarrotStaker.sol#L2

## Description
The solidity compiler version should be fixed to clearly identify the Solidity version with which the contracts will be compiled instead of having a floating pragma:

```solidity
pragma solidity >=0.8.0 <0.9.0;
```

## Recommendation
Update the version to the fixed version that will be used to compile the contract.

## Acknowledgements
- **Puffer Finance**: Acknowledged.
- **Cantina Managed**: Acknowledged.

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

