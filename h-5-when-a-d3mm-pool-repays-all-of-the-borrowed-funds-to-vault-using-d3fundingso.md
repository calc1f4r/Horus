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
solodit_id: 20845
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/89
source_link: none
github_link: https://github.com/sherlock-audit/2023-06-dodo-judging/issues/217

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

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - Proxy
  - HALITUS
  - 0xkaden
  - skyge
  - seeques
---

## Vulnerability Title

H-5: When a D3MM pool repays all of the borrowed funds to vault using `D3Funding.sol repayAll`, an attacker can steal double the amount of those funds from vault

### Overview


This bug report is about an issue found in the D3MM pool contract. When a D3MM pool repays all of the borrowed funds to vault using the function D3Funding.sol repayAll, an attacker can steal double the amount of those funds from vault. This is because the balance of vault is not updated correctly in D3VaultFunding.sol _poolRepayAll.

The vault keeps a record of borrowed funds and its current token balance. The function _poolRepayAll() is supposed to decrease the borrowed funds by the repaid amount and increase the token balance by the same amount, but it is decreasing the token balance instead.

Let's say a vault has 100,000 USDC and a pool borrows 20,000 USDC from vault. When the pool calls `poolRepayAll()`, the asset info in vault will change as follows:

1. `totalBorrows => 20,000 - 20,000 => 0` // info.totalBorrows - amount
2. `balance => 100,000 - 20,000 => 80,000` // info.balance - amount
3. `tokens owned by vault => 100,000 + 20,000 => 120,000 USDC` // 20,000 USDC is transferred from pool to vault (repayment)
4. The difference of recorded balance (80,000) and actual balance (120,000) is `40,000 USDC` 

An attacker waits for the `poolRepayAll()` function call by a pool. When `poolRepayAll()` is executed, the attacker calls D3VaultFunding.sol userDeposit(), which deposits 40,000 USDC in vault on behalf of the attacker. After this, the attacker withdraws the deposited amount using D3VaultFunding.sol userWithdraw() and thus gains 40,000 USDC.

The impact of this vulnerability is a loss of funds from vault. The loss will be equal to 2x amount of borrowed tokens that a D3MM pool repays using D3VaultFunding.sol poolRepayAll.

The code snippet provided is D3VaultFunding.sol _poolRepayAll(). The tool used for discovery is manual review. The recommendation is to replace '-' with '+' in the code snippet. The bug was

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-06-dodo-judging/issues/217 

## Found by 
0x4db5362c, 0xG0P1, 0xkaden, HALITUS, Proxy, Sulpiride, dirk\_y, osmanozdemir1, seeques, skyge
## Summary

