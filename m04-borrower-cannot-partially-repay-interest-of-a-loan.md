---
# Core Classification
protocol: Aave Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11609
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/aave-protocol-audit/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - indexes
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M04] Borrower cannot partially repay interest of a loan

### Overview


The `repay` function of the `LendingPool` contract allows borrowers to repay a loan in a specific reserve. Currently, however, it is impossible for a borrower to partially repay the interest of a loan. This is due to the fact that the transaction reverts when the `borrowBalanceIncrease` is greater than the `paybackAmountMinusFees`.

To address this issue, it is suggested that either the necessary logic is implemented to prevent `repay` from reverting when `borrowBalanceIncrease` is greater than the `paybackAmountMinusFees`, or that the intended behavior of the function is explicitly documented in docstrings.

This issue has been fixed in Merge Request #77.

### Original Finding Content

The [`repay` function](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L329) of the `LendingPool` contract allows a borrower to repay a loan in a specific reserve. However, it is currently impossible for the borrower to partially repay the interest of a loan. This is due to the fact that whenever the `borrowBalanceIncrease` is greater than the `paybackAmountMinusFees`, [the transaction will be reverted](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L371).


Should this be the function’s intended behavior, consider explicitly documenting it in docstrings. Otherwise, consider implementing the necessary logic to prevent `repay` from reverting when `borrowBalanceIncrease` is greater than the `paybackAmountMinusFees`, allowing borrowers to partially repay their loan’s interest.


**Update**: *Fixed in [MR#77](https://gitlab.com/aave-tech/dlp/contracts/merge_requests/77/diffs).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Aave Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/aave-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

