---
# Core Classification
protocol: Autonomint Colored Dollar V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45527
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/1031

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
finders_count: 1
finders:
  - John44
---

## Vulnerability Title

M-37: Health ratio is hardcoded causing issues once the LTV is updated

### Overview


This bug report discusses an issue in the code of a protocol called Autonomint Judging. The issue was found by a user named John44 and it involves the health ratio being hardcoded in several places. The health ratio is used to determine whether a borrower can be liquidated, but the problem is that the protocol's LTV (loan-to-value) is intended to increase over time. This means that the hardcoded health ratio of 80% will become insufficient once the LTV grows. As a result, debt positions will not be liquidatable even when they are insolvent, which can lead to bad debt for the protocol. The bug report suggests that the health ratio should be modifiable to account for the increasing LTV. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/1031 

## Found by 
John44

### Summary

The current LTV of the protocol is 80% and is intended to increase as much as possible once the protocol matures (as stated in the docs). The issue is that the health ratio of borrow positions is hardcoded in several places causing issues once the LTV is actually updated.

### Root Cause

In BorrowLib and in borrowLiquidation the health ratio of a position is hardcoded to 8000 = 80%. This is because the initial LTV of a deposit will be 80%. The health ratio is used to make sure that a withdrawer cannot withdraw their collateral if they are eligible for liquidation and more importantly to determine whether a borrower can be liquidated. The issue is that the LTV is intended to grow, therefore if the LTV grows for example to 90%, a hardcoded health ratio of only 80% will be insufficient.

https://github.com/sherlock-audit/2024-11-autonomint/blob/0d324e04d4c0ca306e1ae4d4c65f0cb9d681751b/Blockchain/Blockchian/contracts/lib/BorrowLib.sol#L501
https://github.com/sherlock-audit/2024-11-autonomint/blob/0d324e04d4c0ca306e1ae4d4c65f0cb9d681751b/Blockchain/Blockchian/contracts/lib/BorrowLib.sol#L822
https://github.com/sherlock-audit/2024-11-autonomint/blob/0d324e04d4c0ca306e1ae4d4c65f0cb9d681751b/Blockchain/Blockchian/contracts/Core_logic/borrowLiquidation.sol#L191
https://github.com/sherlock-audit/2024-11-autonomint/blob/0d324e04d4c0ca306e1ae4d4c65f0cb9d681751b/Blockchain/Blockchian/contracts/Core_logic/borrowLiquidation.sol#L336

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

1. After some time the LTV is increased to 90%, thus the debt of borrowers will be worth 90% of their collateral.
2. However, as the health ratio is hardcoded to 80%, the only way for a borrower to be liquidated is if their collateral decreases it's value by 20%, instead of 10%.
3. Therefore, debt positions will always be heavily insolvent before they can be liquidated, increasing the risks of bad debt accruing to the protocol.

### Impact

Once the LTV is increased, the health ratio will remain the same, causing debt positions to not be liquidatable even when they are insolvent, accruing bad debt to the protocol.

### PoC

_No response_

### Mitigation

The health ratio should be modifiable in order to account for the increasing LTV.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | John44 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/1031
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

