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
solodit_id: 41233
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#11-elrewardsstealingpenaltysettled-event-shouldnt-be-emitted-in-some-cases
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

`ELRewardsStealingPenaltySettled` event shouldn't be emitted in some cases

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the [settleELRewardsStealingPenalty](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSModule.sol#L1089) function of the `CSModule` contract. This function emits `ELRewardsStealingPenaltySettled` event even if the retention period for the locked bond has passed.

The issue is classified as **Low** severity because it may lead to an incorrect event being emitted when the penalty wasn't actually settled.

##### Recommendation
We recommend emitting the `ELRewardsStealingPenaltySettled` event only if `lockedBondBefore > 0` is returned from the `accounting.settleLockedBondETH(nodeOperatorId)` call.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#11-elrewardsstealingpenaltysettled-event-shouldnt-be-emitted-in-some-cases
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

