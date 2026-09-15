---
# Core Classification
protocol: Ondo Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32015
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-ondo-finance
source_link: https://code4rena.com/reports/2024-03-ondo-finance
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
  - leveraged_farming
  - rwa
  - services
  - cdp
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-04] `ousgInstantManager::mint`/`redeem` lacks slippage parameter

### Overview

See description below for full details.

### Original Finding Content


In `ousgInstantManager` you can mint either `rOUSG` or `OUSG` using `USDC` and then redeem back to `USDC`. Both of these use an oracle to track the price of `OUSG`. This price can vary between when a transaction is sent to when it is executed. This can cause a user to mint or redeem at a different price than they intended.

### Recommendation

Consider adding a `minOut` parameter for `ousgInstantManager::mint` and `redeem` calls.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ondo Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-ondo-finance
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-03-ondo-finance

### Keywords for Search

`vulnerability`

