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
solodit_id: 11616
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

[M11] Miscalculation of requested borrow amount in ETH

### Overview


In the `LendingPool` contract of Aave, there is an issue present in the `borrow` function which causes the calculated borrow amount in ETH to be lower than expected. The issue is that the borrow fee is only calculated *after* it is first used. This means that when the requested borrow amount in ETH is calculated, the `vars.borrowFee` variable is zero. As a consequence, the calculated borrow amount in ETH will be lower than expected, inevitably lowering the actual amount of collateral needed in ETH to accept the borrow operation.

To fix this issue, the `borrow` function should be refactored so that the borrow fee is first calculated, and then the `vars.borrowFee` variable is used for further operations. This issue should have been caught if the `borrow` function and its calculations were thoroughly tested. The issue has now been fixed in Merge Request #116.

### Original Finding Content

*Note for the reader: This issue was detected during our review of the fixes for the first audit round. The specific commit where the issue was introduced is [`8521bcd`](https://gitlab.com/aave-tech/dlp/contracts/commit/8521bcd6aeee58d57ae4f0eb57b84ef4e0224fce), which was not present in the audited commit. It must be noted that [the PR that finally merged this commit](https://gitlab.com/aave-tech/dlp/contracts/merge_requests/34) to the `master` branch was created and merged by the same author, without any kind of peer-review nor CI testing process. The commit to which we link in the issue’s description is the latest in the `master` branch at the moment of writing.*


To validate whether there is enough collateral to cover a borrow, the [`borrow` function](https://gitlab.com/aave-tech/dlp/contracts/blob/cf3ba5c501c58efa1d45f4ed9d9e70debff75230/contracts/lendingpool/LendingPool.sol#L211) of the `LendingPool` contract first [calculates how much ETH the amount borrowed represents](https://gitlab.com/aave-tech/dlp/contracts/blob/cf3ba5c501c58efa1d45f4ed9d9e70debff75230/contracts/lendingpool/LendingPool.sol#L253-255). This calculation is intended to take into account the borrow fee paid by the borrower. However, the borrow fee is only [calculated *after* it is first used](https://gitlab.com/aave-tech/dlp/contracts/blob/cf3ba5c501c58efa1d45f4ed9d9e70debff75230/contracts/lendingpool/LendingPool.sol#L303-306). This means that when the requested borrow amount in ETH is calculated, the `vars.borrowFee` variable is zero. As a consequence, the calculated borrow amount in ETH will be lower than expected, inevitably lowering the actual amount of collateral needed in ETH to accept the borrow operation.


Consider refactoring the `borrow` function to first calculate the borrow fee, and only then using the `vars.borrowFee` variable for further operations. Note that this issue should have been caught if the `borrow` function and its calculations were thoroughly tested (as suggested throughout our original assessment).


**Update**: *Fixed in [MR#116](https://gitlab.com/aave-tech/dlp/contracts/merge_requests/116/diffs).*

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

