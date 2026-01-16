---
# Core Classification
protocol: Mantle Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63672
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Mantle%20Network/mETH%20x%20Aave%20Integration/README.md#6-fixed-exchange-rate-at-unstaking-fails-to-socialize-slashing-and-distorts-rewards
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Fixed exchange rate at unstaking fails to socialize slashing and distorts rewards

### Overview


The `Staking.unstakeRequest()` function is causing issues with the mETH/ETH rate being fixed and not reflecting any losses or rewards that may occur while waiting for `Staking.claimUnstakeRequest()` to be executed. This can result in unequal distribution of losses and rewards among users who submit requests at the same time. It is also causing rewards to be misallocated and diluting rewards for users who have not requested to unstake. The client is not planning to fix this issue as it is a trade-off in the protocol design and has only occurred under extreme market conditions. However, the recommendation is to align withdrawal settlement with the latest protocol state and adjust reward accounting to prevent these issues.

### Original Finding Content

##### Description
When `Staking.unstakeRequest()` is called, the mETH/ETH rate is fixed and does not reflect slashing or rewards that may occur by the time `Staking.claimUnstakeRequest()` is executed. If two users create requests concurrently and losses arrive afterward, those losses are not socialized across them. One request may be fully paid while the other may revert on claim due to insufficient allocated funds.

This can be exacerbated by frontrunning updates to `LiquidityBuffer.cumulativeDrawdown()`, enabling informed actors to anticipate loss application.

Rewards are also misallocated: requests lock mETH but do not burn it until `UnstakeRequestsManager.claim()`, so these shares continue participating in reward distribution, diluting rewards for users who have not requested to unstake.

Example: Alice and Bob each hold 100 mETH and the pool controls 200 ETH. Alice submits `Staking.unstakeRequest()` for 100 mETH; the shares are locked but not burned. A subsequent 100 ETH reward is then distributed across 200 mETH, so only ~50 ETH is attributed to Bob instead of ~100 ETH. This dilution persists until Alice calls `UnstakeRequestsManager.claim()` and the 100 mETH are burned.
<br/>
##### Recommendation
We recommend aligning withdrawal settlement with the latest protocol state to socialize slashing and adjusting reward accounting so pending unstakes do not accrue or dilute rewards.

> **Client's Commentary:**
> **Client**: Not fixing: this is a protocol design trade-off.
>  - Users can predict their returns when submitting unstake requests 
>  - unstakeRequestManager also supports the request cancellation and refund mechanism.
>  - This design has proven effective under normal market conditions
>  - This issue only occurs under extreme market conditions (e.g., significant slashing events)
>    - The protocol has robust monitoring and alert systems to detect such scenarios
>    - The affected scope is limited to users who submit unstake requests during the same period
>  - Fixing this issue would require restructuring core unstaking mechanisms, resulting in high development costs
>  
> **MixBytes**: The probability of a significant slashing event leading to net losses not offset by rewards is low, and no such event has occurred to date.
>  
> We acknowledge the design choice to fix the rate at unstake request time: it improves predictability but can, in rare cases, create timing advantages and uneven distribution of losses/rewards.
> 
> We recommend clearly documenting this trade-off for users; an explicit compensation or `topUp()` policy would further reduce residual risk.

---


### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Mantle Network |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Mantle%20Network/mETH%20x%20Aave%20Integration/README.md#6-fixed-exchange-rate-at-unstaking-fails-to-socialize-slashing-and-distorts-rewards
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

