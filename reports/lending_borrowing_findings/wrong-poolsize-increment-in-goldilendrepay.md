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
solodit_id: 30922
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
github_link: none

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
finders_count: 1
finders:
  - Hans
---

## Vulnerability Title

Wrong `PoolSize` increment in `Goldilend.repay()`

### Overview


The bug report states that when a user repays their loan using the `repay()` function, the `poolSize` variable is increased with the wrong amount. This is because the function uses the wrong amount during the increment. This can cause issues with other functions and the `poolSize` variable will not be tracked correctly. The recommended solution is to update the `poolSize` variable using the correct amount, which is the `interest` variable. The bug has been fixed in a recent update.

### Original Finding Content

**Severity:** High

**Description:** When a user repays his loan using `repay()`, it increases `poolSize` with the repaid interest. During the increment, it uses the wrong amount.

```solidity
  function repay(uint256 repayAmount, uint256 _userLoanId) external {
    Loan memory userLoan = loans[msg.sender][_userLoanId];
    if(userLoan.borrowedAmount < repayAmount) revert ExcessiveRepay();
    if(block.timestamp > userLoan.endDate) revert LoanExpired();
    uint256 interestLoanRatio = FixedPointMathLib.divWad(userLoan.interest, userLoan.borrowedAmount);
    uint256 interest = FixedPointMathLib.mulWadUp(repayAmount, interestLoanRatio);
    outstandingDebt -= repayAmount - interest > outstandingDebt ? outstandingDebt : repayAmount - interest;
    loans[msg.sender][_userLoanId].borrowedAmount -= repayAmount;
    loans[msg.sender][_userLoanId].interest -= interest;
    poolSize += userLoan.interest * (1000 - (multisigShare + apdaoShare)) / 1000; //@audit should use interest instead of userLoan.interest
...
  }
```

It should use `interest` instead of `userLoan.interest` because the user repaid `interest` only.

**Impact:** `poolSize` would be tracked wrongly after calling `repay()` and several functions wouldn't work as expected.

**Recommended Mitigation:** `poolSize` should be updated using `interest`.

**Client:** Fixed in [PR #2](https://github.com/0xgeeb/goldilocks-core/pull/2)

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

