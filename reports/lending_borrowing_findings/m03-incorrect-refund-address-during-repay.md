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
solodit_id: 11608
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

[M03] Incorrect refund address during repay

### Overview


This bug report is about the `repay` function of the Aave lending pool contracts. This function allows repayment of a loan on behalf of other accounts. In a scenario where the caller overpays Ether on behalf of another account, the function will refund the excess Ether to the target address and not the caller. The bug report suggested that all excess Ether should be returned to the actual repayer and not the account on whose behalf the loan is being repaid. This issue has been fixed in Merge Request #76, where all excess Ether is now returned to the actual repayer (i.e. the caller).

### Original Finding Content

The [`repay` function](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L329) allows repayment of a loan on behalf of other accounts. In a scenario where the caller overpays Ether on behalf of another account, the function will [refund the excess Ether](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPoolCore.sol#L692-694) to the target address (*i.e.* the address passed in the [`_onBehalfOf` parameter](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L332)) and not the caller.


Whenever a loan is overpaid with Ether, consider returning all excess Ether to the actual repayer and not the account on whose behalf the loan is being repaid.


**Update**: *Fixed in [MR#76](https://gitlab.com/aave-tech/dlp/contracts/merge_requests/76/diffs). All excess Ether is now returned to the actual repayer (i.e. the caller).*

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

