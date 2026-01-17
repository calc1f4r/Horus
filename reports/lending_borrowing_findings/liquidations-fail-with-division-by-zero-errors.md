---
# Core Classification
protocol: Term Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26294
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/term-finance/term1/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/term-finance/term1/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Liquidations fail with "Division by Zero" errors

### Overview


This bug report is about an error that occurs during complete liquidations in a system. The error is a "Division by Zero" error due to the calculations referring to the repaid balance. At the end of the batchLiquidation() function, a function _withinNetExposureCapOnLiquidation() is called, which uses the function termRepoServicer.getBorrowerRepurchaseObligation(borrower) in its calculations. This function will always be 0 when a complete liquidation occurs, causing the calculations to fail with a division by zero error, reverting the liquidation transaction and disabling the ability to fully liquidate the account. 

The recommendation is to modify _withinNetExposureCapOnLiquidation() to recognise borrower’s repurchase obligation being 0. This can be done by adding an if statement to the beginning of the function to return true if the borrower has no repurchase obligation. This will avoid the division by zero error and all the unnecessary calculations. After the implementation of the recommendation, the issue was resolved and complete liquidations no longer fail with "Division by Zero".

### Original Finding Content

## Description

Complete liquidations always fail with a "Division by Zero" error due to the calculations referring to the repaid balance. At the end of `batchLiquidation()`, a function `_withinNetExposureCapOnLiquidation()` is called, which uses the following in its calculations:

```solidity
uint256 getBorrowerRepurchaseObligation = termRepoServicer.getBorrowerRepurchaseObligation(borrower);
// ...snip...
div_(
    excessEquity,
    termPriceOracle.usdValueOfTokens(
        purchaseToken,
        termRepoServicer.getBorrowerRepurchaseObligation(borrower)
    )
);
```

For a complete liquidation, `getBorrowerRepurchaseObligation()` will always be 0 as, during liquidations, the call to `termRepoServicer.liquidatorCoverExposure()` on line [339], will reduce the borrower’s repurchase obligation to zero. The above snippet of code will then always fail with division by 0, reverting the liquidation transaction and disabling the ability to fully liquidate the account.

## Recommendations

Modify `_withinNetExposureCapOnLiquidation()` to recognize the borrower’s repurchase obligation being 0. This could be achieved by adding the following at the beginning of the `_withinNetExposureCapOnLiquidation()` function:

```solidity
uint256 getBorrowerRepurchaseObligation = termRepoServicer.getBorrowerRepurchaseObligation(borrower);

if (getBorrowerRepurchaseObligation == 0) { 
    return true; // <= New code 
}
```

If the borrower has no repurchase obligation, they must be within the levels defined by `netExposureCapOnLiquidation`, and so it is safe to return true and avoid both the division by zero and all the unnecessary calculations.

## Resolution

Based on a retest of commit `e883f0e`, the issue has been resolved - complete liquidations now do not fail with "Division by Zero".

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Term Finance |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/term-finance/term1/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/term-finance/term1/review.pdf

### Keywords for Search

`vulnerability`

