---
# Core Classification
protocol: Yieldoor
chain: everychain
category: uncategorized
vulnerability_type: liquidation

# Attack Vector Details
attack_type: liquidation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55035
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/791
source_link: none
github_link: https://github.com/sherlock-audit/2025-02-yieldoor-judging/issues/158

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
  - liquidation

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - 0x73696d616f
  - future2\_22
  - iamnmt
---

## Vulnerability Title

H-4: Base calculation in `Leverager::isLiquidateable()` is incorrect as the max leverage may be smaller

### Overview


Summary: 

The bug report discusses an issue with the calculation of base amount in the `Leverager::isLiquidateable()` function. The max leverage used in the calculation may not be accurate, leading to an underestimation of the base amount and potentially not liquidating users when necessary. The root cause of the issue is the lack of consideration for the max leverage from the lending pool. This bug can result in losses for the protocol and an increased risk of bad debt. A proof of concept is provided and the suggested mitigation is to compare the max leverage values and use the smaller one in the calculation.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-02-yieldoor-judging/issues/158 

## Found by 
0x73696d616f, future2\_22, iamnmt

### Summary

Base calculation in `Leverager::isLiquidateable()` is:
`uint256 base = owedAmount * 1e18 / (vp.maxTimesLeverage - 1e18);`.
However, the max leverage may not actually be `vp.maxTimesLeverage`, but [be](https://github.com/sherlock-audit/2025-02-yieldoor/blob/main/yieldoor/src/Leverager.sol#L467) `maxLevTimes` from the lending pool. In this case, the base amount would be incorrectly underestimated, leading to users not being liquidated when they should for the protocol's loss (loss of profit and higher bad debt risk).

### Root Cause

In `Leverager:408`, the max leverage from the lending pool is not taken into account.

### Internal Pre-conditions

`maxLevTimes` from the lending pool < `vp.maxTimesLeverage`.

### External Pre-conditions

None.

### Attack Path

1. User has a position that should be liquidated but isn't due to the rhs of the is liquidatable check.

### Impact

Protocols takes losses and risks bad debt creation.

### PoC

If `maxLevTimes` < `vp.maxTimesLeverage`, it means the base calculation would have in the divisor a bigger number than it should, so base will be smaller. As base is smaller, the collateral of the user can decrease more without the user being liquidated.

### Mitigation

Compare the 2 max leverage values and use the smallest, which is the actual maximum leverage allowed in the `Leverager`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Yieldoor |
| Report Date | N/A |
| Finders | 0x73696d616f, future2\_22, iamnmt |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-02-yieldoor-judging/issues/158
- **Contest**: https://app.sherlock.xyz/audits/contests/791

### Keywords for Search

`Liquidation`

