---
# Core Classification
protocol: HMX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54578
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/5977ae92-9528-4871-9968-4ef0508ce9b9
source_link: https://cdn.cantina.xyz/reports/cantina_hmx_sep2023.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Riley Holterhus
  - Throttle
  - 0x4non
---

## Vulnerability Title

Permanent reward accrual after liquidation 

### Overview


The bug report is about a problem in a program called LiquidationService.sol. When a certain action, called liquidation, is performed, the program does not properly handle a process called `onDecreasePosition()` which is responsible for managing rewards. This means that users who have their accounts liquidated may not be able to collect rewards properly. The report recommends triggering the `onDecreasePosition()` process during liquidation to fix this issue. The bug has been fixed in a new version of the program.

### Original Finding Content

## LiquidationService.sol

## Description
When a subaccount is liquidated, each position is wound down completely. In normal circumstances, a position being closed would trigger the protocol's `onDecreasePosition()` hooks, but this is missing during liquidation. Currently, these hooks manage rewards accounting. In particular, `TradingStakingHook.onDecreasePosition()` is responsible for removing the position from the staking pool. So, if a position is liquidated, the user can permanently accumulate and harvest rewards.

## Recommendation
Trigger the `onDecreasePosition()` hooks when a subaccount is liquidated.

## HMX
Fixed in PR 304.

## Cantina
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | HMX |
| Report Date | N/A |
| Finders | Riley Holterhus, Throttle, 0x4non |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_hmx_sep2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/5977ae92-9528-4871-9968-4ef0508ce9b9

### Keywords for Search

`vulnerability`

