---
# Core Classification
protocol: DODO V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20850
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/89
source_link: none
github_link: https://github.com/sherlock-audit/2023-06-dodo-judging/issues/85

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

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Avci
  - BugHunter101
  - 0xDjango
  - dirk\_y
  - Oxhunter526
---

## Vulnerability Title

M-3: `D3VaultFunding.userWithdraw()` doen not have mindTokenAmount

### Overview


This bug report is about a vulnerability in the `D3VaultFunding.userWithdraw()` function in the D3Vault contract. The function does not have a minimum token amount parameter and uses `_getExchangeRate` directly. This is vulnerable to a sandwich attack, which can lead to huge slippage. The code snippet for the bug can be found at https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/D3Vault/D3VaultFunding.sol#L56. This vulnerability was found by 0xDjango, Avci, BugHunter101, Oxhunter526, and dirk\_y. 

The recommended solution to this vulnerability is to add a `mindTokenAmount` parameter for the `userWithdraw()` function and check if `amount < mindTokenAmount`. Attens1423 suggested adding slippage protection in D3Proxy.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-06-dodo-judging/issues/85 

## Found by 
0xDjango, Avci, BugHunter101, Oxhunter526, dirk\_y
## Summary

`D3VaultFunding.userWithdraw()` doen not have mindTokenAmount, and use `_getExchangeRate` directly.This is vulnerable to a sandwich attack.

## Vulnerability Detail

As we can see, `D3VaultFunding.userWithdraw()` doen not have mindTokenAmount, and use `_getExchangeRate` directly.
```solidity
function userWithdraw(address to, address user, address token, uint256 dTokenAmount) external nonReentrant allowedToken(token) returns(uint256 amount) {
        accrueInterest(token);
        AssetInfo storage info = assetInfo[token];
        require(dTokenAmount <= IDToken(info.dToken).balanceOf(msg.sender), Errors.DTOKEN_BALANCE_NOT_ENOUGH);

        amount = dTokenAmount.mul(_getExchangeRate(token));//@audit does not check amount value
        IDToken(info.dToken).burn(msg.sender, dTokenAmount);
        IERC20(token).safeTransfer(to, amount);
        info.balance = info.balance - amount;

        // used for calculate user withdraw amount
        // this function could be called from d3Proxy, so we need "user" param
        // In the meantime, some users may hope to use this function directly,
        // to prevent these users fill "user" param with wrong addresses,
        // we use "msg.sender" param to check.
        emit UserWithdraw(msg.sender, user, token, amount);
    }
```

 And the `_getExchangeRate()` result is about `cash `, `info.totalBorrows`, `info.totalReserves`,`info.withdrawnReserves`,`dTokenSupply`,This is vulnerable to a sandwich attack leading to huge slippage
```solidity
function _getExchangeRate(address token) internal view returns (uint256) {
        AssetInfo storage info = assetInfo[token];
        uint256 cash = getCash(token);
        uint256 dTokenSupply = IERC20(info.dToken).totalSupply();
        if (dTokenSupply == 0) { return 1e18; }
        return (cash + info.totalBorrows - (info.totalReserves - info.withdrawnReserves)).div(dTokenSupply);
    } 
```

## Impact

This is vulnerable to a sandwich attack.

## Code Snippet

https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/D3Vault/D3VaultFunding.sol#L56

## Tool used

Manual Review

## Recommendation

Add `mindTokenAmount` parameter for `userWithdraw()` function and check if `amount < mindTokenAmount`



## Discussion

**Attens1423**

We will add slippage protection in D3Proxy

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | DODO V3 |
| Report Date | N/A |
| Finders | Avci, BugHunter101, 0xDjango, dirk\_y, Oxhunter526 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-06-dodo-judging/issues/85
- **Contest**: https://app.sherlock.xyz/audits/contests/89

### Keywords for Search

`vulnerability`

