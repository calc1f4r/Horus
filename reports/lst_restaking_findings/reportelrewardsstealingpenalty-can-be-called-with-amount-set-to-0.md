---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41232
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#10-reportelrewardsstealingpenalty-can-be-called-with-amount-set-to-0
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

`reportELRewardsStealingPenalty` can be called with `amount` set to `0`

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the [reportELRewardsStealingPenalty](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSModule.sol#L1014) function of the `CSModule` contract. The mentioned function can be called with `amount` set to `0`. In that case, only `EL_REWARDS_STEALING_FINE` is applied, and the `ELRewardsStealingPenaltyReported` event with `stolenAmount == 0` is emitted.

The issue is classified as **Low** severity because it requires a mistake made by the `REPORT_EL_REWARDS_STEALING_PENALTY_ROLE` role owner.

##### Recommendation
We recommend restricting calls to the `reportELRewardsStealingPenalty` with the `amount` parameter set to `0`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#10-reportelrewardsstealingpenalty-can-be-called-with-amount-set-to-0
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

