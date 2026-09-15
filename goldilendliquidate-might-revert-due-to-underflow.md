---
# Core Classification
protocol: Goldilocks
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30931
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
github_link: none

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
  - Hans
---

## Vulnerability Title

`Goldilend.liquidate()` might revert due to underflow

### Overview


This bug report describes a medium severity issue in the `repay()` function of the `Goldilocks Core` contract. The issue is related to a rounding error in the calculation of `interest`, which can result in incorrect values for `outstandingDebt`. This can lead to the `liquidate()` function reverting due to an underflow error. The recommended mitigation for this issue is to update the `outstandingDebt` variable in the `liquidate()` function. This issue has been fixed in the latest version of the contract. 

### Original Finding Content

**Severity:** Medium

**Description:** In `repay()`, there would be a rounding during the `interest` calculation.

```solidity
  function repay(uint256 repayAmount, uint256 _userLoanId) external {
      Loan memory userLoan = loans[msg.sender][_userLoanId];
      if(userLoan.borrowedAmount < repayAmount) revert ExcessiveRepay();
      if(block.timestamp > userLoan.endDate) revert LoanExpired();
      uint256 interestLoanRatio = FixedPointMathLib.divWad(userLoan.interest, userLoan.borrowedAmount);
L425  uint256 interest = FixedPointMathLib.mulWadUp(repayAmount, interestLoanRatio); //@audit rounding issue
      outstandingDebt -= repayAmount - interest > outstandingDebt ? outstandingDebt : repayAmount - interest;
      ...
  }
...
  function liquidate(address user, uint256 _userLoanId) external {
      Loan memory userLoan = loans[msg.sender][_userLoanId];
      if(block.timestamp < userLoan.endDate || userLoan.liquidated || userLoan.borrowedAmount == 0) revert Unliquidatable();
      loans[user][_userLoanId].liquidated = true;
      loans[user][_userLoanId].borrowedAmount = 0;
L448  outstandingDebt -= userLoan.borrowedAmount - userLoan.interest;
      ...
  }
```

Here is a possible scenario.
- There are 2 borrowers of `borrowedAmount = 100, interest = 10`. And `outstandingDebt = 2 * (100 - 10) = 180`.
- The first borrower calls `repay()` with `repayAmount = 100`.
- Due to the rounding issue at L425, `interest` is 9 instead of 10. And `outstandingDebt = 180 - (100 - 9) = 89`.
- In `liquidate()` for the second borrower, it will revert at L448 because `outstandingDebt = 89 < borrowedAmount - interest = 90`.

**Impact:** `liquidate()` might revert due to underflow.

**Recommended Mitigation:** In `liquidate()`, `outstandingDebt` should be updated like the below.

```diff
  /// @inheritdoc IGoldilend
  function liquidate(address user, uint256 _userLoanId) external {
    Loan memory userLoan = loans[msg.sender][_userLoanId];
    if(block.timestamp < userLoan.endDate || userLoan.liquidated || userLoan.borrowedAmount == 0) revert Unliquidatable();
    loans[user][_userLoanId].liquidated = true;
    loans[user][_userLoanId].borrowedAmount = 0;
+  uint256 debtToRepay = userLoan.borrowedAmount - userLoan.interest;
+  outstandingDebt -= debtToRepay > outstandingDebt ? outstandingDebt : debtToRepay;
   ...
  }
```

**Client:** Fixed in [PR #10](https://github.com/0xgeeb/goldilocks-core/pull/10)

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Goldilocks |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