When a D3MM pool repays all of the borrowed funds to vault using [D3Funding.sol repayAll](https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/D3Pool/D3Funding.sol#L40-L46), an attacker can steal double the amount of those funds from vault. This is because the balance of vault is not updated correctly in [D3VaultFunding.sol _poolRepayAll](https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/D3Vault/D3VaultFunding.sol#L117-L133).

`amount` should be added in `info.balance` instead of being subtracted.

```solidity
    function _poolRepayAll(address pool, address token) internal {
        .
        .
        info.totalBorrows = info.totalBorrows - amount;
        info.balance = info.balance - amount; // amount should be added here
        .
        .
    }
```

## Vulnerability Detail
A `D3MM pool` can repay all of the borrowed funds from vault using the function [D3Funding.sol repayAll](https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/D3Pool/D3Funding.sol#L40-L46) which further calls [D3VaultFunding.sol poolRepayAll](https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/D3Vault/D3VaultFunding.sol#L113) and eventually [D3VaultFunding.sol _poolRepayAll](https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/D3Vault/D3VaultFunding.sol#L117-L133).

```solidity
    function repayAll(address token) external onlyOwner nonReentrant poolOngoing {
        ID3Vault(state._D3_VAULT_).poolRepayAll(token);
        _updateReserve(token);
        require(checkSafe(), Errors.NOT_SAFE);
    }
```

The vault keeps a record of borrowed funds and its current token balance.

`_poolRepayAll()` is supposed to:
1. Decrease the borrowed funds by the repaid amount
2. Increase the token balance by the same amount #vulnerability
3. Transfer the borrowed funds from pool to vault

However, `_poolRepayAll()` is decreasing the token balance instead.

```solidity
    function _poolRepayAll(address pool, address token) internal {
        .
        .
        .
        .

        info.totalBorrows = info.totalBorrows - amount;
        info.balance = info.balance - amount; // amount should be added here

        IERC20(token).safeTransferFrom(pool, address(this), amount);

        emit PoolRepay(pool, token, amount, interests);
    }
```
Let's say a vault has 100,000 USDC
A pool borrows 20,000 USDC from vault

When the pool calls `poolRepayAll()`, the asset info in vault will change as follows:

1. `totalBorrows => 20,000 - 20,000 => 0` // info.totalBorrows - amount
2. `balance => 100,000 - 20,000 => 80,000` // info.balance - amount
3. `tokens owned by vault => 100,000 + 20,000 => 120,000 USDC` // 20,000 USDC is transferred from pool to vault (repayment)
4. The difference of recorded balance (80,000) and actual balance (120,000) is `40,000 USDC` 

**An attacker waits for the `poolRepayAll()` function call by a pool.**

When `poolRepayAll()` is executed, the attacker calls [D3VaultFunding.sol userDeposit()](https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/D3Vault/D3VaultFunding.sol#L29), which deposits 40,000 USDC in vault on behalf of the attacker.

After this, the attacker withdraws the deposited amount using [D3VaultFunding.sol userWithdraw()](https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/D3Vault/D3VaultFunding.sol#L51) and thus gains 40,000 USDC.

```solidity
    function userDeposit(address user, address token) external nonReentrant allowedToken(token) {
        .
        .
        .
        AssetInfo storage info = assetInfo[token];
        uint256 realBalance = IERC20(token).balanceOf(address(this)); // check tokens owned by vault
        uint256 amount = realBalance - info.balance; // amount = 120000-80000
        .
        .
        .
        IDToken(info.dToken).mint(user, dTokenAmount);
        info.balance = realBalance;

        emit UserDeposit(user, token, amount);
    }
```

## Impact

Loss of funds from vault. 
The loss will be equal to 2x amount of borrowed tokens that a D3MM pool repays using [D3VaultFunding.sol poolRepayAll]()

## Code Snippet

[D3VaultFunding.sol _poolRepayAll()](https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/D3Vault/D3VaultFunding.sol#L129)

```solidity
    function _poolRepayAll(address pool, address token) internal {
        .
        .
        info.totalBorrows = info.totalBorrows - amount;
        info.balance = info.balance - amount; // vulnerability: amount should be added here

        IERC20(token).safeTransferFrom(pool, address(this), amount);

        emit PoolRepay(pool, token, amount, interests);
    }
```

## Tool used

Manual Review

## Recommendation
In [D3VaultFunding.sol _poolRepayAll](https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/D3Vault/D3VaultFunding.sol#L129), do the following changes:

Current code:
`info.balance = info.balance - amount;`

New (replace '-' with '+'):
`info.balance = info.balance + amount;`



## Discussion

**traceurl**

Fixed in this PR: https://github.com/DODOEX/new-dodo-v3/pull/26

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | DODO V3 |
| Report Date | N/A |
| Finders | Proxy, HALITUS, 0xkaden, skyge, seeques, Sulpiride, dirk\_y, 0xG0P1, 0x4db5362c, osmanozdemir1 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-06-dodo-judging/issues/217
- **Contest**: https://app.sherlock.xyz/audits/contests/89

### Keywords for Search

`vulnerability`

