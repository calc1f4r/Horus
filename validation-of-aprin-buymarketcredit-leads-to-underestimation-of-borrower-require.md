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
solodit_id: 35979
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Size-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Size-Spearbit-Security-Review.pdf
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
finders_count: 4
finders:
  - 0xLeastwood
  - Slowfi
  - Hyh
  - 0x4non
---

## Vulnerability Title

Validation of APRin BuyMarketCredit leads to underestimation of borrower requirements

### Overview


This bug report is about a problem in the BuyMarketCredit smart contract, which is used for lending operations. The issue is that the code checks if the annual percentage rate (APR) is higher than a certain limit, but it should actually be checking if it is lower than a minimum acceptable rate. This can lead to transactions that don't meet the lender's intended minimum yield. The recommendation is to revise the code to check for the minimum APR and update the error message accordingly. This bug has been fixed in a recent commit. It has been acknowledged by the team, but not yet reviewed.

### Original Finding Content

## Severity: High Risk

## Context
`BuyMarketCredit.sol#L61-L65`

## Description
The implementation of the `BuyMarketCredit` checks if the APR exceeds `maxAPR` to decide whether to proceed with a lending operation. However, the intention, as deduced from the business logic, seems to focus on ensuring that the APR should not fall below a certain threshold, which is beneficial for the lender in terms of returns. The current implementation may lead to transactions that do not satisfy the lender's intended minimum yield.

## Recommendation
Consider revising the conditional check and error message to ensure that the APR does not fall below a defined minimum acceptable rate (`minAPR`).

---

```diff
--- a/src/libraries/fixed/actions/BuyMarketCredit.sol
+++ b/src/libraries/fixed/actions/BuyMarketCredit.sol
@@ -60,8 +60,8 @@ library BuyMarketCredit {
 // validate maxAPR
 uint256 apr = borrowOffer.getAPRByDueDate(state.oracle.variablePoolBorrowRateFeed,
 debtPosition.dueDate); , !
- if (apr > params.maxAPR) {
- revert Errors.APR_GREATER_THAN_MAX_APR(apr, params.maxAPR);
+ if (apr < params.minAPR) {
+ revert Errors.APR_LOWER_THAN_MIN_APR(apr, params.minAPR);
 }
```

## Size
Fixed in commit `0f759ac8`.

## Spearbit
Acknowledged but not reviewed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

