---
# Core Classification
protocol: Union Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25597
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-10-union
source_link: https://code4rena.com/reports/2021-10-union
github_link: https://github.com/code-423n4/2021-10-union-findings/issues/21

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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-04] Change in interest rate can disable repay of loan

### Overview


This bug report is about the `InterestRateModel` in the `UToken` contract. It has been discovered that the ability of a borrower to repay a loan can be disabled if the interest rate is set too high. This issue could be used by the `FixedInterestRateModel` owner to disable the repay functionality for some time and later demand a higher interest rate from the borrower. 

The bug is caused by the lack of a check when setting the interest rate in `FixedInterestRateModel.sol`, as well as an indication in the specs of this behavior. The function `UToken::accrueInterest()` fetches the current borrow rate of the interest rate model, which requires a not "absurdly high" rate or fails otherwise. 

The recommended mitigation step is to disallow setting the interest rate too high with a check in `FixedInterestRateModel::setInterestRate()`. This finding has been confirmed by kingjacob (Union) and commented on by GalloDaSballo (judge), who agree with the need for a check on the `setInterestRate` function since the warden showed a specific way to negate certain protocol functionality. The finding has been rated as medium severity.

### Original Finding Content

_Submitted by pmerkleplant_

#### Impact
The ability of a borrower to repay a loan is disabled if the interest rate is
set too high by the `InterestRateModel`.

However, there is neither a check when setting the interest rate nor an
indication in the `IInterestRateModel`'s specs of this behavior.

But this issue could also be used in an adversarial fashion by the
`FixedInterestRateModel`-owner if he/she would disable the repay functionality
for some time and enables it at a later point again with the demand of a
higher interest to be paid by the borrower.

#### Proof of Concept
If an account wants to repay a loan, the function
`UToken::_repayBorrowFresh()` is used. This function calls
`UToken::accrueInterest()` ([line](https://github.com/code-423n4/2021-10-union/blob/main/contracts/market/UToken.sol#L465) 465)
which fetches the current borrow rate of the interest rate model
([line](https://github.com/code-423n4/2021-10-union/blob/main/contracts/market/UToken.sol#L546) 546
and [line](https://github.com/code-423n4/2021-10-union/blob/main/contracts/market/UToken.sol#L330) 330).

The function `UToken::borrowRatePerBlock()` requires an not "absurdly high"
rate, or fails otherwise ([line](https://github.com/code-423n4/2021-10-union/blob/main/contracts/market/UToken.sol#L331) 331).

However, there is no check or indicator in `FixedInterestRateModel.sol` to
prevent the owner to set such a high rate that effectively disables repay
of borrowed funds ([line](https://github.com/code-423n4/2021-10-union/blob/main/contracts/market/FixedInterestRateModel.sol#L36) 36).

#### Recommended Mitigation Steps
Disallow setting the interest rate too high with a check in
`FixedInterestRateModel::setInterestRate()`.

**[kingjacob (Union) confirmed](https://github.com/code-423n4/2021-10-union-findings/issues/21)**

**[GalloDaSballo (judge) commented](https://github.com/code-423n4/2021-10-union-findings/issues/21#issuecomment-966425305):**
 > Agree with the need for a check on the `setInterestRate` function
> Since the warden showed a specific way to negate certain protocol functionality, under specific assumptions, the finding is of medium severity



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Union Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-union
- **GitHub**: https://github.com/code-423n4/2021-10-union-findings/issues/21
- **Contest**: https://code4rena.com/reports/2021-10-union

### Keywords for Search

`vulnerability`

