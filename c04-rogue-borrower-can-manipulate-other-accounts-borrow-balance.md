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
solodit_id: 11595
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

[C04] Rogue borrower can manipulate other account’s borrow balance

### Overview


The `rebalanceFixedBorrowRate` function of the `LendingPool` contract is intended to allow anyone to rebalance the fixed interest rate of a borrower when certain requirements are met. However, when querying the borrow balances, the function calls the `getUserBorrowBalances` function mistakenly passing `msg.sender` as the argument. This has resulted in two attack vectors where malicious borrowers can exploit this vulnerability to manipulate another borrower’s borrow balance or distort their own accrued interest. 

To prevent malicious borrowers from exploiting this vulnerability, the argument passed to the `getUserBorrowBalances` function should be replaced with `_user`. This issue is closely tied to the critical issue “Fixed-rate loans can be repeatedly rebalanced” and high severity issue “It is impossible to rebalance another account’s fixed borrow rate”. This has been fixed in Merge Request #61.

### Original Finding Content

The [`rebalanceFixedBorrowRate` function](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L493) of the `LendingPool` contract is intended to allow anyone to rebalance the fixed interest rate of a borrower when certain requirements are met. All the caller needs to specify is the reserve (in the `_reserve` parameter) and the borrower’s account to be rebalanced (in the `_user` parameter).


[When querying the borrow balances](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L500-502), the function calls the [`getUserBorrowBalances` function](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPoolCore.sol#L499) mistakenly passing `msg.sender` as the argument. Consequently, the `compoundedBalance` and `balanceIncrease` local variables will hold the caller’s borrow balances, and not those of the account to be rebalanced (*i.e.* the address in `_user`). From then on, `balanceIncrease` is used to update the reserve’s data. It is fundamental to note that on [line 514](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L514) the [`increaseUserPrincipalBorrowBalance` function](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPoolCore.sol#L288) increases the `_user`‘s borrow balance by `balanceIncrease`.


Any rogue borrower whose [`compoundedBalance` is greater than zero](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L505-507) can leverage this critical vulnerability to manipulate another borrower’s borrow balance. An attacker holding a large borrow can call `rebalanceFixedBorrowRate` with the victim’s address as the `_user` parameter. Thus increasing the victim’s principal borrow balance.


The attacker can further benefit by particularly targeting accounts close to being liquidated. The increase in their borrow balance would effectively push victims into a “liquidatable” position, allowing the attacker to liquidate them. To prevent front-runs from other liquidators, this attack can be conducted in a single atomic transaction through a malicious contract that first increases the victim’s borrow balance and then liquidates them.


A second attack vector allows rogue borrowers to distort their accrued interest. They can call the `rebalanceFixedBorrowRate` function passing their account in the `_user` parameter, from an account with a very small borrow. This would effectively update their own `lastUpdateTimestamp` without accruing nearly as much interest as they should actually accrue.


To prevent malicious borrowers from exploiting this vulnerability, consider replacing `msg.sender` with `_user` as the argument passed to the `getUserBorrowBalances` function. Please note that this issue is closely tied to critical issue [**“[H09] Fixed-rate loans can be repeatedly rebalanced”**](#h09) and high severity issue [**“[H06] It is impossible to rebalance another account’s fixed borrow rate”**](#h06).


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

