---
# Core Classification
protocol: Filament
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45604
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
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
  - Zokyo
---

## Vulnerability Title

Fees are wrongly accrued when reducing collateral.

### Overview


This bug report is about a critical issue in the `_reduceCollateral()` function in the `TradeFacet.sol` smart contract. This function is used when a user decreases their position. The bug occurs when the fee does not need to be paid and the fundingFee is greater than or equal to the borrowingInterest. The current implementation is incorrect and needs to be fixed. The recommended fix is to change the last case to `fee = toNegativeInt256(fundingfee - borrowingInterest)`. This bug has been resolved.

### Original Finding Content

**Severity**: Critical	

**Status**: Resolved

**Description**

The function `_reduceCollateral()` within the `TradeFacet.sol` smart contract is called when a user decreases a position, this function gets the `fundingFee` and if it needs to be paid:
```solidity
(uint256 fundingfee, bool tobePaid) = IFormula(s.formula).getFundingFee(
           position._indexToken, position.size, position.entryFundingRate, position.isLong
       );

       if (tobePaid) {
           fee = int256(borrowingInterest + fundingfee);
       } else {
           if (borrowingInterest > fundingfee) {
               fee = int256(borrowingInterest - fundingfee);
           } else {
               fee = toNegativeInt256(fundingfee + borrowingInterest);
           }
       }
```

The function differentiates several cases, however, the case when the fee does not have to be paid and the fundingFee is greater or equal to the borrowingInterest is wrongly implemented.

**Recommendation**:

Fix the last case with the correct implementation:
`fee = toNegativeInt256(fundingfee - borrowingInterest);`

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Filament |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

