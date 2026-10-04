---
# Core Classification
protocol: Ante Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17758
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/AnteProtocol.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/AnteProtocol.pdf
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Troy Sargent
  - David Pokora
---

## Vulnerability Title

Looping over an array of unbounded size can cause a denial of service

### Overview


This bug report is about the _checkTestNoRevert function in the AntePool smart contract. If an AnteTest fails, the _checkTestNoRevert function will return false, causing the checkTest function to call _calculateChallengerEligibility to compute eligibleAmount. This value is the total stake of the eligible challengers and is used to calculate the proportion of _remainingStake owed to each challenger. 

The problem is that when the number of challengers is large, the _calculateChallengerEligibility function will consume a large quantity of gas in this operation, potentially triggering an out-of-gas error and causing the transaction to revert. This would be costly to an attacker, as they would need to create many accounts through which to stake funds. As a result, challengers who have staked funds in anticipation of a failed test will not receive a payout.

The recommendation is to determine the number of challengers that can enter an AntePool without rendering the _calculateChallengerEligibility function’s operation too gas intensive. This number should be used as the upper limit on the number of challengers. In the long-term, the recommendation is to avoid calculating every challenger’s proportion of _remainingStake in the same operation; instead, calculate each user's pro-rata share when he or she enters the pool and modify the challenger delay to require that a challenger register and wait 12 blocks before minting his or her pro-rata share. Upon a test failure, a challenger would burn these shares and redeem them for ether.

### Original Finding Content

## Difficulty: Medium

## Type: Data Validation

## Description
If an AnteTest fails, the `_checkTestNoRevert` function will return false, causing the `checkTest` function to call `_calculateChallengerEligibility` to compute `eligibleAmount`; this value is the total stake of the eligible challengers and is used to calculate the proportion of `_remainingStake` owed to each challenger. To calculate `eligibleAmount`, the `_calculateChallengerEligibility` function loops through an unbounded array of challenger addresses. When the number of challengers is large, the function will consume a large quantity of gas in this operation.

```solidity
function _calculateChallengerEligibility() internal {
    uint256 cutoffBlock = failedBlock.sub(CHALLENGER_BLOCK_DELAY);
    for (uint256 i = 0; i < challengers.addresses.length; i++) {
        address challenger = challengers.addresses[i];
        if (eligibilityInfo.lastStakedBlock[challenger] < cutoffBlock) {
            eligibilityInfo.eligibleAmount = eligibilityInfo.eligibleAmount.add(
                _storedBalance(challengerInfo.userInfo[challenger], challengerInfo)
            );
        }
    }
}
```

*Figure 4.1: contracts/AntePool.sol#L553-L563*

However, triggering an out-of-gas error would be costly to an attacker; the attacker would need to create many accounts through which to stake funds, and the amount of each stake would decay over time.

## Exploit Scenario
The length of the challenger address array grows such that the computation of the `eligibleAmount` causes the block to reach its gas limit. Then, because of this Ethereum-imposed gas constraint, the entire transaction reverts, and the failing AnteTest is not marked as failing. As a result, challengers who have staked funds in anticipation of a failed test will not receive a payout.

## Recommendations
- Short term, determine the number of challengers that can enter an AntePool without rendering the `_calculateChallengerEligibility` function’s operation too gas intensive; then, use that number as the upper limit on the number of challengers.
- Long term, avoid calculating every challenger’s proportion of `_remainingStake` in the same operation; instead, calculate each user's pro-rata share when he or she enters the pool and modify the challenger delay to require that a challenger register and wait 12 blocks before minting his or her pro-rata share. Upon a test failure, a challenger would burn these shares and redeem them for ether.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Ante Protocol |
| Report Date | N/A |
| Finders | Troy Sargent, David Pokora |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/AnteProtocol.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/AnteProtocol.pdf

### Keywords for Search

`vulnerability`

