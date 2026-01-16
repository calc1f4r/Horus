---
# Core Classification
protocol: Ajna
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6305
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/32
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/120

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - berndartmueller
  - oxcm
  - ctf\_sec
---

## Vulnerability Title

M-8: Claiming accumulated rewards while the contract is underfunded can lead to a loss of rewards

### Overview


This bug report is about an issue in the Ajna token staking system where the claimable rewards for an NFT staker are capped at the Ajna token balance at the time of claiming. This can lead to a loss of rewards if the `RewardsManager` contract is underfunded with Ajna tokens. 

The `RewardsManager._claimRewards` function transfers the accumulated rewards to the staker, but if the accumulated rewards are higher than the Ajna token balance, the claimer will receive fewer rewards than expected. The remaining rewards cannot be claimed at a later time as the `RewardsManager` contract does not keep track of the rewards that were not transferred.

The impact of this bug is that an NFT staker can claim fewer rewards than expected and is unable to claim the rest of the rewards at a later time if the `RewardsManager` contract is underfunded. 

The bug was found by berndartmueller, ctf_sec, and oxcm and was confirmed by manual review. The recommendation is to consider reverting if insufficient Ajna tokens are available as rewards.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/120 

## Found by 
berndartmueller, ctf\_sec, oxcm

## Summary

The claimable rewards for an NFT staker are capped at the Ajna token balance at the time of claiming. This can lead to a loss of rewards if the `RewardsManager` contract is underfunded with Ajna tokens.

## Vulnerability Detail

The `RewardsManager` contract keeps track of the rewards earned by an NFT staker. The accumulated rewards are claimed by calling the `RewardsManager.claimRewards` function. Internally, the `RewardsManager._claimRewards` function transfers the accumulated rewards to the staker.

However, the transferrable amount of Ajna token rewards are capped at the Ajna token balance at the time of claiming. If the accumulated rewards are higher than the Ajna token balance, the claimer will receive fewer rewards than expected. The remaining rewards cannot be claimed at a later time as the `RewardsManager` contract does not keep track of the rewards that were not transferred.

## Impact

If an NFT staker claims the accumulated rewards in a bad situation (when the `RewardsManager` contract is underfunded with Ajna tokens), the staker will receive fewer rewards than expected and is unable to claim the rest of the rewards at a later time.

## Code Snippet

[contracts/src/RewardsManager.sol#L479](https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/RewardsManager.sol#L479)

```solidity
445: function _claimRewards(
446:     uint256 tokenId_,
447:     uint256 epochToClaim_
448: ) internal {
         // [...]

477:     uint256 ajnaBalance = IERC20(ajnaToken).balanceOf(address(this));
478:
479:     if (rewardsEarned > ajnaBalance) rewardsEarned = ajnaBalance;
480:
481:     // transfer rewards to sender
482:     IERC20(ajnaToken).safeTransfer(msg.sender, rewardsEarned);
483: }
```

## Tool used

Manual Review

## Recommendation

Consider reverting if insufficient Ajna tokens are available as rewards.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Ajna |
| Report Date | N/A |
| Finders | berndartmueller, oxcm, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/120
- **Contest**: https://app.sherlock.xyz/audits/contests/32

### Keywords for Search

`Business Logic`

