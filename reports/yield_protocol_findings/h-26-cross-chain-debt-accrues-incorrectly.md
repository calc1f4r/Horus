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
solodit_id: 58395
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/908
source_link: none
github_link: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/1009

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
finders_count: 6
finders:
  - newspacexyz
  - future
  - JeRRy0422
  - 0xc0ffEE
  - jokr
---

## Vulnerability Title

H-26: Cross chain debt accrues incorrectly

### Overview


This bug report discusses an issue found by multiple users in the LendStorage contract for the Lend protocol. The issue is related to cross chain borrowing, where using the borrow index of an LToken on the same chain can result in incorrect interest being accrued. This is due to a function using the wrong parameters for calculating cross chain borrow interest. This bug can impact cross chain functionality and the accuracy of debt calculations. No response or proof of concept has been provided yet. A possible solution is to change the mechanism for accruing cross chain borrow index.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/1009 

## Found by 
0xc0ffEE, JeRRy0422, future, jokr, newspacexyz, t.aksoy

### Summary

Using the borrow index of LToken on the same chain for cross chain borrow can cause the cross chain borrow to be incorrectly accrued interest

### Root Cause

The function [`LendStorage::borrowWithInterest()` ](https://github.com/sherlock-audit/2025-05-lend-audit-contest/blob/main/Lend-V2/src/LayerZero/LendStorage.sol#L478-L503) is used to calculate cross borrow with interest. However, the parameters `_lToken` actually the LToken on the same chain. The function is accruing cross chain borrow interest **with same-chain LToken borrow index**. This can cause debt calculation of cross chain borrows to be imprecise, hence impacting cross chain functionality.
```solidity
    function borrowWithInterest(address borrower, address _lToken) public view returns (uint256) {
        address _token = lTokenToUnderlying[_lToken];
        uint256 borrowedAmount;

        Borrow[] memory borrows = crossChainBorrows[borrower][_token];
        Borrow[] memory collaterals = crossChainCollaterals[borrower][_token];

        require(borrows.length == 0 || collaterals.length == 0, "Invariant violated: both mappings populated");
        // Only one mapping should be populated:
        if (borrows.length > 0) {
            for (uint256 i = 0; i < borrows.length; i++) {
                if (borrows[i].srcEid == currentEid) {
                    borrowedAmount +=
@>                        (borrows[i].principle * LTokenInterface(_lToken).borrowIndex()) / borrows[i].borrowIndex;
                }
            }
        } else {
            for (uint256 i = 0; i < collaterals.length; i++) {
                // Only include a cross-chain collateral borrow if it originated locally.
                if (collaterals[i].destEid == currentEid && collaterals[i].srcEid == currentEid) {
                    borrowedAmount +=
@>                        (collaterals[i].principle * LTokenInterface(_lToken).borrowIndex()) / collaterals[i].borrowIndex;
                }
            }
        }
        return borrowedAmount;
    }
```

### Internal Pre-conditions

NA

### External Pre-conditions

NA

### Attack Path

NA

### Impact

- Cross chain borrow accrues interest incorrectly
- Cross chain functionalities does not work properly 

### PoC

_No response_

### Mitigation

Consider changing the mechanism to accrue cross chain borrow index

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | LEND |
| Report Date | N/A |
| Finders | newspacexyz, future, JeRRy0422, 0xc0ffEE, jokr, t.aksoy |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/1009
- **Contest**: https://app.sherlock.xyz/audits/contests/908

### Keywords for Search

`vulnerability`

