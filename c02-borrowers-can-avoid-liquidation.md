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
solodit_id: 11593
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/aave-protocol-audit/
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

[C02] Borrowers can avoid liquidation

### Overview


This bug report is about the liquidation process of a loan. When a loan is liquidated, the reduction in the remaining principal and the corresponding reduction in the total borrows is calculated by subtracting the accrued interest from the amount to be repaid. This is a combination of two separate operations, but combining them into a single operation causes the transaction to revert whenever the repayment is less than the accrued interest. This could be exploited by borrowers to prevent liquidation by spreading their collateral across many different assets or by allowing their loan to grow until the interest exceeds a certain threshold. To fix this issue, the principal and total borrows are updated in two steps. This bug was fixed in Merge Requests 56 and 58.

### Original Finding Content

When a loan is liquidated, the [reduction in the remaining principal](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPoolLiquidationManager.sol#L152) and the corresponding reduction in the total borrows (either [fixed](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPoolLiquidationManager.sol#L144) or [variable](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPoolLiquidationManager.sol#L146)) is calculated by subtracting the accrued interest from the amount to be repaid.


Conceptually, this is a combination of two separate operations: the accrued interest is added to the principal when constructing the new loan and then the amount repaid is subtracted. However, combining them into a single operation will cause the transaction to revert whenever the repayment is less than the accrued interest.


In addition to preventing valid repayments, this behavior could be exploited by borrowers to prevent liquidation.


Since the size of each liquidation transaction is [restricted by the amount of collateral that can be recovered](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPoolLiquidationManager.sol#L119-125) from the specified reserve, a borrower could spread their collateral across many different assets in order to ensure the maximum liquidation amount is lower than their accrued interest.


Alternatively, the liquidation amount is also [restricted by the protocol’s close factor](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPoolLiquidationManager.sol#L108), which means a user could simply allow their loan to grow until the interest exceeds this threshold. In practice, this will likely take years to occur.


In either case, when a borrower cannot be liquidated they no longer have any incentive to remain collateralized.


Consider updating the principal and total borrows variables in two independent steps that account for the accrued interest and the loan repayment respectively.


**Update**: *Fixed in [MR#56](https://gitlab.com/aave-tech/dlp/contracts/merge_requests/56/diffs) and [MR#58](https://gitlab.com/aave-tech/dlp/contracts/merge_requests/58/diffs). The principal and total borrows are updated in two steps.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

