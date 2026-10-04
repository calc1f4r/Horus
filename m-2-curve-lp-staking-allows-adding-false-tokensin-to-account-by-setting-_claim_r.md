---
# Core Classification
protocol: Sentiment Update
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3543
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/17
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-sentiment-judging/issues/20

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
  - dexes
  - cdp
  - services
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - obront
---

## Vulnerability Title

M-2: Curve LP staking allows adding false tokensIn to account by setting _claim_rewards to false

### Overview


A bug was discovered in CurveLPStakingController.sol and BalancerLPStakingController.sol, which allows users to add false tokens to their account by using the full function signature and setting the `_claim_rewards` boolean to false. This is because the only requirement to go down this code path is to use the full function signature, and `canDepositAndClaim()` and `canWithdrawAndClaim()` assume that the user is claiming reward tokens, and add these tokens to the `tokensIn` array. 

The bug can lead to mismatches between a user's assets array and hasAsset mapping and the reality of their account. To fix the bug, it was recommended to decode the calldata to get the value of the `_claim_rewards` bool in `canCall()`, and if it is false, call the non-claim version of the function. The fix was confirmed in a pull request.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-sentiment-judging/issues/20 

## Found by 
obront

## Summary

In CurveLPStakingController.sol and BalancerLPStakingController.sol, `canDepositAndClaim()` and `canWithdrawAndClaim()` assume that the user is claiming reward tokens, and add these tokens to the `tokensIn` array (to add to their account). 

However, the only requirement to go down this code path is to use the full function signature (ie `deposit(uint256,address,bool)`), so false tokens will be added to a user account if they use the full signature with the `_claim_rewards` bool set to `false`.

## Vulnerability Detail

Each Controller returns an array of `tokensIn` that will be added to the user's account, if they don't already hold a balance.

In CurveLPStakingController.sol and BalancerLPStakingController.sol, there are two overlapping pairs of function signatures: 
- `deposit(uint256)` and `deposit(uint256,address,bool)` are the same function, but the middle parameter (`_addr`) defaults to `msg.sender` and the final parameter (`_claim_rewards`) defaults to `false`
- `withdraw(uint256)` and `withdraw(uint256,bool)` are the same function, but the final parameter (`_claim_rewards`) defaults to `false`

The assumption in the Controller logic is that, if a user uses the full signature, they are claiming their rewards. However, this isn't always the case. It is perfectly valid for a user to use the full function and pass `false` (the default argument) to the `_claim_rewards` parameter.

In this case, the function signature would lead to `canDepositAndClaim()` or `canWithdrawAndClaim()`, and all the rewards tokens would be added to the user's account.

## Impact

Accounting on user accounts can be thrown off (intentionally or unintentionally), resulting in mismatches between their assets array and hasAsset mapping and the reality of their account.

## Code Snippet

https://github.com/sherlock-audit/2022-11-sentiment/blob/main/controller-merged/src/balancer/BalancerLPStakingController.sol#L24-L25

https://github.com/sherlock-audit/2022-11-sentiment/blob/main/controller-merged/src/balancer/BalancerLPStakingController.sol#L52

https://github.com/sherlock-audit/2022-11-sentiment/blob/main/controller-merged/src/balancer/BalancerLPStakingController.sol#L72-L92

## Tool used

Manual Review

## Recommendation

In `canCall()`, decode the calldata to get the value of the `_claim_rewards` bool. If this value is false, call the non-claim version of the function (ie `canDeposit()` instead of `canDepositAndClaim()`).

## Discussion

**ruvaag**

While I agree with the issue, I'm not sure if it qualifies as a medium because I don't think this can lead to loss of funds or functionality.

**zobront**

Confirmed fix in https://github.com/sentimentxyz/controller/pull/48

**Evert0x**

I think a medium severity is valid as there is a risk of to let users add tokens to their account that they don't really have.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Sentiment Update |
| Report Date | N/A |
| Finders | obront |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-sentiment-judging/issues/20
- **Contest**: https://app.sherlock.xyz/audits/contests/17

### Keywords for Search

`vulnerability`

