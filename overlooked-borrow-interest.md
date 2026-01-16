---
# Core Classification
protocol: Folks Finance X-Chain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47333
audit_firm: OtterSec
contest_link: https://folks.finance/
source_link: https://folks.finance/
github_link: https://github.com/Folks-Finance/audits/blob/13f8d8307902e8ff7018fe9b6df0b5668c638863/OtterSec%20-%20Audit%20of%20XChain%20Lending%20-%20May%202024.pdf

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
  - Robert Chen
  - Woosun Song
  - Matteo Olivia
---

## Vulnerability Title

Overlooked Borrow Interest

### Overview


The liquidation logic in the contract does not account for accrued borrow interest in the violator's debt, resulting in an underestimation of the debt's notional amount. This is because the function that calculates liquidation amounts references the violator's loan balance without updating the borrow index. This oversight leads to an underestimated borrow balance, which affects the accuracy of the repayment amount and may prevent a user from being fully liquidated. To fix this issue, the updateLoanBorrowInterests function should be called before referencing the violator's loan balance. This has been addressed in the latest update of the contract.

### Original Finding Content

## Liquidation Logic Issue

The liquidation logic does not account for borrow interest accrued in the violator debt, resulting in the debt notional amount to be underestimated. This happens because the `calcLiquidationAmounts` function references the `violatorLoanBorrow.balance` variable without updating the borrow index.

> _contracts/hub/logic/LiquidationLogic.sol solidity

```solidity
function calcLiquidationAmounts(
    DataTypes.LiquidationLoansParams memory loansParams,
    mapping(bytes32 => LoanManagerState.UserLoan) storage userLoans,
    mapping(uint16 => LoanManagerState.LoanType) storage loanTypes,
    IHubPool collPool,
    IOracleManager oracleManager,
    uint256 maxRepayBorrowValue,
    uint256 maxAmountToRepay
) external view returns (DataTypes.LiquidationAmountParams memory liquidationAmounts) {
    /* ... */
    LoanManagerState.UserLoanBorrow storage violatorLoanBorrow =
    violatorLoan.borrows[borrPoolId];
    {
        uint256 maxRepayBorrowAmount = Math.mulDiv(maxRepayBorrowValue, MathUtils.ONE_10_DP, 
        borrPrice);
        repayBorrowAmount = Math.min(maxAmountToRepay, Math.min(maxRepayBorrowAmount, 
        violatorLoanBorrow.balance));
    }
    /* ... */
}
```

This oversight results in an underestimated borrow balance to be propagated into `repayBorrowAmount`. The debt of a user `U` is managed by the tuple `(BU, IU)`, where `BU` denotes the balance and `IU` denotes the borrow index. The actual borrow balance is computed by 

\[
\text{BU} \times \frac{\text{IG}}{\text{IU}}
\]

where `IG` denotes a global borrow index. Consequently, `BU` represents the true borrow balance only when the index is up-to-date. Since this condition is not met, `IU < IG` may occur and `BU` may be smaller than the true borrow balance.

Despite this being a significant calculation flaw, we deemed the impact to be moderate because it does not lead to the theft of funds. Instead, the primary consequence is the underestimation of `repayBorrowAmount`, which prevents a user from being fully liquidated.

---

© 2024 Otter Audits LLC. All Rights Reserved. 7/13

## Folks Finance X-Chain Audit 04 — Vulnerabilities Remediation

Call the `updateLoanBorrowInterests` function before referencing `violatorLoanBorrow.balance`.

## Patch
Fixed in e378a26.

---

© 2024 Otter Audits LLC. All Rights Reserved. 8/13

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Folks Finance X-Chain |
| Report Date | N/A |
| Finders | Robert Chen, Woosun Song, Matteo Olivia |

### Source Links

- **Source**: https://folks.finance/
- **GitHub**: https://github.com/Folks-Finance/audits/blob/13f8d8307902e8ff7018fe9b6df0b5668c638863/OtterSec%20-%20Audit%20of%20XChain%20Lending%20-%20May%202024.pdf
- **Contest**: https://folks.finance/

### Keywords for Search

`vulnerability`

