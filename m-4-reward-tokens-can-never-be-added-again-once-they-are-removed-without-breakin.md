---
# Core Classification
protocol: Olympusdao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6680
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/50
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/177

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - cccz
  - cducrest-brainbot
  - 0x52
  - hansfriese
---

## Vulnerability Title

M-4: Reward tokens can never be added again once they are removed without breaking rewards completely

### Overview


This bug report is about an issue with the reward token system in the contract. When a reward token is removed, the global tracker for the accumulated rewards is also removed, but the individual mapping still stores the previously accumulated rewards. If the token is ever added again, the global accumulated reward tracker will now be reset but the individual trackers will not. This will cause an underflow anytime a user tries to claim reward tokens, meaning reward tokens can never be added again once they are removed. The code snippet in the report can be found at https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/abstracts/SingleSidedLiquidityVault.sol#L674-L687 and the tool used was ChatGPT. The recommendation for this issue is to consider tracking accumulatedRewardsPerShare in a mapping rather than in the individual struct or to change how removal of reward tokens works.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/177 

## Found by 
cccz, cducrest-brainbot, 0x52, hansfriese

## Summary

Once reward tokens are removed they can never be added back to the contract. The happens because accumulated rewards are tracked differently globally vs individually. Global accumulated rewards are tracked inside the rewardToken array whereas it is tracked by token address for users. When a reward token is removed the global tracker is cleared but the individual trackers are not. If a removed token is added again, the global tracker will reset to zero but the individual tracker won't. As a result of this claiming will fail due to an underflow.

## Vulnerability Detail

https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/abstracts/SingleSidedLiquidityVault.sol#L491-L493

The amount of accumulated rewards for a specific token is tracked in it's respective rewardToken struct. 

https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/abstracts/SingleSidedLiquidityVault.sol#L624-L629

For individual users the rewards are stored in a mapping.

https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/abstracts/SingleSidedLiquidityVault.sol#L694-L703

When a reward token is removed the global tracker for the accumulated rewards is also removed. The problem is that the individual mapping still stores the previously accumulated rewards. If the token is ever added again, the global accumulated reward tracker will now be reset but the individual trackers will not. This will cause an underflow anytime a user tries to claim reward tokens. 

## Impact

Reward tokens cannot be added again once they are removed

## Code Snippet

https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/abstracts/SingleSidedLiquidityVault.sol#L674-L687

## Tool used

ChatGPT

## Recommendation

Consider tracking accumulatedRewardsPerShare in a mapping rather than in the individual struct or change how removal of reward tokens works

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Olympusdao |
| Report Date | N/A |
| Finders | cccz, cducrest-brainbot, 0x52, hansfriese |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/177
- **Contest**: https://app.sherlock.xyz/audits/contests/50

### Keywords for Search

`vulnerability`

