---
# Core Classification
protocol: LEND
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58387
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/908
source_link: none
github_link: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/831

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
finders_count: 7
finders:
  - FalseGenius
  - ggg\_ttt\_hhh
  - Kvar
  - JeRRy0422
  - jokr
---

## Vulnerability Title

H-18: Incorrect `srcEid` check in `borrowWithInterest()`

### Overview


This bug report discusses an issue with the `borrowWithInterest()` function in the `LendStorage.sol` file. The function incorrectly checks for `srcEid == currentEid` on the source chain, causing it to always return zero for existing cross-chain borrows on Chain A. This is because borrow records store `destEid` as the current chain ID, not `srcEid`. This mismatch causes the function to ignore valid borrows. As a result, cross-chain liquidations are not possible and the borrowed amount is seen as zero, leading to incorrect determinations of liquidation eligibility. No response or mitigation has been provided at this time. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/831 

## Found by 
FalseGenius, JeRRy0422, Kvar, Waydou, ggg\_ttt\_hhh, jokr, rudhra1749

### Summary

NOTE: This is a different issue from the one in the same function involving the line `if (collaterals[i].destEid == currentEid && collaterals[i].srcEid == currentEid)`. That issue concerns chain B, where repayments happen. The issue described here is about the other if statement, which affects chain A, where borrows originate.

`LendStorage.sol#borrowWithInterest()` incorrectly checks `borrows[i].srcEid == currentEid` on the source chain (Chain A), but borrow records store destEid as the current chain ID. This causes the function to always return zero for existing cross-chain borrows on Chain A.

### Root Cause

`LeadStorage.sol#borrowWithInterest()` uses the wrong chain ID field for filtering borrows on the source chain. It checks if `srcEid == currentEid`, which does not match how borrow records are stored. This condition will never be true on chain A (where `userBorrows` exist) because the borrow’s `destEid`  (not `srcEid`) equals the current chain ID. This mismatch causes the function to ignore valid borrows.

When a borrow is stored in `userBorrows`, the `srcEid` is set as Chain B and the `destEid` as Chain A. This happens on Chain A and can be seen [here](https://github.com/sherlock-audit/2025-05-lend-audit-contest/blob/main/Lend-V2/src/LayerZero/CrossChainRouter.sol#L722). In this scenario, `srcEid` corresponds to Chain B while `currentEid` refers to Chain A.

### Internal Pre-conditions

N/A

### External Pre-conditions

N/A

### Attack Path

N/A

### Impact

Calling `borrowWithInterest()` on chain A will always return 0, making cross-chain liquidations impossible. Since `_checkLiquidationValid` is called on chain A, it sees the borrowed amount as zero and incorrectly determines the position is not liquidatable.

### PoC

_No response_

### Mitigation

_No response_

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | LEND |
| Report Date | N/A |
| Finders | FalseGenius, ggg\_ttt\_hhh, Kvar, JeRRy0422, jokr, Waydou, rudhra1749 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/831
- **Contest**: https://app.sherlock.xyz/audits/contests/908

### Keywords for Search

`vulnerability`

