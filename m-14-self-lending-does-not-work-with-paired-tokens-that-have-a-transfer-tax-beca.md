---
# Core Classification
protocol: Peapods
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52766
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/749
source_link: none
github_link: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/300

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
finders_count: 3
finders:
  - pkqs90
  - X77
  - Schnilch
---

## Vulnerability Title

M-14: self-lending does not work with paired tokens that have a transfer tax because addLiquidityV2 does not account for fee-on-transfer on the PAIRED_LP_TOKEN

### Overview


The report discusses a bug in the protocol that prevents self-lending from working with paired tokens that have a transfer tax. This is because the function responsible for adding liquidity does not account for the fee-on-transfer on the paired token. This issue was found by multiple people and has been acknowledged by the protocol. The root cause of the bug is explained, along with the internal and external pre-conditions and the potential attack path. The impact of this bug is that self-lending cannot be used for certain pods, which is an important feature of the protocol.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/300 

The protocol has acknowledged this issue.

## Found by 
Schnilch, X77, pkqs90

### Summary

`addLiquidityV2` transfers PAIRED_LP_TOKEN and pTKN from the address that wants to add liquidity. The issue, however, is that the PAIRED_LP_TOKEN can also be a fee-on-transfer token in a self-lending system where the fTKN is podded. When `addLiquidity` is called on the DEX_HANDLER, there are not enough tokens in the pod, and the call reverts. As a result, the self-lending system cannot be used for PAIRED_LP_TOKEN pods that have transfer tax enabled.

### Root Cause

During `addLeverage` in the `LeverageManager`, the function `addLPAndStake` from `IndexUtils` is used to add liquidity to the UniV2 pool and receive the LP tokens:
https://github.com/sherlock-audit/2025-01-peapods-finance/blob/main/contracts/contracts/IndexUtils.sol#L82-L87
`addLiquidityV2` then transfers the PAIRED_LP_TOKEN and the pTKN into the pod, and uses the DEX_HANDLER to add liquidity:
https://github.com/sherlock-audit/2025-01-peapods-finance/blob/main/contracts/contracts/DecentralizedIndex.sol#L341-L357
The issue here is when it is a self-lending system with a podded fTKN that has transfer tax enabled. In this case, the DEX_HANDLER will revert, as the PAIRED_LP_TOKEN is slightly reduced due to the tax when transferring into the pod. However, the same amount of liquidity is still intended to be added (see lines 345 and 352).


### Internal Pre-conditions

1. hasTransferTax must be true for the paired LP token pod in the self-lending system

### External Pre-conditions

No external pre-conditions

### Attack Path

1. There is pod1 and pod2, where pod2 has the fTKN as its underlying token. Pod2 is the PAIRED_LP_TOKEN of pod1. Pod2 also has a transfer tax enabled.
2. A user now wants to call `addLeverage` with their pTKNs, which they received from bonding in pod1
3. The call fails because there are not enough tokens in pod1 due to the transfer tax in pod2 when liquidity is supposed to be added

### Impact

Self-lending cannot be set up for a PAIRED_LP_TOKEN pod that has transfer tax enabled. As a result, an important feature of the protocol may not be available for certain pods.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Peapods |
| Report Date | N/A |
| Finders | pkqs90, X77, Schnilch |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/300
- **Contest**: https://app.sherlock.xyz/audits/contests/749

### Keywords for Search

`vulnerability`

