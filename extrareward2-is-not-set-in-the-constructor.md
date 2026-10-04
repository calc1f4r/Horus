---
# Core Classification
protocol: Gearbox
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53770
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

extraReward2 is Not Set in the constructor()

### Overview


The report describes a bug in the code of `ConvexV1_BaseRewardPool.sol` where the variable _extraReward2_ is not properly set in the constructor. This can lead to the zero address being stored in _extraReward2_ and the intended address being overwritten in _extraReward1_. To fix this, the code in the constructor should be modified to correctly assign the extra rewards to their corresponding variables. This issue has been resolved by the development team in a recent commit.

### Original Finding Content

## Description

_extraReward2_ is never set in the constructor of `ConvexV1_BaseRewardPool.sol`. Gearbox integrates the Convex platform by allowing borrowers to stake their Convex LP tokens. Gearbox makes use of a phantom ERC20 token to represent the borrower’s position in the reward pool. Extra rewards can be attached to a reward pool on top of any Curve and Convex rewards.

Within the `constructor()` code, _extraReward2_ is never set and will end up storing the zero address. As a result, _extraReward2_ will also contain the zero address and _extraReward1_ will be overwritten with the address intended for _extraReward2_. The affected code is shown below:

```solidity
if (extraRewardLength >= 1) {
    _extraReward1 = IRewards(
        IBaseRewardPool(_baseRewardPool).extraRewards(0)
    ).rewardToken();
    if (extraRewardLength >= 2) {
        _extraReward1 = IRewards(
            IBaseRewardPool(_baseRewardPool).extraRewards(1)
        ).rewardToken(); // assign to _extraReward2, not _extraReward1
    }
}
```

## Recommendations

Modify the `constructor()` code to store the extra rewards in their correct, corresponding variables _extraReward1_ and _extraReward2_.

## Resolution

The development team mitigated this issue in commit `5ae20eb` by implementing the recommendations above.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Gearbox |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf

### Keywords for Search

`vulnerability`

