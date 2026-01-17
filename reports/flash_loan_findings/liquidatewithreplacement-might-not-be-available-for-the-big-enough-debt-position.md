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
solodit_id: 35981
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

LiquidateWithReplacement might not be available for the big enough debt positions

### Overview


This bug report discusses a potential issue with the liquidateWithReplacement function in the LiquidateWithReplacement.sol and Size.sol files. It is assumed that there will always be a borrower with enough collateral to cover the debt being liquidated, but this may not always be the case. The report suggests introducing the possibility for multiple borrowers to cover the debt instead. The bug has been acknowledged by the team, but has not yet been reviewed or addressed.

### Original Finding Content

## Severity: Medium Risk

## Context
- `LiquidateWithReplacement.sol#L113-L122`
- `Size.sol#L228-L238`

## Description
The `liquidatorProfitBorrowAsset` can be substantial for the biggest debt positions, but it is assumed that the corresponding big enough `params.borrower` will always be found. This means that there exists one position that has both an eligible offer and enough free collateral to cover the entire debt position being liquidated at once:
- `Size.sol#L228-L238`

```solidity
function liquidateWithReplacement(LiquidateWithReplacementParams calldata params) 
// ...
{
    state.validateLiquidateWithReplacement(params);
    (liquidatorProfitCollateralAsset, liquidatorProfitBorrowAsset) = 
    state.executeLiquidateWithReplacement(params); 

    state.validateUserIsNotBelowOpeningLimitBorrowCR(params.borrower); // <<
}
```

This might not be the case for prolonged periods of time. Creating such a position in a flash loan manner is not possible since the new debt position has to stay. Thus, a usual Liquidate -> Withdraw might be performed instead, which is compatible with flash borrowing of the face value and selling the collateral proceeds while repaying the loan atomically. In this scenario, there are no additional position existence requirements. 

As a result, the protocol may deprive itself of `liquidatorProfitBorrowAsset` in some cases when it is the largest.

## Recommendation
Consider introducing the possibility to supply a number of borrowers who can cumulatively cover the liquidated debt position (e.g., similarly to treating receivables in `BorrowAsMarketOrder`, `BorrowAsMarketOrder.sol#L124-L152`).

## Size
Acknowledged. This was a known limitation, and since `liquidateWithReplacement` is not vital, we will revise this feature in a future version of the protocol.

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

