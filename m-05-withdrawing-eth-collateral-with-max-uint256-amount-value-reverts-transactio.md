---
# Core Classification
protocol: Sturdy
chain: everychain
category: uncategorized
vulnerability_type: decimals

# Attack Vector Details
attack_type: decimals
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2338
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-sturdy-contest
source_link: https://code4rena.com/reports/2022-05-sturdy
github_link: https://github.com/code-423n4/2022-05-sturdy-findings/issues/85

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:
  - decimals

protocol_categories:
  - liquid_staking
  - lending
  - bridge
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - WatchPug
  - berndartmueller
---

## Vulnerability Title

[M-05] Withdrawing ETH collateral with max uint256 amount value reverts transaction

### Overview


This bug report focuses on a vulnerability found in the `withdrawCollateral` function of the GeneralVault smart contract. The vulnerability occurs when `type(uint256).max` is used for the `_amount` parameter and `_asset` is the zero-address. This causes the transaction to revert because `IERC20Detailed(_asset).decimals()` does not work for native ETH. Manual review was used to identify this vulnerability. The recommended mitigation step is to check `_asset` and use a hard coded decimal value of 18 for native ETH.

### Original Finding Content

_Submitted by berndartmueller, also found by WatchPug_

Withdrawing ETH collateral via the `withdrawCollateral` function using `type(uint256).max` for the `_amount` parameter reverts the transaction due to `_asset` being the zero-address and `IERC20Detailed(_asset).decimals()` not working for native ETH.

#### Proof of Concept

[GeneralVault.sol#L121-L124](https://github.com/code-423n4/2022-05-sturdy/blob/78f51a7a74ebe8adfd055bdbaedfddc05632566f/smart-contracts/GeneralVault.sol#L121-L124)

```solidity
if (_amount == type(uint256).max) {
    uint256 decimal = IERC20Detailed(_asset).decimals(); // @audit-info does not work for native ETH. Transaction reverts
    _amount = _amountToWithdraw.mul(this.pricePerShare()).div(10**decimal);
}
```

### Recommended mitigation steps

Check `_asset` and use hard coded decimal value (`18`) for native ETH.

**[sforman2000 (Sturdy) confirmed](https://github.com/code-423n4/2022-05-sturdy-findings/issues/85)**

**[atozICT20 (Sturdy) commented](https://github.com/code-423n4/2022-05-sturdy-findings/issues/85):**
 > [Fix the issue of transaction fails due to calculate ETH's decimals sturdyfi/code4rena-may-2022#7](https://github.com/sturdyfi/code4rena-may-2022/pull/7)

**[hickuphh3 (judge) commented](https://github.com/code-423n4/2022-05-sturdy-findings/issues/85#issuecomment-1145575544):**
 > Good find! Stated in `_asset` description that null address is interpreted as ETH, which isn't a token, and therefore reverts when attempting to fetch its decimals.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Sturdy |
| Report Date | N/A |
| Finders | WatchPug, berndartmueller |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-sturdy
- **GitHub**: https://github.com/code-423n4/2022-05-sturdy-findings/issues/85
- **Contest**: https://code4rena.com/contests/2022-05-sturdy-contest

### Keywords for Search

`Decimals`

