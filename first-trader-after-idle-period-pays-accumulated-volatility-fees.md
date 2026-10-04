---
# Core Classification
protocol: NUTS Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62688
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Tapio/README.md#18-first-trader-after-idle-period-pays-accumulated-volatility-fees
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
  - MixBytes
---

## Vulnerability Title

First Trader After Idle Period Pays Accumulated Volatility Fees

### Overview

See description below for full details.

### Original Finding Content

##### Description
This issue has been identified within the `_updateMultiplierForToken` function of the `SelfPeggingAsset` contract.

Currently, the volatility multiplier increases only when the `_updateMultiplierForToken` function is triggered by user interaction. If no interaction occurs for an extended period while the external token price significantly changes, the first subsequent trade triggers a multiplier spike. This first trader unfairly incurs the entire accumulated volatility fee due to historical price changes, rather than just the volatility arising from their specific trade.

As an illustrative scenario:

1. The pool remains inactive for several days (e.g. due to admin's pause), during which the token price doubles.
2. The first swap executed after this inactive period experiences an unusually high volatility fee, even if the price remains stable around the new value at the trade time.

This results in a poor user experience and creates a potential denial-of-service vector, as users may avoid trading after prolonged inactivity periods.

##### Recommendation
We recommend applying a continuous linear decay mechanism to the `candidateMultiplier` as well, ensuring new multipliers decay proportionally over time in the same way as current multipliers.


### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | NUTS Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Tapio/README.md#18-first-trader-after-idle-period-pays-accumulated-volatility-fees
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

