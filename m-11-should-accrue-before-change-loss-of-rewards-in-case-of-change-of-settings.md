---
# Core Classification
protocol: Reserve
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16021
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-reserve-contest
source_link: https://code4rena.com/reports/2023-01-reserve
github_link: https://github.com/code-423n4/2023-01-reserve-findings/issues/287

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - launchpad
  - privacy

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - __141345__
  - GalloDaSballo
  - chaduke
---

## Vulnerability Title

[M-11] Should Accrue Before Change, Loss of Rewards in case of change of settings

### Overview


This bug report is about a vulnerability in the code of the Reserve Protocol's StRSR.sol file. Specifically, the function "_payoutRewards" is used to accrue the value of rewards based on the time that has passed since "payoutLastPaid". This function should also be called when the functions "setRewardPeriod" and "setRewardRatio" are called, as these functions will change the rate of rewards. If this is not done, it could create an unfair reward stream or a governance attack. 

The mitigation proposed is that the functions that change the slope or period size should accrue rewards up to that point. This is to avoid incorrect reward distribution, change of rewards from the past, or a gain or loss of yield to stakers. The suggested refactoring is to include the "_payoutRewards" function in the "setRewardPeriod" and "setRewardRatio" functions. 

Overall, this bug report is about a vulnerability in the code of the Reserve Protocol's StRSR.sol file which could create an unfair reward stream or a governance attack. The mitigation proposed is to accrue rewards up to the point when "setRewardPeriod" and "setRewardRatio" are called, and the suggested refactoring is to include the "_payoutRewards" function in these two functions.

### Original Finding Content


In `StRSR.sol`, `_payoutRewards` is used to accrue the value of rewards based on the time that has passed since `payoutLastPaid`

Because of it's dependence on `totalStakes`, `stakeRate` and time, the function is rightfully called on every `stake` and `unstake`.

There is a specific instance, in which `_payoutRewards` should also be called, which could create either an unfair reward stream or a governance attack and that's when `setRewardPeriod` and `setRewardRatio` are called.

If you imagine the ratio at which rewards are paid out as a line, then you can see that by changing `rewardRatio` and `period` you're changing it's slope.

You should then agree, that while governance can *rightfully* change those settings, it should `_payoutRewards` first, to ensure that the slope of rewards changes only for rewards to be distributed after the setting has changed.

### Mitigation

Functions that change the slope or period size should accrue rewards up to that point.

This is to avoid:

*   Incorrect reward distribution
*   Change (positive or negative) of rewards from the past

Without accrual, the change will apply retroactively from `payoutLastPaid`

Which could:

*   Change the period length prematurely
*   Start a new period inadvertently
*   Cause a gain or loss of yield to stakers

Instead of starting a new period

### Suggested Refactoring

```solidity
function setRewardPeriod(uint48 val) public governance {
    require(val > 0 && val <= MAX_REWARD_PERIOD, "invalid rewardPeriod");
    _payoutRewards(); // @audit Payout rewards for fairness
    emit RewardPeriodSet(rewardPeriod, val);
    rewardPeriod = val;
    require(rewardPeriod * 2 <= unstakingDelay, "unstakingDelay/rewardPeriod incompatible");
}

function setRewardRatio(uint192 val) public governance {
    require(val <= MAX_REWARD_RATIO, "invalid rewardRatio");
    _payoutRewards(); // @audit Payout rewards for fairness
    emit RewardRatioSet(rewardRatio, val);
    rewardRatio = val;
}
```

**[tbrent (Reserve) confirmed and commented](https://github.com/code-423n4/2023-01-reserve-findings/issues/287#issuecomment-1404391327):**
 > Nice finding, agree. 

**[tbrent (Reserve) mitigated](https://github.com/code-423n4/2023-02-reserve-mitigation-contest#mitigations-to-be-reviewed):**
 > This PR adds a `Furnace.melt()`/`StRSR.payoutRewards()` step when governance changes the `rewardRatio`: [reserve-protocol/protocol#622](https://github.com/reserve-protocol/protocol/pull/622)

**Status:** Mitigation confirmed with comments. Full details in reports from [HollaDieWaldfee](https://github.com/code-423n4/2023-02-reserve-mitigation-contest-findings/issues/18), [0xA5DF](https://github.com/code-423n4/2023-02-reserve-mitigation-contest-findings/issues/57), and [AkshaySrivastav](https://github.com/code-423n4/2023-02-reserve-mitigation-contest-findings/issues/34).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Reserve |
| Report Date | N/A |
| Finders | __141345__, GalloDaSballo, chaduke |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-reserve
- **GitHub**: https://github.com/code-423n4/2023-01-reserve-findings/issues/287
- **Contest**: https://code4rena.com/contests/2023-01-reserve-contest

### Keywords for Search

`vulnerability`

