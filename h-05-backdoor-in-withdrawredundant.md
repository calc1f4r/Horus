---
# Core Classification
protocol: InsureDAO
chain: everychain
category: uncategorized
vulnerability_type: admin

# Attack Vector Details
attack_type: admin
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1298
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-insuredao-contest
source_link: https://code4rena.com/reports/2022-01-insure
github_link: https://github.com/code-423n4/2022-01-insure-findings/issues/252

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 2

# Context Tags
tags:
  - admin

protocol_categories:
  - services
  - cross_chain
  - indexes
  - insurance

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - WatchPug
  - camden
  - Ruhum
  - cmichel
---

## Vulnerability Title

[H-05] backdoor in withdrawRedundant

### Overview


A bug report has been submitted by user cmichel for the `Vault.withdrawRedundant` function in a smart contract. This function has a wrong logic that allows the admins to steal the underlying vault token. When the `Vault.addValue` is called, the `balance` increases by `_amount` as well as the actual `IERC20(token).balanceOf(this)`. If the admins call `vault.withdrawRedundant(vault.token(), attacker)`, it will transfer out all `vault.token()` amounts to the attacker due to the balance inequality condition being `false`. This creates a backdoor in the `withdrawRedundant` function that allows admins to steal all user deposits.

The recommended mitigation step is to change the code to the following:

```solidity
function withdrawRedundant(address _token, address _to)
     external
     override
     onlyOwner
{
     if (
          _token == address(token)
     ) {
          if (balance < IERC20(token).balanceOf(address(this))) {
               uint256 _redundant = IERC20(token).balanceOf(address(this)) -
                    balance;
               IERC20(token).safeTransfer(_to, _redundant);
          }
     } else if (IERC20(_token).balanceOf(address(this)) > 0) {
          IERC20(_token).safeTransfer(
               _to,
               IERC20(_token).balanceOf(address(this))
          );
     }
}
```

This will ensure that the admins cannot steal the underlying vault token and the user deposits will remain secure.

### Original Finding Content

## Handle

cmichel


## Vulnerability details

The `Vault.withdrawRedundant` has wrong logic that allows the admins to steal the underlying vault token.

```solidity
function withdrawRedundant(address _token, address _to)
     external
     override
     onlyOwner
{
     if (
          _token == address(token) &&
          balance < IERC20(token).balanceOf(address(this))
     ) {
          uint256 _redundant = IERC20(token).balanceOf(address(this)) -
               balance;
          IERC20(token).safeTransfer(_to, _redundant);
     } else if (IERC20(_token).balanceOf(address(this)) > 0) {
          // @audit they can rug users. let's say balance == IERC20(token).balanceOf(address(this)) => first if false => transfers out everything
          IERC20(_token).safeTransfer(
               _to,
               IERC20(_token).balanceOf(address(this))
          );
     }
}
```

#### POC
- Vault deposits increase as `Vault.addValue` is called and the `balance` increases by `_amount` as well as the actual `IERC20(token).balanceOf(this)`. Note that `balance == IERC20(token).balanceOf(this)`
- Admins call `vault.withdrawRedundant(vault.token(), attacker)` which goes into the `else if` branch due to the balance inequality condition being `false`. It will transfer out all `vault.token()` amounts to the attacker.

## Impact
There's a backdoor in the `withdrawRedundant` that allows admins to steal all user deposits.

## Recommended Mitigation Steps
I think the devs wanted this logic from the code instead:

```solidity
function withdrawRedundant(address _token, address _to)
     external
     override
     onlyOwner
{
     if (
          _token == address(token)
     ) {
          if (balance < IERC20(token).balanceOf(address(this))) {
               uint256 _redundant = IERC20(token).balanceOf(address(this)) -
                    balance;
               IERC20(token).safeTransfer(_to, _redundant);
          }
     } else if (IERC20(_token).balanceOf(address(this)) > 0) {
          IERC20(_token).safeTransfer(
               _to,
               IERC20(_token).balanceOf(address(this))
          );
     }
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 2/5 |
| Audit Firm | Code4rena |
| Protocol | InsureDAO |
| Report Date | N/A |
| Finders | WatchPug, camden, Ruhum, cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-insure
- **GitHub**: https://github.com/code-423n4/2022-01-insure-findings/issues/252
- **Contest**: https://code4rena.com/contests/2022-01-insuredao-contest

### Keywords for Search

`Admin`

