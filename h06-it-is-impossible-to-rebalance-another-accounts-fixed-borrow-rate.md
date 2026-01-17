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
solodit_id: 11602
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

[H06] It is impossible to rebalance another account’s fixed borrow rate

### Overview


This bug report is regarding the `rebalanceFixedBorrowRate` function of the `LendingPool` contract. The issue is that when the function is called, the `msg.sender` address is being passed as an argument instead of the target address defined by the `_user` parameter. This means that successful rebalance calls will only ever update the caller's fixed borrow rates, rather than the intended target address. This breaks the intended feature of being able to rebalance other accounts.

The suggested solution is to change the `msg.sender` address used in line 537 to `_user`. Additionally, two related issues must also be taken into consideration, which are "C04: Rogue borrower can manipulate other account's borrow balance" and "H09: Fixed-rate loans can be repeatedly rebalanced".

The issue has been fixed in Merge Request #61.

### Original Finding Content

In the [`rebalanceFixedBorrowRate` function](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L493) of the `LendingPool` contract, the call to [`core.updateUserFixedBorrowRate`](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L537) is executed passing the `msg.sender` address as argument. As a consequence, successful rebalance calls will only ever update the fixed borrow rates of the caller, rather than the target address defined by the `_user` parameter. This breaks the intended feature of being able to rebalance other accounts.


Consider changing the `msg.sender` address used in [line 537](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L537) to `_user`. Related issues that must also be taken into consideration are [**“[C04] Rogue borrower can manipulate other account’s borrow balance”**](#c04) and [**“[H09] Fixed-rate loans can be repeatedly rebalanced”**](#h09).


**Update**: *Fixed in [MR#61](https://gitlab.com/aave-tech/dlp/contracts/merge_requests/61/diffs).*

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

