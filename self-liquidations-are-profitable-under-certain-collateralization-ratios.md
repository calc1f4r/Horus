---
# Core Classification
protocol: Size v1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35980
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Size-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Size-Spearbit-Security-Review.pdf
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
finders_count: 4
finders:
  - 0xLeastwood
  - Slowfi
  - Hyh
  - 0x4non
---

## Vulnerability Title

Self liquidations are profitable under certain collateralization ratios

### Overview


This bug report discusses an issue with the SelfLiquidate function in the SelfLiquidate.sol file. The report states that there may be a possibility for a creditor to profit from a self-liquidation by exploiting a specific eligibility condition. The report suggests updating the parameter for calculating debtInCollateralToken to ensure that self-liquidation only occurs when the position is undercollateralized. The report also mentions two commits that have been made to address the issue. 

### Original Finding Content

## Security Audit Report

## Severity
**Medium Risk**

## Context
`SelfLiquidate.sol#L31-L44`

## Description
The specific eligibility for a self-liquidation as per the spec is when `debtInCollateralToken` exceeds the total collateral allocated to the credit position. Assuming there is only one lender, it seems possible that a creditor could self-liquidate and profit from liquidation because `debtInCollateralToken` considers the debt position's total debt and not just `debtPosition.faceValue`.

```solidity
function validateSelfLiquidate(State storage state, SelfLiquidateParams calldata params) external view {
    CreditPosition storage creditPosition = state.getCreditPosition(params.creditPositionId);
    DebtPosition storage debtPosition = state.getDebtPositionByCreditPositionId(params.creditPositionId);
    uint256 assignedCollateral = state.getCreditPositionProRataAssignedCollateral(creditPosition);
    uint256 debtInCollateralToken = state.debtTokenAmountToCollateralTokenAmount(debtPosition.getTotalDebt());

    // validate creditPositionId
    if (!state.isCreditPositionSelfLiquidatable(params.creditPositionId)) {
        revert Errors.LOAN_NOT_SELF_LIQUIDATABLE(
            params.creditPositionId,
            state.collateralRatio(debtPosition.borrower),
            state.getLoanStatus(params.creditPositionId)
        );
    }
    if (!(assignedCollateral < debtInCollateralToken)) {
        revert Errors.LIQUIDATION_NOT_AT_LOSS(params.creditPositionId, assignedCollateral, debtInCollateralToken);
    }
    // validate msg.sender
    if (msg.sender != creditPosition.lender) {
        revert Errors.LIQUIDATOR_IS_NOT_LENDER(msg.sender, creditPosition.lender);
    }
}
```
In practice, self-liquidations are profitable for creditors when total debt is within the range (assuming there is only a single creditor):

```
state.debtTokenAmountToCollateralTokenAmount(creditPosition.credit) < assignedCollateral < debtInCollateralToken
```

Creditors profit on the collateral that is required to back the debt position's `repayFee` and `overdueLiquidatorReward`. The total profit for creditors is strictly limited to:

```
0 < liquidationProfit < state.debtTokenAmountToCollateralTokenAmount(debtPosition.repayFee + debtPosition.overdueLiquidatorReward)
```

## Recommendation
Consider updating the parameter for calculating `debtInCollateralToken` via `state.debtTokenAmountToCollateralTokenAmount(debtPosition.getTotalDebt())` to be `debtPosition.faceValue` instead. This ensures that a self-liquidation is only ever eligible when the position is undercollateralized. In all other cases, standard liquidations should be incentivized.

## Size
**Fixed:**

1. Commit `420b4061` replaces `repayFee` by `swapFee`, which is charged when a loan is generated.
2. Commit `bfdabea4` removes `overdueLiquidatorReward`.

## Spearbit
Acknowledged but not reviewed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Size v1 |
| Report Date | N/A |
| Finders | 0xLeastwood, Slowfi, Hyh, 0x4non |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Size-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Size-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

