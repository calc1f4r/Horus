---
# Core Classification
protocol: Level  Money
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42054
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/99c7abab-0ff5-4e0e-a796-b1294271ca25
source_link: https://cdn.cantina.xyz/reports/cantina_level_money_sep2024.pdf
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
finders_count: 4
finders:
  - Delvir0
  - tchkvsky
  - MiloTruck
  - xiaoming90
---

## Vulnerability Title

Collateral could be redeemed without locking user 's lvlUSD 

### Overview

See description below for full details.

### Original Finding Content

## LevelMinting Discussion

## Context
**File:** LevelMinting.sol#L277

## Description
It was observed that allowing users to initiate redemption (or start the 7-day cooldown) without locking their collateral would not be beneficial for the protocol.

Assume Bob wants the ability to withdraw at any time without waiting for the cooldown period. To achieve this, Bob will always execute the `initiateRedeem` function immediately after depositing, allowing the cooldown to "age" in the background. Bob has no intention of completing the withdrawal after the 7-day period but wants the option to withdraw instantly once Day 7 passes. Meanwhile, he continues to utilize the minted `lvlUSD` (e.g., staking it on another protocol to earn yield) for the next 14 days before deciding to complete the withdrawal.

### In this scenario:
- Bob earns yields in X protocol for 14 days.
- Protocol picks up Bob's `RedeemInitiated` event on Day 0 and its bot initiates a withdrawal to the restaking protocol. Assuming for this specific restaking protocol, it stops earning rewards when the staked collateral enters the withdrawal queue. Thus, from Day 0 to Day 7, the protocol earns 0 rewards. Assuming that afterward, the protocol's algorithm stakes the unused collateral back to the restaking protocol and earns a total rewards of 7 (1 reward/day) from Day 8 to Day 14.

Assuming another scenario where the protocol requires users to lock their collateral upon initiating the redemption. In this case, since Bob needs to utilize the `lvlUSD` from Day 0 to Day 14, he cannot afford to initiate the redemption and have his `lvlUSD` locked. Therefore, he would only initiate the redemption on Day 15, after he’s finished earning yield on protocol X. As a result, from Day 0 to Day 14, the protocol would earn a total of 14 rewards (1 reward per day).

### Comparison
Comparing the first and second scenarios, the first scenario would result in less revenue for the protocol.

## Recommendation
Consider updating the `initiateRedeem()` function to require users to transfer their `lvlUSD` to this contract, and their `lvlUSD` is only burnt when `completeRedeem()` is called. If this approach is adopted, ensure that the contract includes logic to handle cases where the cooldown is disabled while pending redemptions are ongoing, since the `lvlUSD` is no longer directly burned from the user.

### Level Money
Fixed in commit `5afc185`.

### Cantina
The recommended approach for locking and subsequently burning `lvlUSD` was implemented. However, the case where the cooldown is disabled while pending redemptions are ongoing isn't handled. Consider the following scenario:
- `cooldownDuration` is set to 7 days.
- User calls `initiateRedeem()`, which transfers `lvlUSD` into the LevelMinting contract.
- Admin sets `cooldownDuration` to 0 days.
- User can no longer call `completeRedeem()` due to the `ensureCooldownOn` modifier.
- User cannot call `redeem()` as his `lvlUSD` is locked in the LevelMinting contract.

Whenever the admin disables the cooldown period, all `lvlUSD` locked for pending redemptions instantly become stuck. A possible fix for this would be to remove the `ensureCooldownOn` modifier from `completeRedeem()`, which allows pending redemptions to be completed even when `cooldownDuration = 0`.

### Level Money
Fixed in commit `628bf291`.

### Cantina
Verified, the `ensureCooldownOn` modifier was removed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Level  Money |
| Report Date | N/A |
| Finders | Delvir0, tchkvsky, MiloTruck, xiaoming90 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_level_money_sep2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/99c7abab-0ff5-4e0e-a796-b1294271ca25

### Keywords for Search

`vulnerability`

