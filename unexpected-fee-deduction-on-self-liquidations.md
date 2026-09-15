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
solodit_id: 35982
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

Unexpected fee deduction on self-liquidations

### Overview


This bug report discusses an issue with the selfLiquidate function in SelfLiquidate.sol, which is designed to allow lenders to liquidate their positions without external involvement. According to the technical documentation, no fees should be charged during this process. However, the current implementation incorrectly charges a fee before computing the collateral to be assigned to the lender, reducing the available collateral. The recommendation is to amend the function to omit charging fees during self-liquidation. The bug has been fixed in a recent commit, but it has not been reviewed yet.

### Original Finding Content

## Vulnerability Report

## Severity
**Medium Risk**

## Context
`SelfLiquidate.sol#L52-L73`

## Description
The `selfLiquidate` function is designed to allow lenders to liquidate their positions without external liquidator involvement, improving protocol health by ensuring timely collateral recovery without profitability for the liquidator. According to the technical documentation section **3.5.3.2 Self Liquidation**, no fees should be charged during this process. However, the current implementation incorrectly charges a repay fee before computing the collateral to be assigned to the lender, thereby reducing the collateral amount available contrary to the documentation.

## Recommendation
Amend the `executeSelfLiquidate` function to omit the charging of fees during the self-liquidation process:

```diff
--- a/src/libraries/fixed/actions/SelfLiquidate.sol
+++ b/src/libraries/fixed/actions/SelfLiquidate.sol
@@ -57,7 +57,7 @@ library SelfLiquidate {
 uint256 credit = creditPosition.credit;
 - uint256 repayFeeProRata = state.chargeRepayFeeInCollateral(debtPosition, credit);
 + uint256 repayFeeProRata = Math.mulDivDown(debtPosition.repayFee, credit,
 debtPosition.faceValue); , !
 uint256 assignedCollateral = state.getCreditPositionProRataAssignedCollateral(creditPosition);
 (uint256 debtProRata, bool isFullRepayment) = debtPosition.getDebtProRata(credit,
 repayFeeProRata); , !
 state.data.debtToken.burn(debtPosition.borrower, debtProRata);
```

## Size
Fixed in commit `a2bafef2`.

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

