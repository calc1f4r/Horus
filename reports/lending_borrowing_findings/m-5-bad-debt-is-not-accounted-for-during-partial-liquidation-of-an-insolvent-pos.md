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
solodit_id: 58402
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/908
source_link: none
github_link: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/660

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
finders_count: 5
finders:
  - 0xpetern
  - TessKimy
  - theweb3mechanic
  - rudhra1749
  - ifeco445
---

## Vulnerability Title

M-5: bad debt is not accounted for during partial liquidation of an insolvent position

### Overview


The bug report discusses an issue found in a protocol that allows for partial liquidation of a borrower's position. If a borrower's position is insolvent, a liquidator can liquidate it, resulting in bad debt for the protocol. However, there is currently no mechanism in place to account for this bad debt. This could result in losses for other protocol users. The bug report suggests implementing a mechanism for bad debt accounting as a mitigation strategy.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/660 

## Found by 
0xpetern, TessKimy, ifeco445, rudhra1749, theweb3mechanic

### Summary

https://github.com/sherlock-audit/2025-05-lend-audit-contest/blob/713372a1ccd8090ead836ca6b1acf92e97de4679/Lend-V2/src/LayerZero/CoreRouter.sol#L230-L245
```solidity
    function liquidateBorrow(address borrower, uint256 repayAmount, address lTokenCollateral, address borrowedAsset)
        external
    {
        // The lToken of the borrowed asset
        address borrowedlToken = lendStorage.underlyingTolToken(borrowedAsset);


        LTokenInterface(borrowedlToken).accrueInterest();


        (uint256 borrowed, uint256 collateral) =
            lendStorage.getHypotheticalAccountLiquidityCollateral(borrower, LToken(payable(borrowedlToken)), 0, 0);


        liquidateBorrowInternal(
            msg.sender, borrower, repayAmount, lTokenCollateral, payable(borrowedlToken), collateral, borrowed
        );
    }


```
protocol allows for partial liquidation, if a borrowers position is insolvent then a liquidator can liquidate him leaving bad debt to protocol.And there is no bad debt accounting mechanism in protocol, due to which protocol users should bare this bad debt loss 


### Root Cause

no mechanism to account for bad debt .

### Internal Pre-conditions

none 

### External Pre-conditions

none

### Attack Path

liquidator liquidates a undercollaterized insolvent borrow position due to which bad debt accures.

### Impact

as there is no mechanism to account for bad debt of protocol this loss will be effected to remaining protocol users 

### PoC

_No response_

### Mitigation

implement a mechanism for bad debt accounting

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | LEND |
| Report Date | N/A |
| Finders | 0xpetern, TessKimy, theweb3mechanic, rudhra1749, ifeco445 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/660
- **Contest**: https://app.sherlock.xyz/audits/contests/908

### Keywords for Search

`vulnerability`

