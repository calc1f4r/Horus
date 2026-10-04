---
# Core Classification
protocol: g8keep_2024-12-12
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45308
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/g8keep-security-review_2024-12-12.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-03] It's possible to add liquidity to UniswapV3 while token is not migrated

### Overview


The reported bug is of high severity and has a medium likelihood of occurring. The issue is that the code does not prevent the transfer of tokens to the UniswapV3 pool before they have been migrated. This allows an attacker to add liquidity to the pool and manipulate its balance. The attacker can use the `buy(to)` function to buy tokens for the Uniswap V3 pool address, which increases the pool's token balance. When adding liquidity, the code expects the tokens to be transferred to the pool's address, but the attacker's contract can bypass this and call `mint()` to add liquidity and then call `buy(pool)` to further increase the pool's balance. This can cause the migration process to be disrupted and also manipulate the token price during the migration. The recommendation is to prevent the buying of tokens for the pool's address.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

Code won't allow to transfer of tokens to the UniswapV3 pool when the token hasn't migrated yet so no one could add liquidity to the pool and manipulate the pool. The issue is that it's possible to bypass these checks and add liquidity to the Uniswap pool. The attacker can use `buy(to)` function to buy tokens for the Uniswap V3 pool address and increase the pool's token balance. When adding liquidity to Uniswap V3, it calls `uniswapV3MintCallback()` and expects that function to transfer the tokens to the pool's address:

```solidity
        if (amount0 > 0) balance0Before = balance0();
        if (amount1 > 0) balance1Before = balance1();
        IUniswapV3MintCallback(msg.sender).uniswapV3MintCallback(amount0, amount1, data);
        if (amount0 > 0) require(balance0Before.add(amount0) <= balance0(), 'M0');
        if (amount1 > 0) require(balance1Before.add(amount1) <= balance1(), 'M1');
```

The attacker's contract can call `mint()` to add liquidity to the pool and during the `uniswapV3MintCallback()` callback it would call `buy(pool)` to increase the pool's balance and as a result, Uniswap V3 pool's liquidity would increase. By performing this attacker can DOS the migration process and also manipulate the token price during the migration.

## Recommendations

Won't allow buying tokens for the pool's address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | g8keep_2024-12-12 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/g8keep-security-review_2024-12-12.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

