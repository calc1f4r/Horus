---
# Core Classification
protocol: Burve
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56951
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/858
source_link: none
github_link: https://github.com/sherlock-audit/2025-04-burve-judging/issues/113

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
finders_count: 4
finders:
  - newspacexyz
  - h2134
  - Ziusz
  - bretzel
---

## Vulnerability Title

H-2: Incorrect implementation of `ERC4626ViewAdjustor`

### Overview


This bug report discusses an issue with the implementation of the `ERC4626ViewAdjustor` contract, which is used for converting between real and nominal values of a token. The code for the functions `toNominal` and `toReal` is reversed, causing users to deposit more than they should in certain situations. The root cause of the issue is in the `ERC4626ViewAdjustor` contract, and the fix is to reverse the implementation of these functions. The impact of this bug is a loss of funds for users. The protocol team has already fixed the issue in their code.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-04-burve-judging/issues/113 

## Found by 
Ziusz, bretzel, h2134, newspacexyz

### Summary

Adjustor contracts have 2 main functions which are `toNominal` and `toReal`, which convert between real and nominal values of a token.

`ERC4626ViewAdjustor` is an implementation for LSTs such as `stETH`.
However, the implementation of `toNominal` and `toReal` is incorrect within this contract. Here's code snippets:

```solidity
    function toNominal(
        address token,
        uint256 real,
        bool
    ) external view returns (uint256 nominal) {
        IERC4626 vault = getVault(token);
        return vault.convertToShares(real);
    }

    function toReal(
        address token,
        uint256 nominal,
        bool
    ) external view returns (uint256 real) {
        IERC4626 vault = getVault(token);
        return vault.convertToAssets(nominal);
    }
```

The goal of `toNominal` is to convert a real value to a nominal value, such as converting `stETH` balance in `ETH`.
In vice versa, `toReal` is to convert a nominal value to a real value, such as converting `ETH` to `stETH`.

But as shown in the code snippets above, the implementation of `toNominal` and `toReal` is reversed, as `toNominal` is using `convertToShares` and `toReal` is using `convertToAssets`.

### Root Cause

The root cause of the issue is in [`ERC4626ViewAdjustor`](https://github.com/sherlock-audit/2025-04-burve/blob/44cba36e2a0c3cd7b6999459bf7746db92f8cc0a/Burve/src/integrations/adjustor/E4626ViewAdjustor.sol#L29-L71) contract where the implementation of `toNominal` and `toReal` is reversed.

### Internal Pre-conditions

One of LSTs is used in multi-token pool with `ERC4626ViewAdjustor` as the adjustor.

### External Pre-conditions

None

### Attack Path

- Assume, `stETH` and `WETH` are used in the pool, and `1 stETH = 1.1 WETH`.
- Alice adds 100 value worth of tokens to the pool, which eventually will require 100 `WETH` and 100 `WETH` worth of `stETH`.
- However, as `toReal` function which is used to calculate the amount of `stETH` uses `convertToAssets`, the amount of `stETH` to deposit becomes `110 stETH` instead of `100/1.1 stETH`.

### Impact

Loss of funds for users as they deposit more than they should.

### PoC

_No response_

### Mitigation

The fix is to reverse the implementation of `toNominal` and `toReal` in `ERC4626ViewAdjustor` contract.

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/itos-finance/Burve/commit/c14995d806cdabc20bfedb094d585ed7b8668c8c

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Burve |
| Report Date | N/A |
| Finders | newspacexyz, h2134, Ziusz, bretzel |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-04-burve-judging/issues/113
- **Contest**: https://app.sherlock.xyz/audits/contests/858

### Keywords for Search

`vulnerability`

