---
# Core Classification
protocol: Ouroboros_2024-12-06
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45970
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2024-12-06.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-11] Burning clawback rewards causes total debt to be greater than stable total supply

### Overview

See description below for full details.

### Original Finding Content

The `burnClawbackRewards` function in the `PositionController` contract burns the stable tokens minted to the contract on `claimEscrow`. However, the debt accounted for by the protocol has not been reduced.

This means that the total debt of the protocol (sum of debt in active and default pool for all collaterals) is not anymore equal to the total supply of stable tokens. This results in a overestimation of the total debt in the system and thus, of the minimum collateral ratios.

A simplified example to illustrate the issue:

```
Initial state:
- Total supply: 100 USDx
- Total debt: 100 USDx
- Total collateral value: 200 USD
- TCR: 200%

After clawback rewards are claimed and collateral price decreases:
- Total supply: 60 USDx
- Total debt: 100 USDx
- Total collateral value: 120 USD
- TCR: 120%

While the collateral value backs all the stable tokens in circulation with a 200% ratio, as the debt is greater than the total supply, the TCR is calculated as 120%.
```

Consider removing this function and using in all cases the `distributeClawbackRewards` function to distribute the stables to the fee stakers.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ouroboros_2024-12-06 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2024-12-06.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

