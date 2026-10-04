---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17903
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

One-to-one minting and redeeming operations have di�ferent collateral ratio requirements

### Overview

See description below for full details.

### Original Finding Content

## Patching Report

**Type:** Patching  
**Target:** Throughout  

**Difficulty:** Low  

## Description

`mint1t1FRAX` checks that the global collateral ratio is greater than or equal to the maximum global collateral ratio:

```solidity
require(FRAX.global_collateral_ratio() >= COLLATERAL_RATIO_MAX, "Collateral ratio must be >= 1");
```
Figure 23.1: [contracts/Frax/Pools/FraxPool.sol#179](contracts/Frax/Pools/FraxPool.sol#179)

By contrast, `redeem1t1FRAX` checks that the global collateral ratio is equal to the maximum global collateral ratio:

```solidity
require(FRAX.global_collateral_ratio() == COLLATERAL_RATIO_MAX, "Collateral ratio must be == 1");
```
Figure 23.2: [contracts/Frax/Pools/FraxPool.sol#242](contracts/Frax/Pools/FraxPool.sol#242)

If the collateral ratio ever exceeds the maximum, minting will still be possible but redeeming will not be.

## Exploit Scenario

The global collateral ratio exceeds the maximum global collateral ratio. Alice, a user, can mint FRAX but cannot redeem it until the global collateral ratio decreases to the maximum ratio.

## Recommendations

**Short term:** Ensure that scenarios in which the global collateral ratio exceeds the maximum are handled correctly and consistently, and check the behavior of the system when such scenarios arise. Alternatively, ensure that the ratio can never exceed the maximum, such as by changing `==` to `>=` in `redeem1t1FRAX`.

**Long term:** Check that system values stay within the correct ranges and ensure that the system will not freeze if they exceed those ranges.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels, Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf

### Keywords for Search

`vulnerability`

