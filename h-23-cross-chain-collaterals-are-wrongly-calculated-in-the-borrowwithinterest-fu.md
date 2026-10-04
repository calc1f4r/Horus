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
solodit_id: 58392
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/908
source_link: none
github_link: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/946

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
finders_count: 26
finders:
  - Allen\_George08
  - Brene
  - x0rc1ph3r
  - xiaoming90
  - m3dython
---

## Vulnerability Title

H-23: Cross-chain collaterals are wrongly calculated in the borrowWithInterest function

### Overview


The bug report discusses an issue with the `borrowWithInterest` function in the LendStorage smart contract. This function is responsible for calculating cross-chain collaterals, which are used in the repayment logic. However, the function is not able to correctly calculate the collaterals, which can lead to incorrect or failed repayments. This is due to a condition in the code that is always false, preventing the cross-chain collaterals from being included in the calculation. This bug can only occur when a user has a cross-chain borrow. The impact of this bug is that the borrowed amount will be incorrectly calculated, potentially leading to failed repayments. The suggested mitigation is to rewrite the condition in the code.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/946 

## Found by 
0x1422, 0xB4nkz, 0xubermensch, 0xzey, Allen\_George08, Brene, JeRRy0422, Kvar, Lamsya, TopStar, Ziusz, algiz, anchabadze, dimah7, dystopia, freeking, gkrastenov, heavyw8t, ivanalexandur, m3dython, mahdifa, oxelmiguel, t.aksoy, x0rc1ph3r, xiaoming90, zxriptor

### Summary

The `borrowWithInterest`  function can not correctly calculate the cross-chain collaterals, which affects the entire repayment logic.

### Root Cause

When a user tries to make a cross-chain borrow from source chain A to destination chain B, their `crossChainBorrows` are stored on chain B, and their `crossChainCollaterals `are stored on chain A. The cross-chain collateral is stored during the `_handleValidBorrowRequest` function:

```solidity
   lendStorage.addCrossChainCollateral(
                payload.sender, // user
                destUnderlying,  // underlying
                LendStorage.Borrow({
                   //@audit-issue srcEid != destEid
                    srcEid: srcEid,
                    destEid: currentEid,
                    principle: payload.amount,
                    borrowIndex: currentBorrowIndex,
                    borrowedlToken: payload.destlToken,
                    srcToken: payload.srcToken
                })
            );
```

When the user tries to repay their borrow, the system checks the sum of the cross-chain collaterals on either side. In the `borrowWithInterest` function, while calculating the total collateral, it checks whether:

https://github.com/sherlock-audit/2025-05-lend-audit-contest/blob/main/Lend-V2/src/LayerZero/LendStorage.sol#L497

```solidity
 if (collaterals[i].destEid == currentEid && collaterals[i].srcEid == currentEid)
```

This condition is always false, because `destEid` is always different from `srcEid`. As a result, the amount stored for cross-chain collaterals is never included in the borrow amount calculation, potentially leading to incorrect or failed repayments.

### Internal Pre-conditions

N/A

### External Pre-conditions

User should have cross-chain borrow.

### Attack Path

N/A, just need to be called `repayCrossChainBorrow` function.

### Impact

An incorrect calculation of the borrowed amount will be made as the cross-chain collateral is not included. This can potentially lead to incorrect or failed repayments.

### PoC

_No response_

### Mitigation

Avoid checking if `collaterals[i].destEid == currentEid && collaterals[i].srcEid == currentEid` is true. This condition should be rewritten.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | LEND |
| Report Date | N/A |
| Finders | Allen\_George08, Brene, x0rc1ph3r, xiaoming90, m3dython, zxriptor, ivanalexur, anchabadze, dystopia, 0xzey, t.aksoy, gkrastenov, TopStar, oxelmiguel, mahdifa, 0xB4nkz, Lamsya, Kvar, dimah7, 0xubermensch, 0x1422, JeRRy0422, heavyw8t, Ziusz, freeking, algiz |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/946
- **Contest**: https://app.sherlock.xyz/audits/contests/908

### Keywords for Search

`vulnerability`

