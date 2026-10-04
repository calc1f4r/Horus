---
# Core Classification
protocol: Clave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46278
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/a9206360-7dc7-4e1e-9d5b-b52ad4561016
source_link: https://cdn.cantina.xyz/reports/cantina_clave_december2024.pdf
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
finders_count: 2
finders:
  - MiloTruck
  - Víctor Martínez
---

## Vulnerability Title

Using aToken.balanceOf() in ClaggAaveAdapter._compoundAccounting() allows for inﬂation at- tacks 

### Overview


This bug report discusses an issue with the ClaggAaveAdapter and ClaggBaseAdapter contracts. When the compound() function is called, it sets the totalLiquidity of the pool to the current aToken balance of the contract. This allows an attacker to perform an inflation attack by directly donating aTokens to the contract. This means that the attacker can manipulate the totalLiquidity and totalSupply values, causing other users to lose their shares. The recommendation is to add "dead" shares to the totalSupply on the first deposit to prevent this attack. This has been fixed in a recent commit. The report has been verified and 10,000 "dead" shares are now minted on the first deposit.

### Original Finding Content

## Context
ClaggAaveAdapter.sol#L98-L102, ClaggBaseAdapter.sol#L559-L563

## Description
When `compound()` is called, `ClaggAaveAdapter._compoundAccounting()` sets `totalLiquidity`
of the pool to the current aToken balance of the contract:

```solidity
function _compoundAccounting(address pool, uint256) internal override {
    PoolInfo storage poolInfo = _getPoolInfo(pool);
    poolInfo.totalLiquidity = IERC20(pool).balanceOf(address(this));
}
```

However, this allows an attacker to perform an inflation attack by directly donating aTokens to the contract. For example:

- `ClaggAaveAdapter` is newly deployed and has no deposits yet.
- Attacker deposits 1 wei of asset:
  - 1 wei of aToken is minted.
  - `totalLiquidity = 1` and `totalSupply = 1`.
- Attacker directly transfers `100e18` of aToken to the contract.
- Attacker calls `compound()`:
  - `totalLiquidity = 100e18 + 1`.
- Afterwards, a user calls `deposit()` to deposit `10e18` of assets:
  - `10e18 aToken` is minted.
  - In `_liquidityToShare()`, the amount of shares to mint is calculated as `liquidity * totalSupply / totalLiquidity = 10e18 * 1 / 100e18`, which rounds down to 0.
  - User receives no shares for his deposit.

In the example above, the `10e18` of assets deposited by the user accrues to the attacker's 1 share.

## Recommendation
OpenZeppelin has a writeup on defending against such attacks (see their blog post on ERC4626 inflation attacks).

Consider adding "dead" shares to `totalSupply` on the first deposit in `ClaggBaseAdapter._depositAccounting()` as such:

```solidity
// If pool is empty, shares = liquidity (1:1 ratio)
if (poolInfo.totalSupply == 0) {
    shares = liquidity;
    poolInfo.totalLiquidity = liquidity;
    + poolInfo.totalSupply = 1e6;
} else {
```

The downsides to this are:
1. The first depositor loses a tiny portion of his deposit, since they accrue to the 1e6 dead shares.
2. The shares to liquidity ratio will never be 1:1.
3. A small portion of all future gains (from incentives or compounding rewards) will always accrue to these dead shares.

Alternatively, `ClaggAaveAdapter` could be refactored to use the scaled balance of aTokens instead.

## Clave
Fixed in commit `cc4ff057`.

## Cantina Managed
Verified, `1e4` "dead" shares are now minted on the first deposit.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Clave |
| Report Date | N/A |
| Finders | MiloTruck, Víctor Martínez |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_clave_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/a9206360-7dc7-4e1e-9d5b-b52ad4561016

### Keywords for Search

`vulnerability`

