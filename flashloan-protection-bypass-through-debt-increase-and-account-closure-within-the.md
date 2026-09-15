---
# Core Classification
protocol: Gearbox
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53771
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Flashloan Protection Bypass Through Debt Increase and Account Closure Within The Same Block

### Overview


The report states that there is a bug in the system that allows users to bypass the flashloan attack protection mechanism. This means that users are able to take out loans without paying any fees, which is not intended. The bug can be exploited in two ways, either by making multiple transactions in the same block or by taking advantage of a lack of checks during the closing of credit accounts. To fix this issue, the development team has made some changes, but the bug is still partially present. They have acknowledged this and deemed it an acceptable risk. 

### Original Finding Content

## Description

It is possible to bypass the flashloan attack protection. While the existing flashloan attack protection mechanism prevents users from opening and closing credit accounts within the same transaction (block), this check does not prevent users from increasing their debt position beyond the limits of their collateralization ratio (up to `maxBorrowedAmount`) and closing the account within the same transaction. This acts as a fee-less flashloan for borrowers. 

Specifically, there are two ways to exploit this vulnerability:

- By calling functions of adding collateral, increasing debt, and closing credit account sequentially, in the same block (e.g., when called as a single function from an external contract).
- By exploiting the lack of collateral checks during the `_multicall()` operations in `CreditManager.closeCreditAccount()`, as the pool is assumed to be repaid, and non-underlying assets are assumed to be transferred by the end of the transaction.

## Recommendations

- Implement checks to ensure `increaseDebt()` and `closeCreditAccount()` are not executed in the same block.
- Alter the logic of `CreditFacade._multicall()` to limit its capabilities during account closures.

## Resolution

The development team partially mitigated this issue in commit `bdbabc`. Internal calls within `_multiCall()` are reverted when called via `closeCreditAccount()`, preventing the second flashloan scenario. 

The possibility for the first of the two scenarios detailed above still exists (bypassing `multicall()`). This has been acknowledged by Gearbox in a blog post and determined to be an acceptable risk.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Gearbox |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf

### Keywords for Search

`vulnerability`

