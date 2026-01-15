---
# Core Classification
protocol: Sublime
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1735
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-sublime-contest
source_link: https://code4rena.com/reports/2022-03-sublime
github_link: https://github.com/code-423n4/2022-03-sublime-findings/issues/21

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.20
financial_impact: high

# Scoring
quality_score: 1
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - leveraged_farming
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - hickuphh3
  - rayn  WatchPug
---

## Vulnerability Title

[H-02] `PooledCreditLine`: termination likely fails because `_principleWithdrawable` is treated as shares

### Overview


A bug was found in the LenderPool.sol contract, which is part of the Sublime Finance project. This bug can be found in lines 404-406 of the contract. The bug causes the `_principalWithdrawable` variable to be denominated in the borrowAsset, but it is then treated as the share amount to be withdrawn. This bug can have a significant impact on the project and should be fixed.

The recommended mitigation steps are to use `_sharesHeld` as the amount of shares to withdraw, instead of `_principalWithdrawable`. However, it is important to note that `terminate()` should only be called when the credit line is `ACTIVE` or `EXPIRED`, as `_sharesHeld` excludes principal withdrawals. The code for this can be seen below.

```jsx
function terminate(uint256 _id, address _to) external override onlyPooledCreditLine nonReentrant {
  address _strategy = pooledCLConstants[_id].borrowAssetStrategy;
  address _borrowAsset = pooledCLConstants[_id].borrowAsset;
  uint256 _sharesHeld = pooledCLVariables[_id].sharesHeld;

  SAVINGS_ACCOUNT.withdrawShares(_borrowAsset, _strategy, _to, _sharesHeld, false);
  delete pooledCLConstants[_id];
  delete pooledCLVariables[_id];
}
```

In summary, a bug was found in the LenderPool.sol contract of the Sublime Finance project, which can have a significant impact. The bug causes the `_principalWithdrawable` variable to be denominated in the borrowAsset, but it is then treated as the share amount to be withdrawn. The recommended mitigation steps are to use `_sharesHeld` as the amount of shares to withdraw, but it is important to ensure that `terminate()` is only called when the credit line is `ACTIVE` or `EXPIRED`.

### Original Finding Content

_Submitted by hickuphh3, also found by rayn and WatchPug_

[LenderPool.sol#L404-L406](https://github.com/sublime-finance/sublime-v1/blob/46536a6d25df4264c1b217bd3232af30355dcb95/contracts/PooledCreditLine/LenderPool.sol#L404-L406)<br>

`_principalWithdrawable` is denominated in the borrowAsset, but subsequently treats it as the share amount to be withdrawn.

```jsx
// _notBorrowed = borrowAsset amount that isn't borrowed
// totalSupply[_id] = ERC1155 total supply of _id
// _borrowedTokens = borrower's specified borrowLimit
uint256 _principalWithdrawable = _notBorrowed.mul(totalSupply[_id]).div(_borrowedTokens);

SAVINGS_ACCOUNT.withdrawShares(_borrowAsset, _strategy, _to, _principalWithdrawable.add(_totalInterestInShares), false);
```

### Recommended Mitigation Steps

The amount of shares to withdraw can simply be `_sharesHeld`.

Note that this comes with the assumption that `terminate()` is only called when the credit line is `ACTIVE` or `EXPIRED` (consider ensuring this condition on-chain), because `_sharesHeld` **excludes principal withdrawals,** so the function will fail once a lender withdraws his principal.

```jsx
function terminate(uint256 _id, address _to) external override onlyPooledCreditLine nonReentrant {
  address _strategy = pooledCLConstants[_id].borrowAssetStrategy;
  address _borrowAsset = pooledCLConstants[_id].borrowAsset;
  uint256 _sharesHeld = pooledCLVariables[_id].sharesHeld;

  SAVINGS_ACCOUNT.withdrawShares(_borrowAsset, _strategy, _to, _sharesHeld, false);
  delete pooledCLConstants[_id];
  delete pooledCLVariables[_id];
}
```

**[ritik99 (Sublime) confirmed](https://github.com/code-423n4/2022-03-sublime-findings/issues/21)**



***
 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 1/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sublime |
| Report Date | N/A |
| Finders | hickuphh3, rayn  WatchPug |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-sublime
- **GitHub**: https://github.com/code-423n4/2022-03-sublime-findings/issues/21
- **Contest**: https://code4rena.com/contests/2022-03-sublime-contest

### Keywords for Search

`vulnerability`

