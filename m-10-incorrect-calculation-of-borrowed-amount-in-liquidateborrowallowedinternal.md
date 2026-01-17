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
solodit_id: 58407
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/908
source_link: none
github_link: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/1019

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
finders_count: 44
finders:
  - newspacexyz
  - HeckerTrieuTien
  - Ruppin
  - Brene
  - DharkArtz
---

## Vulnerability Title

M-10: Incorrect calculation of borrowed amount in liquidateBorrowAllowedInternal

### Overview


This bug report discusses an issue found by multiple contributors that results in an incorrect calculation of borrowed amounts and can lead to incorrect liquidation checks. The root cause of this issue is an insufficient shortfall check when the borrowed amount is greater than the collateral. This is caused by the double application of interest in the calculation of the borrowed amount. This can result in users being incorrectly flagged for liquidation. The suggested mitigation is to avoid double-applying interest and to make sure that the borrowed amount is not adjusted again using the borrow index if it already includes accrued interest.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/1019 

## Found by 
0x23r0, 0xAlix2, 0xEkko, 0xc0ffEE, 0xgee, Brene, DharkArtz, Drynooo, Etherking, FalseGenius, HeckerTrieuTien, Hueber, Kirkeelee, Kvar, PNS, Rorschach, Ruppin, SafetyBytes, Sir\_Shades, Smacaud, Sparrow\_Jac, Tigerfrake, Uddercover, Z3R0, anchabadze, coin2own, crazzyivan, future, ggg\_ttt\_hhh, gkrastenov, good0000vegetable, h2134, jokr, khaye26, kom, newspacexyz, oxelmiguel, patitonar, theboiledcorn, theweb3mechanic, udo, wickie, ydlee, zraxx

### Summary

Double interest applied in borrowed amount calculation causes inflated borrow values and incorrect liquidation checks.

### Root Cause

An insufficient shortfall is checked when `borrowedAmount > collateral`. The  `borrowedAmount` is calculated inside the `liquidateBorrowAllowedInternal `function as follows:

https://github.com/sherlock-audit/2025-05-lend-audit-contest/blob/main/Lend-V2/src/LayerZero/CoreRouter.sol#L348
```solidity
 borrowedAmount =
                (borrowed * uint256(LTokenInterface(lTokenBorrowed).borrowIndex())) / borrowBalance.borrowIndex;
```

The borrowed value passed into this function comes from `liquidateBorrow`, where it is calculated using `getHypotheticalAccountLiquidityCollateral`:

```solidity
        (uint256 borrowed, uint256 collateral) =
            lendStorage.getHypotheticalAccountLiquidityCollateral(borrower, LToken(payable(borrowedlToken)), 0, 0);

        liquidateBorrowInternal(
            msg.sender, borrower, repayAmount, lTokenCollateral, payable(borrowedlToken), collateral, borrowed
        );
```

The function` getHypotheticalAccountLiquidityCollateral` already returns the borrowed amount with accrued interest included, since it internally uses the `borrowWithInterestSame` and `borrowWithInterest` methods.

As a result, when the protocol calculates shortfall, it applies interest a second time by again multiplying the already interest-included borrowed amount by the current borrow index and dividing by the stored index.

This causes the `borrowedAmount` used for shortfall checks to be inflated beyond the actual debt.
### Internal Pre-conditions

N/A

### External Pre-conditions

N/A

### Attack Path

N/A

### Impact

Users may be incorrectly flagged for liquidation due to an artificially high perceived borrow amount.

### PoC

_No response_

### Mitigation

Avoid double-applying interest. If the borrowed amount already includes accrued interest, it should not be adjusted again using the borrow index.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | LEND |
| Report Date | N/A |
| Finders | newspacexyz, HeckerTrieuTien, Ruppin, Brene, DharkArtz, 0xAlix2, udo, wickie, zraxx, patitonar, ydlee, Z3R0, 0x23r0, kom, Drynooo, theweb3mechanic, PNS, Rorschach, Kirkeelee, FalseGenius, anchabadze, 0xgee, future, 0xEkko, theboiledcorn, jokr, Etherking, ggg\_ttt\_hhh, Hueber, h2134, gkrastenov, SafetyBytes, Uddercover, crazzyivan, oxelmiguel, khaye26, Smacaud, Kvar, Sir\_Shades, good0000vegetable, 0xc0ffEE, Sparrow\_Jac, Tigerfrake, coin2own |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/1019
- **Contest**: https://app.sherlock.xyz/audits/contests/908

### Keywords for Search

`vulnerability`

