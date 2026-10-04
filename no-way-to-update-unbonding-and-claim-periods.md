---
# Core Classification
protocol: Liquid Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43680
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm1el4vjp00019d2nzombxfzp
source_link: none
github_link: https://github.com/Cyfrin/2024-09-stakelink

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
finders_count: 7
finders:
  - trtrth
  - KrisRenZo
  - federodes
  - 0xaman
  - 0xTheBlackPanther
---

## Vulnerability Title

No way to update unbonding and claim periods

### Overview

See description below for full details.

### Original Finding Content

## Github

https://github.com/Cyfrin/2024-09-stakelink/blob/f5824f9ad67058b24a2c08494e51ddd7efdbb90b/contracts/linkStaking/FundFlowController.sol#L22-L25

## Summary

The **FundFlowController** contract has hardcoded values for unbonding and claim periods, while **Chainlink** can update these periods in their contracts via setters. This mismatch leads to discrepancies in timing, potentially causing issues with fund withdrawals. As Chainlink changes its periods, **FundFlowController** fails to stay in sync, resulting in delays or incorrect processing of user withdrawals.

## Where it occurs?

This issue arises in the **FundFlowController** contract, specifically in how it handles **unbonding and claim periods**. The contract relies on static time periods, which do not update dynamically when Chainlink modifies its own periods in related contracts.

```Solidity
// duration of the unbonding period in the Chainlink staking contract
uint64 public unbondingPeriod;
// duration of the claim period in the Chainlink staking contract
uint64 public claimPeriod;
```

## Actual Cause

The problem stems from **FundFlowController** using fixed, static time periods for unbonding and claiming, while **Chainlink** contracts have the flexibility to change these periods. The **FundFlowController** records the **start time** of the unbonding process but does not account for changes to the actual **end times** of unbonding and claim periods as set by Chainlink.

## Impact

If Chainlink modifies its unbonding or claim periods, the **FundFlowController** will operate based on outdated assumptions, leading to the following potential issues:

* **Withdrawal Delays**: Users can experience delays in accessing their funds if the actual periods shorten but the controller uses outdated timings.
* **Premature or Incorrect Withdrawals**: If the unbonding or claim periods are extended by Chainlink, withdrawals might be processed too early, resulting in failed transactions or reverted operations.
* **Locked Funds**: Users' funds may remain locked for longer than necessary, reducing liquidity and causing potential dissatisfaction with the system.

## Likelihood

The likelihood of this issue occurring is **low to moderate because** it is dependent on how frequently **Chainlink** modifies its periods. Given the evolving nature of Chainlink's contracts, there is a significant risk that these timing discrepancies will occur unless actively managed.

## Recommendations

1. **Dynamic Period Updates**: Modify the **FundFlowController** to dynamically fetch and synchronize the unbonding and claim periods from Chainlink's contracts, ensuring that the controller always operates based on the current period durations.

2. or better approach is to add setters for these values.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Liquid Staking |
| Report Date | N/A |
| Finders | trtrth, KrisRenZo, federodes, 0xaman, 0xTheBlackPanther |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-09-stakelink
- **Contest**: https://codehawks.cyfrin.io/c/cm1el4vjp00019d2nzombxfzp

### Keywords for Search

`vulnerability`

