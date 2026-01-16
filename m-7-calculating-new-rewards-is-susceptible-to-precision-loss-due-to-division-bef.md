---
# Core Classification
protocol: Ajna
chain: everychain
category: arithmetic
vulnerability_type: precision_loss

# Attack Vector Details
attack_type: precision_loss
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6304
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/32
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/121

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.67
financial_impact: medium

# Scoring
quality_score: 3.3333333333333335
rarity_score: 3.3333333333333335

# Context Tags
tags:
  - precision_loss

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - berndartmueller
---

## Vulnerability Title

M-7: Calculating new rewards is susceptible to precision loss due to division before multiplication

### Overview


This bug report is about a vulnerability found in the RewardsManager._calculateNewRewards function in the smart contract code. This vulnerability can cause stakers to not receive rewards due to precision loss. The issue is caused by dividing `interestEarned_` by `totalInterestEarnedInPeriod` and then multiplying by `totalBurnedInPeriod`. If `interestEarned_` is small enough and `totalInterestEarnedInPeriod` is large enough, the division may result in a value of 0, resulting in the staker receiving 0 rewards. The bug was found by manual review and the code snippet is available at the URL provided. The recommended solution is to calculate the new rewards by first multiplying `interestEarned_` by `totalBurnedInPeriod` and then dividing by `totalInterestEarnedInPeriod` to avoid precision loss.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/121 

## Found by 
berndartmueller

## Summary

Rewards may be lost (0) due to division before multiplication precision issues.

## Vulnerability Detail

The `RewardsManager._calculateNewRewards` function calculates the new rewards for a staker by first dividing `interestEarned_` by `totalInterestEarnedInPeriod` and then multiplying by `totalBurnedInPeriod`. If `interestEarned_` is small enough and `totalInterestEarnedInPeriod` is large enough, the division may result in a value of 0, resulting in the staker receiving 0 rewards.

## Impact

Stakers may not receive rewards due to precision loss.

## Code Snippet

[contracts/src/RewardsManager.sol#L426-L428](https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/RewardsManager.sol#L426-L428)

```solidity
408: function _calculateNewRewards(
409:     address ajnaPool_,
410:     uint256 interestEarned_,
411:     uint256 nextEpoch_,
412:     uint256 epoch_,
413:     uint256 rewardsClaimedInEpoch_
414: ) internal view returns (uint256 newRewards_) {
415:     (
416:         ,
417:         // total interest accumulated by the pool over the claim period
418:         uint256 totalBurnedInPeriod,
419:         // total tokens burned over the claim period
420:         uint256 totalInterestEarnedInPeriod
421:     ) = _getPoolAccumulators(ajnaPool_, nextEpoch_, epoch_);
422:
423:     // calculate rewards earned
424:     newRewards_ = Maths.wmul(
425:         REWARD_FACTOR,
426:         Maths.wmul(
427:             Maths.wdiv(interestEarned_, totalInterestEarnedInPeriod), totalBurnedInPeriod
428:         )
429:     );
```

## Tool used

Manual Review

## Recommendation

Consider calculating the new rewards by first multiplying `interestEarned_` by `totalBurnedInPeriod` and then dividing by `totalInterestEarnedInPeriod` to avoid precision loss.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3.3333333333333335/5 |
| Rarity Score | 3.3333333333333335/5 |
| Audit Firm | Sherlock |
| Protocol | Ajna |
| Report Date | N/A |
| Finders | berndartmueller |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/121
- **Contest**: https://app.sherlock.xyz/audits/contests/32

### Keywords for Search

`Precision Loss`

