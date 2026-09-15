---
# Core Classification
protocol: Anchor
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 23437
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-02-anchor
source_link: https://code4rena.com/reports/2022-02-anchor
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
  - services
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[N-02] Incorrect description of `Safe Ratio` in documentation

### Overview

See description below for full details.

### Original Finding Content


### Reference

<https://docs.anchorprotocol.com/protocol/anchor-governance/modify-liquidation-parameters>

### Description

The docs say that

“A **low** `Safe Ratio` value allows for the fast liquidation of collaterals while incurring a high price impact for the collateral, while a **low** `Safe Ratio` value enforces liquidations with lower collateral price impact, albeit with slower collateral liquidation.”

The second statement describes a **high** safe ratio.

### Recommended Mitigation Steps

Change to “while a **high** `Safe Ratio` value enforces liquidations with lower collateral price impact, albeit with slower collateral liquidation.”



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Anchor |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-anchor
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-02-anchor

### Keywords for Search

`vulnerability`

