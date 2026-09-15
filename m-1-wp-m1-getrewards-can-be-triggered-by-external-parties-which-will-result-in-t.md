---
# Core Classification
protocol: Sentiment Update #2
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5644
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/28
source_link: none
github_link: https://github.com/sherlock-audit/2022-12-sentiment-judging/issues/15

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 2

# Context Tags
tags:
  - business_logic

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - yield_aggregator
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WATCHPUG
---

## Vulnerability Title

M-1: [WP-M1] getRewards() can be triggered by external parties which will result in the rewards not be tracking properly by the system

### Overview


This bug report concerns the `ConvexRewardPool#getReward(address)` function in the `ConvexBoosterController.sol` contract, which can be called by any address besides the owner. If a third party helps the owner to call the `getReward()` function, the reward tokens may not be added to the account's assets list, which can lead to the account being liquidated while there are enough assets in the account. The bug was found by WATCHPUG and the recommendation is to add all the reward tokens to the account's assets list in `ConvexBoosterController.sol#canDeposit()`. The bug was fixed by r0ohafza in a pull request.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-12-sentiment-judging/issues/15 

## Found by 
WATCHPUG

## Summary

`ConvexRewardPool#getReward(address)` can be called by any address besides the owner themself.

## Vulnerability Detail

The reward tokens will only be added to the assets list when `getReward()` is called.

If there is a third party that is "helping" the `account` to call `getReward()` from time to time, by keeping the value of unclaimed rewards low, the account owner may not have the motivation to take the initiative to call `getReward()` via the `AccountManager`.

As a result, the reward tokens may never get added to the account's assets list.

## Impact

If the helper/attacker continuously claims the rewards on behalf of the victim, the rewards will not be accounted for in the victim's total assets.

As a result, the victim's account can be liquidated while actual there are enough assets in their account, it is just that these are not accounted for.

## Code Snippet

https://github.com/sentimentxyz/controller/blob/507274a0803ceaa3cbbaf2a696e2458e18437b2f/src/convex/ConvexBoosterController.sol#L31-L46

https://arbiscan.io/address/0x63F00F688086F0109d586501E783e33f2C950e78

## Tool used

Manual Review

## Recommendation

Consider adding all the reward tokens to the account's assets list in `ConvexBoosterController.sol#canDeposit()`.

## Discussion

**r0ohafza**

fix: https://github.com/sentimentxyz/controller/pull/54

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 2/5 |
| Audit Firm | Sherlock |
| Protocol | Sentiment Update #2 |
| Report Date | N/A |
| Finders | WATCHPUG |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-12-sentiment-judging/issues/15
- **Contest**: https://app.sherlock.xyz/audits/contests/28

### Keywords for Search

`Business Logic`

