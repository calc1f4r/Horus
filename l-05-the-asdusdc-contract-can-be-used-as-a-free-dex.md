---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32138
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-canto
source_link: https://code4rena.com/reports/2024-03-canto
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-05] The `asdUSDC` contract can be used as a free DEX

### Overview

See description below for full details.

### Original Finding Content


Due to the permissionless and feeless nature of the [`deposit`(…)](https://github.com/code-423n4/2024-03-canto/blob/1516028017a34ccfb4b0b19f5c5f17f5fa4cad42/contracts/asd/asdUSDC.sol# L34-L44) and [`withdraw`(…)](https://github.com/code-423n4/2024-03-canto/blob/1516028017a34ccfb4b0b19f5c5f17f5fa4cad42/contracts/asd/asdUSDC.sol# L52-L66) methods, everyone can use them to swap whitelisted USDC-like tokens for free. This might be especially attractive (for arbitraging) if such a stablecoin slightly depegs.

### Consequence

Users cannot expect to be able to withdraw the same stablecoin they’ve deposited since its underlying balance might be depleted.

### Recommendation

Restrict the [`deposit`(…)](https://github.com/code-423n4/2024-03-canto/blob/1516028017a34ccfb4b0b19f5c5f17f5fa4cad42/contracts/asd/asdUSDC.sol# L34-L44) method to only be callable from the `asdRouter` contract.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-canto
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-03-canto

### Keywords for Search

`vulnerability`

