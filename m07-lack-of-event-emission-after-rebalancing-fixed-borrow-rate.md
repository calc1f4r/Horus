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
solodit_id: 11612
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

[M07] Lack of event emission after rebalancing fixed borrow rate

### Overview


This bug report is about the `rebalanceFixedBorrowRate` function in the `LendingPool` contract, which allows users to rebalance the fixed interest rate of a user. The issue is that the function does not emit an event after the rebalancing is executed. This is important for users to be notified about the change, so a `RebalanceStableBorrowRate` event was defined and emitted after successful rebalances of stable-rate loans. The bug has been fixed in Merge Request #80.

### Original Finding Content

The [`rebalanceFixedBorrowRate` function](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L493) in the `LendingPool` contract allows anyone to rebalance the fixed interest rate of a user under specific circumstances. However, the function does not emit an event after the rebalancing is executed.


As such a sensitive change is of utter importance to users, consider defining and emitting an event in order to notify clients about it.


**Update**: *Fixed in [MR#80](https://gitlab.com/aave-tech/dlp/contracts/merge_requests/80/diffs). A `RebalanceStableBorrowRate` event has been defined and is now emitted after successful rebalances of stable-rate loans.*

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

